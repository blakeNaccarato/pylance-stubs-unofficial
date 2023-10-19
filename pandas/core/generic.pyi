from collections.abc import (
    Callable,
    Hashable,
    Iterable,
    Mapping,
    Sequence,
)
import sqlite3
from typing import (
    Any,
    ClassVar,
    Literal,
    final,
    overload,
)

import numpy as np
from pandas import Index
import pandas.core.indexing as indexing
from pandas.core.series import Series
import sqlalchemy.engine
from typing_extensions import Self

from pandas._typing import (
    S1,
    ArrayLike,
    Axis,
    AxisIndex,
    CompressionOptions,
    CSVQuoting,
    Dtype,
    DtypeArg,
    DtypeBackend,
    FilePath,
    FileWriteMode,
    FillnaOptions,
    HashableT1,
    HashableT2,
    HDFCompLib,
    IgnoreRaise,
    IndexLabel,
    Level,
    ReplaceMethod,
    SortKind,
    StorageOptions,
    T,
    WriteBuffer,
)

from pandas.io.pytables import HDFStore
from pandas.io.sql import SQLTable

_bool = bool
_str = str

class NDFrame(indexing.IndexingMixin):
    __hash__: ClassVar[None]  # type: ignore[assignment]

    def set_flags(
        self,
        *,
        copy: bool = ...,
        allows_duplicate_labels: bool | None = ...,
    ) -> Self: ...
    @property
    def attrs(self) -> dict[Hashable | None, Any]: ...
    @attrs.setter
    def attrs(self, value: Mapping[Hashable | None, Any]) -> None: ...
    @property
    def shape(self) -> tuple[int, ...]: ...
    @property
    def axes(self) -> list[Index]: ...
    @property
    def ndim(self) -> int: ...
    @property
    def size(self) -> int: ...
    def droplevel(self, level: Level, axis: AxisIndex = ...) -> Self: ...
    def squeeze(self, axis=...): ...
    def equals(self, other: Series[S1]) -> _bool: ...
    def __neg__(self) -> Self: ...
    def __pos__(self) -> Self: ...
    def __nonzero__(self) -> None: ...
    @final
    def bool(self) -> _bool: ...
    def __abs__(self) -> Self: ...
    def __round__(self, decimals: int = ...) -> Self: ...
    def keys(self): ...
    def __len__(self) -> int: ...
    def __contains__(self, key) -> _bool: ...
    @property
    def empty(self) -> _bool: ...
    __array_priority__: int = ...
    def __array__(self, dtype=...) -> np.ndarray: ...
    def to_excel(
        self,
        excel_writer,
        sheet_name: _str = ...,
        na_rep: _str = ...,
        float_format: _str | None = ...,
        columns: _str | Sequence[_str] | None = ...,
        header: _bool | list[_str] = ...,
        index: _bool = ...,
        index_label: _str | Sequence[_str] | None = ...,
        startrow: int = ...,
        startcol: int = ...,
        engine: _str | None = ...,
        merge_cells: _bool = ...,
        inf_rep: _str = ...,
        freeze_panes: tuple[int, int] | None = ...,
    ) -> None: ...
    def to_hdf(
        self,
        path_or_buf: FilePath | HDFStore,
        key: _str,
        mode: Literal["a", "w", "r+"] = ...,
        complevel: int | None = ...,
        complib: HDFCompLib | None = ...,
        append: _bool = ...,
        format: Literal["t", "table", "f", "fixed"] | None = ...,
        index: _bool = ...,
        min_itemsize: int | dict[HashableT1, int] | None = ...,
        nan_rep: _str | None = ...,
        dropna: _bool | None = ...,
        data_columns: Literal[True] | list[HashableT2] | None = ...,
        errors: Literal[
            "strict",
            "ignore",
            "replace",
            "surrogateescape",
            "xmlcharrefreplace",
            "backslashreplace",
            "namereplace",
        ] = ...,
        encoding: _str = ...,
    ) -> None: ...
    @overload
    def to_markdown(
        self,
        buf: FilePath | WriteBuffer[str],
        mode: FileWriteMode | None = ...,
        index: _bool = ...,
        storage_options: StorageOptions = ...,
        **kwargs: Any,
    ) -> None: ...
    @overload
    def to_markdown(
        self,
        buf: None = ...,
        mode: FileWriteMode | None = ...,
        index: _bool = ...,
        storage_options: StorageOptions = ...,
        **kwargs: Any,
    ) -> _str: ...
    def to_sql(
        self,
        name: _str,
        con: str | sqlalchemy.engine.Connectable | sqlite3.Connection,
        schema: _str | None = ...,
        if_exists: Literal["fail", "replace", "append"] = ...,
        index: _bool = ...,
        index_label: IndexLabel = ...,
        chunksize: int | None = ...,
        dtype: DtypeArg | None = ...,
        method: Literal["multi"]
        | Callable[
            [SQLTable, Any, list[str], Iterable[tuple[Any, ...]]],
            int | None,
        ]
        | None = ...,
    ) -> int | None: ...
    def to_pickle(
        self,
        path: FilePath | WriteBuffer[bytes],
        compression: CompressionOptions = ...,
        protocol: int = ...,
        storage_options: StorageOptions = ...,
    ) -> None: ...
    def to_clipboard(
        self, excel: _bool = ..., sep: _str | None = ..., **kwargs
    ) -> None: ...
    @overload
    def to_latex(
        self,
        buf: FilePath | WriteBuffer[str],
        columns: list[_str] | None = ...,
        col_space: int | None = ...,
        header: _bool | list[_str] = ...,
        index: _bool = ...,
        na_rep: _str = ...,
        formatters=...,
        float_format=...,
        sparsify: _bool | None = ...,
        index_names: _bool = ...,
        bold_rows: _bool = ...,
        column_format: _str | None = ...,
        longtable: _bool | None = ...,
        escape: _bool | None = ...,
        encoding: _str | None = ...,
        decimal: _str = ...,
        multicolumn: _bool | None = ...,
        multicolumn_format: _str | None = ...,
        multirow: _bool | None = ...,
        caption: _str | tuple[_str, _str] | None = ...,
        label: _str | None = ...,
        position: _str | None = ...,
    ) -> None: ...
    @overload
    def to_latex(
        self,
        buf: None = ...,
        columns: list[_str] | None = ...,
        col_space: int | None = ...,
        header: _bool | list[_str] = ...,
        index: _bool = ...,
        na_rep: _str = ...,
        formatters=...,
        float_format=...,
        sparsify: _bool | None = ...,
        index_names: _bool = ...,
        bold_rows: _bool = ...,
        column_format: _str | None = ...,
        longtable: _bool | None = ...,
        escape: _bool | None = ...,
        encoding: _str | None = ...,
        decimal: _str = ...,
        multicolumn: _bool | None = ...,
        multicolumn_format: _str | None = ...,
        multirow: _bool | None = ...,
        caption: _str | tuple[_str, _str] | None = ...,
        label: _str | None = ...,
        position: _str | None = ...,
    ) -> _str: ...
    @overload
    def to_csv(
        self,
        path_or_buf: FilePath | WriteBuffer[bytes] | WriteBuffer[str],
        sep: _str = ...,
        na_rep: _str = ...,
        float_format: _str | Callable[[object], _str] | None = ...,
        columns: list[HashableT1] | None = ...,
        header: _bool | list[_str] = ...,
        index: _bool = ...,
        index_label: Literal[False] | _str | list[HashableT2] | None = ...,
        mode: FileWriteMode = ...,
        encoding: _str | None = ...,
        compression: CompressionOptions = ...,
        quoting: CSVQuoting = ...,
        quotechar: _str = ...,
        lineterminator: _str | None = ...,
        chunksize: int | None = ...,
        date_format: _str | None = ...,
        doublequote: _bool = ...,
        escapechar: _str | None = ...,
        decimal: _str = ...,
        errors: _str = ...,
        storage_options: StorageOptions = ...,
    ) -> None: ...
    @overload
    def to_csv(
        self,
        path_or_buf: None = ...,
        sep: _str = ...,
        na_rep: _str = ...,
        float_format: _str | Callable[[object], _str] | None = ...,
        columns: list[HashableT1] | None = ...,
        header: _bool | list[_str] = ...,
        index: _bool = ...,
        index_label: Literal[False] | _str | list[HashableT2] | None = ...,
        mode: FileWriteMode = ...,
        encoding: _str | None = ...,
        compression: CompressionOptions = ...,
        quoting: CSVQuoting = ...,
        quotechar: _str = ...,
        lineterminator: _str | None = ...,
        chunksize: int | None = ...,
        date_format: _str | None = ...,
        doublequote: _bool = ...,
        escapechar: _str | None = ...,
        decimal: _str = ...,
        errors: _str = ...,
        storage_options: StorageOptions = ...,
    ) -> _str: ...
    def take(
        self, indices, axis=..., is_copy: _bool | None = ..., **kwargs
    ) -> Self:
        """
Return the elements in the given *positional* indices along an axis.

This means that we are not indexing according to actual values in
the index attribute of the object. We are indexing according to the
actual position of the element in the object.

Parameters
----------
indices : array-like
    An array of ints indicating which positions to take.
axis : {0 or 'index', 1 or 'columns', None}, default 0
    The axis on which to select elements. ``0`` means that we are
    selecting rows, ``1`` means that we are selecting columns.
    For `Series` this parameter is unused and defaults to 0.
**kwargs
    For compatibility with :meth:`numpy.take`. Has no effect on the
    output.

Returns
-------
same type as caller
    An array-like containing the elements taken from the object.

See Also
--------
DataFrame.loc : Select a subset of a DataFrame by labels.
DataFrame.iloc : Select a subset of a DataFrame by positions.
numpy.take : Take elements from an array along an axis.

Examples
--------
>>> df = pd.DataFrame([('falcon', 'bird', 389.0),
...                    ('parrot', 'bird', 24.0),
...                    ('lion', 'mammal', 80.5),
...                    ('monkey', 'mammal', np.nan)],
...                   columns=['name', 'class', 'max_speed'],
...                   index=[0, 2, 3, 1])
>>> df
     name   class  max_speed
0  falcon    bird      389.0
2  parrot    bird       24.0
3    lion  mammal       80.5
1  monkey  mammal        NaN

Take elements at positions 0 and 3 along the axis 0 (default).

Note how the actual indices selected (0 and 1) do not correspond to
our selected indices 0 and 3. That's because we are selecting the 0th
and 3rd rows, not rows whose indices equal 0 and 3.

>>> df.take([0, 3])
     name   class  max_speed
0  falcon    bird      389.0
1  monkey  mammal        NaN

Take elements at indices 1 and 2 along the axis 1 (column selection).

>>> df.take([1, 2], axis=1)
    class  max_speed
0    bird      389.0
2    bird       24.0
3  mammal       80.5
1  mammal        NaN

We may take elements using negative integers for positive indices,
starting from the end of the object, just like with Python lists.

>>> df.take([-1, -2])
     name   class  max_speed
1  monkey  mammal        NaN
3    lion  mammal       80.5
        """
        pass
    def __delitem__(self, idx: Hashable) -> None: ...
    def get(self, key: object, default: Dtype | None = ...) -> Dtype: ...
    def reindex_like(
        self,
        other,
        method: _str | None = ...,
        copy: _bool = ...,
        limit=...,
        tolerance=...,
    ) -> Self: ...
    @overload
    def drop(
        self,
        labels: Hashable | Sequence[Hashable] = ...,
        *,
        axis: Axis = ...,
        index: Hashable | Sequence[Hashable] = ...,
        columns: Hashable | Sequence[Hashable] = ...,
        level: Level | None = ...,
        inplace: Literal[True],
        errors: IgnoreRaise = ...,
    ) -> None: ...
    @overload
    def drop(
        self,
        labels: Hashable | Sequence[Hashable] = ...,
        *,
        axis: Axis = ...,
        index: Hashable | Sequence[Hashable] = ...,
        columns: Hashable | Sequence[Hashable] = ...,
        level: Level | None = ...,
        inplace: Literal[False] = ...,
        errors: IgnoreRaise = ...,
    ) -> Self: ...
    @overload
    def drop(
        self,
        labels: Hashable | Sequence[Hashable] = ...,
        *,
        axis: Axis = ...,
        index: Hashable | Sequence[Hashable] = ...,
        columns: Hashable | Sequence[Hashable] = ...,
        level: Level | None = ...,
        inplace: _bool = ...,
        errors: IgnoreRaise = ...,
    ) -> Self | None: ...
    def add_prefix(self, prefix: _str) -> Self: ...
    def add_suffix(self, suffix: _str) -> Self: ...
    def sort_index(
        self,
        *,
        axis: Axis = ...,
        level=...,
        ascending: _bool = ...,
        inplace: _bool = ...,
        kind: SortKind = ...,
        na_position: Literal["first", "last"] = ...,
        sort_remaining: _bool = ...,
        ignore_index: _bool = ...,
    ): ...
    def filter(
        self,
        items=...,
        like: _str | None = ...,
        regex: _str | None = ...,
        axis=...,
    ) -> Self: ...
    def head(self, n: int = ...) -> Self: ...
    def tail(self, n: int = ...) -> Self: ...
    def pipe(
        self, func: Callable[..., T] | tuple[Callable[..., T], str], *args, **kwargs
    ) -> T: ...
    def __finalize__(self, other, method=..., **kwargs) -> Self: ...
    def __setattr__(self, name: _str, value) -> None: ...
    @property
    def values(self) -> ArrayLike: ...
    @property
    def dtypes(self): ...
    def copy(self, deep: _bool = ...) -> Self: ...
    def __copy__(self, deep: _bool = ...) -> Self: ...
    def __deepcopy__(self, memo=...) -> Self: ...
    def infer_objects(self) -> Self: ...
    def convert_dtypes(
        self,
        infer_objects: _bool = ...,
        convert_string: _bool = ...,
        convert_integer: _bool = ...,
        convert_boolean: _bool = ...,
        dtype_backend: DtypeBackend = ...,
    ) -> Self: ...
    def fillna(
        self,
        value=...,
        *,
        method=...,
        axis=...,
        inplace: _bool = ...,
        limit=...,
        downcast=...,
    ) -> NDFrame | None:
        """
Fill NA/NaN values using the specified method.

Parameters
----------
value : scalar, dict, Series, or DataFrame
    Value to use to fill holes (e.g. 0), alternately a
    dict/Series/DataFrame of values specifying which value to use for
    each index (for a Series) or column (for a DataFrame).  Values not
    in the dict/Series/DataFrame will not be filled. This value cannot
    be a list.
method : {'backfill', 'bfill', 'ffill', None}, default None
    Method to use for filling holes in reindexed Series:

    * ffill: propagate last valid observation forward to next valid.
    * backfill / bfill: use next valid observation to fill gap.

    .. deprecated:: 2.1.0
        Use ffill or bfill instead.

axis : {0 or 'index'} for Series, {0 or 'index', 1 or 'columns'} for DataFrame
    Axis along which to fill missing values. For `Series`
    this parameter is unused and defaults to 0.
inplace : bool, default False
    If True, fill in-place. Note: this will modify any
    other views on this object (e.g., a no-copy slice for a column in a
    DataFrame).
limit : int, default None
    If method is specified, this is the maximum number of consecutive
    NaN values to forward/backward fill. In other words, if there is
    a gap with more than this number of consecutive NaNs, it will only
    be partially filled. If method is not specified, this is the
    maximum number of entries along the entire axis where NaNs will be
    filled. Must be greater than 0 if not None.
downcast : dict, default is None
    A dict of item->dtype of what to downcast if possible,
    or the string 'infer' which will try to downcast to an appropriate
    equal type (e.g. float64 to int64 if possible).

Returns
-------
Series/DataFrame or None
    Object with missing values filled or None if ``inplace=True``.

See Also
--------
ffill : Fill values by propagating the last valid observation to next valid.
bfill : Fill values by using the next valid observation to fill the gap.
interpolate : Fill NaN values using interpolation.
reindex : Conform object to new index.
asfreq : Convert TimeSeries to specified frequency.

Examples
--------
>>> df = pd.DataFrame([[np.nan, 2, np.nan, 0],
...                    [3, 4, np.nan, 1],
...                    [np.nan, np.nan, np.nan, np.nan],
...                    [np.nan, 3, np.nan, 4]],
...                   columns=list("ABCD"))
>>> df
     A    B   C    D
0  NaN  2.0 NaN  0.0
1  3.0  4.0 NaN  1.0
2  NaN  NaN NaN  NaN
3  NaN  3.0 NaN  4.0

Replace all NaN elements with 0s.

>>> df.fillna(0)
     A    B    C    D
0  0.0  2.0  0.0  0.0
1  3.0  4.0  0.0  1.0
2  0.0  0.0  0.0  0.0
3  0.0  3.0  0.0  4.0

Replace all NaN elements in column 'A', 'B', 'C', and 'D', with 0, 1,
2, and 3 respectively.

>>> values = {"A": 0, "B": 1, "C": 2, "D": 3}
>>> df.fillna(value=values)
     A    B    C    D
0  0.0  2.0  2.0  0.0
1  3.0  4.0  2.0  1.0
2  0.0  1.0  2.0  3.0
3  0.0  3.0  2.0  4.0

Only replace the first NaN element.

>>> df.fillna(value=values, limit=1)
     A    B    C    D
0  0.0  2.0  2.0  0.0
1  3.0  4.0  NaN  1.0
2  NaN  1.0  NaN  3.0
3  NaN  3.0  NaN  4.0

When filling using a DataFrame, replacement happens along
the same column names and same indices

>>> df2 = pd.DataFrame(np.zeros((4, 4)), columns=list("ABCE"))
>>> df.fillna(df2)
     A    B    C    D
0  0.0  2.0  0.0  0.0
1  3.0  4.0  0.0  1.0
2  0.0  0.0  0.0  NaN
3  0.0  3.0  0.0  4.0

Note that column D is not affected since it is not present in df2.
        """
        pass
    def replace(
        self,
        to_replace=...,
        value=...,
        *,
        inplace: _bool = ...,
        limit=...,
        regex: _bool = ...,
        method: ReplaceMethod = ...,
    ):
        """
Replace values given in `to_replace` with `value`.

Values of the Series/DataFrame are replaced with other values dynamically.
This differs from updating with ``.loc`` or ``.iloc``, which require
you to specify a location to update with some value.

Parameters
----------
to_replace : str, regex, list, dict, Series, int, float, or None
    How to find the values that will be replaced.

    * numeric, str or regex:

        - numeric: numeric values equal to `to_replace` will be
          replaced with `value`
        - str: string exactly matching `to_replace` will be replaced
          with `value`
        - regex: regexs matching `to_replace` will be replaced with
          `value`

    * list of str, regex, or numeric:

        - First, if `to_replace` and `value` are both lists, they
          **must** be the same length.
        - Second, if ``regex=True`` then all of the strings in **both**
          lists will be interpreted as regexs otherwise they will match
          directly. This doesn't matter much for `value` since there
          are only a few possible substitution regexes you can use.
        - str, regex and numeric rules apply as above.

    * dict:

        - Dicts can be used to specify different replacement values
          for different existing values. For example,
          ``{'a': 'b', 'y': 'z'}`` replaces the value 'a' with 'b' and
          'y' with 'z'. To use a dict in this way, the optional `value`
          parameter should not be given.
        - For a DataFrame a dict can specify that different values
          should be replaced in different columns. For example,
          ``{'a': 1, 'b': 'z'}`` looks for the value 1 in column 'a'
          and the value 'z' in column 'b' and replaces these values
          with whatever is specified in `value`. The `value` parameter
          should not be ``None`` in this case. You can treat this as a
          special case of passing two lists except that you are
          specifying the column to search in.
        - For a DataFrame nested dictionaries, e.g.,
          ``{'a': {'b': np.nan}}``, are read as follows: look in column
          'a' for the value 'b' and replace it with NaN. The optional `value`
          parameter should not be specified to use a nested dict in this
          way. You can nest regular expressions as well. Note that
          column names (the top-level dictionary keys in a nested
          dictionary) **cannot** be regular expressions.

    * None:

        - This means that the `regex` argument must be a string,
          compiled regular expression, or list, dict, ndarray or
          Series of such elements. If `value` is also ``None`` then
          this **must** be a nested dictionary or Series.

    See the examples section for examples of each of these.
value : scalar, dict, list, str, regex, default None
    Value to replace any values matching `to_replace` with.
    For a DataFrame a dict of values can be used to specify which
    value to use for each column (columns not in the dict will not be
    filled). Regular expressions, strings and lists or dicts of such
    objects are also allowed.

inplace : bool, default False
    If True, performs operation inplace and returns None.
limit : int, default None
    Maximum size gap to forward or backward fill.

    .. deprecated:: 2.1.0
regex : bool or same types as `to_replace`, default False
    Whether to interpret `to_replace` and/or `value` as regular
    expressions. If this is ``True`` then `to_replace` *must* be a
    string. Alternatively, this could be a regular expression or a
    list, dict, or array of regular expressions in which case
    `to_replace` must be ``None``.
method : {'pad', 'ffill', 'bfill'}
    The method to use when for replacement, when `to_replace` is a
    scalar, list or tuple and `value` is ``None``.

    .. deprecated:: 2.1.0

Returns
-------
Series/DataFrame
    Object after replacement.

Raises
------
AssertionError
    * If `regex` is not a ``bool`` and `to_replace` is not
      ``None``.

TypeError
    * If `to_replace` is not a scalar, array-like, ``dict``, or ``None``
    * If `to_replace` is a ``dict`` and `value` is not a ``list``,
      ``dict``, ``ndarray``, or ``Series``
    * If `to_replace` is ``None`` and `regex` is not compilable
      into a regular expression or is a list, dict, ndarray, or
      Series.
    * When replacing multiple ``bool`` or ``datetime64`` objects and
      the arguments to `to_replace` does not match the type of the
      value being replaced

ValueError
    * If a ``list`` or an ``ndarray`` is passed to `to_replace` and
      `value` but they are not the same length.

See Also
--------
Series.fillna : Fill NA values.
DataFrame.fillna : Fill NA values.
Series.where : Replace values based on boolean condition.
DataFrame.where : Replace values based on boolean condition.
DataFrame.map: Apply a function to a Dataframe elementwise.
Series.map: Map values of Series according to an input mapping or function.
Series.str.replace : Simple string replacement.

Notes
-----
* Regex substitution is performed under the hood with ``re.sub``. The
  rules for substitution for ``re.sub`` are the same.
* Regular expressions will only substitute on strings, meaning you
  cannot provide, for example, a regular expression matching floating
  point numbers and expect the columns in your frame that have a
  numeric dtype to be matched. However, if those floating point
  numbers *are* strings, then you can do this.
* This method has *a lot* of options. You are encouraged to experiment
  and play with this method to gain intuition about how it works.
* When dict is used as the `to_replace` value, it is like
  key(s) in the dict are the to_replace part and
  value(s) in the dict are the value parameter.

Examples
--------

**Scalar `to_replace` and `value`**

>>> s = pd.Series([1, 2, 3, 4, 5])
>>> s.replace(1, 5)
0    5
1    2
2    3
3    4
4    5
dtype: int64

>>> df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
...                    'B': [5, 6, 7, 8, 9],
...                    'C': ['a', 'b', 'c', 'd', 'e']})
>>> df.replace(0, 5)
    A  B  C
0  5  5  a
1  1  6  b
2  2  7  c
3  3  8  d
4  4  9  e

**List-like `to_replace`**

>>> df.replace([0, 1, 2, 3], 4)
    A  B  C
0  4  5  a
1  4  6  b
2  4  7  c
3  4  8  d
4  4  9  e

>>> df.replace([0, 1, 2, 3], [4, 3, 2, 1])
    A  B  C
0  4  5  a
1  3  6  b
2  2  7  c
3  1  8  d
4  4  9  e

>>> s.replace([1, 2], method='bfill')
0    3
1    3
2    3
3    4
4    5
dtype: int64

**dict-like `to_replace`**

>>> df.replace({0: 10, 1: 100})
        A  B  C
0   10  5  a
1  100  6  b
2    2  7  c
3    3  8  d
4    4  9  e

>>> df.replace({'A': 0, 'B': 5}, 100)
        A    B  C
0  100  100  a
1    1    6  b
2    2    7  c
3    3    8  d
4    4    9  e

>>> df.replace({'A': {0: 100, 4: 400}})
        A  B  C
0  100  5  a
1    1  6  b
2    2  7  c
3    3  8  d
4  400  9  e

**Regular expression `to_replace`**

>>> df = pd.DataFrame({'A': ['bat', 'foo', 'bait'],
...                    'B': ['abc', 'bar', 'xyz']})
>>> df.replace(to_replace=r'^ba.$', value='new', regex=True)
        A    B
0   new  abc
1   foo  new
2  bait  xyz

>>> df.replace({'A': r'^ba.$'}, {'A': 'new'}, regex=True)
        A    B
0   new  abc
1   foo  bar
2  bait  xyz

>>> df.replace(regex=r'^ba.$', value='new')
        A    B
0   new  abc
1   foo  new
2  bait  xyz

>>> df.replace(regex={r'^ba.$': 'new', 'foo': 'xyz'})
        A    B
0   new  abc
1   xyz  new
2  bait  xyz

>>> df.replace(regex=[r'^ba.$', 'foo'], value='new')
        A    B
0   new  abc
1   new  new
2  bait  xyz

Compare the behavior of ``s.replace({'a': None})`` and
``s.replace('a', None)`` to understand the peculiarities
of the `to_replace` parameter:

>>> s = pd.Series([10, 'a', 'a', 'b', 'a'])

When one uses a dict as the `to_replace` value, it is like the
value(s) in the dict are equal to the `value` parameter.
``s.replace({'a': None})`` is equivalent to
``s.replace(to_replace={'a': None}, value=None, method=None)``:

>>> s.replace({'a': None})
0      10
1    None
2    None
3       b
4    None
dtype: object

When ``value`` is not explicitly passed and `to_replace` is a scalar, list
or tuple, `replace` uses the method parameter (default 'pad') to do the
replacement. So this is why the 'a' values are being replaced by 10
in rows 1 and 2 and 'b' in row 4 in this case.

>>> s.replace('a')
0    10
1    10
2    10
3     b
4     b
dtype: object

    .. deprecated:: 2.1.0
        The 'method' parameter and padding behavior are deprecated.

On the other hand, if ``None`` is explicitly passed for ``value``, it will
be respected:

>>> s.replace('a', None)
0      10
1    None
2    None
3       b
4    None
dtype: object

    .. versionchanged:: 1.4.0
        Previously the explicit ``None`` was silently ignored.
        """
        pass
    def asof(self, where, subset=...): ...
    def isna(self) -> NDFrame: ...
    def isnull(self) -> NDFrame: ...
    def notna(self) -> NDFrame: ...
    def notnull(self) -> NDFrame: ...
    def clip(
        self, lower=..., upper=..., *, axis=..., inplace: _bool = ..., **kwargs
    ) -> Self: ...
    def asfreq(
        self,
        freq,
        method: FillnaOptions | None = ...,
        how: Literal["start", "end"] | None = ...,
        normalize: _bool = ...,
        fill_value=...,
    ) -> Self: ...
    def at_time(self, time, asof: _bool = ..., axis=...) -> Self: ...
    def between_time(
        self,
        start_time,
        end_time,
        axis=...,
    ) -> Self: ...
    def first(self, offset) -> Self: ...
    def last(self, offset) -> Self: ...
    def rank(
        self,
        axis=...,
        method: Literal["average", "min", "max", "first", "dense"] = ...,
        numeric_only: _bool = ...,
        na_option: Literal["keep", "top", "bottom"] = ...,
        ascending: _bool = ...,
        pct: _bool = ...,
    ) -> NDFrame: ...
    def where(
        self,
        cond,
        other=...,
        *,
        inplace: _bool = ...,
        axis=...,
        level=...,
        try_cast: _bool = ...,
    ): ...
    def mask(
        self,
        cond,
        other=...,
        *,
        inplace: _bool = ...,
        axis=...,
        level=...,
        try_cast: _bool = ...,
    ): ...
    def shift(self, periods=..., freq=..., axis=..., fill_value=...) -> Self:
        """
Shift index by desired number of periods with an optional time `freq`.

When `freq` is not passed, shift the index without realigning the data.
If `freq` is passed (in this case, the index must be date or datetime,
or it will raise a `NotImplementedError`), the index will be
increased using the periods and the `freq`. `freq` can be inferred
when specified as "infer" as long as either freq or inferred_freq
attribute is set in the index.

Parameters
----------
periods : int or Sequence
    Number of periods to shift. Can be positive or negative.
    If an iterable of ints, the data will be shifted once by each int.
    This is equivalent to shifting by one value at a time and
    concatenating all resulting frames. The resulting columns will have
    the shift suffixed to their column names. For multiple periods,
    axis must not be 1.
freq : DateOffset, tseries.offsets, timedelta, or str, optional
    Offset to use from the tseries module or time rule (e.g. 'EOM').
    If `freq` is specified then the index values are shifted but the
    data is not realigned. That is, use `freq` if you would like to
    extend the index when shifting and preserve the original data.
    If `freq` is specified as "infer" then it will be inferred from
    the freq or inferred_freq attributes of the index. If neither of
    those attributes exist, a ValueError is thrown.
axis : {0 or 'index', 1 or 'columns', None}, default None
    Shift direction. For `Series` this parameter is unused and defaults to 0.
fill_value : object, optional
    The scalar value to use for newly introduced missing values.
    the default depends on the dtype of `self`.
    For numeric data, ``np.nan`` is used.
    For datetime, timedelta, or period data, etc. :attr:`NaT` is used.
    For extension dtypes, ``self.dtype.na_value`` is used.
suffix : str, optional
    If str and periods is an iterable, this is added after the column
    name and before the shift value for each shifted column name.

Returns
-------
Series/DataFrame
    Copy of input object, shifted.

See Also
--------
Index.shift : Shift values of Index.
DatetimeIndex.shift : Shift values of DatetimeIndex.
PeriodIndex.shift : Shift values of PeriodIndex.

Examples
--------
>>> df = pd.DataFrame({"Col1": [10, 20, 15, 30, 45],
...                    "Col2": [13, 23, 18, 33, 48],
...                    "Col3": [17, 27, 22, 37, 52]},
...                   index=pd.date_range("2020-01-01", "2020-01-05"))
>>> df
            Col1  Col2  Col3
2020-01-01    10    13    17
2020-01-02    20    23    27
2020-01-03    15    18    22
2020-01-04    30    33    37
2020-01-05    45    48    52

>>> df.shift(periods=3)
            Col1  Col2  Col3
2020-01-01   NaN   NaN   NaN
2020-01-02   NaN   NaN   NaN
2020-01-03   NaN   NaN   NaN
2020-01-04  10.0  13.0  17.0
2020-01-05  20.0  23.0  27.0

>>> df.shift(periods=1, axis="columns")
            Col1  Col2  Col3
2020-01-01   NaN    10    13
2020-01-02   NaN    20    23
2020-01-03   NaN    15    18
2020-01-04   NaN    30    33
2020-01-05   NaN    45    48

>>> df.shift(periods=3, fill_value=0)
            Col1  Col2  Col3
2020-01-01     0     0     0
2020-01-02     0     0     0
2020-01-03     0     0     0
2020-01-04    10    13    17
2020-01-05    20    23    27

>>> df.shift(periods=3, freq="D")
            Col1  Col2  Col3
2020-01-04    10    13    17
2020-01-05    20    23    27
2020-01-06    15    18    22
2020-01-07    30    33    37
2020-01-08    45    48    52

>>> df.shift(periods=3, freq="infer")
            Col1  Col2  Col3
2020-01-04    10    13    17
2020-01-05    20    23    27
2020-01-06    15    18    22
2020-01-07    30    33    37
2020-01-08    45    48    52

>>> df['Col1'].shift(periods=[0, 1, 2])
            Col1_0  Col1_1  Col1_2
2020-01-01      10     NaN     NaN
2020-01-02      20    10.0     NaN
2020-01-03      15    20.0    10.0
2020-01-04      30    15.0    20.0
2020-01-05      45    30.0    15.0
        """
        pass
    def slice_shift(self, periods: int = ..., axis=...) -> Self: ...
    def tshift(self, periods: int = ..., freq=..., axis=...) -> Self: ...
    def truncate(self, before=..., after=..., axis=..., copy: _bool = ...) -> Self: ...
    def tz_convert(self, tz, axis=..., level=..., copy: _bool = ...) -> Self: ...
    def tz_localize(
        self,
        tz,
        axis=...,
        level=...,
        copy: _bool = ...,
        ambiguous=...,
        nonexistent: str = ...,
    ) -> Self: ...
    def abs(self) -> Self: ...
    def describe(
        self,
        percentiles=...,
        include=...,
        exclude=...,
        datetime_is_numeric: _bool | None = ...,
    ) -> NDFrame: ...
    def pct_change(
        self, periods=..., fill_method=..., limit=..., freq=..., **kwargs
    ) -> Self: ...
    def first_valid_index(self): ...
    def last_valid_index(self): ...
