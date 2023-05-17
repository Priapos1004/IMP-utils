# plotting functions

Run the following commands in the terminal (current working directory: `IMP-utils` folder). You can change the available parameter of the functions in `IMP_utils_py/config/plotting.gin`. The path parameters in `plotting.gin` have to be relative to the `IMP-utils` folder.

## table of content

- [linear-plot](#linear-plot): linear plot (with and without intercept zero)

- [residual-plot](#residual-plot): residual plot for linear function (with and without intercept zero)

<a name="linear-plot"/>

## linear plot

### path parameters

- RAW_DATA_PATH: location of the csv/excel file with the data
  - `string` e.g. "raw_data.csv" or "raw_data.xlsx"

- LINEAR_PLOT_PATH: location for the png of the plot
  - `string` e.g. "plot.png"

### column name parameters

- LINEAR_PLOT_X_COLUMN: column name of column with x values
  - `string` e.g. "L"

- LINEAR_PLOT_X_ERROR_COLUMN: column name of column with errors of x values
  - `string` e.g. "u_L"
  - **NOTE:** use an empty string "" to provide no error column for the x-values

- LINEAR_PLOT_Y_COLUMN: 
  - column name of column with y values
    - `string` e.g. "f"
  - list of column names with y values *(for multiple linear plots in one graph)*
    - `list of strings` e.g. ["f1", "f2", "f3"]

- LINEAR_PLOT_Y_ERROR_COLUMN:
  - column name of column with errors of y values
    - `string` e.g. "u_f"
  - list of column names of columns with errors of y values *(for multiple linear plots in one graph)*
    - `list of strings` e.g. ["u_f1", "u_f2", "u_f3"]
  - **NOTE:** use an empty string "" to provide no error column for the y-values

### plot legend parameters

- LINEAR_PLOT_PLOTLABELS:
  - label for plot in legend
    - `string` e.g. "Frequenz f"
  - list of labels for plots in legend
    - `list of strings` e.g. ["Frequenz f1", "Frequenz f2", "Frequenz f3"]
  - **NOTE:** use an empty string "" if there shall be no label for this plot

- LINEAR_PLOT_TITLE: title 
  - `string` e.g. "f(L)-Diagramm"
  - **NOTE:** use an empty string "" if there shall be no title for this plot

- LINEAR_PLOT_XLABEL: label of x axes
  - `string` e.g. "Länge L in m"
  - **NOTE:** use an empty string "" if there shall be no label for this axes

- LINEAR_PLOT_YLABEL: label of y axes
  - `string` e.g. "Frequenz f in Hz"
  - **NOTE:** use an empty string "" if there shall be no label for this axes

- LINEAR_PLOT_XTICKS_NUMBER: number of ticks on x axes *(has sometimes to be adjusted a bit for a better laylout)*
  - `integer`

### function parameter

- LINEAR_PLOT_INTERCEPT_ZERO: True (linear model with intercept zero - y=m\*x) or False (linear model - y=m\*x+n)
  - `boolean`

<a name="linear-plot-info"/>

### INFO

The x-/y-values and x-/y-error-values are used to create a linear fit with the [kafe2](https://github.com/PhiLFitters/kafe2) library. The advantage of kafe2 compared to matplotlib or scipy is that the errors in x- and y-axes are used to calculate the increase and also the error of the increase. The parameters of the fit and also their errors will be logged in the console.

If you input more than 5 y-value column names, the plot colors will not be unique anymore.

### linear plot example

<p align="left">
  <img src="./images/plot_O6_bhg.png" width="400" title="linear plot example" alt="linear plot example">
</p>

### multiple linear plots example

<p align="left">
  <img src="./images/plot_M12_kg.png" width="400" title="multiple linear plots example" alt="multiple linear plots example">
</p>

### command

```
python IMP_utils_py/cli.py --mode=linear-plot --gin_file=IMP_utils_py/config/plotting.gin
```

---

<a name="residual-plot"/>

## residual plot

### path parameters

- RAW_DATA_PATH: location of the csv/excel file with the data
  - `string` e.g. "raw_data.csv" or "raw_data.xlsx"

- LINEAR_PLOT_PATH: location for the png of the plot
  - `string` e.g. "plot.png"

### column name parameters

- LINEAR_PLOT_X_COLUMN: column name of column with x values
  - `string` e.g. "L"

- LINEAR_PLOT_X_ERROR_COLUMN: column name of column with errors of x values
  - `string` e.g. "u_L"
  - **NOTE:** use an empty string "" to provide no error column for the x-values

- LINEAR_PLOT_Y_COLUMN: 
  - column name of column with y values
    - `string` e.g. "f"

- LINEAR_PLOT_Y_ERROR_COLUMN:
  - column name of column with errors of y values
    - `string` e.g. "u_f"
  - **NOTE:** use an empty string "" to provide no error column for the y-values

### plot legend parameters

- LINEAR_PLOT_TITLE: title 
  - `string` e.g. "f(L)-Diagramm"
  - **NOTE:** use an empty string "" if there shall be no title for this plot

- LINEAR_PLOT_XLABEL: label of x axes
  - `string` e.g. "Länge L in m"
  - **NOTE:** use an empty string "" if there shall be no label for this axes

- LINEAR_PLOT_YLABEL: label of y axes
  - `string` e.g. "Frequenz f in Hz"
  - **NOTE:** use an empty string "" if there shall be no label for this axes

- LINEAR_PLOT_XTICKS_NUMBER: number of ticks on x axes *(has sometimes to be adjusted a bit for a better laylout)*
  -   `integer`

### function parameter

- LINEAR_PLOT_INTERCEPT_ZERO: True (linear model with intercept zero - y=m\*x) or False (linear model - y=m\*x+n)
  -   `boolean`

### INFO

The residual plot represents the residuals *(actual_y_value − predicted_y_value)* of the linear function mentioned in [linear-plot](#linear-plot-info).

You can only use one set of y-values and not multiple like in linear-plot.

### example plot

<p align="left">
  <img src="./images/plot_O6_bhg_residual.png" width="400" title="residual plot example" alt="residual plot example">
</p>

### command

```
python IMP_utils_py/cli.py --mode=residual-plot --gin_file=IMP_utils_py/config/plotting.gin
```

