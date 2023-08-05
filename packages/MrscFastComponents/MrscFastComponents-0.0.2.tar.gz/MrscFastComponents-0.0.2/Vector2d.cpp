#include "Vector2d.h"

Vector2d::Vector2d()
{
	this->x = INFINITY;
	this->y = INFINITY;
}

Vector2d::Vector2d(double x, double y)
{
	this->x = x;
	this->y = y;
} 

Vector2d Vector2d::operator + (const Vector2d& v) const
{ 
	return Vector2d(this->x + v.x, this->y + v.y); 
};

Vector2d Vector2d::operator - (const Vector2d& v) const
{ 
	return Vector2d(this->x - v.x, this->y - v.y); 
};

Vector2d& Vector2d::operator += (const Vector2d& v) 
{ 
	this->x += v.x; this->y += v.y; return *this; 
};

Vector2d& Vector2d::operator -= (const Vector2d& v) 
{ 
	this->x -= v.x; this->y -= v.y; return *this; 
};

bool Vector2d::operator == (const Vector2d& v) const 
{ 
	return v.x == this->x && v.y == this->y; 
};

Vector2d Vector2d::operator >> (const Vector2d& v) const 
{ 
	return Vector2d(v.x - this->x, v.y - this->y); 
};

Vector2d Vector2d::operator << (const Vector2d& v) const 
{ 
	return Vector2d(this->x - v.x, this->y - v.y); 
}
bool Vector2d::operator<(const Vector2d& v) const
{
	if (this->x < v.x) return true;
	if (this->x > v.x) return false;
	return this->y < v.y;
}

string Vector2d::to_string() const 
{ 
	return "<Vector2d: " + std::to_string(x) + ", " + std::to_string(y) + ">"; 
}

Vector2d Vector2d::getUnitVector() const
{
	double norm = sqrt((this->x * this->x) + (this->y * this->y));
	return Vector2d(this->x / norm, this->y / norm);
}

double Vector2d::getAngleDf(const Vector2d& v) const
{
	auto u = this->getUnitVector();
	auto w = v.getUnitVector();
	return acos(u.x * w.x + u.y * w.y);
}

//double Vector2d::getAngleDf(const Vector2d&& v) const
//{
//	auto u = this->getUnitVector();
//	auto w = v.getUnitVector();
//	return acos(u.x * w.x + u.y * w.y);
//}

double GetAngleDf(const Vector2d&& v1, const Vector2d&& v2)
{
	auto u = v1.getUnitVector();
	auto w = v2.getUnitVector();
	return acos(u.x * w.x + u.y * w.y);
}
