from log import Log

class List():
    """ A persisted list.

    Any call which updates the state of the map will result in an update to the
    backing file with which the map was initialized.

    TODO: check items for JSON-encodability before mutations.

    """

    # Keys for the operations map.
    _append = "append"
    _set = "set"
    _delete = "delete"
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

    def __len__(self):
        """ Returns the number of elements in the list. """
        return len(self._inner_list)

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

    def __getitem__(self, index):
        """ Returns the element at the input index in the list.

        Returns:
            element (object)
                The element at the provided index in the list.
        Raises:
            IndexError
                If the index is not in the range [0, len(list)).

        """
        return self._inner_list[index]

    def __setitem__(self, index, element):
        """ Sets the element at the provided index.

        Args:
            index (int)
                The position of the element to set.
            element (object)
                The element to put at the provided index.
        Raises:
            IndexError
                If the index is not in the range [0, len(list)).
            TODO: something if not JSON encodable
        """
        self._inner_list[index] = element
        self._log.save_operation(_set, index, element)

    def __delitem__(self, index):
        """ Deletes the element at the provided index.

        Args:
            index (int)
                The position in the list of the element to delete.
        Raises:
            IndexError
                If the index is not valid for the list.
        """
        del self._inner_list[index]
        self._log.save_operation(_delete, index)

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

    def __iter__(self):
        pass

    def __reversed__(self):
        pass

    def __contains__(self, element):
        pass

    # TODO: addition operator:
    # https://docs.python.org/3/reference/datamodel.html?emulating-container-types#emulating-container-types

    def _get_compaction_callback(self):
        def callback():
            return [(_append, element) for element in self._inner_list]
        return callback

    def _get_op_map(self):
        return {
            _append : self.append,
            _set : self.__setitem__,
            _delete : self.__delitem__,
            _remove : self.remove,
            _push : self.push,
            _pop : self.pop
        }
