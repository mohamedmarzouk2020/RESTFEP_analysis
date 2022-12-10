#!/Users/marzouk/miniconda3/bin/python
# ------------------
# created 5-12-2022
# To plot relation between the replica numbers and the probability of exchange
# Running from local Machine IN QST Chiba
# ---------------
# Add all libararies required
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams["font.family"] = "serif"

# input required such as dual or ref2 or dual3
if len(sys.argv) == 2:
    dir = str(sys.argv[1])  # the dir required to do analysis for
else:
    print("please enter the dir name to do the probability analysis such as dual3")
    quit()


# Function to pickup the data from every prodrun.part000.log file in the rep dir
def pickupdata(name):
    with open(name) as f:
        data = f.readlines()
        alldata = []
        picklines = []
        for line in data:
            if "Repl     " in line:
                picklines.append(line)
        xx = picklines[1].split()[1:]
        for i in xx:
            alldata.append(float(i))
        alldata = np.array(alldata)
    return alldata


# change the dir. to the rep0 and add all log files in list
os.chdir(f"../{dir}/prodrun/rep0/")
files = []
for i in range(2, 10):
    if os.path.exists(str("prodrun.part000"+str(i)+".log")):
        files.append(str("prodrun.part000"+str(i)+".log"))

# apply the function for all the files in list and get the average
if len(files) == 1:
    data1 = pickupdata(files[0])
    data_avg = data1*100
if len(files) == 2:
    data1 = pickupdata(files[0])
    data2 = pickupdata(files[1])
    data_avg = ((data1+data2)/2)*100
elif len(files) == 3:
    data1 = pickupdata(files[0])
    data2 = pickupdata(files[1])
    data3 = pickupdata(files[2])
    data_avg = ((data1+data2+data3)/3)*100
elif len(files) == 4:
    data1 = pickupdata(files[0])
    data2 = pickupdata(files[1])
    data3 = pickupdata(files[2])
    data4 = pickupdata(files[3])
    data_avg = ((data1+data2+data3+data4)/4)*100
elif len(files) == 5:
    data1 = pickupdata(files[0])
    data2 = pickupdata(files[1])
    data3 = pickupdata(files[2])
    data4 = pickupdata(files[3])
    data5 = pickupdata(files[4])
    data_avg = ((data1+data2+data3+data4+data5)/5)*100
elif len(files) == 6:
    data1 = pickupdata(files[0])
    data2 = pickupdata(files[1])
    data3 = pickupdata(files[2])
    data4 = pickupdata(files[3])
    data5 = pickupdata(files[4])
    data6 = pickupdata(files[5])
    data_avg = ((data1+data2+data3+data4+data5+data6)/6)*100
elif len(files) == 7:
    data1 = pickupdata(files[0])
    data2 = pickupdata(files[1])
    data3 = pickupdata(files[2])
    data4 = pickupdata(files[3])
    data5 = pickupdata(files[4])
    data6 = pickupdata(files[5])
    data7 = pickupdata(files[6])
    data_avg = ((data1+data2+data3+data4+data5+data6+data7)/7)*100
elif len(files) == 8:
    data1 = pickupdata(files[0])
    data2 = pickupdata(files[1])
    data3 = pickupdata(files[2])
    data4 = pickupdata(files[3])
    data5 = pickupdata(files[4])
    data6 = pickupdata(files[5])
    data7 = pickupdata(files[6])
    data8 = pickupdata(files[7])
    data_avg = ((data1+data2+data3+data4+data5+data6+data7+data8)/7)*100

#  Divide the data for different parts based on the probability value lower and higher than 25%
replicalow = []
replicahigh = []
datalow = []
datahigh = []
for index, num in enumerate(data_avg):
    if num > 25 or num == 25:
        replicahigh.append(index)
        datahigh.append(num)
    elif num < 25:
        replicalow.append(index)
        datalow.append(num)

# Plot the data and get the figure
fig = plt.figure(figsize=(12, 8))
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
ax = fig.add_axes([0.2, 0.2, 0.8, 0.8])
ax.set_title(f"The probability of exchange of  {dir}")

ax.set_xlabel('Replica Number', fontsize=24, color='black')
ax.set_ylabel('Probability', fontsize=24, color='black')
ax.bar(replicalow, datalow, linewidth=2, color="red")
ax.bar(replicahigh, datahigh, linewidth=2, color="blue")

fig.savefig(
    f'../../../{dir}_exchange_probability_{len(files)}simulationsteps.png', bbox_inches='tight', dpi=300)
