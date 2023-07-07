# plotting functions

Run the following commands in the terminal (current working directory: `IMP-utils` folder). You can change the available parameter of the functions in `IMP_utils_py/config/plotting.gin`. The path parameters in `plotting.gin` have to be relative to the `IMP-utils` folder.

## table of content

- [errorbar-plot](#errorbar-plot): errorbar plot with possible linear fit(with and without intercept zero)

- [residual-plot](#residual-plot): residual plot for linear fit function (with and without intercept zero)

<a name="errorbar-plot"/>

## errorbar plot

### path parameters

*(not effected by multiple plots in one graph)*

- RAW_DATA_PATH: location of the csv/excel file with the data
  - `string` e.g. "raw_data.csv" or "raw_data.xlsx"

- ERRORBAR_PLOT_PATH: location for the png of the plot
  - `string` e.g. "plot.png"

### column name parameters

- ERRORBAR_PLOT_X_COLUMN: column name of column with x values
  - `string` e.g. "L"
  - `list of strings` e.g. ["L1", "L2", "L3"]

- ERRORBAR_PLOT_X_ERROR_COLUMN: column name of column with errors of x values
  - `string` e.g. "u_L"
  - `list of strings` e.g. ["u_L1", "", "u_L3"]
  - **NOTE:** use an empty string "" to provide no error column for the x-values

- ERRORBAR_PLOT_Y_COLUMN: column name of column with y values
  - `string` e.g. "f"
  - `list of strings` e.g. ["f1", "f2", "f3"]

- ERRORBAR_PLOT_Y_ERROR_COLUMN: column name of column with errors of y values
  - `string` e.g. "u_f"
  - `list of strings` e.g. ["u_f1", "u_f2", ""]
  - **NOTE:** use an empty string "" to provide no error column for the y-values

### plot legend parameters

- ERRORBAR_PLOT_TITLE: title 
  - `string` e.g. "f(L)-Diagramm"
  - **NOTE:** use an empty string "" if there shall be no title for this plot

- ERRORBAR_PLOT_XLABEL: label of x axes
  - `string` e.g. "Länge L in m"
  - **NOTE:** use an empty string "" if there shall be no label for this axes

- ERRORBAR_PLOT_YLABEL: label of y axes
  - `string` e.g. "Frequenz f in Hz"
  - **NOTE:** use an empty string "" if there shall be no label for this axes

- ERRORBAR_PLOT_PLOTLABELS: label for plot in legend
  - `string` e.g. "Frequenz f"
  - `list of strings` e.g. ["Frequenz f1", "Frequenz f2", "Frequenz f3"]
  - **NOTE:** use an empty string "" if there shall be no label for this plot

- ERRORBAR_PLOT_XTICKS_NUMBER: number of ticks on x axes *(has sometimes to be adjusted a bit for a better laylout)*
  - `string` if ERRORBAR_PLOT_XTICKS_NUMBER='auto', the optimal number of x-ticks will be calculated
  - `integer` e.g. 8

- ERRORBAR_PLOT_MIN_XTICKS: min value of ticks on x axes
  - `string` if ERRORBAR_PLOT_MIN_XTICKS='auto', the min tick will be the rounded down min x value from the data
  - `float`/`integer` e.g. 125 or 0.65

- ERRORBAR_PLOT_MAX_XTICKS: max value of ticks on x axes
  - `string` if ERRORBAR_PLOT_MAX_XTICKS='auto', the max tick will be the rounded up max x value from the data
  - `float`/`integer` e.g. 125 or 0.65

### function parameter

- ERRORBAR_PLOT_MODEL: choose the model for the linear fit
  - `string` e.g. "linear"
  - `list of strings` e.g. ["linear", "constant", "none"]
  - 'linear' *(y = m\*x + n)* / 'linear_zero' *(y = m\*x)* / 'constant' *(y = n)* / 'weighted_average' *(y = w_avg)* / 'none' *(no fit will be created)*
  - additionally, you can plot the theoretical Reflexioncoefficientsgraphs from experiment O11 *(Grundpraktikum)* with 'O11_Rs' and 'O11_Rp' (see [example](https://github.com/Priapos1004/IMP-utils/blob/main/readme_files/plotting_examples.md#O11-plot-example) and special command for this plot)

- ERRORBAR_PLOT_SHOW_MODELERROR: if True, the y-error of the model will be shown as light colored area
  - `boolean` e.g. True
  - `list of boolean` e.g. [True, True, False]
  - will create no errorareas for ERRORBAR_PLOT_MODEL = 'linear_zero' and ERRORBAR_PLOT_MODEL = 'none'

- ERRORBAR_PLOT_EXTRA_LOG: if True, additional logs will be shown in console
  - `boolean`
  - additional log:
    - if ERRORBAR_PLOT_MODEL = "linear":
      - Nullstelle *(-n/m)*
      - Unsicherheit der Nullstelle *(Gauß'sche Fehlerfortpflanzung: sqrt((1/m * dn)^2 + (n/m^2 * dm)^2))*

<a name="errorbar-plot-info"/>

### INFO

**FOR MULTIPLE PLOTS IN ONE GRAPH:**
- use `list of strings` (with same length) instead of `string` for parameters with `list of strings` as an option
- You can use a `string` in ERRORBAR_PLOT_MODEL, it will apply to all plots
- You can use a `boolean` in ERRORBAR_PLOT_SHOW_MODELERROR, it will apply to all plots
- You can use a `string` in ERRORBAR_PLOT_X_COLUMN and ERRORBAR_PLOT_X_ERROR_COLUMN, the x values will be used for every set of y values

When *ERRORBAR_PLOT_MODEL* is not *'none'* or *'weighted_average'*, the x-/y-values and x-/y-error-values are used to create a linear fit with the [kafe2](https://github.com/PhiLFitters/kafe2) library. The advantage of kafe2 compared to excel or scipy is that the errors in x- and y-axes are used to calculate the increase and also the error of the increase. The parameters of the fit and also their errors will be logged in the console.

calculation of weighted average *(ERRORBAR_PLOT_MODEL)*:

![equation](https://latex.codecogs.com/png.image?\dpi{110}\bg{white}&space;\bar{y}&space;=&space;\frac{\sum&space;\frac{y_i}{u_{y_i}^2}}{\sum&space;\frac{1}{u_{y_i}^2}}) 

calculation of weighted average error *(ERRORBAR_PLOT_MODEL)*:

![equation](https://latex.codecogs.com/png.image?\dpi{110}\bg{white}&space;u_{\bar{y}}&space;=&space;\frac{1}{\sqrt{\sum&space;\frac{1}{u_{y_i}^2}}}) 


If you input more than 8 y-value column names, the plot colors will not be unique anymore.

### HINT FOR USAGE

Set ERRORBAR_PLOT_MAX_XTICKS='auto'/ERRORBAR_PLOT_MIN_XTICKS='auto' and ERRORBAR_PLOT_XTICKS_NUMBER='auto' because normally, this will work pretty well for the x-ticks and only if this is not good, change it.

Set ERRORBAR_PLOT_EXTRA_LOG=True because some more logs do not hurt and you will always have all the information.

### example plot

<p align="left">
  <img src="./images/plot_E5_UI.png" width="400" title="multiple linear/none plots example" alt="multiple linear/none plots example">
</p>

<details><summary>parameters</summary>

``` // opening
RAW_DATA_PATH = "data/Grundpraktikum/E5_UI.csv"
ERRORBAR_PLOT_PATH = "data/graphics/plot_E5_UI.png"
ERRORBAR_PLOT_X_COLUMN = ["I_EoK", "I_EmK", "I_ZoK", "I_ZmK"]
ERRORBAR_PLOT_X_ERROR_COLUMN = ["u_I_EoK", "u_I_EmK", "u_I_ZoK", "u_I_ZmK"]
ERRORBAR_PLOT_Y_COLUMN = ["U_EoK", "U_EmK", "U_ZoK", "U_ZmK"]
ERRORBAR_PLOT_Y_ERROR_COLUMN = ["u_U_EoK", "u_U_EmK", "u_U_ZoK", "u_U_ZmK"]
ERRORBAR_PLOT_TITLE = ""
ERRORBAR_PLOT_XLABEL = r"Stromstärke I in mA"
ERRORBAR_PLOT_YLABEL = r"Spannung U in V"
ERRORBAR_PLOT_XTICKS_NUMBER = 11
ERRORBAR_PLOT_MIN_XTICKS = 0
ERRORBAR_PLOT_MAX_XTICKS = 125
ERRORBAR_PLOT_PLOTLABELS = ["EWG ohne Kondensator", "EWG mit Kondensator", "ZWG ohne Kondensator", "ZWG mit Kondensator"]
ERRORBAR_PLOT_MODEL = ["linear", "none", "linear", "none"]
ERRORBAR_PLOT_SHOW_MODELERROR = False
ERRORBAR_PLOT_EXTRA_LOG = True
```
</details>

### additional examples

[click me](plotting_examples.md)

### command

```
python IMP_utils_py/cli.py --mode=errorbar-plot --gin_file=IMP_utils_py/config/plotting.gin
```

---

<a name="residual-plot"/>

## residual plot

### path parameters

- RAW_DATA_PATH: location of the csv/excel file with the data
  - `string` e.g. "raw_data.csv" or "raw_data.xlsx"

- RESIDUAL_PLOT_PATH: location for the png of the plot
  - `string` e.g. "plot.png"

### column name parameters

- ERRORBAR_PLOT_X_COLUMN: column name of column with x values
  - `string` e.g. "L"

- ERRORBAR_PLOT_X_ERROR_COLUMN: column name of column with errors of x values
  - `string` e.g. "u_L"
  - **NOTE:** use an empty string "" to provide no error column for the x-values

- ERRORBAR_PLOT_Y_COLUMN: 
  - column name of column with y values
    - `string` e.g. "f"

- ERRORBAR_PLOT_Y_ERROR_COLUMN:
  - column name of column with errors of y values
    - `string` e.g. "u_f"
  - **NOTE:** use an empty string "" to provide no error column for the y-values

### plot legend parameters

- ERRORBAR_PLOT_TITLE: title 
  - `string` e.g. "f(L)-Diagramm"
  - **NOTE:** use an empty string "" if there shall be no title for this plot

- ERRORBAR_PLOT_XLABEL: label of x axes
  - `string` e.g. "Länge L in m"
  - **NOTE:** use an empty string "" if there shall be no label for this axes

- ERRORBAR_PLOT_YLABEL: label of y axes
  - `string` e.g. "Frequenz f in Hz"
  - **NOTE:** use an empty string "" if there shall be no label for this axes

- ERRORBAR_PLOT_XTICKS_NUMBER: number of ticks on x axes *(has sometimes to be adjusted a bit for a better laylout)*
  - `string` if ERRORBAR_PLOT_XTICKS_NUMBER='auto', the optimal number of x-ticks will be calculated
  - `integer`

- ERRORBAR_PLOT_MIN_XTICKS: min value of ticks on x axes
  - `string` if ERRORBAR_PLOT_MIN_XTICKS='auto', the min tick will be the rounded down min x value from the data
  - `float`/`integer` e.g. 125 or 0.65

- ERRORBAR_PLOT_MAX_XTICKS: max value of ticks on x axes
  - `string` if ERRORBAR_PLOT_MAX_XTICKS='auto', the max tick will be the rounded up max x value from the data
  - `float`/`integer` e.g. 125 or 0.65

### function parameter

- ERRORBAR_PLOT_MODEL: choose the model for the linear fit
  - `string`
  - 'linear' *(y = m\*x + n)* / 'linear_zero' *(y = m\*x)* / 'constant' *(y = n)* / 'weighted_average' *(y = w_avg)*

### INFO

The residual plot represents the residuals *(actual_y_value − predicted_y_value)* of the linear fit-function mentioned in [errorbar-plot](#errorbar-plot-info).

You can only use one set of y-values and not multiple like in errorbar-plot.

### HINT FOR USAGE

Set ERRORBAR_PLOT_MAX_XTICKS='auto'/ERRORBAR_PLOT_MIN_XTICKS='auto' and ERRORBAR_PLOT_XTICKS_NUMBER='auto' because normally, this will work pretty well for the x-ticks and only if this is not good, change it.

### example plot

<p align="left">
  <img src="./images/plot_O6_bhg_residual.png" width="400" title="residual plot example" alt="residual plot example">
</p>

<details><summary>parameters</summary>

``` // opening
RAW_DATA_PATH = "data/Grundpraktikum/O6_bhg.csv"
RESIDUAL_PLOT_PATH = "data/graphics/plot_O6_bhg_residual.png"
ERRORBAR_PLOT_X_COLUMN = 'k'
ERRORBAR_PLOT_X_ERROR_COLUMN = ""
ERRORBAR_PLOT_Y_COLUMN = "y"
ERRORBAR_PLOT_Y_ERROR_COLUMN = "uy"
ERRORBAR_PLOT_TITLE = ""
ERRORBAR_PLOT_XLABEL = "k"
ERRORBAR_PLOT_YLABEL = "$r_k^2$ in $mm^2$"
ERRORBAR_PLOT_XTICKS_NUMBER = "auto"
ERRORBAR_PLOT_MIN_XTICKS = 0
ERRORBAR_PLOT_MAX_XTICKS = "auto"
ERRORBAR_PLOT_MODEL = "linear"
```
</details>

### command

```
python IMP_utils_py/cli.py --mode=residual-plot --gin_file=IMP_utils_py/config/plotting.gin
```

