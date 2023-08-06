from . import utils as profiler_utils


class AbstractNode:
    """
    Parent class with common functions needed for RootNode and InnerNode classes
    """

    def get_key(self):
        return self.node_key

    def get_name(self, total_time):
        name = self.function + "()\n" + str((self.time / total_time) * 100) + "%" + "\n" \
               + profiler_utils.get_human_readable_time(self.time) + "\n" + self.file_path_short \
               + ": Line " + str(self.line_no)

        return name
