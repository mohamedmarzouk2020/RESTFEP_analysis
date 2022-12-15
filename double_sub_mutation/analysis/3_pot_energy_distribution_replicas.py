#!/Users/marzouk/miniconda3/bin/python
# ------------------
# created 5-12-2022
# To plot relation between the pot energy distribution of replicas to check the overlab
# Running from local Machine IN QST Chiba
# ---------------
# Add all libraries required
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
    print(f"please enter the dir name to do the probability analysis for pot energy dist such as dual3 ")
    quit()


cwd = os.getcwd()
# Get info about the last replica from directories
os.chdir(f"{cwd}/../{dir}/prodrun/")
files = []
for i in range(1, 200):  # of course I will not have replicas more than 200 if so change this number
    if os.path.exists(str("rep"+str(i))):
        files.append(i)
    else:
        continue
replicas = max(files)  # the total no of replicas


# TODO : change the input to be all the dir one time dual refa refb
# TODO : make one function for each dir then apply for three dir  this is just idea I dont know the applicability

# This function to pickup the data from every deltae.part0002.xvg file
# in all the rep dirs from rep0 to last replica

# path = f"{cwd}/../{dir}/prodrun/"


def pickupdata(dir, name):
    os.chdir(f"{cwd}/../{dir}/prodrun/")
    alldata = []
    # For the rep0
    data1 = []
    with open(f"rep{0}/{name}") as f:
        data = f.readlines()
        for line in data:
            if "#" in line or "@" in line:
                continue
            else:
                data1.append(float(line.split()[2])-float(line.split()[4]))
    alldata.append(data1)

    # for All replicas 1 to before last
    for i in range(1, replicas-1):
        data1 = []
        data2 = []
        with open("rep{}/{}".format(i, name)) as f:
            data = f.readlines()
            for line in data:
                if "#" in line or "@" in line:
                    continue
                else:
                    data1.append(float(line.split()[2])-float(line.split()[4]))
                    data2.append(float(line.split()[4])-float(line.split()[6]))
        alldata.append(data1)
        alldata.append(data2)

    # for the last replica
    with open("rep{}/{}".format(replicas-1, name)) as f:
        data = f.readlines()
        data1 = []
        for line in data:
            if "#" in line or "@" in line:
                continue
            else:
                data1.append(float(line.split()[2])-float(line.split()[4]))
    alldata.append(data1)

    return alldata

# Function to Plot  all replicas


def plothist(list_data):
    fig = plt.figure(figsize=(18, 12))
    plt.rc('xtick', labelsize=18)
    plt.rc('ytick', labelsize=18)
    ax = fig.add_axes([0.2, 0.2, 0.8, 0.8])
    # ax.set_xlim(-400, 400)
    # ax.set_ylim(0, 0.15)
    ax.set_title(
        f"The potential energy distribution of {replicas} replicas {dir}", fontsize=20)
    ax.set_xlabel('Energy ', fontsize=24, color='black')
    ax.set_ylabel('Probability distribution(E)', fontsize=24, color='black')
    for num in range(len(list_data)):
        if num % 2 == 0:
            plt.hist(list_data[num], histtype="step",
                     color="blue", bins=350, density=True)
        elif num % 2 == 1:
            plt.hist(list_data[num], histtype="step",
                     color="g", bins=350, density=True)
    return fig


# count the number of steps from the output files number
files = []
for i in range(2, 10):
    if os.path.exists(f"{cwd}/../{dir}/prodrun/"+str("rep0/deltae.part000"+str(i)+".xvg")):
        files.append(f"{cwd}/../{dir}/prodrun/" +
                     str("rep0/deltae.part000"+str(i)+".xvg"))

# Run everything with conditions based on number of steps two by two
if len(files) == 1:
    # split to obtain only the file name which required for the function to done
    # files[0].split("/")[4]
    data1 = pickupdata(f"{dir}", "deltae.part0002.xvg")
    fig1 = plothist(data1)
    fig1.savefig(
        f'{cwd}/../{dir}_pot_energy_distribution_1simulationsteps.png', bbox_inches='tight', dpi=300)
