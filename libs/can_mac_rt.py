import os
import csv
import operator
import math
import random
import argparse


class Response_time:
    
    def __init__(self,priority, period,TX, full_frame,partial_frame, DLC,cmax,cmac,data_size,bus_speed):
        self.priority = priority
        self.period = period
        self.TX = TX
        self.full_frame = full_frame #beta
        self.DLC = DLC
        self.cmax =cmax
        self.cmac =cmac
        self.bus_speed = bus_speed
        self.data_size = data_size
        self.partial_frame = partial_frame #alpha
        
    @staticmethod
    def generate_data(bus_speed,data_size):
        #full cAN DLC = 8, A+F = 4
        TX = []
        tbit = 1/bus_speed
        DLC = [random.randint(1, 64) for i in range (data_size)]
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
            new_tx = (full_frame[i]-1) * cmax[i] + cmac[i]
            TX.append(new_tx)
        print(TX)
        return priority, period,TX, full_frame,partial_frame, DLC,cmax,cmac,data_size,bus_speed
    
     #calculates length of the busy period    
    def get_length_busy_period(self,p, B, t, j=0, new_t=None): #p = pth priority, B = Blocking of each frame, t= busy interval, j = jitter
        #the recursion base case
        if t == new_t: return new_t            
        sum_val = 0.0
        new_length_m=0
        for r in range(len(self.priority)):
       
            if self.priority[r] <= self.priority[p]: #check for higher priority messages including itself
                #follows the use case for deriving the length of the priority-level m busy period 
                value=math.ceil((t + j)/self.period[r] )  * self.TX[r] 
                sum_val+= value
                #print(sum_val)
        new_length_m = B + sum_val
        try:
            get_length_m = self.get_length_busy_period(p,B, new_length_m,j, t) #recursion
         #calls itself recursively to reach the base case and then terminates 
        except Exception:
            get_length_m=0      # returns 0 if no solution  if found 
         
        return get_length_m
       
    #calculates the queuing delay
    def get_queuing_delay(self,p, tbit, B, q, w, prev_w=None, j=0): # p =priority of each message,q = instance, B = Blocking w= waiting delay, jitter
        
        if w ==prev_w: return  prev_w
        #initialise blocking messages to be zero
        num_frame = [self.full_frame[i] + self.partial_frame[i] for i in range(self.data_size) ]
        next_idx =0                
        sum_interference = 0
        queue_delay = 0
        #follows the use case to derive the worst case queuing delay
        for r in range(len(self.period)):
            if max(self.priority)==p:
                queue_delay = B + q * self.TX[r]
            next_idx=next_idx+1   #nextIndex_holder    
            if self.priority[r]< self.priority[p]:
                interference = (w+j+tbit) / self.period[next_idx-1]
                sum_interference += math.ceil(interference) * self.TX[next_idx-1] 
            queue_delay = B + ((q % num_frame[p]) *self.cmax[p]) + (math.floor(q/num_frame[p])* self.TX[p]) +sum_interference
        
        return self.get_queuing_delay(p,tbit,B,q,queue_delay,w,j) 
    
    def get_Blocking_m(self,p):
        Blocking_m=0
        lp_blocking=[] #blocking due to lower priority
        #incase of lower priority messages in transmission
        for m in range(len(self.priority)):
            if max(self.priority) == self.priority[p]:
                Blocking_m=0
            elif self.priority[m] > self.priority[p]:
                lp_blocking.append(max((math.ceil(self.full_frame[m]/(self.full_frame[m]+1))*self.cmax[m]),self.cmac[m])) #alpha-1 =0 always for profile 1
                Blocking_m =max(lp_blocking)
        return Blocking_m   
      
    def get_Response_time(self,p,Q,B):
        w=0
        tbit = 1/self.bus_speed
        Response_Time, first_q_resp, other_q_resp =0,0,0
        num_frame = [self.full_frame[i] + self.partial_frame[i] for i in range(self.data_size) ]
        #to derive the number of instances of the message 
        for q in range(int(Q)):
            init_w = B + math.floor(q/num_frame[p]) * self.TX[p]
            if q == 0:
                prev_inst = self.get_queuing_delay(p,tbit,B,q,init_w)
                first_q_resp= round((prev_inst - (math.floor(q/num_frame[p]) *self.period[p]) + (math.floor(((q %num_frame[p])+1))/num_frame[p]) *self.cmac[p] +((1- math.floor((q %num_frame[p])+1)/num_frame[p])*self.cmax[p])),6)     
            elif q > 0:
                newq=q-1
                w= self.get_queuing_delay(p,tbit,B,newq,B) + self.TX[p]
                new_inst =self.get_queuing_delay(p,tbit,B,q,w)
                last_q_resp = round((new_inst - (math.floor(q/num_frame[p]) *self.period[p]) + (math.floor(((q %num_frame[p])+1))/num_frame[p]) *self.cmac[p] +((1- (math.floor((q %num_frame[p])+1)/num_frame[p]))*self.cmax[p])),6)
            if first_q_resp > other_q_resp:
                Response_Time = first_q_resp
            else:
                Response_Time = other_q_resp
             
        return Response_Time
    #the code works whether the file is sorted according to the priortiy or not,this method sorts it to a csv file 
        #the code works whether the file is sorted according to the priortiy or not,this method sorts it to a csv file 
    def sort_file_to_csv(self,res):
        file_path = "" # PUT FILE PATH
        with open(file_path, "w",newline="") as output:
            writer = csv.writer(output)
            for  row in range(len(self.period)):
                writer.writerow([self.priority[row],self.period[row],self.DLC[row],self.TX[row],res[row]])        
        data =csv.reader(open(file_path), delimiter =',')      
        sort_file = sorted(data, key=operator.itemgetter(0), reverse = False)
        with open(file_path, "w", newline="") as sort:
            writer =csv.writer(sort)
            writer.writerow(["ID","PERIOD","DLC","TRANSMISSION TIME","RESPONSE TIME"])
            
            writer.writerows(sort_file)
    
def main():
    
    result=[]  
    parser = argparse.ArgumentParser(description="Bus speed and data-size")
    parser.add_argument("--data_size", type = int, required=True)
    parser.add_argument("--bus_speed",type = int,required=True)
    args = parser.parse_args()
    val1,val2,val3,val4,val5,val6,val7,val8,val9,val10= Response_time.generate_data (args.bus_speed,args.data_size)

    resp = Response_time(val1,val2,val3,val4,val5,val6,val7,val8,val9,val10)

    for p in range(len(resp.priority)):
        
        B = resp.get_Blocking_m(p)
        t = resp.TX[p]
        length_m = resp.get_length_busy_period(p, B, t)
    
        Q = math.ceil(length_m /resp.period[p])*(resp.full_frame[p]+resp.partial_frame[p])
       
        result.append(resp.get_Response_time(p,Q,B))
        
    print(result)
    #sort_file_to_csv(priority,period,DLC,TX,result)   
            
if __name__ == '__main__':
    main()        
         