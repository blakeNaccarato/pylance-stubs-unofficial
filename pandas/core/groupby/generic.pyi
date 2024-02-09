from collections.abc import (
    Callable,
    Iterable,
    Iterator,
    Sequence,
)
from typing import (
    Any,
    Generic,
    Literal,
    NamedTuple,
    overload,
)

from matplotlib.axes import (
    Axes as PlotAxes,
    SubplotBase as AxesSubplot,
)
from pandas.core.frame import DataFrame
from pandas.core.generic import NDFrame
from pandas.core.groupby.groupby import (  # , get_groupby as get_groupby
    GroupBy as GroupBy,
)
from pandas.core.groupby.grouper import Grouper
from pandas.core.series import Series
from typing_extensions import TypeAlias

from pandas._typing import (
    S1,
    AggFuncTypeBase,
    AggFuncTypeFrame,
    Axis,
    ByT,
    Level,
    ListLike,
    RandomState,
    Scalar,
)

AggScalar: TypeAlias = str | Callable[..., Any]
ScalarResult = ...

class NamedAgg(NamedTuple):
    column: str = ...
    aggfunc: AggScalar = ...

def generate_property(name: str, klass: type[NDFrame]): ...

class SeriesGroupBy(GroupBy, Generic[S1, ByT]):
    def any(self, skipna: bool = ...) -> Series[bool]: ...
    def all(self, skipna: bool = ...) -> Series[bool]: ...
    def apply(self, func, *args, **kwargs) -> Series:
        """
Apply function ``func`` group-wise and combine the results together.

The function passed to ``apply`` must take a series as its first
argument and return a DataFrame, Series or scalar. ``apply`` will
then take care of combining the results back together into a single
dataframe or series. ``apply`` is therefore a highly flexible
grouping method.

While ``apply`` is a very flexible method, its downside is that
using it can be quite a bit slower than using more specific methods
like ``agg`` or ``transform``. Pandas offers a wide range of method that will
be much faster than using ``apply`` for their specific purposes, so try to
use them before reaching for ``apply``.

Parameters
----------
func : callable
    A callable that takes a series as its first argument, and
    returns a dataframe, a series or a scalar. In addition the
    callable may take positional and keyword arguments.
include_groups : bool, default True
    When True, will attempt to apply ``func`` to the groupings in
    the case that they are columns of the DataFrame. If this raises a
    TypeError, the result will be computed with the groupings excluded.
    When False, the groupings will be excluded when applying ``func``.

    .. versionadded:: 2.2.0

    .. deprecated:: 2.2.0

       Setting include_groups to True is deprecated. Only the value
       False will be allowed in a future version of pandas.

args, kwargs : tuple and dict
    Optional positional and keyword arguments to pass to ``func``.

Returns
-------
Series or DataFrame

See Also
--------
pipe : Apply function to the full GroupBy object instead of to each
    group.
aggregate : Apply aggregate function to the GroupBy object.
transform : Apply function column-by-column to the GroupBy object.
Series.apply : Apply a function to a Series.
DataFrame.apply : Apply a function to each row or column of a DataFrame.

Notes
-----

.. versionchanged:: 1.3.0

    The resulting dtype will reflect the return value of the passed ``func``,
    see the examples below.

Functions that mutate the passed object can produce unexpected
behavior or errors and are not supported. See :ref:`gotchas.udf-mutation`
for more details.

Examples
--------

>>> s = pd.Series([0, 1, 2], index='a a b'.split())
>>> g1 = s.groupby(s.index, group_keys=False)
>>> g2 = s.groupby(s.index, group_keys=True)

From ``s`` above we can see that ``g`` has two groups, ``a`` and ``b``.
Notice that ``g1`` have ``g2`` have two groups, ``a`` and ``b``, and only
differ in their ``group_keys`` argument. Calling `apply` in various ways,
we can get different grouping results:

Example 1: The function passed to `apply` takes a Series as
its argument and returns a Series.  `apply` combines the result for
each group together into a new Series.

.. versionchanged:: 1.3.0

    The resulting dtype will reflect the return value of the passed ``func``.

>>> g1.apply(lambda x: x * 2 if x.name == 'a' else x / 2)
a    0.0
a    2.0
b    1.0
dtype: float64

In the above, the groups are not part of the index. We can have them included
by using ``g2`` where ``group_keys=True``:

>>> g2.apply(lambda x: x * 2 if x.name == 'a' else x / 2)
a  a    0.0
   a    2.0
b  b    1.0
dtype: float64

Example 2: The function passed to `apply` takes a Series as
its argument and returns a scalar. `apply` combines the result for
each group together into a Series, including setting the index as
appropriate:

>>> g1.apply(lambda x: x.max() - x.min())
a    1
b    0
dtype: int64

The ``group_keys`` argument has no effect here because the result is not
like-indexed (i.e. :ref:`a transform <groupby.transform>`) when compared
to the input.

>>> g2.apply(lambda x: x.max() - x.min())
a    1
b    0
dtype: int64
        """
        pass
    @overload
    def aggregate(self, func: list[AggFuncTypeBase], *args, **kwargs) -> DataFrame:
        """
Aggregate using one or more operations over the specified axis.

Parameters
----------
func : function, str, list, dict or None
    Function to use for aggregating the data. If a function, must either
    work when passed a Series or when passed to Series.apply.

    Accepted combinations are:

    - function
    - string function name
    - list of functions and/or function names, e.g. ``[np.sum, 'mean']``
    - None, in which case ``**kwargs`` are used with Named Aggregation. Here the
      output has one column for each element in ``**kwargs``. The name of the
      column is keyword, whereas the value determines the aggregation used to compute
      the values in the column.

      Can also accept a Numba JIT function with
      ``engine='numba'`` specified. Only passing a single function is supported
      with this engine.

      If the ``'numba'`` engine is chosen, the function must be
      a user defined function with ``values`` and ``index`` as the
      first and second arguments respectively in the function signature.
      Each group's index will be passed to the user defined function
      and optionally available for use.

    .. deprecated:: 2.1.0

        Passing a dictionary is deprecated and will raise in a future version
        of pandas. Pass a list of aggregations instead.
*args
    Positional arguments to pass to func.
engine : str, default None
    * ``'cython'`` : Runs the function through C-extensions from cython.
    * ``'numba'`` : Runs the function through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}`` and will be
      applied to the function

**kwargs
    * If ``func`` is None, ``**kwargs`` are used to define the output names and
      aggregations via Named Aggregation. See ``func`` entry.
    * Otherwise, keyword arguments to be passed into func.

Returns
-------
Series

See Also
--------
Series.groupby.apply : Apply function func group-wise
    and combine the results together.
Series.groupby.transform : Transforms the Series on each group
    based on the given function.
Series.aggregate : Aggregate using one or more
    operations over the specified axis.

Notes
-----
When using ``engine='numba'``, there will be no "fall back" behavior internally.
The group data and group index will be passed as numpy arrays to the JITed
user defined function, and no alternative execution attempts will be tried.

Functions that mutate the passed object can produce unexpected
behavior or errors and are not supported. See :ref:`gotchas.udf-mutation`
for more details.

.. versionchanged:: 1.3.0

    The resulting dtype will reflect the return value of the passed ``func``,
    see the examples below.

Examples
--------
>>> s = pd.Series([1, 2, 3, 4])

>>> s
0    1
1    2
2    3
3    4
dtype: int64

>>> s.groupby([1, 1, 2, 2]).min()
1    1
2    3
dtype: int64

>>> s.groupby([1, 1, 2, 2]).agg('min')
1    1
2    3
dtype: int64

>>> s.groupby([1, 1, 2, 2]).agg(['min', 'max'])
   min  max
1    1    2
2    3    4

The output column names can be controlled by passing
the desired column names and aggregations as keyword arguments.

>>> s.groupby([1, 1, 2, 2]).agg(
...     minimum='min',
...     maximum='max',
... )
   minimum  maximum
1        1        2
2        3        4

.. versionchanged:: 1.3.0

    The resulting dtype will reflect the return value of the aggregating function.

>>> s.groupby([1, 1, 2, 2]).agg(lambda x: x.astype(float).min())
1    1.0
2    3.0
dtype: float64
        """
        pass
    @overload
    def aggregate(self, func: AggFuncTypeBase, *args, **kwargs) -> Series: ...
    agg = aggregate
    def transform(self, func: Callable | str, *args, **kwargs) -> Series:
        """
Call function producing a same-indexed Series on each group.

Returns a Series having the same indexes as the original object
filled with the transformed values.

Parameters
----------
f : function, str
    Function to apply to each group. See the Notes section below for requirements.

    Accepted inputs are:

    - String
    - Python function
    - Numba JIT function with ``engine='numba'`` specified.

    Only passing a single function is supported with this engine.
    If the ``'numba'`` engine is chosen, the function must be
    a user defined function with ``values`` and ``index`` as the
    first and second arguments respectively in the function signature.
    Each group's index will be passed to the user defined function
    and optionally available for use.

    If a string is chosen, then it needs to be the name
    of the groupby method you want to use.
*args
    Positional arguments to pass to func.
engine : str, default None
    * ``'cython'`` : Runs the function through C-extensions from cython.
    * ``'numba'`` : Runs the function through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or the global setting ``compute.use_numba``

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}`` and will be
      applied to the function

**kwargs
    Keyword arguments to be passed into func.

Returns
-------
Series

See Also
--------
Series.groupby.apply : Apply function ``func`` group-wise and combine
    the results together.
Series.groupby.aggregate : Aggregate using one or more
    operations over the specified axis.
Series.transform : Call ``func`` on self producing a Series with the
    same axis shape as self.

Notes
-----
Each group is endowed the attribute 'name' in case you need to know
which group you are working on.

The current implementation imposes three requirements on f:

* f must return a value that either has the same shape as the input
  subframe or can be broadcast to the shape of the input subframe.
  For example, if `f` returns a scalar it will be broadcast to have the
  same shape as the input subframe.
* if this is a DataFrame, f must support application column-by-column
  in the subframe. If f also supports application to the entire subframe,
  then a fast path is used starting from the second chunk.
* f must not mutate groups. Mutation is not supported and may
  produce unexpected results. See :ref:`gotchas.udf-mutation` for more details.

When using ``engine='numba'``, there will be no "fall back" behavior internally.
The group data and group index will be passed as numpy arrays to the JITed
user defined function, and no alternative execution attempts will be tried.

.. versionchanged:: 1.3.0

    The resulting dtype will reflect the return value of the passed ``func``,
    see the examples below.

.. versionchanged:: 2.0.0

    When using ``.transform`` on a grouped DataFrame and the transformation function
    returns a DataFrame, pandas now aligns the result's index
    with the input's index. You can call ``.to_numpy()`` on the
    result of the transformation function to avoid alignment.

Examples
--------

>>> ser = pd.Series([390.0, 350.0, 30.0, 20.0],
...                 index=["Falcon", "Falcon", "Parrot", "Parrot"],
...                 name="Max Speed")
>>> grouped = ser.groupby([1, 1, 2, 2])
>>> grouped.transform(lambda x: (x - x.mean()) / x.std())
    Falcon    0.707107
    Falcon   -0.707107
    Parrot    0.707107
    Parrot   -0.707107
    Name: Max Speed, dtype: float64

Broadcast result of the transformation

>>> grouped.transform(lambda x: x.max() - x.min())
Falcon    40.0
Falcon    40.0
Parrot    10.0
Parrot    10.0
Name: Max Speed, dtype: float64

>>> grouped.transform("mean")
Falcon    370.0
Falcon    370.0
Parrot     25.0
Parrot     25.0
Name: Max Speed, dtype: float64

.. versionchanged:: 1.3.0

The resulting dtype will reflect the return value of the passed ``func``,
for example:

>>> grouped.transform(lambda x: x.astype(int).max())
Falcon    390
Falcon    390
Parrot     30
Parrot     30
Name: Max Speed, dtype: int64
        """
        pass
    def filter(self, func, dropna: bool = ..., *args, **kwargs): ...
    def nunique(self, dropna: bool = ...) -> Series: ...
    def describe(self, **kwargs) -> DataFrame:
        """
Generate descriptive statistics.

Descriptive statistics include those that summarize the central
tendency, dispersion and shape of a
dataset's distribution, excluding ``NaN`` values.

Analyzes both numeric and object series, as well
as ``DataFrame`` column sets of mixed data types. The output
will vary depending on what is provided. Refer to the notes
below for more detail.

Parameters
----------
percentiles : list-like of numbers, optional
    The percentiles to include in the output. All should
    fall between 0 and 1. The default is
    ``[.25, .5, .75]``, which returns the 25th, 50th, and
    75th percentiles.
include : 'all', list-like of dtypes or None (default), optional
    A white list of data types to include in the result. Ignored
    for ``Series``. Here are the options:

    - 'all' : All columns of the input will be included in the output.
    - A list-like of dtypes : Limits the results to the
      provided data types.
      To limit the result to numeric types submit
      ``numpy.number``. To limit it instead to object columns submit
      the ``numpy.object`` data type. Strings
      can also be used in the style of
      ``select_dtypes`` (e.g. ``df.describe(include=['O'])``). To
      select pandas categorical columns, use ``'category'``
    - None (default) : The result will include all numeric columns.
exclude : list-like of dtypes or None (default), optional,
    A black list of data types to omit from the result. Ignored
    for ``Series``. Here are the options:

    - A list-like of dtypes : Excludes the provided data types
      from the result. To exclude numeric types submit
      ``numpy.number``. To exclude object columns submit the data
      type ``numpy.object``. Strings can also be used in the style of
      ``select_dtypes`` (e.g. ``df.describe(exclude=['O'])``). To
      exclude pandas categorical columns, use ``'category'``
    - None (default) : The result will exclude nothing.

Returns
-------
Series or DataFrame
    Summary statistics of the Series or Dataframe provided.

See Also
--------
DataFrame.count: Count number of non-NA/null observations.
DataFrame.max: Maximum of the values in the object.
DataFrame.min: Minimum of the values in the object.
DataFrame.mean: Mean of the values.
DataFrame.std: Standard deviation of the observations.
DataFrame.select_dtypes: Subset of a DataFrame including/excluding
    columns based on their dtype.

Notes
-----
For numeric data, the result's index will include ``count``,
``mean``, ``std``, ``min``, ``max`` as well as lower, ``50`` and
upper percentiles. By default the lower percentile is ``25`` and the
upper percentile is ``75``. The ``50`` percentile is the
same as the median.

For object data (e.g. strings or timestamps), the result's index
will include ``count``, ``unique``, ``top``, and ``freq``. The ``top``
is the most common value. The ``freq`` is the most common value's
frequency. Timestamps also include the ``first`` and ``last`` items.

If multiple object values have the highest count, then the
``count`` and ``top`` results will be arbitrarily chosen from
among those with the highest count.

For mixed data types provided via a ``DataFrame``, the default is to
return only an analysis of numeric columns. If the dataframe consists
only of object and categorical data without any numeric columns, the
default is to return an analysis of both the object and categorical
columns. If ``include='all'`` is provided as an option, the result
will include a union of attributes of each type.

The `include` and `exclude` parameters can be used to limit
which columns in a ``DataFrame`` are analyzed for the output.
The parameters are ignored when analyzing a ``Series``.

Examples
--------
Describing a numeric ``Series``.

>>> s = pd.Series([1, 2, 3])
>>> s.describe()
count    3.0
mean     2.0
std      1.0
min      1.0
25%      1.5
50%      2.0
75%      2.5
max      3.0
dtype: float64

Describing a categorical ``Series``.

>>> s = pd.Series(['a', 'a', 'b', 'c'])
>>> s.describe()
count     4
unique    3
top       a
freq      2
dtype: object

Describing a timestamp ``Series``.

>>> s = pd.Series([
...     np.datetime64("2000-01-01"),
...     np.datetime64("2010-01-01"),
...     np.datetime64("2010-01-01")
... ])
>>> s.describe()
count                      3
mean     2006-09-01 08:00:00
min      2000-01-01 00:00:00
25%      2004-12-31 12:00:00
50%      2010-01-01 00:00:00
75%      2010-01-01 00:00:00
max      2010-01-01 00:00:00
dtype: object

Describing a ``DataFrame``. By default only numeric fields
are returned.

>>> df = pd.DataFrame({'categorical': pd.Categorical(['d', 'e', 'f']),
...                    'numeric': [1, 2, 3],
...                    'object': ['a', 'b', 'c']
...                    })
>>> df.describe()
       numeric
count      3.0
mean       2.0
std        1.0
min        1.0
25%        1.5
50%        2.0
75%        2.5
max        3.0

Describing all columns of a ``DataFrame`` regardless of data type.

>>> df.describe(include='all')  # doctest: +SKIP
       categorical  numeric object
count            3      3.0      3
unique           3      NaN      3
top              f      NaN      a
freq             1      NaN      1
mean           NaN      2.0    NaN
std            NaN      1.0    NaN
min            NaN      1.0    NaN
25%            NaN      1.5    NaN
50%            NaN      2.0    NaN
75%            NaN      2.5    NaN
max            NaN      3.0    NaN

Describing a column from a ``DataFrame`` by accessing it as
an attribute.

>>> df.numeric.describe()
count    3.0
mean     2.0
std      1.0
min      1.0
25%      1.5
50%      2.0
75%      2.5
max      3.0
Name: numeric, dtype: float64

Including only numeric columns in a ``DataFrame`` description.

>>> df.describe(include=[np.number])
       numeric
count      3.0
mean       2.0
std        1.0
min        1.0
25%        1.5
50%        2.0
75%        2.5
max        3.0

Including only string columns in a ``DataFrame`` description.

>>> df.describe(include=[object])  # doctest: +SKIP
       object
count       3
unique      3
top         a
freq        1

Including only categorical columns from a ``DataFrame`` description.

>>> df.describe(include=['category'])
       categorical
count            3
unique           3
top              d
freq             1

Excluding numeric columns from a ``DataFrame`` description.

>>> df.describe(exclude=[np.number])  # doctest: +SKIP
       categorical object
count            3      3
unique           3      3
top              f      a
freq             1      1

Excluding object columns from a ``DataFrame`` description.

>>> df.describe(exclude=[object])  # doctest: +SKIP
       categorical  numeric
count            3      3.0
unique           3      NaN
top              f      NaN
freq             1      NaN
mean           NaN      2.0
std            NaN      1.0
min            NaN      1.0
25%            NaN      1.5
50%            NaN      2.0
75%            NaN      2.5
max            NaN      3.0
        """
        pass
    @overload
    def value_counts(
        self,
        normalize: Literal[False] = ...,
        sort: bool = ...,
        ascending: bool = ...,
        bins=...,
        dropna: bool = ...,
    ) -> Series[int]: ...
    @overload
    def value_counts(
        self,
        normalize: Literal[True],
        sort: bool = ...,
        ascending: bool = ...,
        bins=...,
        dropna: bool = ...,
    ) -> Series[float]: ...
    def count(self) -> Series[int]: ...
    def pct_change(
        self,
        periods: int = ...,
        fill_method: str = ...,
        limit=...,
        freq=...,
        axis: Axis = ...,
    ) -> Series[float]: ...
    # Overrides and others from original pylance stubs
    @property
    def is_monotonic_increasing(self) -> bool: ...
    @property
    def is_monotonic_decreasing(self) -> bool: ...
    def bfill(self, limit: int | None = ...) -> Series[S1]: ...
    def cummax(self, axis: Axis = ..., **kwargs) -> Series[S1]: ...
    def cummin(self, axis: Axis = ..., **kwargs) -> Series[S1]: ...
    def cumprod(self, axis: Axis = ..., **kwargs) -> Series[S1]: ...
    def cumsum(self, axis: Axis = ..., **kwargs) -> Series[S1]: ...
    def ffill(self, limit: int | None = ...) -> Series[S1]: ...
    def first(self, **kwargs) -> Series[S1]: ...
    def head(self, n: int = ...) -> Series[S1]: ...
    def last(self, **kwargs) -> Series[S1]: ...
    def max(self, **kwargs) -> Series[S1]: ...
    def mean(self, **kwargs) -> Series[S1]: ...
    def median(self, **kwargs) -> Series[S1]: ...
    def min(self, **kwargs) -> Series[S1]: ...
    def nlargest(self, n: int = ..., keep: str = ...) -> Series[S1]:
        """
Return the largest `n` elements.

Parameters
----------
n : int, default 5
    Return this many descending sorted values.
keep : {'first', 'last', 'all'}, default 'first'
    When there are duplicate values that cannot all fit in a
    Series of `n` elements:

    - ``first`` : return the first `n` occurrences in order
      of appearance.
    - ``last`` : return the last `n` occurrences in reverse
      order of appearance.
    - ``all`` : keep all occurrences. This can result in a Series of
      size larger than `n`.

Returns
-------
Series
    The `n` largest values in the Series, sorted in decreasing order.

See Also
--------
Series.nsmallest: Get the `n` smallest elements.
Series.sort_values: Sort Series by values.
Series.head: Return the first `n` rows.

Notes
-----
Faster than ``.sort_values(ascending=False).head(n)`` for small `n`
relative to the size of the ``Series`` object.

Examples
--------
>>> countries_population = {"Italy": 59000000, "France": 65000000,
...                         "Malta": 434000, "Maldives": 434000,
...                         "Brunei": 434000, "Iceland": 337000,
...                         "Nauru": 11300, "Tuvalu": 11300,
...                         "Anguilla": 11300, "Montserrat": 5200}
>>> s = pd.Series(countries_population)
>>> s
Italy       59000000
France      65000000
Malta         434000
Maldives      434000
Brunei        434000
Iceland       337000
Nauru          11300
Tuvalu         11300
Anguilla       11300
Montserrat      5200
dtype: int64

The `n` largest elements where ``n=5`` by default.

>>> s.nlargest()
France      65000000
Italy       59000000
Malta         434000
Maldives      434000
Brunei        434000
dtype: int64

The `n` largest elements where ``n=3``. Default `keep` value is 'first'
so Malta will be kept.

>>> s.nlargest(3)
France    65000000
Italy     59000000
Malta       434000
dtype: int64

The `n` largest elements where ``n=3`` and keeping the last duplicates.
Brunei will be kept since it is the last with value 434000 based on
the index order.

>>> s.nlargest(3, keep='last')
France      65000000
Italy       59000000
Brunei        434000
dtype: int64

The `n` largest elements where ``n=3`` with all duplicates kept. Note
that the returned Series has five elements due to the three duplicates.

>>> s.nlargest(3, keep='all')
France      65000000
Italy       59000000
Malta         434000
Maldives      434000
Brunei        434000
dtype: int64
        """
        pass
    def nsmallest(self, n: int = ..., keep: str = ...) -> Series[S1]:
        """
Return the smallest `n` elements.

Parameters
----------
n : int, default 5
    Return this many ascending sorted values.
keep : {'first', 'last', 'all'}, default 'first'
    When there are duplicate values that cannot all fit in a
    Series of `n` elements:

    - ``first`` : return the first `n` occurrences in order
      of appearance.
    - ``last`` : return the last `n` occurrences in reverse
      order of appearance.
    - ``all`` : keep all occurrences. This can result in a Series of
      size larger than `n`.

Returns
-------
Series
    The `n` smallest values in the Series, sorted in increasing order.

See Also
--------
Series.nlargest: Get the `n` largest elements.
Series.sort_values: Sort Series by values.
Series.head: Return the first `n` rows.

Notes
-----
Faster than ``.sort_values().head(n)`` for small `n` relative to
the size of the ``Series`` object.

Examples
--------
>>> countries_population = {"Italy": 59000000, "France": 65000000,
...                         "Brunei": 434000, "Malta": 434000,
...                         "Maldives": 434000, "Iceland": 337000,
...                         "Nauru": 11300, "Tuvalu": 11300,
...                         "Anguilla": 11300, "Montserrat": 5200}
>>> s = pd.Series(countries_population)
>>> s
Italy       59000000
France      65000000
Brunei        434000
Malta         434000
Maldives      434000
Iceland       337000
Nauru          11300
Tuvalu         11300
Anguilla       11300
Montserrat      5200
dtype: int64

The `n` smallest elements where ``n=5`` by default.

>>> s.nsmallest()
Montserrat    5200
Nauru        11300
Tuvalu       11300
Anguilla     11300
Iceland     337000
dtype: int64

The `n` smallest elements where ``n=3``. Default `keep` value is
'first' so Nauru and Tuvalu will be kept.

>>> s.nsmallest(3)
Montserrat   5200
Nauru       11300
Tuvalu      11300
dtype: int64

The `n` smallest elements where ``n=3`` and keeping the last
duplicates. Anguilla and Tuvalu will be kept since they are the last
with value 11300 based on the index order.

>>> s.nsmallest(3, keep='last')
Montserrat   5200
Anguilla    11300
Tuvalu      11300
dtype: int64

The `n` smallest elements where ``n=3`` with all duplicates kept. Note
that the returned Series has four elements due to the three duplicates.

>>> s.nsmallest(3, keep='all')
Montserrat   5200
Nauru       11300
Tuvalu      11300
Anguilla    11300
dtype: int64
        """
        pass
    def nth(self, n: int | Sequence[int], dropna: str | None = ...) -> Series[S1]: ...
    def sum(
        self,
        numeric_only: bool = ...,
        min_count: int = ...,
        engine=...,
        engine_kwargs=...,
    ) -> Series[S1]: ...
    def prod(self, numeric_only: bool = ..., min_count: int = ...) -> Series[S1]: ...
    def sem(self, ddof: int = ..., numeric_only: bool = ...) -> Series[float]: ...
    def std(self, ddof: int = ..., numeric_only: bool = ...) -> Series[float]: ...
    def var(self, ddof: int = ..., numeric_only: bool = ...) -> Series[float]: ...
    def tail(self, n: int = ...) -> Series[S1]: ...
    def unique(self) -> Series: ...
    def hist(
        self,
        by=...,
        ax: PlotAxes | None = ...,
        grid: bool = ...,
        xlabelsize: int | None = ...,
        xrot: float | None = ...,
        ylabelsize: int | None = ...,
        yrot: float | None = ...,
        figsize: tuple[float, float] | None = ...,
        bins: int | Sequence = ...,
        backend: str | None = ...,
        legend: bool = ...,
        **kwargs,
    ) -> AxesSubplot:
        """
Draw histogram of the input series using matplotlib.

Parameters
----------
by : object, optional
    If passed, then used to form histograms for separate groups.
ax : matplotlib axis object
    If not passed, uses gca().
grid : bool, default True
    Whether to show axis grid lines.
xlabelsize : int, default None
    If specified changes the x-axis label size.
xrot : float, default None
    Rotation of x axis labels.
ylabelsize : int, default None
    If specified changes the y-axis label size.
yrot : float, default None
    Rotation of y axis labels.
figsize : tuple, default None
    Figure size in inches by default.
bins : int or sequence, default 10
    Number of histogram bins to be used. If an integer is given, bins + 1
    bin edges are calculated and returned. If bins is a sequence, gives
    bin edges, including left edge of first bin and right edge of last
    bin. In this case, bins is returned unmodified.
backend : str, default None
    Backend to use instead of the backend specified in the option
    ``plotting.backend``. For instance, 'matplotlib'. Alternatively, to
    specify the ``plotting.backend`` for the whole session, set
    ``pd.options.plotting.backend``.
legend : bool, default False
    Whether to show the legend.

**kwargs
    To be passed to the actual plotting function.

Returns
-------
matplotlib.AxesSubplot
    A histogram plot.

See Also
--------
matplotlib.axes.Axes.hist : Plot a histogram using matplotlib.

Examples
--------
For Series:

.. plot::
    :context: close-figs

    >>> lst = ['a', 'a', 'a', 'b', 'b', 'b']
    >>> ser = pd.Series([1, 2, 2, 4, 6, 6], index=lst)
    >>> hist = ser.hist()

For Groupby:

.. plot::
    :context: close-figs

    >>> lst = ['a', 'a', 'a', 'b', 'b', 'b']
    >>> ser = pd.Series([1, 2, 2, 4, 6, 6], index=lst)
    >>> hist = ser.groupby(level=0).hist()
        """
        pass
    def idxmax(self, axis: Axis = ..., skipna: bool = ...) -> Series:
        """
Return the row label of the maximum value.

If multiple values equal the maximum, the first row label with that
value is returned.

Parameters
----------
axis : {0 or 'index'}
    Unused. Parameter needed for compatibility with DataFrame.
skipna : bool, default True
    Exclude NA/null values. If the entire Series is NA, the result
    will be NA.
*args, **kwargs
    Additional arguments and keywords have no effect but might be
    accepted for compatibility with NumPy.

Returns
-------
Index
    Label of the maximum value.

Raises
------
ValueError
    If the Series is empty.

See Also
--------
numpy.argmax : Return indices of the maximum values
    along the given axis.
DataFrame.idxmax : Return index of first occurrence of maximum
    over requested axis.
Series.idxmin : Return index *label* of the first occurrence
    of minimum of values.

Notes
-----
This method is the Series version of ``ndarray.argmax``. This method
returns the label of the maximum, while ``ndarray.argmax`` returns
the position. To get the position, use ``series.values.argmax()``.

Examples
--------
>>> s = pd.Series(data=[1, None, 4, 3, 4],
...               index=['A', 'B', 'C', 'D', 'E'])
>>> s
A    1.0
B    NaN
C    4.0
D    3.0
E    4.0
dtype: float64

>>> s.idxmax()
'C'

If `skipna` is False and there is an NA value in the data,
the function returns ``nan``.

>>> s.idxmax(skipna=False)
nan
        """
        pass
    def idxmin(self, axis: Axis = ..., skipna: bool = ...) -> Series:
        """
Return the row label of the minimum value.

If multiple values equal the minimum, the first row label with that
value is returned.

Parameters
----------
axis : {0 or 'index'}
    Unused. Parameter needed for compatibility with DataFrame.
skipna : bool, default True
    Exclude NA/null values. If the entire Series is NA, the result
    will be NA.
*args, **kwargs
    Additional arguments and keywords have no effect but might be
    accepted for compatibility with NumPy.

Returns
-------
Index
    Label of the minimum value.

Raises
------
ValueError
    If the Series is empty.

See Also
--------
numpy.argmin : Return indices of the minimum values
    along the given axis.
DataFrame.idxmin : Return index of first occurrence of minimum
    over requested axis.
Series.idxmax : Return index *label* of the first occurrence
    of maximum of values.

Notes
-----
This method is the Series version of ``ndarray.argmin``. This method
returns the label of the minimum, while ``ndarray.argmin`` returns
the position. To get the position, use ``series.values.argmin()``.

Examples
--------
>>> s = pd.Series(data=[1, None, 4, 1],
...               index=['A', 'B', 'C', 'D'])
>>> s
A    1.0
B    NaN
C    4.0
D    1.0
dtype: float64

>>> s.idxmin()
'A'

If `skipna` is False and there is an NA value in the data,
the function returns ``nan``.

>>> s.idxmin(skipna=False)
nan
        """
        pass
    def __iter__(self) -> Iterator[tuple[ByT, Series[S1]]]: ...
    def diff(self, periods: int = ..., axis: Axis = ...) -> Series: ...

class DataFrameGroupBy(GroupBy, Generic[ByT]):
    def any(self, skipna: bool = ...) -> DataFrame: ...
    def all(self, skipna: bool = ...) -> DataFrame: ...
    # error: Overload 3 for "apply" will never be used because its parameters overlap overload 1
    @overload
    def apply(  # type: ignore[overload-overlap]
        self,
        func: Callable[[DataFrame], Scalar | list | dict],
        *args,
        **kwargs,
    ) -> Series: ...
    @overload
    def apply(
        self,
        func: Callable[[DataFrame], Series | DataFrame],
        *args,
        **kwargs,
    ) -> DataFrame: ...
    @overload
    def apply(  # pyright: ignore[reportOverlappingOverload]
        self,
        func: Callable[[Iterable], float],
        *args,
        **kwargs,
    ) -> DataFrame: ...
    # error: overload 1 overlaps overload 2 because of different return types
    @overload
    def aggregate(self, arg: Literal["size"]) -> Series: ...  # type: ignore[overload-overlap]  # pyright: ignore[reportOverlappingOverload]
    @overload
    def aggregate(self, arg: AggFuncTypeFrame = ..., *args, **kwargs) -> DataFrame:
        """
Aggregate using one or more operations over the specified axis.

Parameters
----------
func : function, str, list, dict or None
    Function to use for aggregating the data. If a function, must either
    work when passed a DataFrame or when passed to DataFrame.apply.

    Accepted combinations are:

    - function
    - string function name
    - list of functions and/or function names, e.g. ``[np.sum, 'mean']``
    - dict of axis labels -> functions, function names or list of such.
    - None, in which case ``**kwargs`` are used with Named Aggregation. Here the
      output has one column for each element in ``**kwargs``. The name of the
      column is keyword, whereas the value determines the aggregation used to compute
      the values in the column.

      Can also accept a Numba JIT function with
      ``engine='numba'`` specified. Only passing a single function is supported
      with this engine.

      If the ``'numba'`` engine is chosen, the function must be
      a user defined function with ``values`` and ``index`` as the
      first and second arguments respectively in the function signature.
      Each group's index will be passed to the user defined function
      and optionally available for use.

*args
    Positional arguments to pass to func.
engine : str, default None
    * ``'cython'`` : Runs the function through C-extensions from cython.
    * ``'numba'`` : Runs the function through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}`` and will be
      applied to the function

**kwargs
    * If ``func`` is None, ``**kwargs`` are used to define the output names and
      aggregations via Named Aggregation. See ``func`` entry.
    * Otherwise, keyword arguments to be passed into func.

Returns
-------
DataFrame

See Also
--------
DataFrame.groupby.apply : Apply function func group-wise
    and combine the results together.
DataFrame.groupby.transform : Transforms the Series on each group
    based on the given function.
DataFrame.aggregate : Aggregate using one or more
    operations over the specified axis.

Notes
-----
When using ``engine='numba'``, there will be no "fall back" behavior internally.
The group data and group index will be passed as numpy arrays to the JITed
user defined function, and no alternative execution attempts will be tried.

Functions that mutate the passed object can produce unexpected
behavior or errors and are not supported. See :ref:`gotchas.udf-mutation`
for more details.

.. versionchanged:: 1.3.0

    The resulting dtype will reflect the return value of the passed ``func``,
    see the examples below.

Examples
--------
>>> data = {"A": [1, 1, 2, 2],
...         "B": [1, 2, 3, 4],
...         "C": [0.362838, 0.227877, 1.267767, -0.562860]}
>>> df = pd.DataFrame(data)
>>> df
   A  B         C
0  1  1  0.362838
1  1  2  0.227877
2  2  3  1.267767
3  2  4 -0.562860

The aggregation is for each column.

>>> df.groupby('A').agg('min')
   B         C
A
1  1  0.227877
2  3 -0.562860

Multiple aggregations

>>> df.groupby('A').agg(['min', 'max'])
    B             C
  min max       min       max
A
1   1   2  0.227877  0.362838
2   3   4 -0.562860  1.267767

Select a column for aggregation

>>> df.groupby('A').B.agg(['min', 'max'])
   min  max
A
1    1    2
2    3    4

User-defined function for aggregation

>>> df.groupby('A').agg(lambda x: sum(x) + 2)
    B          C
A
1       5       2.590715
2       9       2.704907

Different aggregations per column

>>> df.groupby('A').agg({'B': ['min', 'max'], 'C': 'sum'})
    B             C
  min max       sum
A
1   1   2  0.590715
2   3   4  0.704907

To control the output names with different aggregations per column,
pandas supports "named aggregation"

>>> df.groupby("A").agg(
...     b_min=pd.NamedAgg(column="B", aggfunc="min"),
...     c_sum=pd.NamedAgg(column="C", aggfunc="sum")
... )
   b_min     c_sum
A
1      1  0.590715
2      3  0.704907

- The keywords are the *output* column names
- The values are tuples whose first element is the column to select
  and the second element is the aggregation to apply to that column.
  Pandas provides the ``pandas.NamedAgg`` namedtuple with the fields
  ``['column', 'aggfunc']`` to make it clearer what the arguments are.
  As usual, the aggregation can be a callable or a string alias.

See :ref:`groupby.aggregate.named` for more.

.. versionchanged:: 1.3.0

    The resulting dtype will reflect the return value of the aggregating function.

>>> df.groupby("A")[["B"]].agg(lambda x: x.astype(float).min())
      B
A
1   1.0
2   3.0
        """
        pass
    agg = aggregate
    def transform(self, func: Callable | str, *args, **kwargs) -> DataFrame:
        """
Call function producing a same-indexed DataFrame on each group.

Returns a DataFrame having the same indexes as the original object
filled with the transformed values.

Parameters
----------
f : function, str
    Function to apply to each group. See the Notes section below for requirements.

    Accepted inputs are:

    - String
    - Python function
    - Numba JIT function with ``engine='numba'`` specified.

    Only passing a single function is supported with this engine.
    If the ``'numba'`` engine is chosen, the function must be
    a user defined function with ``values`` and ``index`` as the
    first and second arguments respectively in the function signature.
    Each group's index will be passed to the user defined function
    and optionally available for use.

    If a string is chosen, then it needs to be the name
    of the groupby method you want to use.
*args
    Positional arguments to pass to func.
engine : str, default None
    * ``'cython'`` : Runs the function through C-extensions from cython.
    * ``'numba'`` : Runs the function through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or the global setting ``compute.use_numba``

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}`` and will be
      applied to the function

**kwargs
    Keyword arguments to be passed into func.

Returns
-------
DataFrame

See Also
--------
DataFrame.groupby.apply : Apply function ``func`` group-wise and combine
    the results together.
DataFrame.groupby.aggregate : Aggregate using one or more
    operations over the specified axis.
DataFrame.transform : Call ``func`` on self producing a DataFrame with the
    same axis shape as self.

Notes
-----
Each group is endowed the attribute 'name' in case you need to know
which group you are working on.

The current implementation imposes three requirements on f:

* f must return a value that either has the same shape as the input
  subframe or can be broadcast to the shape of the input subframe.
  For example, if `f` returns a scalar it will be broadcast to have the
  same shape as the input subframe.
* if this is a DataFrame, f must support application column-by-column
  in the subframe. If f also supports application to the entire subframe,
  then a fast path is used starting from the second chunk.
* f must not mutate groups. Mutation is not supported and may
  produce unexpected results. See :ref:`gotchas.udf-mutation` for more details.

When using ``engine='numba'``, there will be no "fall back" behavior internally.
The group data and group index will be passed as numpy arrays to the JITed
user defined function, and no alternative execution attempts will be tried.

.. versionchanged:: 1.3.0

    The resulting dtype will reflect the return value of the passed ``func``,
    see the examples below.

.. versionchanged:: 2.0.0

    When using ``.transform`` on a grouped DataFrame and the transformation function
    returns a DataFrame, pandas now aligns the result's index
    with the input's index. You can call ``.to_numpy()`` on the
    result of the transformation function to avoid alignment.

Examples
--------

>>> df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
...                           'foo', 'bar'],
...                    'B' : ['one', 'one', 'two', 'three',
...                           'two', 'two'],
...                    'C' : [1, 5, 5, 2, 5, 5],
...                    'D' : [2.0, 5., 8., 1., 2., 9.]})
>>> grouped = df.groupby('A')[['C', 'D']]
>>> grouped.transform(lambda x: (x - x.mean()) / x.std())
        C         D
0 -1.154701 -0.577350
1  0.577350  0.000000
2  0.577350  1.154701
3 -1.154701 -1.000000
4  0.577350 -0.577350
5  0.577350  1.000000

Broadcast result of the transformation

>>> grouped.transform(lambda x: x.max() - x.min())
    C    D
0  4.0  6.0
1  3.0  8.0
2  4.0  6.0
3  3.0  8.0
4  4.0  6.0
5  3.0  8.0

>>> grouped.transform("mean")
    C    D
0  3.666667  4.0
1  4.000000  5.0
2  3.666667  4.0
3  4.000000  5.0
4  3.666667  4.0
5  4.000000  5.0

.. versionchanged:: 1.3.0

The resulting dtype will reflect the return value of the passed ``func``,
for example:

>>> grouped.transform(lambda x: x.astype(int).max())
C  D
0  5  8
1  5  9
2  5  8
3  5  9
4  5  8
5  5  9
        """
        pass
    def filter(
        self, func: Callable, dropna: bool = ..., *args, **kwargs
    ) -> DataFrame: ...
    def nunique(self, dropna: bool = ...) -> DataFrame: ...
    @overload
    def __getitem__(self, item: str) -> SeriesGroupBy[Any, ByT]: ...
    @overload
    def __getitem__(self, item: list[str]) -> DataFrameGroupBy[ByT]: ...
    def count(self) -> DataFrame: ...
    def boxplot(
        self,
        grouped: DataFrame,
        subplots: bool = ...,
        column: str | Sequence | None = ...,
        fontsize: float | str = ...,
        rot: float = ...,
        grid: bool = ...,
        ax: PlotAxes | None = ...,
        figsize: tuple[float, float] | None = ...,
        layout: tuple[int, int] | None = ...,
        sharex: bool = ...,
        sharey: bool = ...,
        bins: int | Sequence = ...,
        backend: str | None = ...,
        **kwargs,
    ) -> AxesSubplot | Sequence[AxesSubplot]: ...
    # Overrides and others from original pylance stubs
    # These are "properties" but properties can't have all these arguments?!
    def corr(self, method: str | Callable, min_periods: int = ...) -> DataFrame:
        """
Compute pairwise correlation of columns, excluding NA/null values.

Parameters
----------
method : {'pearson', 'kendall', 'spearman'} or callable
    Method of correlation:

    * pearson : standard correlation coefficient
    * kendall : Kendall Tau correlation coefficient
    * spearman : Spearman rank correlation
    * callable: callable with input two 1d ndarrays
        and returning a float. Note that the returned matrix from corr
        will have 1 along the diagonals and will be symmetric
        regardless of the callable's behavior.
min_periods : int, optional
    Minimum number of observations required per pair of columns
    to have a valid result. Currently only available for Pearson
    and Spearman correlation.
numeric_only : bool, default False
    Include only `float`, `int` or `boolean` data.

    .. versionadded:: 1.5.0

    .. versionchanged:: 2.0.0
        The default value of ``numeric_only`` is now ``False``.

Returns
-------
DataFrame
    Correlation matrix.

See Also
--------
DataFrame.corrwith : Compute pairwise correlation with another
    DataFrame or Series.
Series.corr : Compute the correlation between two Series.

Notes
-----
Pearson, Kendall and Spearman correlation are currently computed using pairwise complete observations.

* `Pearson correlation coefficient <https://en.wikipedia.org/wiki/Pearson_correlation_coefficient>`_
* `Kendall rank correlation coefficient <https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient>`_
* `Spearman's rank correlation coefficient <https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient>`_

Examples
--------
>>> def histogram_intersection(a, b):
...     v = np.minimum(a, b).sum().round(decimals=1)
...     return v
>>> df = pd.DataFrame([(.2, .3), (.0, .6), (.6, .0), (.2, .1)],
...                   columns=['dogs', 'cats'])
>>> df.corr(method=histogram_intersection)
      dogs  cats
dogs   1.0   0.3
cats   0.3   1.0

>>> df = pd.DataFrame([(1, 1), (2, np.nan), (np.nan, 3), (4, 4)],
...                   columns=['dogs', 'cats'])
>>> df.corr(min_periods=3)
      dogs  cats
dogs   1.0   NaN
cats   NaN   1.0
        """
        pass
    def cov(self, min_periods: int = ...) -> DataFrame:
        """
Compute pairwise covariance of columns, excluding NA/null values.

Compute the pairwise covariance among the series of a DataFrame.
The returned data frame is the `covariance matrix
<https://en.wikipedia.org/wiki/Covariance_matrix>`__ of the columns
of the DataFrame.

Both NA and null values are automatically excluded from the
calculation. (See the note below about bias from missing values.)
A threshold can be set for the minimum number of
observations for each value created. Comparisons with observations
below this threshold will be returned as ``NaN``.

This method is generally used for the analysis of time series data to
understand the relationship between different measures
across time.

Parameters
----------
min_periods : int, optional
    Minimum number of observations required per pair of columns
    to have a valid result.

ddof : int, default 1
    Delta degrees of freedom.  The divisor used in calculations
    is ``N - ddof``, where ``N`` represents the number of elements.
    This argument is applicable only when no ``nan`` is in the dataframe.

numeric_only : bool, default False
    Include only `float`, `int` or `boolean` data.

    .. versionadded:: 1.5.0

    .. versionchanged:: 2.0.0
        The default value of ``numeric_only`` is now ``False``.

Returns
-------
DataFrame
    The covariance matrix of the series of the DataFrame.

See Also
--------
Series.cov : Compute covariance with another Series.
core.window.ewm.ExponentialMovingWindow.cov : Exponential weighted sample
    covariance.
core.window.expanding.Expanding.cov : Expanding sample covariance.
core.window.rolling.Rolling.cov : Rolling sample covariance.

Notes
-----
Returns the covariance matrix of the DataFrame's time series.
The covariance is normalized by N-ddof.

For DataFrames that have Series that are missing data (assuming that
data is `missing at random
<https://en.wikipedia.org/wiki/Missing_data#Missing_at_random>`__)
the returned covariance matrix will be an unbiased estimate
of the variance and covariance between the member Series.

However, for many applications this estimate may not be acceptable
because the estimate covariance matrix is not guaranteed to be positive
semi-definite. This could lead to estimate correlations having
absolute values which are greater than one, and/or a non-invertible
covariance matrix. See `Estimation of covariance matrices
<https://en.wikipedia.org/w/index.php?title=Estimation_of_covariance_
matrices>`__ for more details.

Examples
--------
>>> df = pd.DataFrame([(1, 2), (0, 3), (2, 0), (1, 1)],
...                   columns=['dogs', 'cats'])
>>> df.cov()
          dogs      cats
dogs  0.666667 -1.000000
cats -1.000000  1.666667

>>> np.random.seed(42)
>>> df = pd.DataFrame(np.random.randn(1000, 5),
...                   columns=['a', 'b', 'c', 'd', 'e'])
>>> df.cov()
          a         b         c         d         e
a  0.998438 -0.020161  0.059277 -0.008943  0.014144
b -0.020161  1.059352 -0.008543 -0.024738  0.009826
c  0.059277 -0.008543  1.010670 -0.001486 -0.000271
d -0.008943 -0.024738 -0.001486  0.921297 -0.013692
e  0.014144  0.009826 -0.000271 -0.013692  0.977795

**Minimum number of periods**

This method also supports an optional ``min_periods`` keyword
that specifies the required minimum number of non-NA observations for
each column pair in order to have a valid result:

>>> np.random.seed(42)
>>> df = pd.DataFrame(np.random.randn(20, 3),
...                   columns=['a', 'b', 'c'])
>>> df.loc[df.index[:5], 'a'] = np.nan
>>> df.loc[df.index[5:10], 'b'] = np.nan
>>> df.cov(min_periods=12)
          a         b         c
a  0.316741       NaN -0.150812
b       NaN  1.248003  0.191417
c -0.150812  0.191417  0.895202
        """
        pass
    def diff(self, periods: int = ..., axis: Axis = ...) -> DataFrame: ...
    def bfill(self, limit: int | None = ...) -> DataFrame: ...
    def corrwith(
        self,
        other: DataFrame,
        axis: Axis = ...,
        drop: bool = ...,
        method: str = ...,
    ) -> Series:
        """
Compute pairwise correlation.

Pairwise correlation is computed between rows or columns of
DataFrame with rows or columns of Series or DataFrame. DataFrames
are first aligned along both axes before computing the
correlations.

Parameters
----------
other : DataFrame, Series
    Object with which to compute correlations.
axis : {0 or 'index', 1 or 'columns'}, default 0
    The axis to use. 0 or 'index' to compute row-wise, 1 or 'columns' for
    column-wise.
drop : bool, default False
    Drop missing indices from result.
method : {'pearson', 'kendall', 'spearman'} or callable
    Method of correlation:

    * pearson : standard correlation coefficient
    * kendall : Kendall Tau correlation coefficient
    * spearman : Spearman rank correlation
    * callable: callable with input two 1d ndarrays
        and returning a float.

numeric_only : bool, default False
    Include only `float`, `int` or `boolean` data.

    .. versionadded:: 1.5.0

    .. versionchanged:: 2.0.0
        The default value of ``numeric_only`` is now ``False``.

Returns
-------
Series
    Pairwise correlations.

See Also
--------
DataFrame.corr : Compute pairwise correlation of columns.

Examples
--------
>>> index = ["a", "b", "c", "d", "e"]
>>> columns = ["one", "two", "three", "four"]
>>> df1 = pd.DataFrame(np.arange(20).reshape(5, 4), index=index, columns=columns)
>>> df2 = pd.DataFrame(np.arange(16).reshape(4, 4), index=index[:4], columns=columns)
>>> df1.corrwith(df2)
one      1.0
two      1.0
three    1.0
four     1.0
dtype: float64

>>> df2.corrwith(df1, axis=1)
a    1.0
b    1.0
c    1.0
d    1.0
e    NaN
dtype: float64
        """
        pass
    def cummax(
        self, axis: Axis = ..., numeric_only: bool = ..., **kwargs
    ) -> DataFrame: ...
    def cummin(
        self, axis: Axis = ..., numeric_only: bool = ..., **kwargs
    ) -> DataFrame: ...
    def cumprod(self, axis: Axis = ..., **kwargs) -> DataFrame: ...
    def cumsum(self, axis: Axis = ..., **kwargs) -> DataFrame: ...
    def describe(self, **kwargs) -> DataFrame: ...
    def ffill(self, limit: int | None = ...) -> DataFrame: ...
    def fillna(
        self,
        value,
        method: str | None = ...,
        axis: Axis = ...,
        inplace: Literal[False] = ...,
        limit: int | None = ...,
        downcast: dict | None = ...,
    ) -> DataFrame: ...
    def first(self, **kwargs) -> DataFrame: ...
    def head(self, n: int = ...) -> DataFrame: ...
    def hist(
        self,
        data: DataFrame,
        column: str | Sequence | None = ...,
        by=...,
        grid: bool = ...,
        xlabelsize: int | None = ...,
        xrot: float | None = ...,
        ylabelsize: int | None = ...,
        yrot: float | None = ...,
        ax: PlotAxes | None = ...,
        sharex: bool = ...,
        sharey: bool = ...,
        figsize: tuple[float, float] | None = ...,
        layout: tuple[int, int] | None = ...,
        bins: int | Sequence = ...,
        backend: str | None = ...,
        **kwargs,
    ) -> AxesSubplot | Sequence[AxesSubplot]:
        """
Make a histogram of the DataFrame's columns.

A `histogram`_ is a representation of the distribution of data.
This function calls :meth:`matplotlib.pyplot.hist`, on each series in
the DataFrame, resulting in one histogram per column.

.. _histogram: https://en.wikipedia.org/wiki/Histogram

Parameters
----------
data : DataFrame
    The pandas object holding the data.
column : str or sequence, optional
    If passed, will be used to limit data to a subset of columns.
by : object, optional
    If passed, then used to form histograms for separate groups.
grid : bool, default True
    Whether to show axis grid lines.
xlabelsize : int, default None
    If specified changes the x-axis label size.
xrot : float, default None
    Rotation of x axis labels. For example, a value of 90 displays the
    x labels rotated 90 degrees clockwise.
ylabelsize : int, default None
    If specified changes the y-axis label size.
yrot : float, default None
    Rotation of y axis labels. For example, a value of 90 displays the
    y labels rotated 90 degrees clockwise.
ax : Matplotlib axes object, default None
    The axes to plot the histogram on.
sharex : bool, default True if ax is None else False
    In case subplots=True, share x axis and set some x axis labels to
    invisible; defaults to True if ax is None otherwise False if an ax
    is passed in.
    Note that passing in both an ax and sharex=True will alter all x axis
    labels for all subplots in a figure.
sharey : bool, default False
    In case subplots=True, share y axis and set some y axis labels to
    invisible.
figsize : tuple, optional
    The size in inches of the figure to create. Uses the value in
    `matplotlib.rcParams` by default.
layout : tuple, optional
    Tuple of (rows, columns) for the layout of the histograms.
bins : int or sequence, default 10
    Number of histogram bins to be used. If an integer is given, bins + 1
    bin edges are calculated and returned. If bins is a sequence, gives
    bin edges, including left edge of first bin and right edge of last
    bin. In this case, bins is returned unmodified.

backend : str, default None
    Backend to use instead of the backend specified in the option
    ``plotting.backend``. For instance, 'matplotlib'. Alternatively, to
    specify the ``plotting.backend`` for the whole session, set
    ``pd.options.plotting.backend``.

legend : bool, default False
    Whether to show the legend.

**kwargs
    All other plotting keyword arguments to be passed to
    :meth:`matplotlib.pyplot.hist`.

Returns
-------
matplotlib.AxesSubplot or numpy.ndarray of them

See Also
--------
matplotlib.pyplot.hist : Plot a histogram using matplotlib.

Examples
--------
This example draws a histogram based on the length and width of
some animals, displayed in three bins

.. plot::
    :context: close-figs

    >>> data = {'length': [1.5, 0.5, 1.2, 0.9, 3],
    ...         'width': [0.7, 0.2, 0.15, 0.2, 1.1]}
    >>> index = ['pig', 'rabbit', 'duck', 'chicken', 'horse']
    >>> df = pd.DataFrame(data, index=index)
    >>> hist = df.hist(bins=3)
        """
        pass
    def idxmax(
        self, axis: Axis = ..., skipna: bool = ..., numeric_only: bool = ...
    ) -> DataFrame: ...
    def idxmin(
        self, axis: Axis = ..., skipna: bool = ..., numeric_only: bool = ...
    ) -> DataFrame: ...
    def last(self, **kwargs) -> DataFrame: ...
    def max(self, **kwargs) -> DataFrame: ...
    def mean(self, **kwargs) -> DataFrame: ...
    def median(self, **kwargs) -> DataFrame: ...
    def min(self, **kwargs) -> DataFrame: ...
    def nth(self, n: int | Sequence[int], dropna: str | None = ...) -> DataFrame: ...
    def pct_change(
        self,
        periods: int = ...,
        fill_method: str = ...,
        limit=...,
        freq=...,
        axis: Axis = ...,
    ) -> DataFrame: ...
    def prod(self, numeric_only: bool = ..., min_count: int = ...) -> DataFrame: ...
    def quantile(
        self, q: float = ..., interpolation: str = ..., numeric_only: bool = ...
    ) -> DataFrame: ...
    def resample(self, rule, *args, **kwargs) -> Grouper: ...
    def sample(
        self,
        n: int | None = ...,
        frac: float | None = ...,
        replace: bool = ...,
        weights: ListLike | None = ...,
        random_state: RandomState | None = ...,
    ) -> DataFrame: ...
    def sem(self, ddof: int = ..., numeric_only: bool = ...) -> DataFrame: ...
    def shift(
        self,
        periods: int = ...,
        freq: str = ...,
        axis: Axis = ...,
        fill_value=...,
    ) -> DataFrame: ...
    @overload
    def skew(
        self,
        axis: Axis = ...,
        skipna: bool = ...,
        numeric_only: bool = ...,
        *,
        level: Level,
        **kwargs,
    ) -> DataFrame: ...
    @overload
    def skew(
        self,
        axis: Axis = ...,
        skipna: bool = ...,
        level: None = ...,
        numeric_only: bool = ...,
        **kwargs,
    ) -> Series: ...
    def std(self, ddof: int = ..., numeric_only: bool = ...) -> DataFrame: ...
    def sum(
        self,
        numeric_only: bool = ...,
        min_count: int = ...,
        engine=...,
        engine_kwargs=...,
    ) -> DataFrame: ...
    def tail(self, n: int = ...) -> DataFrame: ...
    def take(self, indices: Sequence, axis: Axis = ..., **kwargs) -> DataFrame: ...
    def tshift(self, periods: int, freq=..., axis: Axis = ...) -> DataFrame: ...
    def var(self, ddof: int = ..., numeric_only: bool = ...) -> DataFrame: ...
    @overload
    def value_counts(
        self,
        subset: ListLike | None = ...,
        normalize: Literal[False] = ...,
        sort: bool = ...,
        ascending: bool = ...,
        dropna: bool = ...,
    ) -> Series[int]: ...
    @overload
    def value_counts(
        self,
        subset: ListLike | None,
        normalize: Literal[True],
        sort: bool = ...,
        ascending: bool = ...,
        dropna: bool = ...,
    ) -> Series[float]: ...
    def __getattr__(self, name: str) -> SeriesGroupBy[Any, ByT]: ...
    def __iter__(self) -> Iterator[tuple[ByT, DataFrame]]: ...
