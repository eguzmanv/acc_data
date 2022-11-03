import os
import obspy
from obspy import UTCDateTime

from toolkits.utils import validate
from toolkits.wv_conversion.wv_medatada.SEED_naming import set_SEED_naming

# --------------------------------------------------------------------------------------
def export_wv(tr: obspy.core.trace.Trace, output_folder: str, network = None):
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
    validate(export_wv, locals())                                                                    # validate the type of input parameters
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

    print(tr, ' [saved]')