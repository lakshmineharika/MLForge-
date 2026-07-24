import pytest
import tensorflow as tf

import MLForge
from MLForge import tracking
from MLForge.exceptions import INVALID_PARAMETER_VALUE, ErrorCode, MLForgeException
from MLForge.tracking.fluent import start_run
from MLForge.tracking.metric_value_conversion_utils import convert_metric_value_to_float_if_possible


def test_reraised_value_errors():
    multi_item_tf_tensor = tf.random.uniform([2, 2], dtype=tf.float32)

    with pytest.raises(MLForgeException, match=r"Failed to convert metric value to float") as e:
        convert_metric_value_to_float_if_possible(multi_item_tf_tensor)

    assert e.value.error_code == ErrorCode.Name(INVALID_PARAMETER_VALUE)


def test_convert_metric_value_to_float():
    tf_tensor_val = tf.random.uniform([], dtype=tf.float32)
    assert convert_metric_value_to_float_if_possible(tf_tensor_val) == float(tf_tensor_val.numpy())


def test_log_tf_tensor_as_metric():
    tf_tensor_val = tf.random.uniform([], dtype=tf.float32)
    tf_tensor_float_val = float(tf_tensor_val.numpy())

    with start_run() as run:
        MLForge.log_metric("name_tf", tf_tensor_val)

    finished_run = tracking.MLForgeClient().get_run(run.info.run_id)
    assert finished_run.data.metrics == {"name_tf": tf_tensor_float_val}
