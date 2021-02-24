#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:45:11 2021

@author: farrokh
"""

import os
import tempfile
temp_path = tempfile.gettempdir()

'''
status_codes
102 : processing
200 : ok (done!)
500 : internal server error
'''

def send_status(request_id, status, status_code):
    status = 'request_id = %s, %s, status_code = %s'%(request_id, status, status_code)
    print(status)
    with open(os.path.join(temp_path, 'deepmedicModule_status.txt'), 'w') as f:
        f.write(status)
