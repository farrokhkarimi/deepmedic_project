# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 13:21:28 2021

@author: Farrokh
"""

import os
import shutil
import requests

output_path = "/home/karimi/tmp/outputs"
if os.path.exists(output_path):
    shutil.rmtree(output_path)

# processor could be 'cpu' or 'cuda' for gpu

input_json_string = """
{
    "request_id" : 0,
    "processor" : "cpu",
    "input_images" : [{"tag":"flair", "path":"C:/Users/Farrokh/tmp/dicoms/flair", "modality" : "mri"},
                      {"tag":"t1c", "path":"C:/Users/Farrokh/tmp/dicoms/t1c", "modality" : "mri"}],
    "output_data" : [{"tag":"flair", "path":"%s"}]
}
"""%output_path

res = requests.post('http://localhost:5000/deepmedic/run', json=input_json_string)

print(res.json())