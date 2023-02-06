import os
import csv
import math

from periodic_mac.can_pmac_rt import CAN_PMAC_RT
#import utils.can_fd_padding
import can_mac_rt 

def read_file():
    priority,period,TX,size = [],[],[],[]
    bus_speed = 100
    tbit = 1 / float(bus_speed)
    len_message_frame=[]
    
    CURRENT_DIR = os.path.dirname(__file__)
    file_path = os.path.join(CURRENT_DIR,'file_test.csv')
    with open(file_path,'r') as dataset:
        reader = csv.reader(dataset)
        next(reader)
        for row in reader:
            TX.append(round(float((55 + (10 * (int(row[1])))) * tbit),6))
            period.append(int(row[2]))
            priority.append(int((row[0]),16))
            size.append(int(row[1]))
    
    DLC = [utils.can_fd_padding.can_fd_data(i) for i in size]
    print(DLC)
    exit()
    full_frame = [math.floor(4/8) for i in range(len(DLC))]
    partial_frame = [math.ceil(4/8) - full_frame[i] for i in range(len(DLC))]
    modul = [4 %8 for i in range(len(DLC))]
    #print(cmax)
    cmax = [ (55 + (10 *8))*tbit for i in range(len(DLC))] 
    cmac =[ (55 + 10 *modul[i])*tbit for i in range(len(DLC))]   
    pmac_TX = [(full_frame[i])*cmax[i]  + (partial_frame[i]* cmac[i] ) for i in range(len(DLC))]
    print(TX)   
    return priority, period,TX,full_frame, partial_frame,DLC, pmac_TX,cmac,cmax,tbit

def check():
    val1,val2,val3,val4,val5,val6,val7,val8,val9,val10= read_file()
    pmac_resp = CAN_PMAC_RT(val1,val2,val3,val4,val5,val6,val7,val8,val9,val10)
    res = []
    rho = pmac_resp.get_rho(10)
    #print(pmac_resp.cmax)
    

    for p in range(len(pmac_resp.priority)):
        B = pmac_resp.get_Blocking_m(p)
        #print(B)
        t = pmac_resp.pmac_TX[p]+ pmac_resp.TX[p]
        length_m = pmac_resp.get_length_m_periodic(p,rho,B,t)
        #print(pmac_resp.num_frame[p])
        Q = math.ceil(length_m /pmac_resp.period[p]) + (math.ceil(length_m /rho[p]))
        print(Q)
        res.append(pmac_resp.get_Response_time_periodic(p,Q,B,rho))
    
    return res
        
    
        
def main() :   
   d = check()
   print(d)
        
    
if __name__ == '__main__':
        main()        
       
     
       