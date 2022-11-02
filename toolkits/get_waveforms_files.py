import os

from obspy import read

# --------------------------------------------------------
def get_waveforms_files(path: str, format = None) -> list:
    '''
    - Description: this function focuses on finding the paths of the requested file type located inside an input path.

    - Input parameters:
        <<< path   : str
                     Main path                         (e.g. '/home/eguzmanv/data')
        <<< format : str
                     Format type of the requested file (e.g. 'EVT', 'GCF', 'MSEED' ...)

    - Returns:
        >>> fpaths : list
                    List of paths of the requested file type
    '''
    
    # File extensions
    fextensions = {
                   'MSEED': ['mseed', 'MSEED', 'seed'],
                   'EVT'  : ['evt', 'EVT'],
                   'GCF'  : ['gcf', 'GCF']
                  }
        # Get list of file extensions
    fextensions_list = [ext for list_ in list(fextensions.values()) for ext in list_]

    # Waveform formats
    wv_formats = {
                  'MSEED' : ['MSEED'],
                  'EVT'   : ['KINEMETRICS_EVT'],
                 }
    wv_formats_list = [format for list_ in list(wv_formats.values()) for format in list_]

    fpaths = []                                                     # empty list of files paths
    
    # Loop: find paths of the files which end with '.format'
    for root_path, dirs, files in os.walk(path):
        
        # Loop: append each file in files_list list (if that's the case)
        for file in files:

            # Condition: file ends with '.format' or not
            if format != None: 
                
                if (format in fextensions_list) and (file.endswith(tuple(fextensions_list))):                  # e.g. if format = 'EVT', then the 'N001.EVT' file applies
                    fpaths.append(os.path.join(root_path, file))
                    continue
                
                elif (format in fextensions_list) and (not file.endswith(tuple(fextensions_list))):
                    
                    try:
                        
                        st = read(root_path, file)
                        if (st[0].stats._format in wv_formats_list):
                            pass
                    
                    except:
                        continue

            else:
                fpaths.append(os.path.join(root_path, file))

    return fpaths


