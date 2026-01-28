#!/usr/bin/env python3


from pathlib import Path
import subprocess
import sys   

#creating a function that allows stdout and stderr to be captured in log files
logdir = Path("logs")
logdir.mkdir(exist_ok = True) #safely creates logs directory if it doesn't already exist

def run_command(cmd, step_name):
    out_file = logdir/f"{step_name}.out"
    err_file = logdir/f"{step_name}.err"
    print (f"Logging to: {out_file}, {err_file}")
    with open (out_file, "w") as out, open (err_file, "w") as err:
        result = subprocess.run(cmd, stdout = out, stderr = err)
    
    if result.returncode != 0:
        print ("ERROR")
        sys.exit(1)
    print(f"{step_name} completed successfully")

def run_pdb2gmx(pdb_file):
    print("Generating coordinate file in GROMACS format")
    cmd = ("gmx", "pdb2gmx", "-f", pdb_file, "-p", "topol.top",
           "-o", "processed.gro", "-water", "tip3p", "-ignh", "-ter")

    #user_inputs = ("1\n1\n1n\")#if you want to hardcode the interactive
    #inputs, set an input flag in the subprocess call and set text = True
    
    run_command(cmd, "pdb2gmx")
     
def run_editconf():
    print("specifiying simulation box")
    cmd = ("gmx", "editconf", "-f", "processed.gro", "-d", "4",
           "-bt", "dodecahedron", "-o", "newbox.gro")
    
    run_command(cmd, "editconf")
    
def run_solvate():
    print("solvating the simulation box")
    cmd = ("gmx", "solvate", "-cp", "newbox.gro", "-cs", "spc216.gro",
            "-o", "solvate.gro", "-p", "topol.top")
    result = subprocess.run(cmd)

    run_command(cmd, "solvate")

#specifying different parameters in the function 
#for grompp and mdrun for iterative handling
    
def run_grompp(mdp, gro, tpr):
    print("Generating binary file: {tpr}")
    cmd = ("gmx", "grompp", "-f", mdp, "-c", "solvate.gro",
           "-p", "topol.top", "-o", tpr)
    result = subprocess.run(cmd)

    run_command(cmd, "grompp")

def run_mdrun(deffnm):
    print(f"starting {defnm} production")
    cmd = ("gmx", "mdrun", "-v", "-deffnm", deffnm)
    result = subprocess.run(cmd)

    run_command(cmd, "mdrun")

def main():
    pdb_files = list(Path('.').glob('*.pdb'))
    if not pdb_files:
        print("Error: no .pdb files found")
        sys.exit(1)
    pdb_file = pdb_files[0].name

    run_pdb2gmx(pdb_file)
    run_editconf()
    run_solvate()
    
    ######  MINIMIZATION ######
    run_grompp("em.mdp", "solvate.gro", "em.tpr")
    run_mdrun("em")
    
    ######  NVT EQUILIBRATION ######
    run_grompp("nvt.mdp", "em.gro", "nvt.tpr")
    run_mdrun("nvt")

    ######  NPT EQUILIBRATION ######
    run_grompp("npt.mdp", "nvt.gro", "npt.tpr")
    run_mdrun("npt")

     ######  PRODUCTION RUN ######
    run_grompp("prod.mdp", "npt.gro", "prod.tpr")
    run_mdrun("prod")
    
if __name__ == "__main__":
    main()
