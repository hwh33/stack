from log import Log, test_json_encoding

# Keys for the operations map.
_set = "set"
_delete = "delete"

class Map():
    """ A persisted map.

    Any call which updates the state of the map will result in an update to the
    backing file with which the map was initialized.

    TODO: check items for JSON-encodability before mutations.

    """

    def __init__(self, path_to_backing_file):
        """ Initializes the map using the provided file.

        Args:
            path_to_backing_file (string):
                The file at this path will be used to record the state of the
                map. If no file currently exists at this location, one will be
                created. Otherwise, the file will be used to initialize the
                state of this map.

        """
        self._inner_map = {}
        self._log = Log(path_to_backing_file, self._get_compaction_callback())
        # We make sure persistence is turned off during the replay so that we
        # don't duplicate everything in the log file.
        self._persist = False
        self._log.replay(self._get_op_map())
        self._persist = True

    def __len__(self):
        """ Returns the number of key-value pairs in the map. """
        return len(self._inner_map)

    def __setitem__(self, key, value):
        """ Puts the key / value pair into the map.

        Args:
            key (object)
                The key by which the value will be retrievable. Must be
                encodable by the json.dumps method.
            value (object)
                The value stored by the key. Must be encodable by the json.dumps
                method.
        Raises:
            TODO: something if not JSON encodable

        """
        test_json_encoding(key, value)
        self._inner_map[key] = value
        if self._persist: self._log.save_operation(_set, key, value)

    def __getitem__(self, key):
        """ Used to query the value mapped to the input key.

        Args:
            key (object)
                The key whose value should be retrieved.
        Returns:
            value (object)
                The value mapped to by the input key.
        Raises:
            KeyError
                If the key was not found in the map.

        """
        return self._inner_map[key]

    def __delitem__(self, key):
        """ Used to delete the mapping for the input key.

        Args:
            key (object)
                The key for the mapping to be deleted.
        Returns:
            value (object)
                The value which was removed from the map.
        Raises:
            KeyError
                If the key was not found in the map.

        """
        test_json_encoding(key)
        val = self._inner_map[key]
        del self._inner_map[key]
        if self._persist: self._log.save_operation(_delete, key)
        return val

    def __contains__(self, key):
        """ Returns true iff the key is present in the map. """
        return key in self._inner_map

    def __iter__(self):
        """ Returns an iterator over the keys in the map. """
        return self._inner_map.__iter__()

    def iteritems(self):
        """ Returns an iterator over the (key, value) pairs in the map. """
        return self._inner_map.iteritems()

    def iterkeys(self):
        """ Returns an iterator over the keys in the map. """
        return self._inner_map.iterkeys()

    def itervalues(self):
        """ Returns an iterator over the values in the map. """
        return self._inner_map.itervalues()

    def _get_compaction_callback(self):
        def make_kv_tuple(key):
            return (_set, [key, self._inner_map[key]])
        def callback():
            return [make_kv_tuple(key) for key in self._inner_map]
        return callback

    def _get_op_map(self):
        return {_set : self.__setitem__, _delete : self.__delitem__}
