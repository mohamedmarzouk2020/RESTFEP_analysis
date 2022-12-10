#!/Users/marzouk/miniconda3/bin/python
# ------------------
# created 1-9-2022
# In this script I would like to use all the well prepared index files for omega phi psi angles
# which required for every case ref A&B and dual A&B to calculate the angles itself using the gromacs
# Running from local Machine IN QST KIZU
# Modifed4-9-2022
# better to get the last step for trajectories concatenate as input because some time I need it certain part
# TODO : I think it is very easy to combine the two functions together to make the code more clean but TAKECARE of omega and residues for dual case
# ---------------
# Add all libararies required
import numpy as np
import os
import sys

# input required such as dual or ref2 or dual3
if len(sys.argv) == 6:
    dir1 = str(sys.argv[1])  # ref dir
    dir2 = str(sys.argv[2])  # dual dir
    end_step = int(sys.argv[3])
    targetresid = int(sys.argv[4])  # the residue deleted or added
    modified_res = int(sys.argv[5])  # the no. of neighbour residue changed
else:
    print("please enter the dir names, last step, target res, modified res num. \n such as ref3 dual3 9 73 172 ")
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


# residues list in both state A & state B
##########################################
targetresidsA = [targetresid-2, targetresid-1, targetresid,
                 targetresid+1]  # FIXME: if u want to modify the residues
targetresidsB = [targetresid-2, modified_res, targetresid+1]

targetresidsA_dual = [targetresid-3, targetresid-2, targetresid-1, targetresid,
                      targetresid+1, targetresid+2]
targetresidsB_dual = [targetresid-3, targetresid -
                      2, modified_res, targetresid+1, targetresid+2]

# IMP NOTE for OMEGA ANGLE
# residues chosen in dual and ref are the same (3 for state A and 2 for state B) because the angle between the two residues
# So use targetresidsA & B in omega
# FOR PHI & PSI
# the angles needs one atom form previous residues so we increase one in both cases then dual with ( 5 stA + 4 stB)
# while ref still the same as limited by residue numbers (3 for state A and 2 for state B)
# So use targetresidsA & B for ref in phi_psi and targetresidsA_dual & B_dual for dual
# As a result I have to make function for omega and another for phi_psi


def omega_calculator(dir, state, residues):
   # define the paths of first replica & last one based on dir ( ref or dual)
    rep0 = f"{cwd}/../{dir}/prodrun/rep0/"
    replast = f"{cwd}/../{dir}/prodrun/rep{replast_no}/"
   # chnage dir to rep0 or last rep based on state A or B entered
    if state == "A":
        os.chdir(rep0)
    elif state == "B":
        os.chdir(replast)

    # # Detect the last traj automatic
    # files = []
    # for i in range(2, 20):
    #     if os.path.exists(str("prodrun.part000"+str(i)+".log")):
    #         files.append(i)
    #     else:
    #         continue
    # end_step = max(files)

    residue_order = residues
    for i in range(len(residue_order) - 1):
        res1 = residue_order[i]
        res2 = residue_order[i + 1]
        # (1) Calculate the omega angles
        os.system(
            f"echo \"omega{res1}{res2}\" | gmx angle -f prodrun.part0004_{end_step}_center.xtc -n omegaindex_{dir}_stat{state}.ndx -type dihedral -ov omega_{res1}_{res2}.xvg -od omega_{res1}_{res2}distribution.xvg")


def phi_psi_calculator(dir, state, residues):
   # define the paths of first replica & last one based on dir ( ref or dual)
    rep0 = f"{cwd}/../{dir}/prodrun/rep0/"
    replast = f"{cwd}/../{dir}/prodrun/rep{replast_no}/"
   # chnage dir to rep0 or last rep based on state A or B entered
    if state == "A":
        os.chdir(rep0)
    elif state == "B":
        os.chdir(replast)

    # # Detect the last traj automatic
    # files = []
    # for i in range(2, 20):
    #     if os.path.exists(str("prodrun.part000"+str(i)+".log")):
    #         files.append(i)
    #     else:
    #         continue
    # end_step = max(files)

    residue_order = residues
    for i in range(len(residue_order) - 1):
        res1 = residue_order[i]
        res2 = residue_order[i + 1]
        # (1) Calculate the phi angles
        os.system(
            f"echo \"phi{res1}{res2}\" | gmx angle -f prodrun.part0004_{end_step}_center.xtc -n phiindex_{dir}_stat{state}.ndx -type dihedral -ov phi_{res1}_{res2}.xvg -od phi_{res1}_{res2}_distribution.xvg")
        # (2) Calculate the psi angles
        os.system(
            f"echo \"psi{res1}{res2}\" | gmx angle -f prodrun.part0004_{end_step}_center.xtc -n psiindex_{dir}_stat{state}.ndx -type dihedral -ov psi_{res1}_{res2}.xvg -od psi_{res1}_{res2}_distribution.xvg")


omega_calculator(dir1, "A", targetresidsA)
omega_calculator(dir1, "B", targetresidsB)
# take the same residues group of the ref as angles between 2 atoms not one like phi psi
omega_calculator(dir2, "A", targetresidsA)
omega_calculator(dir2, "B", targetresidsB)

phi_psi_calculator(dir1, "A", targetresidsA)
phi_psi_calculator(dir1, "B", targetresidsB)
phi_psi_calculator(dir2, "A", targetresidsA_dual)
phi_psi_calculator(dir2, "B", targetresidsB_dual)
