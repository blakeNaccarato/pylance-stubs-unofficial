from typing import Any, Self
from sympy import Complement, ConditionSet, FiniteSet, Intersection
from sympy.core import Basic
from sympy.sets.sets import Set, Union

class ImplicitRegion(Basic):
    def __new__(cls, variables, equation) -> Self:
        ...
    
    @property
    def variables(self) -> Basic:
        ...
    
    @property
    def equation(self) -> Basic:
        ...
    
    @property
    def degree(self) -> Any:
        ...
    
    def regular_point(self) -> tuple[Any] | tuple[Any, Any] | tuple[int, int, Any] | type[list[Any]]:
        ...
    
    def singular_points(self) -> FiniteSet | Set | Intersection | Union | Complement | ConditionSet:
        ...
    
    def multiplicity(self, point) -> Any:
        ...
    
    def rational_parametrization(self, parameters=..., reg_point=...) -> tuple[Basic] | tuple[Any, Any] | tuple[Any, Any, Any]:
        ...
    


def conic_coeff(variables, equation) -> tuple[Any, Any, Any, Any, Any, Any]:
    ...

