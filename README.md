# HFR_PACKAGE

A Python package for generating and analyzing **homodesmotic reaction enthalpies** using RDKit, PuLP, and AaronTools.

---

## Features

- Balance homodesmotic reactions automatically.
- Compute reaction enthalpies from Gaussian output.
- Support for single and multiple computation workflows.
- Command-line interface (CLI) tools for ease of use.

---

## Installation

### Prerequisites

This package depends on some scientific libraries that are easiest to install via **Conda**:

- [RDKit](https://www.rdkit.org/docs/Install.html)  
- [PuLP](https://coin-or.github.io/pulp/)  
- [AaronTools](https://github.com/QChASM/AaronTools.py) (installed automatically via pip)

### Using Conda Environment (Recommended)

1. Create the conda environment from the provided `environment.yml`:

   ```bash
   conda env create -f environment.yml
   conda activate hfrpkg-env
