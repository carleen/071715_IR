'''This statement allows you to use the pyfits package,
which is useful for processing fits images'''
import pyfits as pyfits 
import matplotlib.pyplot as plt
import numpy as np

class FormatInError(Exception):
    pass

''' Asks for the file name and tries to open the file. Throws an error
if the file can't be opened or found.'''
def get_root_name():
    while True:
        try:
            root_name = raw_input('Enter the name of the files: ')
            file = open(root_name + '1.fts')
            break
        except IOError:
            print("Error: improper root file name or missing files.")
    return root_name

''' Calculates the gain for the image. '''  
def get_mad_gains_breh():
    dark = pyfits.getdata('dark.fts')
    hdulist = pyfits.open('dark.fts')
    hdulist.info()
    flat = pyfits.getdata('flat_beg.fts')
    median_value = pyfits.np.median(flat)
    sub = flat - dark
    # the following nexted for loop checks for values that would cause error
    for i in range (0, 251, 1):
        for j in range (0, 315, 1):
            if sub[0][i][j] == 0:
                sub[0][i][j] = 1
    gain = median_value/(sub)
    return gain

''' Plots the corrected image.'''
def flat_fielding(gain, root_name):
    dark = pyfits.getdata('dark.fts')
    for i in range(9, 10, 1):
        science_file = pyfits.getdata(root_name + str(i) + '.fts') 
        final = (science_file - dark)*gain
        write_fits_file(final, i)
        plt.imshow(final[0], cmap = 'gray')
        plt.show()

def write_fits_file(corrected_image, i):
    pyfits.writeto(str(i) + '_corrected.fit', corrected_image)

if __name__ == "__main__":
    root_name = get_root_name()
    gain_frame = get_mad_gains_breh()
    flat_fielding(gain_frame, root_name)

