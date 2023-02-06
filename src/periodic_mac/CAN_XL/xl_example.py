import random
import math
from libs.can_pmac_res import pmac_result

def generate_data():
    dtbit = 1/10000
    tbit = 500
    priority = [i for i in range(1,16)]
    DLC = [random.randint(8,2048) for i in range(15)]
    period_set = [10,50,100,1000]
    period = sorted([random.choice(period_set) for i in range(15)])
    print(period)
    TX = [xl_TX(i, tbit, dtbit) for i in DLC] 
    
    modul = [4 %2048 for i in range(len(DLC))]
    full_frame = [math.floor(4/2048) for i in range(len(DLC))]
    partial_frame = [math.ceil(4/2048) - full_frame[i] for i in range(len(DLC))]
    #print(cmax)
    cmax = [ 37 * tbit + ((129 + (8 * 2048)+ math.floor((9+ (8*2048))/10)) * dtbit) for i in range(len(DLC))]
    cmac =[ 37 * tbit + ((129 + (8 * modul[i])+ math.floor((9+ (8*modul[i]))/10)) * dtbit) for i in range(len(DLC))]   
    pmac_TX = [(full_frame[i])*cmax[i]  + (partial_frame[i]* cmac[i] ) for i in range(len(DLC))]
    pmac_res = pmac_result(priority, period,TX,full_frame, partial_frame,DLC, pmac_TX,cmac,cmax,tbit)
    
    return pmac_res
        
def xl_TX(payload, tbit, dtbit):
    # assuming base format
    Trans_time= 37 * tbit + ((129 + (8 * payload)+math.floor((9+ (8*payload))/10)) * dtbit)

    return Trans_time




