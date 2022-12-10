#!/Users/marzouk/miniconda3/bin/python
# ------------------
# created 4-9-2022
# This script to create index files for omega & phi & psi angles
# from the pdb file of rep0 rep_last of ref & dual
# Running from local Machine IN QST KIZU
# TODO : idea to combine the 3 functions for omega, phi, psi all in one function
# ---------------
# Add all libararies required
import MDAnalysis as mda
from MDAnalysis.analysis import dihedrals
import numpy as np
import os
import sys

# input required such as dual or ref2 or dual3
if len(sys.argv) == 6:
    dir1 = str(sys.argv[1])  # the dir required to do analysis for
    dir2 = str(sys.argv[2])
    end_step = int(sys.argv[3])
    targetresid = int(sys.argv[4])  # the residue deleted or added
    modified_res = int(sys.argv[5])  # the no. of neighbour residue changed
else:
    print("please enter the dir names, last step, target res, modified res num. \n such as ref3 dual3 9 73 172")
    quit()

cwd = os.getcwd()

# Get info about the last replica from ref directories to its save
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
targetresidsA_ref = [targetresid-2, targetresid-1, targetresid,
                     targetresid+1]  # FIXME: if u want to modify the residues
targetresidsB_ref = [targetresid-2, modified_res, targetresid+1]

targetresidsA_dual = [targetresid-3, targetresid-2, targetresid-1, targetresid,
                      targetresid+1, targetresid+2]
targetresidsB_dual = [targetresid-3, targetresid -
                      2, modified_res, targetresid+1, targetresid+2]


# 1) Function to make index for omega angles at each residue in ref and dual cases
def omega_index(dir, state, residues):  # state,residues
    # define the paths of first replica & last one based on dir ( ref or dual)
    rep0 = f"{cwd}/../{dir}/prodrun/rep0/"
    replast = f"{cwd}/../{dir}/prodrun/rep{replast_no}/"
    # chnage dir to rep0 or last rep based on state A or B entered
    if state == "A":
        os.chdir(rep0)
    elif state == "B":
        os.chdir(replast)
    structure = mda.Universe("prodrun.part0002.pdb")
    with open(f"omegaindex_{dir}_stat{state}.ndx", "w") as index_file:
        # choose the spec. residues corr. to case such as RefA 4 residues refB 3 so on
        residue_order = residues

        # define the omega angles for residues
        for i in range(len(residue_order) - 1):
            res1 = residue_order[i]
            res2 = residue_order[i + 1]
            omega_definition = [
                (res1, "O"),
                (res1, "C"),
                (res2, "N"),
                (res2, "H")
            ]
            output_buffer = []
            for res, atomname in omega_definition:
                atom = structure.select_atoms(
                    f"resid {res} and name {atomname}")[0]
                output_buffer.append(atom.ix + 1)
            print(f"[ omega_{res1}_{res2} ]", file=index_file)
            print(*output_buffer, file=index_file)


# 2) Function to make index for phi angles at each residue in ref  and dual cases
def phi_index(dir, state, residues):
    # define the paths of first replica & last one based on dir ( ref or dual)
    rep0 = f"{cwd}/../{dir}/prodrun/rep0/"
    replast = f"{cwd}/../{dir}/prodrun/rep{replast_no}/"
    # chnage dir to rep0 or last rep based on state A or B entered
    if state == "A":
        os.chdir(rep0)
    elif state == "B":
        os.chdir(replast)
    structure = mda.Universe("prodrun.part0002.pdb")
    with open(f"phiindex_{dir}_stat{state}.ndx", "w") as index_file:
        residue_order = residues
        for i in range(len(residue_order) - 1):
            res1 = residue_order[i]
            res2 = residue_order[i + 1]
            phi_definition = [
                (res1, "C"),
                (res2, "N"),
                (res2, "CA"),
                (res2, "C")
            ]
            output_buffer = []
            for res, atomname in phi_definition:
                atom = structure.select_atoms(
                    f"resid {res} and name {atomname}")[0]
                output_buffer.append(atom.ix + 1)

            print(f"[ phi_{res1}_{res2} ]", file=index_file)
            print(*output_buffer, file=index_file)


# 3) Function to make index for psi angles at each residue in ref  and dual cases
def psi_index(dir, state, residues):  # state,residues
    # define the paths of first replica & last one based on dir ( ref or dual)
    rep0 = f"{cwd}/../{dir}/prodrun/rep0/"
    replast = f"{cwd}/../{dir}/prodrun/rep{replast_no}/"
    # chnage dir to rep0 or last rep based on state A or B entered
    if state == "A":
        os.chdir(rep0)
    elif state == "B":
        os.chdir(replast)
    structure = mda.Universe("prodrun.part0002.pdb")
    with open(f"psiindex_{dir}_stat{state}.ndx", "w") as index_file:
        residue_order = residues
        for i in range(len(residue_order) - 1):
            res1 = residue_order[i]
            res2 = residue_order[i + 1]
            psi_definition = [
                (res1, "N"),
                (res1, "CA"),
                (res1, "C"),
                (res2, "N")
            ]
            output_buffer = []
            for res, atomname in psi_definition:
                atom = structure.select_atoms(
                    f"resid {res} and name {atomname}")[0]
                output_buffer.append(atom.ix + 1)

            print(f"[ psi_{res1}_{res2} ]", file=index_file)
            print(*output_buffer, file=index_file)


omega_index(dir1, "A", targetresidsA_ref)
omega_index(dir1, "B", targetresidsB_ref)
omega_index(dir2, "A", targetresidsA_dual)
omega_index(dir2, "B", targetresidsB_dual)

phi_index(dir1, "A", targetresidsA_ref)
phi_index(dir1, "B", targetresidsB_ref)
phi_index(dir2, "A", targetresidsA_dual)
phi_index(dir2, "B", targetresidsB_dual)

psi_index(dir1, "A", targetresidsA_ref)
psi_index(dir1, "B", targetresidsB_ref)
psi_index(dir2, "A", targetresidsA_dual)
psi_index(dir2, "B", targetresidsB_dual)
