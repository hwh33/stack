""" Tests for persisted.Log """

def test_init_new():
    """ Tests initialization of brand new log. """
    pass

def test_init_existing():
    """ Tests initialization of a log from a previous log's backing file. """
    pass

def test_init_corrupted():
    """ Tests initialization of a log from a badly formatted file. """
    pass

def test_save_and_replay():
    """ Tests that operations are saved in the log and can be replayed. """
    pass

def test_compact():
    """ Tests that compaction reduces log file size when possible. """
    pass

def test_compact_if_necessary():
    """ Tests that compaction is run when the threshold is exceeded. """
    pass


test_init_new()
test_init_existing()
test_init_corrupted()
test_save_and_replay()
test_compact()
test_compact_if_necessary()
print "All tests passed!"
