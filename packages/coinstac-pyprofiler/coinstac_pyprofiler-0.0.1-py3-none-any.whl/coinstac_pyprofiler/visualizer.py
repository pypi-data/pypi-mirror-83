from anytree.exporter import DotExporter

from coinstac_pyprofiler.core import RootNode as r_node


def visualize_json(json_input_file, output_file_name, max_level=None, profile_type="pyinstrument"):
    """
    Generates a tree visualization of json file generated from pyinstrument profiler.

    :param json_input_file: name of the json file with path
    :param output_file_name: name of the output image file with path
    :param profile_type: Type of profiling used
    """

    assert (profile_type == "pyinstrument" and json_input_file.endswith(".json")), \
        "This visualizer works for json file format from pyinstrument profiler"

    with open(json_input_file, "r") as content:
        main_node = r_node.RootNode(content)

    root_node = main_node.get_tree()
    depth_str = '_depth_' + str(max_level) if max_level else ''
    
    dot_obj = DotExporter(root_node, nodeattrfunc=lambda node: "shape=box", maxlevel=max_level)
    dot_obj.to_picture(output_file_name + depth_str + ".png")
