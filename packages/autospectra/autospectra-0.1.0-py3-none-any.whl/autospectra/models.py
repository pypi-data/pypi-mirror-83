from autospectra.preprocessing import test_module
import optuna
import tensorflow as tf
import sys


def test_module():
    print(
        f'Using optuna {optuna.__version__} and tensorflow {tf.__version__} for modelling.'
    )

    pass
