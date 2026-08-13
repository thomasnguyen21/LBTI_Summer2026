import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob
import os

# goes through the files in a folder and creates a list composed of the files, where the 
# part of the file titles that makes them distinct is replaced by * for example *.fits
def create_file_list(file_paths):
    file_list = glob.glob(file_paths)
    return file_list

# given a list of files and a string describing the type of files, creates a new averaged 
# file with an updated header
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

# takes a list of files, averages the files, then subtracts a supplied mean sky background 
# file creating a new file with an updated header
def reduce_files(filelist, filetype, skyfile):
    # make an average sky file for a given sky position
    avg_file = average_files(filelist, filetype)

    # subtract the average sky background from the newly averaged sky file
    reduced = avg_file[0] - skyfile[0]

    # copy over the header of the averaged sky position and 
    # add more doccumentation
    new_header = avg_file[1].copy()
    new_header['HISTORY'] = "reduced by subtracting averaged sky image"

    return reduced, new_header

# makes a new file based on a string name (that must end in .fits), the new data you created, 
# and an updated header
def create_file(filename, filedata, header):
    hdu = fits.PrimaryHDU(filedata, header=header)
    hdu.writeto(filename, overwrite=True)

if __name__ == '__main__':

    # average the left sky background files
    left_sky = average_files(create_file_list(r"C:\Documents\2026 Summer Research LBT\Downloaded Files\Week 8\Left Sky\*.fits.gz"), "left mirror sky")

    # same to the right sky background files
    right_sky = average_files(create_file_list(r"C:\Documents\2026 Summer Research LBT\Downloaded Files\Week 8\Right Sky\*.fits.gz"), "right mirror sky")
    
    # loop through left science folders
    left_folders = glob.glob(
        r"C:\Documents\2026 Summer Research LBT\Downloaded Files\Week 8\Left\*"
    )

    for folder in left_folders:
        file_list = create_file_list(os.path.join(folder, "*.fits.gz"))
        reduced = reduce_files(file_list, "left side mirror", left_sky)
        create_file(f"left_sky_reduced_line_{os.path.basename(folder)}.fits",
                    reduced[0], reduced[1])


    # loop through right science folders
    right_folders = glob.glob(
        r"C:\Documents\2026 Summer Research LBT\Downloaded Files\Week 8\Right\*"
    )

    for folder in right_folders:
        file_list = create_file_list(os.path.join(folder, "*.fits.gz"))
        reduced = reduce_files(file_list, "right side mirror", right_sky)
        create_file(f"right_sky_reduced_line_{os.path.basename(folder)}.fits",
                    reduced[0], reduced[1])