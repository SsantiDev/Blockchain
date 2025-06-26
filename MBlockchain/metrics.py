import time
import functools
import threading
import json
import statistics
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, deque

@dataclass
class MetricData:
    """
    Class to hold individual metric data.
    It includes the name, value, timestamp, metadata, and category of the metric.
    """
    name: str
    value: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    category: str = "general"
    
    
@dataclass
class AggregatedMetrics:
    """
    Class to hold aggregated metrics for a specific metric name.
    It includes count, total, average, minimum, maximum, and recent values.
    """
    count: int = 0
    total: float = 0.0
    avg: float = 0.0
    min: float = float('inf')
    max: float = 0.0
    recent_values: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def update(self, value: float) -> None:
        """
        Update the aggregated metrics with a new value.
        
        Args:
            value (float): The new value to update the metrics with.
        """
        self.count += 1
        self.total += value
        self.avg = self.total / self.count
        self.min = min(self.min, value)
        self.max = max(self.max, value)
        self.recent_values.append(value)
        
class MetricsCollector:
    def __init__(self, max_history: int = 10000):
        """
        Initialize the MetricsCollector with a maximum history size.
        
        Args:
            max_history (int): Maximum number of historical metrics to keep.
        """
        self._metrics: list[MetricData] = []
        self._aggregated: Dict[str, AggregatedMetrics] = defaultdict(AggregatedMetrics)
        self._max_history = max_history
        self._lock = threading.Lock()
        
        
        #metrics specific to the blockchain
        self.mining_times: List[float] = []
        self.validation_times: List[float] = []
        self.nonce_iteracions: List[int] = []
        
    def add_metric(self, name: str, value: float, category: str = "general", **metadata):
        """
        Add a new metric to the collector.
        
        Args:
            name (str): The name of the metric.
            value (float): The value of the metric.
            category (str): The category of the metric, default is "general".
            **metadata: Additional metadata for the metric.
        """
        with self._lock:
            metric = MetricData(
                name=name,
                value=value,
                timestamp=datetime.now(),
                metadata=metadata,
                category=category
            )
            
            self._metrics.append(metric)
            self._aggregated[name].update(value)
            
            if len(self._metrics) > self._max_history:
                self._metrics = self._metrics[-self._max_history:]  # Keep only the last max_history metrics
                
                
    def get_stats(self, metric_name: str) -> Dict[str, Any]:
        """
        Get statistics for a specific metric.
        Args:
            metric_name (str): The name of the metric to get statistics for.
        Returns:
            Dict[str, Any]: A dictionary containing the statistics for the metric.
        """
        if metric_name not in self._aggregated:
            return{}
        
        agg = self._aggregated[metric_name]
        recent = list(agg.recent_values)
        
        stats ={
            "count": agg.count,
            "total": agg.total,
            "average": agg.avg,
            "min": agg.min,
            "max": agg.max,
        }
        
        if recent:
            stats.update({
                "median": statistics.median(recent),
                "std_dev": statistics.stdev(recent) if len(recent) > 1 else 0,
                "recent_avg": sum(recent) / len(recent),
                "p95": statistics.quantiles(recent, n=20)[18] if len(recent) >= 20 else None,
            }) 
            
        return stats
    
    
    def get_blockchain_reports(self) -> Dict[str, Any]:
        """
        Get a report of the blockchain-specific metrics.
        
        Returns:
            Dict[str, Any]: A dictionary containing the blockchain metrics.
        """
        return {
            "mining": self.get_stats("mining_time"),
            "validation": self.get_stats("validation_time"),
            "nonce_iterations": self.get_stats("nonce_iterations"),
            "difficulty_adjustment": self.get_stats("difficulty_adjustment"),
            "block_creation": self.get_stats("block_creation_time"),
            "chain_validation": self.get_stats("chain_validation_time"),
            "attack_simulation": self.get_stats("attack_simulation_time"),
            "timestamp": datetime.now().isoformat(),
            "total_metrics": len(self._metrics),
        }
        
    def export_metrics(self, filename: str = None) -> str:
        """
        Export the collected metrics to a JSON string or file.
        
        Args:
            filename (str): Optional filename to save the metrics to. If None, returns JSON string.
        
        Returns:
            str: JSON string containing the metrics data.
            If a filename is provided, the data is saved to that file instead.
        """
        data = {
            "report": self.get_blockchain_reports(),
            "raw_metrics": [
                {
                    "name": m.name,
                    "value": m.value,
                    "timestamp": m.timestamp.isoformat(),
                    "category": m.category,
                    "metadata": m.metadata
                }
                for m in self._metrics[-1000:]
            ]}
        
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json_data)
                
        return json_data
    
    
metrics = MetricsCollector() # This is a global instance of the MetricsCollector for use in the blockchain application.

#decorators for metrics specific to the blockchain application

def measure_mining_time(func: Callable) -> Callable:
    """
    Decorator to measure the mining time of a block.
    
    Args:
        func (Callable): The function to decorate.
        
    Returns:
        Callable: The decorated function that measures mining time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        metadata = {}
        if hasattr(result, '__dict__'):
            if hasattr(result, 'difficulty'):
                metadata['difficulty'] = getattr(result, 'difficulty', None)
            if hasattr(result, 'nonce'):
                metadata['nonce'] = getattr(result, 'nonce', None)
                
        metrics.add_metric(
            "mining_time",
            duration,
            category="mining",
            function=func.__name__,
            **metadata
        )
         
        return result
    return wrapper

def measure_validation_time(func: Callable) -> Callable:
    """
    Decorator to measure the validation time of a block.
    
    Args:
        func (Callable): The function to decorate.
        
    Returns:
        Callable: The decorated function that measures validation time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        metadata = {
            'validation_resutl': bool(result),
            'function': func.__name__
        }
        
        if args: 
            if hasattr(args[0], '__len__'): 
                metadata['chain_length'] = len(args[0])
            elif hasattr(args[0], 'index'):
                metadata['block_index'] = getattr(args[0], 'index', None)
                
                
        metrics.add_metric(
            "validation_time",
            duration,
            category="validation",
            **metadata
        )        
        return result
    return wrapper
    
def count_nonce_iterations(func: Callable) -> Callable:
    """
    Decorator to count the number of nonce iterations during mining.
    
    Args:
        func (Callable): The function to decorate.
        
    Returns:
        Callable: The decorated function that counts nonce iterations.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # hook to the nonce iterations
        original_nonce = 0
        if len(args) > 0 and hasattr(args[0], 'nonce'):
            original_nonce = args[0].nonce
            
        result = func(*args, **kwargs)
        
        final_nonce = 0
        if hasattr(result, 'nonce'):
            final_nonce = result.nonce
        elif len(args) > 0 and hasattr(args[0], 'nonce'):
            final_nonce = args[0].nonce
        
        iterations = final_nonce - original_nonce 
        
        metadata = {
            'final_nonce': final_nonce,
            'original_nonce': original_nonce,
            'function': func.__name__,
        }
        
        if hasattr(result, 'difficulty'):
            metadata['difficulty'] = result.difficulty 
            
        metrics.add_metric(
            "nonce_iterations",
            iterations,
            category="mining",
            **metadata
        )
        
        return result
    return wrapper
    
    

