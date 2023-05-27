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
def constant_model(x, a=1.0):
    """ y = a """
    return a

def linear_zero_model(x, a=1.0):
    """ y = a * x """
    return a*x

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
def errorbar_plot(data_path: str, graphic_path: str, x_column: Union[str, list], x_error_column: Union[str, list], y_column: Union[str, list], y_plot_label: Union[str, list], y_error_column: Union[str, list], title: str, x_label: str, y_label: str, x_ticks_number: int, model_type: Union[str, list]):
    """
    @params (str or list[str]):
        x_column: column name for x values
        x_error_column: column name for x value errors
        y_column: column name for y values
        y_plot_label: label for y-plot
        y_error_column: column name for y value errors
        model_type: 'linear' (y = m*x + n) / 'linear_zero' (y = m*x) / 'constant' (y = n) / 'none' (no model will be shown)

    @output:
        plot saved in graphic_path and errors in console

    @Note: max 5 y-value sets
    """
    data = read_data(data_path)

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

    # check if x_ticks_number >= 0
    if x_ticks_number < 0:
        raise ValueError(f"x_ticks_number has to be greater 0 or 0 for no x-axes ticks (found: {x_ticks_number} < 0)")

    if type(x_column) == str:
        x_column = [x_column]
    if type(x_error_column) == str:
        x_error_column = [x_error_column]

    # max value on x-axes
    max_length = 0
    for x_col in x_column:
        x = data[x_col]
        max_length_x = int(np.ceil(max(x)*10))/10
        if max_length_x > max_length:
            max_length = max_length_x

    # if 1 x-value and multiple y-values
    if len(x_column) == len(x_error_column) == 1 and len(y_column) > 1:
        x_column = x_column * len(y_column)
        x_error_column = x_error_column * len(y_column)
    else:
        # check length of x and y columns
        if not (len(x_column) == len(x_error_column) == len(y_column)):
            raise ValueError(f"Number of y_columns ({len(y_column)}), number of x_column ({len(x_column)}), or number of x_error_column ({len(x_error_column)}) do not match")
        
    # model_type to list
    if type(model_type) == str:
        model_type = [model_type]*len(y_column)
    else:
        # check length of show_linear_fit list and y columns
        if not (len(model_type) == len(y_column)):
            raise ValueError(f"Number of y_columns ({len(y_column)}) and number of model_type ({len(model_type)}) does not match")
    

    # replace empty strings with None in y_plot_label
    y_plot_label = [None if elem == "" else elem for elem in y_plot_label]
    
    fig = plt.figure()
    ax = fig.add_subplot()

    # colors for y-value fits
    colors = ["steelblue", "lightgreen", "lightcoral", "plum", "paleturquoise"]
    errorbar_colors = ['blue', 'green', 'red', 'magenta', 'cyan']

    for y_idx in range(len(y_column)):
        data.sort_values(by=[x_column[y_idx]])

        x = data[x_column[y_idx]]
        if x_error_column[y_idx] != "":
            dx = data[x_error_column[y_idx]]
        else:
            dx = None

        y = data[y_column[y_idx]]
        if y_error_column[y_idx] != "":
            dy = data[y_error_column[y_idx]]
        else:
            dy = None

        # select model based on model_type
        if model_type[y_idx] == "linear_zero":
            model = linear_zero_model
            logger.debug(f"selected linear_zero model ({y_column[y_idx]})")
        elif model_type[y_idx] == "linear":
            model = linear_model
            logger.debug(f"selected linear model ({y_column[y_idx]})")
        elif model_type[y_idx] == "constant":
            model = constant_model
            logger.debug(f"selected constant model ({y_column[y_idx]})")
        elif model_type[y_idx] == "none":
            model = None
            logger.debug(f"no model ({y_column[y_idx]})")
        else:
            raise ValueError(f"Model '{model_type[y_idx]}' ist not supported -> choose 'linear_zero', 'linear', 'constant', or 'none'")

        # if a model was selected
        if model is not None:
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
            if model_type[y_idx] in ("linear", "linear_zero"):
                m = model_params[0]
                dm = model_params_error[0]
                logger.info(f"Steigung der Gerade ({y_column[y_idx]}): {m}")
                logger.info(f"Unsicherheit der Steigung ({y_column[y_idx]}): {dm}")
                if model_type[y_idx] == "linear":
                    n = model_params[1]
                    dn = model_params_error[1]
                    logger.info(f"y-Achsenschnitt der Gerade ({y_column[y_idx]}): {n}")
                    logger.info(f"Unsicherheit des y-Achsenschnitt ({y_column[y_idx]}): {dn}")
            elif model_type[y_idx] == "constant":
                n = model_params[0]
                dn = model_params_error[0]
                logger.info(f"y-Achsenschnitt der Gerade ({y_column[y_idx]}): {n}")
                logger.info(f"Unsicherheit des y-Achsenschnitt ({y_column[y_idx]}): {dn}")

            # add graphs to plot
            x_intervall = np.linspace(0, max_length, 1000)
            if model_type[y_idx] == "constant":
                ax.plot(x_intervall, [n]*len(x_intervall), '--', color=colors[y_idx%len(colors)])
                logger.debug(f"added constant fit ({y_plot_label[y_idx]})")
            elif model_type[y_idx] == "linear_zero":
                ax.plot(x_intervall, m*x_intervall, '--', color=colors[y_idx%len(colors)])
                logger.debug(f"added linear_zero fit ({y_plot_label[y_idx]})")
            elif model_type[y_idx] == "linear":
                # not below zero fit line if decreasing
                if m<0:
                    x_intervall = np.linspace(0, min(max_length, -n/m), 1000)
                ax.plot(x_intervall, m*x_intervall+n, '--', color=colors[y_idx%len(colors)])
                logger.debug(f"added linear fit ({y_plot_label[y_idx]})")

        else:
            logger.info(f"Fits are deactivated ({y_column[y_idx]})")

        plt.errorbar(x, y, yerr=dy, xerr=dx, linestyle='None', label=y_plot_label[y_idx], marker='.', elinewidth=0.5, capsize=3, color=errorbar_colors[y_idx%len(errorbar_colors)])

    # legend settings
    ax.set_xticks(np.linspace(0, max_length, x_ticks_number))
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if not all(v is None for v in y_plot_label):
        ax.legend()

    # if y-axes values are long numbers, the y-label is cut off. Has to be tested if always best solution for this.
    fig.subplots_adjust(left=0.15)

    fig.savefig(graphic_path)
    logger.info("plot saved")

@gin.configurable
def residual_plot(data_path: str, graphic_path: str, x_column: str, x_error_column: str, y_column: str, y_error_column: str, title: str, x_label: str, y_label: str, x_ticks_number: int, model_type: str):
    """
    @params:
        x_column: column name for x values
        x_error_column: column name for x value errors
        y_column: column name for y values
        y_error_column: column name for y value errors
        model_type: 'linear' (y = m*x + n) / 'linear_zero' (y = m*x) / 'constant' (y = n)

    @output:
        plot saved in graphic_path
    """

    if model_type == "linear_zero":
        model = linear_zero_model
        logger.debug("selected linear_zero model")
    elif model_type == "linear":
        model = linear_model
        logger.debug("selected linear model")
    elif model_type == "constant":
        model = constant_model
        logger.debug("selected constant model")
    else:
        raise ValueError(f"Model '{model_type}' ist not supported -> choose 'linear_zero', 'linear', or 'constant'")


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
    if model_type == "linear":
        n = model_params[1]

    # calculate residuals
    if model_type == "linear_zero":
        residuals = [y.iloc[idx]-linear_zero_model(x.iloc[idx], m) for idx in range(len(x))]
    elif model_type == "linear":
        residuals = [y.iloc[idx]-linear_model(x.iloc[idx], m, n) for idx in range(len(x))]
    elif model_type == "constant":
        residuals = [y.iloc[idx]-constant_model(x.iloc[idx], m) for idx in range(len(x))]

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
