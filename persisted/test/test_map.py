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
        test_map = Map(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        assert len(test_map) == 0
        for i in range(number_elements):
            test_map[i] = i
        assert len(test_map) == number_elements

    def test_setitem(self):
        " Tests the __setitem__ method. "
        test_map = Map(tempfile.NamedTemporaryFile().name)
        test_map["testKey1"] = "testValue1"
        test_map.__setitem__("testKey2", "testValue2")
        assert test_map["testKey1"] == "testValue1"
        assert test_map["testKey2"] == "testValue2"

    def test_getitem(self):
        " Tests the __getitem__ method. "
        test_map = Map(tempfile.NamedTemporaryFile().name)
        test_map["testKey1"] = "testValue1"
        assert test_map["testKey1"] == "testValue1"
        assert test_map.__getitem__("testKey1") == "testValue1"

    def test_delitem(self):
        " Tests the __delitem__ method. "
        test_map = Map(tempfile.NamedTemporaryFile().name)
        test_map["testKey1"] = "testValue1"
        assert test_map["testKey1"] == "testValue1"
        del test_map["testKey1"]
        assert len(test_map) == 0
        try:
            test_map["testKey1"]
            self.fail("key should not exist after deletion")
        except KeyError:
            # This is what we want to happen.
            return

    def test_contains(self):
        " Tests the __contains__ method. "
        test_map = Map(tempfile.NamedTemporaryFile().name)
        test_map["testKey1"] = "testValue1"
        assert "testKey1" in test_map
        assert test_map.__contains__("testKey1")
        assert not "someOtherKey" in test_map
        assert not test_map.__contains__("someOtherKey")

    def test_iter(self):
        "Tests the __iter__ method. "
        test_map = Map(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            test_map[i] = i * 10
        iterator = test_map.__iter__()
        for i in range(number_elements):
            assert iterator.next() == i
        try:
            iterator.next()
            self.fail("iterator should have been exhausted")
        except StopIteration:
            # This is what we expect to happen
            return

    def test_iteritems(self):
        "Tests the iteritems method. "
        test_map = Map(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            test_map[i] = i * 10
        iterator = test_map.iteritems()
        for i in range(number_elements):
            assert iterator.next() == (i, i * 10)
        try:
            iterator.next()
            self.fail("iterator should have been exhausted")
        except StopIteration:
            # This is what we expect to happen
            return

    def test_iterkeys(self):
        "Tests the iteritems method. "
        test_map = Map(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            test_map[i] = i * 10
        iterator = test_map.iterkeys()
        for i in range(number_elements):
            assert iterator.next() == i
        try:
            iterator.next()
            self.fail("iterator should have been exhausted")
        except StopIteration:
            # This is what we expect to happen
            return

    def test_itervalues(self):
        "Tests the iteritems method. "
        test_map = Map(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            test_map[i] = i * 10
        iterator = test_map.itervalues()
        for i in range(number_elements):
            assert iterator.next() == i * 10
        try:
            iterator.next()
            self.fail("iterator should have been exhausted")
        except StopIteration:
            # This is what we expect to happen
            return
