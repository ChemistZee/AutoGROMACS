# GROMACS MD Automation Script

This repository contains a Python script that automates core steps of a
GROMACS molecular dynamics (MD) workflow. The goal is to provide a simple,
readable, and extensible pipeline for running standard GROMACS preprocessing
and minimization steps while preserving GROMACS’ interactive behavior when
needed.

## Features

- Automates common GROMACS steps:
  - `pdb2gmx`
  - `editconf`
  - `solvate`
  - `grompp`
  - `mdrun`
- Uses Python’s `subprocess` module to call GROMACS commands
- Checks return codes and stops execution on failure
- Preserves interactive GROMACS input (menus/prompts) when required
- Designed to be readable and easy to extend for additional MD steps

## Requirements

- Python 3
- GROMACS (accessible via the `gmx` command in your PATH)
- A valid input `.pdb` file
- Required GROMACS input files (e.g., `.mdp` files)

## Usage

Make the script executable:

```bash
chmod +x gromacs.py
