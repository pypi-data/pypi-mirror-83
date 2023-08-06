import json
import os

import numpy
import pylab


base_path = os.path.join(
    "log", "Linux-CPython-{}-64bit".format(os.environ["PYTHONVERSION"])
)
results = dict()
for counter in ["0001", "0002"]:
    try:
        with open(
            os.path.join(
                base_path,
                "{}_benchmark_py{}_{}.json".format(
                    counter,
                    os.environ["PYTHONVERSION"].replace(".", ""),
                    os.environ["PYTHONUPDATE"],
                ),
            )
        ) as json_file:
            for stats in json.load(json_file)["benchmarks"]:
                try:
                    pkg, fun = stats["name"].split("[", 1)[0].split("_")[1:]
                    ptype, porder = stats["param"].split("-")
                except BaseException:
                    continue
                if pkg not in results:
                    results[pkg] = dict()
                if fun not in results[pkg]:
                    results[pkg][fun] = dict()
                if ptype not in results[pkg][fun]:
                    results[pkg][fun][ptype] = dict()
                if porder not in results[pkg][fun][ptype]:
                    results[pkg][fun][ptype][porder] = stats["stats"]["ops"]
    except BaseException:
        continue

    if "fallback" in results:
        for fun in results["fallback"].keys():
            fig = pylab.figure(figsize=(8.25, 11.75))

            ax_ipps, ax_numpy, ax_relative = fig.subplots(3, 1)

            for ptype in results["ipps"][fun].keys():
                data_ipps = numpy.asarray(
                    [
                        [int(k), results["ipps"][fun][ptype][k]]
                        for k in results["ipps"][fun][ptype].keys()
                    ]
                )
                ax_ipps.plot(
                    data_ipps[:, 0], data_ipps[:, 1] * 1e-6, "o-.", label=ptype
                )
                data_numpy = numpy.asarray(
                    [
                        [int(k), results["fallback"][fun][ptype][k]]
                        for k in results["ipps"][fun][ptype].keys()
                    ]
                )
                ax_numpy.plot(
                    data_numpy[:, 0],
                    data_numpy[:, 1] * 1e-6,
                    "x-.",
                    label=ptype,
                )
                ax_relative.plot(
                    data_ipps[:, 0],
                    100 * (data_ipps[:, 1] / data_numpy[:, 1] - 1),
                    "d-.",
                    label=ptype,
                )

            ax_numpy.legend(loc="upper right")
            ax_relative.set_xlabel("Order")

            ax_ipps.set_ylabel("MOPS")
            ax_numpy.set_ylabel("MOPS")
            ax_relative.set_ylabel("IPP vs Numpy (%)")

            fig.savefig(
                os.path.join(base_path, "{}{}.svg".format(fun, counter))
            )
