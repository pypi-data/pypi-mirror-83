"""
Licensed Materials - Property of IBM
Restricted Materials of IBM
20190891
© Copyright IBM Corp. 2020 All Rights Reserved.
"""
#!/usr/bin/env python3

import logging
import importlib

from warnings import warn

required_libraries = ["tensorflow==2.1.0", "scikit-learn==0.23.1",
                        "keras==2.2.4", "numpy==1.17.4", "pandas", "pytest",
                        "PyYAML", "parse", "websockets", "jsonpickle", "requests",
                        "scipy==1.4.1", "environs", "pathlib2", "diffprivlib",
                        "psutil", "setproctitle", "tabulate", "lz4",
                        "opencv-python", "gym", "ray==0.8.0", "cloudpickle==1.3.0", "image"]


for lib in required_libraries:

    req_lib = lib.split("==")
    
    try:    
        var = importlib.import_module(req_lib[0])
        #print("Found", req_lib[0], var.__version__)

        if len(req_lib) == 2:
            if var.__version__ != req_lib[1]:
                print("Module ", req_lib[0], "has incompatible version", var.__version__, "Required version is", req_lib[1])

    except Exception as e:
        if len(req_lib) == 2:
            print(e, "Required version is ", req_lib[1])
        else:
            print(e)
        continue