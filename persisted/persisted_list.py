from log import Log

class List():
    """ A persisted list.

    Any call which updates the state of the map will result in an update to the
    backing file with which the map was initialized.

    """

    # Keys for the operations map.
    _append = "append"
    _remove = "remove"
    _push = "push"
    _pop = "pop"

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
        self._inner_list = []
        self._log.replay(self._get_op_map())

    def append(self, new_element):
        """ Appends the input element to the end of the list.

        Args:
            new_element (object)
                The element to append. Must be encodable by the json.dumps
                method.
        Raises:
            TODO: something if not JSON encodable

        """
        self._inner_list.append(new_element)
        self._log.save_operation(_append, new_element)

    def get(self, index):
        """ Returns the element at the input index in the list.

        Returns:
            element (object)
                The element at the provided index in the list.
        Raises:
            IndexError
                If the index is not in the range [0, len(list)).

        """
        return self._inner_list[index]

    def index(self, value):
        """ Returns the index of the first occurrence of the input value.

        Args:
            value (object)
                The value to find in the list.
        Returns:
            index (int)
                The index of the first occurrence of 'value' in the list.
        Raises:
            ValueError
                If the value was not found in the list.
        """
        return self._inner_list.index(value)

    def remove(self, value):
        """ Removes the first occurrence of the input value.

        Returns:
            value (object)
                The value to remove from the list.
        Raises:
            ValueError
                If the value was not found in the list.

        """
        self._inner_list.remove(value)
        self._log.save_operation(_remove, value)

    def push(self, new_element):
        """ Pushes the input element into the first position in the list.

        Args:
            new_element (object)
                The element to push. Must be encodable by the json.dumps
                method.
        Raises:
            something if not JSON encodable

        """
        self._inner_list = [new_element] + self._inner_list
        self._log.save_operation(_push, new_element)

    def pop(self):
        """ Removes and returns the last element in the list.

        Returns:
            element (object)
                The last element in the list.
        Raises:
            IndexError
                If the list is currently empty.

        """
        value = self._inner_list.pop()
        self._log.save_operation(_pop)
        return value

    def size(self):
        """ Used to query the size of the list.

        Returns:
            size (int)
                The number of elements in the list.

        """
        # TODO: can we be 'lengthable'? iterable?
        return len(self._inner_list)

    def _get_compaction_callback(self):
        def callback():
            # TODO: could probably be list comprehension
            ops = []
            for element in self._inner_list:
                ops.append(_append, [element])
            return ops
        return callback

    def _get_op_map(self):
        return {
            _append : self.append,
            _remove : self.remove,
            _push : self.push,
            _pop : self.pop
        }
