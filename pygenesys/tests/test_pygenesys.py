from pygenesys import technology
from pygenesys import driver


def test_technology_placeholder_is_none():
    ret_value = technology.placeholder()

    assert(ret_value is None)

    return

def test_name_from_path():
    assert(driver.name_from_path("/Users/test/test.py") == "test")
    assert(driver.name_from_path("/Users/test/test") == "test")
    assert(driver.name_from_path("test.py") == "test")
    assert(driver.name_from_path("~/test.py") == "test")
    assert(driver.name_from_path("~/test") == "test")

    return


def test_name_from_path_has_p():
    assert(driver.name_from_path("/Users/test/testp.py") == "testp")
    assert(driver.name_from_path("testp.py") == "testp")
    assert(driver.name_from_path("~/testp.py") == "testp")
    assert(driver.name_from_path("~/testp") == "testp")

    return
