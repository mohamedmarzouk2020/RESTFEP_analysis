#!/Users/marzouk/miniconda3/bin/python
# ------------------
# created 8-8-2022
# To check the convergence of dg of dual and ref then ddg
# Running from local Machine IN QST KIZU
# modified 8-11-2022 @ Chiba QST
# convert the free energy form kj to kcal to be in consistnce with the experimental
# results and all things in poster
# ---------------
# Add all libararies required
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams["font.family"] = "serif"


# input required such as dual or ref2 or dual3
if len(sys.argv) == 3:
    dir1 = str(sys.argv[1])  # should be dual
    dir2 = str(sys.argv[2])
else:
    print("please enter the dir. names to do the probability analysis such as dual ref ")
    quit()


# This function to pickup the data from every prodrun.part000.log file in the rep dir
def pickupdata(name):
    with open(name) as f:
        data = f.readlines()
        energy = []
        time = []
        for line in data:
            if "BAR " in line:  # make space to choose only that started with bar which is the data
                bar = line.split()
                # I divided over 4.185 to convert for kj to kcal
                energy.append(float("{:.2f}".format(float(bar[2])))/4.185)
                # I want to get average of the two numbers of simulation time
                time.append(
                    ((float(bar[1].split("-")[0]))+(float(bar[1].split("-")[1].split(":")[0])))/2)
    return time, energy


timedual, energydual = pickupdata(f"../{dir1}/bar1.log")
timeref, energyref = pickupdata(f"../{dir2}/bar1.log")
# Calculate the diff in energy between the ref and dual to be able to compare directly
energydiff = list((np.array(energyref))-(np.array(energydual)))
# I am adding these conditions to keep the convergence at 0 kcal/mole not any random number
energydual = list(np.array(energydual)-energydual[-1])
energyref = list(np.array(energyref)-energyref[-1])

# Plot the dg for ref and dual
fig = plt.figure(figsize=(12, 8))
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
ax = fig.add_axes([0.2, 0.2, 0.8, 0.8])
ax.set_title(f"The $\Delta$G convergence for {dir1} and {dir2} ", fontsize=20)
ax.set_xlabel('Time (ps)', fontsize=24, color='black')
ax.set_ylabel('$\Delta$G (kcal/mol)', fontsize=24, color='black')
ax.plot(timedual, energydual, linewidth=2, c='b', label='Dual',
        marker='o', markerfacecolor='r', markersize=8)
ax.plot(timeref, energyref, linewidth=2, c='r', label='Refrence',
        marker='o', markerfacecolor='b', markersize=8)
ax.legend(fontsize=16)
fig.savefig(
    f'../{dir1}_{dir2}_dG_convergence_kcal.png', bbox_inches='tight', dpi=300)


# Plot the ddg  ref - dual
fig = plt.figure(figsize=(12, 8))
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
ax = fig.add_axes([0.2, 0.2, 0.8, 0.8])
ax.set_title(
    f" The convergnce  $\Delta\Delta$G for {dir1} and {dir2} ", fontsize=20)
ax.set_xlabel('Time (ps)', fontsize=24, color='black')
ax.set_ylabel('$\Delta\Delta$G (kcal/mol)', fontsize=24, color='black')
ax.plot(timeref, energydiff, linewidth=2, c='b',
        marker='o', markerfacecolor='r', markersize=8)
fig.savefig(
    f'../{dir1}_{dir2}_ddg_convergence_kcal.png', bbox_inches='tight', dpi=300)
