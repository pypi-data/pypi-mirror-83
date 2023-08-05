#include "PyInterfaceEdge.h"

void bindEdge(py::module& m) {

    py::class_<Edge>(m, "Edge", R"delimiter(

        A class with two vertices (endPointX and endPointY). This is to represent directed edge.

        :var endPointX: First endpoint. 
        :type endPointX: Vector2d
        :var endPointY: Second endpoint.
        :type endPointY: Vector2d

    )delimiter")

        .def(py::init<Vertex&, Vertex&>(), R"delimiter(

            Constructor of Edge with two parameters.

            :param Vertex v1: endPointX.
            :param Vertex v2: endPointY.

            :Example:
            
            >>> from mrscfastcom.workspace import *
            >>> v1 = Vertex(1)
            >>> v2 = Vertex(2)
            >>> Edge(v1, v2)
            <Edge: 1, 2>

        )delimiter", "v1"_a, "v2"_a)
        .def_readwrite("endPointX", &Edge::endPointX)
        .def_readwrite("endPointY", &Edge::endPointY)
        .def("__repr__", &Edge::to_string)
        .def("__hash__", &Edge::get_hash)
        .def(py::self == py::self, R"delimiter(

            Two edges e1, e2 are same if e1.endPointX == e2.endPointX and e1.endPointY == e2.endPointY.
            
            :Example:
            
            >>> from mrscfastcom.workspace import *
            >>> v1 = Vertex(1)
            >>> v2 = Vertex(2)
            >>> e1 = Edge(v1, v2)
            >>> e2 = Edge(v2, v1)
            >>> e1 == e2
            False

            >>> e1 == Edge(v1, v2)
            True

        )delimiter");
}
