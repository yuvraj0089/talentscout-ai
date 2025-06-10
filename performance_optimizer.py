"""
Performance Optimization Module for TalentScout
Handles caching, async operations, and performance monitoring
"""

import asyncio
import time
import functools
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
import streamlit as st
import threading
from concurrent.futures import ThreadPoolExecutor
import queue

class PerformanceOptimizer:
    """Handles performance optimization for the TalentScout application."""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {}
        self.performance_metrics = {}
        self.request_queue = queue.Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.response_cache_duration = 300  # 5 minutes
        
    def timed_cache(self, ttl_seconds: int = 300):
        """Decorator for caching function results with TTL."""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                cache_key = f"{func.__name__}_{hash(str(args) + str(sorted(kwargs.items())))}"
                
                # Check if cached result exists and is still valid
                if cache_key in self.cache:
                    if datetime.now() < self.cache_ttl[cache_key]:
                        return self.cache[cache_key]
                    else:
                        # Remove expired cache entry
                        del self.cache[cache_key]
                        del self.cache_ttl[cache_key]
                
                # Execute function and cache result
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Store in cache with TTL
                self.cache[cache_key] = result
                self.cache_ttl[cache_key] = datetime.now() + timedelta(seconds=ttl_seconds)
                
                # Record performance metrics
                self.record_performance_metric(func.__name__, execution_time)
                
                return result
            return wrapper
        return decorator
    
    def async_wrapper(self, func: Callable) -> Callable:
        """Wrapper to run synchronous functions asynchronously."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.thread_pool.submit(func, *args, **kwargs)
        return wrapper
    
    def record_performance_metric(self, operation: str, execution_time: float):
        """Record performance metrics for monitoring."""
        if operation not in self.performance_metrics:
            self.performance_metrics[operation] = {
                'total_calls': 0,
                'total_time': 0.0,
                'avg_time': 0.0,
                'min_time': float('inf'),
                'max_time': 0.0,
                'last_call': None
            }
        
        metrics = self.performance_metrics[operation]
        metrics['total_calls'] += 1
        metrics['total_time'] += execution_time
        metrics['avg_time'] = metrics['total_time'] / metrics['total_calls']
        metrics['min_time'] = min(metrics['min_time'], execution_time)
        metrics['max_time'] = max(metrics['max_time'], execution_time)
        metrics['last_call'] = datetime.now()
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report."""
        return {
            'cache_size': len(self.cache),
            'cache_hit_ratio': self.calculate_cache_hit_ratio(),
            'operations': self.performance_metrics.copy(),
            'memory_usage': self.estimate_memory_usage()
        }
    
    def calculate_cache_hit_ratio(self) -> float:
        """Calculate cache hit ratio."""
        total_operations = sum(
            metrics['total_calls'] 
            for metrics in self.performance_metrics.values()
        )
        
        if total_operations == 0:
            return 0.0
        
        # Estimate cache hits (simplified calculation)
        cache_operations = len(self.cache)
        return min(cache_operations / total_operations, 1.0)
    
    def estimate_memory_usage(self) -> Dict[str, int]:
        """Estimate memory usage of cached data."""
        import sys
        
        cache_size = sum(sys.getsizeof(value) for value in self.cache.values())
        metrics_size = sys.getsizeof(self.performance_metrics)
        
        return {
            'cache_bytes': cache_size,
            'metrics_bytes': metrics_size,
            'total_bytes': cache_size + metrics_size
        }
    
    def cleanup_expired_cache(self):
        """Clean up expired cache entries."""
        current_time = datetime.now()
        expired_keys = [
            key for key, expiry_time in self.cache_ttl.items()
            if current_time >= expiry_time
        ]
        
        for key in expired_keys:
            del self.cache[key]
            del self.cache_ttl[key]
        
        return len(expired_keys)
    
    def preload_common_responses(self):
        """Preload common responses to improve performance."""
        common_tech_stacks = [
            ['Python', 'JavaScript', 'React'],
            ['Java', 'Spring', 'MySQL'],
            ['Python', 'Django', 'PostgreSQL'],
            ['JavaScript', 'Node.js', 'MongoDB'],
            ['C#', '.NET', 'SQL Server']
        ]
        
        # Preload fallback questions for common tech stacks
        for tech_stack in common_tech_stacks:
            try:
                from utils import get_fallback_questions
                self.cache[f"fallback_questions_{hash(str(tech_stack))}"] = get_fallback_questions(tech_stack)
                self.cache_ttl[f"fallback_questions_{hash(str(tech_stack))}"] = datetime.now() + timedelta(hours=24)
            except ImportError:
                pass
    
    def batch_process_requests(self, requests: List[Callable], max_concurrent: int = 3) -> List[Any]:
        """Process multiple requests concurrently."""
        results = []
        
        # Split requests into batches
        for i in range(0, len(requests), max_concurrent):
            batch = requests[i:i + max_concurrent]
            
            # Submit batch to thread pool
            futures = [self.thread_pool.submit(request) for request in batch]
            
            # Collect results
            for future in futures:
                try:
                    result = future.result(timeout=30)  # 30 second timeout
                    results.append(result)
                except Exception as e:
                    results.append(f"Error: {e}")
        
        return results
    
    def optimize_streamlit_performance(self):
        """Apply Streamlit-specific performance optimizations."""
        # Configure Streamlit caching
        if 'performance_optimizer_initialized' not in st.session_state:
            st.session_state.performance_optimizer_initialized = True
            
            # Set up periodic cache cleanup
            if 'last_cache_cleanup' not in st.session_state:
                st.session_state.last_cache_cleanup = datetime.now()
            
            # Clean up cache every 10 minutes
            if datetime.now() - st.session_state.last_cache_cleanup > timedelta(minutes=10):
                cleaned_entries = self.cleanup_expired_cache()
                st.session_state.last_cache_cleanup = datetime.now()
                if cleaned_entries > 0:
                    st.sidebar.success(f"Cleaned {cleaned_entries} expired cache entries")
    
    def create_performance_dashboard(self):
        """Create performance monitoring dashboard."""
        st.sidebar.subheader("⚡ Performance Monitor")
        
        report = self.get_performance_report()
        
        # Cache statistics
        st.sidebar.metric("Cache Size", report['cache_size'])
        st.sidebar.metric("Cache Hit Ratio", f"{report['cache_hit_ratio']:.2%}")
        
        # Memory usage
        memory = report['memory_usage']
        memory_mb = memory['total_bytes'] / (1024 * 1024)
        st.sidebar.metric("Memory Usage", f"{memory_mb:.2f} MB")
        
        # Operation performance
        if report['operations']:
            with st.sidebar.expander("Operation Performance"):
                for op_name, metrics in report['operations'].items():
                    st.write(f"**{op_name}**")
                    st.write(f"Avg Time: {metrics['avg_time']:.3f}s")
                    st.write(f"Total Calls: {metrics['total_calls']}")
                    st.write("---")
        
        # Performance controls
        if st.sidebar.button("Clear Cache"):
            self.cache.clear()
            self.cache_ttl.clear()
            st.sidebar.success("Cache cleared!")
        
        if st.sidebar.button("Preload Common Data"):
            self.preload_common_responses()
            st.sidebar.success("Common data preloaded!")

class AsyncOperationManager:
    """Manages asynchronous operations for better responsiveness."""
    
    def __init__(self):
        self.pending_operations = {}
        self.completed_operations = {}
    
    async def generate_questions_async(self, tech_stack: List[str]) -> List[str]:
        """Generate technical questions asynchronously."""
        try:
            from utils import generate_technical_questions
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            questions = await loop.run_in_executor(
                None, 
                generate_technical_questions, 
                tech_stack
            )
            return questions
        except Exception as e:
            # Fallback to synchronous operation
            from utils import get_fallback_questions
            return get_fallback_questions(tech_stack)
    
    async def analyze_sentiment_async(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment asynchronously."""
        try:
            from sentiment_analyzer import sentiment_analyzer
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                sentiment_analyzer.analyze_sentiment,
                text
            )
            return result
        except Exception as e:
            return {'error': str(e), 'emotion': 'neutral', 'polarity': 0.0}
    
    def start_background_operation(self, operation_id: str, operation: Callable, *args, **kwargs):
        """Start a background operation."""
        future = asyncio.create_task(operation(*args, **kwargs))
        self.pending_operations[operation_id] = future
        return operation_id
    
    def check_operation_status(self, operation_id: str) -> Dict[str, Any]:
        """Check the status of a background operation."""
        if operation_id in self.completed_operations:
            return {
                'status': 'completed',
                'result': self.completed_operations[operation_id]
            }
        elif operation_id in self.pending_operations:
            future = self.pending_operations[operation_id]
            if future.done():
                try:
                    result = future.result()
                    self.completed_operations[operation_id] = result
                    del self.pending_operations[operation_id]
                    return {
                        'status': 'completed',
                        'result': result
                    }
                except Exception as e:
                    del self.pending_operations[operation_id]
                    return {
                        'status': 'error',
                        'error': str(e)
                    }
            else:
                return {'status': 'pending'}
        else:
            return {'status': 'not_found'}

# Global instances
performance_optimizer = PerformanceOptimizer()
async_manager = AsyncOperationManager()
