import os
import glob

import obspy
from obspy import read, UTCDateTime

from toolkits.utils import validate
from toolkits.wv_conversion.wv_fnames.wv_fpaths import get_wv_fpaths, get_sc_mseed_fpaths

# ---------------------------------------
def rename_uptade_mseed(ifolder: str):
    '''
    - Description: Restructure a group of .mseed files in a format 'net.sta.loc.cha.YYYYMMDDThhmmss' 
                   (where 'YYYYMMDDThhmmss' is the starttime of the trace) to the format 
                   'net.sta.loc.cha.year.julday'.
                       
                   This function reads a list of dirs paths, goes to each file present in each dir 
                   and reads them to define if it needs to be renamed or updated (via the method: 
                   obspy.core.stream.Stream.merge).

    - Input parameters:
        <<< ifolder : str
                      Path of input folder

    - Returns:
        >>> renamed files in the format: 'net.sta.loc.cha.julday'

    - Code sections:
        1. List files
            >>> output of interest: files (list)
        2. Rename or overwrite existing files
    '''
    
    validate(rename_uptade_mseed, locals())                                                    # validate the type of input parameters

    # Get dir paths (paths of each channel dir)
    dpaths = sorted(glob.glob(os.path.join(ifolder, '*', '*', '*', '*')))

    # Loop: go through each directory
    for dpath in dpaths:

        # =============
        # 1. List files
        # =============

        files = sorted(os.listdir(dpath))                                                      # list of files in dir_path

        # Loop: loop through each file on dir_path
        for file in files:                                     
            fpath = os.path.join(dpath, file)                                                  # file path
            net, sta, loc, cha, dq, year, starttime = file.split('.')                          # extract SEED naming from filename
            
            # =====================================
            # 2. Rename or overwrite existing files
            # =====================================

            # Condition: the file ends with a term of length != 3? 
            if len(starttime) != 3:                                                            # the file is in format net.sta.loc.cha.YYYYMMDDThhmmss

                julday = UTCDateTime(starttime).julday                                         # julday

                existing_jd_fpath = get_sc_mseed_fpaths(dpath = dpath, julday = f'{julday:03}')# list a pre-existing file that ends with that julday
                
                # Condition: does a file exist with that julday in its name? If not rename that file, otherwise, update it
                if len(existing_jd_fpath) == 0:                                                # renaming the file
                    
                    # File characteristics
                        # new file name of the .mseed file
                    new_fname = f'{net}.{sta}.{loc}.{cha}.{dq}.{year}.{julday:03}'             # e.g. net.sta.loc.cha.D.001
                        # new file path of the .mseed file
                    new_fpath = os.path.join(dpath, new_fname)                                 # e.g. ../test/2017/CM/CSLUI/HNZ.D/RED_ANTIOQUIA.CSLUI.10.HNZ.D.001 

                    # Rename file
                    os.rename(fpath, new_fpath)

                    print(new_fpath, ' [CREATED]')

                else:                                                                          # update/overwrite the file
                    
                    existing_fpath = existing_jd_fpath[0]                                      # path of the existing file
                    
                    # Read stream
                    st_ = read(existing_fpath)                                                 # format: net.sta.loc.cha.D.001

                    # Add the new stream and compile the result using 'merge'
                    st_ += read(fpath)                                                         # format: net.sta.loc.cha.YYYYMMDDThhmmss
                    st_.merge(method = 1, fill_value = 'interpolate')

                    # Overwrite and export the existing file
                    st_.write(existing_fpath, format = 'MSEED', encoding = 'STEIM2')           # format: net.sta.loc.cha.D.001

                    # Remove the file in format net.sta.loc.cha.YYYYMMDDThhmmss
                    os.remove(fpath)

                    print(existing_fpath, ' [updated]')
