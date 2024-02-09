from typing import Any

class PandasDelegate: ...

def delegate_names(
    delegate: Any, accessors: Any, typ: str, overwrite: bool = ...
) -> Any: ...

class CachedAccessor:
    def __init__(self, name: str, accessor: Any) -> None: ...
    def __get__(self, obj: Any, cls: Any): ...

def register_dataframe_accessor(name: Any):
    """
Register a custom accessor on DataFrame objects.

Parameters
----------
name : str
    Name under which the accessor should be registered. A warning is issued
    if this name conflicts with a preexisting attribute.

Returns
-------
callable
    A class decorator.

See Also
--------
register_dataframe_accessor : Register a custom accessor on DataFrame objects.
register_series_accessor : Register a custom accessor on Series objects.
register_index_accessor : Register a custom accessor on Index objects.

Notes
-----
When accessed, your accessor will be initialized with the pandas object
the user is interacting with. So the signature must be

.. code-block:: python

    def __init__(self, pandas_object):  # noqa: E999
        ...

For consistency with pandas methods, you should raise an ``AttributeError``
if the data passed to your accessor has an incorrect dtype.

>>> pd.Series(['a', 'b']).dt
Traceback (most recent call last):
...
AttributeError: Can only use .dt accessor with datetimelike values

Examples
--------
In your library code::

    import pandas as pd

    @pd.api.extensions.register_dataframe_accessor("geo")
    class GeoAccessor:
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        @property
        def center(self):
            # return the geographic center point of this DataFrame
            lat = self._obj.latitude
            lon = self._obj.longitude
            return (float(lon.mean()), float(lat.mean()))

        def plot(self):
            # plot this array's data on a map, e.g., using Cartopy
            pass

Back in an interactive IPython session:

    .. code-block:: ipython

        In [1]: ds = pd.DataFrame({"longitude": np.linspace(0, 10),
           ...:                    "latitude": np.linspace(0, 20)})
        In [2]: ds.geo.center
        Out[2]: (5.0, 10.0)
        In [3]: ds.geo.plot()  # plots data on a map
    """
    pass
def register_series_accessor(name: Any):
    """
Register a custom accessor on Series objects.

Parameters
----------
name : str
    Name under which the accessor should be registered. A warning is issued
    if this name conflicts with a preexisting attribute.

Returns
-------
callable
    A class decorator.

See Also
--------
register_dataframe_accessor : Register a custom accessor on DataFrame objects.
register_series_accessor : Register a custom accessor on Series objects.
register_index_accessor : Register a custom accessor on Index objects.

Notes
-----
When accessed, your accessor will be initialized with the pandas object
the user is interacting with. So the signature must be

.. code-block:: python

    def __init__(self, pandas_object):  # noqa: E999
        ...

For consistency with pandas methods, you should raise an ``AttributeError``
if the data passed to your accessor has an incorrect dtype.

>>> pd.Series(['a', 'b']).dt
Traceback (most recent call last):
...
AttributeError: Can only use .dt accessor with datetimelike values

Examples
--------
In your library code::

    import pandas as pd

    @pd.api.extensions.register_dataframe_accessor("geo")
    class GeoAccessor:
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        @property
        def center(self):
            # return the geographic center point of this DataFrame
            lat = self._obj.latitude
            lon = self._obj.longitude
            return (float(lon.mean()), float(lat.mean()))

        def plot(self):
            # plot this array's data on a map, e.g., using Cartopy
            pass

Back in an interactive IPython session:

    .. code-block:: ipython

        In [1]: ds = pd.DataFrame({"longitude": np.linspace(0, 10),
           ...:                    "latitude": np.linspace(0, 20)})
        In [2]: ds.geo.center
        Out[2]: (5.0, 10.0)
        In [3]: ds.geo.plot()  # plots data on a map
    """
    pass
def register_index_accessor(name: Any):
    """
Register a custom accessor on Index objects.

Parameters
----------
name : str
    Name under which the accessor should be registered. A warning is issued
    if this name conflicts with a preexisting attribute.

Returns
-------
callable
    A class decorator.

See Also
--------
register_dataframe_accessor : Register a custom accessor on DataFrame objects.
register_series_accessor : Register a custom accessor on Series objects.
register_index_accessor : Register a custom accessor on Index objects.

Notes
-----
When accessed, your accessor will be initialized with the pandas object
the user is interacting with. So the signature must be

.. code-block:: python

    def __init__(self, pandas_object):  # noqa: E999
        ...

For consistency with pandas methods, you should raise an ``AttributeError``
if the data passed to your accessor has an incorrect dtype.

>>> pd.Series(['a', 'b']).dt
Traceback (most recent call last):
...
AttributeError: Can only use .dt accessor with datetimelike values

Examples
--------
In your library code::

    import pandas as pd

    @pd.api.extensions.register_dataframe_accessor("geo")
    class GeoAccessor:
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        @property
        def center(self):
            # return the geographic center point of this DataFrame
            lat = self._obj.latitude
            lon = self._obj.longitude
            return (float(lon.mean()), float(lat.mean()))

        def plot(self):
            # plot this array's data on a map, e.g., using Cartopy
            pass

Back in an interactive IPython session:

    .. code-block:: ipython

        In [1]: ds = pd.DataFrame({"longitude": np.linspace(0, 10),
           ...:                    "latitude": np.linspace(0, 20)})
        In [2]: ds.geo.center
        Out[2]: (5.0, 10.0)
        In [3]: ds.geo.plot()  # plots data on a map
    """
    pass
