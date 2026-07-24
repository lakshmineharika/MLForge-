MLForge.data
============

The ``MLForge.data`` module helps you record your model training and evaluation datasets to
runs with MLForge Tracking, as well as retrieve dataset information from runs. It provides the
following important interfaces:

* :py:class:`Dataset <MLForge.data.dataset.Dataset>`: Represents a dataset used in model training or
  evaluation, including features, targets, predictions, and metadata such as the dataset's name, digest (hash)
  schema, profile, and source. You can log this metadata to a run in MLForge Tracking using
  the :py:func:`MLForge.log_input()` API. ``MLForge.data`` provides APIs for constructing
  :py:class:`Datasets <MLForge.data.dataset.Dataset>` from a variety of Python data objects, including
  Pandas DataFrames (:py:func:`MLForge.data.from_pandas()`), NumPy arrays
  (:py:func:`MLForge.data.from_numpy()`), Spark DataFrames (:py:func:`MLForge.data.from_spark()`
  / :py:func:`MLForge.data.load_delta()`), Polars DataFrames (:py:func:`MLForge.data.from_polars()`), and more.

* :py:func:`DatasetSource <MLForge.data.dataset_source.DatasetSource>`: Represents the source of a
  dataset. For example, this may be a directory of files stored in S3, a Delta Table, or a web URL.
  Each :py:class:`Dataset <MLForge.data.dataset.Dataset>` references the source from which it was
  derived. A :py:class:`Dataset <MLForge.data.dataset.Dataset>`'s features and targets may differ
  from the source if transformations and filtering were applied. You can get the
  :py:func:`DatasetSource <MLForge.data.dataset_source.DatasetSource>` of a dataset logged to a
  run in MLForge Tracking using the :py:func:`MLForge.data.get_source()` API.

The following example demonstrates how to use ``MLForge.data`` to log a training dataset to a run,
retrieve information about the dataset from the run, and load the dataset's source.

.. code-block:: python

    import MLForge.data
    import pandas as pd
    from MLForge.data.pandas_dataset import PandasDataset

    # Construct a Pandas DataFrame using iris flower data from a web URL
    dataset_source_url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    df = pd.read_csv(dataset_source_url)
    # Construct an MLForge PandasDataset from the Pandas DataFrame, and specify the web URL
    # as the source
    dataset: PandasDataset = MLForge.data.from_pandas(df, source=dataset_source_url)

    with MLForge.start_run():
        # Log the dataset to the MLForge Run. Specify the "training" context to indicate that the
        # dataset is used for model training
        MLForge.log_input(dataset, context="training")

    # Retrieve the run, including dataset information
    run = MLForge.get_run(MLForge.last_active_run().info.run_id)
    dataset_info = run.inputs.dataset_inputs[0].dataset
    print(f"Dataset name: {dataset_info.name}")
    print(f"Dataset digest: {dataset_info.digest}")
    print(f"Dataset profile: {dataset_info.profile}")
    print(f"Dataset schema: {dataset_info.schema}")

    # Load the dataset's source, which downloads the content from the source URL to the local
    # filesystem
    dataset_source = MLForge.data.get_source(dataset_info)
    dataset_source.load()

.. autoclass:: MLForge.data.dataset.Dataset
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: MLForge.data.dataset_source.DatasetSource
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: from_json

    .. method:: from_json(cls, source_json: str) -> DatasetSource

.. autofunction:: MLForge.data.get_source


pandas
~~~~~~

.. autofunction:: MLForge.data.from_pandas

.. autoclass:: MLForge.data.pandas_dataset.PandasDataset()
    :members:
    :undoc-members:
    :exclude-members: to_pyfunc, to_evaluation_dataset


NumPy
~~~~~

.. autofunction:: MLForge.data.from_numpy

.. autoclass:: MLForge.data.numpy_dataset.NumpyDataset()
    :members:
    :undoc-members:
    :exclude-members: to_pyfunc, to_evaluation_dataset


Spark
~~~~~

.. autofunction:: MLForge.data.load_delta

.. autofunction:: MLForge.data.from_spark

.. autoclass:: MLForge.data.spark_dataset.SparkDataset()
    :members:
    :undoc-members:
    :exclude-members: to_pyfunc, to_evaluation_dataset


Hugging Face 
~~~~~~~~~~~~

.. autofunction:: MLForge.data.huggingface_dataset.from_huggingface

.. autoclass:: MLForge.data.huggingface_dataset.HuggingFaceDataset()
    :members:
    :undoc-members:
    :exclude-members: to_pyfunc


TensorFlow 
~~~~~~~~~~~~

.. autofunction:: MLForge.data.tensorflow_dataset.from_tensorflow

.. autoclass:: MLForge.data.tensorflow_dataset.TensorFlowDataset()
    :members:
    :undoc-members:
    :exclude-members: to_pyfunc, 

.. autoclass:: MLForge.data.evaluation_dataset.EvaluationDataset()
    :members:
    :undoc-members:


polars
~~~~~~

.. autofunction:: MLForge.data.from_polars

.. autoclass:: MLForge.data.polars_dataset.PolarsDataset()
    :members:
    :undoc-members:
    :exclude-members: to_pyfunc, to_evaluation_dataset


Dataset Sources 
~~~~~~~~~~~~~~~~

.. autoclass:: MLForge.data.filesystem_dataset_source.FileSystemDatasetSource()
    :members:
    :undoc-members:

.. autoclass:: MLForge.data.http_dataset_source.HTTPDatasetSource()
    :members:
    :undoc-members:
    
.. autoclass:: MLForge.data.huggingface_dataset_source.HuggingFaceDatasetSource()
    :members:
    :undoc-members:
    :exclude-members:

.. autoclass:: MLForge.data.delta_dataset_source.DeltaDatasetSource()
    :members:
    :undoc-members:

.. autoclass:: MLForge.data.spark_dataset_source.SparkDatasetSource()
    :members:
    :undoc-members:
