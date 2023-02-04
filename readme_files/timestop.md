# Timestop functions

Run the following commands in the terminal (current working directory: `IMP-utils` folder). You can change the available parameter of the functions in `IMP_utils_py/config/timestop_config.gin`.

## table of content

- [time-stop](#time-stop): time stopping of periods

- [eval-raw-data](#eval-raw-data): evaluating raw data

- [hist-gauss](#hist-gauss): creating a histogram with gaussian fit for the raw data

- [errorbar-phi](#errorbar-phi): creating a errorbar plot with normed period duration

- [errorbar-l](#errorbar-l): creating a errorbar plot with linear fit of length and squared period duration

<a name="time-stop"/>

## For the time stopping

- RAW_DATA_PATH: location for the csv file of the raw data

- EVALUATION_DATA_PATH: location for the csv file of the evaluation data

**Instructions:**

1. you can start the time measurement with the "space" key and every time you click it, the time is taken

2. to end the measurement press "a", to pause the measurement press "p" and start it with "space" again

3. the program will automatically create two files one with the raw data and one with its evaluation values

**INFO:**

- the three counting types are (all will be shown in raw and evaluation data):

    - periods: every click means a new period
    - half periods: every second click means a period and the others are ignored
    - half periods v2: the periods will be 1+2, 2+3, 3+4, 4+5, ... (every time is used for two periods)

- the program needs a moment to initialize and a message will appear when the program is ready for the key board input


```
python IMP_utils_py/cli.py --mode=time-stop --gin_file=IMP_utils_py/config/timestop_config.gin
```

<a name="eval-raw-data"/>

## For evaluating the raw data

- RAW_DATA_PATH: location of the csv file for the raw data

- EVALUATION_DATA_PATH: location for the csv file of the evaluation data

**Instructions:**

- the raw data will be evaluated and as an evaluation file saved (old evaluation file will be overwritten)


```
python IMP_utils_py/cli.py --mode=eval-raw-data --gin_file=IMP_utils_py/config/timestop_config.gin
```

<a name="hist-gauss"/>

## For creating a histogram with gaussian fit for the raw data

- RAW_DATA_PATH: location of the csv file for the data

- HIST_PATH: location for the png of the histogram

- HIST_COLUMN: column name from data to use for the histogram

- HIST_CLASS_NUMBER: number of classes in the histogram

- HIST_TITLE: title of histogram

- HIST_XLABEL: x label of histogram

- HIST_YLABEL: y label of histogram

- HIST_NORMED_Y: y ticks normed (True or False)

```
python IMP_utils_py/cli.py --mode=hist-gauss --gin_file=IMP_utils_py/config/timestop_config.gin
```

<a name="errorbar-phi"/>

## For creating a errorbar plot with normed period duration

- RAW_DATA_PATH: location of the csv file for the data

- ERRORBAR_PHI_PATH: location for the png of the errorbar

- ERRORBAR_PHI_TITLE: title of errorbar

- ERRORBAR_PHI_XLABEL: x label of errorbar

- ERRORBAR_PHI_YLABEL: y label of errorbar

Column names:

- ERRORBAR_PHI_AMPLITUDE_COLUMN: column with amplitudes in degree

- ERRORBAR_PHI_NORMED_PERIOD_COLUMN: column with period durations normed with period duration of 5 degree

- ERRORBAR_PHI_ERROR_COLUMN: column with error of degree for amplitudes

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
python IMP_utils_py/cli.py --mode=errorbar-phi --gin_file=IMP_utils_py/config/timestop_config.gin
```

<a name="errorbar-l"/>

## For creating a errorbar plot with linear fit of length and squared period duration

- RAW_DATA_PATH: location of the csv file for the data

- ERRORBAR_L_PATH: location for the png of the errorbar

- ERRORBAR_L_TITLE: title of errorbar

- ERRORBAR_L_XLABEL: x label of errorbar

- ERRORBAR_L_YLABEL: y label of errorbar

- ERRORBAR_L_XTICKS_NUMBER: number of ticks on x axes (has sometimes to be adjusted a bit for a better laylout)

Column names:

- ERRORBAR_L_LENGTH_COLUMN: column with length in meters

- ERRORBAR_L_LENGTH_ERROR_COLUMN: column with length error in meters

- ERRORBAR_L_Y_COLUMN: column with $y = T^2$ with $T$ single period duration

- ERRORBAR_L_Y_ERROR_COLUMN: column with $\Delta y = 2 * T * \Delta T$ with $\Delta T$ the error of a single period duration

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
- current calculation of $\Delta m = \sqrt{max(length_{error})^2 + max(y_{error})^2}$ (Unsicherheit der Steigung $m$)
- calculation of $g = \frac{4\pi^2}{m}$ (Gravitationsbeschleunigung)
- calculation of $\Delta g = \sqrt{\left(\frac{4\pi^2}{m^2} \cdot \Delta m\right)^2}$ (Unsicherheit der Gravitationsbeschleunigung)
- the columns `length` and `length error` are both in meters (relevant for unit $m/s^2$ of $g$)

```
python IMP_utils_py/cli.py --mode=errorbar-l --gin_file=IMP_utils_py/config/timestop_config.gin
```
