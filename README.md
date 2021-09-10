# deepmedic_project
Tumor Segmentation in Brain MRI Images

The goal of this project is to segment tumors in brain MRI images based on [deepMedic](https://www.sciencedirect.com/science/article/pii/S1361841516301839). This project has been tested and works on both Windows and Ubuntu.
<p align="center"><img src="https://github.com/farrokhkarimi/deepmedic_project/blob/main/documentation/deepMedic.png" /></p>

# Installation and Requirements
Install the required packages using the requirements.txt file:
```
pip3 install requirements.txt
```
Install GDCM package based on your operating system:

**- Linux:**
```
sudo apt update
sudo apt install libgdcm2.4
sudo apt install libgdcm-tools
```

**- Windows:**

Download and install GDCM from [http://gdcm.sourceforge.net/](http://gdcm.sourceforge.net/) or [https://sourceforge.net/projects/gdcm/](https://sourceforge.net/projects/gdcm/)

**Note:** Install the CUDA and cuDNN requirements if you want to use the GPU.

# Running the Software
Run wsgi.py if you want to have a local web service and run client_test_request.py to send a local request to the service.

**Server-side:**
```
python3 wsgi.py
```

**Client-side:**
```
python3 client_test_request.py
```
Run project_runner.py to execute the main project process directly:
```
python3 project_runner.py
```
You should define the project output path and data path in the project_runner or client_test_request script. You must also define the processor between `cpu` or `cuda` as GPU. A sample data is placed in the dicom_images folder. Also, the saved model is placed in the model folder.

**Note** for large images: Large 3D CNNs are computationally expensive. Consider downsampling the images or reducing the size of the network if you encounter computational difficulties.

# Sample Data
<p align="center"><img src="https://github.com/farrokhkarimi/deepmedic_project/blob/main/documentation/sample.png" /></p>

# Result
<p align="center"><img src="https://github.com/farrokhkarimi/deepmedic_project/blob/main/documentation/result.png" /></p>

# Acknowledgments
It should be noted that this project was done for [MarcoPax](https://www.marcopacs.com/en/) company.

# Author
**Developed** by [Farrokh Karimi](https://farrokhkarimi.github.io/)
