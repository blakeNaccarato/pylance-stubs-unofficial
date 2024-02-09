from collections.abc import Callable
from typing import Any

from pandas import (
    DataFrame,
    Series,
)
from pandas.core.window.rolling import (
    BaseWindowGroupby,
    RollingAndExpandingMixin,
)

from pandas._typing import (
    NDFrameT,
    QuantileInterpolation,
    WindowingEngine,
    WindowingEngineKwargs,
    WindowingRankType,
)

class Expanding(RollingAndExpandingMixin[NDFrameT]):
    def count(self) -> NDFrameT:
        """
Calculate the expanding count of non NaN observations.

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.count : Aggregating count for Series.
pandas.DataFrame.count : Aggregating count for DataFrame.

Examples
--------
>>> ser = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
>>> ser.expanding().count()
a    1.0
b    2.0
c    3.0
d    4.0
dtype: float64
        """
        pass
    def apply(
        self,
        func: Callable[..., Any],
        raw: bool = ...,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
        args: tuple[Any, ...] | None = ...,
        kwargs: dict[str, Any] | None = ...,
    ) -> NDFrameT:
        """
Calculate the expanding custom aggregation function.

Parameters
----------
func : function
    Must produce a single value from an ndarray input if ``raw=True``
    or a single value from a Series if ``raw=False``. Can also accept a
    Numba JIT function with ``engine='numba'`` specified.

raw : bool, default False
    * ``False`` : passes each row or column as a Series to the
      function.
    * ``True`` : the passed function will receive ndarray
      objects instead.
      If you are just applying a NumPy reduction function this will
      achieve much better performance.

engine : str, default None
    * ``'cython'`` : Runs rolling apply through C-extensions from cython.
    * ``'numba'`` : Runs rolling apply through JIT compiled code from numba.
      Only available when ``raw`` is set to ``True``.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}`` and will be
      applied to both the ``func`` and the ``apply`` rolling aggregation.

args : tuple, default None
    Positional arguments to be passed into func.

kwargs : dict, default None
    Keyword arguments to be passed into func.

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.apply : Aggregating apply for Series.
pandas.DataFrame.apply : Aggregating apply for DataFrame.

Examples
--------
>>> ser = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
>>> ser.expanding().apply(lambda s: s.max() - 2 * s.min())
a   -1.0
b    0.0
c    1.0
d    2.0
dtype: float64
        """
        pass
    def sum(
        self,
        numeric_only: bool = ...,
        *,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT:
        """
Calculate the expanding sum.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

engine : str, default None
    * ``'cython'`` : Runs the operation through C-extensions from cython.
    * ``'numba'`` : Runs the operation through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

      .. versionadded:: 1.3.0

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}``

      .. versionadded:: 1.3.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.sum : Aggregating sum for Series.
pandas.DataFrame.sum : Aggregating sum for DataFrame.

Notes
-----
See :ref:`window.numba_engine` and :ref:`enhancingperf.numba` for extended documentation and performance considerations for the Numba engine.

Examples
--------
>>> ser = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
>>> ser.expanding().sum()
a     1.0
b     3.0
c     6.0
d    10.0
dtype: float64
        """
        pass
    def max(
        self,
        numeric_only: bool = ...,
        *,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT:
        """
Calculate the expanding maximum.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

engine : str, default None
    * ``'cython'`` : Runs the operation through C-extensions from cython.
    * ``'numba'`` : Runs the operation through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

      .. versionadded:: 1.3.0

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}``

      .. versionadded:: 1.3.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.max : Aggregating max for Series.
pandas.DataFrame.max : Aggregating max for DataFrame.

Notes
-----
See :ref:`window.numba_engine` and :ref:`enhancingperf.numba` for extended documentation and performance considerations for the Numba engine.

Examples
--------
>>> ser = pd.Series([3, 2, 1, 4], index=['a', 'b', 'c', 'd'])
>>> ser.expanding().max()
a    3.0
b    3.0
c    3.0
d    4.0
dtype: float64
        """
        pass
    def min(
        self,
        numeric_only: bool = ...,
        *,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT:
        """
Calculate the expanding minimum.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

engine : str, default None
    * ``'cython'`` : Runs the operation through C-extensions from cython.
    * ``'numba'`` : Runs the operation through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

      .. versionadded:: 1.3.0

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}``

      .. versionadded:: 1.3.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.min : Aggregating min for Series.
pandas.DataFrame.min : Aggregating min for DataFrame.

Notes
-----
See :ref:`window.numba_engine` and :ref:`enhancingperf.numba` for extended documentation and performance considerations for the Numba engine.

Examples
--------
>>> ser = pd.Series([2, 3, 4, 1], index=['a', 'b', 'c', 'd'])
>>> ser.expanding().min()
a    2.0
b    2.0
c    2.0
d    1.0
dtype: float64
        """
        pass
    def mean(
        self,
        numeric_only: bool = ...,
        *,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT:
        """
Calculate the expanding mean.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

engine : str, default None
    * ``'cython'`` : Runs the operation through C-extensions from cython.
    * ``'numba'`` : Runs the operation through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

      .. versionadded:: 1.3.0

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}``

      .. versionadded:: 1.3.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.mean : Aggregating mean for Series.
pandas.DataFrame.mean : Aggregating mean for DataFrame.

Notes
-----
See :ref:`window.numba_engine` and :ref:`enhancingperf.numba` for extended documentation and performance considerations for the Numba engine.

Examples
--------
>>> ser = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
>>> ser.expanding().mean()
a    1.0
b    1.5
c    2.0
d    2.5
dtype: float64
        """
        pass
    def median(
        self,
        numeric_only: bool = ...,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT:
        """
Calculate the expanding median.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

engine : str, default None
    * ``'cython'`` : Runs the operation through C-extensions from cython.
    * ``'numba'`` : Runs the operation through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

      .. versionadded:: 1.3.0

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}``

      .. versionadded:: 1.3.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.median : Aggregating median for Series.
pandas.DataFrame.median : Aggregating median for DataFrame.

Notes
-----
See :ref:`window.numba_engine` and :ref:`enhancingperf.numba` for extended documentation and performance considerations for the Numba engine.

Examples
--------
>>> ser = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
>>> ser.expanding().median()
a    1.0
b    1.5
c    2.0
d    2.5
dtype: float64
        """
        pass
    def std(
        self,
        ddof: int = ...,
        numeric_only: bool = ...,
        *,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT:
        """
Calculate the expanding standard deviation.

Parameters
----------
ddof : int, default 1
    Delta Degrees of Freedom.  The divisor used in calculations
    is ``N - ddof``, where ``N`` represents the number of elements.

numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

engine : str, default None
    * ``'cython'`` : Runs the operation through C-extensions from cython.
    * ``'numba'`` : Runs the operation through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

      .. versionadded:: 1.4.0

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}``

      .. versionadded:: 1.4.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
numpy.std : Equivalent method for NumPy array.
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.std : Aggregating std for Series.
pandas.DataFrame.std : Aggregating std for DataFrame.

Notes
-----
The default ``ddof`` of 1 used in :meth:`Series.std` is different
than the default ``ddof`` of 0 in :func:`numpy.std`.

A minimum of one period is required for the rolling calculation.

Examples
--------
>>> s = pd.Series([5, 5, 6, 7, 5, 5, 5])

>>> s.expanding(3).std()
0         NaN
1         NaN
2    0.577350
3    0.957427
4    0.894427
5    0.836660
6    0.786796
dtype: float64
        """
        pass
    def var(
        self,
        ddof: int = ...,
        numeric_only: bool = ...,
        *,
        engine: WindowingEngine = ...,
        engine_kwargs: WindowingEngineKwargs = ...,
    ) -> NDFrameT:
        """
Calculate the expanding variance.

Parameters
----------
ddof : int, default 1
    Delta Degrees of Freedom.  The divisor used in calculations
    is ``N - ddof``, where ``N`` represents the number of elements.

numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

engine : str, default None
    * ``'cython'`` : Runs the operation through C-extensions from cython.
    * ``'numba'`` : Runs the operation through JIT compiled code from numba.
    * ``None`` : Defaults to ``'cython'`` or globally setting ``compute.use_numba``

      .. versionadded:: 1.4.0

engine_kwargs : dict, default None
    * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
    * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
      and ``parallel`` dictionary keys. The values must either be ``True`` or
      ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
      ``{'nopython': True, 'nogil': False, 'parallel': False}``

      .. versionadded:: 1.4.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
numpy.var : Equivalent method for NumPy array.
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.var : Aggregating var for Series.
pandas.DataFrame.var : Aggregating var for DataFrame.

Notes
-----
The default ``ddof`` of 1 used in :meth:`Series.var` is different
than the default ``ddof`` of 0 in :func:`numpy.var`.

A minimum of one period is required for the rolling calculation.

Examples
--------
>>> s = pd.Series([5, 5, 6, 7, 5, 5, 5])

>>> s.expanding(3).var()
0         NaN
1         NaN
2    0.333333
3    0.916667
4    0.800000
5    0.700000
6    0.619048
dtype: float64
        """
        pass
    def sem(self, ddof: int = ..., numeric_only: bool = ...) -> NDFrameT:
        """
Calculate the expanding standard error of mean.

Parameters
----------
ddof : int, default 1
    Delta Degrees of Freedom.  The divisor used in calculations
    is ``N - ddof``, where ``N`` represents the number of elements.

numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.sem : Aggregating sem for Series.
pandas.DataFrame.sem : Aggregating sem for DataFrame.

Notes
-----
A minimum of one period is required for the calculation.

Examples
--------
>>> s = pd.Series([0, 1, 2, 3])

>>> s.expanding().sem()
0         NaN
1    0.707107
2    0.707107
3    0.745356
dtype: float64
        """
        pass
    def skew(
        self,
        numeric_only: bool = ...,
    ) -> NDFrameT:
        """
Calculate the expanding unbiased skewness.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
scipy.stats.skew : Third moment of a probability density.
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.skew : Aggregating skew for Series.
pandas.DataFrame.skew : Aggregating skew for DataFrame.

Notes
-----
A minimum of three periods is required for the rolling calculation.

Examples
--------
>>> ser = pd.Series([-1, 0, 2, -1, 2], index=['a', 'b', 'c', 'd', 'e'])
>>> ser.expanding().skew()
a         NaN
b         NaN
c    0.935220
d    1.414214
e    0.315356
dtype: float64
        """
        pass
    def kurt(
        self,
        numeric_only: bool = ...,
    ) -> NDFrameT:
        """
Calculate the expanding Fisher's definition of kurtosis without bias.

Parameters
----------
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
scipy.stats.kurtosis : Reference SciPy method.
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.kurt : Aggregating kurt for Series.
pandas.DataFrame.kurt : Aggregating kurt for DataFrame.

Notes
-----
A minimum of four periods is required for the calculation.

Examples
--------
The example below will show a rolling calculation with a window size of
four matching the equivalent function call using `scipy.stats`.

>>> arr = [1, 2, 3, 4, 999]
>>> import scipy.stats
>>> print(f"{scipy.stats.kurtosis(arr[:-1], bias=False):.6f}")
-1.200000
>>> print(f"{scipy.stats.kurtosis(arr, bias=False):.6f}")
4.999874
>>> s = pd.Series(arr)
>>> s.expanding(4).kurt()
0         NaN
1         NaN
2         NaN
3   -1.200000
4    4.999874
dtype: float64
        """
        pass
    def quantile(
        self,
        quantile: float,
        interpolation: QuantileInterpolation = ...,
        numeric_only: bool = ...,
    ) -> NDFrameT:
        """
Calculate the expanding quantile.

Parameters
----------
quantile : float
    Quantile to compute. 0 <= quantile <= 1.

    .. deprecated:: 2.1.0
        This will be renamed to 'q' in a future version.
interpolation : {'linear', 'lower', 'higher', 'midpoint', 'nearest'}
    This optional parameter specifies the interpolation method to use,
    when the desired quantile lies between two data points `i` and `j`:

        * linear: `i + (j - i) * fraction`, where `fraction` is the
          fractional part of the index surrounded by `i` and `j`.
        * lower: `i`.
        * higher: `j`.
        * nearest: `i` or `j` whichever is nearest.
        * midpoint: (`i` + `j`) / 2.
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.quantile : Aggregating quantile for Series.
pandas.DataFrame.quantile : Aggregating quantile for DataFrame.

Examples
--------
>>> ser = pd.Series([1, 2, 3, 4, 5, 6], index=['a', 'b', 'c', 'd', 'e', 'f'])
>>> ser.expanding(min_periods=4).quantile(.25)
a     NaN
b     NaN
c     NaN
d    1.75
e    2.00
f    2.25
dtype: float64
        """
        pass
    def rank(
        self,
        method: WindowingRankType = ...,
        ascending: bool = ...,
        pct: bool = ...,
        numeric_only: bool = ...,
    ) -> NDFrameT:
        """
Calculate the expanding rank.

.. versionadded:: 1.4.0 

Parameters
----------
method : {'average', 'min', 'max'}, default 'average'
    How to rank the group of records that have the same value (i.e. ties):

    * average: average rank of the group
    * min: lowest rank in the group
    * max: highest rank in the group

ascending : bool, default True
    Whether or not the elements should be ranked in ascending order.
pct : bool, default False
    Whether or not to display the returned rankings in percentile
    form.
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.rank : Aggregating rank for Series.
pandas.DataFrame.rank : Aggregating rank for DataFrame.

Examples
--------
>>> s = pd.Series([1, 4, 2, 3, 5, 3])
>>> s.expanding().rank()
0    1.0
1    2.0
2    2.0
3    3.0
4    5.0
5    3.5
dtype: float64

>>> s.expanding().rank(method="max")
0    1.0
1    2.0
2    2.0
3    3.0
4    5.0
5    4.0
dtype: float64

>>> s.expanding().rank(method="min")
0    1.0
1    2.0
2    2.0
3    3.0
4    5.0
5    3.0
dtype: float64
        """
        pass
    def cov(
        self,
        other: DataFrame | Series | None = ...,
        pairwise: bool | None = ...,
        ddof: int = ...,
        numeric_only: bool = ...,
    ) -> NDFrameT:
        """
Calculate the expanding sample covariance.

Parameters
----------
other : Series or DataFrame, optional
    If not supplied then will default to self and produce pairwise
    output.
pairwise : bool, default None
    If False then only matching columns between self and other will be
    used and the output will be a DataFrame.
    If True then all pairwise combinations will be calculated and the
    output will be a MultiIndexed DataFrame in the case of DataFrame
    inputs. In the case of missing elements, only complete pairwise
    observations will be used.
ddof : int, default 1
    Delta Degrees of Freedom.  The divisor used in calculations
    is ``N - ddof``, where ``N`` represents the number of elements.
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.cov : Aggregating cov for Series.
pandas.DataFrame.cov : Aggregating cov for DataFrame.

Examples
--------
>>> ser1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
>>> ser2 = pd.Series([10, 11, 13, 16], index=['a', 'b', 'c', 'd'])
>>> ser1.expanding().cov(ser2)
a         NaN
b    0.500000
c    1.500000
d    3.333333
dtype: float64
        """
        pass
    def corr(
        self,
        other: DataFrame | Series | None = ...,
        pairwise: bool | None = ...,
        ddof: int = ...,
        numeric_only: bool = ...,
    ) -> NDFrameT:
        """
Calculate the expanding correlation.

Parameters
----------
other : Series or DataFrame, optional
    If not supplied then will default to self and produce pairwise
    output.
pairwise : bool, default None
    If False then only matching columns between self and other will be
    used and the output will be a DataFrame.
    If True then all pairwise combinations will be calculated and the
    output will be a MultiIndexed DataFrame in the case of DataFrame
    inputs. In the case of missing elements, only complete pairwise
    observations will be used.
numeric_only : bool, default False
    Include only float, int, boolean columns.

    .. versionadded:: 1.5.0

Returns
-------
Series or DataFrame
    Return type is the same as the original object with ``np.float64`` dtype.

See Also
--------
cov : Similar method to calculate covariance.
numpy.corrcoef : NumPy Pearson's correlation calculation.
pandas.Series.expanding : Calling expanding with Series data.
pandas.DataFrame.expanding : Calling expanding with DataFrames.
pandas.Series.corr : Aggregating corr for Series.
pandas.DataFrame.corr : Aggregating corr for DataFrame.

Notes
-----

This function uses Pearson's definition of correlation
(https://en.wikipedia.org/wiki/Pearson_correlation_coefficient).

When `other` is not specified, the output will be self correlation (e.g.
all 1's), except for :class:`~pandas.DataFrame` inputs with `pairwise`
set to `True`.

Function will return ``NaN`` for correlations of equal valued sequences;
this is the result of a 0/0 division error.

When `pairwise` is set to `False`, only matching columns between `self` and
`other` will be used.

When `pairwise` is set to `True`, the output will be a MultiIndex DataFrame
with the original index on the first level, and the `other` DataFrame
columns on the second level.

In the case of missing elements, only complete pairwise observations
will be used.

Examples
--------
>>> ser1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
>>> ser2 = pd.Series([10, 11, 13, 16], index=['a', 'b', 'c', 'd'])
>>> ser1.expanding().corr(ser2)
a         NaN
b    1.000000
c    0.981981
d    0.975900
dtype: float64
        """
        pass

class ExpandingGroupby(BaseWindowGroupby, Expanding): ...
