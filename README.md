# IMP-utils
stuff to make your life easier


## IMP_utils_py

### pre-requirements

python version 3.9 or higher is required for using the package

*check your python version in the terminal with:*

```
python --version
```

You can install python, a virtual environment managementsystem, and nearly all packages you will ever need with simply installing [anaconda](https://www.anaconda.com/download) *(highly recommended)*

### getting started

1. clone this repository into your current working directory (you can also download the code as zip-file or use tools like [GitHub Desktop](https://desktop.github.com))

```
git clone https://github.com/Priapos1004/IMP-utils
```

2. go into the `IMP-utils` folder

```
cd IMP-utils/
```

3. install the package to your activated virtual environment (don't forget the `.` at the end of the command)

```
pip install -e .
```

4. now you can use the package:

You can find the terminal commands of the package in '[readme files](readme_files)' and edit the parameters of the commands in the different gin-files in `IMP_utils_py/config/`.

**ALLWAYS** run the commands with the current working directory: `IMP-utils` folder

### command sets

- [timestop](readme_files/timestop.md): Einführungspraktikum Physik (Fadenpendel)
- [plotting](readme_files/plotting.md): general plotfunctions *(beinhaltet benötigte Funktionen für folgende Experimente des Grundpraktikums: O6, M12, T4, E5, E12, E1, A2, O11)*
- [playground](readme_files/playground.md): helpful tools *(e.g. grade calculation)*

### example notebooks

- [timestop and pandas](IMP_utils_py_examples/timestop.ipynb): Pandas basics for timestop
