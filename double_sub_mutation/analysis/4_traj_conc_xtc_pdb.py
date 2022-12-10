#!/Users/marzouk/miniconda3/bin/python
# ------------------
# created 24-8-2022
# This script to concatenate all the output trajectories after 2nd step
# This means leave first two steps as continue for equilibration then run analysis
# Running from local Machine IN QST KIZU
# Modifed4-9-2022
# better to get the last step for trajectories concatenate as input because some time I need it certain part
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
    dir = str(sys.argv[1])  # the dir required to do analysis for
    end_step = int(sys.argv[2])
else:
    print("please enter the dir name and last step to stop at  such as dual3  11")
    quit()
# IMP Note
# The strating step from which u want to do analysis
# Almost use 4 as beginig because 2 & 3 are fitst two steps so u can consider them as equilibrium
start_step = 4    # analysis should be start after two steps as equilibrium
# Last_step will be defined automatically
cwd = os.getcwd()

# define function that can do all preparation steps required for trajectories


def preparing_traj(path):
    os.chdir(path)
    # Detect the last traj automatic  #4-9-22 better to add this number as input
    # files = []
    # for i in range(2, 20):
    #     if os.path.exists(str("prodrun.part000"+str(i)+".log")):
    #         files.append(i)
    #     else:
    #         continue
    # end_step = max(files)
    # (1) Create pdb file from the gro file to help me in the ndx file next step
    os.system("gmx editconf -f prodrun.part0002.gro -o prodrun.part0002.pdb")

    # (2) concatenate all trajectories after 2 and change the traj from trr to xtc
    os.system(
        f"gmx trjcat -f prodrun.part000{{4..{end_step}}}.trr -o prodrun.part0004_{end_step}.xtc")

    # (3) remove the pbc and wraping the system
    os.system(
        f"echo  \"System\" \"System\" | gmx trjconv -s run.tpr -f prodrun.part0004_{end_step}.xtc -o prodrun.part0004_{end_step}_center.xtc -center -pbc mol -ur compact")

    # (4) Calculate the RMSD for the output traj
    # choose Backbone first then Protein
    os.system(
        f"echo  \"Backbone\" \"Protein\" |gmx rms -s run.tpr -f  prodrun.part0004_{end_step}_center.xtc -o rmsd_traj_4_{end_step}.xvg -tu ns")


# Get info about the last replica from directories
os.chdir(f"{cwd}/../{dir}/prodrun/")
files = []
for i in range(1, 200):  # of course I will not have replicals more than 200 if so change this number
    if os.path.exists(str("rep"+str(i))):
        files.append(i)
    else:
        continue
replast_no = max(files)

# define the pathes of first replica & last one
rep0 = f"{cwd}/../{dir}/prodrun/rep0/"
replast = f"{cwd}/../{dir}/prodrun/rep{replast_no}/"


# function running
preparing_traj(rep0)
preparing_traj(replast)
