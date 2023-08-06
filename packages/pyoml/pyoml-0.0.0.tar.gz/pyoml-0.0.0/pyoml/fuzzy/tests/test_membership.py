from pyoml.fuzzy.membership import TriMF

def test_trimf_set_abc_params():
    # Test getting/setting the parameters of the Triangular MF
    mf = TriMF(2,1,0)
    assert mf.get_params() == (0,1,2)

def test_trimf_get_membership_degree():
    # Test getting/setting the parameters of the Triangular MF
    mf = TriMF(2,1,0)
    assert mf.get_degree(-0.5) == 0
    assert mf.get_degree(0) == 0
    assert mf.get_degree(0.5) == 0.5
    assert mf.get_degree(1) == 1
    assert mf.get_degree(1.5) == 0.5
    assert mf.get_degree(2) == 0
    assert mf.get_degree(2.5) == 0