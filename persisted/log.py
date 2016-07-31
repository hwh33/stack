import json
from tempfile import TemporaryFile

class Log():
    """ A log to back data structures in the 'persisted' library. """

    _key = "key"
    _parameters = "parameters"
    # Initialize the compaction threshold to 1 MB for new logs.
    _initial_compation_threshold = 1024 * 1024

    def __init__(self, filepath, compaction_callback):
        """ Initializes a log backed by a file at the given filepath.

        Args:
            filepath (string)
                The path to the file which backs this log. If no file exists at
                that path, one will be created.
            compaction_callback (function)
                A function which returns a list of operations representing the
                current state of the data structure represented by this log. The
                operations should be 2-tuples. The first element should be a
                string defining the operation's name and the second should be a
                list of parameters for the operation (can be empty). These
                should be the same as would be passed to the save_operation
                method. This function should be callable multiple times.

        """

        # TODO: check file?
        self._backing_file = filepath
        self._compaction_callback = compaction_callback
        self._compaction_threshold = _initial_compation_threshold
        # Compact during initialization so we can avoid it later.
        self._compact()

    def save_operation(self, op_name, *parameters):
        """ Saves an operation in the log.

        Args:
            op_name (string)
                The name of the operation. Should be consistent across mutliple
                calls.
            *parameters (object)
                The parameters to the operation. There need not be any. The only
                requirement for these parameters is that they be encodable by
                the json.dumps method.

        """

        op_as_json = json.dumps({_key : op_name, _parameters : parameters})
        log_file = open(self._backing_file, 'a')
        log_file.write(op_as_json + '\n')
        log_file.close()

    def replay(self, op_map):
        """ Replays the log to update the persisted data structure.

        Args:
            op_map (dict)
                Maps operation names to functions. Every operation in the log
                has a name and a record of the parameters saved with it. The
                name will be used to look up the corresponding function in the
                map which will then be called with the saved parameters.

        """

        log_file = open(self._backing_file, 'r')
        op_strings = log_file.readlines()
        log_file.close()
        for op_string in op_strings:
            op_dict = json.loads(op_string)
            # Retrieve the operation function from the input map and call it
            # with the saved parameters.
            op = op_map[op_dict[_key]]
            op(op_dict[_parameters])

    def _compact(self):
        new_log = TemporaryFile()
        for op_name, params in self._compaction_callback():
            op_as_json = json.dumps({_key : op_name, _parameters : params})
            new_log.write(op_as_json + '\n')
        # TODO: use OS to copy temp file over log file
        new_log.close()

    # TODO: use this to wrap save_operation and replay methods.
    def _compact_if_necessary(self):
        # TODO: replace placeholder with real size of backing file
        size = 10
        if size < self._compaction_threshold:
            return
        self._compact()
        # TODO: update size
        if size > self._compaction_threshold:
            # If we are still over the threshold, we need to increase it to
            # avoid thrashing.
            self._compaction_threshold = size * 2
