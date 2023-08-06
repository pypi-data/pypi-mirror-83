import cProfile
import pstats
from datetime import datetime

from pyinstrument import Profiler
from pyinstrument import renderers

from coinstac_pyprofiler.core import utils as prof_ut


class profile(object):
    """
    Decorator class to profile any method.
    Note: 'output_file_prefix' should include its (absolute) directory path
    Usage: Keep the following line above the method definition which needs to be profiled.

    @profile(type="pyinstrument", output_file_prefix=output_file_prefix)
    """

    def __init__(self, type, output_file_prefix, params_dict={}):
        self.type = type
        self.output_file_prefix = output_file_prefix
        self.params_dict = params_dict

    def __call__(self, func):

        def wrapped_profiler(*args):

            if self.type.lower() == 'pyinstrument':
                profiler = Profiler()
                profiler.start()
                retval = func(*args)
                profiler.stop()

                json_object = profiler.output(renderers.JSONRenderer())
                output_file = self.output_file_prefix + '_' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S.%f")

                prof_ut.write_json_to_file(json_object, output_file + '.json')
                if self.params_dict.get('save_html', False):
                    page = prof_ut.render_html_from_json_string(json_object)
                    prof_ut.write_to_file(page, output_file + '.html')

                return retval

            elif self.type.lower() == 'cprofile':
                output_file = self.output_file_prefix + '_' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S.%f")
                """
                TODO: This section is not tested
                """
                pr = cProfile.Profile()
                pr.enable()
                retval = func(*args)
                pr.disable()
                pr.dump_stats(output_file + ".prof")

                """ 
                Perform additional operations on .prof output file
                """
                with open(output_file, 'w') as f:
                    ps = pstats.Stats(pr, stream=f)
                    if self.params_dict.get('strip_dirs', False):
                        ps.strip_dirs()

                    if self.params_dict.get('sort_by', False):
                        sort_by = self.params_dict['sort_by']
                        if isinstance(sort_by, (tuple, list)):
                            ps.sort_stats(*sort_by)
                        else:
                            ps.sort_stats(sort_by)
                return retval

        return wrapped_profiler


class Profile():
    """
    Use this class if you prefer to start and stop the profiler as per your needs instead of using a decorator.
    Note: 'output_file_prefix' should include its absolute directory path
        "type" : "pyinstrument"
        params_dict: has directory of other parameters;
                save_html: False :  When 'pyinstrument' type is selected, it saves log as json file;
                                    Set this to True and pass as params_dict for html output to be saved

    obj = Profile(type="pyinstrument", output_file_prefix=output_file_prefix)

    """

    def __init__(self, type, output_file_prefix, params_dict={}):
        def initialize():
            """
            Inner method to initialize profiler
            """
            if self.type == 'pyinstrument':
                self.profiler = Profiler()

        self.type = type.lower()
        self.output_file_prefix = output_file_prefix
        self.params_dict = params_dict
        self.profiler = None
        initialize()

    def start(self):
        self.profiler.start()

    def stop(self):
        self.profiler.stop()

    def persist_log(self, save_html=False):
        output_file = self.output_file_prefix + '_' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S.%f")

        if self.type == 'pyinstrument':
            json_object = self.profiler.output(renderers.JSONRenderer())

            prof_ut.write_json_to_file(json_object, output_file + '.json')
            if self.params_dict.get('save_html', False) or save_html:
                page = prof_ut.render_html_from_json_string(json_object)
                prof_ut.write_to_file(page, output_file + '.html')

        if self.type == 'cprofile':
            raise ("Not implemented for cprofile profiler..")
