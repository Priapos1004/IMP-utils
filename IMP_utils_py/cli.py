import gin
from absl import app, flags

from IMP_utils_py.physics import (errorbar_l, errorbar_phi, eval_raw_data,
                                  hist_gauss, linear_plot, points_plot,
                                  residual_plot, time_stop)

flags.DEFINE_enum(
    "mode",
    "test",
    [
        "test",
        "time-stop",
        "eval-raw-data",
        "hist-gauss",
        "errorbar-phi",
        "errorbar-l",
        "linear-plot",
        "points-plot",
        "residual-plot",
    ],
    "just ask Samuel",
)
flags.DEFINE_multi_string("gin_file", None, "List of paths to the config files.")
flags.DEFINE_multi_string(
    "gin_param", None, "Newline separated list of Gin parameter bindings."
)
FLAGS = flags.FLAGS


def main(*unused_argv):
    gin.parse_config_files_and_bindings(FLAGS.gin_file, FLAGS.gin_param)
    if FLAGS.mode == "test":
        pass
    elif FLAGS.mode == "time-stop":
        time_stop()
    elif FLAGS.mode == "eval-raw-data":
        eval_raw_data() 
    elif FLAGS.mode == "hist-gauss":
        hist_gauss() 
    elif FLAGS.mode == "errorbar-phi":
        errorbar_phi() 
    elif FLAGS.mode == "errorbar-l":
        errorbar_l() 
    elif FLAGS.mode == "linear-plot":
        linear_plot()
    elif FLAGS.mode == "points-plot":
        points_plot()
    elif FLAGS.mode == "residual-plot":
        residual_plot()

def console_entry_point():
    """From pip installed script."""
    app.run(main)


if __name__ == "__main__":
    console_entry_point()
