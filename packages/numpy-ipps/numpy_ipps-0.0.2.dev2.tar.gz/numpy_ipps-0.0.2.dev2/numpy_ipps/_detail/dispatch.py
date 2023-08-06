import ctypes

import numpy
import numpy.ctypeslib

import numpy_ipps._detail.debug
import numpy_ipps._detail.libipp


def as_type_tag(dtype):
    if dtype == numpy.complex64:
        return "32fc"
    elif dtype == numpy.complex128:
        return "64fc"
    else:
        ctype_type = numpy.ctypeslib.as_ctypes_type(dtype)
        if ctype_type in (
            numpy.ctypeslib.as_ctypes_type(numpy.dtype(ctypes.c_uint8)),
            numpy.ctypeslib.as_ctypes_type(numpy.dtype(ctypes.c_int8)),
        ):
            return "8u"
        elif ctype_type in (
            numpy.ctypeslib.as_ctypes_type(numpy.dtype(ctypes.c_uint16)),
            numpy.ctypeslib.as_ctypes_type(numpy.dtype(ctypes.c_int16)),
        ):
            return "16s"
        elif ctype_type in (
            numpy.ctypeslib.as_ctypes_type(numpy.dtype(ctypes.c_uint32)),
            numpy.ctypeslib.as_ctypes_type(numpy.dtype(ctypes.c_int32)),
        ):
            return "32s"
        elif ctype_type == numpy.ctypeslib.as_ctypes_type(
            numpy.dtype(ctypes.c_float)
        ):
            return "32f"
        elif ctype_type in (
            numpy.ctypeslib.as_ctypes_type(numpy.dtype(ctypes.c_uint64)),
            numpy.ctypeslib.as_ctypes_type(numpy.dtype(ctypes.c_int64)),
        ):
            return "64s"
        elif ctype_type == numpy.ctypeslib.as_ctypes_type(
            numpy.dtype(ctypes.c_double)
        ):
            return "64f"
        else:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError, "Unknown dtype: {}".format(dtype), name=__name__
            )


def ipps_function(name, signature, *args):
    if len(args) > 0:
        function_name = "ipps{}_{}".format(
            name, "".join(as_type_tag(arg) for arg in args)
        )
    else:
        function_name = "ipps{}".format(name)
    if not hasattr(numpy_ipps._detail.libipp.ipp_signal, function_name):
        numpy_ipps._detail.libipp.ffi.cdef(
            "int {}({});".format(function_name, ",".join(signature))
        )
    return numpy_ipps._detail.libipp.ipp_signal.__getattr__(function_name)
