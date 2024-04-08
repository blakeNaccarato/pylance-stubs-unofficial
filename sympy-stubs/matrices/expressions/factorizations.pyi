from typing import Any
from sympy.matrices.expressions import MatrixExpr

class Factorization(MatrixExpr):
    arg = ...
    shape = ...


class LofLU(Factorization):
    @property
    def predicates(self) -> tuple[Any]:
        ...
    


class UofLU(Factorization):
    @property
    def predicates(self) -> tuple[Any]:
        ...
    


class LofCholesky(LofLU):
    ...


class UofCholesky(UofLU):
    ...


class QofQR(Factorization):
    @property
    def predicates(self) -> tuple[Any]:
        ...
    


class RofQR(Factorization):
    @property
    def predicates(self) -> tuple[Any]:
        ...
    


class EigenVectors(Factorization):
    @property
    def predicates(self) -> tuple[Any]:
        ...
    


class EigenValues(Factorization):
    @property
    def predicates(self) -> tuple[Any]:
        ...
    


class UofSVD(Factorization):
    @property
    def predicates(self) -> tuple[Any]:
        ...
    


class SofSVD(Factorization):
    @property
    def predicates(self) -> tuple[Any]:
        ...
    


class VofSVD(Factorization):
    @property
    def predicates(self) -> tuple[Any]:
        ...
    


def lu(expr) -> tuple[LofLU, UofLU]:
    ...

def qr(expr) -> tuple[QofQR, RofQR]:
    ...

def eig(expr) -> tuple[EigenValues, EigenVectors]:
    ...

def svd(expr) -> tuple[UofSVD, SofSVD, VofSVD]:
    ...

