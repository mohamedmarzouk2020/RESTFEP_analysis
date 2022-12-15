#!/Users/marzouk/miniconda3/bin/python
# ------------------
# created 24-8-2022
# This script to concatenate all the output trajectories after 2nd step
# This means leave first two steps as continue for equilibration then run analysis
# Running from local Machine IN QST KIZU
# Modified 12-12-2022 @Chiba for double mutation or lets say for the very basic cases of just 8 steps
# we will deal with only one traj
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
    print("please enter the dir name such as dual3 ")
    quit()

# IMP Note
"""
In this study we usually got the convergence too quickly so only one step is
enough then no more steps like the add/delete mutation so script a little bit modified
"""
cwd = os.getcwd()

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


# define function that can do all preparation steps required for trajectories
def preparing_traj(path):
    os.chdir(path)
    # (1) Create pdb file from the gro file to help me in the ndx file next step
    # u have to remove the pbc to create this pdb as well
    os.system(f"echo  \"System\" | gmx trjconv -s run.tpr -f prodrun.part0002.gro -o prodrun.part0002.pdb -ur compact -pbc atom")

    #  (2)  convert the .trr traj to .xtc
    os.system(
        f"gmx trjcat -f prodrun.part0002.trr -o prodrun.part0002.xtc")

    # (3) Remove the PBC in two steps a) Centering the protein in the center of the box and all others around it b) remove the translation and rotation motion then u keep only the vibrational
    # Centering the protein in the center of the box
    os.system(
        f"echo  \"System\" \"System\" | gmx trjconv -s run.tpr -f prodrun.part0002.xtc -o prodrun.part0002_center.xtc  -pbc mol -center -ur compact")

    # removing the rotation and translation
    os.system(f"echo  \"System\" \"System\" | gmx trjconv -s run.tpr -f prodrun.part0002_center.xtc -o prodrun.part0002_center_noRot.xtc  -fit rot+trans")

    #  (4) Calculate the RMSD for the output traj
    # # choose Backbone first then Protein
    os.system(
        f"echo  \"Backbone\" \"Protein\" |gmx rms -s run.tpr -f   prodrun.part0002_center_noRot.xtc  -o rmsd_protein.xvg -tu ns")


# running function for two cases the first replica and the last one
preparing_traj(rep0)
preparing_traj(replast)
