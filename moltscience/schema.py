from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ExperimentStatus(str, Enum):
    KEEP = "keep"
    DISCARD = "discard"
    CRASH = "crash"


class MetricDirection(str, Enum):
    LOWER_IS_BETTER = "lower_is_better"
    HIGHER_IS_BETTER = "higher_is_better"


@dataclass
class Metric:
    name: str
    value: float
    direction: MetricDirection


@dataclass
class Experiment:
    id: str
    problem: str
    title: str
    agent: str
    status: ExperimentStatus
    metric: Metric
    timestamp: str
    methodology: str = ""
    hypotheses: list[str] = field(default_factory=list)
    related_experiments: list[str] = field(default_factory=list)
    sub_experiments: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Manifest:
    id: str
    problem: str
    title: str
    agent: str
    status: ExperimentStatus
    metric_name: str
    metric_value: float
    metric_direction: MetricDirection
    timestamp: str
    methodology: str = ""
    motivation: str = ""
    hypotheses: list[str] = field(default_factory=list)
    related_experiments: list[str] = field(default_factory=list)
    sub_experiments: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Manifest":
        return cls(
            id=data["id"],
            problem=data["problem"],
            title=data["title"],
            agent=data["agent"],
            status=ExperimentStatus(data["status"]),
            metric_name=data["metric_name"],
            metric_value=float(data["metric_value"]),
            metric_direction=MetricDirection(data["metric_direction"]),
            timestamp=data["timestamp"],
            methodology=data.get("methodology", ""),
            motivation=data.get("motivation", ""),
            hypotheses=list(data.get("hypotheses", [])),
            related_experiments=list(data.get("related_experiments", [])),
            sub_experiments=list(data.get("sub_experiments", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["metric_direction"] = self.metric_direction.value
        return data

    def to_index_record(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "problem": self.problem,
            "title": self.title,
            "agent": self.agent,
            "status": self.status.value,
            "metric_name": self.metric_name,
            "metric_value": self.metric_value,
            "metric_direction": self.metric_direction.value,
            "timestamp": self.timestamp,
        }
