from typing import Union

import gin
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from kafe2 import Fit, XYContainer

from IMP_utils_py.config.logging import setup_logger

### logging setup
logger = setup_logger()

### helper functions
def linear_zero_model(x, a=1.0):
    """ y = a * x """
    return a * x

def linear_model(x, a=1.0, b=0.0):
    """ y = a * x + b """
    return a*x+b

def read_data(data_path: str) -> pd.DataFrame:
    """ read data as pandas DataFrame from path """
    if data_path.split(".")[-1] == "csv":
        data = pd.read_csv(data_path, index_col=0)
    elif data_path.split(".")[-1] == "xlsx":
        data = pd.read_excel(data_path)
    else:
        raise ValueError(f"raw data path '{data_path}' file format is not supported -> use .csv or .xlsx")
    
    return data

### command functions
@gin.configurable
def linear_plot(data_path: str, graphic_path: str, x_column: str, x_error_column: str, y_column: Union[str, list], y_plot_label: Union[str, list], y_error_column: Union[str, list], title: str, x_label: str, y_label: str, x_ticks_number: int, intercept_zero: bool, show_linear_fit: bool):
    """
    @params:
        x_column: column name for x values
        x_error_column: column name for x value errors
        y_column: column name for y values or list of column names for y values
        y_plot_label: label for y-plot or list of labels for y-plots
        y_error_column: column name for y value errors or list of column names for y value errors
        intercept_zero: True (y = m*x) or False (y = m*x + n)
        show_linear_fit: if False, the linear fit will not be shown

    @output:
        plot saved in graphic_path and errors in console

    @Note: max 5 y-value sets
    """

    if intercept_zero:
        model = linear_zero_model
    else:
        model = linear_model

    data = read_data(data_path)
    data.sort_values(by=[x_column])

    x = data[x_column]
    if x_error_column != "":
        dx = data[x_error_column]
    else:
        dx = None

    # convert string input to list of string
    if type(y_column) == str:
        y_column = [y_column]
    if type(y_plot_label) == str:
        y_plot_label = [y_plot_label]
    if type(y_error_column) == str:
        y_error_column = [y_error_column]

    # check if lengths of y columns is correct
    if not (len(y_column) == len(y_error_column) == len(y_plot_label)):
        raise ValueError(f"Number of y_columns ({len(y_column)}), number of y_error_column ({len(y_error_column)}), or number of y_plot_label ({len(y_plot_label)}) do not match")
    elif len(y_column) > 5:
        logger.warning(f"Found more than 5 y-value sets ({len(y_column)} > 5) -> the plot colors will not be unique")

    # replace empty strings with None in y_plot_label
    y_plot_label = [None if elem == "" else elem for elem in y_plot_label]
    
    fig = plt.figure()
    ax = fig.add_subplot()

    # max value on x-axes
    max_length = int(np.ceil(max(x)*10))/10
    # colors for y-value fits
    colors = ["lightskyblue", "lightgreen", "lightcoral", "paleturquoise", "plum"]
    errorbar_colors = ['blue', 'green', 'red', 'cyan', 'magenta']

    for y_idx in range(len(y_column)):
        y = data[y_column[y_idx]]
        if y_error_column != "":
            dy = data[y_error_column[y_idx]]
        else:
            dy = None

        ### kafe2 calculation
        xy_data = XYContainer(x,y)
        if dx is not None:
            xy_data.add_error("x", dx)
        if dy is not None:
            xy_data.add_error("y", dy)

        my_fit = Fit(xy_data, model)
        my_fit.do_fit()
        model_params = my_fit.parameter_values
        model_params_error = my_fit.parameter_errors

        # fit values
        m = model_params[0]
        dm = model_params_error[0]
        if not intercept_zero:
            n = model_params[1]
            dn = model_params_error[1]

        logger.info(f"Steigung der Gerade ({y_column[y_idx]}): {m}")
        logger.info(f"Unsicherheit der Steigung ({y_column[y_idx]}): {dm}")
        if not intercept_zero:
            logger.info(f"y-Achsenschnitt der Gerade ({y_column[y_idx]}): {n}")
            logger.info(f"Unsicherheit des y-Achsenschnitt ({y_column[y_idx]}): {dn}")

        # add graphs to plot
        if show_linear_fit:
            x_intervall = np.linspace(0, max_length, 1000)
            if intercept_zero:
                ax.plot(x_intervall, m*x_intervall, '--', label=y_plot_label[y_idx], color=colors[y_idx%len(colors)])
            else:
                ax.plot(x_intervall, m*x_intervall+n, '--', label=y_plot_label[y_idx], color=colors[y_idx%len(colors)])
        plt.errorbar(x, y, yerr=dy, xerr=dx, linestyle='None', marker='.', elinewidth=0.5, capsize=3, color=errorbar_colors[y_idx%len(errorbar_colors)])

    # legend settings
    ax.set_xticks(np.linspace(0, max_length, x_ticks_number))
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if not all(v is None for v in y_plot_label) and show_linear_fit:
        ax.legend()

    # if y-axes values are long numbers, the y-label is cut off. Has to be tested if always best solution for this.
    fig.subplots_adjust(left=0.15)

    fig.savefig(graphic_path)
    logger.info("plot saved")

@gin.configurable
def residual_plot(data_path: str, graphic_path: str, x_column: str, x_error_column: str, y_column: str, y_error_column: str, title: str, x_label: str, y_label: str, x_ticks_number: int, intercept_zero: bool):
    """
    @params:
        x_column: column name for x values
        x_error_column: column name for x value errors
        y_column: column name for y values
        y_error_column: column name for y value errors
        intercept_zero: True (y = m*x) or False (y = m*x + n)

    @output:
        plot saved in graphic_path
    """

    if intercept_zero:
        model = linear_zero_model
    else:
        model = linear_model

    data = read_data(data_path)
    data.sort_values(by=[x_column])

    x = data[x_column]
    y = data[y_column]

    if x_error_column != "":
        dx = data[x_error_column]
    else:
        dx = None
    if y_error_column != "":
        dy = data[y_error_column]
    else:
        dy = None

    # max value on x-axes
    max_length = int(np.ceil(max(x)*10))/10

    fig = plt.figure()
    ax = fig.add_subplot()

    ### kafe2 calculation
    xy_data = XYContainer(x,y)
    if dx is not None:
        xy_data.add_error("x", dx)
    if dy is not None:
        xy_data.add_error("y", dy)

    my_fit = Fit(xy_data, model)
    my_fit.do_fit()
    model_params = my_fit.parameter_values

    m = model_params[0]
    if not intercept_zero:
        n = model_params[1]

    # calculate residuals
    if intercept_zero:
        residuals = [y.iloc[idx]-linear_zero_model(x.iloc[idx], m) for idx in range(len(x))]
    else:
        residuals = [y.iloc[idx]-linear_model(x.iloc[idx], m, n) for idx in range(len(x))]

    # add graphs to plot
    plt.scatter(x, residuals, s=10)
    x_intervall = np.linspace(0, max_length, 1000)
    ax.plot(x_intervall, 0*x_intervall, '--k', linewidth=1)
    
    # legend settings
    ax.set_xticks(np.linspace(0, max_length, x_ticks_number))
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.subplots_adjust(left=0.15)

    fig.savefig(graphic_path)
    logger.info("plot saved")
