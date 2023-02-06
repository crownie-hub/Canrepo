import math
from libs.can_pmac_rt import CAN_PMAC_RT

def pmac_result(priority, period,TX,full_frame, partial_frame,DLC, pmac_TX,cmac,cmax,tbit):
    
    pmac_resp = CAN_PMAC_RT(priority, period,TX,full_frame, partial_frame,DLC, pmac_TX,cmac,cmax,tbit)
    res = []
    rho = pmac_resp.get_rho(10)
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
        