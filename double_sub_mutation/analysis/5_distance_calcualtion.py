#!/Users/marzouk/miniconda3/bin/python
# ------------------
# created 13-12-2022 @QST @Chiba
# This script to the distance between the two mutated residues in case of double mutations
# The goal : to confirm if the two residues mutated already not interact with each others
# The distance will be computed between
# 1) CA of both resides
# 2) the +ve and -ve ion of each residue (rep0 as it is wt)
# 2')the closest atoms in each residue after mutation (replast as it is fully mutated so no charge )
# ---------------
# Add all libararies required
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams["font.family"] = "serif"
# input required such as dual or ref2 or dual3
if len(sys.argv) == 4:
    dir = str(sys.argv[1])
    mut1 = int(sys.argv[2])  # the mutated residue no 1
    mut2 = int(sys.argv[3])  # the mutated residue no 2
else:
    print("please enter the ref dir name, and no of mutated residue 1 and 2 such as refab 11 34 ")
    quit()

# in this script we are calculating the distance in case of mutation K11E34 to A11S34
# so if you are using any other residues you have to modify the atoms between them the distance
# will be calculated in case of ions and closest atoms only as CA will be fixed anyway

cwd = os.getcwd()

# dir = "ref"  # this analysis only for ref in double mutation only

# Get info about the last replica from directories
os.chdir(f"{cwd}/../{dir}/prodrun/")
files = []
for i in range(1, 200):  # of course I will not have replicas more than 200 if so change this number
    if os.path.exists(str("rep"+str(i))):
        files.append(i)
    else:
        continue
replast_no = max(files)  # this consider as the total number of replicas used


# define the paths of first replica & last one
rep0 = f"{cwd}/../{dir}/prodrun/rep0/"
replast = f"{cwd}/../{dir}/prodrun/rep{replast_no}/"


# distance calculation
def dis_calculator(path):
    os.chdir(path)
    os.system(
        f"gmx distance -s run.tpr -f prodrun.part0002_center_noRot.xtc -select 'resid {mut1} and name CA plus resid {mut2} and name CA' -oall distance_res{mut1}_res{mut2}_CA.xvg")
    if path == rep0:  # os.chdir(rep0)  # wt so completely ions
        os.system(
            f"gmx distance -s run.tpr -f prodrun.part0002_center_noRot.xtc -select 'resid {mut1} and name NZ plus resid {mut2} and name OE1' -oall distance_res{mut1}_res{mut2}_ions.xvg")
    # os.chdir(replast)  # mut so no ions we choose the closest ions
    elif path == replast:
        os.system(
            f"gmx distance -s run.tpr -f prodrun.part0002_center_noRot.xtc -select 'resid {mut1} and name CB plus resid {mut2} and name OG' -oall distance_res{mut1}_res{mut2}_closestatoms.xvg")


dis_calculator(rep0)
dis_calculator(replast)


########################

# part (2) : plot the distance figures

# 1) function to pick up the data from files
def pickup_dis_data(dir, filename):
    os.chdir(dir)
    with open(filename) as f:
        data = f.readlines()
        time = []
        distance = []
        for line in data:
            if "#" in line or "@" in line:
                continue
            else:
                time.append(float(line.split()[0]))
                # *10 to convert from nm to Ang.
                distance.append(float(line.split()[1])*10)
    return time, distance


# 2) plot the distance time relation
def plot_dis_time(path):
    fig = plt.figure(figsize=(18, 12))
    plt.rc('xtick', labelsize=18)
    plt.rc('ytick', labelsize=18)
    ax = fig.add_axes([0.2, 0.2, 0.8, 0.8])
    time,  dist_CA = pickup_dis_data(
        path, f"distance_res{mut1}_res{mut2}_CA.xvg")
    ax.plot(time, dist_CA, linewidth=2, c='red',
            label=f"CA_res{mut1}_res{mut2}")
    if path == rep0:
        time1,  dist_rep0_ion = pickup_dis_data(
            rep0, f"distance_res{mut1}_res{mut2}_ions.xvg")
        ax.plot(time1, dist_rep0_ion, linewidth=2,
                c='blue', label=f"Ions_res{mut1}_res{mut2}")
        name = "rep0"  # just for figure save
    elif path == replast:
        time1,  dist_replast_catoms = pickup_dis_data(
            replast, f"distance_res{mut1}_res{mut2}_closestatoms.xvg")
        ax.plot(time1, dist_replast_catoms, linewidth=2, c='blue',
                label=f"Closest_atoms_res{mut1}_res{mut2}")
        name = "replast"

    ax.set_xlabel('Time (ns)', fontsize=18, color='black')
    ax.set_ylabel('Distance ($\AA$)', fontsize=18, color='black')
    ax.set_ylim(0, 30)
    ax.legend(loc='upper right', fontsize=16)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
        ax.spines[axis].set_linewidth(2)
    fig.savefig(f'{cwd}/../distance_time_res{mut1}_res{mut2}_{name}.png',
                bbox_inches='tight', dpi=300)


plot_dis_time(rep0)
plot_dis_time(replast)

# TODO think if possible to add function 2 and 3 in same one by using fig1, ax1 and fig2, ax2

# 3) plot the distance histogram to see the distribution of the values of the distance


def plot_dis_hist(path):
    fig = plt.figure(figsize=(18, 12))
    plt.rc('xtick', labelsize=18)
    plt.rc('ytick', labelsize=18)
    ax = fig.add_axes([0.2, 0.2, 0.8, 0.8])
    time,  dist_CA = pickup_dis_data(
        path, f"distance_res{mut1}_res{mut2}_CA.xvg")

    plt.hist(dist_CA, histtype="step", color="red", linewidth=2,
             bins=10, density=True, label=f"CA_res{mut1}_res{mut2}")

    if path == rep0:
        time1,  dist_rep0_ion = pickup_dis_data(
            rep0, f"distance_res{mut1}_res{mut2}_ions.xvg")
        plt.hist(dist_rep0_ion, histtype="step", color="blue", linewidth=2,
                 bins=10, density=True, label=f"Ions_res{mut1}_res{mut2}")
        name = "rep0"  # just for figure save
    elif path == replast:
        time1,  dist_replast_catoms = pickup_dis_data(
            replast, f"distance_res{mut1}_res{mut2}_closestatoms.xvg")
        plt.hist(dist_replast_catoms, histtype="step", color="blue", linewidth=2,
                 bins=10, density=True, label=f"Closest_atoms_res{mut1}_res{mut2}")
        name = "replast"

    ax.set_xlabel('Distance ($\AA$) ', fontsize=24, color='black')
    ax.set_ylabel('Probability distribution', fontsize=24, color='black')
    ax.legend(loc='upper right', fontsize=16)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
        ax.spines[axis].set_linewidth(2)
    fig.savefig(f'{cwd}/../distance_hist_res{mut1}_res{mut2}_{name}.png',
                bbox_inches='tight', dpi=300)


plot_dis_hist(rep0)
plot_dis_hist(replast)
