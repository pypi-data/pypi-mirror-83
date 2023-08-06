# Python asynchronous I/O package for LDMud

This is a python module that enables the use of the Python asyncio module
with LDMud 3.6.2 and later. The module doesn't export any names, it just
extends the Python asyncio module to work with LDMud.

## Usage

### Install from the python package index

The efun package can be downloaded from the python package index:

```
pip3 install --user ldmud-asyncio
```

### Build & install the package yourself

You can build the package yourself.

First clone the repository
```
git clone https://github.com/ldmud/python-asyncio.git
```

Install the package
```
cd python-asyncio
python3 setup.py install --user
```

### Automatically load the module at startup

In your Python startup script for LDMud add the following line:
```
import ldmud_asyncio
```

## Examples

### call_out() replacement

```python
import ldmud, ldmud_asyncio, asyncio

async def do_call_out(cb, sec):
    await asyncio.sleep(sec)
    cb()

def efun_call_out(cb: ldmud.Closure, sec: int) -> None:
    asyncio.run(do_call_out(cb, sec))

ldmud.register_efun("py_call_out", efun_call_out)

```

### Call a program and return the lines

```python
import ldmud, ldmud_asyncio, asyncio

async def do_exec(prog, cb):
    proc = await asyncio.create_subprocess_exec(prog, stdout=asyncio.subprocess.PIPE)

    async for line in proc.stdout:
        cb(line.decode())

    await proc.wait()
    cb(0)

def efun_exec(prog: str, cb: ldmud.Closure) -> None:
    asyncio.run(do_exec(prog, cb))

ldmud.register_efun("py_exec", efun_exec)
```

### Start a websockets server

This is the synchronization example from the websockets package.
Here we only added an efun to influence the value as well.

This is the Python code:
```python
import ldmud, ldmud_asyncio, asyncio, websockets, json

STATE = {"value": 0}
USERS = set()

def state_event():
    return json.dumps({"type": "state", **STATE})

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "minus":
                STATE["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                STATE["value"] += 1
                await notify_state()
    finally:
        await unregister(websocket)

asyncio.run(websockets.serve(counter, "localhost", 6789))

async def do_ws_set_value(val):
    STATE["value"] = val
    await notify_state()

def efun_ws_set_value(val: int) -> None:
    asyncio.run(do_ws_set_value(val))

ldmud.register_efun("py_ws_set_value", efun_ws_set_value)
```

And here the HTML code to run in the browser:
```html
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket demo</title>
        <style type="text/css">
            body {
                font-family: "Courier New", sans-serif;
                text-align: center;
            }
            .buttons {
                font-size: 4em;
                display: flex;
                justify-content: center;
            }
            .button, .value {
                line-height: 1;
                padding: 2rem;
                margin: 2rem;
                border: medium solid;
                min-height: 1em;
                min-width: 1em;
            }
            .button {
                cursor: pointer;
                user-select: none;
            }
            .minus {
                color: red;
            }
            .plus {
                color: green;
            }
            .value {
                min-width: 2em;
            }
            .state {
                font-size: 2em;
            }
        </style>
    </head>
    <body>
        <div class="buttons">
            <div class="minus button">-</div>
            <div class="value">?</div>
            <div class="plus button">+</div>
        </div>
        <div class="state">
            <span class="users">?</span> online
        </div>
        <script>
            var minus = document.querySelector('.minus'),
                plus = document.querySelector('.plus'),
                value = document.querySelector('.value'),
                users = document.querySelector('.users'),
                websocket = new WebSocket("ws://127.0.0.1:6789/");
            minus.onclick = function (event) {
                websocket.send(JSON.stringify({action: 'minus'}));
            }
            plus.onclick = function (event) {
                websocket.send(JSON.stringify({action: 'plus'}));
            }
            websocket.onmessage = function (event) {
                data = JSON.parse(event.data);
                switch (data.type) {
                    case 'state':
                        value.textContent = data.value;
                        break;
                    case 'users':
                        users.textContent = (
                            data.count.toString() + " user" +
                            (data.count == 1 ? "" : "s"));
                        break;
                    default:
                        console.error(
                            "unsupported event", data);
                }
            };
        </script>
    </body>
</html>
```

Have fun!
