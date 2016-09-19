""" Tests for persisted_map.Map """

import tempfile
import unittest

from persisted import Map

class TestMap(unittest.TestCase):

    def test_init_new(self):
        " Tests initialization of brand new map. "
        Map(tempfile.NamedTemporaryFile().name)

    def test_init_existing(self):
        " Tests initialization of a log from a previous map's backing file. "
        # First save some stuff so we have something to load.
        existing_map = Map(tempfile.NamedTemporaryFile().name)
        existing_map[1] = 1
        existing_map[2] = "two"
        existing_map["three"] = 3
        existing_map["list"] = [1,2,3]
        existing_map["to be deleted"] = 5
        del existing_map["to be deleted"]
        newly_loaded_map = Map(existing_map._log._backing_file)
        assert len(newly_loaded_map) == len(existing_map)
        for key, value in existing_map.iteritems():
            assert key in newly_loaded_map
            assert newly_loaded_map[key] == value
        return newly_loaded_map

    def test_init_corrupted(self):
        """ Tests initialization of a map from a badly formatted file. """
        # Copy the log file then corrupt it by adding a bad line.
        existing_map = Map(tempfile.NamedTemporaryFile().name)
        existing_map[1] = 1
        existing_map[2] = "two"
        existing_map["three"] = 3
        existing_map["list"] = [1,2,3]
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

    def test_len(self):
        " Tests the __len__ method"

    def test_append(self):
        " Tests the append method. "
        pass

    def test_getitem(self):
        " Tests the __getitem__ method. "
        pass

    def test_delitem(self):
        " Tests the delitem method. "
        pass

    def test_contains(self):
        " Tests the __contains__ method. "
        pass

    def test_iter(self):
        "Tests the __iter__ method. "
        pass

    def test_iteritems(self):
        "Tests the iteritems method. "
        pass

    def test_iterkeys(self):
        "Tests the iteritems method. "
        pass

    def test_itervalues(self):
        "Tests the iteritems method. "
        pass
