#!/Users/marzouk/miniconda3/bin/python
# ------------------
# created 1-9-2022
# In this script I would like to use all the well prepared index files for omega phi psi angles
# which required for every case ref A&B and dual A&B to calculate the angles itself using the gromacs
# Running from local Machine IN QST KIZU
# modified 19-10-2022 @ QST CHIBA
# To be able to use it for addition/delete cases
# modifiy 10-11-2022
# to add dgree for angle and modify figure title
# ---------------
# Add all libararies required
import MDAnalysis as mda
from MDAnalysis.analysis import dihedrals
from MDAnalysis.analysis.data.filenames import Rama_ref
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams["font.family"] = "serif"

# input required such as dual or ref2 or dual3
if len(sys.argv) == 8:
    # del or add to decide which case and which order required
    case = str(sys.argv[1]).lower()
    dir1 = str(sys.argv[2])  # the dir required to do analysis for
    dir2 = str(sys.argv[3])
    end_step = int(sys.argv[4])
    # the residue deleted or after which added new one called target residue
    targetresid = int(sys.argv[5])
    modified_res = int(sys.argv[6])  # the no. of neighbour residue changed
    # in case of deleted residue add anu nuber in this filed say 0
    added_res = int(sys.argv[7])
else:
    print("please enter the dir names, last step, target res, modified res num. \n such as add ref3 dual3 7 88 188 189 \n or del ref4 dual4 7 73 173 0(or any no. as no add)")
    quit()

# As mentioned in previous script analysis should be start after two steps as equilibrium
start_step = 4
# Last_step better

cwd = os.getcwd()

# Get info about the last replica from directories
os.chdir(f"{cwd}/../{dir1}/prodrun/")
files = []
for i in range(1, 200):  # of course I will not have replicals more than 200 if so change this number
    if os.path.exists(str("rep"+str(i))):
        files.append(i)
    else:
        continue
replast_no = max(files)


if case == "add":
    # residues list in both state A & state B  add cases
    ####################################################
    targetresidsA = [targetresid-1, targetresid,
                     targetresid+1]  # FIXME: if u want to modify the residues
    targetresidsB = [targetresid-1, modified_res, added_res, targetresid+1]

    targetresidsA_dual = [targetresid-2, targetresid-1, targetresid,
                          targetresid+1, targetresid+2]
    targetresidsB_dual = [targetresid-2, targetresid-1,
                          modified_res, added_res, targetresid+1, targetresid+2]
if case == "del":
    # residues list in both state A & state B  delete cases
    ####################################################
    targetresidsA = [targetresid-2,
                     targetresid-1, targetresid, targetresid+1]
    targetresidsB = [targetresid-2, modified_res, targetresid+1]

    targetresidsA_dual = [targetresid-3, targetresid-2,
                          targetresid-1, targetresid, targetresid+1, targetresid+2]
    targetresidsB_dual = [targetresid-3, targetresid -
                          2, modified_res, targetresid+1, targetresid+2]

# 1) Define function to easily pickup the omega angels from the files and return data in list
# then I can use all lists to plot in one figure
# As example for ref state A we have three angles then we will get list including three big lists omega angle1 2 3


def pick_up_omega_angles(dir, state, residues):
    # define the pathes of first replica & last one
    rep0 = f"{cwd}/../{dir}/prodrun/rep0/"
    replast = f"{cwd}/../{dir}/prodrun/rep{replast_no}/"
    # chnage dir to rep0 or last rep based on state A or B entered
    if state == "A":
        os.chdir(rep0)
    elif state == "B":
        os.chdir(replast)
    residue_order = residues
    omega_data = []
    for i in range(len(residue_order) - 1):
        res1 = residue_order[i]
        res2 = residue_order[i + 1]
        with open(f"omega_{res1}_{res2}.xvg") as f:
            data = f.readlines()
            omega_angle = []
            for line in data:
                if "#" in line or "@" in line:
                    continue
                else:
                    omega_angle.append(float(line.split()[1]))
        omega_data.append(omega_angle)
    return omega_data


# run the function 4 times to get the data
refA = pick_up_omega_angles(dir1, "A",  targetresidsA)
refB = pick_up_omega_angles(dir1, "B",  targetresidsB)
dualB = pick_up_omega_angles(dir2, "B", targetresidsB)
dualA = pick_up_omega_angles(dir2, "A", targetresidsA)

# 2) Plot the omega angles for all 4 cases in one figure
# plot omega angles of the four states refA (3 angles) refB (2 angles) dualA (3 angles) dualB  (2 angles) in one figure
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(14, 10))
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)

# plot all data for each case in one graph like RefA in one grap and RefB in another graph
color = ["red", "blue", "green"]
for i in range(len(refA)):
    axes[0, 0].hist(refA[i], histtype="step", color=color[i],
                    bins=100, density=True, linewidth=2.5)
for i in range(len(refB)):
    axes[0, 1].hist(refB[i], histtype="step", color=color[i],
                    bins=100, density=True, linewidth=2.5)
for i in range(len(dualA)):
    axes[1, 0].hist(dualA[i], histtype="step", color=color[i],
                    bins=100, density=True, linewidth=2.5)
for i in range(len(dualB)):
    axes[1, 1].hist(dualB[i], histtype="step", color=color[i],
                    bins=100, density=True, linewidth=2.5)

# Defining custom 'xlim' and 'ylim' values.
plt.setp(axes, xlim=(-360, 360))
# To write titke for each subplot
axes[0, 0].set_title("Ref State A", fontsize=16, color='blue')
axes[0, 1].set_title("Ref State B", fontsize=16, color='blue')
axes[1, 0].set_title("Dual State A", fontsize=16, color='blue')
axes[1, 1].set_title("Dual State B", fontsize=16, color='blue')
# main title and labels
fig.suptitle('The $\omega$ angles for all states', fontsize=24, color='red')
fig.supxlabel('$\omega$$\degree$ ', fontsize=24, color='black')
fig.supylabel('Probability Density', fontsize=24, color='black')

fig.savefig(f'{cwd}/../omega_angles_{dir1}_{dir2}_step4_{end_step}add_nov22.png',
            bbox_inches='tight', dpi=300)


# 3) Define function to pickup the phi & psi angles from the files and return wo data lists (one for phi another for psi)

def pick_up_phi_psi_angles(dir, state, residues):
    # define the pathes of first replica & last one
    rep0 = f"{cwd}/../{dir}/prodrun/rep0/"
    replast = f"{cwd}/../{dir}/prodrun/rep{replast_no}/"
    # chnage dir to rep0 or last rep based on state A or B entered
    if state == "A":
        os.chdir(rep0)
    elif state == "B":
        os.chdir(replast)
    # Choose the residue order 4 or 3 based on the dual or ref
    residue_order = residues
    phi_data = []
    psi_data = []
    for i in range(len(residue_order) - 1):
        res1 = residue_order[i]
        res2 = residue_order[i + 1]
        with open(f"phi_{res1}_{res2}.xvg") as f:
            data = f.readlines()
            phi_angle = []
            for line in data:
                if "#" in line or "@" in line:
                    continue
                else:
                    phi_angle.append(float(line.split()[1]))
        phi_data.append(phi_angle)
        with open(f"psi_{res1}_{res2}.xvg") as f2:
            data = f2.readlines()
            psi_angle = []
            for line in data:
                if "#" in line or "@" in line:
                    continue
                else:
                    psi_angle.append(float(line.split()[1]))
        psi_data.append(psi_angle)
    return phi_data, psi_data


# Run this function to get the data for the 4 cases in diff variables

phi_refA, psi_refA = pick_up_phi_psi_angles(dir1, "A", targetresidsA)
phi_refB, psi_refB = pick_up_phi_psi_angles(dir1, "B", targetresidsB)
phi_dualA, psi_dualA = pick_up_phi_psi_angles(
    dir2, "A", targetresidsA_dual)
phi_dualB, psi_dualB = pick_up_phi_psi_angles(
    dir2, "B", targetresidsB_dual)

# 4) Define function to plot 4 Ramchandran plots for the 4 different cases refA & B dualA &B


def ramachandran_plot(dir, residues, case, phi, psi):
    # Using dir only for name saved in last step

    # decide the number of plots from the ref =2  or dual =4
    if case.strip()[:-1] == "ref":
        fig, axes = plt.subplots(
            2, 1, sharex=True, sharey=True, figsize=(8, 10))  # ,figsize=(14,10)
        # TO be able to access the axes by this way ax[0], ax[1] so on
        ax = [axes[i] for i in range(2)]   # [axes[0],axes[1]]
    if case.strip()[:-1] == "dual":
        fig, axes = plt.subplots(
            2, 2, sharex=True, sharey=True, figsize=(14, 10))
        # TO be able to access the axes by this way ax[0], ax[1] so on
        # [axes[0,0],axes[0,1],axes[1,0],axes[1,1]]
        ax = [axes[i, j] for i in range(2) for j in range(2)]

    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=16)

    for i in range(len(phi)-1):  # as angles equal residues - 1
        # Plot the common parts of the 4 figures
        ax[i].axis([-180, 180, -180, 180])
        ax[i].axhline(0, color='k', lw=1)
        ax[i].axvline(0, color='k', lw=1)
        ax[i].set(xticks=range(-180, 181, 60), yticks=range(-180, 181, 60),
                  )  # this one used for phi psi for each figure  # xlabel=r"$\phi$", ylabel=r"$\psi$",
        # control the label size after creation
        ax[i].xaxis.label.set_size(20)
        ax[i].yaxis.label.set_size(20)
        degree_formatter = plt.matplotlib.ticker.StrMethodFormatter(
            r"{x:g}$\degree$")
        ax[i].xaxis.set_major_formatter(degree_formatter)
        ax[i].yaxis.set_major_formatter(degree_formatter)
        X, Y = np.meshgrid(np.arange(-180, 180, 4), np.arange(-180, 180, 4))
        levels = [1, 17, 15000]
        colors = ['#A1D4FF', '#35A1FF']
        ax[i].contourf(X, Y, np.load(Rama_ref), levels=levels, colors=colors)

        # adjust certain color for specific angle, we use dictiionary instead of normal list
        color_add = {
            f"{targetresidsA[0]}": "red",
            f"{targetresidsA[1]}": "darkgreen",
            f"{targetresidsB[1]}": "darkgreen",
            f"{targetresidsA[2]}": "gold",
            f"{targetresidsB[2]}": "indigo"
        }
        # IMP Line for plot the data
        ax[i].scatter(phi[i], psi[i+1],
                      c=color_add[f"{residues[i+1]}"], marker='.')
        # NOTE : phi1 & psi2 as first residue phi is phi1 but psi is psi2 based on psi defination
        # Add title for each one based on rediues number
        ax[i].set_title(
            f"Residue number {residues[i+1]} ", fontsize=18, color='blue')
        for axis in ['top', 'bottom', 'left', 'right']:
            ax[i].spines[axis].set_linewidth(2)

    fig.supxlabel('$\phi$', fontsize=24, color='black')
    fig.supylabel('$\psi$', fontsize=24, color='black')
    fig.suptitle(
        f' {case.strip()[:-1]} {case.strip()[-1]} angles', fontsize=24, color='black')  # Ramachandran plot for
    fig.savefig(f'{cwd}/../ramchandran_plot_{dir}_{end_step}_{case}_nov22.png',
                bbox_inches='tight', dpi=300)


ramachandran_plot(dir2, targetresidsA_dual, "dualA", phi_dualA, psi_dualA)
ramachandran_plot(dir2, targetresidsB_dual, "dualB", phi_dualB, psi_dualB)
ramachandran_plot(dir1, targetresidsA, "refA", phi_refA, psi_refA)
ramachandran_plot(dir1, targetresidsB, "refB", phi_refB, psi_refB)
