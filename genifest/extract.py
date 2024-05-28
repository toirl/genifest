from datetime import UTC, datetime, timedelta
from typing import Protocol

import requests

from genifest.transform import DataResult

queries = {
    "cpu-usage": 'label_replace(100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m]))), "metric", "cpu-usage", "", "")',
    "mem-total": 'label_replace((node_memory_total_bytes/1024/1024/1024), "metric", "mem-total", "", "")',
    "mem-free": 'label_replace(((node_memory_active_bytes/1024/1024/1024)/(node_memory_total_bytes/1024/1024/1024)*100), "metric", "mem-free", "", "")',
}


class DataQuery(Protocol):
    """A DataQuery represents a query to the Prometheus API to fetch data."""

    def query(self) -> str:
        """Returns the PromQL string which is sent to the prometheus server"""
        ...

    def step(self) -> int:
        """Returns the width of steps in seconds for the query"""
        ...

    def start_time(self) -> datetime:
        """Returns start of the timeframe for the query as UTC datetime"""
        ...

    def end_time(self) -> datetime:
        """Returns end of the timeframe for the query as UTC datetime"""
        ...

    def length(self) -> int:
        """Returns the number of metrics which will be returned by the query"""
        ...


class CPUandMem:
    def __init__(self):
        # Zeitstempel für den Start und das Ende des Zeitbereichs
        self._end_time = datetime.now(tz=UTC)
        self._start_time = self._end_time - timedelta(hours=1)
        self._step = 60  # Schrittweite der Abfrage (1 Minute)

    def query(self) -> str:
        # TODO: Build query using the step width. Currently static
        return f"{queries["cpu-usage"]} or {queries['mem-total']} or {queries['mem-free']}"

    def start_time(self) -> datetime:
        return self._start_time

    def step(self) -> int:
        return self._step

    def end_time(self) -> datetime:
        return self._end_time

    def length(self) -> int:
        return 3


class PrometheusDataExtractor:
    """The PrometheusDataExtractor fetches data from a Prometheus API based on
    the given DataQuery object. It will return a DataResult object."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_data(self, query: DataQuery) -> DataResult:
        url = f"{self.base_url}/api/v1/query_range"
        params = {
            "query": query.query(),
            "start": query.start_time().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": query.end_time().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "step": f"{query.step()}s",
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return DataResult(data, query.length())
