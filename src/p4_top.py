# Added support
from __future__ import print_function

"""p4_top.py Top-level for P4_16 API.  Takes input P4 device and generates JSON"""

__author__ = "Colin Burgin"
__copyright__ = "Copyright 2017, Virginia Tech"
__credits__ = [""]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = ""
__email__ = "cburgin@vt.edu"
__status__ = "in progress"

# Standard Python Libraries
import json
from pprint import pprint
import subprocess
from collections import OrderedDict

# Installed Packages/Libraries

# P4 Specfic Libraries

# Local API Libraries
from p4_graphs import P4_Graphs
from p4_utils import dict_or_OrdDict_to_formatted_str
from p4_constraints import generate_constraints

class P4_Top():
    """Top-level for P4_16 API. Takes input P4 device and generates JSON"""

    # Standard Init stuff
    def __init__(self, debug):

        # Set class variables
        self.debug = debug
        self.json_file = None
        self.json_obj = None

        # # Build parser graph
        # self.graphs = P4_Graphs(self.debug, self.hlir)
        # self.graphs.get_parser()

    # Build P4 Top object from input .p4 device file
    ## Still needs improvement ##
    def build_from_p4(self, input_file, flags):
        # Parse input_file
        [name, version, extension] = input_file.split(".")
        name = name.split("/")
        outfile_name = "compiled_p4_programs/" + name[-1] + "." + version + ".json"

        call_list = ["-o", outfile_name, input_file]
        
        # Parse Flags
        if flags != None:
            flags = flags.split(" ")
            call_list = flags + call_list

        # Add compiler call
        call_list.insert(0, "p4c-bm2-ss")

        if self.debug:
            print("The compiler call was: " + str(call_list))

        for path in self.graphs.paths:
            generate_constraints(self.hlir, path, input_file)

        # Make the command line call
        subprocess.call(call_list)

        # Output file destination
        self.json_file = outfile_name
        self.json_obj = self.load_json(self.json_file)


    # Build P4 Top object from input .json file
    def build_from_json(self, input_file):
        # Output file destination
        self.json_file = input_file
        self.json_obj = self.load_json(self.json_file)

    # Converts the JSON file to the OD we use as our IR
    def load_json(self, input_file):
        data = json.load(open(input_file), object_pairs_hook=OrderedDict)
        return data
