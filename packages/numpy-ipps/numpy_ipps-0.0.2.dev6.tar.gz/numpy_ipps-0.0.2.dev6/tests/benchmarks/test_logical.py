import importlib
import logging
import os

import numpy
import psutil
import pytest

import numpy_ipps.logical
import numpy_ipps.utils


max_cache_size = psutil.virtual_memory().total
orders = range(3, int(numpy.floor(numpy.log2(max_cache_size))) - 6)
dtypes = (
    numpy.int8,
    numpy.uint8,
    numpy.int16,
    numpy.uint16,
    numpy.int32,
    numpy.uint32,
    numpy.int64,
    numpy.uint64,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_logical.log",
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
def test_ipps_andc(logger_fixture, benchmark, order, dtype):
    andc = numpy_ipps.logical.AndC(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    value = 0
    if dtype in [numpy.int8, numpy.uint8]:
        value = numpy_ipps.utils.cast("char", value)

    with numpy_ipps.utils.context(src, dst):
        benchmark(andc, src, value, dst)

    numpy.testing.assert_almost_equal(dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_andcI(logger_fixture, benchmark, order, dtype):
    andc_I = numpy_ipps.logical.AndC_I(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    value = 0
    if dtype in [numpy.int8, numpy.uint8]:
        value = numpy_ipps.utils.cast("char", value)

    with numpy_ipps.utils.context(src_dst):
        benchmark(andc_I, value, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_andc(logger_fixture, benchmark, order, dtype):
    andc = numpy_ipps.logical.AndC(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    value = 0

    with numpy_ipps.utils.context(src, dst):
        benchmark(andc._fallback, src, value, dst)

    numpy.testing.assert_almost_equal(dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_andcI(logger_fixture, benchmark, order, dtype):
    andc_I = numpy_ipps.logical.AndC_I(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    value = 0

    with numpy_ipps.utils.context(src_dst):
        benchmark(andc_I._fallback, value, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_orc(logger_fixture, benchmark, order, dtype):
    orc = numpy_ipps.logical.OrC(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    value = 1
    if dtype in [numpy.int8, numpy.uint8]:
        value = numpy_ipps.utils.cast("char", value)

    with numpy_ipps.utils.context(src, dst):
        benchmark(orc, src, value, dst)

    if dtype in [numpy.int64, numpy.uint64]:
        numpy.testing.assert_almost_equal(dst, 4294967297)
    else:
        numpy.testing.assert_almost_equal(dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_orcI(logger_fixture, benchmark, order, dtype):
    orc_I = numpy_ipps.logical.OrC_I(dtype=dtype)
    src_dst = numpy.zeros(1 << order, dtype=dtype)

    value = 1
    if dtype in [numpy.int8, numpy.uint8]:
        value = numpy_ipps.utils.cast("char", value)

    with numpy_ipps.utils.context(src_dst):
        benchmark(orc_I, value, src_dst)

    if dtype in [numpy.int64, numpy.uint64]:
        numpy.testing.assert_almost_equal(src_dst, 4294967297)
    else:
        numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_orc(logger_fixture, benchmark, order, dtype):
    orc = numpy_ipps.logical.OrC(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    value = 1

    with numpy_ipps.utils.context(src, dst):
        benchmark(orc._fallback, src, value, dst)

    numpy.testing.assert_almost_equal(dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_orcI(logger_fixture, benchmark, order, dtype):
    orc_I = numpy_ipps.logical.OrC_I(dtype=dtype)
    src_dst = numpy.zeros(1 << order, dtype=dtype)

    value = 1

    with numpy_ipps.utils.context(src_dst):
        benchmark(orc_I._fallback, value, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_xorc(logger_fixture, benchmark, order, dtype):
    xorc = numpy_ipps.logical.XorC(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    value = 0
    if dtype in [numpy.int8, numpy.uint8]:
        value = numpy_ipps.utils.cast("char", value)

    with numpy_ipps.utils.context(src, dst):
        benchmark(xorc, src, value, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_xorcI(logger_fixture, benchmark, order, dtype):
    xorc_I = numpy_ipps.logical.XorC_I(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    value = 1
    if dtype in [numpy.int8, numpy.uint8]:
        value = numpy_ipps.utils.cast("char", value)

    with numpy_ipps.utils.context(src_dst):
        benchmark(xorc_I, value, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_xorc(logger_fixture, benchmark, order, dtype):
    xorc = numpy_ipps.logical.XorC(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    value = 0

    with numpy_ipps.utils.context(src, dst):
        benchmark(xorc._fallback, src, value, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_xorcI(logger_fixture, benchmark, order, dtype):
    xorc_I = numpy_ipps.logical.XorC_I(dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    value = 1

    with numpy_ipps.utils.context(src_dst):
        benchmark(xorc_I._fallback, value, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_and(logger_fixture, benchmark, order, dtype):
    andb = numpy_ipps.logical.And(dtype=dtype)
    src1 = numpy.empty(1 << order, dtype=dtype)
    src2 = numpy.zeros(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(andb, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_andI(logger_fixture, benchmark, order, dtype):
    and_I = numpy_ipps.logical.And_I(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(and_I, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_and(logger_fixture, benchmark, order, dtype):
    andb = numpy_ipps.logical.And(dtype=dtype)
    src1 = numpy.empty(1 << order, dtype=dtype)
    src2 = numpy.zeros(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(andb._fallback, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_andI(logger_fixture, benchmark, order, dtype):
    and_I = numpy_ipps.logical.And_I(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(and_I._fallback, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_or(logger_fixture, benchmark, order, dtype):
    orb = numpy_ipps.logical.Or(dtype=dtype)
    src1 = numpy.zeros(1 << order, dtype=dtype)
    src2 = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(orb, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_orI(logger_fixture, benchmark, order, dtype):
    or_I = numpy_ipps.logical.Or_I(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    src_dst = numpy.zeros(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(or_I, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_or(logger_fixture, benchmark, order, dtype):
    orb = numpy_ipps.logical.Or(dtype=dtype)
    src1 = numpy.zeros(1 << order, dtype=dtype)
    src2 = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(orb._fallback, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_orI(logger_fixture, benchmark, order, dtype):
    or_I = numpy_ipps.logical.Or_I(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    src_dst = numpy.zeros(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(or_I._fallback, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_xor(logger_fixture, benchmark, order, dtype):
    xor = numpy_ipps.logical.Xor(dtype=dtype)
    src1 = numpy.empty(1 << order, dtype=dtype)
    src2 = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(xor, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_xorI(logger_fixture, benchmark, order, dtype):
    xor_I = numpy_ipps.logical.Xor_I(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(xor_I, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_xor(logger_fixture, benchmark, order, dtype):
    xor = numpy_ipps.logical.Xor(dtype=dtype)
    src1 = numpy.empty(1 << order, dtype=dtype)
    src2 = numpy.empty(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(xor._fallback, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_xorI(logger_fixture, benchmark, order, dtype):
    xor_I = numpy_ipps.logical.Xor_I(dtype=dtype)
    src = numpy.empty(1 << order, dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(xor_I._fallback, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_not(logger_fixture, benchmark, order, dtype):
    notu = numpy_ipps.logical.Not(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(notu, src, dst)

    numpy.testing.assert_almost_equal(dst, ~dtype(0))


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_ipps_notI(logger_fixture, benchmark, order, dtype):
    notu_I = numpy_ipps.logical.Not_I(dtype=dtype)
    src_dst = numpy.zeros(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(notu_I, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_not(logger_fixture, benchmark, order, dtype):
    notu = numpy_ipps.logical.Not(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(notu._fallback, src, dst)

    numpy.testing.assert_almost_equal(dst, ~dtype(0))


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
def test_fallback_notI(logger_fixture, benchmark, order, dtype):
    notu_I = numpy_ipps.logical.Not_I(dtype=dtype)
    src_dst = numpy.zeros(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(notu_I._fallback, src_dst)
