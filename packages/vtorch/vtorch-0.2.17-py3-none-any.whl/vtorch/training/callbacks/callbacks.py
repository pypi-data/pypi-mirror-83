from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from trains import Task

if TYPE_CHECKING:
    from .early_stopping import EarlyStopping  # noqa: F401


class Callbacks:
    def __init__(self, trains_task: Optional[Task] = None, early_stopping: Optional["EarlyStopping"] = None) -> None:
        self.trains_task = trains_task
        self.trains_logger = None
        if self.trains_task is not None:
            self.trains_logger = self.trains_task.get_logger()
        self.early_stopping = early_stopping

    def trains_update_parameters(self, parameters: Dict[str, Any]) -> None:
        if self.trains_task is not None:
            self.trains_task.connect(parameters)

    def trains_report_scalar(self, title: str, series: str, value: Union[int, float], iteration: int) -> None:
        if self.trains_logger is not None:
            self.trains_logger.report_scalar(
                title=title, series=series, value=value, iteration=iteration,
            )

    def add_metric(self, val_metrics: Dict[str, float]) -> None:
        if self.early_stopping is not None:
            self.early_stopping.add_metric(val_metrics[self.early_stopping.metric_name])

    def should_stop_early(self) -> bool:
        if self.early_stopping is not None:
            return self.early_stopping.should_stop_early()
        return False

    def is_best_so_far(self) -> bool:
        if self.early_stopping is not None:
            return self.early_stopping.is_best_so_far()
        return True
