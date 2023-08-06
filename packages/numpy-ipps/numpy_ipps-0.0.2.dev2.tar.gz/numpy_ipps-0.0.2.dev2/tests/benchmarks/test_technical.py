import ctypes
import enum
import inspect

import numpy
import pytest
import regex

import numpy_ipps._detail.libipp
import numpy_ipps.initialization
import numpy_ipps.utils


class ipps_enum(enum.IntEnum):
    ndarray = 0
    cdata = 1
    size = 2
    shape = 3


def numpy_ipps_dict(array):
    return {
        "ndarray": array,
        "cdata": numpy_ipps._detail.libipp.ffi.from_buffer(array),
        "size": numpy_ipps._detail.libipp.ffi.cast("int", array.size),
        "shape": numpy_ipps._detail.libipp.ffi.new("int[]", array.shape),
    }


def indirect_dict(lhs, rhs):
    lhs["cdata"]
    lhs["size"]
    lhs["shape"]
    rhs["cdata"]
    rhs["size"]
    lhs["shape"]


def test_indirect_dict(benchmark):
    lhs = numpy_ipps_dict(numpy.empty(1 << 10))
    rhs = numpy_ipps_dict(numpy.empty(1 << 10))
    benchmark(indirect_dict, lhs, rhs)


def numpy_ipps_list(array):
    return [
        array,
        numpy_ipps._detail.libipp.ffi.from_buffer(array),
        numpy_ipps._detail.libipp.ffi.cast("int", array.size),
        numpy_ipps._detail.libipp.ffi.new("int[]", array.shape),
    ]


def indirect_list_tuple(lhs, rhs):
    lhs[ipps_enum.cdata]
    lhs[ipps_enum.size]
    lhs[ipps_enum.shape]
    rhs[ipps_enum.cdata]
    rhs[ipps_enum.size]
    rhs[ipps_enum.shape]


def test_indirect_list(benchmark):
    lhs = numpy_ipps_list(numpy.empty(1 << 10))
    rhs = numpy_ipps_list(numpy.empty(1 << 10))
    benchmark(indirect_list_tuple, lhs, rhs)


def numpy_ipps_tuple(array):
    return (
        array,
        numpy_ipps._detail.libipp.ffi.from_buffer(array),
        numpy_ipps._detail.libipp.ffi.cast("int", array.size),
        numpy_ipps._detail.libipp.ffi.new("int[]", array.shape),
    )


def test_indirect_tuple(benchmark):
    lhs = numpy_ipps_tuple(numpy.empty(1 << 10))
    rhs = numpy_ipps_tuple(numpy.empty(1 << 10))
    benchmark(indirect_list_tuple, lhs, rhs)


class indirection_class:
    def __init__(self, array):
        self.ndarray = array
        self.cdata = numpy_ipps._detail.libipp.ffi.from_buffer(array)
        self.size = numpy_ipps._detail.libipp.ffi.cast("int", array.size)
        self.shape = numpy_ipps._detail.libipp.ffi.new("int[]", array.shape)


def indirect_class(lhs, rhs):
    lhs.cdata
    lhs.size
    lhs.shape
    rhs.cdata
    rhs.size
    rhs.shape


def test_indirect_class(benchmark):
    lhs = indirection_class(numpy.empty(1 << 10))
    rhs = indirection_class(numpy.empty(1 << 10))
    benchmark(indirect_class, lhs, rhs)


class indirection_class_slots:
    __slots__ = ("ndarray", "cdata", "size", "shape")

    def __init__(self, array):
        self.ndarray = array
        self.cdata = numpy_ipps._detail.libipp.ffi.from_buffer(array)
        self.size = numpy_ipps._detail.libipp.ffi.cast("int", array.size)
        self.shape = numpy_ipps._detail.libipp.ffi.new("int[]", array.shape)


def test_indirect_class_slots(benchmark):
    lhs = indirection_class_slots(numpy.empty(1 << 10))
    rhs = indirection_class_slots(numpy.empty(1 << 10))
    benchmark(indirect_class, lhs, rhs)


class AssignNoSlots:
    def __init__(self, dtype=float, overlap=False):
        if overlap:
            self.callback = numpy_ipps._detail.dispatch.ipps_function(
                "Move", ("void*", "void*", "int"), dtype
            )
        else:
            self.callback = numpy_ipps._detail.dispatch.ipps_function(
                "Copy", ("void*", "void*", "int"), dtype
            )

    def __call__(self, src, dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            dst.cdata,
            dst.size,
        )


class AssignSlots:
    __slots__ = ("callback",)

    def __init__(self, dtype=float, overlap=False):
        if overlap:
            self.callback = numpy_ipps._detail.dispatch.ipps_function(
                "Move", ("void*", "void*", "int"), dtype
            )
        else:
            self.callback = numpy_ipps._detail.dispatch.ipps_function(
                "Copy", ("void*", "void*", "int"), dtype
            )

    def __call__(self, src, dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            dst.cdata,
            dst.size,
        )


@pytest.mark.parametrize("order", [10, 20])
@pytest.mark.parametrize(
    "dtype", [numpy.int32, numpy.int64, numpy.float32, numpy.float64]
)
def test_ipps_assign_no_slots(benchmark, order, dtype):
    assign = AssignNoSlots(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign, src, dst)


@pytest.mark.parametrize("order", [10, 20])
@pytest.mark.parametrize(
    "dtype", [numpy.int32, numpy.int64, numpy.float32, numpy.float64]
)
def test_ipps_assign_slots(benchmark, order, dtype):
    assign = AssignSlots(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign, src, dst)


class context_ws:
    __slots__ = (
        "symbols",
        "_outer_frame",
        "_outer_frame_ptr",
        "_PyFrame_flag",
    )
    _pattern = regex.compile(
        r".*context_ws\s*\(((?:[^,()]+)(?:,[^,()]+)*)\).*", regex.V1
    )

    def __init__(self, *args):
        self._outer_frame = inspect.currentframe().f_back
        self._outer_frame_ptr = ctypes.py_object(self._outer_frame)
        self._PyFrame_flag = ctypes.c_int(0)
        self.symbols = (
            regex.search(
                context_ws._pattern,
                inspect.getframeinfo(self._outer_frame).code_context[0],
            )
            .group(1)
            .replace(" ", "")
            .split(",")
        )

    def _LocalsToFast(self):
        ctypes.pythonapi.PyFrame_LocalsToFast(
            self._outer_frame_ptr, self._PyFrame_flag
        )

    def __enter__(self):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = numpy_ipps.utils.ndarray(
                self._outer_frame.f_locals[symbol]
            )
            self._LocalsToFast()

    def __exit__(self, *args):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = self._outer_frame.f_locals[
                symbol
            ].ndarray
            self._LocalsToFast()
        return False


class context_ns:
    _pattern = regex.compile(
        r".*context_ns\s*\(((?:[^,()]+)(?:,[^,()]+)*)\).*", regex.V1
    )

    def __init__(self, *args):
        self._outer_frame = inspect.currentframe().f_back
        self._outer_frame_ptr = ctypes.py_object(self._outer_frame)
        self._PyFrame_flag = ctypes.c_int(0)
        self.symbols = (
            regex.search(
                context_ns._pattern,
                inspect.getframeinfo(self._outer_frame).code_context[0],
            )
            .group(1)
            .replace(" ", "")
            .split(",")
        )

    def _LocalsToFast(self):
        ctypes.pythonapi.PyFrame_LocalsToFast(
            self._outer_frame_ptr, self._PyFrame_flag
        )

    def __enter__(self):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = numpy_ipps.utils.ndarray(
                self._outer_frame.f_locals[symbol]
            )
            self._LocalsToFast()

    def __exit__(self, *args):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = self._outer_frame.f_locals[
                symbol
            ].ndarray
            self._LocalsToFast()
        return False


def call_context_ns(assign, src, dst):
    with context_ns(src, dst):
        assign(src, dst)


@pytest.mark.parametrize("order", [10, 20])
@pytest.mark.parametrize(
    "dtype", [numpy.int32, numpy.int64, numpy.float32, numpy.float64]
)
def test_context_ns(benchmark, order, dtype):
    assign = numpy_ipps.initialization.Assign(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    benchmark(call_context_ns, assign, src, dst)


def call_context_ws(assign, src, dst):
    with context_ws(src, dst):
        assign(src, dst)


@pytest.mark.parametrize("order", [10, 20])
@pytest.mark.parametrize(
    "dtype", [numpy.int32, numpy.int64, numpy.float32, numpy.float64]
)
def test_context_ws(benchmark, order, dtype):
    assign = numpy_ipps.initialization.Assign(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    benchmark(call_context_ws, assign, src, dst)
