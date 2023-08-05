#include "Graph.h"

bool Graph::exists(Edge& e)
{
	return this->edges.find(e) != this->edges.end();
}

bool Graph::exists(Vertex& v)
{
	return this->vertices.find(v) != this->vertices.end();
}

void Graph::insert(Edge& e)
{
	this->edges.insert(e);
	this->vertices.insert(e.endPointX);
	this->vertices.insert(e.endPointY);

	this->edges_in_map[e.endPointX].insert(e.endPointY);
	this->inv_edges_in_map[e.endPointY].insert(e.endPointX);
	this->left_vertex_incident_edges[e.endPointX].insert(e);
	this->right_vertex_incident_edges[e.endPointY].insert(e);
}

void Graph::insert(Vertex& v)
{
	this->vertices.insert(v);
}

void Graph::insert(Edge&& e)
{
	this->edges.insert(e);
	this->vertices.insert(e.endPointX);
	this->vertices.insert(e.endPointY);

	this->edges_in_map[e.endPointX].insert(e.endPointY);
	this->inv_edges_in_map[e.endPointY].insert(e.endPointX);
	this->left_vertex_incident_edges[e.endPointX].insert(e);
	this->right_vertex_incident_edges[e.endPointY].insert(e);
}

void Graph::insert(Vertex&& v)
{
	this->vertices.insert(v);
}

void Graph::remove(Vertex& v)
{
	vector<Edge> edges_to_remove;

	auto it = this->edges_in_map.find(v);
	if (it != this->edges_in_map.end()) {
		for (auto it_inner = (*it).second.begin(); it_inner != (*it).second.end(); it_inner++) {
			edges_to_remove.push_back(Edge(v, *it_inner));
			this->inv_edges_in_map.find(*it_inner)->second.erase(v);
		}
		this->edges_in_map.erase(v);
	}

	for (auto e : edges_to_remove) {
		this->edges.erase(e);
	}

	this->vertices.erase(v);
}

void Graph::remove(Edge& e)
{
	auto it = this->edges_in_map.find(e.endPointX);

	if (it != this->edges_in_map.end())
		(*it).second.erase(e.endPointY);

	it = this->inv_edges_in_map.find(e.endPointY);

	if (it != this->inv_edges_in_map.end())
		(*it).second.erase(e.endPointX);

	this->edges.erase(e);
}

set<Vertex> Graph::get_dt_successors(const Vertex& v) const
{
	auto it = this->edges_in_map.find(v);

	if (it == this->edges_in_map.end())
		return set<Vertex>();
	else
		return (*it).second;
}

set<Vertex> Graph::get_dt_predecessors(const Vertex& v) const 
{

	auto it = this->inv_edges_in_map.find(v);

	if (it == this->inv_edges_in_map.end())
		return set<Vertex>();
	else
		return (*it).second;
}

//set<Edge> Graph::get_edges() const 
//{
//	return this->edges;
//}
//
//set<Vertex> Graph::get_vertices() const 
//{
//	return this->vertices;
//}
