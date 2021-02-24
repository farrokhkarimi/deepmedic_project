#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: farrokh
"""

import os
import sys
import json
import time
import tempfile
import platform
import subprocess

import dicom2nifti

from send_status import send_status
from normalization import image_normalization
from deepmedic_config import deepmedic_config

sys.path.append(os.path.join(os.getcwd(), 'deepmedic'))
from deepmedic_run import deepmedic_runner

os.environ['FSLOUTPUTTYPE'] = 'NIFTI'

os_type = platform.system()

if os_type == 'Linux':
    executer = 'wine '
elif os_type == 'Windows':
    executer = ''

def init(input_json_string):
    input_json = json.loads(input_json_string)
    project_path = os.getcwd()
    request_id = input_json['request_id']
    output_path = input_json['output_data'][0]['path']
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    dicoms_paths = dict([(el['tag'] , el['path']) for el in input_json['input_images']])
    niftis_path = os.path.join(output_path, 'niftis_request_%s'%request_id)
    if not os.path.exists(niftis_path):
        os.makedirs(niftis_path)
    flirt_path = os.path.join(project_path, 'utilities', 'flirt.exe')
    bet2_path = os.path.join(project_path, 'utilities', 'bet2.exe')
    config_files_path = os.path.join(project_path, 'configFiles')
    saved_model_path = os.path.join(project_path, 'model', 'TrainedModel', 'deepMedic.trainSessionDm.final.2020-06-18.20.55.20.742338.model.ckpt')
    processor = input_json['processor']
    temp_path = tempfile.gettempdir()
    with open(os.path.join(temp_path, 'deepmedicModule_status.txt'), 'w') as f:
        f.write('None')
    with open(os.path.join(temp_path, 'deepmedicModule_result.txt'), 'w') as f:
        f.write('No result have been generated yet')
    return (request_id, output_path, dicoms_paths, niftis_path, flirt_path, bet2_path, config_files_path, saved_model_path, processor, temp_path)

def deepmedic_process(input_json_string):
    t = time.time()
    
    request_id, output_path, dicoms_paths, niftis_path, flirt_path, bet2_path, config_files_path, saved_model_path, processor, temp_path = init(input_json_string)
    
    # dicom2nifti
    send_status(request_id, 'dicom2nifti conversion started', 102)
    for i in list(dicoms_paths.keys()):
        dicom2nifti.dicom_series_to_nifti(dicoms_paths[i], os.path.join(niftis_path, i))
        send_status(request_id, '%s converted to nifti'%i, 102)
    
    # register flair based on t1c
    send_status(request_id, 'registration started', 102)
    try:
        subprocess.run('{0}{1} -in {2} -ref {3} -out {2}_registered -interp nearestneighbour'.format(executer, flirt_path, os.path.join(niftis_path, 'flair'), os.path.join(niftis_path, 't1c')), shell=True, check=True)
        send_status(request_id, 'flair registered based on t1c', 102)
    except subprocess.CalledProcessError as error:
        send_status(request_id, 'registration failed. error: %s'%error, 500)
    
    # brain_extraction
    send_status(request_id, 'brain extraction started', 102)
    try:
        subprocess.run('{0}{1} {2}.nii {2}_brain.nii -m'.format(executer, bet2_path, os.path.join(niftis_path, 'flair_registered')), shell=True, check=True)
        send_status(request_id, 'flair brain extracted', 102)
        subprocess.run('{0}{1} {2} {2}_brain -m'.format(executer, bet2_path, os.path.join(niftis_path, 't1c')), shell=True, check=True)
        send_status(request_id, 't1c brain extracted', 102)
    except subprocess.CalledProcessError as error:
        send_status(request_id, 'brain extraction failed. error: %s'%error, 500)
    
    # image_normalization
    send_status(request_id, 'image normalization started', 102)
    image_normalization(os.path.join(niftis_path, 'flair_registered_brain'))
    send_status(request_id, 'flair normalized', 102)
    image_normalization(os.path.join(niftis_path, 't1c_brain'))
    send_status(request_id, 't1c normalized', 102)
    
    #config and run
    send_status(request_id, 'deepmedic running started', 102)
    test_flair_file_name = 'flair_registered_brain_normalized.nii'
    test_t1c_file_name = 't1c_brain_normalized.nii'
    mask = 't1c_brain_mask.nii'
    prediction_file_name = 'predic_flair.nii.gz'
    deepmedic_config(config_files_path, niftis_path, test_flair_file_name, test_t1c_file_name, mask, prediction_file_name, output_path)
    model_cfg_file_path = os.path.join(config_files_path, 'model', 'modelConfig.cfg')
    test_cfg_file_path = os.path.join(config_files_path, 'test', 'testConfig.cfg')
    result = deepmedic_runner(device_name=processor,
                              model_cfg_file_path=model_cfg_file_path,
                              test_cfg_file_path=test_cfg_file_path,
                              train_cfg_file_path=None,
                              saved_model_path=saved_model_path,
                              reset_trainer=False)
    
    send_status(request_id, 'the project successfully ran in %s seconds' % int(time.time()-t), 200)
    output_seg_path = os.path.join(output_path, 'predictions', 'testSessionDm', 'predictions', 'predic_flair_Segm.nii.gz')
    output_json_dict = {
        "request_id" : request_id,
        "result" : result,
        "generated_files" : {"tag" : "flair", "path" : output_seg_path},
        }
    
    with open(os.path.join(temp_path, 'deepmedicModule_result.txt'), 'w') as result_file:
        result_file.write(str(output_json_dict))
    
    return json.dumps(output_json_dict)
