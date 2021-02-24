#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 12:28:37 2021

@author: farrokh
"""

import os
import tempfile
temp_path = tempfile.gettempdir()

from flask import Flask, request

from deepmedic_process import deepmedic_process

app = Flask(__name__)

tmp_status_txt_file_path = os.path.join(temp_path, 'deepmedicModule_status.txt')
if os.path.exists(tmp_status_txt_file_path):
    os.remove(tmp_status_txt_file_path)
    
tmp_result_txt_file_path = os.path.join(temp_path, 'deepmedicModule_result.txt')
if os.path.exists(tmp_result_txt_file_path):
    os.remove(tmp_result_txt_file_path)

@app.route('/deepmedic/run', methods=['GET', 'POST'])
def get_input_json_string_and_run_project():
    input_json_string = request.json
    output_json_string = deepmedic_process(input_json_string)
    return(output_json_string)

@app.route('/deepmedic/status', methods=['GET', 'POST'])
def get_status():
    if os.path.exists(tmp_status_txt_file_path):
        with open(os.path.join(tmp_status_txt_file_path), 'r') as status_file:
            return(status_file.read())
    else:
        return('There is no status yet')

@app.route('/deepmedic/result', methods=['GET', 'POST'])
def get_result():
    if os.path.exists(tmp_result_txt_file_path):
        with open(os.path.join(tmp_result_txt_file_path), 'r') as result_file:
            return(result_file.read())
    else:
        return('No result have been generated yet')
    
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port='5000' ,debug=True)