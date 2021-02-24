#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 12:28:37 2021

@author: farrokh
"""

import os
import shutil

from deepmedic_process import deepmedic_process

output_path = "/home/karimi/tmp/outputs"
if os.path.exists(output_path):
    shutil.rmtree(output_path)

# processor could be 'cpu' or 'cuda' for gpu

input_json_string = """
{
    "request_id" : 0,
    "processor" : "cuda",
    "input_images" : [{"tag":"flair", "path":"/home/karimi/tmp/dicoms/flair", "modality" : "mri"},
                      {"tag":"t1c", "path":"/home/karimi/tmp/dicoms/t1c", "modality" : "mri"}],
    "output_data" : [{"tag":"flair", "path":"%s"}]
}
"""%output_path

output_json_string = deepmedic_process(input_json_string)

print(output_json_string)