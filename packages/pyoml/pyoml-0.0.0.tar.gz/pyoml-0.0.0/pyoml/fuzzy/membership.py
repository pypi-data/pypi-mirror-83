# Authors: Murilo Camargos <murilo.camargosf@gmail.com>
# License: MIT

__all__ = [
    'TriMF',
]

class TriMF:
    """Triangular membership function.

    Parameters
    ----------
    p1 : float
        First parameter to control the triangular shape.

    p2 : float
        Second parameter to control the triangular shape.

    p3 : float
        Third parameter to control the triangular shape.

    Attributes
    ----------
    a_ : float
        Triangular shape lower bound.

    b_ : float
        Triangular shape mid point.

    c_ : float
        Triangular shape upper bound.
    
    Examples
    --------
    >>> from pyoml.fuzzy.membership import TriMF
    >>> mf = TriMF(0,1,2)
    """
    def __init__(self, p1: float, p2: float, p3: float):
        p = sorted([p1, p2, p3])
        self.a_ = p[0]
        self.b_ = p[1]
        self.c_ = p[2]

    def get_params(self):
        """Get the triangular form's parameters.

        Returns
        -------
        params : tuple(float, float, float)
            Ordered triangular three parameters (a,b,c).
        """
        params = (self.a_, self.b_, self.c_)
        return params
    
    def get_degree(self, x: float):
        """Get the membership degree of a float value `x` for
        the triangular MF.

        Parameters
        ----------
        x : float
            Input data for which the membership degree will be
            computed.
        
        Returns
        -------
        degree : float 
            The membership degree for the input `x`. The value
            is in [0, 1].
        """
        degree = max(min((x - self.a_)/(self.b_ - self.a_),\
            (self.c_ - x)/(self.c_ - self.b_)), 0)
        return degree