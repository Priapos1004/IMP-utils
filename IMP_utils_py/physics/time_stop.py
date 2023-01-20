"""
Instructions for "time_stop" function:

1. check that you have "pandas" and "numpy" installed
(e.g. you can use "pip install pandas" and "pip install numpy" in the terminal)

2. run the code (e.g. in the terminal with "python <file path>")

3. you can start the time measurement with the "space" key and every time you click it, the time is taken

4. to end the measurement press "a"

5. the program will automatically create two files "raw_data.csv" and "evaluation_data.csv" with the data and its evaluation

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
import tty

import numpy as np  # pip install numpy
import pandas as pd  # pip install pandas

from IMP_utils_py.config.logging import setup_logger


### logging setup
logger = setup_logger()

### periods calculation functions
def calc_periods(data: list):
    periods = [data[i]-data[i-1] if i!=0 else data[i] for i in range(len(data))]
    return periods

def calc_half_periods(data: list):
    periods = []
    for i in range(1, len(data), 2):
        periods.append(data[i])
    periods = calc_periods(periods)
    periods += [None]*(len(data)-len(periods))
    return periods

def calc_half_periods_v2(data: list):
    periods = []
    for i in range(1, len(data)):
        if i==1:
            periods.append(data[i])
        else:
            periods.append(data[i]-data[i-2])
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

def eval(data: pd.Series) -> tuple[int, float, float, float]:
    """
    returns tuple (number of values, average, std, std of average)
    """
    data = list(data.dropna()) # clear list from None values
    avg_data = np.mean(data)
    std_data = std(data, avg_data)
    std_avg_data = std_data/np.sqrt(len(data))
    return len(data), avg_data, std_data, std_avg_data

### main program
def time_stop() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    returns raw_data and evaluation_data dataframes (also saves them as csv)
    """
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
        if key==97: #  press "a" to stop
            logger.info("... finished \n")
            break

    df_raw_data = pd.DataFrame({"periods": calc_periods(times), "half periods": calc_half_periods(times), "half periods v2": calc_half_periods_v2(times)})
    
    eval_p = eval(df_raw_data["periods"])
    eval_hp = eval(df_raw_data["half periods"])
    eval_hp_v2 = eval(df_raw_data["half periods v2"])
    eval_list = [eval_p, eval_hp, eval_hp_v2]

    df_evaluation = pd.DataFrame({"counting": ["periods", "half periods", "half periods v2"]})
    df_evaluation["Messwerte Anzahl"] = [ev[0] for ev in eval_list]
    df_evaluation["Mittelwert"] = [ev[1] for ev in eval_list]
    df_evaluation["Standardabweichung"] = [ev[2] for ev in eval_list]
    df_evaluation["Vertrauensbereich"] = [ev[3] for ev in eval_list]

    df_raw_data.to_csv("raw_data.csv")
    df_evaluation.to_csv("evaluation_data.csv")

    logger.info("data files are created and saved")

    return df_raw_data, df_evaluation

if __name__ == "__main__":
    time_stop()
