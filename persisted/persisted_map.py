from log import Log

class Map():
    """ A persisted map.

    Any call which updates the state of the map will result in an update to the
    backing file with which the map was initialized.

    """

    # Keys for the operations map.
    _put = "put"
    _delete = "delete"

    def __init__(self, path_to_backing_file):
        """ Initializes the map using the provided file.

        Args:
            path_to_backing_file (string):
                The file at this path will be used to record the state of the
                map. If no file currently exists at this location, one will be
                created. Otherwise, the file will be used to initialize the
                state of this map.

        """
        self._log = Log(path_to_backing_file, _get_compaction_callback())
        self._inner_map = {}
        self._log.replay(self._get_op_map())

    def put(self, key, value):
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
        self._inner_map[key] = value
        self._log.save_operation(_put, key, value)

    def get(self, key):
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

    def delete(self, key):
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
        # TODO: check for KeyError
        val = self._inner_map[key]
        # TODO: delete mapping
        self._log.save_operation(_delete, key)
        return val

    def size(self):
        """ Used to query the size of the map.

        Returns:
            size (int)
                The number of key / value pairs in this map.

        """
        # TODO: can we be 'lengthable'? iterable?
        return len(self._inner_map)

    def _get_compaction_callback(self):
        def callback():
            # TODO: could probably be list comprehension
            ops = []
            for key in self._inner_map:
                ops.append(_put, [key, self._inner_map[key]])
            return ops
        return callback

    def _get_op_map(self):
        return {_put : self.put, _delete : self.delete}
