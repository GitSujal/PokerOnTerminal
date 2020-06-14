import numpy as np

Dates = []
Times = []
Power_Readings = []
Time_differences = []
Power_Differences = []
Cumulative_Powers = []

with open("power.csv","r") as fp:
    for line in fp.readlines()[2:]:
        linelist = line.split(",")
        
        Dates.append(linelist[0])
        Times.append(linelist[1])
        Power_Readings.append(linelist[2])
        Time_differences.append(float(linelist[3].split(" ")[1]))
        Power_Differences.append(int(linelist[4]))
        Cumulative_Powers.append(int(linelist[5]))

print(Dates)
print(Time_differences)

