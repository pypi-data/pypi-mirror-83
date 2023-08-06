#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2D geometry types and operations.

This library has NOTHING to do with pygame. It is a pure math
library and it's place in pygstuff is temporary.

This uses the classic trigonometric functions. I plan to replace
all of that with rational trigonometry. I'll break this out to
its own package at that time. For now this is a helper to make a
higher-level drawing interface for my pygame ray-tracing
applications.
"""

from collections import namedtuple
import math

# -----------------------------------
# | Create points and line segments |
# -----------------------------------

Point = namedtuple('Point', ['x', 'y'])

class PointMath():
    """Define operations on points.

    Notes
    -----
    I originally made :class:`PointMath` in a ``Point`` class, but it
    is more convenient from the caller's perspective to treat Points as
    simple tuples. I had to make the tuple an attribute of the Point
    class, which made the syntax awkwardly redundant.

    Now this is a pure static methods class. No state.
    """

    @staticmethod
    def scale(point:Point, scale:float) -> object:
        """Scale the point.

        Example
        -------
        >>> PointMath.scale(Point(1,2), -1)
        Point(x=-1, y=-2)

        Return
        ------
        object
            Return a Point instance as the scaled point.
        """
        # TODO: use this:
        #   - to calculate the midpoint for LineSegment.midpoint
        return Point(scale*point.x, scale*point.y)

    @staticmethod
    def subtract(A:Point, B:Point) -> object:
        """Return point B-A.

        This only takes two points. Order matters.

        Example
        -------
        Subtract these two points
        >>> A = Point(1,2)
        >>> B = Point(3,4)
        >>> PointMath.subtract(A,B) # B-A (subtract A from B)
        Point(x=2, y=2)
        >>> PointMath.subtract(B,A) # A-B (subtract B from A)
        Point(x=-2, y=-2)

        A LineSegment has two endpoints, subtract those:
        >>> l = LineSegment.from_length(10, angle=45)
        >>> PointMath.subtract(l.endpoints[0], l.endpoints[1])
        Point(x=7.0710678118654755, y=7.0710678118654755)

        Return
        ------
        object
            Return a Point instance as the difference between the two
            points.
        """
        # Scale by -1, then add
        return PointMath.add([B, PointMath.scale(A,-1)])

    @staticmethod
    def add(points:list) -> object:
        """Add the points in the list.

        Works for an arbitrary number of points

        Example
        -------
        >>> p1 = Point(1,2)
        >>> p2 = Point(3,4)
        >>> p3 = Point(5,6)
        >>> PointMath.add([p1,p2,p3])
        Point(x=9, y=12)

        Adding one point just returns the point:
        >>> PointMath.add([p3])
        Point(x=5, y=6)

        Adding only works for Points:
        >>> PointMath.add([1,2])
        Traceback (most recent call last):
        ...
        TypeError: 'int' object is not iterable

        Adding does not work for an empty list:
        >>> PointMath.add([])
        Traceback (most recent call last):
        ...
        ValueError: Point addition is undefined for an empty list.

        Parameters
        ----------
        points
            List of points to add. Each point is type Point (an x,y
            coordinate).

        Return
        ------
        object
            Return a Point instance as the sum of the points.
        """

        # Tell users not to add empty lists
        if len(points) == 0:
            raise ValueError("Point addition is undefined for an empty list.")

        # Get the coordinates of the points
        # coordinates = [point._coordinate for point in points]
        # all_x, all_y = tuple(zip(*coordinates))
        all_x, all_y = tuple(zip(*points))
        return Point( sum(all_x), sum(all_y) )

class LineSegment():
    """Define a line segment.

    This class has multiple initializers.

    The default construction uses the line segment's endpoints.
    The alternative construction ``from_length()`` uses length, midpoint,
    and angle.

    Example
    -------
    Define a line segment by listing its two endpoints:
    >>> l1 = LineSegment([Point(-5.4,0), Point(5.4,0)])

    Access the endpoints:
    >>> print(l1.endpoints)
    (Point(x=-5.4, y=0), Point(x=5.4, y=0))

    The LineSegment also calculates its own length, midpoint, and angle:
    >>> print(l1.length)
    10.8
    >>> print(l1.midpoint)
    Point(x=0.0, y=0.0)
    >>> print(l1.angle)
    0.0

    Define the same line segment by its length:
    >>> l2 = LineSegment.from_length(length=10.8)
    >>> print(l2.endpoints)
    (Point(x=-5.4, y=0.0), Point(x=5.4, y=0.0))

    Optionally specify the midpoint of the line segment:
    >>> l3 = LineSegment.from_length(length=10.8, midpoint=Point(1,1))
    >>> print(l3.endpoints)
    (Point(x=-4.4, y=1.0), Point(x=6.4, y=1.0))

    Optionally specify the angle of the line segment:
    >>> l4 = LineSegment.from_length(12, angle=60)
    >>> print(l4.endpoints)
    (Point(x=-3.000000000000001, y=-5.196152422706632), Point(x=3.000000000000001, y=5.196152422706632))

    This also works for negative angles:
    >>> l5 = LineSegment.from_length(12, angle=-60)
    >>> print(l5.endpoints)
    (Point(x=-3.000000000000001, y=5.196152422706632), Point(x=3.000000000000001, y=-5.196152422706632))
    """

    def __init__(self, endpoints:list):
        """Initialize line segment with its endpoints.

        Parameters
        ----------
        endpoints
            List of two points, e.g., [Point(0,0), Point(1,0)].
            The line segment is the line connecting these two points.
        """
        self.endpoints = tuple(endpoints)

    @classmethod
    def from_length(cls,
        length:float,
        midpoint:Point = Point(0,0),
        angle:float = 0
        ) -> object:
        """Alternative line segment definition by length.

        Parameters
        ----------
        length
            Length of the line segment.
            Units are whatever drawing units the application uses.
        midpoint
            Midpoint of the line segment.
            Default to the origin.
        angle
            Angle of the line segment.
            Default to the horizontal plane (0°).

        Return
        ------
        object
            An instance of LineSegment, as if the user initialized it
            with endpoints instead of length, midpoint, and angle.
        """

        dy = length*math.sin(math.radians(angle))
        dx = length*math.cos(math.radians(angle))

        endpoints = [
            Point(midpoint.x - dx/2, midpoint.y - dy/2),
            Point(midpoint.x + dx/2, midpoint.y + dy/2)
            ]
        return cls(endpoints)

    @property
    def midpoint(self) -> Point:
        """Return the midpoint of the line segment.

        """
        # In general:
        # A + λ( B-A )
        # where A and B are the endpoints
        # Substituting λ = 0.5:
        # midpoint = A + 0.5 B - 0.5 A
        # midpoint = 0.5(A+B)
        psum = PointMath.add(self.endpoints)
        return Point(psum.x/2, psum.y/2)

    @property
    def length(self) -> float:
        """Return the length of the line segment.

        """
        a = self.endpoints[0]
        b = self.endpoints[1]
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

    @property
    def angle(self) -> float:
        """Return the angle (in degrees) of the line segment.

        """
        a = self.endpoints[0]
        b = self.endpoints[1]
        dy = b.y-a.y
        dx = b.x-a.x
        return math.atan(dy/dx)

    # @property
    # def endpoints(self) -> list:
    #     """Return the end points of the line segment

    #     Example
    #     -------
    #     >>> lineseg = LineSegment(midpoint=Point(0,0), width=100)
    #     >>> print(lineseg.endpoints)
    #     (Point(x=-50.0, y=0), Point(x=50.0, y=0))
    #     """
    #     return (
    #         Point(self.midpoint.x - self.width/2, self.midpoint.y),
    #         Point(self.midpoint.x + self.width/2, self.midpoint.y)
    #         )

class Line():
    """A line defined by a point and a slope.

    Example
    -------
    Make a line. The default line is a horizontal through the origin.
    >>> L = Line()
    >>> print(L.point)
    Point(x=0, y=0)
    >>> print(L.slope)
    (1, 0)

    Make a line with a 45° angle.
    >>> L = Line(slope=(1,1))
    >>> print(L.point)
    Point(x=0, y=0)
    >>> print(L.slope)
    (1, 1)

    Parameters
    ----------
    point
        x,y coordinate as tuple (x, y).
        Default is (0,0).
    slope
        Δx and Δy as tuple (Δx, Δy).
        Default is (1,0) (a horizontal line).

    Notes
    -----
    There are many several ways to encode a line.

    There is the Cartesian form:

        ax + by = c     <------ (a,b,c are scalars)

    There is the parameteric form:

        A + λ( Δx, Δy ) <------ (A is a point, λ is a scalar)

    And combining the above two forms, here is what I call
    *the Cartesian form with parameteric coefficients*:

        (Δx)y - (Δy)x = (Δx)Ay - (Δy)Ax

    This is ``ax + by = c`` where:

        a = -Δy
        b = Δx
        c = (Δx)Ay - (Δy)Ax

    The point (Ax, Ay) is always known since at least one point is always specified
    in all types of geometric objects.

    Give a point and a slope, insert values for (Ax, Ay) and (Δx, Δy).

    (Δx)y - (Δy)x = (Δx)Ay - (Δy)Ax

    - (Ax,Ay) is the given point
    - (Δx,Δy) is the given slope

    """
    def __init__(self,
                point:Point = Point(0,0),
                slope:tuple = (1,0)
                ):
        self.point = point
        self.slope = slope

    def meet(self, lineseg:LineSegment) -> object:
        """Find the point where this line intersects the line segment.

        Example
        -------
        A 45° line passing through the origin
        >>> L = Line(slope=(1,1))

        A -45° line segment, also passing through the origin
        >>> seg = LineSegment.from_length(2, angle=-45)

        Of course they meet at the origin
        >>> L.meet(seg)
        Point(x=0.0, y=0.0)

        Here is a different line segment
        >>> seg = LineSegment([Point(-1,2), Point(5,1)])

        Find where the line meets this line segment:
        >>> L.meet(seg)
        Point(x=1.5714285714285714, y=1.5714285714285714)

        Return
        ------
        object
            An instance of Point. The intersection point.
        """

        # rename inputs that define the line
        dx=self.slope[0]; dy=self.slope[1]; A=self.point
        
        # (Δx)y - (Δy)x = (Δx)Ay - (Δy)Ax
        #     ax +    by = k1 # EQN1
        # (-Δy)x + (Δx)y = (Δx)Ay - (Δy)Ax
        a = -dy; b = dx; k1 = dx*A.y - dy*A.x

        d = PointMath.subtract(lineseg.endpoints[0], lineseg.endpoints[1])
        dx = d.x; dy = d.y; A = lineseg.endpoints[0]
        #    cx  +    dy = k2 # EQN2
        # (-Δy)x + (Δx)y = (Δx)Ay - (Δy)Ax
        c = -dy; d = dx; k2 = dx*A.y - dy*A.x

        # Combine EQN1 and EQN2 to eliminate x
        # a*EQN2 - c*EQN1
        #  acx + ady =  ak2
        # -acx - bcy = -ck1
        #   0x + (ad-bc)y = ak2-ck1
        #   y = (a/det)k2 - (c/det)k1

        # Combine EQN1 and EQN2 to eliminate y
        # d*EQN1 - b*EQN2
        #       adx + bdy =  dk1
        #      -bcx - bdy = -bk2
        #  (ad-bc)x + 0y = dk1-bk2
        #  x = (d/det)k1 - (b/det)k2

        det = a*d - b*c

        x = ( d/det)*k1  + (-b/det)*k2
        y = (-c/det)*k1  + ( a/det)*k2

        return Point(x,y)

