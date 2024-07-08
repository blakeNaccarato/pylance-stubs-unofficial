from types import NotImplementedType
from typing import Any, Callable, Literal, Never, Self

from sympy.core.sympify import CantSympify
from sympy.external.gmpy import GROUND_TYPES
from sympy.polys.domains import Domain
from sympy.polys.polyutils import PicklableWithSlots

class GenericPoly(PicklableWithSlots):
    def ground_to_ring(f): ...
    def ground_to_field(f): ...
    def ground_to_exact(f): ...

def init_normal_DMP(rep, lev, dom) -> DMP: ...

class DMP(PicklableWithSlots, CantSympify):
    __slots__ = ...
    def __init__(self, rep, dom, lev=..., ring=...) -> None: ...
    def __repr__(f) -> str: ...
    def __hash__(f) -> int: ...
    def unify(
        f, g
    ) -> (
        tuple[Any, Any, Callable[..., Any | DMP], list[Any] | Any | list[list[Any]], list[Any] | Any | list[list[Any]]]
        | tuple[Any, Any, Callable[..., Any | DMP], Any | list[list[Any]], Any | list[list[Any]]]
    ): ...
    def per(f, rep, dom=..., kill=..., ring=...) -> DMP: ...
    @classmethod
    def zero(cls, lev, dom, ring=...) -> DMP: ...
    @classmethod
    def one(cls, lev, dom, ring=...) -> DMP: ...
    @classmethod
    def from_list(cls, rep, lev, dom) -> Self: ...
    @classmethod
    def from_sympy_list(cls, rep, lev, dom) -> Self: ...
    def to_dict(f, zero=...) -> dict[tuple[Literal[0]], Any] | dict[Any, Any]: ...
    def to_sympy_dict(f, zero=...) -> dict[tuple[Literal[0]], Any] | dict[Any, Any]: ...
    def to_list(f) -> list[Any] | list[list[Any]]: ...
    def to_sympy_list(f) -> list[Any]: ...
    def to_tuple(f) -> tuple[Any, ...]: ...
    @classmethod
    def from_dict(cls, rep, lev, dom) -> Self: ...
    @classmethod
    def from_monoms_coeffs(cls, monoms, coeffs, lev, dom, ring=...) -> DMP: ...
    def to_ring(f) -> Self | DMP: ...
    def to_field(f) -> Self | DMP: ...
    def to_exact(f) -> Self | DMP: ...
    def convert(f, dom) -> Self | DMP: ...
    def slice(f, m, n, j=...) -> DMP: ...
    def coeffs(f, order=...) -> list[Any]: ...
    def monoms(f, order=...) -> list[Any]: ...
    def terms(f, order=...) -> list[tuple[Any, Any]] | list[Any]: ...
    def all_coeffs(f) -> list[Any] | list[list[Any]]: ...
    def all_monoms(f) -> list[tuple[Literal[0]]] | list[tuple[Any | int]]: ...
    def all_terms(f) -> list[tuple[tuple[Literal[0]], Any]] | list[tuple[tuple[Any | int], list[Any]]]: ...
    def lift(f) -> DMP: ...
    def deflate(f) -> tuple[Any | tuple[Any, ...], Any | DMP]: ...
    def inject(f, front=...) -> Self: ...
    def eject(f, dom, front=...) -> Self: ...
    def exclude(f) -> tuple[list[Any], Self]: ...
    def permute(f, P) -> DMP: ...
    def terms_gcd(f) -> tuple[Any | tuple[Any, ...], Any | DMP]: ...
    def add_ground(f, c) -> DMP: ...
    def sub_ground(f, c) -> DMP: ...
    def mul_ground(f, c) -> DMP: ...
    def quo_ground(f, c) -> DMP: ...
    def exquo_ground(f, c) -> DMP: ...
    def abs(f) -> DMP: ...
    def neg(f) -> DMP: ...
    def add(f, g) -> DMP: ...
    def sub(f, g) -> DMP: ...
    def mul(f, g) -> DMP: ...
    def sqr(f) -> DMP: ...
    def pow(f, n) -> DMP: ...
    def pdiv(f, g) -> tuple[Any | DMP, Any | DMP]: ...
    def prem(f, g) -> DMP: ...
    def pquo(f, g) -> DMP: ...
    def pexquo(f, g) -> DMP: ...
    def div(f, g) -> tuple[Any | DMP, Any | DMP]: ...
    def rem(f, g) -> DMP: ...
    def quo(f, g) -> DMP: ...
    def exquo(f, g) -> DMP: ...
    def degree(f, j=...) -> int: ...
    def degree_list(f) -> tuple[Any, ...]: ...
    def total_degree(f) -> int: ...
    def homogenize(f, s) -> DMP: ...
    def homogeneous_order(f) -> int | None: ...
    def LC(f): ...
    def TC(f): ...
    def nth(f, *N): ...
    def max_norm(f): ...
    def l1_norm(f) -> int: ...
    def l2_norm_squared(f) -> int: ...
    def clear_denoms(f) -> tuple[Any, Any | DMP]: ...
    def integrate(f, m=..., j=...) -> DMP: ...
    def diff(f, m=..., j=...) -> DMP: ...
    def eval(f, a, j=...) -> DMP: ...
    def half_gcdex(f, g) -> tuple[Any | DMP, Any | DMP]: ...
    def gcdex(f, g) -> tuple[Any | DMP, Any | DMP, Any | DMP]: ...
    def invert(f, g) -> DMP: ...
    def revert(f, n) -> DMP: ...
    def subresultants(f, g) -> list[Any | DMP]: ...
    def resultant(f, g, includePRS=...) -> tuple[Any | DMP, list[Any | DMP]] | DMP: ...
    def discriminant(f) -> DMP: ...
    def cofactors(f, g) -> tuple[Any | DMP, Any | DMP, Any | DMP]: ...
    def gcd(f, g) -> DMP: ...
    def lcm(f, g) -> DMP: ...
    def cancel(
        f, g, include=...
    ) -> tuple[Any | DMP, Any | DMP] | tuple[Any | list[Any], Any | list[Any], Any | DMP, Any | DMP]: ...
    def trunc(f, p) -> DMP: ...
    def monic(f) -> DMP: ...
    def content(f): ...
    def primitive(f) -> tuple[Any, Any | DMP]: ...
    def compose(f, g) -> DMP: ...
    def decompose(f) -> list[Any | DMP]: ...
    def shift(f, a) -> DMP: ...
    def transform(f, p, q) -> DMP: ...
    def sturm(f) -> list[Any | DMP]: ...
    def cauchy_upper_bound(f): ...
    def cauchy_lower_bound(f): ...
    def mignotte_sep_bound_squared(f): ...
    def gff_list(f) -> list[tuple[Any | DMP, Any]]: ...
    def norm(f) -> DMP: ...
    def sqf_norm(f) -> tuple[int, Any | DMP, Any | DMP]: ...
    def sqf_part(f) -> DMP: ...
    def sqf_list(f, all=...) -> tuple[Any, list[tuple[Any | DMP, Any]]]: ...
    def sqf_list_include(f, all=...) -> list[tuple[Any | DMP, Literal[1]]]: ...
    def factor_list(f) -> tuple[Any, list[tuple[Any | DMP, Any]]]: ...
    def factor_list_include(f) -> list[tuple[Any | DMP, Any | Literal[1]]]: ...
    def intervals(
        f, all=..., eps=..., inf=..., sup=..., fast=..., sqf=...
    ) -> (
        list[Any]
        | list[tuple[tuple[Any, Any], Any, Any] | tuple[Any, Any]]
        | list[tuple[Any, Any] | tuple[Any | list[Any], tuple[Any, Any, Any, Any]]]
        | list[Any]
        | tuple[list[tuple[tuple[Any | list[Any], Any | tuple[Any, Any, Any, Any]], Any]], list[tuple[tuple[Any, Any], Any]]]
        | tuple[list[Any] | list[tuple[Any, Any] | tuple[Any | list[Any], tuple[Any, Any, Any, Any]]] | list[Any], Any]
    ): ...
    def refine_root(
        f, s, t, eps=..., steps=..., fast=...
    ) -> tuple[Any, Any] | tuple[Any | list[Any], Any | tuple[Any, Any, Any, Any]]: ...
    def count_real_roots(f, inf=..., sup=...) -> int: ...
    def count_complex_roots(f, inf=..., sup=...) -> int: ...
    @property
    def is_zero(f) -> bool: ...
    @property
    def is_one(f) -> bool: ...
    @property
    def is_ground(f) -> bool: ...
    @property
    def is_sqf(f) -> bool: ...
    @property
    def is_monic(f): ...
    @property
    def is_primitive(f): ...
    @property
    def is_linear(f) -> bool: ...
    @property
    def is_quadratic(f) -> bool: ...
    @property
    def is_monomial(f) -> bool: ...
    @property
    def is_homogeneous(f) -> bool: ...
    @property
    def is_irreducible(f) -> bool: ...
    @property
    def is_cyclotomic(f) -> bool: ...
    def __abs__(f) -> DMP: ...
    def __neg__(f) -> DMP: ...
    def __add__(f, g) -> NotImplementedType | DMP: ...
    def __radd__(f, g) -> NotImplementedType | DMP: ...
    def __sub__(f, g) -> NotImplementedType | DMP: ...
    def __rsub__(f, g) -> NotImplementedType | DMP: ...
    def __mul__(f, g) -> DMP | NotImplementedType: ...
    def __truediv__(f, g) -> DMP | NotImplementedType: ...
    def __rtruediv__(f, g) -> DMP | NotImplementedType: ...
    def __rmul__(f, g) -> DMP | NotImplementedType: ...
    def __pow__(f, n) -> DMP: ...
    def __divmod__(f, g) -> tuple[Any | DMP, Any | DMP]: ...
    def __mod__(f, g) -> DMP: ...
    def __floordiv__(f, g) -> DMP | NotImplementedType: ...
    def __eq__(f, g) -> bool: ...
    def __ne__(f, g) -> bool: ...
    def eq(f, g, strict=...) -> bool: ...
    def ne(f, g, strict=...) -> bool: ...
    def __lt__(f, g) -> bool: ...
    def __le__(f, g) -> bool: ...
    def __gt__(f, g) -> bool: ...
    def __ge__(f, g) -> bool: ...
    def __bool__(f) -> bool: ...

def init_normal_DMF(num, den, lev, dom) -> DMF: ...

class DMF(PicklableWithSlots, CantSympify):
    __slots__ = ...
    def __init__(self, rep, dom, lev=..., ring=...) -> None: ...
    @classmethod
    def new(cls, rep, dom, lev=..., ring=...) -> Self: ...
    def __repr__(f) -> str: ...
    def __hash__(f) -> int: ...
    def poly_unify(
        f, g
    ) -> (
        tuple[Any, Any, Callable[..., Any | Self], tuple[Any | list[Any], Any | list[Any]], list[Any] | Any | list[list[Any]]]
        | tuple[Any, Any, Callable[..., Any | Self], tuple[Any | list[list[Any]], Any | list[list[Any]]], Any | list[list[Any]]]
    ): ...
    def frac_unify(f, g) -> (
        tuple[
            Any, Any, Callable[..., Any | Self], tuple[Any | list[Any], Any | list[Any]], tuple[Any | list[Any], Any | list[Any]]
        ]
        | tuple[
            Any,
            Any,
            Callable[..., Any | Self],
            tuple[Any | list[list[Any]], Any | list[list[Any]]],
            tuple[Any | list[list[Any]], Any | list[list[Any]]],
        ]
    ): ...
    def per(f, num, den, cancel=..., kill=..., ring=...) -> Self: ...
    def half_per(f, rep, kill=...) -> DMP: ...
    @classmethod
    def zero(cls, lev, dom, ring=...) -> Self: ...
    @classmethod
    def one(cls, lev, dom, ring=...) -> Self: ...
    def numer(f) -> DMP: ...
    def denom(f) -> DMP: ...
    def cancel(f) -> Self: ...
    def neg(f) -> Self: ...
    def add(f, g) -> Self: ...
    def sub(f, g) -> Self: ...
    def mul(f, g) -> Self: ...
    def pow(f, n) -> Self: ...
    def quo(f, g) -> Self: ...

    exquo = ...
    def invert(f, check=...) -> Self: ...
    @property
    def is_zero(f) -> bool: ...
    @property
    def is_one(f) -> bool: ...
    def __neg__(f) -> Self: ...
    def __add__(f, g) -> Self | NotImplementedType: ...
    def __radd__(f, g) -> Self | NotImplementedType: ...
    def __sub__(f, g) -> Self | NotImplementedType: ...
    def __rsub__(f, g) -> DMF | NotImplementedType: ...
    def __mul__(f, g) -> Self | NotImplementedType: ...
    def __rmul__(f, g) -> Self | NotImplementedType: ...
    def __pow__(f, n) -> Self: ...
    def __truediv__(f, g) -> Self | NotImplementedType: ...
    def __rtruediv__(self, g): ...
    def __eq__(f, g) -> bool: ...
    def __ne__(f, g) -> bool: ...
    def __lt__(f, g) -> bool: ...
    def __le__(f, g) -> bool: ...
    def __gt__(f, g) -> bool: ...
    def __ge__(f, g) -> bool: ...
    def __bool__(f) -> bool: ...

def init_normal_ANP(rep, mod, dom) -> ANP: ...

class ANP(PicklableWithSlots, CantSympify):
    __slots__ = ...
    def __init__(self, rep, mod, dom) -> None: ...
    def __repr__(f) -> str: ...
    def __hash__(f) -> int: ...
    def unify(
        f, g
    ) -> (
        tuple[Any, Callable[..., ANP], list[Any] | Any, list[Any] | Any, list[Any] | Any | list[list[Any]]]
        | tuple[Any, Callable[..., ANP], Any, Any, Any | list[Any] | list[list[Any]]]
    ): ...
    def per(f, rep, mod=..., dom=...) -> ANP: ...
    @classmethod
    def zero(cls, mod, dom) -> ANP: ...
    @classmethod
    def one(cls, mod, dom) -> ANP: ...
    def to_dict(f) -> dict[tuple[Literal[0]], Any] | dict[Any, Any]: ...
    def to_sympy_dict(f) -> dict[tuple[Literal[0]], Any] | dict[Any, Any]: ...
    def to_list(f) -> list[Any]: ...
    def to_sympy_list(f) -> list[Any]: ...
    def to_tuple(f) -> tuple[Any, ...]: ...
    @classmethod
    def from_list(cls, rep, mod, dom) -> ANP: ...
    def neg(f) -> ANP: ...
    def add(f, g) -> ANP: ...
    def sub(f, g) -> ANP: ...
    def mul(f, g) -> ANP: ...
    def pow(f, n) -> ANP: ...
    def div(f, g) -> tuple[ANP, ANP]: ...
    def rem(f, g) -> ANP: ...
    def quo(f, g) -> ANP: ...

    exquo = ...
    def LC(f): ...
    def TC(f): ...
    @property
    def is_zero(f) -> bool: ...
    @property
    def is_one(f) -> bool: ...
    @property
    def is_ground(f) -> bool: ...
    def __pos__(f) -> Self: ...
    def __neg__(f) -> ANP: ...
    def __add__(f, g) -> ANP | NotImplementedType: ...
    def __radd__(f, g) -> ANP | NotImplementedType: ...
    def __sub__(f, g) -> ANP | NotImplementedType: ...
    def __rsub__(f, g) -> ANP | NotImplementedType: ...
    def __mul__(f, g) -> ANP | NotImplementedType: ...
    def __rmul__(f, g) -> ANP | NotImplementedType: ...
    def __pow__(f, n) -> ANP: ...
    def __divmod__(f, g) -> tuple[ANP, ANP]: ...
    def __mod__(f, g) -> ANP: ...
    def __truediv__(f, g) -> ANP | NotImplementedType: ...
    def __eq__(f, g) -> bool: ...
    def __ne__(f, g) -> bool: ...
    def __lt__(f, g) -> bool: ...
    def __le__(f, g) -> bool: ...
    def __gt__(f, g) -> bool: ...
    def __ge__(f, g) -> bool: ...
    def __bool__(f) -> bool: ...