from typing import Union, Callable, Set, Dict

from gev.utils import import_from_string


def _parse_func(func: Union[str, Callable]) -> Callable:
    return import_from_string(func) if isinstance(func, str) else func


class Event:
    def __init__(self, source: str, type: str, payload: dict):
        self.source = source
        self.type = type
        self.payload = payload

    def __repr__(self) -> str:
        return f'<Event source={self.source!r} type={self.type!r} payload={self.payload!r}>'


class OnSpec:
    def __init__(self, source: str, type: str):
        self.source = source
        self.type = type

    @classmethod
    def from_raw(cls, raw: str):
        """Parse raw string into an OnSpec."""
        source, type = raw.split("::")
        return cls(source=source, type=type)

    def __str__(self):
        return f"{self.source}::{self.type}"

    def __hash__(self) -> int:
        return hash(str(self))


class EventManager:
    _handlers: Dict[str, Set[Callable]]

    def __init__(self):
        self._handlers = {}

    def on(self, spec: str) -> 'ActionDescriptor':
        """
        Register handler for specific type of events.

        Args:
            spec: in format "source::type", e.g. "sys1::step_core_vessel_marked"
        """
        return ActionDescriptor(manager=self, on_spec=spec)

    def take(self, event: Event):
        """Give an event, take actions."""
        on_spec = str(OnSpec(source=event.source, type=event.type))
        if on_spec in self._handlers:
            for handler in self._handlers[on_spec]:
                handler(event)


class ActionDescriptor:
    manager: EventManager
    on_spec: str
    action: Callable

    def __init__(self, manager: EventManager, on_spec: str):
        self.manager = manager
        self.on_spec = on_spec

    def do(self, action: Callable) -> 'EventManager':
        self.manager._handlers.setdefault(self.on_spec, set()).add(
            _parse_func(action)
        )
        return self.manager


default_manager = EventManager()

on = default_manager.on
take = default_manager.take
