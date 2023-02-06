
import csv
import operator
import math


class CAN_PMAC_RT:
    
    def __init__(self,priority, period,TX,full_frame, partial_frame,DLC, pmac_TX,cmac,cmax,tbit):
        self.priority = priority
        self.period = period
        self.TX = TX
        self.DLC = DLC
        self.pmac_TX = pmac_TX
        self.cmac =cmac
        self.cmax =cmax
        self.tbit =tbit
        self.full_frame = full_frame
        self.partial_frame = partial_frame
        

    def get_length_m_periodic(self,p,rho,B,t,j=0, new_t=None): #pth priority (ID),B=blocking, 
        #the recursion base case
        if t == new_t: return new_t
           
        sum_value= 0.0
        length_m=0
        for i in range(len(self.period)):
            if self.priority[i] <= self.priority[p]:
                
                #follows the use case for deriving the length of the priority-level m busy period 
                inf_m =(t + j) / self.period[i] 
                add_frame = ((t + j) / rho[i])
                
                total_inf = math.ceil(inf_m)* self.TX[i]   + (math.ceil(add_frame) * self.pmac_TX[i])
                
                sum_value += total_inf 
    
        length_m = B + sum_value #replaces t, t replaces new_t
        #calls itself recursively to reach the base case and then terminates      
        try:
            len_busy_periodic = self.get_length_m_periodic(p,rho,B,length_m,j, t)
            
        except Exception:
            len_busy_periodic =0  #returns 0 if it fails
        
        return len_busy_periodic

    def get_Blocking_m(self,p,):
        Blocking_m=0
        lp_msg_blocking=[]
        #incase of lower priority messages in transmission
        for m in range(len(self.priority)):
            if max(self.priority) == self.priority[p]:
                Blocking_m=0
            elif self.priority[m] > self.priority[p]:
                lp_msg_blocking.append(max(self.TX[m],(math.ceil(self.full_frame[m]/(self.full_frame[m]+1))),self.cmac[m])) #full_frame inst at 0 
                Blocking_m =max(lp_msg_blocking)
        return Blocking_m     
    #calculates queuing delay
    def get_qd_m_periodic(self,p,rho,B,q,w, prev_w = None, j=0): #q = q instance of a frame, w= worst-case delay
    
        if w ==prev_w: return  prev_w
        #initialise blocking messages to be zero
        
        next_idx=0                
        sum_val = 0
        queue_delay = 0
        len_frames = self.full_frame[p] + self.partial_frame[p]
        q_nt = q %((rho[p]/self.period[p])+(len_frames))
        #follows the use case to derive the worst case queuing delay
        for i in range(len(self.period)):
            
            if max(self.priority)==p:
                queue_delay = B + q * self.TX[p]
                
            next_idx=next_idx+1 #nextIndex_holder
            p_batch= B + math.floor(q/((rho[p]/self.period[p])+((len_frames))))*(((rho[p]/self.period[p])*self.TX[p])+self.pmac_TX[p]) + min(q_nt,(rho[p]/self.period[p]))*self.TX[p] + max(0,((q_nt-rho[p]/self.period[p])))*self.cmax[p]  
            if self.priority[i] < self.priority[p]:
                
                inf = ((w + j + self.tbit) / self.period[next_idx-1]) 
                add_inf = (((w + j + self.tbit) / rho[next_idx-1]))  #alpha is constant 1 in this case

                total_inst =(math.ceil(inf)* self.TX[next_idx-1]) + math.ceil(add_inf)* self.pmac_TX[next_idx-1]
                sum_val += total_inst 
                
            queue_delay = p_batch + sum_val   
        
    
        return self.get_qd_m_periodic(p,rho,B,q,queue_delay,w,j) 
            

    def get_Response_time_periodic(self,p,Q,B,rho):
        w=0
        Response_Time, first_q_resp,other_q_resp =0,0,0
        r=[]
        len_frames = self.full_frame[p]+self.partial_frame[p]
        #to derive the number of instances of the message 
        for q in range(int(Q)):
            init_w = B + q * self.TX[p]
            if q == 0:
                prev_inst = self.get_qd_m_periodic(p,rho,B,q,init_w)
                first_q_resp = round((prev_inst - ((math.floor(q/((rho[p]/self.period[p])+(len_frames))))*self.period[p])+ max(self.pmac_TX[p],self.TX[p])),6)
                #print(f_resp)
            elif q > 0:
                new_q =q-1
                w= self.get_qd_m_periodic(p,rho,B,q,B) + self.TX[p]
                new_inst = self.get_qd_m_periodic(p,rho,B,q,w)
                print(new_inst)
                other_q_resp= round((new_inst - ((math.floor(q/((rho[p]/self.period[p])+(len_frames))))*self.period[p])+ max(self.pmac_TX[p],self.TX[p])),6)
            if first_q_resp >other_q_resp:
                    Response_Time = first_q_resp
            else:
                Response_Time = other_q_resp  
        return Response_Time    
    
    def sort_file_to_csv(self,res):
        file_path2 = ""
        with open(file_path2, "w",newline="") as output:
            writer = csv.writer(output)
            for  row in range(len(self.period)):
                writer.writerow([self.priority[row],self.period[row],self.DLC[row],self.TX[row],res[row]])        
        data =csv.reader(open(file_path2), delimiter =',')      
        sort_file = sorted(data, key=operator.itemgetter(0), reverse = False)
        with open(file_path2, "w", newline="") as sort:
            writer =csv.writer(sort)
            writer.writerow(["ID","PERIOD","DLC","TRANSMISSION TIME","RESPONSE TIME"])
            
            writer.writerows(sort_file)    

    def get_rho(self,multiplier):
        rho_message= [self.period[i]*multiplier for i in range(len(self.period))] 
        print(rho_message)
        return rho_message












