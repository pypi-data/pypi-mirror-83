import re
import itertools
from functools import reduce
from typing import List, Union, Tuple, Dict
from .exceptions import ParseError, ZSetError, ZVarError, ResolveError


class ZnTerm:
    """Integer representation in Zn"""
    n: int
    raw: str
    coef: int
    powers: List[int]
    variables: List[str]

    def __init__(self, n: int, raw: str):
        self.n = n
        self.raw = raw
        self.parse()
        self.validate_neutral_result()

    def __str__(self):
        return str(self.coef if self.coef != 1 or len(self.factors) == 0 else '') + ''.join(self.factors)

    def __repr__(self):
        return f"ZnTerm({self.n}, '{self.coef if self.coef != 1 or len(self.factors) == 0 else ''}{''.join(self.factors)}')"

    @property
    def factors(self):
        facts = [var + (f'^{self.powers[ind]}' if self.powers[ind] > 1 else '') for ind, var in enumerate(self.variables)]
        sorted_facts = sorted(facts, key=lambda x: x[0])
        return tuple(sorted_facts)

    def __add__(self, znterm: "ZnTerm") -> "ZnTerm":
        self.validate_n(znterm)
        self.validate_variables(znterm)
        new_znterm = eval(repr(self)) # type: ZnTerm
        if znterm.coef == 0:
            return new_znterm
        if new_znterm.coef == 0:
            return znterm
        new_znterm.coef = new_znterm.z_to_zn(new_znterm.coef + znterm.coef)
        new_znterm.validate_neutral_result()
        return new_znterm

    def __sub__(self, znterm: "ZnTerm") -> "ZnTerm":
        self.validate_n(znterm)
        self.validate_variables(znterm)
        new_znterm = eval(repr(self)) # type: ZnTerm
        if znterm.coef == 0:
            return new_znterm
        if new_znterm.coef == 0:
            return -znterm
        new_znterm.coef = new_znterm.z_to_zn(new_znterm.coef + (-znterm).coef)
        new_znterm.validate_neutral_result()
        return new_znterm

    def __mul__(self, znterm: Union["ZnTerm", "ZnExpression"]) -> Union["ZnTerm", "ZnExpression"]:
        if isinstance(znterm, ZnTerm):
            self.validate_n(znterm)
            new_znterm = eval(repr(self)) # type: ZnTerm
            if new_znterm.coef == 0:
                return new_znterm
            new_znterm.coef = new_znterm.z_to_zn(new_znterm.coef * znterm.coef)
            for ind, var in enumerate(znterm.variables):
                found = False
                for self_ind, self_var in enumerate(new_znterm.variables):
                    if self_var == var:
                        new_znterm.powers[self_ind] += znterm.powers[ind]
                        found = True
                if not found:
                    new_znterm.variables.append(var)
                    new_znterm.powers.append(znterm.powers[ind])
            new_znterm.validate_neutral_result()
            return new_znterm
        else:
            znexpression = znterm
            for ind, term in enumerate(znexpression.terms):
                znexpression.terms[ind] = term * self
            return znexpression

    def __neg__(self) -> "ZnTerm":
        new_znterm = eval(repr(self)) # type: ZnTerm
        new_znterm.coef = -new_znterm.coef % new_znterm.n
        return new_znterm

    def __eq__(self, znterm: "ZnTerm") -> bool:
        if self.coef == znterm.coef:
            return self.validate_n(znterm, False) and self.validate_variables(znterm, False)
        return False

    def parse(self) -> Tuple:
        """Parse this term"""
        raw = str(self.raw)
        if "." in raw:
            raise ParseError('Floating point was passed')
        coef = ""
        if raw[0] == "-":
            coef += "-"
            raw = raw[1:]
        variables = []
        powers = []
        powering = False
        power = ""
        for char in raw:
            if powering and not char.isdigit():
                if not power:
                    raise ParseError('Missing power after power sign')
                powering = False
                if not variables:
                    coef = str(int(coef)**int(power))
                else:
                    powers.append(int(power))
                power = ""
            if char.isdigit():
                if powering:
                    power += char
                elif variables:
                    raise ParseError('Variables leads integers')
                else:
                    coef += char
            elif char == "^":
                powering = True
            else:
                if len(powers) < len(variables):
                    powers.append(1)
                if char in variables:
                    raise ParseError('Repeated variable in term')
                variables.append(char)
        if len(powers) < len(variables):
            if power:
                powers.append(int(power))
            else:
                powers.append(1)
        if not coef:
            coef = 1
        self.coef = int(coef) % self.n
        self.powers = powers
        self.variables = variables
        for var in self.variables:
            if not re.match(r'[a-zA-Z]', var):
                raise ParseError(f"Unsupported variable '{char}'")

    def eval(self, values: Dict[str, int]) -> "ZnTerm":
        """Evaluate the variable in this term"""
        new_znterm = eval(repr(self)) # type: ZnTerm
        rvar = []
        rpower = []
        leftvar = []
        leftpower = []
        for ind, var in enumerate(new_znterm.variables):
            if var in values:
                rvar.append(var)
                rpower.append(new_znterm.powers[ind])
            else:
                leftvar.append(var)
                leftpower.append(new_znterm.powers[ind])
        new_znterm.variables = leftvar
        new_znterm.powers = leftpower
        for ind, var in enumerate(rvar):
            new_znterm.coef = new_znterm.z_to_zn(new_znterm.coef * (values[var] ** rpower[ind]))
        return new_znterm

    def validate_n(self, znterm: "ZnTerm", raise_ex: bool = True):
        """Validate n of another instance to n"""
        if znterm.n != self.n:
            if raise_ex:
                raise ZSetError
            return False
        return True

    def validate_variables(self, znterm: "ZnTerm", raise_ex: bool = True):
        """Validate variable of another instance to this variable"""
        if len(self.variables) != len(znterm.variables):
            if raise_ex:
                raise ZVarError
            return False
        for ind, var in enumerate(znterm.variables):
            found = False
            for self_ind, self_var in enumerate(self.variables):
                if self_var == var and self.powers[self_ind] == znterm.powers[ind]:
                    found = True
            if not found:
                if raise_ex:
                    raise ZVarError
                return False
        return True

    def validate_neutral_result(self):
        """Validate neutral result and adjust"""
        if self.coef == 0:
            self.powers = []
            self.variables = []

    def z_to_zn(self, num: int):
        """Convert Z to Zn"""
        return num % self.n


class ZnExpression:
    """Define and reduce a Zn Expression"""
    n: int
    raw: str
    terms: List[ZnTerm]

    def __init__(self, n: int, raw: str = None):
        self.n = n
        self.raw = raw
        if raw is None:
            self.terms = []
            return
        self.validate_allowed_characters()
        self.validate_parenthesis()
        self.parse()
        self.reduce()

    def __repr__(self):
        return f"ZnExpression({self.n}, '{str(self)}')"

    def __str__(self):
        return '+'.join([str(term) for term in self.terms])

    def __mul__(self, znexp: Union[ZnTerm, "ZnExpression"]) -> "ZnExpression":
        if isinstance(znexp, ZnTerm):
            return znexp * self
        else:
            znexpression = ZnExpression(self.n)
            for term in self.terms:
                for term2 in znexp.terms:
                    znexpression.terms.append(term * term2)
            znexpression.reduce()
            return znexpression

    def __eq__(self, exp: "ZnExpression") -> bool:
        if self.n == exp.n:
            for term in self.terms:
                if term not in exp.terms:
                    return False
            return True
        return False

    def parse(self):
        """Parse the expression"""
        raw = self.raw
        n = self.n
        raw_str = ""
        opened = 0
        for ind, char in enumerate(raw):
            if char == "(":
                if ind > 0 and raw[ind - 1] != "*":
                    raw_str += "*"
                opened += 1
            elif char == ")":
                opened -= 1
            if ind < len(raw) - 1 and raw[ind] in "+-" and opened == 0:
                raw_str += "$"
            raw_str += char
        raw_terms = raw_str.split('$')
        zn_terms = []
        for term in raw_terms:
            if term[0] == "+":
                term = term[1:]
            if term[0] == "*":
                term = term[1:]
            if "(" not in term and "*" not in term:
                zn_terms.append(ZnTerm(n, term))
            elif "*" in term:
                inner_terms = []
                opened = 0
                term_to_append = ""
                for char in term:
                    if char == "(":
                        opened += 1
                    elif char == ")":
                        opened -= 1
                    if char == "*" and opened == 0:
                        inner_terms.append(term_to_append)
                        term_to_append = ""
                    if char == "*" and opened > 0 or char != "*":
                        term_to_append += char
                if term_to_append:
                    inner_terms.append(term_to_append)
                multipliers = [ZnTerm(n, multiplier) if "(" not in multiplier else ZnExpression(n, multiplier[1:-1]) for multiplier in inner_terms]
                multiplied_terms = reduce(lambda a, b: a * b, multipliers)
                if isinstance(multiplied_terms, ZnTerm):
                    zn_terms.append(multiplied_terms)
                else:
                    zn_terms += multiplied_terms.terms
            else:
                zn_terms += ZnExpression(n, term[1:-1]).terms
        self.terms = zn_terms

    def validate_parenthesis(self):
        """Validate parenthesis of raw expression"""
        raw = self.raw
        opened = 0
        closed = 0
        for ind, char in enumerate(raw):
            if char == "(":
                opened += 1
            elif char == ")":
                closed += 1
            if (char == "=" or ind == len(raw) - 1) and opened != closed:
                raise ParseError('Missing closure of parenthesis')
            if closed > opened:
                raise ParseError('Parenthesis closed before opening')

    def validate_allowed_characters(self):
        """Validate allowed characters"""
        for char in self.raw:
            if not re.match(r'[a-zA-Z0-9\+\-\*\(\)\^]', char):
                raise ParseError(f"Unsupported character '{char}'")

    def reduce(self):
        """Evaluate parsed terms"""
        terms = self.terms
        groups = {}
        for term in terms:
            if term.factors not in groups:
                groups[term.factors] = []
            groups[term.factors].append(term)
        for group in groups:
            groups[group] = reduce(lambda a, b: a + b, groups[group])
        self.terms = [term for term in groups.values() if term.coef != 0]
        if len(self.terms) == 0:
            self.terms.append(ZnTerm(self.n, 0))

    def eval(self, values: Dict[str, int]) -> "ZnExpression":
        """Evaluate variables of expression"""
        new_znexp = eval(repr(self)) # type: ZnExpression
        for ind, _ in enumerate(new_znexp.terms):
            new_znexp.terms[ind] = new_znexp.terms[ind].eval(values)
        new_znexp.reduce()
        return new_znexp


class ZnEquation:
    """Define and solve a Zn equation"""
    n: int
    raw: str
    target_var: str
    left: ZnExpression
    right: ZnExpression
    solutions: List[int]
    var_amount: int = 1

    def __init__(self, n: int, raw: str):
        self.n = n
        self.raw = raw
        self.validate_equation()
        self.target_var = self.validate_var()
        self.left, self.right = [ZnExpression(n, raw_exp) for raw_exp in raw.split('=')]
        self.reduce()

    def __str__(self):
        return f"{str(self.left)}={str(self.right)}"

    def __repr__(self):
        return f"ZnEquation({self.n}, '{str(self)}')"

    def validate_var(self) -> str:
        """Validate and find an unique variable to target"""
        raw = self.raw
        found = None
        for char in raw:
            if re.match('[A-Za-z]', char):
                if found is None:
                    found = char
                    continue
                elif char == found:
                    continue
                raise ParseError('More than one variable in equation')
        return found

    def validate_equation(self):
        """Validate if there is and only one equal sign"""
        raw = self.raw
        if len(raw.split('=')) != 2:
            raise ParseError('Not an equation')

    def reduce(self):
        """Reduce the equation to the simplest form"""
        left = self.left
        right = self.right
        left_terms = []
        right_terms = []
        for term in right.terms:
            if len(term.variables) == 1:
                left_terms.append(-term)
            if len(term.variables) == 0:
                right_terms.append(term)
        for term in left.terms:
            if len(term.variables) == 1:
                left_terms.append(term)
            if len(term.variables) == 0:
                right_terms.append(-term)
        left.terms = left_terms
        right.terms = right_terms
        left.reduce()
        right.reduce()
        self.left, self.right = left, right

    def solve(self) -> List[int]:
        """Solve the equation and return list of solutions"""
        left = self.left
        right = self.right
        match = right.terms[0]
        answers = []
        for possible_ans in range(self.n):
            evaled = left.eval({self.target_var: possible_ans})
            if len(evaled.terms) != 1:
                raise ResolveError
            if evaled.terms[0] == match:
                answers.append(possible_ans)
        return answers
