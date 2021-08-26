import os
os.system('clear')
print("FWHM Calculation")

import numpy as np
import matplotlib.pyplot as plt

def normalize(arr): #   Need 3D array
    for s in range(arr.shape[0]):        
        arr[s,:,:] = (arr[s,:,:]-np.min(arr[s,:,:])) / (np.max(arr[s,:,:])-np.min(arr[s,:,:]))
    return arr

path = '/Users/kajetan/Documents/GATE_macros/1Ring_twoPS_spat/two_ps_recon/two_ps_recon_it20.img'
img = np.fromfile(path, dtype=np.int32).reshape((160,160,160),order='F')

print(np.shape(img))
print("Max: "+str(np.max(img)))
print("Min: "+str(np.min(img)))
print(np.shape(img))

plt.imshow(img[:,:,79])
plt.show()

rd_fov_img = img[50:110, 50:110, 50:110]    # make reduced FOV to measure central PS closely
print(np.shape(rd_fov_img))
plt.imshow(rd_fov_img[:,:,15])
plt.show()

half_max = 0.5*(np.max(rd_fov_img)-np.min(rd_fov_img)) # calculate half of peak value
print("Half_max: "+str(half_max))
max_position = np.argmax(rd_fov_img[:,:,15])    # find index of max in image
print("Max_position: "+str(max_position))

right_index = np.argmin(np.abs(rd_fov_img[0:max_position,0:max_position,15]-half_max))
left_index = np.argmin(np.abs(rd_fov_img[max_position:,max_position:,15]-half_max))
fwhm = right_index-left_index
print(fwhm)