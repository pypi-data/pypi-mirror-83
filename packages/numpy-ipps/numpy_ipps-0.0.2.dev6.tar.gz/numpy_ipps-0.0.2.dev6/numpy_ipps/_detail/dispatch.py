import ctypes
import enum
import logging

import numpy
import numpy.ctypeslib

import numpy_ipps._detail.debug
import numpy_ipps._detail.libipp


class TagPolicy(enum.Enum):
    KEEP = 1
    UNSIGNED = 2
    SIGNED = 3
    DOWN_KEEP = 4
    DOWN_UNSIGNED = 5
    DOWN_SIGNED = 6


class Policies:
    def __init__(
        self,
        bytes1=TagPolicy.KEEP,
        bytes2=TagPolicy.KEEP,
        bytes3=TagPolicy.KEEP,
        bytes4=TagPolicy.KEEP,
    ):
        self.bytes1 = (bytes1, ctypes.c_uint8, ctypes.c_int8, None)
        self.bytes2 = (bytes2, ctypes.c_uint16, ctypes.c_int16, ctypes.c_int8)
        self.bytes3 = (bytes3, ctypes.c_uint32, ctypes.c_int32, ctypes.c_int16)
        self.bytes4 = (bytes4, ctypes.c_uint64, ctypes.c_int64, ctypes.c_int32)


keep_all = Policies()
unsigned_all = Policies(
    bytes1=TagPolicy.UNSIGNED,
    bytes2=TagPolicy.UNSIGNED,
    bytes3=TagPolicy.UNSIGNED,
    bytes4=TagPolicy.UNSIGNED,
)
signed_all = Policies(
    bytes1=TagPolicy.SIGNED,
    bytes2=TagPolicy.SIGNED,
    bytes3=TagPolicy.SIGNED,
    bytes4=TagPolicy.SIGNED,
)


def as_type_tag(
    dtype,
    policies=keep_all,
):
    if dtype == numpy.complex64:
        return "32fc"
    elif dtype == numpy.complex128:
        return "64fc"
    else:
        ctype_type = numpy.ctypeslib.as_ctypes_type(dtype)
        for (policy, ctype_ref_u, ctype_ref_s, _ctype_ref_down) in (
            policies.bytes1,
            policies.bytes2,
            policies.bytes3,
            policies.bytes4,
        ):
            if ctype_type == ctype_ref_u:
                if policy in (TagPolicy.KEEP, TagPolicy.UNSIGNED):
                    return "{}u".format(8 * numpy.dtype(ctype_ref_u).itemsize)
                elif policy == TagPolicy.SIGNED:
                    return "{}s".format(8 * numpy.dtype(ctype_ref_u).itemsize)
                if policy in (TagPolicy.DOWN_KEEP, TagPolicy.DOWN_UNSIGNED):
                    return "{}u".format(4 * numpy.dtype(ctype_ref_u).itemsize)
                elif policy == TagPolicy.DOWN_SIGNED:
                    return "{}s".format(4 * numpy.dtype(ctype_ref_u).itemsize)
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
            if ctype_type == ctype_ref_s:
                if policy in (TagPolicy.KEEP, TagPolicy.SIGNED):
                    return "{}s".format(8 * numpy.dtype(ctype_ref_s).itemsize)
                elif policy == TagPolicy.UNSIGNED:
                    return "{}u".format(8 * numpy.dtype(ctype_ref_s).itemsize)
                if policy in (TagPolicy.DOWN_KEEP, TagPolicy.DOWN_SIGNED):
                    return "{}s".format(4 * numpy.dtype(ctype_ref_u).itemsize)
                elif policy == TagPolicy.DOWN_UNSIGNED:
                    return "{}u".format(4 * numpy.dtype(ctype_ref_u).itemsize)
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
        if ctype_type == numpy.ctypeslib.as_ctypes_type(
            numpy.dtype(ctypes.c_float)
        ):
            return "32f"
        elif ctype_type == numpy.ctypeslib.as_ctypes_type(
            numpy.dtype(ctypes.c_double)
        ):
            return "64f"
        else:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError, "Unknown dtype: {}".format(dtype), name=__name__
            )


def as_ctype_str(
    dtype,
    policies=keep_all,
):
    if dtype == numpy.complex64:
        return "float complex"
    elif dtype == numpy.complex128:
        return "double complex"
    else:
        ctype_type = numpy.ctypeslib.as_ctypes_type(dtype)
        for (policy, ctype_ref_u, ctype_ref_s, ctype_ref_down) in (
            policies.bytes1,
            policies.bytes2,
            policies.bytes3,
            policies.bytes4,
        ):
            ctype_ref_name = ctype_ref_s.__name__[2:]
            if ctype_ref_down is not None:
                ctype_ref_down_name = ctype_ref_down.__name__[2:]
                if ctype_ref_down_name == "byte":
                    ctype_ref_down_name = "char"
            if ctype_ref_name == "byte":
                ctype_ref_name = "char"
            if ctype_type == ctype_ref_u:
                if policy in (TagPolicy.KEEP, TagPolicy.UNSIGNED):
                    return "unsigned {}".format(ctype_ref_name)
                elif policy == TagPolicy.SIGNED:
                    return ctype_ref_name
                if policy in (TagPolicy.DOWN_KEEP, TagPolicy.DOWN_UNSIGNED):
                    return "unsigned {}".format(ctype_ref_down_name)
                elif policy == TagPolicy.DOWN_SIGNED:
                    return ctype_ref_down_name
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
            if ctype_type == ctype_ref_s:
                if policy in (TagPolicy.KEEP, TagPolicy.SIGNED):
                    return ctype_ref_name
                elif policy == TagPolicy.UNSIGNED:
                    return "unsigned {}".format(ctype_ref_name)
                if policy in (TagPolicy.DOWN_KEEP, TagPolicy.DOWN_SIGNED):
                    return ctype_ref_down_name
                elif policy == TagPolicy.DOWN_UNSIGNED:
                    return "unsigned {}".format(ctype_ref_down_name)
                else:
                    numpy_ipps._detail.debug.log_and_raise(
                        RuntimeError,
                        "Unknown policy for {} : {}".format(dtype, policy),
                        name=__name__,
                    )
        if ctype_type == numpy.ctypeslib.as_ctypes_type(
            numpy.dtype(ctypes.c_float)
        ):
            return "float"
        elif ctype_type == numpy.ctypeslib.as_ctypes_type(
            numpy.dtype(ctypes.c_double)
        ):
            return "double"
        else:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError, "Unknown dtype: {}".format(dtype), name=__name__
            )


def ipps_function(name, signature, *args, policies=keep_all):
    name_split = name.split("_")
    function_name = "ipps{}".format(
        "_".join(
            name_split[:1]
            + [as_type_tag(arg, policies=policies) for arg in args]
            + name_split[1:]
        )
    )

    if not hasattr(numpy_ipps._detail.libipp.ipp_signal, function_name):
        func_signature = "int {}({});".format(
            function_name, ",".join(signature)
        )
        numpy_ipps._detail.libipp.ffi.cdef(func_signature)
        if hasattr(numpy_ipps._detail.libipp.ipp_signal, function_name):
            logging.getLogger(__name__).info(
                "CFFI: Register [ {} ]".format(func_signature)
            )
        else:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "CFFI: Register [ {} ] FAILED".format(func_signature),
                name=__name__,
            )

    return numpy_ipps._detail.libipp.ipp_signal.__getattr__(function_name)
