from collections.abc import (
    Callable,
    Generator,
    Hashable,
    Mapping,
)
from typing import (
    Generic,
    Literal,
    overload,
)

import numpy as np
from pandas import (
    DataFrame,
    Index,
    Series,
)
from pandas.core.groupby.generic import SeriesGroupBy
from pandas.core.groupby.groupby import BaseGroupBy
from typing_extensions import TypeAlias

from pandas._typing import (
    Axis,
    InterpolateOptions,
    NDFrameT,
    Scalar,
    npt,
)

_FrameGroupByFunc: TypeAlias = (
    Callable[[DataFrame], Scalar]
    | Callable[[DataFrame], Series]
    | Callable[[DataFrame], DataFrame]
    | np.ufunc
)
_FrameGroupByFuncTypes: TypeAlias = (
    _FrameGroupByFunc | str | list[_FrameGroupByFunc | str]
)
_FrameGroupByFuncArgs: TypeAlias = (
    _FrameGroupByFuncTypes | Mapping[Hashable, _FrameGroupByFuncTypes]
)

_SeriesGroupByFunc: TypeAlias = (
    Callable[[Series], Scalar] | Callable[[Series], Series] | np.ufunc
)
_SeriesGroupByFuncTypes: TypeAlias = (
    _SeriesGroupByFunc | str | list[_SeriesGroupByFunc | str]
)
_SeriesGroupByFuncArgs: TypeAlias = (
    _SeriesGroupByFuncTypes | Mapping[Hashable, _SeriesGroupByFunc | str]
)

class Resampler(BaseGroupBy, Generic[NDFrameT]):
    def __getattr__(self, attr: str) -> SeriesGroupBy: ...
    def __iter__(self) -> Generator[tuple[Hashable, NDFrameT], None, None]: ...
    @property
    def obj(self) -> NDFrameT: ...
    @property
    def ax(self) -> Index: ...
    @overload
    def pipe(
        self: Resampler[DataFrame],
        func: Callable[..., DataFrame]
        | tuple[Callable[..., DataFrame], str]
        | Callable[..., Series]
        | tuple[Callable[..., Series], str],
        *args,
        **kwargs,
    ) -> DataFrame:
        """
Apply a ``func`` with arguments to this Resampler object and return its result.

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
    Function to apply to this Resampler object or, alternatively,
    a `(callable, data_keyword)` tuple where `data_keyword` is a
    string indicating the keyword of `callable` that expects the
    Resampler object.
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
    full Resampler object.

Notes
-----
See more `here
<https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#piping-function-calls>`_

Examples
--------

    >>> df = pd.DataFrame({'A': [1, 2, 3, 4]},
    ...                   index=pd.date_range('2012-08-02', periods=4))
    >>> df
                A
    2012-08-02  1
    2012-08-03  2
    2012-08-04  3
    2012-08-05  4

    To get the difference between each 2-day period's maximum and minimum
    value in one pass, you can do

    >>> df.resample('2D').pipe(lambda x: x.max() - x.min())
                A
    2012-08-02  1
    2012-08-04  1
        """
        pass
    @overload
    def pipe(
        self: Resampler[DataFrame],
        func: Callable[..., Scalar] | tuple[Callable[..., Scalar], str],
        *args,
        **kwargs,
    ) -> Series: ...
    @overload
    def pipe(
        self: Resampler[Series],
        func: Callable[..., Series] | tuple[Callable[..., Series], str],
        *args,
        **kwargs,
    ) -> Series: ...
    @overload
    def pipe(
        self: Resampler[Series],
        func: Callable[..., Scalar] | tuple[Callable[..., Scalar], str],
        *args,
        **kwargs,
    ) -> Scalar: ...
    @overload
    def pipe(
        self: Resampler[Series],
        func: Callable[..., DataFrame] | tuple[Callable[..., DataFrame], str],
        *args,
        **kwargs,
    ) -> DataFrame: ...
    @overload
    def aggregate(
        self: Resampler[DataFrame],
        func: _FrameGroupByFuncArgs | None = ...,
        *args,
        **kwargs,
    ) -> Series | DataFrame:
        """
Aggregate using one or more operations over the specified axis.

Parameters
----------
func : function, str, list or dict
    Function to use for aggregating the data. If a function, must either
    work when passed a DataFrame or when passed to DataFrame.apply.

    Accepted combinations are:

    - function
    - string function name
    - list of functions and/or function names, e.g. ``[np.sum, 'mean']``
    - dict of axis labels -> functions, function names or list of such.

*args
    Positional arguments to pass to `func`.
**kwargs
    Keyword arguments to pass to `func`.

Returns
-------
scalar, Series or DataFrame

    The return can be:

    * scalar : when Series.agg is called with single function
    * Series : when DataFrame.agg is called with a single function
    * DataFrame : when DataFrame.agg is called with several functions

See Also
--------
DataFrame.groupby.aggregate : Aggregate using callable, string, dict,
    or list of string/callables.
DataFrame.resample.transform : Transforms the Series on each group
    based on the given function.
DataFrame.aggregate: Aggregate using one or more
    operations over the specified axis.

Notes
-----
The aggregation operations are always performed over an axis, either the
index (default) or the column axis. This behavior is different from
`numpy` aggregation functions (`mean`, `median`, `prod`, `sum`, `std`,
`var`), where the default is to compute the aggregation of the flattened
array, e.g., ``numpy.mean(arr_2d)`` as opposed to
``numpy.mean(arr_2d, axis=0)``.

`agg` is an alias for `aggregate`. Use the alias.

Functions that mutate the passed object can produce unexpected
behavior or errors and are not supported. See :ref:`gotchas.udf-mutation`
for more details.

A passed user-defined-function will be passed a Series for evaluation.

Examples
--------
>>> s = pd.Series([1, 2, 3, 4, 5],
...               index=pd.date_range('20130101', periods=5, freq='s'))
>>> s
2013-01-01 00:00:00    1
2013-01-01 00:00:01    2
2013-01-01 00:00:02    3
2013-01-01 00:00:03    4
2013-01-01 00:00:04    5
Freq: s, dtype: int64

>>> r = s.resample('2s')

>>> r.agg("sum")
2013-01-01 00:00:00    3
2013-01-01 00:00:02    7
2013-01-01 00:00:04    5
Freq: 2s, dtype: int64

>>> r.agg(['sum', 'mean', 'max'])
                     sum  mean  max
2013-01-01 00:00:00    3   1.5    2
2013-01-01 00:00:02    7   3.5    4
2013-01-01 00:00:04    5   5.0    5

>>> r.agg({'result': lambda x: x.mean() / x.std(),
...        'total': "sum"})
                       result  total
2013-01-01 00:00:00  2.121320      3
2013-01-01 00:00:02  4.949747      7
2013-01-01 00:00:04       NaN      5

>>> r.agg(average="mean", total="sum")
                         average  total
2013-01-01 00:00:00      1.5      3
2013-01-01 00:00:02      3.5      7
2013-01-01 00:00:04      5.0      5
        """
        pass
    @overload
    def aggregate(
        self: Resampler[Series],
        func: _SeriesGroupByFuncArgs | None = ...,
        *args,
        **kwargs,
    ) -> Series | DataFrame: ...
    agg = aggregate
    apply = aggregate
    def transform(
        self, arg: Callable[[Series], Series], *args, **kwargs
    ) -> NDFrameT: ...
    def ffill(self, limit: int | None = ...) -> NDFrameT: ...
    def nearest(self, limit: int | None = ...) -> NDFrameT: ...
    def bfill(self, limit: int | None = ...) -> NDFrameT: ...
    def fillna(
        self,
        method: Literal["pad", "backfill", "ffill", "bfill", "nearest"],
        limit: int | None = ...,
    ) -> NDFrameT: ...
    @overload
    def interpolate(
        self,
        method: InterpolateOptions = ...,
        *,
        axis: Axis = ...,
        limit: int | None = ...,
        inplace: Literal[True],
        limit_direction: Literal["forward", "backward", "both"] = ...,
        limit_area: Literal["inside", "outside"] | None = ...,
        downcast: Literal["infer"] | None = ...,
        **kwargs,
    ) -> None: ...
    @overload
    def interpolate(
        self,
        method: InterpolateOptions = ...,
        *,
        axis: Axis = ...,
        limit: int | None = ...,
        inplace: Literal[False] = ...,
        limit_direction: Literal["forward", "backward", "both"] = ...,
        limit_area: Literal["inside", "outside"] | None = ...,
        downcast: Literal["infer"] | None = ...,
        **kwargs,
    ) -> NDFrameT: ...
    def asfreq(self, fill_value: Scalar | None = ...) -> NDFrameT: ...
    def std(
        self, ddof: int = ..., numeric_only: bool = ..., *args, **kwargs
    ) -> NDFrameT: ...
    def var(
        self, ddof: int = ..., numeric_only: bool = ..., *args, **kwargs
    ) -> NDFrameT: ...
    def size(self) -> Series:
        """
Compute group sizes.

Returns
-------
DataFrame or Series
    Number of rows in each group as a Series if as_index is True
    or a DataFrame if as_index is False.

See Also
--------
Series.groupby : Apply a function groupby to a Series.
DataFrame.groupby : Apply a function groupby
    to each row or column of a DataFrame.

Examples
--------

For SeriesGroupBy:

>>> lst = ['a', 'a', 'b']
>>> ser = pd.Series([1, 2, 3], index=lst)
>>> ser
a     1
a     2
b     3
dtype: int64
>>> ser.groupby(level=0).size()
a    2
b    1
dtype: int64

>>> data = [[1, 2, 3], [1, 5, 6], [7, 8, 9]]
>>> df = pd.DataFrame(data, columns=["a", "b", "c"],
...                   index=["owl", "toucan", "eagle"])
>>> df
        a  b  c
owl     1  2  3
toucan  1  5  6
eagle   7  8  9
>>> df.groupby("a").size()
a
1    2
7    1
dtype: int64

For Resampler:

>>> ser = pd.Series([1, 2, 3], index=pd.DatetimeIndex(
...                 ['2023-01-01', '2023-01-15', '2023-02-01']))
>>> ser
2023-01-01    1
2023-01-15    2
2023-02-01    3
dtype: int64
>>> ser.resample('MS').size()
2023-01-01    2
2023-02-01    1
Freq: MS, dtype: int64
        """
        pass
    def count(self) -> NDFrameT:
        """
Compute count of group, excluding missing values.

Returns
-------
Series or DataFrame
    Count of values within each group.

See Also
--------
Series.groupby : Apply a function groupby to a Series.
DataFrame.groupby : Apply a function groupby
    to each row or column of a DataFrame.

Examples
--------
For SeriesGroupBy:

>>> lst = ['a', 'a', 'b']
>>> ser = pd.Series([1, 2, np.nan], index=lst)
>>> ser
a    1.0
a    2.0
b    NaN
dtype: float64
>>> ser.groupby(level=0).count()
a    2
b    0
dtype: int64

For DataFrameGroupBy:

>>> data = [[1, np.nan, 3], [1, np.nan, 6], [7, 8, 9]]
>>> df = pd.DataFrame(data, columns=["a", "b", "c"],
...                   index=["cow", "horse", "bull"])
>>> df
        a         b     c
cow     1       NaN     3
horse   1       NaN     6
bull    7       8.0     9
>>> df.groupby("a").count()
    b   c
a
1   0   2
7   1   1

For Resampler:

>>> ser = pd.Series([1, 2, 3, 4], index=pd.DatetimeIndex(
...                 ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15']))
>>> ser
2023-01-01    1
2023-01-15    2
2023-02-01    3
2023-02-15    4
dtype: int64
>>> ser.resample('MS').count()
2023-01-01    2
2023-02-01    2
Freq: MS, dtype: int64
        """
        pass
    def quantile(
        self,
        q: float | list[float] | npt.NDArray[np.float_] | Series[float] = ...,
        **kwargs,
    ) -> NDFrameT: ...
    def sum(
        self, numeric_only: bool = ..., min_count: int = ..., *args, **kwargs
    ) -> NDFrameT: ...
    def prod(
        self, numeric_only: bool = ..., min_count: int = ..., *args, **kwargs
    ) -> NDFrameT: ...
    def min(
        self, numeric_only: bool = ..., min_count: int = ..., *args, **kwargs
    ) -> NDFrameT: ...
    def max(
        self, numeric_only: bool = ..., min_count: int = ..., *args, **kwargs
    ) -> NDFrameT: ...
    def first(
        self, numeric_only: bool = ..., min_count: int = ..., *args, **kwargs
    ) -> NDFrameT:
        """
Compute the first non-null entry of each column.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.
min_count : int, default -1
    The required number of valid values to perform the operation. If fewer
    than ``min_count`` non-NA values are present the result will be NA.

Returns
-------
Series or DataFrame
    First non-null of values within each group.

See Also
--------
DataFrame.groupby : Apply a function groupby to each row or column of a
    DataFrame.
pandas.core.groupby.DataFrameGroupBy.last : Compute the last non-null entry
    of each column.
pandas.core.groupby.DataFrameGroupBy.nth : Take the nth row from each group.

Examples
--------
>>> df = pd.DataFrame(dict(A=[1, 1, 3], B=[None, 5, 6], C=[1, 2, 3],
...                        D=['3/11/2000', '3/12/2000', '3/13/2000']))
>>> df['D'] = pd.to_datetime(df['D'])
>>> df.groupby("A").first()
     B  C          D
A
1  5.0  1 2000-03-11
3  6.0  3 2000-03-13
>>> df.groupby("A").first(min_count=2)
    B    C          D
A
1 NaN  1.0 2000-03-11
3 NaN  NaN        NaT
>>> df.groupby("A").first(numeric_only=True)
     B  C
A
1  5.0  1
3  6.0  3
        """
        pass
    def last(
        self, numeric_only: bool = ..., min_count: int = ..., *args, **kwargs
    ) -> NDFrameT:
        """
Compute the last non-null entry of each column.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns. If None, will attempt to use
    everything, then use only numeric data.
min_count : int, default -1
    The required number of valid values to perform the operation. If fewer
    than ``min_count`` non-NA values are present the result will be NA.

Returns
-------
Series or DataFrame
    Last non-null of values within each group.

See Also
--------
DataFrame.groupby : Apply a function groupby to each row or column of a
    DataFrame.
pandas.core.groupby.DataFrameGroupBy.first : Compute the first non-null entry
    of each column.
pandas.core.groupby.DataFrameGroupBy.nth : Take the nth row from each group.

Examples
--------
>>> df = pd.DataFrame(dict(A=[1, 1, 3], B=[5, None, 6], C=[1, 2, 3]))
>>> df.groupby("A").last()
     B  C
A
1  5.0  2
3  6.0  3
        """
        pass
    def mean(self, numeric_only: bool = ..., *args, **kwargs) -> NDFrameT: ...
    def sem(self, numeric_only: bool = ..., *args, **kwargs) -> NDFrameT:
        """
Compute standard error of the mean of groups, excluding missing values.

For multiple groupings, the result index will be a MultiIndex.

Parameters
----------
ddof : int, default 1
    Degrees of freedom.

numeric_only : bool, default False
    Include only `float`, `int` or `boolean` data.

    .. versionadded:: 1.5.0

    .. versionchanged:: 2.0.0

        numeric_only now defaults to ``False``.

Returns
-------
Series or DataFrame
    Standard error of the mean of values within each group.

Examples
--------
For SeriesGroupBy:

>>> lst = ['a', 'a', 'b', 'b']
>>> ser = pd.Series([5, 10, 8, 14], index=lst)
>>> ser
a     5
a    10
b     8
b    14
dtype: int64
>>> ser.groupby(level=0).sem()
a    2.5
b    3.0
dtype: float64

For DataFrameGroupBy:

>>> data = [[1, 12, 11], [1, 15, 2], [2, 5, 8], [2, 6, 12]]
>>> df = pd.DataFrame(data, columns=["a", "b", "c"],
...                   index=["tuna", "salmon", "catfish", "goldfish"])
>>> df
           a   b   c
    tuna   1  12  11
  salmon   1  15   2
 catfish   2   5   8
goldfish   2   6  12
>>> df.groupby("a").sem()
      b  c
a
1    1.5  4.5
2    0.5  2.0

For Resampler:

>>> ser = pd.Series([1, 3, 2, 4, 3, 8],
...                 index=pd.DatetimeIndex(['2023-01-01',
...                                         '2023-01-10',
...                                         '2023-01-15',
...                                         '2023-02-01',
...                                         '2023-02-10',
...                                         '2023-02-15']))
>>> ser.resample('MS').sem()
2023-01-01    0.577350
2023-02-01    1.527525
Freq: MS, dtype: float64
        """
        pass
    def median(self, numeric_only: bool = ..., *args, **kwargs) -> NDFrameT:
        """
Compute median of groups, excluding missing values.

For multiple groupings, the result index will be a MultiIndex

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionchanged:: 2.0.0

        numeric_only no longer accepts ``None`` and defaults to False.

Returns
-------
Series or DataFrame
    Median of values within each group.

Examples
--------
For SeriesGroupBy:

>>> lst = ['a', 'a', 'a', 'b', 'b', 'b']
>>> ser = pd.Series([7, 2, 8, 4, 3, 3], index=lst)
>>> ser
a     7
a     2
a     8
b     4
b     3
b     3
dtype: int64
>>> ser.groupby(level=0).median()
a    7.0
b    3.0
dtype: float64

For DataFrameGroupBy:

>>> data = {'a': [1, 3, 5, 7, 7, 8, 3], 'b': [1, 4, 8, 4, 4, 2, 1]}
>>> df = pd.DataFrame(data, index=['dog', 'dog', 'dog',
...                   'mouse', 'mouse', 'mouse', 'mouse'])
>>> df
         a  b
  dog    1  1
  dog    3  4
  dog    5  8
mouse    7  4
mouse    7  4
mouse    8  2
mouse    3  1
>>> df.groupby(level=0).median()
         a    b
dog    3.0  4.0
mouse  7.0  3.0

For Resampler:

>>> ser = pd.Series([1, 2, 3, 3, 4, 5],
...                 index=pd.DatetimeIndex(['2023-01-01',
...                                         '2023-01-10',
...                                         '2023-01-15',
...                                         '2023-02-01',
...                                         '2023-02-10',
...                                         '2023-02-15']))
>>> ser.resample('MS').median()
2023-01-01    2.0
2023-02-01    4.0
Freq: MS, dtype: float64
        """
        pass
    def ohlc(self, *args, **kwargs) -> DataFrame:
        """
Compute open, high, low and close values of a group, excluding missing values.

For multiple groupings, the result index will be a MultiIndex

Returns
-------
DataFrame
    Open, high, low and close values within each group.

Examples
--------

For SeriesGroupBy:

>>> lst = ['SPX', 'CAC', 'SPX', 'CAC', 'SPX', 'CAC', 'SPX', 'CAC',]
>>> ser = pd.Series([3.4, 9.0, 7.2, 5.2, 8.8, 9.4, 0.1, 0.5], index=lst)
>>> ser
SPX     3.4
CAC     9.0
SPX     7.2
CAC     5.2
SPX     8.8
CAC     9.4
SPX     0.1
CAC     0.5
dtype: float64
>>> ser.groupby(level=0).ohlc()
     open  high  low  close
CAC   9.0   9.4  0.5    0.5
SPX   3.4   8.8  0.1    0.1

For DataFrameGroupBy:

>>> data = {2022: [1.2, 2.3, 8.9, 4.5, 4.4, 3, 2 , 1],
...         2023: [3.4, 9.0, 7.2, 5.2, 8.8, 9.4, 8.2, 1.0]}
>>> df = pd.DataFrame(data, index=['SPX', 'CAC', 'SPX', 'CAC',
...                   'SPX', 'CAC', 'SPX', 'CAC'])
>>> df
     2022  2023
SPX   1.2   3.4
CAC   2.3   9.0
SPX   8.9   7.2
CAC   4.5   5.2
SPX   4.4   8.8
CAC   3.0   9.4
SPX   2.0   8.2
CAC   1.0   1.0
>>> df.groupby(level=0).ohlc()
    2022                 2023
    open high  low close open high  low close
CAC  2.3  4.5  1.0   1.0  9.0  9.4  1.0   1.0
SPX  1.2  8.9  1.2   2.0  3.4  8.8  3.4   8.2

For Resampler:

>>> ser = pd.Series([1, 3, 2, 4, 3, 5],
...                 index=pd.DatetimeIndex(['2023-01-01',
...                                         '2023-01-10',
...                                         '2023-01-15',
...                                         '2023-02-01',
...                                         '2023-02-10',
...                                         '2023-02-15']))
>>> ser.resample('MS').ohlc()
            open  high  low  close
2023-01-01     1     3    1      2
2023-02-01     4     5    3      5
        """
        pass
    def nunique(self, *args, **kwargs) -> NDFrameT:
        """
Return number of unique elements in the group.

Returns
-------
Series
    Number of unique values within each group.

Examples
--------
For SeriesGroupby:

>>> lst = ['a', 'a', 'b', 'b']
>>> ser = pd.Series([1, 2, 3, 3], index=lst)
>>> ser
a    1
a    2
b    3
b    3
dtype: int64
>>> ser.groupby(level=0).nunique()
a    2
b    1
dtype: int64

For Resampler:

>>> ser = pd.Series([1, 2, 3, 3], index=pd.DatetimeIndex(
...                 ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15']))
>>> ser
2023-01-01    1
2023-01-15    2
2023-02-01    3
2023-02-15    3
dtype: int64
>>> ser.resample('MS').nunique()
2023-01-01    2
2023-02-01    1
Freq: MS, dtype: int64
        """
        pass
