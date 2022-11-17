# Gev (General Events Manager)

```shell
$ pip install gev
```

---

## Usage

```python
from gev import Event, EventManager

manager = EventManager()

def handler_1(e):
    print("handler_1 called with", e)

def handler_2(e):
    print("handler_2 called with", e)

# Register event handlers
manager.on('sys_1::event_a').do(handler_1)
manager.on('sys_1::event_b').do(handler_2)

manager.take(Event(
    source='sys_1',
    type='event_a',
    payload={'a': 1}
))  # handler_1 will be called

manager.take(Event(
    source='sys_1',
    type='event_b',
    payload={'b': 1}
))  # handler_1 will be called
```

If you don't want to initialize an `EventManager` instance,
you can use the global `default_manager` and its `on` and `take` methods exposed at module level.

```python
from gev import on, take, Event

def handler_1(e):
    print("handler_1 called with", e)

on('sys_1::event_a').do(handler_1)

take(Event(
    source='sys_1',
    type='event_a',
    payload={'a': 1}
))  # handler_1 will be called
```
