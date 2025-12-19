#print("Test") 

import psutil 
import time 
import statistics 
from collections import deque 


#print("Test") 

Time_window = 30 
Anomaly_threshold = 3     # works in standard deviations 
Anomaly_Count = 3     # this many in a row for alert 

history_CPU = deque(maxlen=Time_window) 
history_Mem = deque(maxlen=Time_window) 
consecutive_CPU = 0 
consecutive_Mem = 0

while True: 
    value_CPU = psutil.cpu_percent(interval=1) 
    history_CPU.append(value_CPU) 
    #print("Test") 
    value_Mem = psutil.virtual_memory() 
    history_Mem.append(value_Mem.percent) 

    CPU_Potential = 0
    Mem_Potential = 0

    if len(history_CPU) == Time_window: 
        mean = statistics.mean(history_CPU)
        standarddev = statistics.pstdev(history_CPU)

        threshold = mean + Anomaly_threshold * standarddev 
        #print(threshold)

        if value_CPU > threshold: 
            consecutive_CPU += 1 
            print(consecutive_CPU)
            if consecutive_CPU >= Anomaly_Count:
                print("test: consistent spike found") 
                print(f"CPU: {value_CPU}%") 
                print(f"Baseline: {mean}%") 
                #print("=+=+=+=+=+=+=") 
            else: 
                print("test: potential spike found") 
                print(f"CPU: {value_CPU}%") 
                print(f"Baseline: {mean}%") 
                CPU_Potential = 1
                #print("=+=+=+=+=+=+=") 
        else: 
            consecutive_CPU = 0 
            CPU_Potential = 0
            print("test: no spike") 
            print(f"CPU: {value_CPU}%") 
            print(f"Baseline: {mean}%") 
            #print("=+=+=+=+=+=+=") 
        
        #if consecutive > Anomaly_Count:
            #print("test: sustained strain found") 
            #print(f"CPU: {value}%") 
            #print(f"Baseline: {mean}%") 
            #print("=+=+=+=+=+=+=") 
    else: 
        print("Currently unfilled") 
        print("current CPU length = ", len(history_CPU)) 
        print(f"CPU: {value_CPU}%") 
        #print(f"Baseline: {mean}%") 
        #print("=+=+=+=+=+=+=")  
    
    if len(history_Mem) == Time_window: 
        mean = statistics.mean(history_Mem)
        standarddev = statistics.pstdev(history_Mem)

        threshold = mean + Anomaly_threshold * standarddev 
        print(threshold)

        if value_Mem.percent > threshold: 
            consecutive_Mem += 1 
            print(consecutive_Mem)
            if consecutive_Mem >= Anomaly_Count:
                print("test: consistent spike found") 
                print(f"Mem: {value_Mem.percent}%") 
                print(f"Baseline: {mean}%") 

            else: 
                print("test: potential spike found") 
                print(f"Mem: {value_Mem.percent}%") 
                print(f"Baseline: {mean}%") 
                Mem_Potential = 1

        else: 
            consecutive_Mem = 0 
            print("test: no spike") 
            print(f"Mem: {value_Mem.percent}%") 
            print(f"Baseline: {mean}%") 
            Mem_Potential = 1
    else: 
        print("Currently unfilled") 
        print("current Memory length = ", len(history_Mem)) 
        print(f"Mem: {value_Mem.percent}%") 

    print("=+=+=+=+=+=+=")  

    if CPU_Potential == 1 and Mem_Potential == 1: 
        print("Potential Spike found in multiple data sources")