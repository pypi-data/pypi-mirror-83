#include "PyInterfaceGraph.h"
#include "pybind11/stl_bind.h"
#include <set>

void bindGraph(py::module& m) {

    py::class_<Graph>(m, "Graph", R"delimiter(

        Directed graph with edges and vertices.

        :var vertices: A readonly-set of vertices.
        :var edges: A readonly-set of edges.

    )delimiter")
        .def(py::init<>())
        .def("insert", py::overload_cast<Edge&>(&Graph::insert),
            R"delimiter(
            This function receives Vertex or Edge as input. The provided input will be added to the corresponding set.
            
            :param item: An instance of Vertex or Edge.
            :type item: Union[Edge, Vertex]

            :Example:
            
            >>> v1 = Vertex(1)
            >>> v2 = Vertex(2)
            >>> v3 = Vertex(3)
            >>> e = Edge(v1, v2)

            >>> g = Graph()
            >>> g.insert(v3)
            >>> g.vertices
            {<Vertex: 3>}

            >>> g.insert(e)
            >>> v1 in g.vertices and v2 in g.vertices and v3 in g.vertices
            True

            >>> g.edges
            {<Edge: 1, 2>}

        )delimiter", "item"_a)

        .def("insert", py::overload_cast<Vertex&>(&Graph::insert))
        .def("remove", py::overload_cast<Edge&>(&Graph::remove),
            R"delimiter(
            This function receives Vertex or Edge as input. The provided input will be removed from the corresponding set.
            Please note that removing a vertex will also remove the edges containing the vertex.
            However, removing an edge does not delete the vertices of the edge.
            
            :param item: An instance of Vertex or Edge.
            :type item: Union[Edge, Vertex]

            :Example:
            
            >>> v1 = Vertex(1)
            >>> v2 = Vertex(2)
            >>> v3 = Vertex(3)
            >>> e = Edge(v1, v2)

            >>> g = Graph()
            >>> g.insert(v3)
            >>> g.insert(e)
            >>> v1 in g.vertices and v2 in g.vertices and v3 in g.vertices and e in g.edges
            True

            >>> g.remove(e)
            >>> e not in g.edges and e.endPointX in g.vertices and e.endPointY in g.vertices 
            True

            >>> g.remove(v3)
            >>> v3 in g.vertices
            False

            >>> g.edges
            set()

        )delimiter", "item"_a)

        .def("remove", py::overload_cast<Vertex&>(&Graph::remove))
        .def("exists", py::overload_cast<Edge&>(&Graph::exists),
            R"delimiter(
            This function receives Vertex or Edge as input. 
            Check if a given input in the graph instance.
            
            :param item: An instance of Vertex or Edge.
            :type item: Union[Edge, Vertex]
            :return: true if the provided input in the graph instance, false otherwise.
            :rtype: bool

            :Example:
            
            >>> from mrscfastcom.workspace import *
            >>> v1 = Vertex(1)
            >>> v2 = Vertex(2)
            >>> v3 = Vertex(3)
            >>> e = Edge(v1, v2)

            >>> g = Graph()
            >>> g.insert(v1)
            >>> g.exists(v1)
            True

            >>> g.exists(v2)
            False

            >>> g.insert(e)
            >>> g.exists(e)
            True
            
            >>> e2 = Edge(v2, v1)
            >>> g.exists(e2)
            False

        )delimiter")

        .def("exists", py::overload_cast<Vertex&>(&Graph::exists))
        .def_readonly("vertices", &Graph::vertices)
        .def_readonly("edges", &Graph::edges)
        .def("get_dt_predecessors", &Graph::get_dt_predecessors, R"delimiter(
            This function is to get the direct predecessors of the input vertex.
            
            :param v: An instance of Vertex.
            :type v: Union[Edge, Vertex]
            :return: A set of predecessors.
            :rtype: Set[Vertex]

            :Example:
            
            >>> v1 = Vertex(1)
            >>> v2 = Vertex(2)
            >>> v3 = Vertex(3)
            >>> e1 = Edge(v1, v2)
            >>> e2 = Edge(v1, v3)
            >>> e3 = Edge(v3, v2)

            >>> g = Graph()
            >>> g.insert(e1)
            >>> g.insert(e2)
            >>> g.insert(e3)

            >>> g.get_dt_predecessors(v1)
            set()
            
            >>> {v1, v3} == g.get_dt_predecessors(v2)
            True

            >>> g.get_dt_predecessors(v3)
            {<Vertex: 1>}

        )delimiter")
        .def("get_dt_successors", &Graph::get_dt_successors, R"delimiter(
            This function is to get the direct successors of the input vertex.
            
            :param v: An instance of Vertex.
            :type v: Union[Edge, Vertex]
            :return: A set of successors.
            :rtype: Set[Vertex]

            :Example:
            
            >>> v1 = Vertex(1)
            >>> v2 = Vertex(2)
            >>> v3 = Vertex(3)
            >>> e1 = Edge(v1, v2)
            >>> e2 = Edge(v1, v3)
            >>> e3 = Edge(v3, v2)

            >>> g = Graph()
            >>> g.insert(e1)
            >>> g.insert(e2)
            >>> g.insert(e3)

            >>> {v2, v3} == g.get_dt_successors(v1)
            True
            
            >>> g.get_dt_successors(v2)
            set()

            >>> g.get_dt_successors(v3)
            {<Vertex: 2>}

        )delimiter");
}