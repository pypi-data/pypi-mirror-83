#include "PyInterfaceVector2d.h"

void bindVector2d(py::module& m) {

    py::class_<Vector2d>(m, "Vector2d", R"delimiter(
        This is a class with two numerical attributes. Its instances have similar properties as mathematical 2d vectors.

        :var x: x-value.
        :type x: double
        :var y: y-value.
        :type y: double

    )delimiter")

        .def(py::init<double, double>(), R"delimiter(
            Constructor.

            :param x: x-value.
            :type x: double
            :param y: y-value.
            :type y: double

            :Example:

            >>> Vector2d(2, 0)
            <Vector2d: 2.000000, 0.000000>

        )delimiter", "x"_a, "y"_a)

        .def_readwrite("x", &Vector2d::x)
        .def_readwrite("y", &Vector2d::y)

        .def("get_unit_vector", &Vector2d::getUnitVector, R"delimiter(
            Calculate and return the unit vector of the caller.

            :rtype: Vector2d

            :Example:

            >>> Vector2d(2, 0).get_unit_vector()
            <Vector2d: 1.000000, 0.000000>

        )delimiter")

        .def("get_angle_df", &Vector2d::getAngleDf, R"delimiter(
            Calculate and return the angle difference between two vectors (in radian).
            
            .. math::
                \theta = cos^{-1} \frac{v_1 \cdot v_2}{|v_1||v_2|}

            :param v: target vector.
            :type v: Vector2d
            :rtype: double

            :Example:
                
            >>> Vector2d(1, 0).get_angle_df(Vector2d(2, 0))
            0.0

            >>> Vector2d(1, 0).get_angle_df(Vector2d(-1, 0))
            3.141592653589793
                
            >>> Vector2d(1, 0).get_angle_df(Vector2d(0, 1))
            1.5707963267948966

            >>> Vector2d(1, 0).get_angle_df(Vector2d(0, -1))
            1.5707963267948966

            >>> Vector2d(1, 0).get_angle_df(Vector2d(1.123, 2.324))
            1.120663750004051

        )delimiter", "v"_a)

        .def(py::self + py::self, R"delimiter(
            Add two vectors and returns the result.
            
            :Example:

            >>> from mrscfastcom.workspace import Vector2d
            >>> Vector2d(1, 2) + Vector2d(5, 3)
            <Vector2d: 6.000000, 5.000000>

        )delimiter", "rhs"_a)

        .def(py::self += py::self, R"delimiter(
            Add two vectors and updates the value of lhs-vector.

            :Example:

            >>> v1 = Vector2d(1, 2)
            >>> v1 += Vector2d(5, 3)
            >>> v1
            <Vector2d: 6.000000, 5.000000>

        )delimiter", "rhs"_a)

        .def(py::self - py::self, R"delimiter(
            lhs-vector subtracts rhs-vector and returns the result.

            :Example:

            >>> Vector2d(1, 2) - Vector2d(5, 3)
            <Vector2d: -4.000000, -1.000000>

        )delimiter", "rhs"_a)

        .def(py::self -= py::self, R"delimiter(
            lhs-vector subtracts rhs-vector and updates the value of lhs-vector.

            :Example:

            >>> v1 = Vector2d(1, 2)
            >>> v1 -= Vector2d(5, 3)
            >>> v1
            <Vector2d: -4.000000, -1.000000>

        )delimiter", "rhs"_a)

        .def(py::self == py::self, R"delimiter(
            Compare two vectors.

            :Example:

            >>> Vector2d(1, 2) == Vector2d(5, 3)
            False

            >>> Vector2d(1, 2) != Vector2d(5, 3)
            True

            >>> Vector2d(1, 2) == Vector2d(1, 2)
            True

        )delimiter", "rhs"_a)

        .def(py::self >> py::self, R"delimiter(
            Equivalent to rhs-vector subtracts lhs-vector (rhs - lhs).

            :Example:

            >>> v1 = Vector2d(1, 2)
            >>> v2 = Vector2d(2, 0)
            >>> v1 >> v2
            <Vector2d: 1.000000, -2.000000>

        )delimiter", "rhs"_a)

        .def(py::self << py::self, R"delimiter(
            Equivalent to lhs-vector subtracts rhs-vector (lhs - rhs).

            :Example:

            >>> v1 = Vector2d(1, 2)
            >>> v2 = Vector2d(2, 0)
            >>> v1 << v2
            <Vector2d: -1.000000, 2.000000>

        )delimiter", "rhs"_a)

        .def("__repr__", &Vector2d::to_string);
}