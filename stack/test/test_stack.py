""" Tests for stack.Stack """

import random
import tempfile
import time
import unittest

from stack import Stack

def has_page(pages_as_dicts, page_as_list):
    """ Helper. Returns true if page_dicts contains page_as_list. """
    reducer = lambda already_found, page_as_dict: \
        already_found or set(page_as_dict.itervalues()) == set(page_as_list)
    return reduce(reducer, pages_as_dicts, False)

class TestStack(unittest.TestCase):

    def test_init_new(self):
        " Tests initialization of a brand new stack. "
        Stack(tempfile.NamedTemporaryFile().name)

    def test_init_existing(self):
        " Tests initialization of a stack from a previous stack's backing file."
        # First save some stuff so we have something to load.
        backing_file = tempfile.NamedTemporaryFile().name
        existing_stack = Stack(backing_file)
        existing_stack.add(
            "someurl.example.com", "title", time.time())
        existing_stack.add(
            "someotherurl.example.com", "other title", time.time())
        existing_stack.add(
            "tobedeleted.example.com", "Bye bye =(", time.time())
        existing_stack.delete("tobedeleted.example.com")
        newly_loaded_stack = Stack(backing_file)
        assert newly_loaded_stack == existing_stack

    def test_add(self):
        " Tests the add method. "
        stack = Stack(tempfile.NamedTemporaryFile().name)
        page1 = [ "test.com", "test title", time.time() ]
        page2 = [ "example.com", "example title", time.time() ]
        stack.add(page1[0], page1[1], page1[2])
        stack.add(page2[0], page2[1], page2[2])
        pages = stack.as_sorted_list()
        assert has_page(pages, page1)
        assert has_page(pages, page2)

    def test_delete(self):
        " Tests the delete method. "
        " Tests the add method. "
        stack = Stack(tempfile.NamedTemporaryFile().name)
        page1 = [ "test.com", "test title", time.time() ]
        page2 = [ "example.com", "example title", time.time() ]
        stack.add(page1[0], page1[1], page1[2])
        stack.add(page2[0], page2[1], page2[2])
        pages = stack.as_sorted_list()
        # Sanity checks.
        assert has_page(pages, page1)
        assert has_page(pages, page2)
        stack.delete(page1[0])
        pages = stack.as_sorted_list()
        assert not has_page(pages, page1)
        assert has_page(pages, page2)
        # Deletions of non-existing pages should be no-ops.
        try:
            stack.delete(page1[0])
        except:
            self.fail("no exception expected")

    def test_as_sorted_list(self):
        " Tests as_sorted_list. "
        pages_as_lists = []
        for i in range(10):
            page_as_list = ["url" + str(i) + ".com", "title", time.time()]
            pages_as_lists.append(page_as_list)
        random.shuffle(pages_as_lists)
        stack = Stack(tempfile.NamedTemporaryFile().name)
        for page_as_list in pages_as_lists:
            stack.add(page_as_list[0], page_as_list[1], page_as_list[2])
        pages_as_dicts = stack.as_sorted_list()
        last_timestamp = float("inf")
        for page_as_dict in pages_as_dicts:
            assert page_as_dict[Stack.timestamp_key] <= last_timestamp
            last_timestamp = page_as_dict[Stack.timestamp_key]

    def test_eq(self):
        " Tests the __eq__ method. "
        test_stack1 = Stack(tempfile.NamedTemporaryFile().name)
        test_stack2 = Stack(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            page = ["url" + str(i) + ".com", "title", time.time()]
            test_stack1.add(page[0], page[1], page[2])
            test_stack2.add(page[0], page[1], page[2])
        assert test_stack1 == test_stack2
        assert not test_stack1 == Stack(tempfile.NamedTemporaryFile().name)
        # Equality check should fail for subclasses which do not implement
        # __eq__ themselves.
        class StackChild(Stack): pass
        child = StackChild(tempfile.NamedTemporaryFile().name)
        assert test_stack1.__eq__(child) == NotImplemented
        assert child.__eq__(test_stack1) == NotImplemented
        # Other types shouldn't pass equality checks.
        assert not test_stack1 == "some string"

    def test_ne(self):
        " Tests the __ne__ method. "
        test_stack1 = Stack(tempfile.NamedTemporaryFile().name)
        test_stack2 = Stack(tempfile.NamedTemporaryFile().name)
        number_elements = 10
        for i in range(number_elements):
            page = ["url" + str(i) + ".com", "title", time.time()]
            test_stack1.add(page[0], page[1], page[2])
            test_stack2.add(page[0], page[1], page[2])
        assert not test_stack1 != test_stack2
        assert test_stack1 != Stack(tempfile.NamedTemporaryFile().name)
        # Inequality check should fail for subclasses which do not implement
        # __ne__ themselves.
        class StackChild(Stack): pass
        child = StackChild(tempfile.NamedTemporaryFile().name)
        assert test_stack1.__ne__(child) == NotImplemented
        assert child.__ne__(test_stack1) == NotImplemented
        # Other types should pass inequality checks.
        assert test_stack1 != "some string"
