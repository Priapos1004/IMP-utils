import math
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

def get_best_divider(number: float, possible_divider: list = list(range(5,13))) -> int:
    """
    get best divider of a number out of a given list of possible divider

    scoring:
        - first by length: shorter is better
        - second by ranking based on last_digit: 
            - rank/last digit: 0-0, 1-5, 2-2, 3-1, 4-4, 5-6, 6-8, 7-3, 8-7, 9-9
        - third by divider: higher value with same length and ranking is better

    example:
        - number = 100.8 and possible_divider = list(range(5,12)) -> best divider 10
            - tick_number 5, one_tick 25.2, length 3, last_digit 2, ranking 2
            - tick_number 6, one_tick 20.16, length 4, last_digit 6, ranking 5
            - tick_number 7, one_tick 16.8, length 3, last_digit 8, ranking 6
            - tick_number 8, one_tick 14.4, length 3, last_digit 4, ranking 4
            - tick_number 9, one_tick 12.6, length 3, last_digit 6, ranking 5
            - tick_number 10, one_tick 11.2, length 3, last_digit 2, ranking 2
            - tick_number 11, one_tick 10.08, length 4, last_digit 8, ranking 6
    """
    auto_ticks = possible_divider
    # tick number
    best_tick_number = -1
    # rank/last digit: 0-0, 1-5, 2-2, 3-1, 4-4, 5-6, 6-8, 7-3, 8-7, 9-9
    best_tick_ranking = 10
    ranking_mapping = {0: 0, 5: 1, 2: 2, 1: 3, 4: 4, 6: 5, 8: 6, 3: 7, 7: 8, 9: 9}
    # length of string without special characters
    best_tick_length = -1
    for tick in auto_ticks:
        one_tick = number/(tick-1)
        tick_length = len(str(one_tick).replace(".",""))
        last_digit = int(str(one_tick)[-1])
        ranking = ranking_mapping[last_digit]
        logger.debug(f"tick_number {tick}, one_tick {one_tick}, length {tick_length}, last_digit {last_digit}, ranking {ranking}")
        if tick_length<best_tick_length or best_tick_length==-1:
            best_tick_number = tick
            best_tick_length = tick_length
            best_tick_ranking = ranking
        elif tick_length == best_tick_length:
            if best_tick_ranking > ranking:
                best_tick_number = tick
                best_tick_length = tick_length
                best_tick_ranking = ranking
            elif best_tick_ranking == ranking:
                if best_tick_number < tick:
                    best_tick_number = tick
                    best_tick_length = tick_length
                    best_tick_ranking = ranking
    return best_tick_number

def signif(x, digits=2):
    """ function to round up number to first <digits>. significant figures """
    if x == 0 or not math.isfinite(x):
        return x
    digits -= math.ceil(math.log10(abs(x)))
    return np.ceil(x*10**digits)/10**digits

### command functions
@gin.configurable
def errorbar_plot(data_path: str, graphic_path: str, x_column: Union[str, list], x_error_column: Union[str, list], y_column: Union[str, list], y_plot_label: Union[str, list], y_error_column: Union[str, list], title: str, x_label: str, y_label: str, x_ticks_number: Union[str, int], max_x_ticks: Union[str, float, int], model_type: Union[str, list], extra_log: bool):
    """
    @params (str or list[str]):
        x_column: column name for x values
        x_error_column: column name for x value errors
        y_column: column name for y values
        y_plot_label: label for y-plot
        y_error_column: column name for y value errors
        model_type: 'linear' (y = m*x + n) / 'linear_zero' (y = m*x) / 'constant' (y = n) / 'none' (no model will be shown)
        max_x_ticks: 'auto' or float/int

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

    if type(x_column) == str:
        x_column = [x_column]
    if type(x_error_column) == str:
        x_error_column = [x_error_column]

    # max value on x-axes
    if max_x_ticks == "auto":
        max_length = max([signif(max(data[x_col])) for x_col in x_column])
        logger.info(f"auto max_length = {max_length}")
    elif type(max_x_ticks) in (float, int):
        # check if max_x_ticks > 0
        if max_x_ticks <= 0:
            raise ValueError(f"max_x_ticks has to be greater 0, but {max_x_ticks} <= 0")
        max_value = max([max(data[x_col]) for x_col in x_column])
        if max_x_ticks < max_value:
            logger.warning(f"max_x_ticks is smaller than the largest value of the x data ({max_x_ticks} < {max_value})")
        max_length = max_x_ticks
    else:
        raise ValueError(f"max_x_ticks has to be 'auto' or float/int greater 0 (found: {max_x_ticks} with type {type(max_x_ticks)})")
    
    # number of ticks on x-axes
    if x_ticks_number == "auto":
        x_ticks_number = get_best_divider(max_length)
        logger.info(f"auto x_ticks_number = {x_ticks_number}")
    elif type(x_ticks_number) == int:
        # check if x_ticks_number >= 0
        if x_ticks_number < 0:
            raise ValueError(f"x_ticks_number has to be greater 0 or 0 for no x-axes ticks (found: {x_ticks_number} < 0)")
    else:
        raise ValueError(f"x_ticks_number has to be 'auto' or int greater 0 (found: {x_ticks_number} with type {type(x_ticks_number)})")

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
                    if extra_log:
                        zero_point = -n/m
                        dzero_point = np.sqrt((1/m * dn)**2 + (n/m**2 * dm)**2)
                        logger.info(f"Nullstelle der Gerade  ({y_column[y_idx]}): {zero_point}")
                        logger.info(f"Unsicherheit der Nullstelle der Gerade  ({y_column[y_idx]}): {dzero_point}")
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
def residual_plot(data_path: str, graphic_path: str, x_column: str, x_error_column: str, y_column: str, y_error_column: str, title: str, x_label: str, y_label: str, x_ticks_number: Union[str, int], max_x_ticks: Union[str, float, int], model_type: str):
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
    if max_x_ticks == "auto":
        max_length = signif(max(x))
        logger.info(f"auto max_length = {max_length}")
    elif type(max_x_ticks) in (float, int):
        # check if max_x_ticks > 0
        if max_x_ticks <= 0:
            raise ValueError(f"max_x_ticks has to be greater 0, but {max_x_ticks} <= 0")
        max_length = max_x_ticks
    else:
        raise ValueError(f"max_x_ticks has to be 'auto' or float/int greater 0 (found: {max_x_ticks} with type {type(max_x_ticks)})")
    
    # number of ticks on x-axes
    if x_ticks_number == "auto":
        x_ticks_number = get_best_divider(max_length)
        logger.info(f"auto x_ticks_number = {x_ticks_number}")
    elif type(x_ticks_number) == int:
        # check if x_ticks_number >= 0
        if x_ticks_number < 0:
            raise ValueError(f"x_ticks_number has to be greater 0 or 0 for no x-axes ticks (found: {x_ticks_number} < 0)")
    else:
        raise ValueError(f"x_ticks_number has to be 'auto' or int greater 0 (found: {x_ticks_number} with type {type(x_ticks_number)})")

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
