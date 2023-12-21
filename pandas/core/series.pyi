from collections.abc import (
    Callable,
    Hashable,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    Sequence,
)
from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from typing import (
    Any,
    ClassVar,
    Generic,
    Literal,
    overload,
)

from matplotlib.axes import (
    Axes as PlotAxes,
    SubplotBase,
)
import numpy as np
from pandas import (
    Period,
    PeriodDtype,
    Timedelta,
    Timestamp,
)
from pandas.core.api import (
    Int8Dtype as Int8Dtype,
    Int16Dtype as Int16Dtype,
    Int32Dtype as Int32Dtype,
    Int64Dtype as Int64Dtype,
)
from pandas.core.arrays.base import ExtensionArray
from pandas.core.arrays.categorical import CategoricalAccessor
from pandas.core.arrays.interval import IntervalArray
from pandas.core.base import IndexOpsMixin
from pandas.core.frame import DataFrame
from pandas.core.generic import NDFrame
from pandas.core.groupby.generic import SeriesGroupBy
from pandas.core.indexers import BaseIndexer
from pandas.core.indexes.accessors import (
    CombinedDatetimelikeProperties,
    PeriodProperties,
    TimedeltaProperties,
    TimestampProperties,
)
from pandas.core.indexes.base import Index
from pandas.core.indexes.category import CategoricalIndex
from pandas.core.indexes.datetimes import DatetimeIndex
from pandas.core.indexes.interval import IntervalIndex
from pandas.core.indexes.multi import MultiIndex
from pandas.core.indexes.period import PeriodIndex
from pandas.core.indexes.timedeltas import TimedeltaIndex
from pandas.core.indexing import (
    _AtIndexer,
    _iAtIndexer,
    _iLocIndexer,
    _IndexSliceTuple,
    _LocIndexer,
)
from pandas.core.resample import Resampler
from pandas.core.strings import StringMethods
from pandas.core.window import (
    Expanding,
    ExponentialMovingWindow,
)
from pandas.core.window.rolling import (
    Rolling,
    Window,
)
from typing_extensions import (
    Never,
    Self,
    TypeAlias,
)
import xarray as xr

from pandas._libs.interval import (
    Interval,
    _OrderableT,
)
from pandas._libs.missing import NAType
from pandas._libs.tslibs import BaseOffset
from pandas._typing import (
    S1,
    AggFuncTypeBase,
    AggFuncTypeDictFrame,
    AggFuncTypeSeriesToFrame,
    AnyArrayLike,
    ArrayLike,
    Axes,
    Axis,
    AxisColumn,
    AxisIndex,
    BooleanDtypeArg,
    BytesDtypeArg,
    CalculationMethod,
    CategoryDtypeArg,
    ComplexDtypeArg,
    CompressionOptions,
    Dtype,
    DtypeObj,
    FilePath,
    FillnaOptions,
    FloatDtypeArg,
    GroupByObjectNonScalar,
    HashableT1,
    HashableT2,
    HashableT3,
    IgnoreRaise,
    IndexingInt,
    IntDtypeArg,
    InterpolateOptions,
    IntervalClosedType,
    IntervalT,
    JoinHow,
    JsonSeriesOrient,
    Level,
    ListLike,
    ListLikeU,
    MaskType,
    NaPosition,
    ObjectDtypeArg,
    QuantileInterpolation,
    RandomState,
    Renamer,
    ReplaceMethod,
    Scalar,
    ScalarT,
    SeriesByT,
    SortKind,
    StrDtypeArg,
    StrLike,
    TimedeltaDtypeArg,
    TimestampConvention,
    TimestampDtypeArg,
    UIntDtypeArg,
    VoidDtypeArg,
    WriteBuffer,
    np_ndarray_anyint,
    np_ndarray_bool,
    npt,
    num,
)

from pandas.core.dtypes.base import ExtensionDtype

from pandas.plotting import PlotAccessor

_bool = bool
_str = str

class _iLocIndexerSeries(_iLocIndexer, Generic[S1]):
    # get item
    @overload
    def __getitem__(self, idx: IndexingInt) -> S1: ...
    @overload
    def __getitem__(self, idx: Index | slice | np_ndarray_anyint) -> Series[S1]: ...
    # set item
    @overload
    def __setitem__(self, idx: int, value: S1 | None) -> None: ...
    @overload
    def __setitem__(
        self,
        idx: Index | slice | np_ndarray_anyint | list[int],
        value: S1 | Series[S1] | None,
    ) -> None: ...

class _LocIndexerSeries(_LocIndexer, Generic[S1]):
    # ignore needed because of mypy.  Overlapping, but we want to distinguish
    # having a tuple of just scalars, versus tuples that include slices or Index
    @overload
    def __getitem__(  # type: ignore[misc]
        self,
        idx: Scalar | tuple[Scalar, ...],
        # tuple case is for getting a specific element when using a MultiIndex
    ) -> S1: ...
    @overload
    def __getitem__(
        self,
        idx: MaskType
        | Index
        | Sequence[float]
        | list[str]
        | slice
        | _IndexSliceTuple
        | Callable,
        # _IndexSliceTuple is when having a tuple that includes a slice.  Could just
        # be s.loc[1, :], or s.loc[pd.IndexSlice[1, :]]
    ) -> Series[S1]: ...
    @overload
    def __setitem__(
        self,
        idx: Index | MaskType,
        value: S1 | ArrayLike | Series[S1] | None,
    ) -> None: ...
    @overload
    def __setitem__(
        self,
        idx: str,
        value: S1 | None,
    ) -> None: ...
    @overload
    def __setitem__(
        self,
        idx: MaskType | StrLike | _IndexSliceTuple | list[ScalarT],
        value: S1 | ArrayLike | Series[S1] | None,
    ) -> None: ...

_ListLike: TypeAlias = (
    ArrayLike | dict[_str, np.ndarray] | Sequence[S1] | IndexOpsMixin[S1]
)

class Series(IndexOpsMixin[S1], NDFrame):
    __hash__: ClassVar[None]

    @overload
    def __new__(  # type: ignore[misc]
        cls,
        data: DatetimeIndex
        | Sequence[np.datetime64 | datetime]
        | np.datetime64
        | datetime,
        index: Axes | None = ...,
        *,
        dtype: TimestampDtypeArg = ...,
        name: Hashable = ...,
        copy: bool = ...,
    ) -> TimestampSeries: ...
    @overload
    def __new__(  # type: ignore[misc]
        cls,
        data: _ListLike,
        index: Axes | None = ...,
        *,
        dtype: TimestampDtypeArg,
        name: Hashable = ...,
        copy: bool = ...,
    ) -> TimestampSeries: ...
    @overload
    def __new__(  # type: ignore[misc]
        cls,
        data: PeriodIndex,
        index: Axes | None = ...,
        *,
        dtype: PeriodDtype = ...,
        name: Hashable = ...,
        copy: bool = ...,
    ) -> PeriodSeries: ...
    @overload
    def __new__(  # type: ignore[misc]
        cls,
        data: TimedeltaIndex
        | Sequence[np.timedelta64 | timedelta]
        | np.timedelta64
        | timedelta,
        index: Axes | None = ...,
        *,
        dtype: TimedeltaDtypeArg = ...,
        name: Hashable = ...,
        copy: bool = ...,
    ) -> TimedeltaSeries: ...
    @overload
    def __new__(  # type: ignore[misc]
        cls,
        data: IntervalIndex[Interval[_OrderableT]]
        | Interval[_OrderableT]
        | Sequence[Interval[_OrderableT]],
        index: Axes | None = ...,
        *,
        dtype: Literal["Interval"] = ...,
        name: Hashable = ...,
        copy: bool = ...,
    ) -> IntervalSeries[_OrderableT]: ...
    @overload
    def __new__(
        cls,
        data: Scalar | _ListLike | dict[int, Any] | dict[_str, Any] | None,
        index: Axes | None = ...,
        *,
        dtype: type[S1],
        name: Hashable = ...,
        copy: bool = ...,
    ) -> Self: ...
    @overload
    def __new__(
        cls,
        data: S1 | _ListLike[S1] | dict[int, S1] | dict[_str, S1],
        index: Axes | None = ...,
        *,
        dtype: Dtype = ...,
        name: Hashable = ...,
        copy: bool = ...,
    ) -> Self: ...
    @overload
    def __new__(
        cls,
        data: Scalar | _ListLike | dict[int, Any] | dict[_str, Any] | None = ...,
        index: Axes | None = ...,
        *,
        dtype: Dtype = ...,
        name: Hashable = ...,
        copy: bool = ...,
    ) -> Series: ...
    @property
    def hasnans(self) -> bool: ...
    def div(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[float]: ...
    def rdiv(
        self,
        other: Series[S1] | Scalar,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    @property
    def dtype(self) -> DtypeObj: ...
    @property
    def dtypes(self) -> DtypeObj: ...
    @property
    def name(self) -> Hashable | None: ...
    @name.setter
    def name(self, value: Hashable | None) -> None: ...
    @property
    def values(self) -> ArrayLike: ...
    @property
    def array(self) -> ExtensionArray: ...
    def ravel(self, order: _str = ...) -> np.ndarray: ...
    def __len__(self) -> int: ...
    def view(self, dtype=...) -> Series[S1]: ...
    def __array_ufunc__(self, ufunc: Callable, method: _str, *inputs, **kwargs): ...
    def __array__(self, dtype=...) -> np.ndarray: ...
    @property
    def axes(self) -> list: ...
    def take(
        self,
        indices: Sequence,
        axis: AxisIndex = ...,
        is_copy: _bool | None = ...,
        **kwargs,
    ) -> Series[S1]: ...
    def __getattr__(self, name: _str) -> S1: ...
    @overload
    def __getitem__(
        self,
        idx: list[_str]
        | Index
        | Series[S1]
        | slice
        | MaskType
        | tuple[Hashable | slice, ...],
    ) -> Self: ...
    @overload
    def __getitem__(self, idx: Scalar) -> S1: ...
    def __setitem__(self, key, value) -> None: ...
    def repeat(
        self, repeats: int | list[int], axis: AxisIndex | None = ...
    ) -> Series[S1]: ...
    @property
    def index(self) -> Index | MultiIndex: ...
    @index.setter
    def index(self, idx: Index) -> None: ...
    # TODO: combine Level | Sequence[Level] github.com/python/mypy/issues/14311
    @overload
    def reset_index(
        self,
        level: Sequence[Level] = ...,
        *,
        drop: Literal[False] = ...,
        name: Level = ...,
        inplace: Literal[False] = ...,
        allow_duplicates: bool = ...,
    ) -> DataFrame: ...
    @overload
    def reset_index(
        self,
        level: Sequence[Level] = ...,
        *,
        drop: Literal[True],
        name: Level = ...,
        inplace: Literal[False] = ...,
        allow_duplicates: bool = ...,
    ) -> Series[S1]: ...
    @overload
    def reset_index(
        self,
        level: Sequence[Level] = ...,
        *,
        drop: bool = ...,
        name: Level = ...,
        inplace: Literal[True],
        allow_duplicates: bool = ...,
    ) -> None: ...
    @overload
    def reset_index(
        self,
        level: Level | None = ...,
        *,
        drop: Literal[False] = ...,
        name: Level = ...,
        inplace: Literal[False] = ...,
        allow_duplicates: bool = ...,
    ) -> DataFrame: ...
    @overload
    def reset_index(
        self,
        level: Level | None = ...,
        *,
        drop: Literal[True],
        name: Level = ...,
        inplace: Literal[False] = ...,
        allow_duplicates: bool = ...,
    ) -> Series[S1]: ...
    @overload
    def reset_index(
        self,
        level: Level | None = ...,
        *,
        drop: bool = ...,
        name: Level = ...,
        inplace: Literal[True],
        allow_duplicates: bool = ...,
    ) -> None: ...
    @overload
    def to_string(
        self,
        buf: FilePath | WriteBuffer[str],
        na_rep: _str = ...,
        float_format: Callable[[float], str] = ...,
        header: _bool = ...,
        index: _bool = ...,
        length: _bool = ...,
        dtype: _bool = ...,
        name: _bool = ...,
        max_rows: int | None = ...,
        min_rows: int | None = ...,
    ) -> None: ...
    @overload
    def to_string(
        self,
        buf: None = ...,
        na_rep: _str = ...,
        float_format: Callable[[float], str] = ...,
        header: _bool = ...,
        index: _bool = ...,
        length: _bool = ...,
        dtype: _bool = ...,
        name: _bool = ...,
        max_rows: int | None = ...,
        min_rows: int | None = ...,
    ) -> _str: ...
    @overload
    def to_json(
        self,
        path_or_buf: FilePath | WriteBuffer[str],
        *,
        orient: Literal["records"],
        date_format: Literal["epoch", "iso"] | None = ...,
        double_precision: int = ...,
        force_ascii: _bool = ...,
        date_unit: Literal["s", "ms", "us", "ns"] = ...,
        default_handler: Callable[[Any], _str | float | _bool | list | dict]
        | None = ...,
        lines: Literal[True],
        compression: CompressionOptions = ...,
        index: _bool = ...,
        indent: int | None = ...,
        mode: Literal["a"],
    ) -> None: ...
    @overload
    def to_json(
        self,
        path_or_buf: None = ...,
        *,
        orient: Literal["records"],
        date_format: Literal["epoch", "iso"] | None = ...,
        double_precision: int = ...,
        force_ascii: _bool = ...,
        date_unit: Literal["s", "ms", "us", "ns"] = ...,
        default_handler: Callable[[Any], _str | float | _bool | list | dict]
        | None = ...,
        lines: Literal[True],
        compression: CompressionOptions = ...,
        index: _bool = ...,
        indent: int | None = ...,
        mode: Literal["a"],
    ) -> _str: ...
    @overload
    def to_json(
        self,
        path_or_buf: FilePath | WriteBuffer[str],
        orient: JsonSeriesOrient | None = ...,
        date_format: Literal["epoch", "iso"] | None = ...,
        double_precision: int = ...,
        force_ascii: _bool = ...,
        date_unit: Literal["s", "ms", "us", "ns"] = ...,
        default_handler: Callable[[Any], _str | float | _bool | list | dict]
        | None = ...,
        lines: _bool = ...,
        compression: CompressionOptions = ...,
        index: _bool = ...,
        indent: int | None = ...,
        mode: Literal["w"] = ...,
    ) -> None: ...
    @overload
    def to_json(
        self,
        path_or_buf: None = ...,
        orient: JsonSeriesOrient | None = ...,
        date_format: Literal["epoch", "iso"] | None = ...,
        double_precision: int = ...,
        force_ascii: _bool = ...,
        date_unit: Literal["s", "ms", "us", "ns"] = ...,
        default_handler: Callable[[Any], _str | float | _bool | list | dict]
        | None = ...,
        lines: _bool = ...,
        compression: CompressionOptions = ...,
        index: _bool = ...,
        indent: int | None = ...,
        mode: Literal["w"] = ...,
    ) -> _str: ...
    def to_xarray(self) -> xr.DataArray: ...
    def items(self) -> Iterable[tuple[Hashable, S1]]: ...
    def keys(self) -> list: ...
    @overload
    def to_dict(self, *, into: type[dict] = ...) -> dict[Any, S1]: ...
    @overload
    def to_dict(
        self, *, into: type[MutableMapping] | MutableMapping
    ) -> MutableMapping[Hashable, S1]: ...
    def to_frame(self, name: object | None = ...) -> DataFrame: ...
    @overload
    def groupby(
        self,
        by: Scalar,
        axis: AxisIndex = ...,
        level: Level | None = ...,
        as_index: _bool = ...,
        sort: _bool = ...,
        group_keys: _bool = ...,
        squeeze: _bool = ...,
        observed: _bool = ...,
        dropna: _bool = ...,
    ) -> SeriesGroupBy[S1, Scalar]:
        """
Group Series using a mapper or by a Series of columns.

A groupby operation involves some combination of splitting the
object, applying a function, and combining the results. This can be
used to group large amounts of data and compute operations on these
groups.

Parameters
----------
by : mapping, function, label, pd.Grouper or list of such
    Used to determine the groups for the groupby.
    If ``by`` is a function, it's called on each value of the object's
    index. If a dict or Series is passed, the Series or dict VALUES
    will be used to determine the groups (the Series' values are first
    aligned; see ``.align()`` method). If a list or ndarray of length
    equal to the selected axis is passed (see the `groupby user guide
    <https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#splitting-an-object-into-groups>`_),
    the values are used as-is to determine the groups. A label or list
    of labels may be passed to group by the columns in ``self``.
    Notice that a tuple is interpreted as a (single) key.
axis : {0 or 'index', 1 or 'columns'}, default 0
    Split along rows (0) or columns (1). For `Series` this parameter
    is unused and defaults to 0.

    .. deprecated:: 2.1.0

        Will be removed and behave like axis=0 in a future version.
        For ``axis=1``, do ``frame.T.groupby(...)`` instead.

level : int, level name, or sequence of such, default None
    If the axis is a MultiIndex (hierarchical), group by a particular
    level or levels. Do not specify both ``by`` and ``level``.
as_index : bool, default True
    Return object with group labels as the
    index. Only relevant for DataFrame input. as_index=False is
    effectively "SQL-style" grouped output. This argument has no effect
    on filtrations (see the `filtrations in the user guide
    <https://pandas.pydata.org/docs/dev/user_guide/groupby.html#filtration>`_),
    such as ``head()``, ``tail()``, ``nth()`` and in transformations
    (see the `transformations in the user guide
    <https://pandas.pydata.org/docs/dev/user_guide/groupby.html#transformation>`_).
sort : bool, default True
    Sort group keys. Get better performance by turning this off.
    Note this does not influence the order of observations within each
    group. Groupby preserves the order of rows within each group. If False,
    the groups will appear in the same order as they did in the original DataFrame.
    This argument has no effect on filtrations (see the `filtrations in the user guide
    <https://pandas.pydata.org/docs/dev/user_guide/groupby.html#filtration>`_),
    such as ``head()``, ``tail()``, ``nth()`` and in transformations
    (see the `transformations in the user guide
    <https://pandas.pydata.org/docs/dev/user_guide/groupby.html#transformation>`_).

    .. versionchanged:: 2.0.0

        Specifying ``sort=False`` with an ordered categorical grouper will no
        longer sort the values.

group_keys : bool, default True
    When calling apply and the ``by`` argument produces a like-indexed
    (i.e. :ref:`a transform <groupby.transform>`) result, add group keys to
    index to identify pieces. By default group keys are not included
    when the result's index (and column) labels match the inputs, and
    are included otherwise.

    .. versionchanged:: 1.5.0

       Warns that ``group_keys`` will no longer be ignored when the
       result from ``apply`` is a like-indexed Series or DataFrame.
       Specify ``group_keys`` explicitly to include the group keys or
       not.

    .. versionchanged:: 2.0.0

       ``group_keys`` now defaults to ``True``.

observed : bool, default False
    This only applies if any of the groupers are Categoricals.
    If True: only show observed values for categorical groupers.
    If False: show all values for categorical groupers.

    .. deprecated:: 2.1.0

        The default value will change to True in a future version of pandas.

dropna : bool, default True
    If True, and if group keys contain NA values, NA values together
    with row/column will be dropped.
    If False, NA values will also be treated as the key in groups.

Returns
-------
pandas.api.typing.SeriesGroupBy
    Returns a groupby object that contains information about the groups.

See Also
--------
resample : Convenience method for frequency conversion and resampling
    of time series.

Notes
-----
See the `user guide
<https://pandas.pydata.org/pandas-docs/stable/groupby.html>`__ for more
detailed usage and examples, including splitting an object into groups,
iterating through groups, selecting a group, aggregation, and more.

Examples
--------
>>> ser = pd.Series([390., 350., 30., 20.],
...                 index=['Falcon', 'Falcon', 'Parrot', 'Parrot'],
...                 name="Max Speed")
>>> ser
Falcon    390.0
Falcon    350.0
Parrot     30.0
Parrot     20.0
Name: Max Speed, dtype: float64
>>> ser.groupby(["a", "b", "a", "b"]).mean()
a    210.0
b    185.0
Name: Max Speed, dtype: float64
>>> ser.groupby(level=0).mean()
Falcon    370.0
Parrot     25.0
Name: Max Speed, dtype: float64
>>> ser.groupby(ser > 100).mean()
Max Speed
False     25.0
True     370.0
Name: Max Speed, dtype: float64

**Grouping by Indexes**

We can groupby different levels of a hierarchical index
using the `level` parameter:

>>> arrays = [['Falcon', 'Falcon', 'Parrot', 'Parrot'],
...           ['Captive', 'Wild', 'Captive', 'Wild']]
>>> index = pd.MultiIndex.from_arrays(arrays, names=('Animal', 'Type'))
>>> ser = pd.Series([390., 350., 30., 20.], index=index, name="Max Speed")
>>> ser
Animal  Type
Falcon  Captive    390.0
        Wild       350.0
Parrot  Captive     30.0
        Wild        20.0
Name: Max Speed, dtype: float64
>>> ser.groupby(level=0).mean()
Animal
Falcon    370.0
Parrot     25.0
Name: Max Speed, dtype: float64
>>> ser.groupby(level="Type").mean()
Type
Captive    210.0
Wild       185.0
Name: Max Speed, dtype: float64

We can also choose to include `NA` in group keys or not by defining
`dropna` parameter, the default setting is `True`.

>>> ser = pd.Series([1, 2, 3, 3], index=["a", 'a', 'b', np.nan])
>>> ser.groupby(level=0).sum()
a    3
b    3
dtype: int64

>>> ser.groupby(level=0, dropna=False).sum()
a    3
b    3
NaN  3
dtype: int64

>>> arrays = ['Falcon', 'Falcon', 'Parrot', 'Parrot']
>>> ser = pd.Series([390., 350., 30., 20.], index=arrays, name="Max Speed")
>>> ser.groupby(["a", "b", "a", np.nan]).mean()
a    210.0
b    350.0
Name: Max Speed, dtype: float64

>>> ser.groupby(["a", "b", "a", np.nan], dropna=False).mean()
a    210.0
b    350.0
NaN   20.0
Name: Max Speed, dtype: float64
        """
        pass
    @overload
    def groupby(
        self,
        by: DatetimeIndex,
        axis: AxisIndex = ...,
        level: Level | None = ...,
        as_index: _bool = ...,
        sort: _bool = ...,
        group_keys: _bool = ...,
        squeeze: _bool = ...,
        observed: _bool = ...,
        dropna: _bool = ...,
    ) -> SeriesGroupBy[S1, Timestamp]: ...
    @overload
    def groupby(
        self,
        by: TimedeltaIndex,
        axis: AxisIndex = ...,
        level: Level | None = ...,
        as_index: _bool = ...,
        sort: _bool = ...,
        group_keys: _bool = ...,
        squeeze: _bool = ...,
        observed: _bool = ...,
        dropna: _bool = ...,
    ) -> SeriesGroupBy[S1, Timedelta]: ...
    @overload
    def groupby(
        self,
        by: PeriodIndex,
        axis: AxisIndex = ...,
        level: Level | None = ...,
        as_index: _bool = ...,
        sort: _bool = ...,
        group_keys: _bool = ...,
        squeeze: _bool = ...,
        observed: _bool = ...,
        dropna: _bool = ...,
    ) -> SeriesGroupBy[S1, Period]: ...
    @overload
    def groupby(
        self,
        by: IntervalIndex[IntervalT],
        axis: AxisIndex = ...,
        level: Level | None = ...,
        as_index: _bool = ...,
        sort: _bool = ...,
        group_keys: _bool = ...,
        squeeze: _bool = ...,
        observed: _bool = ...,
        dropna: _bool = ...,
    ) -> SeriesGroupBy[S1, IntervalT]: ...
    @overload
    def groupby(
        self,
        by: MultiIndex | GroupByObjectNonScalar = ...,
        axis: AxisIndex = ...,
        level: Level | None = ...,
        as_index: _bool = ...,
        sort: _bool = ...,
        group_keys: _bool = ...,
        squeeze: _bool = ...,
        observed: _bool = ...,
        dropna: _bool = ...,
    ) -> SeriesGroupBy[S1, tuple]: ...
    @overload
    def groupby(
        self,
        by: Series[SeriesByT],
        axis: AxisIndex = ...,
        level: Level | None = ...,
        as_index: _bool = ...,
        sort: _bool = ...,
        group_keys: _bool = ...,
        squeeze: _bool = ...,
        observed: _bool = ...,
        dropna: _bool = ...,
    ) -> SeriesGroupBy[S1, SeriesByT]: ...
    @overload
    def groupby(
        self,
        by: CategoricalIndex | Index | Series,
        axis: AxisIndex = ...,
        level: Level | None = ...,
        as_index: _bool = ...,
        sort: _bool = ...,
        group_keys: _bool = ...,
        squeeze: _bool = ...,
        observed: _bool = ...,
        dropna: _bool = ...,
    ) -> SeriesGroupBy[S1, Any]: ...
    # need the ignore because None is Hashable
    @overload
    def count(self, level: None = ...) -> int: ...  # type: ignore[misc]
    @overload
    def count(self, level: Hashable) -> Series[S1]: ...
    def mode(self, dropna=...) -> Series[S1]: ...
    def unique(self) -> np.ndarray: ...
    @overload
    def drop_duplicates(
        self, *, keep: NaPosition | Literal[False] = ..., inplace: Literal[False] = ...
    ) -> Series[S1]: ...
    @overload
    def drop_duplicates(
        self, *, keep: NaPosition | Literal[False] = ..., inplace: Literal[True]
    ) -> None: ...
    @overload
    def drop_duplicates(
        self, *, keep: NaPosition | Literal[False] = ..., inplace: bool = ...
    ) -> Series[S1] | None: ...
    def duplicated(self, keep: NaPosition | Literal[False] = ...) -> Series[_bool]: ...
    def idxmax(
        self, axis: AxisIndex = ..., skipna: _bool = ..., *args, **kwargs
    ) -> int | _str: ...
    def idxmin(
        self, axis: AxisIndex = ..., skipna: _bool = ..., *args, **kwargs
    ) -> int | _str: ...
    def round(self, decimals: int = ..., *args, **kwargs) -> Series[S1]: ...
    @overload
    def quantile(
        self,
        q: float = ...,
        interpolation: QuantileInterpolation = ...,
    ) -> float: ...
    @overload
    def quantile(
        self,
        q: _ListLike,
        interpolation: QuantileInterpolation = ...,
    ) -> Series[S1]: ...
    def corr(
        self,
        other: Series[S1],
        method: Literal["pearson", "kendall", "spearman"] = ...,
        min_periods: int = ...,
    ) -> float: ...
    def cov(
        self, other: Series[S1], min_periods: int | None = ..., ddof: int = ...
    ) -> float: ...
    def diff(self, periods: int = ...) -> Series[S1]: ...
    def autocorr(self, lag: int = ...) -> float: ...
    @overload
    def dot(self, other: Series[S1]) -> Scalar: ...
    @overload
    def dot(self, other: DataFrame) -> Series[S1]: ...
    @overload
    def dot(
        self, other: ArrayLike | dict[_str, np.ndarray] | Sequence[S1] | Index[S1]
    ) -> np.ndarray: ...
    def __matmul__(self, other): ...
    def __rmatmul__(self, other): ...
    @overload
    def searchsorted(  # type: ignore[misc]
        self,
        value: _ListLike,
        side: Literal["left", "right"] = ...,
        sorter: _ListLike | None = ...,
    ) -> list[int]:
        """
Find indices where elements should be inserted to maintain order.

Find the indices into a sorted Series `self` such that, if the
corresponding elements in `value` were inserted before the indices,
the order of `self` would be preserved.

.. note::

    The Series *must* be monotonically sorted, otherwise
    wrong locations will likely be returned. Pandas does *not*
    check this for you.

Parameters
----------
value : array-like or scalar
    Values to insert into `self`.
side : {'left', 'right'}, optional
    If 'left', the index of the first suitable location found is given.
    If 'right', return the last such index.  If there is no suitable
    index, return either 0 or N (where N is the length of `self`).
sorter : 1-D array-like, optional
    Optional array of integer indices that sort `self` into ascending
    order. They are typically the result of ``np.argsort``.

Returns
-------
int or array of int
    A scalar or array of insertion points with the
    same shape as `value`.

See Also
--------
sort_values : Sort by the values along either axis.
numpy.searchsorted : Similar method from NumPy.

Notes
-----
Binary search is used to find the required insertion points.

Examples
--------
>>> ser = pd.Series([1, 2, 3])
>>> ser
0    1
1    2
2    3
dtype: int64

>>> ser.searchsorted(4)
3

>>> ser.searchsorted([0, 4])
array([0, 3])

>>> ser.searchsorted([1, 3], side='left')
array([0, 2])

>>> ser.searchsorted([1, 3], side='right')
array([1, 3])

>>> ser = pd.Series(pd.to_datetime(['3/11/2000', '3/12/2000', '3/13/2000']))
>>> ser
0   2000-03-11
1   2000-03-12
2   2000-03-13
dtype: datetime64[ns]

>>> ser.searchsorted('3/14/2000')
3

>>> ser = pd.Categorical(
...     ['apple', 'bread', 'bread', 'cheese', 'milk'], ordered=True
... )
>>> ser
['apple', 'bread', 'bread', 'cheese', 'milk']
Categories (4, object): ['apple' < 'bread' < 'cheese' < 'milk']

>>> ser.searchsorted('bread')
1

>>> ser.searchsorted(['bread'], side='right')
array([3])

If the values are not monotonically sorted, wrong locations
may be returned:

>>> ser = pd.Series([2, 1, 3])
>>> ser
0    2
1    1
2    3
dtype: int64

>>> ser.searchsorted(1)  # doctest: +SKIP
0  # wrong result, correct would be 1
        """
        pass
    @overload
    def searchsorted(
        self,
        value: Scalar,
        side: Literal["left", "right"] = ...,
        sorter: _ListLike | None = ...,
    ) -> int: ...
    @overload
    def compare(
        self,
        other: Series,
        align_axis: AxisIndex,
        keep_shape: bool = ...,
        keep_equal: bool = ...,
    ) -> Series: ...
    @overload
    def compare(
        self,
        other: Series,
        align_axis: AxisColumn = ...,
        keep_shape: bool = ...,
        keep_equal: bool = ...,
    ) -> DataFrame: ...
    def combine(
        self, other: Series[S1], func: Callable, fill_value: Scalar | None = ...
    ) -> Series[S1]: ...
    def combine_first(self, other: Series[S1]) -> Series[S1]: ...
    def update(self, other: Series[S1] | Sequence[S1] | Mapping[int, S1]) -> None: ...
    @overload
    def sort_values(
        self,
        *,
        axis: Axis = ...,
        ascending: _bool | Sequence[_bool] = ...,
        kind: SortKind = ...,
        na_position: NaPosition = ...,
        ignore_index: _bool = ...,
        inplace: Literal[True],
        key: Callable | None = ...,
    ) -> None: ...
    @overload
    def sort_values(
        self,
        *,
        axis: Axis = ...,
        ascending: _bool | Sequence[_bool] = ...,
        kind: SortKind = ...,
        na_position: NaPosition = ...,
        ignore_index: _bool = ...,
        inplace: Literal[False] = ...,
        key: Callable | None = ...,
    ) -> Series[S1]: ...
    @overload
    def sort_values(
        self,
        *,
        axis: Axis = ...,
        ascending: _bool | Sequence[_bool] = ...,
        inplace: _bool | None = ...,
        kind: SortKind = ...,
        na_position: NaPosition = ...,
        ignore_index: _bool = ...,
        key: Callable | None = ...,
    ) -> Series[S1] | None: ...
    @overload
    def sort_index(
        self,
        *,
        axis: Axis = ...,
        level: Level | None = ...,
        ascending: _bool | Sequence[_bool] = ...,
        kind: SortKind = ...,
        na_position: NaPosition = ...,
        sort_remaining: _bool = ...,
        ignore_index: _bool = ...,
        inplace: Literal[True],
        key: Callable | None = ...,
    ) -> None: ...
    @overload
    def sort_index(
        self,
        *,
        axis: Axis = ...,
        level: Level | list[int] | list[_str] | None = ...,
        ascending: _bool | Sequence[_bool] = ...,
        kind: SortKind = ...,
        na_position: NaPosition = ...,
        sort_remaining: _bool = ...,
        ignore_index: _bool = ...,
        inplace: Literal[False] = ...,
        key: Callable | None = ...,
    ) -> Self: ...
    @overload
    def sort_index(
        self,
        *,
        axis: Axis = ...,
        level: Level | list[int] | list[_str] | None = ...,
        ascending: _bool | Sequence[_bool] = ...,
        inplace: _bool | None = ...,
        kind: SortKind = ...,
        na_position: NaPosition = ...,
        sort_remaining: _bool = ...,
        ignore_index: _bool = ...,
        key: Callable | None = ...,
    ) -> Series | None: ...
    def argsort(
        self,
        axis: AxisIndex = ...,
        kind: SortKind = ...,
        order: None = ...,
    ) -> Series[int]: ...
    def nlargest(
        self, n: int = ..., keep: NaPosition | Literal["all"] = ...
    ) -> Series[S1]: ...
    def nsmallest(
        self, n: int = ..., keep: NaPosition | Literal["all"] = ...
    ) -> Series[S1]: ...
    def swaplevel(
        self, i: Level = ..., j: Level = ..., copy: _bool = ...
    ) -> Series[S1]: ...
    def reorder_levels(self, order: list) -> Series[S1]: ...
    def explode(self) -> Series[S1]: ...
    def unstack(
        self,
        level: Level = ...,
        fill_value: int | _str | dict | None = ...,
    ) -> DataFrame: ...
    def map(self, arg, na_action: Literal["ignore"] | None = ...) -> Series[S1]: ...
    @overload
    def aggregate(  # type: ignore[misc]
        self: Series[int],
        func: Literal["mean"],
        axis: AxisIndex = ...,
        *args,
        **kwargs,
    ) -> float:
        """
Aggregate using one or more operations over the specified axis.

Parameters
----------
func : function, str, list or dict
    Function to use for aggregating the data. If a function, must either
    work when passed a Series or when passed to Series.apply.

    Accepted combinations are:

    - function
    - string function name
    - list of functions and/or function names, e.g. ``[np.sum, 'mean']``
    - dict of axis labels -> functions, function names or list of such.
axis : {0 or 'index'}
        Unused. Parameter needed for compatibility with DataFrame.
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

    Return scalar, Series or DataFrame.

See Also
--------
Series.apply : Invoke function on a Series.
Series.transform : Transform function producing a Series with like indexes.

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
>>> s = pd.Series([1, 2, 3, 4])
>>> s
0    1
1    2
2    3
3    4
dtype: int64

>>> s.agg('min')
1

>>> s.agg(['min', 'max'])
min   1
max   4
dtype: int64
        """
        pass
    @overload
    def aggregate(
        self,
        func: AggFuncTypeBase,
        axis: AxisIndex = ...,
        *args,
        **kwargs,
    ) -> S1: ...
    @overload
    def aggregate(
        self,
        func: AggFuncTypeSeriesToFrame = ...,
        axis: AxisIndex = ...,
        *args,
        **kwargs,
    ) -> Series: ...
    agg = aggregate
    @overload
    def transform(
        self,
        func: AggFuncTypeBase,
        axis: AxisIndex = ...,
        *args,
        **kwargs,
    ) -> Series[S1]:
        """
Call ``func`` on self producing a Series with the same axis shape as self.

Parameters
----------
func : function, str, list-like or dict-like
    Function to use for transforming the data. If a function, must either
    work when passed a Series or when passed to Series.apply. If func
    is both list-like and dict-like, dict-like behavior takes precedence.

    Accepted combinations are:

    - function
    - string function name
    - list-like of functions and/or function names, e.g. ``[np.exp, 'sqrt']``
    - dict-like of axis labels -> functions, function names or list-like of such.
axis : {0 or 'index'}
        Unused. Parameter needed for compatibility with DataFrame.
*args
    Positional arguments to pass to `func`.
**kwargs
    Keyword arguments to pass to `func`.

Returns
-------
Series
    A Series that must have the same length as self.

Raises
------
ValueError : If the returned Series has a different length than self.

See Also
--------
Series.agg : Only perform aggregating type operations.
Series.apply : Invoke function on a Series.

Notes
-----
Functions that mutate the passed object can produce unexpected
behavior or errors and are not supported. See :ref:`gotchas.udf-mutation`
for more details.

Examples
--------
>>> df = pd.DataFrame({'A': range(3), 'B': range(1, 4)})
>>> df
   A  B
0  0  1
1  1  2
2  2  3
>>> df.transform(lambda x: x + 1)
   A  B
0  1  2
1  2  3
2  3  4

Even though the resulting Series must have the same length as the
input Series, it is possible to provide several input functions:

>>> s = pd.Series(range(3))
>>> s
0    0
1    1
2    2
dtype: int64
>>> s.transform([np.sqrt, np.exp])
       sqrt        exp
0  0.000000   1.000000
1  1.000000   2.718282
2  1.414214   7.389056

You can call transform on a GroupBy object:

>>> df = pd.DataFrame({
...     "Date": [
...         "2015-05-08", "2015-05-07", "2015-05-06", "2015-05-05",
...         "2015-05-08", "2015-05-07", "2015-05-06", "2015-05-05"],
...     "Data": [5, 8, 6, 1, 50, 100, 60, 120],
... })
>>> df
         Date  Data
0  2015-05-08     5
1  2015-05-07     8
2  2015-05-06     6
3  2015-05-05     1
4  2015-05-08    50
5  2015-05-07   100
6  2015-05-06    60
7  2015-05-05   120
>>> df.groupby('Date')['Data'].transform('sum')
0     55
1    108
2     66
3    121
4     55
5    108
6     66
7    121
Name: Data, dtype: int64

>>> df = pd.DataFrame({
...     "c": [1, 1, 1, 2, 2, 2, 2],
...     "type": ["m", "n", "o", "m", "m", "n", "n"]
... })
>>> df
   c type
0  1    m
1  1    n
2  1    o
3  2    m
4  2    m
5  2    n
6  2    n
>>> df['size'] = df.groupby('c')['type'].transform(len)
>>> df
   c type size
0  1    m    3
1  1    n    3
2  1    o    3
3  2    m    4
4  2    m    4
5  2    n    4
6  2    n    4
        """
        pass
    @overload
    def transform(
        self,
        func: list[AggFuncTypeBase] | AggFuncTypeDictFrame,
        axis: AxisIndex = ...,
        *args,
        **kwargs,
    ) -> DataFrame: ...
    @overload
    def apply(
        self,
        func: Callable[..., Scalar | Sequence | set | Mapping | NAType | None],
        convertDType: _bool = ...,
        args: tuple = ...,
        **kwds,
    ) -> Series: ...
    @overload
    def apply(
        self,
        func: Callable[..., Series],
        convertDType: _bool = ...,
        args: tuple = ...,
        **kwds,
    ) -> DataFrame: ...
    def align(
        self,
        other: DataFrame | Series,
        join: JoinHow = ...,
        axis: Axis | None = ...,
        level: Level | None = ...,
        copy: _bool = ...,
        fill_value=...,
        method: FillnaOptions | None = ...,
        limit: int | None = ...,
        fill_axis: AxisIndex = ...,
        broadcast_axis: AxisIndex | None = ...,
    ) -> tuple[Series, Series]: ...
    @overload
    def rename(
        self,
        index: Renamer | Hashable | None = ...,
        *,
        axis: Axis | None = ...,
        copy: bool = ...,
        inplace: Literal[True],
        level: Level | None = ...,
        errors: IgnoreRaise = ...,
    ) -> None: ...
    @overload
    def rename(
        self,
        index: Renamer | None = ...,
        *,
        axis: Axis | None = ...,
        copy: bool = ...,
        inplace: Literal[False] = ...,
        level: Level | None = ...,
        errors: IgnoreRaise = ...,
    ) -> Self: ...
    @overload
    def rename(
        self,
        index: Hashable | None = ...,
        *,
        axis: Axis | None = ...,
        copy: bool = ...,
        inplace: Literal[False] = ...,
        level: Level | None = ...,
        errors: IgnoreRaise = ...,
    ) -> Self: ...
    @overload
    def rename(
        self,
        index: Renamer | Hashable | None = ...,
        *,
        axis: Axis | None = ...,
        copy: bool = ...,
        inplace: bool = ...,
        level: Level | None = ...,
        errors: IgnoreRaise = ...,
    ) -> Series | None: ...
    def reindex_like(
        self,
        other: Series[S1],
        method: _str | FillnaOptions | Literal["nearest"] | None = ...,
        copy: _bool = ...,
        limit: int | None = ...,
        tolerance: float | None = ...,
    ) -> Self: ...
    @overload
    def drop(
        self,
        labels: Hashable | list[HashableT1] | Index = ...,
        *,
        axis: Axis = ...,
        index: Hashable | list[HashableT2] | Index = ...,
        columns: Hashable | list[HashableT3] | Index = ...,
        level: Level | None = ...,
        inplace: Literal[True],
        errors: IgnoreRaise = ...,
    ) -> None: ...
    @overload
    def drop(
        self,
        labels: Hashable | list[HashableT1] | Index = ...,
        *,
        axis: Axis = ...,
        index: Hashable | list[HashableT2] | Index = ...,
        columns: Hashable | list[HashableT3] | Index = ...,
        level: Level | None = ...,
        inplace: Literal[False] = ...,
        errors: IgnoreRaise = ...,
    ) -> Self: ...
    @overload
    def drop(
        self,
        labels: Hashable | list[HashableT1] | Index = ...,
        *,
        axis: Axis = ...,
        index: Hashable | list[HashableT2] | Index = ...,
        columns: Hashable | list[HashableT3] | Index = ...,
        level: Level | None = ...,
        inplace: bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Series | None: ...
    @overload
    def fillna(
        self,
        value: Scalar | NAType | dict | Series[S1] | DataFrame | None = ...,
        *,
        method: FillnaOptions | None = ...,
        axis: AxisIndex = ...,
        limit: int | None = ...,
        downcast: dict | None = ...,
        inplace: Literal[True],
    ) -> None: ...
    @overload
    def fillna(
        self,
        value: Scalar | NAType | dict | Series[S1] | DataFrame | None = ...,
        *,
        method: FillnaOptions | None = ...,
        axis: AxisIndex = ...,
        limit: int | None = ...,
        downcast: dict | None = ...,
        inplace: Literal[False] = ...,
    ) -> Series[S1]: ...
    @overload
    def fillna(
        self,
        value: Scalar | NAType | dict | Series[S1] | DataFrame | None = ...,
        *,
        method: FillnaOptions | None = ...,
        axis: AxisIndex = ...,
        inplace: _bool = ...,
        limit: int | None = ...,
        downcast: dict | None = ...,
    ) -> Series[S1] | None: ...
    @overload
    def replace(
        self,
        to_replace: _str | list | dict | Series[S1] | float | None = ...,
        value: Scalar | NAType | dict | list | _str | None = ...,
        *,
        inplace: Literal[False] = ...,
        limit: int | None = ...,
        regex=...,
        method: ReplaceMethod = ...,
    ) -> Series[S1]: ...
    @overload
    def replace(
        self,
        to_replace: _str | list | dict | Series[S1] | float | None = ...,
        value: Scalar | NAType | dict | list | _str | None = ...,
        *,
        limit: int | None = ...,
        regex=...,
        method: ReplaceMethod = ...,
        inplace: Literal[True],
    ) -> None: ...
    @overload
    def replace(
        self,
        to_replace: _str | list | dict | Series[S1] | float | None = ...,
        value: Scalar | NAType | dict | list | _str | None = ...,
        *,
        inplace: _bool = ...,
        limit: int | None = ...,
        regex=...,
        method: ReplaceMethod = ...,
    ) -> Series[S1] | None: ...
    def shift(
        self,
        periods: int = ...,
        freq=...,
        axis: AxisIndex = ...,
        fill_value: object | None = ...,
    ) -> Series[S1]: ...
    def memory_usage(self, index: _bool = ..., deep: _bool = ...) -> int: ...
    def isin(self, values: Iterable | Series[S1] | dict) -> Series[_bool]: ...
    def between(
        self,
        left: Scalar | ListLikeU,
        right: Scalar | ListLikeU,
        inclusive: Literal["both", "neither", "left", "right"] = ...,
    ) -> Series[_bool]: ...
    def isna(self) -> Series[_bool]:
        """
Detect missing values.

Return a boolean same-sized object indicating if the values are NA.
NA values, such as None or :attr:`numpy.NaN`, gets mapped to True
values.
Everything else gets mapped to False values. Characters such as empty
strings ``''`` or :attr:`numpy.inf` are not considered NA values
(unless you set ``pandas.options.mode.use_inf_as_na = True``).

Returns
-------
Series
    Mask of bool values for each element in Series that
    indicates whether an element is an NA value.

See Also
--------
Series.isnull : Alias of isna.
Series.notna : Boolean inverse of isna.
Series.dropna : Omit axes labels with missing values.
isna : Top-level isna.

Examples
--------
Show which entries in a DataFrame are NA.

>>> df = pd.DataFrame(dict(age=[5, 6, np.nan],
...                        born=[pd.NaT, pd.Timestamp('1939-05-27'),
...                              pd.Timestamp('1940-04-25')],
...                        name=['Alfred', 'Batman', ''],
...                        toy=[None, 'Batmobile', 'Joker']))
>>> df
   age       born    name        toy
0  5.0        NaT  Alfred       None
1  6.0 1939-05-27  Batman  Batmobile
2  NaN 1940-04-25              Joker

>>> df.isna()
     age   born   name    toy
0  False   True  False   True
1  False  False  False  False
2   True  False  False  False

Show which entries in a Series are NA.

>>> ser = pd.Series([5, 6, np.nan])
>>> ser
0    5.0
1    6.0
2    NaN
dtype: float64

>>> ser.isna()
0    False
1    False
2     True
dtype: bool
        """
        pass
    def isnull(self) -> Series[_bool]:
        """
Series.isnull is an alias for Series.isna.

Detect missing values.

Return a boolean same-sized object indicating if the values are NA.
NA values, such as None or :attr:`numpy.NaN`, gets mapped to True
values.
Everything else gets mapped to False values. Characters such as empty
strings ``''`` or :attr:`numpy.inf` are not considered NA values
(unless you set ``pandas.options.mode.use_inf_as_na = True``).

Returns
-------
Series
    Mask of bool values for each element in Series that
    indicates whether an element is an NA value.

See Also
--------
Series.isnull : Alias of isna.
Series.notna : Boolean inverse of isna.
Series.dropna : Omit axes labels with missing values.
isna : Top-level isna.

Examples
--------
Show which entries in a DataFrame are NA.

>>> df = pd.DataFrame(dict(age=[5, 6, np.nan],
...                        born=[pd.NaT, pd.Timestamp('1939-05-27'),
...                              pd.Timestamp('1940-04-25')],
...                        name=['Alfred', 'Batman', ''],
...                        toy=[None, 'Batmobile', 'Joker']))
>>> df
   age       born    name        toy
0  5.0        NaT  Alfred       None
1  6.0 1939-05-27  Batman  Batmobile
2  NaN 1940-04-25              Joker

>>> df.isna()
     age   born   name    toy
0  False   True  False   True
1  False  False  False  False
2   True  False  False  False

Show which entries in a Series are NA.

>>> ser = pd.Series([5, 6, np.nan])
>>> ser
0    5.0
1    6.0
2    NaN
dtype: float64

>>> ser.isna()
0    False
1    False
2     True
dtype: bool
        """
        pass
    def notna(self) -> Series[_bool]:
        """
Detect existing (non-missing) values.

Return a boolean same-sized object indicating if the values are not NA.
Non-missing values get mapped to True. Characters such as empty
strings ``''`` or :attr:`numpy.inf` are not considered NA values
(unless you set ``pandas.options.mode.use_inf_as_na = True``).
NA values, such as None or :attr:`numpy.NaN`, get mapped to False
values.

Returns
-------
Series
    Mask of bool values for each element in Series that
    indicates whether an element is not an NA value.

See Also
--------
Series.notnull : Alias of notna.
Series.isna : Boolean inverse of notna.
Series.dropna : Omit axes labels with missing values.
notna : Top-level notna.

Examples
--------
Show which entries in a DataFrame are not NA.

>>> df = pd.DataFrame(dict(age=[5, 6, np.nan],
...                        born=[pd.NaT, pd.Timestamp('1939-05-27'),
...                              pd.Timestamp('1940-04-25')],
...                        name=['Alfred', 'Batman', ''],
...                        toy=[None, 'Batmobile', 'Joker']))
>>> df
   age       born    name        toy
0  5.0        NaT  Alfred       None
1  6.0 1939-05-27  Batman  Batmobile
2  NaN 1940-04-25              Joker

>>> df.notna()
     age   born  name    toy
0   True  False  True  False
1   True   True  True   True
2  False   True  True   True

Show which entries in a Series are not NA.

>>> ser = pd.Series([5, 6, np.nan])
>>> ser
0    5.0
1    6.0
2    NaN
dtype: float64

>>> ser.notna()
0     True
1     True
2    False
dtype: bool
        """
        pass
    def notnull(self) -> Series[_bool]:
        """
Series.notnull is an alias for Series.notna.

Detect existing (non-missing) values.

Return a boolean same-sized object indicating if the values are not NA.
Non-missing values get mapped to True. Characters such as empty
strings ``''`` or :attr:`numpy.inf` are not considered NA values
(unless you set ``pandas.options.mode.use_inf_as_na = True``).
NA values, such as None or :attr:`numpy.NaN`, get mapped to False
values.

Returns
-------
Series
    Mask of bool values for each element in Series that
    indicates whether an element is not an NA value.

See Also
--------
Series.notnull : Alias of notna.
Series.isna : Boolean inverse of notna.
Series.dropna : Omit axes labels with missing values.
notna : Top-level notna.

Examples
--------
Show which entries in a DataFrame are not NA.

>>> df = pd.DataFrame(dict(age=[5, 6, np.nan],
...                        born=[pd.NaT, pd.Timestamp('1939-05-27'),
...                              pd.Timestamp('1940-04-25')],
...                        name=['Alfred', 'Batman', ''],
...                        toy=[None, 'Batmobile', 'Joker']))
>>> df
   age       born    name        toy
0  5.0        NaT  Alfred       None
1  6.0 1939-05-27  Batman  Batmobile
2  NaN 1940-04-25              Joker

>>> df.notna()
     age   born  name    toy
0   True  False  True  False
1   True   True  True   True
2  False   True  True   True

Show which entries in a Series are not NA.

>>> ser = pd.Series([5, 6, np.nan])
>>> ser
0    5.0
1    6.0
2    NaN
dtype: float64

>>> ser.notna()
0     True
1     True
2    False
dtype: bool
        """
        pass
    @overload
    def dropna(
        self,
        *,
        axis: AxisIndex = ...,
        inplace: Literal[True],
        how: Literal["any", "all"] | None = ...,
    ) -> None: ...
    @overload
    def dropna(
        self,
        *,
        axis: AxisIndex = ...,
        inplace: Literal[False] = ...,
        how: Literal["any", "all"] | None = ...,
    ) -> Series[S1]: ...
    @overload
    def dropna(
        self,
        *,
        axis: AxisIndex = ...,
        inplace: _bool = ...,
        how: Literal["any", "all"] | None = ...,
    ) -> Series[S1] | None: ...
    def to_timestamp(
        self,
        freq=...,
        how: TimestampConvention = ...,
        copy: _bool = ...,
    ) -> Series[S1]: ...
    def to_period(self, freq: _str | None = ..., copy: _bool = ...) -> DataFrame: ...
    @property
    def str(self) -> StringMethods[Series, DataFrame]: ...
    @property
    def dt(self) -> CombinedDatetimelikeProperties: ...
    @property
    def plot(self) -> PlotAccessor: ...
    sparse = ...
    def hist(
        self,
        by: object | None = ...,
        ax: PlotAxes | None = ...,
        grid: _bool = ...,
        xlabelsize: int | None = ...,
        xrot: float | None = ...,
        ylabelsize: int | None = ...,
        yrot: float | None = ...,
        figsize: tuple[float, float] | None = ...,
        bins: int | Sequence = ...,
        backend: _str | None = ...,
        **kwargs,
    ) -> SubplotBase: ...
    def swapaxes(
        self, axis1: AxisIndex, axis2: AxisIndex, copy: _bool = ...
    ) -> Series[S1]: ...
    def droplevel(self, level: Level | list[Level], axis: AxisIndex = ...) -> Self: ...
    def pop(self, item: Hashable) -> S1: ...
    def squeeze(self, axis: AxisIndex | None = ...) -> Scalar: ...
    def __abs__(self) -> Series[S1]: ...
    def add_prefix(self, prefix: _str, axis: AxisIndex | None = ...) -> Series[S1]: ...
    def add_suffix(self, suffix: _str, axis: AxisIndex | None = ...) -> Series[S1]: ...
    def reindex(
        self,
        index: Axes | None = ...,
        method: FillnaOptions | Literal["nearest"] | None = ...,
        copy: bool = ...,
        level: int | _str = ...,
        fill_value: Scalar | None = ...,
        limit: int | None = ...,
        tolerance: float | None = ...,
    ) -> Series[S1]:
        """
Conform Series to new index with optional filling logic.

Places NA/NaN in locations having no value in the previous index. A new object
is produced unless the new index is equivalent to the current one and
``copy=False``.

Parameters
----------

index : array-like, optional
    New labels for the index. Preferably an Index object to avoid
    duplicating data.
axis : int or str, optional
    Unused.
method : {None, 'backfill'/'bfill', 'pad'/'ffill', 'nearest'}
    Method to use for filling holes in reindexed DataFrame.
    Please note: this is only applicable to DataFrames/Series with a
    monotonically increasing/decreasing index.

    * None (default): don't fill gaps
    * pad / ffill: Propagate last valid observation forward to next
      valid.
    * backfill / bfill: Use next valid observation to fill gap.
    * nearest: Use nearest valid observations to fill gap.

copy : bool, default True
    Return a new object, even if the passed indexes are the same.
level : int or name
    Broadcast across a level, matching Index values on the
    passed MultiIndex level.
fill_value : scalar, default np.nan
    Value to use for missing values. Defaults to NaN, but can be any
    "compatible" value.
limit : int, default None
    Maximum number of consecutive elements to forward or backward fill.
tolerance : optional
    Maximum distance between original and new labels for inexact
    matches. The values of the index at the matching locations most
    satisfy the equation ``abs(index[indexer] - target) <= tolerance``.

    Tolerance may be a scalar value, which applies the same tolerance
    to all values, or list-like, which applies variable tolerance per
    element. List-like includes list, tuple, array, Series, and must be
    the same size as the index and its dtype must exactly match the
    index's type.

Returns
-------
Series with changed index.

See Also
--------
DataFrame.set_index : Set row labels.
DataFrame.reset_index : Remove row labels or move them to new columns.
DataFrame.reindex_like : Change to same indices as other DataFrame.

Examples
--------
``DataFrame.reindex`` supports two calling conventions

* ``(index=index_labels, columns=column_labels, ...)``
* ``(labels, axis={'index', 'columns'}, ...)``

We *highly* recommend using keyword arguments to clarify your
intent.

Create a dataframe with some fictional data.

>>> index = ['Firefox', 'Chrome', 'Safari', 'IE10', 'Konqueror']
>>> df = pd.DataFrame({'http_status': [200, 200, 404, 404, 301],
...                   'response_time': [0.04, 0.02, 0.07, 0.08, 1.0]},
...                   index=index)
>>> df
           http_status  response_time
Firefox            200           0.04
Chrome             200           0.02
Safari             404           0.07
IE10               404           0.08
Konqueror          301           1.00

Create a new index and reindex the dataframe. By default
values in the new index that do not have corresponding
records in the dataframe are assigned ``NaN``.

>>> new_index = ['Safari', 'Iceweasel', 'Comodo Dragon', 'IE10',
...              'Chrome']
>>> df.reindex(new_index)
               http_status  response_time
Safari               404.0           0.07
Iceweasel              NaN            NaN
Comodo Dragon          NaN            NaN
IE10                 404.0           0.08
Chrome               200.0           0.02

We can fill in the missing values by passing a value to
the keyword ``fill_value``. Because the index is not monotonically
increasing or decreasing, we cannot use arguments to the keyword
``method`` to fill the ``NaN`` values.

>>> df.reindex(new_index, fill_value=0)
               http_status  response_time
Safari                 404           0.07
Iceweasel                0           0.00
Comodo Dragon            0           0.00
IE10                   404           0.08
Chrome                 200           0.02

>>> df.reindex(new_index, fill_value='missing')
              http_status response_time
Safari                404          0.07
Iceweasel         missing       missing
Comodo Dragon     missing       missing
IE10                  404          0.08
Chrome                200          0.02

We can also reindex the columns.

>>> df.reindex(columns=['http_status', 'user_agent'])
           http_status  user_agent
Firefox            200         NaN
Chrome             200         NaN
Safari             404         NaN
IE10               404         NaN
Konqueror          301         NaN

Or we can use "axis-style" keyword arguments

>>> df.reindex(['http_status', 'user_agent'], axis="columns")
           http_status  user_agent
Firefox            200         NaN
Chrome             200         NaN
Safari             404         NaN
IE10               404         NaN
Konqueror          301         NaN

To further illustrate the filling functionality in
``reindex``, we will create a dataframe with a
monotonically increasing index (for example, a sequence
of dates).

>>> date_index = pd.date_range('1/1/2010', periods=6, freq='D')
>>> df2 = pd.DataFrame({"prices": [100, 101, np.nan, 100, 89, 88]},
...                    index=date_index)
>>> df2
            prices
2010-01-01   100.0
2010-01-02   101.0
2010-01-03     NaN
2010-01-04   100.0
2010-01-05    89.0
2010-01-06    88.0

Suppose we decide to expand the dataframe to cover a wider
date range.

>>> date_index2 = pd.date_range('12/29/2009', periods=10, freq='D')
>>> df2.reindex(date_index2)
            prices
2009-12-29     NaN
2009-12-30     NaN
2009-12-31     NaN
2010-01-01   100.0
2010-01-02   101.0
2010-01-03     NaN
2010-01-04   100.0
2010-01-05    89.0
2010-01-06    88.0
2010-01-07     NaN

The index entries that did not have a value in the original data frame
(for example, '2009-12-29') are by default filled with ``NaN``.
If desired, we can fill in the missing values using one of several
options.

For example, to back-propagate the last valid value to fill the ``NaN``
values, pass ``bfill`` as an argument to the ``method`` keyword.

>>> df2.reindex(date_index2, method='bfill')
            prices
2009-12-29   100.0
2009-12-30   100.0
2009-12-31   100.0
2010-01-01   100.0
2010-01-02   101.0
2010-01-03     NaN
2010-01-04   100.0
2010-01-05    89.0
2010-01-06    88.0
2010-01-07     NaN

Please note that the ``NaN`` value present in the original dataframe
(at index value 2010-01-03) will not be filled by any of the
value propagation schemes. This is because filling while reindexing
does not look at dataframe values, but only compares the original and
desired indexes. If you do want to fill in the ``NaN`` values present
in the original dataframe, use the ``fillna()`` method.

See the :ref:`user guide <basics.reindexing>` for more.
        """
        pass
    def filter(
        self,
        items: _ListLike | None = ...,
        like: _str | None = ...,
        regex: _str | None = ...,
        axis: AxisIndex | None = ...,
    ) -> Series[S1]: ...
    def head(self, n: int = ...) -> Series[S1]: ...
    def tail(self, n: int = ...) -> Series[S1]: ...
    def sample(
        self,
        n: int | None = ...,
        frac: float | None = ...,
        replace: _bool = ...,
        weights: _str | _ListLike | np.ndarray | None = ...,
        random_state: RandomState | None = ...,
        axis: AxisIndex | None = ...,
        ignore_index: _bool = ...,
    ) -> Series[S1]: ...
    @overload
    def astype(  # type: ignore[misc]
        self,
        dtype: BooleanDtypeArg,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Series[bool]: ...
    @overload
    def astype(
        self,
        dtype: IntDtypeArg | UIntDtypeArg,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Series[int]: ...
    @overload
    def astype(
        self,
        dtype: StrDtypeArg,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Series[_str]: ...
    @overload
    def astype(
        self,
        dtype: BytesDtypeArg,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Series[bytes]: ...
    @overload
    def astype(
        self,
        dtype: FloatDtypeArg,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Series[float]: ...
    @overload
    def astype(
        self,
        dtype: ComplexDtypeArg,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Series[complex]: ...
    @overload
    def astype(
        self,
        dtype: TimedeltaDtypeArg,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> TimedeltaSeries: ...
    @overload
    def astype(
        self,
        dtype: TimestampDtypeArg,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> TimestampSeries: ...
    @overload
    def astype(
        self,
        dtype: CategoryDtypeArg,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Series: ...
    @overload
    def astype(
        self,
        dtype: ObjectDtypeArg | VoidDtypeArg | ExtensionDtype | DtypeObj,
        copy: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Series: ...
    def copy(self, deep: _bool = ...) -> Series[S1]: ...
    def infer_objects(self) -> Series[S1]: ...
    @overload
    def ffill(
        self,
        *,
        axis: AxisIndex | None = ...,
        inplace: Literal[True],
        limit: int | None = ...,
        downcast: dict | None = ...,
    ) -> None: ...
    @overload
    def ffill(
        self,
        *,
        axis: AxisIndex | None = ...,
        inplace: Literal[False] = ...,
        limit: int | None = ...,
        downcast: dict | None = ...,
    ) -> Series[S1]: ...
    @overload
    def bfill(
        self,
        *,
        axis: AxisIndex | None = ...,
        inplace: Literal[True],
        limit: int | None = ...,
        downcast: dict | None = ...,
    ) -> None: ...
    @overload
    def bfill(
        self,
        *,
        axis: AxisIndex | None = ...,
        inplace: Literal[False] = ...,
        limit: int | None = ...,
        downcast: dict | None = ...,
    ) -> Series[S1]: ...
    @overload
    def bfill(
        self,
        *,
        value: S1 | dict | Series[S1] | DataFrame,
        axis: AxisIndex = ...,
        inplace: _bool = ...,
        limit: int | None = ...,
        downcast: dict | None = ...,
    ) -> Series[S1] | None: ...
    def interpolate(
        self,
        method: InterpolateOptions = ...,
        *,
        axis: AxisIndex | None = ...,
        limit: int | None = ...,
        inplace: _bool = ...,
        limit_direction: Literal["forward", "backward", "both"] | None = ...,
        limit_area: Literal["inside", "outside"] | None = ...,
        downcast: Literal["infer"] | None = ...,
        **kwargs,
    ) -> Series[S1]: ...
    def asof(
        self,
        where: Scalar | Sequence[Scalar],
        subset: _str | Sequence[_str] | None = ...,
    ) -> Scalar | Series[S1]: ...
    def clip(
        self,
        lower: AnyArrayLike | float | None = ...,
        upper: AnyArrayLike | float | None = ...,
        *,
        axis: AxisIndex | None = ...,
        inplace: _bool = ...,
        **kwargs,
    ) -> Series[S1]: ...
    def asfreq(
        self,
        freq,
        method: FillnaOptions | None = ...,
        how: Literal["start", "end"] | None = ...,
        normalize: _bool = ...,
        fill_value: Scalar | None = ...,
    ) -> Series[S1]: ...
    def at_time(
        self,
        time: _str | time,
        asof: _bool = ...,
        axis: AxisIndex | None = ...,
    ) -> Series[S1]: ...
    def between_time(
        self,
        start_time: _str | time,
        end_time: _str | time,
        axis: AxisIndex | None = ...,
    ) -> Series[S1]: ...
    def resample(
        self,
        rule,
        axis: AxisIndex = ...,
        closed: _str | None = ...,
        label: _str | None = ...,
        convention: TimestampConvention = ...,
        kind: Literal["timestamp", "period"] | None = ...,
        loffset=...,
        base: int = ...,
        on: _str | None = ...,
        level: Level | None = ...,
        origin: Timestamp
        | Literal["epoch", "start", "start_day", "end", "end_day"] = ...,
        offset: Timedelta | _str | None = ...,
    ) -> Resampler[Series]: ...
    def first(self, offset) -> Series[S1]: ...
    def last(self, offset) -> Series[S1]: ...
    def rank(
        self,
        axis: AxisIndex = ...,
        method: Literal["average", "min", "max", "first", "dense"] = ...,
        numeric_only: _bool = ...,
        na_option: Literal["keep", "top", "bottom"] = ...,
        ascending: _bool = ...,
        pct: _bool = ...,
    ) -> Series[float]: ...
    def where(
        self,
        cond: Series[S1]
        | Series[_bool]
        | np.ndarray
        | Callable[[Series[S1]], Series[bool]]
        | Callable[[S1], bool],
        other=...,
        *,
        inplace: _bool = ...,
        axis: AxisIndex | None = ...,
        level: Level | None = ...,
        try_cast: _bool = ...,
    ) -> Series[S1]: ...
    def mask(
        self,
        cond: MaskType,
        other: Scalar | Series[S1] | DataFrame | Callable | NAType | None = ...,
        *,
        inplace: _bool = ...,
        axis: AxisIndex | None = ...,
        level: Level | None = ...,
        try_cast: _bool = ...,
    ) -> Series[S1]: ...
    def slice_shift(self, periods: int = ..., axis: AxisIndex = ...) -> Series[S1]: ...
    def tshift(
        self, periods: int = ..., freq=..., axis: AxisIndex = ...
    ) -> Series[S1]: ...
    def truncate(
        self,
        before: date | _str | int | None = ...,
        after: date | _str | int | None = ...,
        axis: AxisIndex | None = ...,
        copy: _bool = ...,
    ) -> Series[S1]: ...
    def tz_convert(
        self,
        tz,
        axis: AxisIndex = ...,
        level: Level | None = ...,
        copy: _bool = ...,
    ) -> Series[S1]: ...
    def tz_localize(
        self,
        tz,
        axis: AxisIndex = ...,
        level: Level | None = ...,
        copy: _bool = ...,
        ambiguous=...,
        nonexistent: _str = ...,
    ) -> Series[S1]: ...
    def abs(self) -> Series[S1]: ...
    def describe(
        self,
        percentiles: list[float] | None = ...,
        include: Literal["all"] | list[S1] | None = ...,
        exclude: S1 | list[S1] | None = ...,
        datetime_is_numeric: _bool | None = ...,
    ) -> Series[S1]: ...
    def pct_change(
        self,
        periods: int = ...,
        fill_method: _str = ...,
        limit: int | None = ...,
        freq=...,
        **kwargs,
    ) -> Series[S1]: ...
    def first_valid_index(self) -> Scalar: ...
    def last_valid_index(self) -> Scalar: ...
    def value_counts(
        self,
        normalize: _bool = ...,
        sort: _bool = ...,
        ascending: _bool = ...,
        bins: int | None = ...,
        dropna: _bool = ...,
    ) -> Series[int]: ...
    def transpose(self, *args, **kwargs) -> Series[S1]: ...
    @property
    def T(self) -> Self: ...
    # The rest of these were left over from the old
    # stubs we shipped in preview. They may belong in
    # the base classes in some cases; I expect stubgen
    # just failed to generate these so I couldn't match
    # them up.
    @overload
    def __add__(self, other: S1 | Self) -> Self: ...
    @overload
    def __add__(
        self, other: num | _str | Timedelta | _ListLike | Series | np.timedelta64
    ) -> Series: ...
    # ignore needed for mypy as we want different results based on the arguments
    @overload  # type: ignore[override]
    def __and__(  # type: ignore[misc]
        self, other: bool | list[bool] | list[int] | np_ndarray_bool | Series[bool]
    ) -> Series[bool]: ...
    @overload
    def __and__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: int | np_ndarray_anyint | Series[int]
    ) -> Series[int]: ...
    # def __array__(self, dtype: Optional[_bool] = ...) -> _np_ndarray
    def __div__(self, other: num | _ListLike | Series[S1]) -> Series[S1]: ...
    def __eq__(self, other: object) -> Series[_bool]: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def __floordiv__(self, other: num | _ListLike | Series[S1]) -> Series[int]: ...
    def __ge__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: S1 | _ListLike | Series[S1] | datetime | timedelta
    ) -> Series[_bool]: ...
    def __gt__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: S1 | _ListLike | Series[S1] | datetime | timedelta
    ) -> Series[_bool]: ...
    def __le__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: S1 | _ListLike | Series[S1] | datetime | timedelta
    ) -> Series[_bool]: ...
    def __lt__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: S1 | _ListLike | Series[S1] | datetime | timedelta
    ) -> Series[_bool]: ...
    @overload
    def __mul__(
        self, other: Timedelta | TimedeltaSeries | np.timedelta64
    ) -> TimedeltaSeries: ...
    @overload
    def __mul__(self, other: num | _ListLike | Series) -> Series: ...
    def __mod__(self, other: num | _ListLike | Series[S1]) -> Series[S1]: ...
    def __ne__(self, other: object) -> Series[_bool]: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def __pow__(self, other: num | _ListLike | Series[S1]) -> Series[S1]: ...
    # ignore needed for mypy as we want different results based on the arguments
    @overload  # type: ignore[override]
    def __or__(  # type: ignore[misc]
        self, other: bool | list[bool] | list[int] | np_ndarray_bool | Series[bool]
    ) -> Series[bool]: ...
    @overload
    def __or__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: int | np_ndarray_anyint | Series[int]
    ) -> Series[int]: ...
    @overload
    def __radd__(self, other: S1 | Series[S1]) -> Self: ...
    @overload
    def __radd__(self, other: num | _str | _ListLike | Series) -> Series: ...
    # ignore needed for mypy as we want different results based on the arguments
    @overload  # type: ignore[override]
    def __rand__(  # type: ignore[misc]
        self, other: bool | list[bool] | list[int] | np_ndarray_bool | Series[bool]
    ) -> Series[bool]: ...
    @overload
    def __rand__(self, other: int | np_ndarray_anyint | Series[int]) -> Series[int]: ...  # type: ignore[misc] # pyright: ignore[reportIncompatibleMethodOverride]
    def __rdiv__(self, other: num | _ListLike | Series[S1]) -> Series[S1]: ...
    def __rdivmod__(self, other: num | _ListLike | Series[S1]) -> Series[S1]: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def __rfloordiv__(self, other: num | _ListLike | Series[S1]) -> Series[S1]: ...
    def __rmod__(self, other: num | _ListLike | Series[S1]) -> Series[S1]: ...
    def __rmul__(self, other: num | _ListLike | Series) -> Series: ...
    def __rnatmul__(self, other: num | _ListLike | Series[S1]) -> Series[S1]: ...
    def __rpow__(self, other: num | _ListLike | Series[S1]) -> Series[S1]: ...
    # ignore needed for mypy as we want different results based on the arguments
    @overload  # type: ignore[override]
    def __ror__(  # type: ignore[misc]
        self, other: bool | list[bool] | list[int] | np_ndarray_bool | Series[bool]
    ) -> Series[bool]: ...
    @overload
    def __ror__(self, other: int | np_ndarray_anyint | Series[int]) -> Series[int]: ...  # type: ignore[misc] # pyright: ignore[reportIncompatibleMethodOverride]
    def __rsub__(self, other: num | _ListLike | Series[S1]) -> Series: ...
    def __rtruediv__(self, other: num | _ListLike | Series[S1]) -> Series: ...
    # ignore needed for mypy as we want different results based on the arguments
    @overload  # type: ignore[override]
    def __rxor__(  # type: ignore[misc]
        self, other: bool | list[bool] | list[int] | np_ndarray_bool | Series[bool]
    ) -> Series[bool]: ...
    @overload
    def __rxor__(self, other: int | np_ndarray_anyint | Series[int]) -> Series[int]: ...  # type: ignore[misc] # pyright: ignore[reportIncompatibleMethodOverride]
    @overload
    def __sub__(
        self: Series[Timestamp],
        other: Timedelta | TimedeltaSeries | TimedeltaIndex | np.timedelta64,
    ) -> TimestampSeries: ...
    @overload
    def __sub__(
        self: Series[Timedelta],
        other: Timedelta | TimedeltaSeries | TimedeltaIndex | np.timedelta64,
    ) -> TimedeltaSeries: ...
    @overload
    def __sub__(
        self, other: Timestamp | datetime | TimestampSeries
    ) -> TimedeltaSeries: ...
    @overload
    def __sub__(self, other: num | _ListLike | Series) -> Series: ...
    def __truediv__(self, other: num | _ListLike | Series[S1]) -> Series: ...
    # ignore needed for mypy as we want different results based on the arguments
    @overload  # type: ignore[override]
    def __xor__(  # type: ignore[misc]
        self, other: bool | list[bool] | list[int] | np_ndarray_bool | Series[bool]
    ) -> Series[bool]: ...
    @overload
    def __xor__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: int | np_ndarray_anyint | Series[int]
    ) -> Series[int]: ...
    def __invert__(self) -> Series[bool]: ...
    # properties
    # @property
    # def array(self) -> _npndarray
    @property
    def at(self) -> _AtIndexer: ...
    @property
    def cat(self) -> CategoricalAccessor: ...
    @property
    def iat(self) -> _iAtIndexer: ...
    @property
    def iloc(self) -> _iLocIndexerSeries[S1]: ...
    @property
    def loc(self) -> _LocIndexerSeries[S1]: ...
    # Methods
    def add(
        self,
        other: Series[S1] | Scalar,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: int = ...,
    ) -> Series[S1]: ...
    def all(
        self,
        axis: AxisIndex = ...,
        bool_only: _bool | None = ...,
        skipna: _bool = ...,
        **kwargs,
    ) -> _bool: ...
    def any(
        self,
        *,
        axis: AxisIndex = ...,
        bool_only: _bool | None = ...,
        skipna: _bool = ...,
        **kwargs,
    ) -> _bool: ...
    def cummax(
        self, axis: AxisIndex | None = ..., skipna: _bool = ..., *args, **kwargs
    ) -> Series[S1]: ...
    def cummin(
        self, axis: AxisIndex | None = ..., skipna: _bool = ..., *args, **kwargs
    ) -> Series[S1]: ...
    def cumprod(
        self, axis: AxisIndex | None = ..., skipna: _bool = ..., *args, **kwargs
    ) -> Series[S1]: ...
    def cumsum(
        self, axis: AxisIndex | None = ..., skipna: _bool = ..., *args, **kwargs
    ) -> Series[S1]: ...
    def divide(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[float]: ...
    def divmod(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    def eq(
        self,
        other: Scalar | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[_bool]: ...
    def ewm(
        self,
        com: float | None = ...,
        span: float | None = ...,
        halflife: float | None = ...,
        alpha: float | None = ...,
        min_periods: int = ...,
        adjust: _bool = ...,
        ignore_na: _bool = ...,
    ) -> ExponentialMovingWindow[Series]: ...
    def expanding(
        self,
        min_periods: int = ...,
        method: CalculationMethod = ...,
    ) -> Expanding[Series]: ...
    def floordiv(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex | None = ...,
    ) -> Series[int]: ...
    def ge(
        self,
        other: Scalar | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[_bool]: ...
    def gt(
        self,
        other: Scalar | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[_bool]: ...
    def item(self) -> S1: ...
    def kurt(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Scalar: ...
    def kurtosis(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Scalar: ...
    def le(
        self,
        other: Scalar | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[_bool]: ...
    def lt(
        self,
        other: Scalar | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[_bool]: ...
    def max(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> S1: ...
    def mean(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> float: ...
    def median(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> float: ...
    def min(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> S1: ...
    def mod(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex | None = ...,
    ) -> Series[S1]: ...
    def mul(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex | None = ...,
    ) -> Series[S1]: ...
    def multiply(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex | None = ...,
    ) -> Series[S1]: ...
    def ne(
        self,
        other: Scalar | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[_bool]: ...
    def nunique(self, dropna: _bool = ...) -> int: ...
    def pow(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex | None = ...,
    ) -> Series[S1]: ...
    def prod(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        min_count: int = ...,
        **kwargs,
    ) -> Scalar: ...
    def product(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        min_count: int = ...,
        **kwargs,
    ) -> Scalar: ...
    def radd(
        self,
        other: Series[S1] | Scalar,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    def rdivmod(
        self,
        other: Series[S1] | Scalar,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    def rfloordiv(
        self,
        other,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    def rmod(
        self,
        other: Series[S1] | Scalar,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    def rmul(
        self,
        other: Series[S1] | Scalar,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    @overload
    def rolling(
        self,
        window: int | _str | timedelta | BaseOffset | BaseIndexer,
        min_periods: int | None = ...,
        center: _bool = ...,
        on: _str | None = ...,
        closed: IntervalClosedType | None = ...,
        step: int | None = ...,
        method: CalculationMethod = ...,
        *,
        win_type: _str,
    ) -> Window[Series]: ...
    @overload
    def rolling(
        self,
        window: int | _str | timedelta | BaseOffset | BaseIndexer,
        min_periods: int | None = ...,
        center: _bool = ...,
        on: _str | None = ...,
        closed: IntervalClosedType | None = ...,
        step: int | None = ...,
        method: CalculationMethod = ...,
        *,
        win_type: None = ...,
    ) -> Rolling[Series]: ...
    def rpow(
        self,
        other: Series[S1] | Scalar,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    def rsub(
        self,
        other: Series[S1] | Scalar,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    def rtruediv(
        self,
        other,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[S1]: ...
    def sem(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        ddof: int = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Scalar: ...
    def skew(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Scalar: ...
    def std(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        ddof: int = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> float: ...
    def sub(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex | None = ...,
    ) -> Series[S1]: ...
    def subtract(
        self,
        other: num | _ListLike | Series[S1],
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex | None = ...,
    ) -> Series[S1]: ...
    # ignore needed because of mypy, for using `Never` as type-var.
    @overload
    def sum(
        self: Series[Never],
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        min_count: int = ...,
        **kwargs,
    ) -> Any: ...
    # ignore needed because of mypy, for overlapping overloads
    # between `Series[bool]` and `Series[int]`.
    @overload
    def sum(  # type: ignore[misc]
        self: Series[bool],
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        min_count: int = ...,
        **kwargs,
    ) -> int: ...
    @overload
    def sum(
        self: Series[S1],
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        min_count: int = ...,
        **kwargs,
    ) -> S1: ...
    def to_list(self) -> list[S1]: ...
    def to_numpy(
        self,
        dtype: npt.DTypeLike | None = ...,
        copy: bool = ...,
        na_value: Scalar = ...,
        **kwargs,
    ) -> np.ndarray: ...
    def tolist(self) -> list[S1]: ...
    def truediv(
        self,
        other,
        level: Level | None = ...,
        fill_value: float | None = ...,
        axis: AxisIndex = ...,
    ) -> Series[float]: ...
    def var(
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        ddof: int = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Scalar: ...
    @overload
    def rename_axis(
        self,
        mapper: Scalar | ListLike = ...,
        index: Scalar | ListLike | Callable | dict | None = ...,
        columns: Scalar | ListLike | Callable | dict | None = ...,
        axis: AxisIndex | None = ...,
        copy: _bool = ...,
        *,
        inplace: Literal[True],
    ) -> None: ...
    @overload
    def rename_axis(
        self,
        mapper: Scalar | ListLike = ...,
        index: Scalar | ListLike | Callable | dict | None = ...,
        columns: Scalar | ListLike | Callable | dict | None = ...,
        axis: AxisIndex | None = ...,
        copy: _bool = ...,
        inplace: Literal[False] = ...,
    ) -> Self: ...
    def set_axis(self, labels, *, axis: Axis = ..., copy: _bool = ...) -> Self: ...
    def __iter__(self) -> Iterator[S1]: ...
    def xs(
        self,
        key: Hashable,
        axis: AxisIndex = ...,
        level: Level | None = ...,
        drop_level: _bool = ...,
    ) -> Self: ...

class TimestampSeries(Series[Timestamp]):
    @property
    def dt(self) -> TimestampProperties: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def __add__(self, other: TimedeltaSeries | np.timedelta64 | timedelta) -> TimestampSeries: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def __radd__(self, other: TimedeltaSeries | np.timedelta64 | timedelta) -> TimestampSeries: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    @overload  # type: ignore[override]
    def __sub__(
        self, other: Timestamp | datetime | TimestampSeries
    ) -> TimedeltaSeries: ...
    @overload
    def __sub__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: timedelta | TimedeltaSeries | TimedeltaIndex | np.timedelta64,
    ) -> TimestampSeries: ...
    def __mul__(self, other: float | Series[int] | Series[float] | Sequence[float]) -> TimestampSeries: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def __truediv__(self, other: float | Series[int] | Series[float] | Sequence[float]) -> TimestampSeries: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def mean(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Timestamp: ...
    def median(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Timestamp: ...
    def std(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        ddof: int = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Timedelta: ...

class TimedeltaSeries(Series[Timedelta]):
    # ignores needed because of mypy
    @overload  # type: ignore[override]
    def __add__(self, other: Period) -> PeriodSeries: ...
    @overload
    def __add__(
        self, other: Timestamp | TimestampSeries | DatetimeIndex
    ) -> TimestampSeries: ...
    @overload
    def __add__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Timedelta | np.timedelta64
    ) -> TimedeltaSeries: ...
    def __radd__(self, other: Timestamp | TimestampSeries) -> TimestampSeries: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def __mul__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: num | Sequence[num] | Series[int] | Series[float]
    ) -> TimedeltaSeries: ...
    def __sub__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: Timedelta | TimedeltaSeries | TimedeltaIndex | np.timedelta64
    ) -> TimedeltaSeries: ...
    @overload  # type: ignore[override]
    def __truediv__(self, other: float | Sequence[float]) -> Self: ...
    @overload
    def __truediv__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: timedelta
        | TimedeltaSeries
        | np.timedelta64
        | TimedeltaIndex
        | Sequence[timedelta],
    ) -> Series[float]: ...
    def __rtruediv__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: timedelta
        | TimedeltaSeries
        | np.timedelta64
        | TimedeltaIndex
        | Sequence[timedelta],
    ) -> Series[float]: ...
    @overload  # type: ignore[override]
    def __floordiv__(self, other: float | Sequence[float]) -> Self: ...
    @overload
    def __floordiv__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: timedelta
        | TimedeltaSeries
        | np.timedelta64
        | TimedeltaIndex
        | Sequence[timedelta],
    ) -> Series[int]: ...
    def __rfloordiv__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: timedelta
        | TimedeltaSeries
        | np.timedelta64
        | TimedeltaIndex
        | Sequence[timedelta],
    ) -> Series[int]: ...
    @property
    def dt(self) -> TimedeltaProperties: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def mean(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Timedelta: ...
    def median(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool = ...,
        level: None = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Timedelta: ...
    def std(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        axis: AxisIndex | None = ...,
        skipna: _bool | None = ...,
        level: None = ...,
        ddof: int = ...,
        numeric_only: _bool = ...,
        **kwargs,
    ) -> Timedelta: ...

class PeriodSeries(Series[Period]):
    @property
    def dt(self) -> PeriodProperties: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
    def __sub__(self, other: PeriodSeries) -> OffsetSeries: ...  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]

class OffsetSeries(Series):
    @overload  # type: ignore[override]
    def __radd__(self, other: Period) -> PeriodSeries: ...
    @overload
    def __radd__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, other: BaseOffset
    ) -> OffsetSeries: ...

class IntervalSeries(Series[Interval[_OrderableT]], Generic[_OrderableT]):
    @property
    def array(self) -> IntervalArray: ...
