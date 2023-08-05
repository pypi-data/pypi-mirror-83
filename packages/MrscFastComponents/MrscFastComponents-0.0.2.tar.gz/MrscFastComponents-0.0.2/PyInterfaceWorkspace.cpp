#include "PyInterfaceWorkspace.h"
#include "Workspace.h"

void bindWorkspace(py::module& m) {

    py::class_<Workspace>(m, "Workspace", R"delimiter(

        A class with a Graph instance, grid length and vertices and coordinates one-to-one mapping.

        :var graph: A Graph instance. 
        :type graph: Graph
        :var grid_length: The length of the grids in the workspace. Assume all the grids are square.
        :type grid_length: double

    )delimiter")

        .def(py::init<>())
        .def(py::init<int, int, double>(), R"delimiter(

        There have two constructors: non-arg or :math:`(n, m, l)`. 
        :math:`n \times m` is the number of grids in the workspace and :math:`l` is the length of the grids. 
        Note that all grids are square in shape.
        For the second constructor, all the vertices, edges, and mapping will be created.

        :param n: The number of grids in row.
        :type n: int
        :param m: The number of grids in col.
        :type m: int
        :param l: The length of grids.
        :type l: double
        :rtype: None

        :Example:
        
        >>> from mrscfastcom.workspace import *
        >>> w = Workspace(75, 75, 0.6)
        >>> len(w.graph.vertices)
        5625
        >>> len(w.graph.edges)
        22200
        
    )delimiter", "n"_a, "m"_a, "l"_a)

        .def_readwrite("grid_length", &Workspace::grid_length)
        .def("set_mapping", py::overload_cast<const Vector2d&, const Vertex&>(&Workspace::set_mapping), R"delimiter(

        Set the one-to-one mapping between a coordinate and a vertex. Equivalent with w[v] = c or w[c] = v where w is the instance of Workspace.

        :param v: Target vertex.
        :type v: Vertex
        :param c: Target coordinate.
        :type c: Vector2d
        :rtype: None
        
        :Example:
        
        >>> w = Workspace()
        >>> w.set_mapping(Vertex(1), Vector2d(10, 10))
        >>> w[Vertex(1)]
        <Vector2d: 10.000000, 10.000000>

        >>> w[Vertex(2)] = Vector2d(10, 12)
        >>> w[Vertex(2)]
        <Vector2d: 10.000000, 12.000000>
        
        >>> w[w[Vertex(1)]]
        <Vertex: 1>
         

    )delimiter", "v"_a, "c"_a)

        .def("set_mapping", py::overload_cast<const Vertex&, const Vector2d&>(&Workspace::set_mapping))
        .def("get_cord", &Workspace::get_cord, R"delimiter(

        Get coordinate that map to the given vertex. Equivalent with w[v] where w is the instance of Workspace.

        :param v: Target vertex.
        :type v: Vertex
        :return: The coordinate mapped to the given vertex.
        :rtype: Vector2d
        :raises KeyError: Item doesn't exist.

    )delimiter")

        .def("get_inv_cord", &Workspace::get_cord_inv, R"delimiter(

        Get vertex that map to the given coordinate. Equivalent with w[c] where w is the instance of Workspace.

        :param c: Target coordinate.
        :type c: Vector2d
        :return: The vertex mapped to the given coordinate.
        :rtype: Vertex
        :raises KeyError: Item doesn't exist.

    )delimiter")

        .def_readonly("graph", &Workspace::graph)
        .def("__getitem__", py::overload_cast<const Vector2d&>(&Workspace::operator[]), R"delimiter(

        This operator received Vertex, Vector2d, or 2d-tuple instance as input. 
        If a vertex is provided, then return the coordinate of the vertex (if the mapping exists).
        If a Vector2d or 2d-tuple instance is provided, then return the instance that is mapped to the coordinate. 
        The 2d-tuple will be automatic converted to Vector2d with the corresponding coordinate.
        KeyError will be raised if there have no mapping from the given input.

        :param c: Target coordinate.
        :type c: Vector2d
        :return: The vertex mapped to the given coordinate.
        :rtype: Vertex
        :raises KeyError: Item doesn't exist.
        
        :Example:

        >>> from mrscfastcom.workspace import *
        >>> w = Workspace(75, 75, 0.6)
        
        >>> w[Vector2d(0, 0)]
        <Vertex: 0>
        
        >>> w[(0, 0)] == w[Vector2d(0, 0)]
        True

        >>> w[Vertex(0)]
        <Vector2d: 0.000000, 0.000000>

        >>> try:
        ...     w[Vertex(-1)]
        ... except KeyError:
        ...     print("KeyError")
        KeyError

    )delimiter")

        .def("__getitem__", py::overload_cast<const Vertex&>(&Workspace::operator[]))
        .def("__getitem__", py::overload_cast<const PythonTuple&>(&Workspace::operator[]))
        .def("__setitem__", py::overload_cast<const Vertex&, const Vector2d&>(&Workspace::set_mapping))
        .def("__setitem__", py::overload_cast<const Vector2d& , const Vertex&>(&Workspace::set_mapping))
        .def("__setitem__", py::overload_cast<const PythonTuple&, const Vertex&>(&Workspace::set_mapping))
        .def("__setitem__", py::overload_cast<const Vertex&, const PythonTuple&>(&Workspace::set_mapping));
}