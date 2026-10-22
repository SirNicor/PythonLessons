from typing import Protocol, runtime_checkable


@runtime_checkable
class Reportable(Protocol):
    def get_report_data(self) -> str:
        ...