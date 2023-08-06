import importlib
import logging
import os

import numpy
import psutil
import pytest

import numpy_ipps.initialization
import numpy_ipps.utils


max_cache_size = psutil.virtual_memory().total
orders = range(2, int(numpy.floor(numpy.log2(max_cache_size))) - 6)
dtypes = (
    numpy.int8,
    numpy.uint8,
    numpy.int16,
    numpy.uint16,
    numpy.int32,
    numpy.uint32,
    numpy.int64,
    numpy.uint64,
    numpy.float32,
    numpy.float64,
    numpy.complex64,
    numpy.complex128,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_initialization.log",
    )
    ch = logging.FileHandler(log_file, mode="w")
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(ch)
    importlib.reload(numpy_ipps)

    yield logger

    logger.removeHandler(ch)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_assign(logger_fixture, benchmark, order, dtype):
    assign = numpy_ipps.initialization.Assign(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign, src, dst)

    numpy.testing.assert_almost_equal(dst, src)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_assign(logger_fixture, benchmark, order, dtype):
    assign = numpy_ipps.initialization.Assign(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign._fallback, src, dst)

    numpy.testing.assert_almost_equal(dst, src)


@pytest.mark.parametrize("order", orders)
def test_ipps_bitshiftLE(logger_fixture, benchmark, order):
    bitshift_le = numpy_ipps.initialization.BitShift(
        3, 5, numpy_ipps.initialization.Endian.little
    )
    src = numpy.empty(1 << order, dtype=numpy.uint8)
    dst = numpy.empty(1 << order, dtype=numpy.uint8)
    size = 8 * (1 << order) - 12

    with numpy_ipps.utils.context(src, dst):
        benchmark(bitshift_le, src, dst, size)


@pytest.mark.parametrize("order", orders)
def test_ipps_bitshiftBE(logger_fixture, benchmark, order):
    bitshift_be = numpy_ipps.initialization.BitShift(
        3, 5, numpy_ipps.initialization.Endian.big
    )
    src = numpy.empty(1 << order, dtype=numpy.uint8)
    dst = numpy.empty(1 << order, dtype=numpy.uint8)
    size = 8 * (1 << order) - 12

    with numpy_ipps.utils.context(src, dst):
        benchmark(bitshift_be, src, dst, size)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_set0(logger_fixture, benchmark, order, dtype):
    zeros = numpy_ipps.initialization.Zeros(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src):
        benchmark(zeros, src)

    numpy.testing.assert_almost_equal(
        src, numpy.zeros(1 << order, dtype=dtype)
    )


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes[2:-2])
def test_ipps_set1(logger_fixture, benchmark, order, dtype):
    set_to_1 = numpy_ipps.initialization.SetTo(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src):
        benchmark(set_to_1, src, 1)

    numpy.testing.assert_almost_equal(src, numpy.ones(1 << order, dtype=dtype))


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_set0(logger_fixture, benchmark, order, dtype):
    zeros = numpy_ipps.initialization.Zeros(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src):
        benchmark(zeros._fallback, src)

    numpy.testing.assert_almost_equal(
        src, numpy.zeros(1 << order, dtype=dtype)
    )


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes[2:-2])
def test_fallback_set1(logger_fixture, benchmark, order, dtype):
    set_to_1 = numpy_ipps.initialization.SetTo(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src):
        benchmark(set_to_1._fallback, src, 1)

    numpy.testing.assert_almost_equal(src, numpy.ones(1 << order, dtype=dtype))
