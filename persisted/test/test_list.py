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

    def test_len(self):
        " Tests the __len__ method"
        test_list = List(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        assert len(test_list) == 0
        for i in range(number_elements):
            test_list.append(i)
        assert len(test_list) == number_elements

    def test_append(self):
        " Tests the append method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        test_list.append("item0")
        test_list.append("item1")
        assert test_list[0] == "item0"
        assert test_list[1] == "item1"

    def test_getitem(self):
        " Tests the __getitem__ method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        test_list.append("item0")
        assert test_list[0] == "item0"
        assert test_list.__getitem__(0) == "item0"

    def test_setitem(self):
        " Tests the __setitem__ method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            test_list.append(i)
        test_list[3] = "three"
        test_list.__setitem__(4, "four")
        assert test_list[3] == "three"
        assert test_list[4] == "four"

    def test_delitem(self):
        " Tests the delitem method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        test_list.append("zero")
        test_list.append("one")
        test_list.append("two")
        del test_list[0]
        test_list.__delitem__(0)
        assert len(test_list) == 1
        assert test_list[0] == "two"

    def test_index(self):
        " Tests the index method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        test_list.append("zero")
        test_list.append("one")
        test_list.append("two")
        test_list.append("two")
        assert test_list.index("zero") == 0
        assert test_list.index("two") == 2

    def test_remove(self):
        " Tests the remove method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        test_list.append("zero")
        test_list.append("one")
        test_list.append("two")
        test_list.append("two")
        test_list.remove("zero")
        test_list.remove("two")
        assert len(test_list) == 2
        assert test_list[0] == "one"
        assert test_list[1] == "two"

    def test_push(self):
        " Tests the push method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            test_list.push(i)
        for i in range(number_elements):
            assert test_list[i] == number_elements - 1 - i

    def test_pop(self):
        " Tests the pop method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            test_list.append(i)
        pops = 0
        while len(test_list) > 0:
            pops += 1
            assert test_list.pop() == number_elements - pops

    def test_iter(self):
        "Tests the __iter__ method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            test_list.append(i)
        iterator = test_list.__iter__()
        for i in range(number_elements):
            assert iterator.next() == i
        try:
            iterator.next()
            self.fail("iterator should have been exhausted")
        except StopIteration:
            # This is what we expect to happen
            return

    def test_reversed(self):
        " Tests the __reversed__ method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            test_list.append(i)
        current = 9
        for element in reversed(test_list):
            assert element == current
            current -= 1

    def test_contains(self):
        " Tests the __contains__ method. "
        test_list = List(tempfile.NamedTemporaryFile().name)
        test_list.append(1)
        assert 1 in test_list
        assert test_list.__contains__(1)
        assert not "someOtherElement" in test_list
        assert not test_list.__contains__("someOtherElement")
