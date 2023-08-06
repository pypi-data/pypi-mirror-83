import io
import json
import os
import sys
from datetime import timedelta


def combine_strings(*strings):
    return ''.join(str(string) for string in strings)


def render_html_from_json_file(json_file_path):
    with io.open(json_file_path) as json_file:
        session_json = json_file.read()
        return render_html_from_json_string(session_json)


def render_html_from_json_string(json_string):
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


def write_json_to_file(json_object, file_name):
    if isinstance(json_object, str):
        json_object = json.loads(json_object)
    out = json.dumps(json_object, indent=4)
    write_to_file(out, file_name)


def write_to_file(string_content, file_name):
    with open(file_name, 'w') as out_file:
        out_file.write(string_content)

    os.chmod(file_name, 0o777)


def get_human_readable_time(time_in_sec):
    return "{}".format(str(timedelta(seconds=time_in_sec)))
