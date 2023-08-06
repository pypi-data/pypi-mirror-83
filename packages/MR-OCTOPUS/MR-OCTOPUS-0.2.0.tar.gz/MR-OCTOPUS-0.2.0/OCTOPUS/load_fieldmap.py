import math
import matplotlib.pyplot as plt

from OCTOPUS.utils.dataio import get_data_from_file


fieldmap_path = r'C:\Users\marin\Documents\PhD\B0inhomogeneity\Data\DWI\fieldmap_unwrapped.nii.gz'

fmap = get_data_from_file(fieldmap_path) / (2 * math.pi)

plt.imshow(fmap[:,:,1], cmap='gray')
plt.axis('off')
plt.colorbar()
plt.title('Field map')
plt.show()

print('Hello')