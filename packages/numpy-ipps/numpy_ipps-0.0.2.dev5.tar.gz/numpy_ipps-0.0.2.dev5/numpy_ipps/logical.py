"""Logical Functions."""
import numpy
import numpy.ctypeslib

import numpy_ipps._detail.debug
import numpy_ipps._detail.dispatch
import numpy_ipps._detail.dtype
import numpy_ipps.utils


_logical_policies = numpy_ipps._detail.dispatch.Policies(
    bytes1=numpy_ipps._detail.dispatch.TagPolicy.UNSIGNED,
    bytes2=numpy_ipps._detail.dispatch.TagPolicy.UNSIGNED,
    bytes3=numpy_ipps._detail.dispatch.TagPolicy.UNSIGNED,
    bytes4=numpy_ipps._detail.dispatch.TagPolicy.DOWN_UNSIGNED,
)


class AndC:
    """AndC Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "AndC",
            (
                "void*",
                numpy_ipps._detail.dispatch.as_ctype_str(
                    dtype, policies=_logical_policies
                ),
                "void*",
                "int",
            ),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src_cdata, val, dst_cdata, dst_size):
        return self._callback_ipps(
            src_cdata,
            val,
            dst_cdata,
            2 * int(dst_size),
        )

    def __call__(self, src, val, dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            val,
            dst.cdata,
            dst.size,
        )

    def _fallback(self, src, val, dst):
        numpy.bitwise_and(src.ndarray, val, dst.ndarray)


class AndC_I:
    """AndC Inplace Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "AndC_I",
            (
                numpy_ipps._detail.dispatch.as_ctype_str(
                    dtype, policies=_logical_policies
                ),
                "void*",
                "int",
            ),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, val, src_dst_cdata, src_dst_size):
        return self._callback_ipps(
            val,
            src_dst_cdata,
            2 * int(src_dst_size),
        )

    def __call__(self, val, src_dst):
        numpy_ipps.status = self.callback(
            val,
            src_dst.cdata,
            src_dst.size,
        )

    def _fallback(self, val, src_dst):
        numpy.bitwise_and(src_dst.ndarray, val, src_dst.ndarray)


class OrC:
    """OrC Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "OrC",
            (
                "void*",
                numpy_ipps._detail.dispatch.as_ctype_str(
                    dtype, policies=_logical_policies
                ),
                "void*",
                "int",
            ),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src_cdata, val, dst_cdata, dst_size):
        return self._callback_ipps(
            src_cdata,
            val,
            dst_cdata,
            2 * int(dst_size),
        )

    def __call__(self, src, val, dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            val,
            dst.cdata,
            dst.size,
        )

    def _fallback(self, src, val, dst):
        numpy.bitwise_or(src.ndarray, val, dst.ndarray)


class OrC_I:
    """OrC Inplace Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "OrC_I",
            (
                numpy_ipps._detail.dispatch.as_ctype_str(
                    dtype, policies=_logical_policies
                ),
                "void*",
                "int",
            ),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, val, src_dst_cdata, src_dst_size):
        return self._callback_ipps(
            val,
            src_dst_cdata,
            2 * int(src_dst_size),
        )

    def __call__(self, val, src_dst):
        numpy_ipps.status = self.callback(
            val,
            src_dst.cdata,
            src_dst.size,
        )

    def _fallback(self, val, src_dst):
        numpy.bitwise_or(src_dst.ndarray, val, src_dst.ndarray)


class XorC:
    """XorC Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "XorC",
            (
                "void*",
                numpy_ipps._detail.dispatch.as_ctype_str(
                    dtype, policies=_logical_policies
                ),
                "void*",
                "int",
            ),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src_cdata, val, dst_cdata, dst_size):
        return self._callback_ipps(
            src_cdata,
            val,
            dst_cdata,
            2 * int(dst_size),
        )

    def __call__(self, src, val, dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            val,
            dst.cdata,
            dst.size,
        )

    def _fallback(self, src, val, dst):
        numpy.bitwise_xor(src.ndarray, val, dst.ndarray)


class XorC_I:
    """XorC Inplace Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "XorC_I",
            (
                numpy_ipps._detail.dispatch.as_ctype_str(
                    dtype, policies=_logical_policies
                ),
                "void*",
                "int",
            ),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, val, src_dst_cdata, src_dst_size):
        return self._callback_ipps(
            val,
            src_dst_cdata,
            2 * int(src_dst_size),
        )

    def __call__(self, val, src_dst):
        numpy_ipps.status = self.callback(
            val,
            src_dst.cdata,
            src_dst.size,
        )

    def _fallback(self, val, src_dst):
        numpy.bitwise_xor(src_dst.ndarray, val, src_dst.ndarray)


class And:
    """And Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "And",
            ("void*", "void*", "void*", "int"),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src1_cdata, src2_cdata, dst_cdata, dst_size):
        return self._callback_ipps(
            src1_cdata,
            src2_cdata,
            dst_cdata,
            2 * int(dst_size),
        )

    def __call__(self, src1, src2, dst):
        numpy_ipps.status = self.callback(
            src1.cdata,
            src2.cdata,
            dst.cdata,
            dst.size,
        )

    def _fallback(self, src1, src2, dst):
        numpy.bitwise_and(src1.ndarray, src2.ndarray, dst.ndarray)


class And_I:
    """And Inplace Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "And_I",
            ("void*", "void*", "int"),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src_cdata, src_dst_cdata, src_dst_size):
        return self._callback_ipps(
            src_cdata,
            src_dst_cdata,
            2 * int(src_dst_size),
        )

    def __call__(self, src, src_dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            src_dst.cdata,
            src_dst.size,
        )

    def _fallback(self, src, src_dst):
        numpy.bitwise_and(src.ndarray, src_dst.ndarray, src_dst.ndarray)


class Or:
    """Or Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "Or",
            ("void*", "void*", "void*", "int"),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src1_cdata, src2_cdata, dst_cdata, dst_size):
        return self._callback_ipps(
            src1_cdata,
            src2_cdata,
            dst_cdata,
            2 * int(dst_size),
        )

    def __call__(self, src1, src2, dst):
        numpy_ipps.status = self.callback(
            src1.cdata,
            src2.cdata,
            dst.cdata,
            dst.size,
        )

    def _fallback(self, src1, src2, dst):
        numpy.bitwise_or(src1.ndarray, src2.ndarray, dst.ndarray)


class Or_I:
    """Or Inplace Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "Or_I",
            ("void*", "void*", "int"),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src_cdata, src_dst_cdata, src_dst_size):
        return self._callback_ipps(
            src_cdata,
            src_dst_cdata,
            2 * int(src_dst_size),
        )

    def __call__(self, src, src_dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            src_dst.cdata,
            src_dst.size,
        )

    def _fallback(self, src, src_dst):
        numpy.bitwise_or(src.ndarray, src_dst.ndarray, src_dst.ndarray)


class Xor:
    """XorC Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "Xor",
            ("void*", "void*", "void*", "int"),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src1_cdata, src2_cdata, dst_cdata, dst_size):
        return self._callback_ipps(
            src1_cdata,
            src2_cdata,
            dst_cdata,
            2 * int(dst_size),
        )

    def __call__(self, src1, src2, dst):
        numpy_ipps.status = self.callback(
            src1.cdata,
            src2.cdata,
            dst.cdata,
            dst.size,
        )

    def _fallback(self, src1, src2, dst):
        numpy.bitwise_xor(src1.ndarray, src2.ndarray, dst.ndarray)


class Xor_I:
    """Xor Inplace Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "Xor_I",
            ("void*", "void*", "int"),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src_cdata, src_dst_cdata, src_dst_size):
        return self._callback_ipps(
            src_cdata,
            src_dst_cdata,
            2 * int(src_dst_size),
        )

    def __call__(self, src, src_dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            src_dst.cdata,
            src_dst.size,
        )

    def _fallback(self, src, src_dst):
        numpy.bitwise_xor(src.ndarray, src_dst.ndarray, src_dst.ndarray)


class Not:
    """Not Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "Not",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src_cdata, dst_cdata, dst_size):
        return self._callback_ipps(
            src_cdata,
            dst_cdata,
            2 * int(dst_size),
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            dst.cdata,
            dst.size,
        )

    def _fallback(self, src, dst):
        numpy.invert(src.ndarray, dst.ndarray)


class Not_I:
    """Not Inplace Function."""

    __slots__ = ("callback", "_callback_ipps")

    def __init__(self, dtype=numpy.uint32):
        self._callback_ipps = numpy_ipps._detail.dispatch.ipps_function(
            "Not_I",
            (
                "void*",
                "int",
            ),
            dtype,
            policies=_logical_policies,
        )
        if numpy.dtype(dtype).itemsize == 8:
            self.callback = self._callback_64
        else:
            self.callback = self._callback_ipps

    def _callback_64(self, src_dst_cdata, src_dst_size):
        return self._callback_ipps(
            src_dst_cdata,
            2 * int(src_dst_size),
        )

    def __call__(self, src_dst):
        numpy_ipps.status = self.callback(
            src_dst.cdata,
            src_dst.size,
        )

    def _fallback(self, src_dst):
        numpy.invert(src_dst.ndarray, src_dst.ndarray)
