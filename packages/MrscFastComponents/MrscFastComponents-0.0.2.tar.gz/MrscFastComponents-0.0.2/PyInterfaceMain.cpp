#pragma once
#include <pybind11/stl.h>
#include "Vector2d.h"
#include "pybind11/pybind11.h"
#include <pybind11/operators.h>
#include "PyInterfaceVector2d.h"
#include "PyInterfaceEdge.h"
#include "PyInterfaceVertex.h"
#include "PyInterfaceGraph.h"
#include "pybind11/stl_bind.h"
#include "PyInterfaceWorkspace.h"

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(mrscfastcom, m) {

    py::options options;
    options.disable_function_signatures();

    m.doc() = "Fast Multi-Robot Sorting Centers Components for Prototyping.";
    py::module m1 = m.def_submodule("workspace", "Workspace - The Lowest-Level Environmental Layout.");

    bindVector2d(m1);
    bindVertex(m1);
    bindEdge(m1); 
    bindGraph(m1);
    bindWorkspace(m1);
}