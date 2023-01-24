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

- TIMESTOP_RAW_DATA_PATH: location for the csv file of the raw data

- TIMESTOP_EVALUATION_DATA_PATH: location for the csv file of the evaluation data

```
python IMP_utils_py/cli.py --mode=time-stop --gin_file=IMP_utils_py/config/config.gin
```

**For evaluating the raw data**

- TIMESTOP_RAW_DATA_PATH: location of the csv file for the raw data

- TIMESTOP_EVALUATION_DATA_PATH: location for the csv file of the evaluation data

```
python IMP_utils_py/cli.py --mode=eval-raw-data --gin_file=IMP_utils_py/config/config.gin
```

**For creating a histogram with gaussian fit for the raw data**

- TIMESTOP_RAW_DATA_PATH: location of the csv file for the data

- TIMESTOP_HIST_PATH: location for the png of the histogram

- TIMESTOP_HIST_COLUMN: column name from data to use for the histogram

- TIMESTOP_HIST_CLASS_NUMBER: number of classes in the histogram

- TIMESTOP_HIST_TITLE: title of histogram

- TIMESTOP_HIST_XLABEL: x label of histogram

- TIMESTOP_HIST_YLABEL: y label of histogram

- TIMESTOP_HIST_NORMED_Y: y ticks normed (True or False)

```
python IMP_utils_py/cli.py --mode=hist-gauss --gin_file=IMP_utils_py/config/config.gin
```
