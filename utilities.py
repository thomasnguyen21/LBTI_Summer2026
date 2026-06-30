# Import packages
import numpy as np
from astropy.io import fits

# Define a function to create an averaged FITS file from a list of FITS file
def average_fits(filelist):
    '''
    This function averages the FITS file and creates an updated header with information about averaging
    Args:
        filelist: an array that contains paths to the files to be averaged
    Returns:
        A NumPy array that represents the averaged FITS data and a dictionary that represents the updated header
    '''
    # Create an empty array to store our FITS files to be averaged 
    image_frames = [None]*len(filelist)
    
    # Extract image data and store in the array above
    for i, filename in enumerate(filelist):
        image_data = fits.getdata(filename)
        image_frames[i] = image_data
    
    # Average all the frames in the updated NumPy array
    mean_imagedata = np.average(image_frames,axis=0)
    
    # Carry over first image header and add information on averaging
    original_header = fits.getheader(filelist[0])
    mean_header = fits.Header()
    mean_header = original_header
    mean_header["Reduction"] = f"Average {len(filelist)} files."
    
    # Return the averaged FITS data and updated header
    return mean_imagedata, mean_header
    