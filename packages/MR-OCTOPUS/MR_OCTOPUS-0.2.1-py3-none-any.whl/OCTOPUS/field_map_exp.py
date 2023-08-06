from OCTOPUS.fieldmap.unwrap import fsl_prep

rawdat_path = r'C:\Users\marin\Documents\PhD\B0inhomogeneity\Data\DWI\rawdata_fieldmap.mat'
dicom_path = r'C:\Users\marin\Documents\PhD\B0inhomogeneity\Data\DWI\b0maps_for_dwi.mat'
dst_folder = r'C:\Users\marin\Documents\PhD\B0inhomogeneity\Data\DWI'
dTE = 2.46e-3



fsl_prep(rawdat_path, dicom_path, dst_folder, dTE)