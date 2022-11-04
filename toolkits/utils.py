import os
import glob

from obspy import read
# ----------------------------------------------------------------
def validate(func, locals):
    '''
    - Description: this function validates parameter types for a specific function. 
    '''
    for var, test in func.__annotations__.items():
        if var == "return":
            continue
        value = locals[var]
        msg = f"Error in {func}: {var} argument must be {test}"
        assert isinstance(value,test),msg

# ----------------------------------------------------------------
def validate_mseed_consistency(ifolder: str):
    '''
    - Description: validate the consistency between data and file name of mseed files.
    '''
    # Get dir paths (paths of each channel dir)
    dpaths = sorted(glob.glob(os.path.join(ifolder, '*', '*', '*', '*')))

    for dir_path in dpaths:

        files = sorted(os.listdir(dir_path))

        for file in files:
            file_path = os.path.join(dir_path, file)

            net_, sta_, loc_, cha_, dq_, year_, julday_ = file.split('.')

            st = read(file_path)
            starttime_, endtime_ = st[0].stats.starttime, st[0].stats.endtime
        
            if starttime_.julday == endtime_.julday == int(julday_):
                print(file_path, ' [OK]')
            else:
                print(file_path, ' [ERROR]')