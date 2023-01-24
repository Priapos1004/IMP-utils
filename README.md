# IMP-utils
stuff to make your life easier


## IMP_utils_py

### getting started

1. clone this repository into your current working directory (you can also download the code as zip-file)

```
git clone https://github.com/Priapos1004/IMP-utils
```

2. go into the `IMP-utils` folder

```
cd IMP-utils/
```

3. install the package to your activated virtual environment

```
pip install -e .
```

4. now you can use the package:

Run the following commands in the terminal (current working directory: `IMP-utils` folder). You can change the available parameter of the functions in `IMP_utils_py/config/config.gin`.

**For the time stopping**

```
python IMP_utils_py/cli.py --mode=time-stop --gin_file=IMP_utils_py/config/config.gin
```

**For evaluating the raw data**

```
python IMP_utils_py/cli.py --mode=eval-raw-data --gin_file=IMP_utils_py/config/config.gin
```

**For creating a histogram with gaussian fit for the raw data**

```
python IMP_utils_py/cli.py --mode=hist-gauss --gin_file=IMP_utils_py/config/config.gin
```
