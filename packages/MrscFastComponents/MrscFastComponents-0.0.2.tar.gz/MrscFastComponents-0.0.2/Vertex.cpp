#include "Vertex.h"

Vertex::Vertex()
{
	this->id = -1;
}

Vertex::Vertex(int id)
{
	this->id = id;
}

bool Vertex::operator==(const Vertex& v) const
{
	return v.id == this->id;
}

void Vertex::operator=(const Vertex& v)
{
	this->id = v.get_id();
}

bool Vertex::operator<(const Vertex& v) const
{
	return this->id < v.id;
}

int Vertex::get_id() const
{
	return this->id;
}

string Vertex::to_string() const 
{
	return "<Vertex: " + std::to_string(this->get_id()) + ">";
}

std::size_t Vertex::get_hash()
{
	return this->id;
}

std::size_t Vertex::HashFunction::operator()(const Vertex& k) const
{
	return k.id;
}
