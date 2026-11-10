from pydantic import TypeAdapter

from src.dto.clicks import ClicksMetrics


class ClicksJsonSerializer:
    _metrics_adapter = TypeAdapter(ClicksMetrics)

    @classmethod
    def to_json(cls, metrics: ClicksMetrics) -> str:
        return cls._metrics_adapter.dump_json(metrics).decode()

    @classmethod
    def from_json(cls, metrics_json: str | bytes) -> ClicksMetrics:
        return cls._metrics_adapter.validate_json(metrics_json)
