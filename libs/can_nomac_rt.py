
import csv
import operator
import math


class CAN_PMAC_RT:
    
    def __init__(self,priority, period,TX,DLC,tbit):
        self.priority = priority
        self.period = period
        self.TX = TX
        self.DLC = DLC
        
        self.tbit =tbit
        
    def get_length_m(self, p,B,t,j=0, new_t=None):
            #the recursion base case
        if t == new_t: return new_t      
        sum_val = 0.0
        length_m=0
        for i in range(len(self.priority)):
            if self.priority[i] <= self.priority[p]:
                
                #follows the use case for deriving the length of the priority-level m busy period 
                val=(t + j)/self.period[i]  
                
                b_delay= math.ceil(val) *self.TX[i]
                sum_val+= b_delay
                #print(sum_val)
        length_m = B + sum_val
                
        #calls itself recursively to reach the base case and then terminates      
        return self.get_length_m(p,B, length_m,j, t)  
    def get_qd_m(self, p,B,q,w, prev_w=None, j=0):
    
        if w ==prev_w: return  prev_w
        #initialise blocking messages to be zero
        next_idx=0                
        sum_val = 0
        qd = 0
        for i in range(len(self.priority)):    
            if max(self.priority)==p:
                qd = B + q * self.TX[i]
                #print(qd)
            next_idx=next_idx+1           
            if self.priority[i]<self.priority[p]:    
                val = (w+j+self.tbit)/self.period[next_idx-1]
                #print(math.ceil(val))
                sum_val += math.ceil(val) * self.TX[next_idx-1]
                #print("--",sum_val)
            qd = B + q * self.TX[i] + sum_val 
        return self.get_qd_m(p,B,q,qd,w,j) 
    
    def get_Response_time(self,p,Q,B):
        w=0
        Response_time = 0
        first_inst_rt =0
        other_inst_rt =0
        for q in range(int(Q)):
            
            if q == 0:
                prev_inst = self.get_qd_m(p,B,q,B)
                #print(prev_inst)
                first_inst_rt= prev_inst +self.TX[p]         
            elif q > 0:
                w= self.get_qd_m(p,B,0,B) + self.TX[p]

                new_inst = self.get_qd_m(p,B,q,w)
                other_inst_rt = new_inst -q*self.period[p] +self.TX[p]
                #if Response_Time>Deadline[p]:
                    #break;
            if first_inst_rt > other_inst_rt:
                Response_time = first_inst_rt
            else:
                Response_time = other_inst_rt
        return Response_time