# Projet Labyrinthe | PeiP2 2023-2023 | LAURENT Esteban, RENIMEL Pacôme

## Installation :

1. Clone the repository

```bash
git clone https://github.com/herbemalveillante/ProjetPeiP24.git
```

2. Check that you have the required version of Python installed. The project has been developed with Python 3.10.0 but should work with any later version. Any version below 3.7 is guaranteed not to work.

```bash
python --version

# or

python3 --version

# or

python3.10 --version

# depending on your OS and Python installation.
```

3. (Optional) Create a virtual environment

```bash
python3 -m venv .envi
```

4. Activate the virtual environment (this may be different depending on your OS, or handled by your code editor)

```bash

# MacOS/Linux:
source .envi/bin/activate

# Windows:
.envi\Scripts\activate
```

5. Install the required packages

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

If you encounter any pygame-related issue, make sure you installed the community version of pygame, which is the one used in this project.

```bash
python3 -m pip uninstall pygame
python3 -m pip install pygame-ce
```

6. Run the game

```bash
python3 main.py
```
