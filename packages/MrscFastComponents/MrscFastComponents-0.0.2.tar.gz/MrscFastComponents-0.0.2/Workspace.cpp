#include "Workspace.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;

Workspace::Workspace(int m, int n, double l)
{
	this->grid_length = l;
	Vertex v;
	Vector2d c;

	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
			int id = i * m + j;
			v = Vertex(id);
			c = Vector2d(i, j);
			graph.insert(v);
			z[v] = c;
			z_inv[c] = v;
		}
	}

	for (auto v : graph.vertices) {

		c = (*this)[v];
		auto c_up = Vector2d(c.x, c.y + 1);
		auto c_down = Vector2d(c.x, c.y - 1);
		auto c_left = Vector2d(c.x - 1, c.y);
		auto c_right = Vector2d(c.x + 1, c.y);
		Edge e;

		try {
			auto v1 = (*this)[c_up];
			e = Edge(v, v1);
			graph.insert(e);
		}
		catch (py::key_error e) {}

		try {
			auto v1 = (*this)[c_down];
			e = Edge(v, v1);
			graph.insert(e);
		}
		catch (py::key_error e) {}

		try {
			auto v1 = (*this)[c_left];
			e = Edge(v, v1);
			graph.insert(e);
		}
		catch (py::key_error e) {}

		try {
			auto v1 = (*this)[c_right];
			e = Edge(v, v1);
			graph.insert(e);
		}
		catch (py::key_error e) {}
	}
}

Workspace::Workspace()
{
	this->grid_length = 0.6;
}

void Workspace::set_mapping(const Vertex& v, const Vector2d& c)
{
	z[v] = c;
	z_inv[c] = v;
}

void Workspace::set_mapping(const Vector2d& c, const Vertex& v)
{
	this->set_mapping(v, c);
}

Vector2d Workspace::get_cord(const Vertex& v)
{
	if (z.find(v) == z.end()) {
		throw py::key_error(v.to_string());
	}
	return z[v];
}

Vertex Workspace::get_cord_inv(const Vector2d& c)
{
	if (z_inv.find(c) == z_inv.end()) {
		throw py::key_error(c.to_string());
	}
	return z_inv[c];
}

Vertex Workspace::operator[](const Vector2d& c)
{
	return this->get_cord_inv(c);
}

Vector2d Workspace::operator[](const Vertex& v)
{
	return this->get_cord(v);
}

Vertex Workspace::operator[](const PythonTuple& c)
{
	return this->get_cord_inv(Vector2d(c.first, c.second));
}

void Workspace::set_mapping(const PythonTuple& c, const Vertex& v)
{
	this->set_mapping(Vector2d(c.first, c.second), v);
}

void Workspace::set_mapping(const Vertex& v, const PythonTuple& c)
{
	this->set_mapping(v, Vector2d(c.first, c.second));
}
