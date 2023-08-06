import json
import os
from datetime import timedelta


def combine_strings(*strings):
    return ''.join(str(string) for string in strings)


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
