from src.dto.clicks import ClicksMetrics


class ClicksMapper:
    @staticmethod
    def to_clicks_metrics(total: int, unique: int) -> ClicksMetrics:
        return ClicksMetrics(total=total, unique=unique)
