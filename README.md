# IMP-utils
stuff to make your life easier


## IMP_utils_py

### getting started

1. clone this repository into your current working directory (you can also download the code as zip-file or use tools like `GitHub Desktop`)

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

## For the time stopping

- TIMESTOP_RAW_DATA_PATH: location for the csv file of the raw data

- TIMESTOP_EVALUATION_DATA_PATH: location for the csv file of the evaluation data

```
python IMP_utils_py/cli.py --mode=time-stop --gin_file=IMP_utils_py/config/config.gin
```

## For evaluating the raw data

- TIMESTOP_RAW_DATA_PATH: location of the csv file for the raw data

- TIMESTOP_EVALUATION_DATA_PATH: location for the csv file of the evaluation data

```
python IMP_utils_py/cli.py --mode=eval-raw-data --gin_file=IMP_utils_py/config/config.gin
```

## For creating a histogram with gaussian fit for the raw data

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

## For creating a errorbar plot with normed period duration

- TIMESTOP_RAW_DATA_PATH: location of the csv file for the data

- TIMESTOP_ERRORBAR_PHI_PATH: location for the png of the errorbar

- TIMESTOP_ERRORBAR_PHI_TITLE: title of errorbar

- TIMESTOP_ERRORBAR_PHI_XLABEL: x label of errorbar

- TIMESTOP_ERRORBAR_PHI_YLABEL: y label of errorbar

Column names:

- TIMESTOP_ERRORBAR_PHI_AMPLITUDE_COLUMN: column with amplitudes in degree

- TIMESTOP_ERRORBAR_PHI_NORMED_PERIOD_COLUMN: column with period durations normed with period duration of 5 degree

- TIMESTOP_ERRORBAR_PHI_ERROR_COLUMN: column with error of degree for amplitudes

Example table for raw data:

|    |   amplitude |   normed periods |   error |
|---:|------------:|-----------------:|--------:|
|  0 |           5 |          1       |     1.5 |
|  1 |          10 |          1.00139 |     1.5 |
|  2 |          15 |          1.00274 |     1.5 |
|  3 |          20 |          1.00402 |     1.5 |
|  4 |          30 |          1.00541 |     1.5 |
|  5 |          45 |          1.01253 |     1.5 |

```
python IMP_utils_py/cli.py --mode=errorbar-phi --gin_file=IMP_utils_py/config/config.gin
```

## For creating a errorbar plot with linear fit of length and squared period duration

- TIMESTOP_RAW_DATA_PATH: location of the csv file for the data

- TIMESTOP_ERRORBAR_L_PATH: location for the png of the errorbar

- TIMESTOP_ERRORBAR_L_TITLE: title of errorbar

- TIMESTOP_ERRORBAR_L_XLABEL: x label of errorbar

- TIMESTOP_ERRORBAR_L_YLABEL: y label of errorbar

- TIMESTOP_ERRORBAR_L_XTICKS_NUMBER: number of ticks on x axes (has sometimes to be adjusted a bit for a better laylout)

Column names:

- TIMESTOP_ERRORBAR_L_LENGTH_COLUMN: column with length in meters

- TIMESTOP_ERRORBAR_L_LENGTH_ERROR_COLUMN: column with length error in meters

- TIMESTOP_ERRORBAR_L_Y_COLUMN: column with $y = T^2$

- TIMESTOP_ERRORBAR_L_Y_ERROR_COLUMN: column with $\Delta y = 2 * T * \Delta T$

Example table of data:

|    |   length |   length error |       y |   y error |
|---:|---------:|---------------:|--------:|----------:|
|  0 |   1.0935 |     0.00131939 | 4.09769 |  0.518774 |
|  1 |   1.2605 |     0.00137074 | 4.91041 |  0.57056  |
|  2 |   1.3675 |     0.00140431 | 5.27111 |  0.592302 |
|  3 |   1.4945 |     0.0014448  | 5.88793 |  0.628006 |
|  4 |   1.5755 |     0.00147096 | 6.21804 |  0.646433 |
|  5 |   1.6725 |     0.00150261 | 6.67994 |  0.671512 |
|  6 |   1.7805 |     0.00153822 | 7.02253 |  0.689624 |
|  7 |   1.8895 |     0.00157456 | 7.25691 |  0.701794 |
|  8 |   1.9875 |     0.00160753 | 7.92647 |  0.735653 |
|  9 |   2.0925 |     0.00164317 | 8.05976 |  0.742244 |

**IMPORTANT:**
- currently calculation of "Steigungsunsicherheit": dm = sqrt(max(length_error)^2 + max(y_error)^2)
- the columns `length` and `length error` are both in meters (relevant for unit m/s^2 of g)

```
python IMP_utils_py/cli.py --mode=errorbar-l --gin_file=IMP_utils_py/config/config.gin
```
