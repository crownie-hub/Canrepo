import os
import csv
import math

from libs.can_pmac_res import pmac_result
from libs.can_fd_padding import can_fd_data

#import utils.can_fd_padding
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
    
    DLC = [can_fd_data(i) for i in size]
    print(DLC)
    full_frame = [math.floor(4/8) for i in range(len(DLC))]
    partial_frame = [math.ceil(4/8) - full_frame[i] for i in range(len(DLC))]
    modul = [4 %8 for i in range(len(DLC))]
    #print(cmax)
    cmax = [ (55 + (10 *8))*tbit for i in range(len(DLC))] 
    cmac =[ (55 + 10 *modul[i])*tbit for i in range(len(DLC))]   
    pmac_TX = [(full_frame[i])*cmax[i]  + (partial_frame[i]* cmac[i] ) for i in range(len(DLC))]
       
    pmac_res = pmac_result(priority, period,TX,full_frame, partial_frame,DLC, pmac_TX,cmac,cmax,tbit)
    
    return pmac_res


    
        
def main() :   
   d = read_file()
   print(d)
        
    
if __name__ == '__main__':
        main()        
       
     
       