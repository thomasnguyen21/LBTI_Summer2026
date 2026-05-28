import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob


def create_file_list(file_paths):
    file_list = glob.glob(file_paths)
    return file_list


# getting an average file for a given list of files, carrying over header
# filelist is a list of the full fits files, filetype is light or dark files
def average_files(filelist, filetype):

    #making a list of the data from each fits file
    file_concat = [fits.getdata(image) for image in filelist]

    #finding the mean (averaging the files)
    #.astype(np.float32) shrinks the acuracy of the estimation, since the mean auto
    #defaults to float64, so this will make the file smaller
    final_file_data = np.mean(file_concat, axis=0).astype(np.float32)

    #carry over first image header and add information on averaging
    original_header = fits.getheader(filelist[0])
    new_header = original_header.copy()
    # will return something of the style: averaged 10 light files
    new_header['HISTORY'] = f"averaged {len(filelist)} {filetype} files"
    # gives numeber of averaged files
    new_header['NFILES'] = len(filelist)
    new_header['METHOD'] = 'MEAN'

    return final_file_data, new_header

# making a net light file, and adjusting the header to reflect this
def calculate_difference(lightdata, darkdata, header):
    # calculate difference in light and dark files
    net_data = lightdata - darkdata

    #adjust header for new net_data file
    new_header = header.copy()
    new_header['HISTORY'] = f"difference between averaged light and dark file data"
    return net_data, new_header

#creating and saving a new fits file to my computer
def create_file(filename, filedata, header):
    hdu = fits.PrimaryHDU(filedata, header=header)
    hdu.writeto(filename, overwrite=True)

if __name__ == "__main__":
    # I kept the basic structure and only changed the folder when creating 
    # the dark and light file list, with each folder assigned to fast, med, or slow
    light_files = create_file_list(r"C:\Users\brie_\OneDrive - University of Arizona\Documents\2026 Summer Research LBT\Downloaded Files\Week 2\Week 2 Fits\Slow Light\*.fits.gz")
    avg_light, light_header = average_files(light_files, "light")
    dark_files = create_file_list(r"C:\Users\brie_\OneDrive - University of Arizona\Documents\2026 Summer Research LBT\Downloaded Files\Week 2\Week 2 Fits\Slow Dark\*.fits.gz")
    avg_dark, dark_header = average_files(dark_files, "dark")
    net_data, net_header = calculate_difference(avg_light, avg_dark, light_header)
    create_file("avg_slow_light_image_week2.fits", avg_light, light_header)
    create_file("avg_slow_dark_image_week2.fits", avg_dark, dark_header)
    create_file("net_slow_image_week2.fits", net_data, net_header)