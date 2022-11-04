import os
import obspy
from obspy import read, UTCDateTime

from toolkits.utils import validate
from toolkits.wv_conversion.wv_medatada.SEED_naming import set_SEED_naming

# --------------------------------------------------------------------------------------
def write_mseed(tr: obspy.core.trace.Trace, output_folder: str, network = None):
    '''
    - Description: Export a trace object as format MSEED from a trace, network and 
                   output folder as input.

    - Input parameters:
        <<< tr            : obspy.core.trace.Trace
                            Input trace
        <<< network       : str
                            Input network                 (e.g. 'CM')
        <<< output_folder : str
                            Output directory path

    - Returns:
        >>> exported      : bool
                            True if the waveform was writed as mseed
                            False if the waveform was reseted (starttime < year 2000)

        - Code sections:
            1. Set file naming
                >>> output of interest: file_name, file_path (str)
            2. Edit the NSLC naming in the stats
                >>> Expected result: trace.stats edited
            3. Export mseed file
                >>> Expected result: .mseed exported
    '''
    validate(write_mseed, locals())                                                                    # validate the type of input parameters
    # ==================
    # 1. Set file naming
    # ==================

        # SEED naming
    net, sta, loc, cha = set_SEED_naming(tr, network = network).split('.')                           # extract net, cha, loc and cha codes
            
            # some considerations
    dq = 'D' # !!!!                                                                                  # set data quality

        # Time window
    starttime, endtime = tr.stats.starttime, tr.stats.endtime                                        # starttime and endtime (obspy.core.utcdatetime.UTCDateTime)
    
        # File characteristics
            # .mseed file name
    fname = f'{net}.{sta}.{loc}.{cha}.{dq}.{starttime.year}.{starttime.strftime("%Y%m%dT%H%M%S")}'   # e.g. net.sta.loc.cha.dq.year.YYYYMMDDThhmmss
            # .mseed file path
    fpath = os.path.join(output_folder, 
                         f'{starttime.year}', f'{net}', f'{sta}', f'{cha}.{dq}', 
                         fname)                                                                      # i.e. ../output_folder/year/net/sta/cha/file_name
                                                                                                     # e.g. ../test/2017/CM/CSLUI/HNZ.D/CM.CSLUI.10.HNZ.D.2017.20170127T120000
    
    # ====================================
    # 2. Edit the NSLC naming in the stats
    # ====================================

    tr.stats.network  = net
    tr.stats.station  = sta
    tr.stats.location = loc
    tr.stats.channel  = cha
    
    # ====================
    # 3. Export mseed file
    # ====================

        # Condition: Create dirs (if these do not exist)
    if not os.path.isdir(os.path.dirname(fpath)):
        os.makedirs(os.path.dirname(fpath))

        # Export file as MSEED
    tr.write(fpath, format = 'MSEED')

    print(f'{fpath} | [saved]')

# -----------------------------------------------------------------------
def export_mseeds(fpaths_list: list, ofolder: str):
    '''
    - Description: Export mseed files to output folder.

    - Input parameters:
        <<< fpaths_list: list
                         List of file paths of waveforms
        <<< ofolder    : str
                         Path of output folder
    - Returns: waveform files exported as mseeds
    
    - Code sections:
        1. Some considerations
        2. 
    '''
    
    validate(export_mseeds, locals())                                       # validate the type of input parameters
    # ===================
    # 1. Some considerations
    # ===================
    network = 'CM'                                                          # set network code

    # Damaged files
    dam_fpaths     = []                                                     # list of paths of damaged files
    reseted_fpaths = []                                                     # list of paths of reseted waveforms
    
    # =====================
    # 2. Export mseed files
    # =====================

    # Loop: go through each fpath in fpaths_list
    for fpath in sorted(fpaths_list):
        
        # Read seismograms
        try:
            st = read(fpath)                                                 # get stream
            # Merge seismograms per channel
            st.merge(fill_value = 'interpolate')                             # fill possible gaps
        except:
            dam_fpaths.append(fpath)
            print(f'{fpath} [ERROR]')
            continue
        
        # Export mseed file
            # Loop: go through each trace in stream
        for tr in st:
                # Get start and end times
            starttime_, endtime_ = tr.stats.starttime, tr.stats.endtime
            
                # Condition: ignore reseted traces (starttime < year 2000)
                    # Trace with starttime < 2000-01-01
            if starttime_ < UTCDateTime('2000-01-01T00:00:00'):
                reseted_fpaths.append(fpath)
                break;
                    
                    # Trace with starttime > 2000-01-01
            else:
                        # Condition: consider traces with different julday between starttime and endtime
                            # Trace with starttime.juldy != endtime.julday
                if starttime_.julday != endtime_.julday:
                                # Get cutoff date
                    cutoff_date_ = UTCDateTime(f'{endtime_.year}-{endtime_.month}-{endtime_.day}T00:00:00')
                                # Cut traces
                    tr1 = tr.copy()
                    tr2 = tr.copy()
                                    # First trace
                    tr1.trim(starttime = starttime_, endtime = cutoff_date_)
                                    # Second trace
                    tr2.trim(starttime = cutoff_date_, endtime = endtime_)
                                # Export mseed
                    write_mseed(tr1, network = network, output_folder = ofolder)
                    write_mseed(tr2, network = network, output_folder = ofolder)
                            
                            # Trace with starttime.julday == endtime.julday
                else:
                                # Export mseed
                    write_mseed(tr, network = network, output_folder = ofolder)

    # =========================
    # Export damaged file paths
    # =========================

        # Quality folder
    quality_folder = os.path.join(os.sep, 'home', 'eguzman', 'eguzmanv', 'acc_wv', 'data_quality')
            # Create
    if not os.path.isdir(quality_folder):
        os.makedirs(quality_folder)
        
        # Damaged files
    with open(os.path.join(quality_folder, 'dam_wv.txt'), 'a+') as file:
        file.writelines('\n'.join(dam_fpaths))

    with open(os.path.join(quality_folder, 'reseted_wv.txt'), 'a+') as  file:
        file.writelines('\n'.join(reseted_fpaths))