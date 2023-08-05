#pragma once
#include "PyInterfaceVertex.h"

void bindVertex(py::module& m) {

    py::class_<Vertex>(m, "Vertex", R"delimiter(
       This a class to generate vertices with immutable unique identifiers (id).  

       :var id: The unique identifier of instance. Vertices with same id are considered identical. 
       :type id: unsigned int

    )delimiter")

        .def_property_readonly("id", &Vertex::get_id)
        .def(py::init<int>(), R"delimiter(

            Constructor of vertex. The id of any vertex should be a nonnegative int.

            :param id: The custom unique identifier of the vertex.
            :type id: unsigned int

            :Example:

            >>> Vertex(1)
            <Vertex: 1>

        )delimiter", "id"_a)
        .def("__repr__", &Vertex::to_string)
        .def(py::self == py::self, R"delimiter(
            
            Two vertices are considered identical if they both have the same id.
            
            :Example:

            >>> from mrscfastcom.workspace import *
            >>> v1 = Vertex(1)
            >>> v2 = Vertex(v1.id)
            >>> v1 == v2
            True

            >>> v3 = Vertex(2)
            >>> v1 == v3
            False

        )delimiter")
        .def("__hash__", &Vertex::get_hash);
}
