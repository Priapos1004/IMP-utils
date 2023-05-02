# plotting functions

Run the following commands in the terminal (current working directory: `IMP-utils` folder). You can change the available parameter of the functions in `IMP_utils_py/config/plotting.gin`.

## table of content

- [linear-plot](#linear-plot): linear plot (with and without intercept zero)

- [residual-plot](#residual-plot): residual plot for linear function (with and without intercept zero)

<a name="linear-plot"/>

## linear plot

### path parameters

- RAW_DATA_PATH: location of the csv file with the data

- LINEAR_PLOT_PATH: location for the png of the plot

### column name parameters

- LINEAR_PLOT_X_COLUMN: column name of column with x values

- LINEAR_PLOT_X_ERROR_COLUMN: column name of column with errors of x values

- LINEAR_PLOT_Y_COLUMN: column name of column with y values

- LINEAR_PLOT_Y_ERROR_COLUMN: column name of column with errors of y values

### plot legend parameters

- LINEAR_PLOT_TITLE: title 

- LINEAR_PLOT_XLABEL: label of x axes

- LINEAR_PLOT_YLABEL: label of y axes

- LINEAR_PLOT_XTICKS_NUMBER: number of ticks on x axes *(has sometimes to be adjusted a bit for a better laylout)*

### function parameter

- LINEAR_PLOT_INTERCEPT_ZERO: True (linear model with intercept zero - y=m\*x) or False (linear model- y=m\*x+n)

<a name="linear-plot-info"/>
### INFO

The x-/y-values and x-/y-error-values are used to create a linear fit with the [kafe2](https://github.com/PhiLFitters/kafe2) library. The parameters of the fit and also their errors will be logged in the console.

### example plot

<p align="left">
  <img src="./images/plot_O6_bhg.png" width="400" title="linear plot example" alt="linear plot example">
</p>

### command

```
python IMP_utils_py/cli.py --mode=linear-plot --gin_file=IMP_utils_py/config/plotting.gin
```

<a name="residual-plot"/>

## residual plot

### path parameters

- RAW_DATA_PATH: location of the csv file with the data

- RESIDUAL_PLOT_PATH: location for the png of the plot

### column name parameters

- LINEAR_PLOT_X_COLUMN: column name of column with x values

- LINEAR_PLOT_X_ERROR_COLUMN: column name of column with errors of x values

- LINEAR_PLOT_Y_COLUMN: column name of column with y values

- LINEAR_PLOT_Y_ERROR_COLUMN: column name of column with errors of y values

### plot legend parameters

- LINEAR_PLOT_TITLE: title 

- LINEAR_PLOT_XLABEL: label of x axes

- LINEAR_PLOT_YLABEL: label of y axes

- LINEAR_PLOT_XTICKS_NUMBER: number of ticks on x axes *(has sometimes to be adjusted a bit for a better laylout)*

### function parameter

- LINEAR_PLOT_INTERCEPT_ZERO: True (linear model with intercept zero - y=m\*x) or False (linear model- y=m\*x+n)

### INFO

The residual plot represents the residuals *(actual_y_value − predicted_y_value)* of the linear function mentioned in [linear-plot](#linear-plot-info).

### example plot

<p align="left">
  <img src="./images/plot_O6_bhg_residual.png" width="400" title="residual plot example" alt="residual plot example">
</p>

### command

```
python IMP_utils_py/cli.py --mode=residual-plot --gin_file=IMP_utils_py/config/plotting.gin
```

