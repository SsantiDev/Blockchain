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

