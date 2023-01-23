"""
Instructions for "time_stop" function:

1. you can start the time measurement with the "space" key and every time you click it, the time is taken

2. to end the measurement press "a", to pause the measurement press "p" and start it with "space" again

3. the program will automatically create two files "raw_data.csv" and "evaluation_data.csv" with the data and its evaluation

Instructions for "eval_raw_data" function:

- the raw data will be evaluated and as an evaluation file saved (old evaluation file will be overwritten)

INFO:
    the three counting types are (all will be shown in raw and evaluation data):

    - periods: every click means a new period
    - half periods: every second click means a period and the others are ignored
    - half periods v2: the periods will be 1+2, 2+3, 3+4, 4+5, ... (every time is used for two periods)

NOTE:
    - the program needs a moment to initialize and a message will appear when the program is ready for the key board input
    - python version 3.9 and higher
"""

import sys
import time

SYSTEM: str = ""
try:
    import tty  # MacOS
    SYSTEM = "MacOS"
except:
    import keyboard  # Windows
    SYSTEM = "Windows"

import gin
import numpy as np  # pip install numpy
import pandas as pd  # pip install pandas

from IMP_utils_py.config.logging import setup_logger

### logging setup
logger = setup_logger()

### periods calculation functions
def calc_half_periods(data: list):
    periods = [data[i]+data[i-1] for i in range(1, len(data), 2)]
    periods += [None]*(len(data)-len(periods))
    return periods

def calc_half_periods_v2(data: list):
    periods = [data[i]+data[i-1] for i in range(1, len(data))]
    periods += [None]*(len(data)-len(periods))
    return periods

### evaluation functions
def std(data: list, mean: float) -> float:
    """
    sigma = sqrt(sum(x_i - mean)^2/(N-1))
    """
    sum = 0
    for i in range(len(data)):
        sum += np.power((data[i]-mean),2)
    sigma = np.sqrt(sum/(len(data)-1))
    return sigma

def calc_metrics(data: pd.Series) -> tuple[int, float, float, float]:
    """
    returns tuple (number of values, average, std, std of average)
    """
    data = list(data.dropna()) # clear list from None values

    # special cases
    if not data:
        return 0, None, None, None
    elif len(data)==1:
        return 1, data[0], 0, 0

    avg_data = np.mean(data)
    std_data = std(data, avg_data)
    std_avg_data = std_data/np.sqrt(len(data))

    return len(data), avg_data, std_data, std_avg_data

def eval_df(df: pd.DataFrame) -> pd.DataFrame:
    columns_metrics = [calc_metrics(df[col]) for col in df.columns]

    df_evaluation = pd.DataFrame({"counting": df.columns})
    df_evaluation["Messwerte Anzahl"] = [ev[0] for ev in columns_metrics]
    df_evaluation["Mittelwert"] = [ev[1] for ev in columns_metrics]
    df_evaluation["Standardabweichung"] = [ev[2] for ev in columns_metrics]
    df_evaluation["Vertrauensbereich"] = [ev[3] for ev in columns_metrics]

    return df_evaluation

### keyboard input functions
def keyboard_input_MacOS() -> list[float]:
    tty.setcbreak(sys.stdin)  # needed for keyboard input

    times: list[float] = []
    start_time: float = 0
    start_press: bool = False # first "space" press happend

    logger.info("now ready for key board input \n")

    while True:
        key = ord(sys.stdin.read(1))
        if key==32: # press "space" to time
            if not start_press:
                logger.info("Time started...")
                start_time = time.time()
                start_press = True
            else:
                times.append(time.time()-start_time)
                logger.info(f"Round: {len(times)}")
                start_time = time.time()
        elif key==97: #  press "a" to stop
            logger.info("... finished \n")
            break

        elif key==112: #  press "p" to pause
            logger.info("paused")
            start_press = False

    return times

def keyboard_input_Windows() -> list[float]:
    times: list[float] = []
    start_time: float = 0
    start_press: bool = False # first "space" press happend

    logger.info("now ready for key board input \n")

    space_clicked = False
    a_clicked = False
    p_clicked = False

    while True:
        if keyboard.is_pressed("space") and not space_clicked: # press "space" to time
            if not start_press:
                logger.info("Time started...")
                start_time = time.time()
                start_press = True
            else:
                times.append(time.time()-start_time)
                logger.info(f"Round: {len(times)}")
                start_time = time.time()
            space_clicked = True

        elif keyboard.is_pressed("a") and not a_clicked: #  press "a" to stop
            logger.info("... finished \n")
            a_clicked = True
            break

        elif keyboard.is_pressed("p") and not p_clicked: # press "p" to pause
            logger.info("paused")
            start_press = False
            p_clicked = True

        elif not keyboard.is_pressed("space") and space_clicked:
            space_clicked=False
        elif not keyboard.is_pressed("a") and a_clicked:
            a_clicked=False
        elif not keyboard.is_pressed("p") and p_clicked:
            p_clicked=False

    return times


### main program
@gin.configurable
def time_stop(raw_data_path: str, evaluation_data_path: str):
    """
    returns raw_data and evaluation_data dataframes (also saves them as csv)
    """
    if SYSTEM == "Windows":
        times = keyboard_input_Windows()
    elif SYSTEM == "MacOS":
        times = keyboard_input_MacOS()
    else:
        raise ValueError(f"wrong input ('{SYSTEM}') for variable system -> needs to be 'Windows' or 'MacOS'")


    df_raw_data = pd.DataFrame({"periods": times, "half periods": calc_half_periods(times), "half periods v2": calc_half_periods_v2(times)})
    df_evaluation = eval_df(df_raw_data)

    df_raw_data.to_csv(raw_data_path)
    df_evaluation.to_csv(evaluation_data_path)

    logger.info("data files are created and saved")

### eval program
@gin.configurable
def eval_raw_data(raw_data_path: str, evaluation_data_path: str):
    logger.info("start reading raw data")
    df_raw_data = pd.read_csv(raw_data_path, index_col=0)
    df_evaluation = eval_df(df_raw_data)
    df_evaluation.to_csv(evaluation_data_path)
    logger.info("evaluation file created and saved")
