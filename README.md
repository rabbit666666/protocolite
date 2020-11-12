A tool for generate net message from protocol define to lua table or python dict. now, it only support generate Python and Lua.

* protocol define in python.
* output python and lua code for parsing and serializing.
* the setter function will check input type.
* example of protocol define.
```python
class Apple:
    name: str
    weight: float
    size: float

class Pair:
    name: str
    weight: float
    size: float


class Basket:
    apples: [Apple]
    pairs: [Pair]
```
