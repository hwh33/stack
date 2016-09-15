import json
import os
from tempfile import TemporaryFile

_key = "key"
_parameters = "parameters"
# Initialize the compaction threshold to 1 MB for new logs.
_initial_compaction_threshold = 1024 * 1024

def test_json_encoding(*objs):
    """ A helper function for users of this library.

    Raises an error if the input object is not JSON-encodable.

    Args:
        objs (*object)
            The objects to test for JSON-encodability.
    Raises:
        TypeError:
            If any of the input objects is not encodable as JSON.
    """
    for obj in objs: json.dumps(obj)

class Log():
    """ A log to back data structures in the 'persisted' library. """

    def __init__(self, filepath, compaction_callback):
        """ Initializes a log backed by a file at the given filepath.

        Args:
            filepath (string)
                The path to the file which backs this log. If no file exists at
                that path, one will be created.
            compaction_callback (function: () -> (string, object list) list)
                A function which returns a list of operations representing the
                current state of the data structure backed by this log. The
                operations should be 2-tuples. The first element should be a
                string defining the operation's name and the second should be a
                list of parameters for the operation (can be empty). These
                should be the same as would be passed to the save_operation
                method. This function should be callable multiple times.

        """
        self._backing_file = filepath
        # We do this to create the file if it does not exist.
        try:
            log_file = open(self._backing_file, 'a+')
            log_file.close()
        except IOError as e:
            raise IOError("Error initializing log file", e)
        # Check that every line is decodable (we want to fail fast otherwise).
        log_file = open(self._backing_file)
        for line in log_file.readlines():
            try:
                json.loads(line)
            except Exception as e:
                raise ValueError("Malformed input file", e)
        self._compaction_callback = compaction_callback
        self._compaction_threshold = _initial_compaction_threshold

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
        self._compact_if_necessary()

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
            op(*op_dict[_parameters])

    def compact(self):
        """ Uses the compaction callback to reduce the log.

        After this method returns, the log will consist of only the operations
        returned by the compaction callback. Compaction is run automatically
        when thresholds are met, so users of the log do not usually need to
        worry about calling this method.

        """
        new_log = TemporaryFile()
        for op_name, params in self._compaction_callback():
            op_as_json = json.dumps({_key : op_name, _parameters : params})
            new_log.write(op_as_json + '\n')
        # If all went well, we overwrite the old log file with the new one.
        new_log.seek(0)
        log_file = open(self._backing_file, 'w')
        log_file.writelines(new_log.readlines())
        new_log.close()
        log_file.close()

    def _compact_if_necessary(self):
        size = os.stat(self._backing_file).st_size
        if size < self._compaction_threshold:
            return
        self.compact()
        size = os.stat(self._backing_file).st_size
        if size > self._compaction_threshold:
            # If we are still over the threshold, we need to increase it to
            # avoid thrashing.
            self._compaction_threshold = size * 2
