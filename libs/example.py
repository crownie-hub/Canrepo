import random
import math
import libs.CAN_MAC_Response_time

def generate_data(bus_speed,data_size):
    #full cAN DLC = 8, A+F = 4
    TX = []
    tbit = 1/bus_speed
    DLC = [random.randint(1, 8) for i in range (data_size)]
    print(DLC)
    priority = [i+1 for i in range (data_size)]
    period_set = [5,10,100,1000,5000] #user can change period set
    period= sorted([random.choice(period_set) for i in range(data_size)])
    full_frame=[(math.floor((float(i + 4)/8))) for i in DLC] #using the first mac profile
    partial_frame = [(math.ceil((float(DLC[i] + 4)/8))- full_frame[i]) for i in range(len(DLC))]            
    DLC_modul = [(DLC[i] + 4) % 8 for i in range(len(DLC))] #mac &fv =4  Calculates(D+A+F)_mod Dmax
    cmax = [ (55 + (10 * 8)) * tbit for i in range(len(DLC)) ] #C_Dmax
    cmac =[(55 + 10 * DLC_modul[i]) * tbit for i in range(len(DLC)) ]  # calculates C_(D+A+F)_mod Dmax

    #appends the result to the transmission time TX of each messages 
    for i in range(len(DLC)):
        new_tx = (full_frame[i]) * cmax[i] + (partial_frame[i]*cmac[i])
        TX.append(new_tx)
    print(TX)
    return priority, period,TX, full_frame,partial_frame, DLC,cmax,cmac,data_size,bus_speed
def rand_result(bus_speed,data_size):
    
    result=[]  
   

    val1,val2,val3,val4,val5,val6,val7,val8,val9,val10= generate_data (bus_speed,data_size)

    resp = libs.CAN_MAC_Response_time.Response_time(val1,val2,val3,val4,val5,val6,val7,val8,val9,val10)

    for p in range(len(resp.priority)):
        
        B = resp.get_Blocking_m(p)
        t = resp.TX[p]
        length_m = resp.get_length_busy_period(p, B, t)
    
        Q = math.ceil(length_m /resp.period[p])*(resp.full_frame[p]+resp.partial_frame[p])
       
        result.append(resp.get_Response_time(p,Q,B))
        
    return result
    #sort_file_to_csv(priority,period,DLC,TX,result)   
