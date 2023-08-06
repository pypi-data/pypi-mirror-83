# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplemonads']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simplemonads',
    'version': '1.0.12',
    'description': 'Easy to use monads (containers), with pattern matching, that improve the quality of your python code. Use Just to end checking for None, Success to end unhandled exceptions, Future for async, and Reader for dependencies.',
    'long_description': '# [simplemonads](https://sdaves.github.io/simplemonads/)\n\nLet\'s make monads easy, fun, and productive.\n\n## Platform support\n\nJust `pip install simplemonads` and you\'re done. You can also download [this single file](https://sdaves.github.io/simplemonads/tests/simplemonads.py) into your project and use it as you wish without dependencies. Works across all platforms, so CPython >= 3.5 (Windows, Linux, Mac, Android, iOS), in a [single standalone html](https://sdaves.github.io/simplemonads/tests/test_brython_standalone.html) file, multiple files in the browser with [dynamic loading](https://sdaves.github.io/simplemonads/tests/index.html), and [even on microcontrollers with micropython](https://micropython.org).\n\n## Docs\n\n[Read the docs here.](https://sdaves.github.io/simplemonads/docs/)\n\n## Example GUI using monads: `Success`, `Failure`, `Just`, `Reader`, and `Printer`\n\n![Screenshot of test_reader.py](https://sdaves.github.io/simplemonads/docs/test_reader.png)\n\n```python\nimport simplemonads as sm\n\ntry:\n\n    class Deps(sm.Protocol):\n        "Dependencies for your application"\n\n        def popup(self, msg: str) -> None:\n            "Display a popup with the specified message."\n\n\nexcept:\n    pass\n\n\n@sm.run\nclass TestReader:\n    @classmethod\n    def make(cls, create: "sm.Callable[[],sm.Any]") -> "sm.Callable[[],Deps]":\n        gui = create()\n\n        class GuiDeps:\n            def popup(self, x: str):\n                gui.Popup(x)\n\n        return GuiDeps\n\n    @classmethod\n    def app(cls, divide_by_zero: bool = False) -> sm.Reader:\n        data = sm.Success(sm.Just(7))\n        double = lambda x: x + (lambda y: y * 2)\n        triple = lambda x: x + (lambda y: y * 3)\n        result = data + triple + double\n\n        if divide_by_zero:\n            result += lambda x: x + (lambda x: x / 0)\n\n        def effect(deps: "Deps") -> "sm.Monad":\n            msg = "Answer to the Universe: "\n            err = "Whoops, an error happened: "\n            result | {\n                sm.Success: lambda x: x\n                | {sm.Just: lambda val: deps.popup(msg + str(val))},\n                sm.Failure: lambda x: deps.popup(err + x),\n            }\n            return result\n\n        return sm.Reader(effect)\n\n    @classmethod\n    def main(cls):\n        gui = sm.Success() + (lambda x: __import__("PySimpleGUI")) | {\n            sm.Success: lambda x: x,\n            sm.Failure: lambda x: sm.Printer(),\n        }\n\n        return cls.app() + cls.make(lambda: gui)\n```\n',
    'author': 'Stephen Daves',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdaves/simplemonads',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
