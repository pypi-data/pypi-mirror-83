import io
import os
import sys

from anytree.exporter import DotExporter

from coinstac_pyprofiler.core import RootNode as r_node


def render_html_from_json_file(json_file_path):
    """
    Generates a html page to visualize merged json file format generated from pyinstrument profiler.
    This is similar to the htmlrenderer in pyinstrument source code.

    :param json_file_path: name of the json file with path
    """

    with io.open(json_file_path) as json_file:
        session_json = json_file.read()
        return render_html_from_json_string(session_json)


def render_html_from_json_string(json_string):
    """
    Generates a html page to visualize merged json content from using pyinstrument profiler.
    This is similar to the htmlrenderer in pyinstrument source code.

    :param json_string: json content in a string
    """

    def get_js_from_pyinstrument_html_resources():
        RESOURCES_PATH = os.sep.join(["pyinstrument", "renderers", "html_resources", "app.js"])

        for package_path in sys.path:
            if "-packages" in package_path and os.path.exists(os.path.join(package_path, RESOURCES_PATH)):
                with io.open(os.path.join(package_path, RESOURCES_PATH), encoding='utf-8') as f:
                    return f.read()

        """
        Raises exception if system doesnot have pyinstrument html resources path
        """
        raise RuntimeError("Could not find app.js. If you are running "
                           "pyinstrument from a git checkout, run 'python "
                           "setup.py build' to compile the Javascript "
                           "(requires nodejs).")
        return None

    js = get_js_from_pyinstrument_html_resources()
    """
    Generates html page for visualizing json file
    # https://github.com/joerick/pyinstrument/blob/master/pyinstrument/renderers/html.py
    """
    html_page_content = u'''<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>
                <script>
                    window.profileSession = {json_string}
                </script>
                <script>
                    {js}
                </script>
            </body>
            </html>'''.format(js=js, json_string=json_string)

    return html_page_content


def render_tree_from_json(json_input_file, output_file_name, max_level=None, profile_type="pyinstrument"):
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
