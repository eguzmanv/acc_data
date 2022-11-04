import obspy

from toolkits.utils import validate

# ------------------------------------------------------------------------
def set_SEED_naming(tr: obspy.core.trace.Trace, network = None) -> str:
    '''
    - Description: Read the stats of an input trace and returns the NSLC naming 
                   convention as string.

    - Input parameters:
        <<< trace   : obspy.core.trace.Trace
                      Input trace
        <<< network : str
                      Input network                           (e.g 'CM')

    - Returns:
        >>> str                                               (e.g. 'NET.STA.LOC.CHA')

    - Code sections:
        1. Extract original SEED naming
            >>> output of interest: net_, sta_, loc_ (str)
        2. Rename the channel id (if required)
            >>> output of interers: cha_ (str)
    '''
    validate(set_SEED_naming, locals())                          # validate the type of input parameters
    
    # ===============================
    # 1. Extract original SEED naming
    # ===============================
    net, sta, loc, cha = tr.get_id().split('.')                  # get net, sta, loc and cha codes from trace id         
        
        # Some considerations
            
            # set network code manually
    if network != None:
        net = network

            # set station code manually
    sta = 'C' + sta                                              # rename the sta code with a 'C' in front 
                
                # consider special cases
    if 'LEJ' in sta:                                           
        sta = 'CLEJA'                                            # 'Lejanías Meta' station: LEJA

            # set location code manually
    loc = '10'                                                   # set the loc code as 10

    # ======================================
    # 2. Rename the channel id (if required)
    # ======================================
    
    # Condition: evaluate the trace format
            
        # _format: KINEMETRICS_EVT
    if tr.stats._format == 'KINEMETRICS_EVT':
                
                # set the band code and instrument code
        if tr.stats.sampling_rate == 200:                          
            cha = 'HN'                                           # H: High Broad Band (80, 250)Hz, N: Accelerometer

                # rename the orientation code
        if tr.stats.kinemetrics_evt['chan_id'] == 'X':
            cha += 'E'                                           # e.g. HNX --> HNE 
        elif tr.stats.kinemetrics_evt['chan_id'] == 'Y':
            cha += 'N'                                           # e.g. HNN --> HNN
        elif tr.stats.kinemetrics_evt['chan_id'] == 'Z':
            cha += 'Z'                                           # e.g. HNZ --> HNZ
        else:
            cha = tr.stats.kinemetrics_evt['chan_id']            # for other orientations (e.g. A, B, C, T, R, U, V, W ...)
        
        # _format: ...

                #(...)

    return f'{net}.{sta}.{loc}.{cha}'