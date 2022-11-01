import os

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
        >>> flist : list
                         List of paths of the requested file type
    '''
    
    fpaths = []                                                     # empty list of files paths
    
    # Loop: find paths of the files which end with '.format'
    for root_path, dirs, files in os.walk(path):
        
        # Loop: append each file in files_list list (if that's the case)
        for file in files:

            # Condition: file ends with '.format' or not
            if format != None: 
                
                if file.endswith(f'.{format}'):                  # e.g. if format = 'EVT', then the 'N001.EVT' file applies
                    fpaths.append(os.path.join(root_path, file))
                
                continue
            else:
                fpaths.append(os.path.join(root_path, file))

    return fpaths


