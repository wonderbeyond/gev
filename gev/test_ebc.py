from unittest.mock import Mock
from gev import default_manager, on, take, Event, EventManager


def _reset_default_manager():
    default_manager._handlers = {}


def test_bare_default_manager():
    assert on == default_manager.on
    assert on != EventManager().on

    assert take == default_manager.take
    assert take != EventManager().take


def test_registry():
    sys1_a_handler = Mock()
    sys1_b_handler = Mock()
    sys1_b_handler_2 = Mock()

    (
        on('sys1::event_a').do(sys1_a_handler)
        .on('sys1::event_b').do(sys1_b_handler)
        .on('sys1::event_b').do(sys1_b_handler_2)
    )

    assert len(default_manager._handlers) == 2
    assert default_manager._handlers['sys1::event_a'] == {sys1_a_handler}
    assert default_manager._handlers['sys1::event_b'] == {
        sys1_b_handler, sys1_b_handler_2
    }

    _reset_default_manager()


def test_take_action_on_event():
    sys1_a_handler = Mock()
    sys1_b_handler = Mock()
    sys1_b_handler_2 = Mock()

    on('sys1::event_a').do(sys1_a_handler)
    on('sys1::event_b').do(sys1_b_handler)
    on('sys1::event_b').do(sys1_b_handler_2)

    take(Event(
        source='sys2', type='event_a', payload={'a': 1}
    ))
    assert sys1_a_handler.call_count == 0
    assert sys1_b_handler.call_count == 0

    take(Event(
        source='sys1', type='event_b', payload={'a': 1}
    ))
    assert sys1_a_handler.call_count == 0
    assert sys1_b_handler.call_count == 1
    assert sys1_b_handler_2.call_count == 1

    _reset_default_manager()
