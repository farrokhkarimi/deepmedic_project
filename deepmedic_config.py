import os

def deepmedic_config(config_files_path, niftis_path, test_flair_file_name, test_t1c_file_name, mask, prediction_file_name, output_path):
    
    with open(os.path.join(config_files_path, 'model', 'modelConfig.cfg'), 'r') as f:
        lines = f.readlines()
        lines[8] = 'folderForOutput = "%s"\n' % output_path
        
    with open(os.path.join(config_files_path, 'model', 'modelConfig.cfg'), 'w') as f:
        f.writelines(lines)
    
    with open(os.path.join(config_files_path, 'test', 'testConfig.cfg'), 'r') as f:
        lines = f.readlines()
        lines[8] = 'folderForOutput = "%s"\n' % output_path
        
    with open(os.path.join(config_files_path, 'test', 'testConfig.cfg'), 'w') as f:
        f.writelines(lines)
        
    with open(os.path.join(config_files_path, 'test', 'testChannels_flair.cfg'), 'w') as f:
        f.write(os.path.join(niftis_path, test_flair_file_name))
        
    with open (os.path.join(config_files_path, 'test', 'testChannels_t1c.cfg'), 'w') as f:
        f.write(os.path.join(niftis_path, test_t1c_file_name))
        
    with open(os.path.join(config_files_path, 'test', 'testRoiMasks.cfg'), 'w') as f:
        f.write(os.path.join(niftis_path, mask))
        
    with open(os.path.join(config_files_path, 'test' 'testNamesOfPredictions.cfg'), 'w') as f:
        f.write(prediction_file_name)