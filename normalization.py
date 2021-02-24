import numpy as np
import nibabel as nib

def image_normalization(input_file_path):
    img = nib.load(input_file_path + '.nii')
    m = img.shape[0]
    n = img.shape[1]
    p = img.shape[2]
    totalvoxels = m * n * p
    volume = img.get_fdata()
    Array = volume.ravel()
    numberofzero = np.count_nonzero(Array == 0)
    Alpha = np.double(totalvoxels) / np.double((totalvoxels - numberofzero))
    Exp = sum(Array) / totalvoxels
    Exp2 = sum(np.power(Array, 2)) / totalvoxels
    Mean_in_mask = Exp * Alpha
    SD_in_mask = ((Alpha * Exp2) - (Alpha * Exp) ** 2) ** 0.5
    Normalized = (volume - Mean_in_mask) / SD_in_mask
    ni_img = nib.Nifti1Image(Normalized, img.affine)
    nib.save(ni_img, input_file_path + '_normalized')