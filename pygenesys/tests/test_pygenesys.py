from pygenesys import technology


def test_technology_placeholder():
    """
    Tests the placeholder function in
    pygenesys.technology
    """

    ret_value = technology.placeholder()

    assert(ret_value is None)

    return
