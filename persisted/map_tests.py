""" Tests for persisted_map.Map """

import tempfile
from persisted_map import Map

def test_init_new():
    """ Tests initialization of brand new map.

    We return the map created for use in other tests.

    """
    return Map(tempfile.NamedTemporaryFile().name)

def test_init_existing():
    """ Tests initialization of a log from a previous map's backing file.

    We return the map for use in other tests.

    """
    # First save some stuff so we have something to load.
    existing_map = test_init_new()
    existing_map[1] = 1
    existing_map[2] = "two"
    existing_map["three"] = 3
    existing_map["list"] = [1,2,3]
    existing_map["to be deleted"] = 5
    del existing_map["to be deleted"]
    newly_loaded_map = Map(existing_map._log._backing_file)
    for key, value in existing_map.iteritems():
        assert key in newly_loaded_map
        assert newly_loaded_map[key] == value
    assert len(newly_loaded_map) == len(existing_map)
    return newly_loaded_map

def test_init_corrupted():
    """ Tests initialization of a map from a badly formatted file. """
    # Copy the log file then corrupt it by adding a bad line.
    existing_map = test_init_existing()
    # Sanity check (we're putting the bad data between the 1st and 2nd line).
    assert len(open(existing_map._log._backing_file).readlines()) > 1
    copied_backing_file = tempfile.NamedTemporaryFile()
    bad_line_written = False
    for line in open(existing_map._log._backing_file).readlines():
        copied_backing_file.write(line + "\n")
        if not bad_line_written:
            copied_backing_file.write("ooga booga I'm corrupted data")
            bad_line_written = True
    copied_backing_file.flush()
    try:
        Map(copied_backing_file.name)
    except ValueError:
        # This is what we expected - success.
        return
    raise Exception("Init call on corrupted file should have failed")

test_init_new()
test_init_existing()
test_init_corrupted()
print "All tests passed!"
