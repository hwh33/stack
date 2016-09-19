""" Tests for persisted_list.List """

import tempfile
from persisted_list import List

def test_init_new():
    """ Tests initialization of brand new list.

    We return the list created for use in other tests.

    """
    return List(tempfile.NamedTemporaryFile().name)

def test_init_existing():
    """ Tests initialization of a list from a previous list's backing file.

    We return the list for use in other tests.

    """
    # First save some stuff so we have something to load.
    existing_list = test_init_new()
    existing_list.append(1)
    existing_list.append(2)
    existing_list.append("to be deleted")
    existing_list.append("boo")
    del existing_list[2]
    newly_loaded_list = List(existing_list._log._backing_file)
    assert len(newly_loaded_list) == len(existing_list)
    for index in range(0, len(existing_list)):
        assert newly_loaded_list[index] == existing_list[index]
    return newly_loaded_list

def test_init_corrupted():
    """ Tests initialization of a list from a badly formatted file. """
    # Copy the log file then corrupt it by adding a bad line.
    existing_list = test_init_existing()
    # Sanity check (we're putting the bad data between the 1st and 2nd line).
    assert len(open(existing_list._log._backing_file).readlines()) > 1
    copied_backing_file = tempfile.NamedTemporaryFile()
    bad_line_written = False
    for line in open(existing_list._log._backing_file).readlines():
        copied_backing_file.write(line + "\n")
        if not bad_line_written:
            copied_backing_file.write("ooga booga I'm corrupted data")
            bad_line_written = True
    copied_backing_file.flush()
    try:
        List(copied_backing_file.name)
    except ValueError:
        # This is what we expected - success.
        return
    raise Exception("Init call on corrupted file should have failed")

def test_append_and_get():
    """ Tests that elements can be appended and retrieved with get. """
    pass

def test_push_and_pop():
    """ Tests that elements can be pushed and then popped. """
    pass

def test_index():
    """ Tests that the index method returns correct values. """
    pass

def test_remove():
    """ Tests that the remove method truly removes an element from a list. """
    pass

def test_size():
    """ Tests that the size method returns correct values. """
    pass

test_init_new()
test_init_existing()
test_init_corrupted()
test_append_and_get()
test_push_and_pop()
test_index()
test_remove()
test_size()
print "All tests passed!"
