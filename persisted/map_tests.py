""" Tests for persisted_map.Map """

from persisted_map import Map

def test_init_new():
    """ Tests initialization of brand new map. """
    pass

def test_init_existing():
    """ Tests initialization of a log from a previous map's backing file. """
    pass

def test_init_corrupted():
    """ Tests initialization of a map from a badly formatted file. """
    pass

def test_put_and_get():
    """ Tests that we can put key / value pairs in and query them with get. """
    pass

def test_delete():
    """ Tests that elements are removed by the delete method. """
    pass

def test_size():
    """ Tests that the size method returns the proper result. """
    pass

test_init_new()
test_init_existing()
test_init_corrupted()
test_put_and_get()
test_delete()
test_size()
print "All tests passed!"
