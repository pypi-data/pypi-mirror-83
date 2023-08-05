import argparse
from sys import version_info

import gmsh
import meshplex
import meshio
import numpy
import termplotlib
from .__about__ import __version__, __gmsh_version__


def optimize(argv=None):
    parser = argparse.ArgumentParser(
        description=("Optimize mesh."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("infile", type=str, help="mesh to optimize")
    parser.add_argument("outfile", type=str, help="optimized mesh")

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=_get_version_text(),
        help="display version information",
    )
    args = parser.parse_args(argv)

    mesh = meshio.read(args.infile)
    mesh.remove_lower_dimensional_cells()
    mesh.cell_data = {}

    meshplex_mesh = meshplex.from_meshio(mesh)
    print_stats(meshplex_mesh)

    # optimize
    tmp_filename = "tmp.msh"
    mesh.write(tmp_filename)
    gmsh.initialize()
    gmsh.model.add("Mesh from file")
    gmsh.merge(tmp_filename)
    gmsh.model.mesh.optimize("Netgen")
    gmsh.write(tmp_filename)
    gmsh.finalize()
    mesh = meshio.read(tmp_filename)
    mesh.write(args.outfile)
    return


def _get_version_text():
    return "\n".join(
        [
            f"pygmsh {__version__} "
            f"[Gmsh {__gmsh_version__}, "
            f"Python {version_info.major}.{version_info.minor}.{version_info.micro}]",
            "Copyright (c) 2013-2020 Nico Schlömer et al.",
        ]
    )


def print_stats(mesh, extra_cols=None):
    extra_cols = [] if extra_cols is None else extra_cols

    # angles = mesh.angles / numpy.pi * 180
    # angles_hist, angles_bin_edges = numpy.histogram(
    #     angles, bins=numpy.linspace(0.0, 180.0, num=73, endpoint=True)
    # )

    q = mesh.q_radius_ratio
    q_hist, q_bin_edges = numpy.histogram(
        q, bins=numpy.linspace(0.0, 1.0, num=41, endpoint=True)
    )
    print(q_hist)

    grid = termplotlib.subplot_grid(
        (1, 4 + len(extra_cols)), column_widths=None, border_style=None
    )
    # grid[0, 0].hist(angles_hist, angles_bin_edges, grid=[24], bar_width=1, strip=True)
    # grid[0, 1].aprint("min angle:     {:7.3f}".format(numpy.min(angles)))
    # grid[0, 1].aprint("avg angle:     {:7.3f}".format(60))
    # grid[0, 1].aprint("max angle:     {:7.3f}".format(numpy.max(angles)))
    # grid[0, 1].aprint("std dev angle: {:7.3f}".format(numpy.std(angles)))
    grid[0, 2].hist(q_hist, q_bin_edges, bar_width=1, strip=True)
    grid[0, 3].aprint("min quality: {:5.3f}".format(numpy.min(q)))
    grid[0, 3].aprint("avg quality: {:5.3f}".format(numpy.average(q)))
    grid[0, 3].aprint("max quality: {:5.3f}".format(numpy.max(q)))

    for k, col in enumerate(extra_cols):
        grid[0, 4 + k].aprint(col)

    grid.show()
