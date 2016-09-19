""" Tests for persisted.list.List """

import tempfile
import unittest

from persisted import List

class TestList(unittest.TestCase):

    def test_init_new(self):
        " Tests initialization of brand new list. "
        List(tempfile.NamedTemporaryFile().name)

    def test_init_existing(self):
        " Tests initialization of a list from a previous list's backing file. "
        # First save some stuff so we have something to load.
        existing_list = List(tempfile.NamedTemporaryFile().name)
        existing_list.append(1)
        existing_list.append(2)
        existing_list.append("to be deleted")
        existing_list.append("boo")
        del existing_list[2]
        newly_loaded_list = List(existing_list._log._backing_file)
        assert len(newly_loaded_list) == len(existing_list)
        for index in range(0, len(existing_list)):
            assert newly_loaded_list[index] == existing_list[index]

    def test_init_corrupted(self):
        " Tests initialization of a list from a badly formatted file. "
        # Copy the log file then corrupt it by adding a bad line.
        existing_list = List(tempfile.NamedTemporaryFile().name)
        existing_list.append(1)
        existing_list.append(2)
        existing_list.append("boo")
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

    def test_append_and_get(self):
        " Tests that elements can be appended and retrieved with get. "
        pass

    def test_push_and_pop(self):
        " Tests that elements can be pushed and then popped. "
        pass

    def test_index(self):
        " Tests that the index method returns correct values. "
        pass

    def test_remove(self):
        " Tests that the remove method truly removes an element from a list. "
        pass

    def test_size(self):
        " Tests that the size method returns correct values. "
        pass