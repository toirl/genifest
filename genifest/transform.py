from collections import OrderedDict
from datetime import UTC, datetime
from typing import List

from genifest.write import ManifestData


class Value:
    def __init__(self, date: datetime, value: float):
        self.date = date
        self.value = value


metric_name_mapping = {
    "cpu-usage": "cpu/utilization",
    "mem-free": "memory/utilization",
    "mem-total": "memory/capacity",
}


class Metric:
    def __init__(self, name: str, instance: str, values: List[dict]):
        self.name = metric_name_mapping[name]
        self.instance = instance
        self.values: List[Value] = []

        # Convert values
        for value_pair in values:
            date = datetime.fromtimestamp(value_pair[0], UTC)
            value = float(value_pair[1])  # values as float
            self.values.append(Value(date, value))

        # Calculate the duration
        v1_dt = self.values[0].date
        v2_dt = self.values[1].date
        td = v2_dt - v1_dt
        self.duration = int(td.total_seconds())


class DataResult:
    def __init__(self, data: dict, length: int):
        assert data["data"]["resultType"] == "matrix", "Expected multiple results"
        self.length = length
        self._metrics = []
        self._data = data
        for result in data["data"]["result"]:
            metric = result["metric"]["metric"]
            instance = result["metric"]["instance"].split(":")[0]
            values = result["values"]
            self._metrics.append(Metric(metric, instance, values))

    def metrics(self) -> List[Metric]:
        return self._metrics


class Transformer:
    """The Transformer will transform the given DataResult into ManifestData
    which is the source for the ManifestWriter"""

    def transform(self, data: DataResult) -> ManifestData:
        manifest_data = ManifestData()
        extracted = {}

        # Collect metrics for an instance
        for metric in data.metrics():
            if metric.instance not in extracted:
                extracted[metric.instance] = {}

            for value in metric.values:
                iso_time = value.date.isoformat()
                if iso_time not in extracted[metric.instance]:
                    extracted[metric.instance][iso_time] = {}

                if metric not in extracted[metric.instance][iso_time]:
                    extracted[metric.instance][iso_time][metric.name] = value.value
                extracted[metric.instance][iso_time]["duration"] = metric.duration

        for instance in extracted:
            inputs = []
            for date in extracted[instance]:
                input_data = OrderedDict()
                input_data["timestamp"] = date
                input_data.update(extracted[instance][date])

                # Make sure that the lenth of the data indicates that data
                # contains all expected fields.
                # With the timestamp and duration are two additional fields in
                # input data.
                if len(input_data) - 2 != data.length:
                    continue
                inputs.append(dict(input_data))

            manifest_data.add_instance(instance, inputs)

        return manifest_data
