# Znop
Library that solves discrete math operations of the group Zn, provides both as calculator program or third party library.

> The group Zn consists of the elements {0, 1, 2, . . . , n−1} with addition mod n as the operation. You can also multiply elements of Zn, but you do not obtain a group: The element 0 does not have a multiplicative inverse, for instance.
> However, if you confine your attention to the units in Zn — the elements which have multiplicative inverses — you do get a group under multiplication mod n. It is denoted Un, and is called the group of units in Zn.

## Program Usage
Describe how to install the calculator and its commands.

> ***Note***: This program will ***always create a `znop_db.json` file if it doesn't exist*** in the directory you execute the program, this file is aimed to save your last ~30 commands and the Zn group (default n=10) set on your program.

### Install from source

0. Make sure to have python > v3.6 installed.
1. `$ git clone https://github.com/paaksing/Znop.git`
2. `$ cd Znop`
3. `$ python setup.py install`
4. `$ znop`.

### Install using pip

0. Make sure to have python > v3.6 installed and `pip` installed.
1. `$ pip install znop`.
2. `$ znop`.

### Install as executable

1. Find the latest executable in this repository's [Releases](https://github.com/paaksing/Znop/releases).
2. Download it to local machine 
3. Execute it.

### Commands

All payload passed to the commands should strictly match this regex: `[a-zA-Z0-9\+\-\*\(\)\^]`

| Command | Description |
| --- | --- |
| set n=`<setnumber>`   | Set the set number of Z |
| reduce `<expression>` | Reduce a Zn expression or equation |
| solve `<equation>`    | Solve an one-dimensional Zn equation |
| help                | Usage of this program |
| quit                | Quit this program |

### Example

```bash
(n=10) reduce (3x*9)+78-4x
3x+8

(n=10) set n=6
OK

(n=6) solve x^2+3x+2=0
x ∈ {1, 2, 4, 5}

(n=6) quit
```

## Library Usage
Describe usage and API of this library.

### Requirements and installation

- Python 3.6 (due to requirements of f-strings)
- Install using `pip install znop`

## API Documentation
This library consists of 3 modules: `core` and `exceptions`. All objects in this library can be "copied" or "reinstantiated" by doing `eval(repr(obj))` where obj is an `znop` object. `str()` will return the string representation of the object and `repr()` will return the string representation of the object in python syntax.

Import the object from the respective modules e.g.: `from znop.core import ZnEquation`

### znop.core.ZnTerm
Represents a term in the group of ZnTerm

- `__init__(n: int, raw: str)`: Create an instance of ZnTerm, arguments: n (set number), raw (raw string of term, e.g. `'2x'`).

- `__add__, __sub__, __mul__, __neg__, __eq__`: This object supports [`+`, `-`, `*`] operations between ZnTerms, with the exception of multiplications that it can multiply a ZnExpression by doing distributive, it will always return a new ZnTerm. Supports `-` (negate) operation and returns a new ZnTerm. It also supports equality comparison `==` between ZnTerms.

- `eval(values: Dict[str, int])`: Evaluate the variables in the term, receives a mapping of variable name to value e.g. `{'x': 6}`, and return a new ZnTerm.

### znop.core.ZnExpression
- `__init__(n: int, raw: str)`: Create an instance of ZnExpression, arguments: n (set number), raw (raw string of expression, e.g. `'2x+x-3'`). This expression is automatically reduced to its simplest form.

- `__mul__, __eq__`: This objects supports `*` between ZnExpressions and ZnTerms by doing distributive, It also supports equality comparison `==` between ZnExpressions.

- `reduce()`: Reduce the expression to the simplest form, this function is automatically called on instantiation.

- `eval(values: Dict[str, int])`: Evaluate the variables in the expression, receives a mapping of variable name to value e.g. `{'x': 6}`, and return a new ZnExpression.

### znop.core.ZnEquation
- `__init__(n: int, raw: str)`: Create an instance of ZnEquation, arguments: n (set number), raw (raw string of equation, e.g. `'2x^2+3=0'`). This equation is automatically reduced to its simplest form.

- `reduce()`: Reduce the equation to the simplest form, this function is automatically called on instantiation.

- `solve()`: Solve the equation by returning a list of solutions (ints). If the equation cannot be solved, then `ResolveError` will be raised.

### znop.exceptions.ZSetError
Operation between ZnInt of different Z set.

### znop.exceptions.ZVarError
Operation between ZnInt of different variables outside products.

### znop.exceptions.ParseError
Indicates a parsing error, reason will be stated when `ParseError` is thrown.

### znop.exceptions.ResolveError
Could not resolve equation.
