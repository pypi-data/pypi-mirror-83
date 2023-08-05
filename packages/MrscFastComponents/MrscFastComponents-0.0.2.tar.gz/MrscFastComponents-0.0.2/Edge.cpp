#include "Edge.h"

std::size_t Edge::HashFunction::operator()(const Edge& k) const
{
	return ((long long)k.endPointX.id + 1) << 32 | ((long long)k.endPointY.id + 1);
}

string Edge::to_string()
{
	return "<Edge: " + std::to_string(endPointX.get_id()) + ", " + std::to_string(endPointY.get_id()) + ">";
}

size_t Edge::get_hash()
{
	return ((long long)this->endPointX.id + 1) << 32 | ((long long)this->endPointY.id + 1);
}

bool Edge::operator<(const Edge& e) const
{
	if (e.endPointX.id == this->endPointX.id)
		return this->endPointY.id < e.endPointY.id;

	return this->endPointX.id < e.endPointX.id;
}

Edge::Edge() {}

Edge::Edge(const Vertex& v1, const Vertex& v2)
{
	this->endPointX = v1;
	this->endPointY = v2;
}

bool Edge::operator==(const Edge& e) const
{
	return this->endPointX == e.endPointX && this->endPointY == e.endPointY;
}