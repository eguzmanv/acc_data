import os

from obspy import read

# --------------------------------------------------------
def get_waveforms_files(path: str, fmt_type = None,) -> list:
    '''
    - Description: Find the paths of the requested format type located inside an input path.
                   Format types by default: MSEED, 'EVT', GCF.

    - Input parameters:
        <<< path     : str
                       Main path                         (e.g. '/home/eguzmanv/data')
        <<< fmt_type : str, default None
                       Format type of the requested file (e.g. 'EVT', 'GCF', 'MSEED' ...)
                       If None, the function returns all available waveform paths

    - Returns:
        >>> fpaths   : list
                       List of paths of the requested file type

    - Code sections:
        1. Define some useful dictionaries
        2. Append file paths to list
    '''
    # ==================================
    # 1. Define some useful dictionaries
    # ==================================

    # File extensions
    f_exts_dict = {
                   'MSEED': ['mseed', 'MSEED', 'seed'],
                   'EVT'  : ['evt', 'EVT'],
                   'GCF'  : ['gcf', 'GCF'],
                   'SAC'  : ['sac', 'SAC']
                  }
        # Get list of file extensions
    f_exts_list = [ext for list_ in list(f_exts_dict.values()) for ext in list_]

    # Waveform formats
    wv_fmts_dict = {
                    'MSEED' : 'MSEED',
                    'EVT'   : 'KINEMETRICS_EVT',
                    }
        # List of waveform formats
    wv_fmts_list = list(wv_fmts_dict.values())
    
    # =========================
    # Append file paths to list
    # =========================

    fpaths = []                                                                                       # empty list of files paths
    
        # Loop: go through each dirpath, dirs and files in input path
    for dpath, dirs, files in os.walk(path):
            # Loop: go through each file in files
        for file in files:

                # Condition: a format type was requested?
                    # Format type requested
            if fmt_type != None: 
                        
                        # Condition: is the fmt_type in file extension lists and this file ends with that extension?
                            # File with extension
                if file.endswith(tuple(f_exts_dict[fmt_type])):                                       
                    fpaths.append(os.path.join(dpath, file))
                    continue
                            # File without extension
                else:
                    if not file.endswith(tuple(f_exts_list)):     
                                # Try to read the file with obspy read() function 
                        try:
                                        # Read stream and get the format type of waveform
                            st     = read(os.path.join(dpath, file))                                   # stream object
                            wv_fmt = st[0].stats._format                                               # format type of waveform
                                                                                                       # e.g. 'KINEMETRICS_EVT' for EVT files
                                                                                                       # e.g. 'MSEED' for mseed files ...
                                        # Verify if the file type is in the file extensions
                            key_idx = list(wv_fmts_dict.values()).index(wv_fmt)                        # file type index
                            ftype   = list(wv_fmts_dict.keys())[key_idx]                               # file type

                            if ftype in f_exts_dict[fmt_type]:
                                fpaths.append(os.path.join(dpath, file))
                            
                            continue 
        
                        except:
                            continue
                    else:
                        continue

                    # A format type was not requested
            else:
                        # Condition: verify if the file extension is in f_exts_list
                if file.endswith(tuple(f_exts_list)):     
                    fpaths.append(os.path.join(dpath, file))
                else:
                            # Try to read the file with obspy read() function
                    try:
                        st     = read(os.path.join(dpath, file))                                       # stream object
                        fpaths.append(os.path.join(dpath, file))
                    except:
                        continue

    return fpaths


