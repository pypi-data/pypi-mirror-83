import glob
import os

from coinstac_pyprofiler.core import RootNode as r_node
from coinstac_pyprofiler.core import utils as prof_ut


def merge_json_computation(simulator_test_dir, num_clients, json_dir_name, output_dir, output_file_prefix,
                           save_format="html", has_remote=True):
    """
    Merges the json profile output files generated using pyinstrument for every iteration of a computation
    and saves merged output.

    USECASE:
    For a computation in coinstac-simulator, some computation has many iterations and every iteration of python call
    generates a separate profile json output file. All such json files can be merged separately for each client/remote
    using this call.

    :param simulator_test_dir:  Absolute path to Simulator test directory
    :param num_clients: number of clients in the simulator test output directory to merge
    :param json_dir_name: name of the directory which has json profile files
    :param output_dir: Absolute path of the directory where the merged output files to be written. Creates one if it
                    doesnot exist.
    :param output_file_prefix: Name (or prefix) of the output merged file; DONOT include directory path here
    :param save_format: html or json formats are allowed. To save both formats, "json|html" can be used.
    :param has_remote: Set to false if only client

    """
    CLIENT_DIR_NAME = 'local'
    REMOTE_DIR_NAME = 'remote'
    dir_structures = ['output', CLIENT_DIR_NAME, 'simulatorRun']
    working_dir = os.path.join(simulator_test_dir, os.sep.join(dir_structures), json_dir_name)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_file_prefix)
    for client_num in range(num_clients):
        current_client = CLIENT_DIR_NAME + str(client_num)
        current_dir = working_dir.replace(CLIENT_DIR_NAME, current_client)
        curr_output_file = output_file + "_" + current_client + "_merged"
        merge(current_dir, curr_output_file, save_html='html' in save_format, save_json='json' in save_format)

    """
    merge remote files
    """
    if has_remote:
        master_node = REMOTE_DIR_NAME
        current_dir = working_dir.replace(CLIENT_DIR_NAME, master_node)
        curr_output_file = output_file + "_" + master_node + "_merged"
        merge(current_dir, curr_output_file, save_html='html' in save_format, save_json='json' in save_format)


def merge(input_dir, output_file_prefix, save_html=True, save_json=False):
    """
    Merges all the json in a file in a given directory 'input_dir' and saves the merged output in the output directory
    and file prefix mentioned in 'output_file_prefix'
    """
    current_files = os.path.join(input_dir, "*.json")
    profiler_logs_file_names = glob.glob(current_files)

    assert (len(profiler_logs_file_names) > 0), "No .json files to merge in " + input_dir
    """
    creates a main node to store the merged results
    """
    with open(profiler_logs_file_names[0], "r") as content:
        print("loading json files in dir: " + input_dir)
        main_node = r_node.RootNode(content)

    for file_name in profiler_logs_file_names[1:]:
        with open(file_name, "r") as content:
            other_node = r_node.RootNode(content)
            main_node.merge(other_node)

    json_string = main_node.get_json_string()
    print("Finished merging json files in : ", input_dir, ";  Storing merged file in: ", output_file_prefix)

    if save_json:
        prof_ut.write_json_to_file(json_string, output_file_prefix + ".json")
    if save_html:
        prof_ut.write_to_file(prof_ut.render_html_from_json_string(json_string), output_file_prefix + ".html")
