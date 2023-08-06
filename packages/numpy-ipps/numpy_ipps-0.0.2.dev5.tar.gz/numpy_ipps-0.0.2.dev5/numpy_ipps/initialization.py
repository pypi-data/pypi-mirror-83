"""Vector Initialization Functions."""
import enum

import numpy
import numpy.ctypeslib

import numpy_ipps._detail.debug
import numpy_ipps._detail.dispatch
import numpy_ipps.utils


_init_policies = numpy_ipps._detail.dispatch.Policies(
    bytes1=numpy_ipps._detail.dispatch.TagPolicy.UNSIGNED,
    bytes2=numpy_ipps._detail.dispatch.TagPolicy.SIGNED,
    bytes3=numpy_ipps._detail.dispatch.TagPolicy.SIGNED,
    bytes4=numpy_ipps._detail.dispatch.TagPolicy.SIGNED,
)


class Assign:
    """Assign Function."""

    __slots__ = ("callback",)

    def __init__(self, dtype=float, overlap=False):
        if overlap:
            self.callback = numpy_ipps._detail.dispatch.ipps_function(
                "Move",
                ("void*", "void*", "int"),
                dtype,
                policies=_init_policies,
            )
        else:
            self.callback = numpy_ipps._detail.dispatch.ipps_function(
                "Copy",
                ("void*", "void*", "int"),
                dtype,
                policies=_init_policies,
            )

    def __call__(self, src, dst):
        assert (
            src.ndarray.size == dst.ndarray.size
        ), "src and dst size not compatible."

        numpy_ipps.status = self.callback(
            src.cdata,
            dst.cdata,
            dst.size,
        )

    def _fallback(self, src, dst):
        assert (
            src.ndarray.size == dst.ndarray.size
        ), "src and dst size not compatible."

        numpy.copyto(dst.ndarray, src.ndarray)


class Endian(enum.Enum):
    """Endianess Enum."""

    LITTLE = 1
    BIG = 2


class BitShift:
    """BitShift Function."""

    __slots__ = ("callback", "src_bit_offset", "dst_bit_offset")

    def __init__(
        self,
        src_bit_offset=0,
        dst_bit_offset=0,
        endian=Endian.LITTLE,
    ):
        self.src_bit_offset = numpy_ipps.utils.cast("int", src_bit_offset)
        self.dst_bit_offset = numpy_ipps.utils.cast("int", dst_bit_offset)

        if endian == Endian.LITTLE:
            self.callback = numpy_ipps._detail.dispatch.ipps_function(
                "CopyLE_1u",
                ("void*", "int", "void*", "int", "int"),
                policies=_init_policies,
            )
        elif endian == Endian.BIG:
            self.callback = numpy_ipps._detail.dispatch.ipps_function(
                "CopyBE_1u",
                ("void*", "int", "void*", "int", "int"),
                policies=_init_policies,
            )
        else:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Unknown endianess: {}".format(endian),
                name=__name__,
            )

    def __call__(self, src, dst, size):
        numpy_ipps.status = self.callback(
            src.cdata,
            self.src_bit_offset,
            dst.cdata,
            self.dst_bit_offset,
            size,
        )

    def _fallback(self, src, dst):
        raise NotImplementedError


class SetTo:
    """SetTo Function."""

    __slots__ = ("callback",)

    def __init__(self, dtype=float):
        self.callback = numpy_ipps._detail.dispatch.ipps_function(
            "Set",
            (
                numpy_ipps._detail.dispatch.as_ctype_str(
                    dtype, policies=_init_policies
                ),
                "void*",
                "int",
            ),
            dtype,
            policies=_init_policies,
        )

    def __call__(self, src, value):
        numpy_ipps.status = self.callback(value, src.cdata, src.size)

    def _fallback(self, src, value):
        src.ndarray[:] = value


class Zeros:
    """Zeros Function."""

    __slots__ = ("callback",)

    def __init__(self, dtype=float):
        self.callback = numpy_ipps._detail.dispatch.ipps_function(
            "Zero", ("void*", "int"), dtype, policies=_init_policies
        )

    def __call__(self, src):
        numpy_ipps.status = self.callback(src.cdata, src.size)

    def _fallback(self, src):
        src.ndarray[:] = 0
