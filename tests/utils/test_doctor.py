from unittest import mock

import MLForge


def test_doctor(capsys):
    MLForge.doctor()
    captured = capsys.readouterr()
    assert f"MLForge version: {MLForge.__version__}" in captured.out


def test_doctor_active_run(capsys):
    with MLForge.start_run() as run:
        MLForge.doctor()
        captured = capsys.readouterr()
        assert f"Active run ID: {run.info.run_id}" in captured.out


def test_doctor_databricks_runtime(capsys):
    mock_version = "12.0"
    with mock.patch(
        "MLForge.utils.doctor.get_databricks_runtime_version", return_value=mock_version
    ) as mock_runtime:
        MLForge.doctor()
        mock_runtime.assert_called_once()
        captured = capsys.readouterr()
        assert f"Databricks runtime version: {mock_version}" in captured.out
