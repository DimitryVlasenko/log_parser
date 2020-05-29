from dataclasses import dataclass
from datetime import datetime
from dataclasses_json import dataclass_json
from typing import (Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar,
                    Union)

@dataclass_json()
@dataclass()
class TraceModel:
    """description of class"""
    start_time: datetime
    end_time: datetime
    trace_id: str
    service_name: str
    span_received: str
    span_assigned: str
    created: datetime

@dataclass_json
@dataclass#(frozen=True)
class ChildOutputModel:
    service: str
    start: str
    end: str
    span: str
    cals: [] #List[Any]#[ChildOutputModel]

@dataclass_json
@dataclass#(frozen=True)
class RootOutputModel:
    id: str
    root: ChildOutputModel

