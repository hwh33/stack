""" Tests for persisted.Log """

import os
import random
import string
import tempfile
from log import Log


class DummyOperation():
    """ A dummy operation for testing the log. """

    def __init__(self):
        # Give the dummy operation a random string for a name.
        self.name = ''.join(
            random.choice(string.ascii_lowercase) for _ in range(10))
        # Include in our parameters on of every type encodable as JSON.
        # See: https://docs.python.org/3/library/json.html#py-to-json-table
        self.parameters = [
            "dummy string",
            10,
            2.718,
            True,
            False
        ]
        self.parameters.append(list(self.parameters))
        self.parameters.append(tuple(self.parameters))
        dict_parameter = {}
        key = 0
        for parameter in self.parameters:
            dict_parameter[key] = parameter
            key += 1
        self.parameters.append(dict_parameter)
        # Include a list, tuple, and dictionary with nested objects.
        self.parameters.append(list(self.parameters))
        self.parameters.append(tuple(self.parameters))
        dict_parameter = {}
        key = 0
        for parameter in self.parameters:
            dict_parameter[key] = parameter
            key += 1
        self.parameters.append(dict_parameter)
        self.function_called = False

    def get_function(self):
        def set_called(*args):
            """ Ignore input - just mark that the function has been called. """
            self.function_called = True
        return set_called


# Used in tests which don't care about compaction.
dummy_compaction_callback = lambda: []


def test_init_new():
    """ Tests initialization of brand new log.

    We return the log created for use in other tests.

    """
    backing_file = tempfile.NamedTemporaryFile()
    return Log(backing_file.name, dummy_compaction_callback)

def test_init_existing(existing_log):
    """ Tests initialization of a log from a previous log's backing file. """
    # First save some operations so that we have something to load.
    for _ in range(10):
        operation = DummyOperation()
        existing_log.save_operation(operation.name, *operation.parameters)
    # Note that this will wipe the log (because the compaction callback returns
    # an empty list).
    Log(existing_log._backing_file, dummy_compaction_callback)

def test_init_corrupted(existing_log):
    """ Tests initialization of a log from a badly formatted file. """
    # Copy the log file then corrupt it by adding a bad line.
    # Save some data to the log.
    for _ in range(10):
        operation = DummyOperation()
        existing_log.save_operation(operation.name, *operation.parameters)
    # Sanity check (we're putting the bad data between the 1st and 2nd line).
    assert len(open(existing_log._backing_file).readlines()) > 1
    copied_backing_file = tempfile.NamedTemporaryFile()
    bad_line_written = False
    for line in open(existing_log._backing_file).readlines():
        copied_backing_file.write(line + "\n")
        if not bad_line_written:
            copied_backing_file.write("ooga booga I'm corrupted data")
            bad_line_written = True
    copied_backing_file.flush()
    try:
        Log(copied_backing_file.name, dummy_compaction_callback)
    except ValueError:
        # this is what we expected - success
        return
    raise Exception("Init call on corrupted file should have failed")

def test_save_and_replay():
    """ Tests that operations are saved in the log and can be replayed. """
    # Get a fresh log from the test_init_new method.
    log = test_init_new()
    # Save every operation and simultaneously build up the ops map for the
    # replay method.
    dummy_ops = []
    ops_map = {}
    for _ in range(10):
        dummy_op = DummyOperation()
        dummy_ops.append(dummy_op)
        log.save_operation(dummy_op.name, *dummy_op.parameters)
        ops_map[dummy_op.name] = dummy_op.get_function()
    # Now replay the log and check that every function was called.
    log.replay(ops_map)
    for dummy_op in dummy_ops:
        assert dummy_op.function_called

def test_compact():
    """ Tests that compaction reduces log file size when possible. """
    operation = DummyOperation()
    backing_file = tempfile.NamedTemporaryFile()
    compaction_callback = lambda: [(operation.name, operation.parameters)]
    log = Log(backing_file.name, compaction_callback)
    # Save the same operation many times.
    for _ in range(100):
        log.save_operation(operation.name, *operation.parameters)
    # After compaction, the log should be condensed to one instance of the saved
    # operation.
    original_size = os.stat(log._backing_file).st_size
    log.compact()
    compacted_size = os.stat(log._backing_file).st_size
    assert compacted_size < original_size
    assert compacted_size > 0

def test_compact_if_necessary():
    """ Tests that compaction is run when the threshold is exceeded. """
    operation = DummyOperation()
    backing_file = tempfile.NamedTemporaryFile()
    compaction_callback = lambda: [(operation.name, operation.parameters)]
    log = Log(backing_file.name, compaction_callback)
    # Save the same operation many times.
    for _ in range(100):
        log.save_operation(operation.name, *operation.parameters)
    # Set the compaction threshold to less than the current size of the backing
    # file.
    original_size = os.stat(log._backing_file).st_size
    log._compaction_threshold = original_size - 1
    # Save an operation to trigger compaction.
    log.save_operation(operation.name, *operation.parameters)
    compacted_size = os.stat(log._backing_file).st_size
    assert compacted_size < original_size
    assert compacted_size > 0
    # Now check that the log never goes over the threshold over the course of
    # many saves.
    threshold = log._compaction_threshold
    for _ in range(1000):
        log.save_operation(operation.name, *operation.parameters)
        current_size = os.stat(log._backing_file).st_size
        assert current_size < threshold
        assert current_size > 0


new_log = test_init_new()
test_init_existing(new_log)
test_init_corrupted(new_log)
test_save_and_replay()
test_compact()
test_compact_if_necessary()
print "All tests passed!"
