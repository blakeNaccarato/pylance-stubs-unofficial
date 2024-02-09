from collections.abc import (
    Callable,
    Hashable,
)

import numpy as np
from pandas.core.base import SelectionMixin
from pandas.core.frame import DataFrame
from pandas.core.generic import NDFrame
from pandas.core.groupby import ops
from pandas.core.indexes.api import Index
from pandas.core.series import Series

from pandas._typing import (
    Axis,
    KeysArgType,
    NDFrameT,
    npt,
)

class GroupByPlot:
    def __init__(self, groupby) -> None: ...
    def __call__(self, *args, **kwargs): ...
    def __getattr__(self, name: str): ...

class BaseGroupBy(SelectionMixin[NDFrameT]):
    level = ...
    as_index = ...
    keys = ...
    sort = ...
    group_keys = ...
    squeeze = ...
    observed = ...
    mutated = ...
    @property
    def obj(self) -> NDFrameT: ...
    axis = ...
    grouper = ...
    exclusions = ...
    def __len__(self) -> int: ...
    @property
    def groups(self) -> dict[Hashable, list[Hashable]]: ...
    @property
    def ngroups(self) -> int: ...
    @property
    def indices(self) -> dict[Hashable, Index | npt.NDArray[np.int_] | list[int]]: ...
    def pipe(self, func: Callable, *args, **kwargs):
        """
Apply a ``func`` with arguments to this GroupBy object and return its result.

Use `.pipe` when you want to improve readability by chaining together
functions that expect Series, DataFrames, GroupBy or Resampler objects.
Instead of writing

>>> h = lambda x, arg2, arg3: x + 1 - arg2 * arg3
>>> g = lambda x, arg1: x * 5 / arg1
>>> f = lambda x: x ** 4
>>> df = pd.DataFrame([["a", 4], ["b", 5]], columns=["group", "value"])
>>> h(g(f(df.groupby('group')), arg1=1), arg2=2, arg3=3)  # doctest: +SKIP

You can write

>>> (df.groupby('group')
...    .pipe(f)
...    .pipe(g, arg1=1)
...    .pipe(h, arg2=2, arg3=3))  # doctest: +SKIP

which is much more readable.

Parameters
----------
func : callable or tuple of (callable, str)
    Function to apply to this GroupBy object or, alternatively,
    a `(callable, data_keyword)` tuple where `data_keyword` is a
    string indicating the keyword of `callable` that expects the
    GroupBy object.
args : iterable, optional
       Positional arguments passed into `func`.
kwargs : dict, optional
         A dictionary of keyword arguments passed into `func`.

Returns
-------
the return type of `func`.

See Also
--------
Series.pipe : Apply a function with arguments to a series.
DataFrame.pipe: Apply a function with arguments to a dataframe.
apply : Apply function to each group instead of to the
    full GroupBy object.

Notes
-----
See more `here
<https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#piping-function-calls>`_

Examples
--------
>>> df = pd.DataFrame({'A': 'a b a b'.split(), 'B': [1, 2, 3, 4]})
>>> df
   A  B
0  a  1
1  b  2
2  a  3
3  b  4

To get the difference between each groups maximum and minimum value in one
pass, you can do

>>> df.groupby('A').pipe(lambda x: x.max() - x.min())
   B
A
a  2
b  2
        """
        pass
    plot = ...
    def get_group(self, name, obj: NDFrameT | None = ...) -> NDFrameT: ...

class GroupBy(BaseGroupBy[NDFrameT]):
    def count(self) -> DataFrame | Series: ...
    def mean(self, **kwargs) -> DataFrame | Series: ...
    def median(self, **kwargs) -> DataFrame | Series: ...
    def std(self, ddof: int = ..., numeric_only: bool = ...) -> DataFrame | Series: ...
    def var(self, ddof: int = ..., numeric_only: bool = ...) -> DataFrame | Series: ...
    def sem(self, ddof: int = ..., numeric_only: bool = ...) -> DataFrame | Series: ...
    def ohlc(self) -> DataFrame: ...
    def describe(self, **kwargs) -> DataFrame | Series: ...
    def resample(self, rule, *args, **kwargs): ...
    def rolling(self, *args, **kwargs): ...
    def expanding(self, *args, **kwargs): ...
    def ffill(self, limit: int | None = ...) -> DataFrame | Series: ...
    def bfill(self, limit: int | None = ...) -> DataFrame | Series: ...
    def nth(
        self, n: int | list[int], dropna: str | None = ...
    ) -> DataFrame | Series: ...
    def quantile(self, q=..., interpolation: str = ...): ...
    def ngroup(self, ascending: bool = ...) -> Series: ...
    def cumcount(self, ascending: bool = ...) -> Series: ...
    def rank(
        self,
        method: str = ...,
        ascending: bool = ...,
        na_option: str = ...,
        pct: bool = ...,
        axis: int = ...,
    ) -> DataFrame: ...
    def cummax(self, axis: Axis = ..., **kwargs) -> DataFrame | Series: ...
    def cummin(self, axis: Axis = ..., **kwargs) -> DataFrame | Series: ...
    def cumprod(self, axis: Axis = ..., **kwargs) -> DataFrame | Series: ...
    def cumsum(self, axis: Axis = ..., **kwargs) -> DataFrame | Series: ...
    def shift(self, periods: int = ..., freq=..., axis: Axis = ..., fill_value=...): ...
    def pct_change(
        self,
        periods: int = ...,
        fill_method: str = ...,
        limit=...,
        freq=...,
        axis: Axis = ...,
    ) -> DataFrame | Series: ...
    def head(self, n: int = ...) -> DataFrame | Series: ...
    def tail(self, n: int = ...) -> DataFrame | Series: ...
    # Surplus methods from original pylance stubs; should they go away?
    def first(self, **kwargs) -> DataFrame | Series: ...
    def last(self, **kwargs) -> DataFrame | Series: ...
    def max(self, **kwargs) -> DataFrame | Series: ...
    def min(self, **kwargs) -> DataFrame | Series: ...
    def size(self) -> Series[int]: ...

def get_groupby(
    obj: NDFrame,
    by: KeysArgType | None = ...,
    axis: int = ...,
    level=...,
    grouper: ops.BaseGrouper | None = ...,
    exclusions=...,
    selection=...,
    as_index: bool = ...,
    sort: bool = ...,
    group_keys: bool = ...,
    squeeze: bool = ...,
    observed: bool = ...,
    mutated: bool = ...,
) -> GroupBy:
    """
Class for grouping and aggregating relational data.

See aggregate, transform, and apply functions on this object.

It's easiest to use obj.groupby(...) to use GroupBy, but you can also do:

::

    grouped = groupby(obj, ...)

Parameters
----------
obj : pandas object
axis : int, default 0
level : int, default None
    Level of MultiIndex
groupings : list of Grouping objects
    Most users should ignore this
exclusions : array-like, optional
    List of columns to exclude
name : str
    Most users should ignore this

Returns
-------
**Attributes**
groups : dict
    {group name -> group labels}
len(grouped) : int
    Number of groups

Notes
-----
After grouping, see aggregate, apply, and transform functions. Here are
some other brief notes about usage. When grouping by multiple groups, the
result index will be a MultiIndex (hierarchical) by default.

Iteration produces (key, group) tuples, i.e. chunking the data by group. So
you can write code like:

::

    grouped = obj.groupby(keys, axis=axis)
    for key, group in grouped:
        # do something with the data

Function calls on GroupBy, if not specially implemented, "dispatch" to the
grouped data. So if you group a DataFrame and wish to invoke the std()
method on each group, you can simply do:

::

    df.groupby(mapper).std()

rather than

::

    df.groupby(mapper).aggregate(np.std)

You can pass arguments to these "wrapped" functions, too.

See the online documentation for full exposition on these topics and much
more
    """
    pass
