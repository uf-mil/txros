"""
Various classes dedicated specifically to improving type annotations throughout
the repository.
"""
from __future__ import annotations

import asyncio
from abc import ABCMeta, abstractmethod
from io import BytesIO
from typing import (
    Any,
    Callable,
    ClassVar,
    Coroutine,
    Dict,
    Optional,
    Protocol,
    TypeVar,
    runtime_checkable,
)

from actionlib_msgs.msg import GoalID, GoalStatus
from std_msgs.msg import Header

TCPROSHeader = Dict[str, str]
TCPROSProtocol = Callable[
    [TCPROSHeader, asyncio.StreamReader, asyncio.StreamWriter],
    Coroutine[Any, Any, None],
]


@runtime_checkable
class Message(Protocol):
    _md5sum: ClassVar[str]
    _type: ClassVar[str]
    _has_header: ClassVar[bool]
    _full_text: ClassVar[str]
    _slot_types: ClassVar[list[str]]

    @abstractmethod
    def _get_types(self) -> list[str]:
        ...

    @abstractmethod
    def serialize(self, buff: BytesIO) -> None:
        ...

    @abstractmethod
    def deserialize(self, str: bytes) -> Message:
        ...


@runtime_checkable
class MessageWithHeader(Message, Protocol, metaclass=ABCMeta):
    header: Header


Request = TypeVar("Request", bound=Message)
Response = TypeVar("Response", bound=Message)


class ServiceMessage(Protocol[Request, Response]):
    _type: str
    _md5sum: str
    _request_class: type[Request]
    _response_class: type[Response]


Goal = TypeVar("Goal", bound=Message)
Feedback = TypeVar("Feedback", bound=Message)
Result = TypeVar("Result", bound=Message)


@runtime_checkable
class ActionGoal(MessageWithHeader, Protocol[Goal], metaclass=ABCMeta):
    goal_id: GoalID
    goal: Goal


@runtime_checkable
class ActionResult(Message, Protocol[Result], metaclass=ABCMeta):
    status: GoalStatus


@runtime_checkable
class ActionFeedback(Message, Protocol[Feedback], metaclass=ABCMeta):
    status: GoalStatus


@runtime_checkable
class Action(Protocol[Goal, Feedback, Result]):
    action_goal: ActionGoal[Goal]
    action_result: ActionResult[Result]
    action_feedback: ActionFeedback[Feedback]
