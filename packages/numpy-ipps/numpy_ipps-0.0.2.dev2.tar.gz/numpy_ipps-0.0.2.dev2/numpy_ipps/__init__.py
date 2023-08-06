"""Numpy Intel IPP signal."""

import logging

from pkg_resources import get_distribution

import numpy_ipps._detail.debug
import numpy_ipps._detail.libipp
import numpy_ipps.support


__version__ = get_distribution(__name__).version

__title__ = "numpy_ipps"
__description__ = "Numpy Intel IPP signal."
__uri__ = "https://gitlab.com/fblanchet/numpy_ipps"

__author__ = "Florian Blanchet"
__email__ = "florian.blanchet@supoptique.org"
__license__ = "Apache Software License"
__copyright__ = "2020 Florian Blanchet"

__all__ = ["__version__"]


status = numpy_ipps._detail.libipp.ipp_signal.ippInit()
numpy_ipps._detail.debug.assert_status(status, message="Init", name=__name__)

logging.getLogger(__name__).info(
    "Intel IPP signal version {5} [{6}] for CPU target: {3}.".format(
        *numpy_ipps._detail.debug.safe_call(numpy_ipps.support.library_version)
    )
)

logging.getLogger(__name__).info(
    "CPU frequency: {:.3f} GHz.".format(
        numpy_ipps._detail.debug.safe_call(numpy_ipps.support.cpu_frequency)
        * 1e-9
    )
)

logging.getLogger(__name__).info("CPU cache information:")
for cache_type, cache_level, cache_size in numpy_ipps._detail.debug.safe_call(
    numpy_ipps.support.cache_params
):
    logging.getLogger(__name__).info(
        "\tL{} {} cache: {:.3f} MB".format(
            cache_level, cache_type, cache_size * 1e-6
        )
    )

logging.getLogger(__name__).info("CPU features:")
for feature in sorted(
    numpy_ipps._detail.debug.safe_call(numpy_ipps.support.cpu_features)
):
    logging.getLogger(__name__).info("\t{}".format(feature))
