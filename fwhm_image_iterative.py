import os

os.system('clear')
print("FWHM Calculation")
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def find_fwhm(arr):

    half_max = 0.5*np.max(arr)
    r = np.linspace(0,60,60,True)
    f = CubicSpline(r, arr-half_max, bc_type='natural')     # perform interpolation for intermediate values
    r_new = np.linspace(0,60,6000,True)
    points = [i for i in r_new if f(i) > 0]                 # find points where value equals half max
    return max(points) - min(points)

path = '/Users/kajetan/Documents/GATE_macros/1Ring_twoPS_spat/two_ps_recon/'

img = []                                              #   Create empty array for input data
inputdata_path = os.path.join(path, 'InputData.txt')
iterations = 0

fwhm_array_x = []
fwhm_array_y = []
fwhm_array_z = []

with open(inputdata_path) as fp:     #   Open file containing data list, each line is a file to be loaded
    line = fp.read().splitlines()       
    for fn in line:
        
        iterations += 1

        img = np.fromfile(os.path.join(path,'two_ps_recon_it'+fn), dtype=np.float32).reshape((160,160,160),order='F')
        print(str(os.path.join(path,'two_ps_recon_it'+fn)))
        print("Max: "+str(np.max(img)))
        print("Min: "+str(np.min(img)))
        print(np.shape(img))

        rd_fov_img = img[50:110, 50:110, 50:110]    # make reduced FOV to measure central PS closely
        print(np.shape(rd_fov_img))
        index_max = np.unravel_index(np.argmax(rd_fov_img, axis=None), rd_fov_img.shape)    # array with indices
        print("index: "+str(index_max))
        
        x_points = rd_fov_img[:,index_max[1],index_max[2]]
        y_points = rd_fov_img[index_max[0],:,index_max[2]]
        z_points = rd_fov_img[index_max[0],index_max[1],:]

        fwhm_x = find_fwhm(x_points)*2.5
        fwhm_array_x.append(fwhm_x)
        print("\nIteration "+str(iterations)+" FWHM_x: "+str(fwhm_x)+" mm")
        fwhm_y = find_fwhm(y_points)*2.5
        fwhm_array_y.append(fwhm_y)
        print("Iteration "+str(iterations)+" FWHM_y: "+str(fwhm_y)+" mm")
        fwhm_z = find_fwhm(z_points)*2.5
        fwhm_array_z.append(fwhm_z)
        print("Iteration "+str(iterations)+" FWHM_z: "+str(fwhm_z)+" mm\n")

#   Plot production
plt.imshow(img[:,:,80])
plt.show()

plt.imshow(rd_fov_img[:,:,30])
plt.show()

plt.plot(x_points)
plt.legend("x points")
plt.show()

plt.plot(y_points)
plt.legend("y points")
plt.show()

plt.plot(z_points)
plt.legend("z points")
plt.show()

plt.plot(range(1,iterations+1),fwhm_array_x, label = "FWHM_X")
plt.plot(range(1,iterations+1),fwhm_array_y, label = "FWHM_Y")
plt.plot(range(1,iterations+1),fwhm_array_z, label = "FWHM_Z")
plt.legend()
plt.ylabel('FWHM in mm')
plt.xlabel('iteration')
plt.xticks(range(1,iterations+1))
plt.show()