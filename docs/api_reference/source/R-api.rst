.. _R-api:

========
R API
========

The MLForge `R <https://www.r-project.org/about.html>`_ API allows you to use MLForge `Tracking <../tracking/index.html>`_, `Projects <../projects/index.html>`_ and `Models <../models/index.html>`_.

Prerequisites
=============

To use the MLForge R API, you must install `the MLForge Python package <https://pypi.org/project/MLForge/>`_.

.. code-block:: bash

    pip install MLForge

Installing with an Available Conda Environment example:

.. code-block:: bash
    
    conda create -n MLForge-env python
    conda activate MLForge-env
    pip install MLForge

The above provided commands create a new Conda environment named MLForge-env, specifying the default Python version. It then activates this environment, making it the active working environment. Finally, it installs the MLForge package using pip, ensuring that MLForge is isolated within this environment, allowing for independent Python and package management for MLForge-related tasks.

Optionally, you can set the ``MLForge_PYTHON_BIN`` and ``MLForge_BIN`` environment variables to specify the Python and MLForge binaries to use. By default, the R client automatically finds them using ``Sys.which('python')`` and ``Sys.which('MLForge')``.

.. code-block:: bash

    export MLForge_PYTHON_BIN=/path/to/bin/python
    export MLForge_BIN=/path/to/bin/MLForge

You can use the R API to start the `user interface <MLForge_ui_>`_, `create experiment <MLForge_create_experiment_>`_ and `search experiments <MLForge_search_experiments_>`_, `save models <MLForge_save_model.crate_>`_, `run projects <MLForge_run_>`_ and `serve models <MLForge_rfunc_serve_>`_ among many other functions available in the R API.

.. contents:: Table of Contents
    :local:
    :depth: 1

``build_context_tags_from_databricks_job_info``
===============================================

Get information from a Databricks job execution context

Parses the data from a job execution context when running on Databricks
in a non-interactive mode. This function extracts relevant data that
MLForge needs in order to properly utilize the MLForge APIs from this
context.

.. code:: r

   build_context_tags_from_databricks_job_info(job_info)

Arguments
---------

============ ======================================================
Argument     Description
============ ======================================================
``job_info`` The job-related metadata from a running Databricks job
============ ======================================================

Value
-----

A list of tags to be set by the run context when creating MLForge runs in
the current Databricks Job environment

``build_context_tags_from_databricks_notebook_info``
====================================================

Get information from Databricks Notebook environment

Retrieves the notebook id, path, url, name, version, and type from the
Databricks Notebook execution environment and sets them to a list to be
used for setting the configured environment for executing an MLForge run
in R from Databricks.

.. code:: r

   build_context_tags_from_databricks_notebook_info(notebook_info)

.. _arguments-1:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``notebook_info``             | The configuration data from the      |
|                               | Databricks Notebook environment      |
+-------------------------------+--------------------------------------+

.. _value-1:

Value
-----

A list of tags to be set by the run context when creating MLForge runs in
the current Databricks Notebook environment

``MLForge_client``
=================

Initialize an MLForge Client

Initializes and returns an MLForge client that communicates with the
tracking server or store at the specified URI.

.. code:: r

   MLForge_client(tracking_uri = NULL)

.. _arguments-2:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``tracking_uri``              | The tracking URI. If not provided,   |
|                               | defaults to the service set by       |
|                               | ``MLForge_set_tracking_uri()``.       |
+-------------------------------+--------------------------------------+

``MLForge_create_experiment``
============================

Create Experiment

Creates an MLForge experiment and returns its id.

.. code:: r

   MLForge_create_experiment(
     name,
     artifact_location = NULL,
     client = NULL,
     tags = NULL
   )

.. _arguments-3:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | The name of the experiment to        |
|                               | create.                              |
+-------------------------------+--------------------------------------+
| ``artifact_location``         | Location where all artifacts for     |
|                               | this experiment are stored. If not   |
|                               | provided, the remote server will     |
|                               | select an appropriate default.       |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+
| ``tags``                      | Experiment tags to set on the        |
|                               | experiment upon experiment creation. |
+-------------------------------+--------------------------------------+

``MLForge_create_model_version``
===============================

Create a model version

Create a model version

.. code:: r

   MLForge_create_model_version(
     name,
     source,
     run_id = NULL,
     tags = NULL,
     run_link = NULL,
     description = NULL,
     client = NULL
   )

.. _arguments-4:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | Register model under this name.      |
+-------------------------------+--------------------------------------+
| ``source``                    | URI indicating the location of the   |
|                               | model artifacts.                     |
+-------------------------------+--------------------------------------+
| ``run_id``                    | MLForge run ID for correlation, if    |
|                               | ``source`` was generated by an       |
|                               | experiment run in MLForge Tracking.   |
+-------------------------------+--------------------------------------+
| ``tags``                      | Additional metadata.                 |
+-------------------------------+--------------------------------------+
| ``run_link``                  | MLForge run link - This is the exact  |
|                               | link of the run that generated this  |
|                               | model version.                       |
+-------------------------------+--------------------------------------+
| ``description``               | Description for model version.       |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_create_registered_model``
==================================

Create registered model

Creates a new registered model in the model registry

.. code:: r

   MLForge_create_registered_model(
     name,
     tags = NULL,
     description = NULL,
     client = NULL
   )

.. _arguments-5:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | The name of the model to create.     |
+-------------------------------+--------------------------------------+
| ``tags``                      | Additional metadata for the          |
|                               | registered model (Optional).         |
+-------------------------------+--------------------------------------+
| ``description``               | Description for the registered model |
|                               | (Optional).                          |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_delete_experiment``
============================

Delete Experiment

Marks an experiment and associated runs, params, metrics, etc. for
deletion. If the experiment uses FileStore, artifacts associated with
experiment are also deleted.

.. code:: r

   MLForge_delete_experiment(experiment_id, client = NULL)

.. _arguments-6:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``experiment_id``             | ID of the associated experiment.     |
|                               | This field is required.              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_delete_model_version``
===============================

Delete a model version

Delete a model version

.. code:: r

   MLForge_delete_model_version(name, version, client = NULL)

.. _arguments-7:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | Name of the registered model.        |
+-------------------------------+--------------------------------------+
| ``version``                   | Model version number.                |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_delete_registered_model``
==================================

Delete registered model

Deletes an existing registered model by name

.. code:: r

   MLForge_delete_registered_model(name, client = NULL)

.. _arguments-8:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | The name of the model to delete      |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_delete_run``
=====================

Delete a Run

Deletes the run with the specified ID.

.. code:: r

   MLForge_delete_run(run_id, client = NULL)

.. _arguments-9:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_delete_tag``
=====================

Delete Tag

Deletes a tag on a run. This is irreversible. Tags are run metadata that
can be updated during a run and after a run completes.

.. code:: r

   MLForge_delete_tag(key, run_id = NULL, client = NULL)

.. _arguments-10:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``key``                       | Name of the tag. Maximum size is 255 |
|                               | bytes. This field is required.       |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_download_artifacts``
=============================

Download Artifacts

Download an artifact file or directory from a run to a local directory
if applicable, and return a local path for it.

.. code:: r

   MLForge_download_artifacts(path, run_id = NULL, client = NULL)

.. _arguments-11:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``path``                      | Relative source path to the desired  |
|                               | artifact.                            |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_end_run``
==================

End a Run

Terminates a run. Attempts to end the current active run if ``run_id``
is not specified.

.. code:: r

   MLForge_end_run(
     status = c("FINISHED", "FAILED", "KILLED"),
     end_time = NULL,
     run_id = NULL,
     client = NULL
   )

.. _arguments-12:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``status``                    | Updated status of the run. Defaults  |
|                               | to ``FINISHED``. Can also be set to  |
|                               | “FAILED” or “KILLED”.                |
+-------------------------------+--------------------------------------+
| ``end_time``                  | Unix timestamp of when the run ended |
|                               | in milliseconds.                     |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_get_experiment``
=========================

Get Experiment

Gets metadata for an experiment and a list of runs for the experiment.
Attempts to obtain the active experiment if both ``experiment_id`` and
``name`` are unspecified.

.. code:: r

   MLForge_get_experiment(experiment_id = NULL, name = NULL, client = NULL)

.. _arguments-13:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``experiment_id``             | ID of the experiment.                |
+-------------------------------+--------------------------------------+
| ``name``                      | The experiment name. Only one of     |
|                               | ``name`` or ``experiment_id`` should |
|                               | be specified.                        |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_get_latest_versions``
==============================

Get latest model versions

Retrieves a list of the latest model versions for a given model.

.. code:: r

   MLForge_get_latest_versions(name, stages = list(), client = NULL)

.. _arguments-14:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | Name of the model.                   |
+-------------------------------+--------------------------------------+
| ``stages``                    | A list of desired stages. If the     |
|                               | input list is NULL, return latest    |
|                               | versions for ALL_STAGES.             |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_get_metric_history``
=============================

Get Metric History

Get a list of all values for the specified metric for a given run.

.. code:: r

   MLForge_get_metric_history(metric_key, run_id = NULL, client = NULL)

.. _arguments-15:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``metric_key``                | Name of the metric.                  |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_get_model_version``
============================

Get a model version

Get a model version

.. code:: r

   MLForge_get_model_version(name, version, client = NULL)

.. _arguments-16:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | Name of the registered model.        |
+-------------------------------+--------------------------------------+
| ``version``                   | Model version number.                |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_get_registered_model``
===============================

Get a registered model

Retrieves a registered model from the Model Registry.

.. code:: r

   MLForge_get_registered_model(name, client = NULL)

.. _arguments-17:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | The name of the model to retrieve.   |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_get_run``
==================

Get Run

Gets metadata, params, tags, and metrics for a run. Returns a single
value for each metric key: the most recently logged metric value at the
largest step.

.. code:: r

   MLForge_get_run(run_id = NULL, client = NULL)

.. _arguments-18:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_get_tracking_uri``
===========================

Get Remote Tracking URI

Gets the remote tracking URI.

.. code:: r

   MLForge_get_tracking_uri()

``MLForge_id``
=============

Get Run or Experiment ID

Extracts the ID of the run or experiment.

.. code:: r

   MLForge_id(object)
   list(list("MLForge_id"), list("MLForge_run"))(object)
   list(list("MLForge_id"), list("MLForge_experiment"))(object)

.. _arguments-19:

Arguments
---------

========== ==================================================
Argument   Description
========== ==================================================
``object`` An ``MLForge_run`` or ``MLForge_experiment`` object.
========== ==================================================

``MLForge_list_artifacts``
=========================

List Artifacts

Gets a list of artifacts.

.. code:: r

   MLForge_list_artifacts(path = NULL, run_id = NULL, client = NULL)

.. _arguments-20:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``path``                      | The run’s relative artifact path to  |
|                               | list from. If not specified, it is   |
|                               | set to the root artifact path        |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_load_flavor``
======================

Load MLForge Model Flavor

Loads an MLForge model using a specific flavor. This method is called
internally by `MLForge_load_model <#MLForge-load-model>`__ , but is
exposed for package authors to extend the supported MLForge models. See
https://MLForge.org/docs/latest/models.html#storage-format for more info
on MLForge model flavors.

.. code:: r

   MLForge_load_flavor(flavor, model_path)

.. _arguments-21:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``flavor``                    | An MLForge flavor object loaded by    |
|                               | `mlflo                               |
|                               | w_load_model <#MLForge-load-model>`__ |
|                               | , with class loaded from the flavor  |
|                               | field in an MLmodel file.            |
+-------------------------------+--------------------------------------+
| ``model_path``                | The path to the MLForge model wrapped |
|                               | in the correct class.                |
+-------------------------------+--------------------------------------+

``MLForge_load_model``
=====================

Load MLForge Model

Loads an MLForge model. MLForge models can have multiple model flavors.
Not all flavors / models can be loaded in R. This method by default
searches for a flavor supported by R/MLForge.

.. code:: r

   MLForge_load_model(model_uri, flavor = NULL, client = MLForge_client())

.. _arguments-22:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``model_uri``                 | The location, in URI format, of the  |
|                               | MLForge model.                        |
+-------------------------------+--------------------------------------+
| ``flavor``                    | Optional flavor specification        |
|                               | (string). Can be used to load a      |
|                               | particular flavor in case there are  |
|                               | multiple flavors available.          |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

Details
-------

The URI scheme must be supported by MLForge - i.e. there has to be an
MLForge artifact repository corresponding to the scheme of the URI. The
content is expected to point to a directory containing MLmodel. The
following are examples of valid model uris:

-  ``file:///absolute/path/to/local/model``
-  ``file:relative/path/to/local/model``
-  ``s3://my_bucket/path/to/model``
-  ``runs:/<MLForge_run_id>/run-relative/path/to/model``
-  ``models:/<model_name>/<model_version>``
-  ``models:/<model_name>/<stage>``

For more information about supported URI schemes, see the Artifacts
Documentation at
https://www.MLForge.org/docs/latest/tracking.html#artifact-stores.

``MLForge_log_artifact``
=======================

Log Artifact

Logs a specific file or directory as an artifact for a run.

.. code:: r

   MLForge_log_artifact(path, artifact_path = NULL, run_id = NULL, client = NULL)

.. _arguments-23:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``path``                      | The file or directory to log as an   |
|                               | artifact.                            |
+-------------------------------+--------------------------------------+
| ``artifact_path``             | Destination path within the run’s    |
|                               | artifact URI.                        |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

.. _details-1:

Details
-------

When logging to Amazon S3, ensure that you have the s3:PutObject,
s3:GetObject, s3:ListBucket, and s3:GetBucketLocation permissions on
your bucket.

Additionally, at least the ``AWS_ACCESS_KEY_ID`` and
``AWS_SECRET_ACCESS_KEY`` environment variables must be set to the
corresponding key and secrets provided by Amazon IAM.

``MLForge_log_batch``
====================

Log Batch

Log a batch of metrics, params, and/or tags for a run. The server will
respond with an error (non-200 status code) if any data failed to be
persisted. In case of error (due to internal server error or an invalid
request), partial data may be written.

.. code:: r

   MLForge_log_batch(
     metrics = NULL,
     params = NULL,
     tags = NULL,
     run_id = NULL,
     client = NULL
   )

.. _arguments-24:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``metrics``                   | A dataframe of metrics to log,       |
|                               | containing the following columns:    |
|                               | “key”, “value”, “step”, “timestamp”. |
|                               | This dataframe cannot contain any    |
|                               | missing (‘NA’) entries.              |
+-------------------------------+--------------------------------------+
| ``params``                    | A dataframe of params to log,        |
|                               | containing the following columns:    |
|                               | “key”, “value”. This dataframe       |
|                               | cannot contain any missing (‘NA’)    |
|                               | entries.                             |
+-------------------------------+--------------------------------------+
| ``tags``                      | A dataframe of tags to log,          |
|                               | containing the following columns:    |
|                               | “key”, “value”. This dataframe       |
|                               | cannot contain any missing (‘NA’)    |
|                               | entries.                             |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_log_metric``
=====================

Log Metric

Logs a metric for a run. Metrics key-value pair that records a single
float measure. During a single execution of a run, a particular metric
can be logged several times. The MLForge Backend keeps track of
historical metric values along two axes: timestamp and step.

.. code:: r

   MLForge_log_metric(
     key,
     value,
     timestamp = NULL,
     step = NULL,
     run_id = NULL,
     client = NULL
   )

.. _arguments-25:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``key``                       | Name of the metric.                  |
+-------------------------------+--------------------------------------+
| ``value``                     | Float value for the metric being     |
|                               | logged.                              |
+-------------------------------+--------------------------------------+
| ``timestamp``                 | Timestamp at which to log the        |
|                               | metric. Timestamp is rounded to the  |
|                               | nearest integer. If unspecified, the |
|                               | number of milliseconds since the     |
|                               | Unix epoch is used.                  |
+-------------------------------+--------------------------------------+
| ``step``                      | Step at which to log the metric.     |
|                               | Step is rounded to the nearest       |
|                               | integer. If unspecified, the default |
|                               | value of zero is used.               |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_log_model``
====================

Log Model

Logs a model for this run. Similar to ``MLForge_save_model()`` but stores
model as an artifact within the active run.

.. code:: r

   MLForge_log_model(model, artifact_path, ...)

.. _arguments-26:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``model``                     | The model that will perform a        |
|                               | prediction.                          |
+-------------------------------+--------------------------------------+
| ``artifact_path``             | Destination path where this MLForge   |
|                               | compatible model will be saved.      |
+-------------------------------+--------------------------------------+
| ``...``                       | Optional additional arguments passed |
|                               | to ``MLForge_save_model()`` when      |
|                               | persisting the model. For example,   |
|                               | ``conda_env = /path/to/conda.yaml``  |
|                               | may be passed to specify a conda     |
|                               | dependencies file for flavors        |
|                               | (e.g. keras) that support conda      |
|                               | environments.                        |
+-------------------------------+--------------------------------------+

``MLForge_log_param``
====================

Log Parameter

Logs a parameter for a run. Examples are params and hyperparams used for
ML training, or constant dates and values used in an ETL pipeline. A
param is a STRING key-value pair. For a run, a single parameter is
allowed to be logged only once.

.. code:: r

   MLForge_log_param(key, value, run_id = NULL, client = NULL)

.. _arguments-27:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``key``                       | Name of the parameter.               |
+-------------------------------+--------------------------------------+
| ``value``                     | String value of the parameter.       |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_param``
================

Read Command-Line Parameter

Reads a command-line parameter passed to an MLForge project MLForge allows
you to define named, typed input parameters to your R scripts via the
MLForge_param API. This is useful for experimentation, e.g. tracking
multiple invocations of the same script with different parameters.

.. code:: r

   MLForge_param(name, default = NULL, type = NULL, description = NULL)

.. _arguments-28:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | The name of the parameter.           |
+-------------------------------+--------------------------------------+
| ``default``                   | The default value of the parameter.  |
+-------------------------------+--------------------------------------+
| ``type``                      | Type of this parameter. Required if  |
|                               | ``default`` is not set. If           |
|                               | specified, must be one of “numeric”, |
|                               | “integer”, or “string”.              |
+-------------------------------+--------------------------------------+
| ``description``               | Optional description for the         |
|                               | parameter.                           |
+-------------------------------+--------------------------------------+

Examples
--------

.. code:: r

   # This parametrized script trains a GBM model on the Iris dataset and can be run as an MLForge
   # project. You can run this script (assuming it's saved at /some/directory/params_example.R)
   # with custom parameters via:
   # MLForge_run(entry_point = "params_example.R", uri = "/some/directory",
   #   parameters = list(num_trees = 200, learning_rate = 0.1))
   install.packages("gbm")
   library(MLForge)
   library(gbm)
   # define and read input parameters
   num_trees <- MLForge_param(name = "num_trees", default = 200, type = "integer")
   lr <- MLForge_param(name = "learning_rate", default = 0.1, type = "numeric")
   # use params to fit a model
   ir.adaboost <- gbm(Species ~., data=iris, n.trees=num_trees, shrinkage=lr)

``MLForge_predict``
==================

Generate Prediction with MLForge Model

Performs prediction over a model loaded using ``MLForge_load_model()`` ,
to be used by package authors to extend the supported MLForge models.

.. code:: r

   MLForge_predict(model, data, ...)

.. _arguments-29:

Arguments
---------

+-----------+---------------------------------------------------------+
| Argument  | Description                                             |
+===========+=========================================================+
| ``model`` | The loaded MLForge model flavor.                         |
+-----------+---------------------------------------------------------+
| ``data``  | A data frame to perform scoring.                        |
+-----------+---------------------------------------------------------+
| ``...``   | Optional additional arguments passed to underlying      |
|           | predict methods.                                        |
+-----------+---------------------------------------------------------+

``MLForge_register_external_observer``
=====================================

Register an external MLForge observer

Registers an external MLForge observer that will receive a
``register_tracking_event(event_name, data)`` callback on any model
tracking event such as “create_run”, “delete_run”, or “log_metric”. Each
observer should have a ``register_tracking_event(event_name, data)``
callback accepting a character vector ``event_name`` specifying the name
of the tracking event, and ``data`` containing a list of attributes of
the event. The callback should be non-blocking, and ideally should
complete instantaneously. Any exception thrown from the callback will be
ignored.

.. code:: r

   MLForge_register_external_observer(observer)

.. _arguments-30:

Arguments
---------

============ =================================
Argument     Description
============ =================================
``observer`` The observer object (see example)
============ =================================

.. _examples-1:

Examples
--------

.. code:: r

   library(MLForge)

   observer <- structure(list())
   observer$register_tracking_event <- function(event_name, data) {
   print(event_name)
   print(data)
   }
   MLForge_register_external_observer(observer)

``MLForge_rename_experiment``
============================

Rename Experiment

Renames an experiment.

.. code:: r

   MLForge_rename_experiment(new_name, experiment_id = NULL, client = NULL)

.. _arguments-31:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``new_name``                  | The experiment’s name will be        |
|                               | changed to this. The new name must   |
|                               | be unique.                           |
+-------------------------------+--------------------------------------+
| ``experiment_id``             | ID of the associated experiment.     |
|                               | This field is required.              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_rename_registered_model``
==================================

Rename a registered model

Renames a model in the Model Registry.

.. code:: r

   MLForge_rename_registered_model(name, new_name, client = NULL)

.. _arguments-32:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | The current name of the model.       |
+-------------------------------+--------------------------------------+
| ``new_name``                  | The new name for the model.          |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_restore_experiment``
=============================

Restore Experiment

Restores an experiment marked for deletion. This also restores
associated metadata, runs, metrics, and params. If experiment uses
FileStore, underlying artifacts associated with experiment are also
restored.

.. code:: r

   MLForge_restore_experiment(experiment_id, client = NULL)

.. _arguments-33:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``experiment_id``             | ID of the associated experiment.     |
|                               | This field is required.              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

.. _details-2:

Details
-------

Throws ``RESOURCE_DOES_NOT_EXIST`` if the experiment was never created
or was permanently deleted.

``MLForge_restore_run``
======================

Restore a Run

Restores the run with the specified ID.

.. code:: r

   MLForge_restore_run(run_id, client = NULL)

.. _arguments-34:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_rfunc_serve``
======================

Serve an RFunc MLForge Model

Serves an RFunc MLForge model as a local REST API server. This interface
provides similar functionality to ``MLForge models serve`` cli command,
however, it can only be used to deploy models that include RFunc flavor.
The deployed server supports standard MLForge models interface with /ping
and /invocation endpoints. In addition, R function models also support
deprecated /predict endpoint for generating predictions. The /predict
endpoint will be removed in a future version of MLForge.

.. code:: r

   MLForge_rfunc_serve(
     model_uri,
     host = "127.0.0.1",
     port = 8090,
     daemonized = FALSE,
     browse = !daemonized,
     ...
   )

.. _arguments-35:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``model_uri``                 | The location, in URI format, of the  |
|                               | MLForge model.                        |
+-------------------------------+--------------------------------------+
| ``host``                      | Address to use to serve model, as a  |
|                               | string.                              |
+-------------------------------+--------------------------------------+
| ``port``                      | Port to use to serve model, as       |
|                               | numeric.                             |
+-------------------------------+--------------------------------------+
| ``daemonized``                | Makes ``httpuv`` server daemonized   |
|                               | so R interactive sessions are not    |
|                               | blocked to handle requests. To       |
|                               | terminate a daemonized server, call  |
|                               | ``httpuv::stopDaemonizedServer()``   |
|                               | with the handle returned from this   |
|                               | call.                                |
+-------------------------------+--------------------------------------+
| ``browse``                    | Launch browser with serving landing  |
|                               | page?                                |
+-------------------------------+--------------------------------------+
| ``...``                       | Optional arguments passed to         |
|                               | ``MLForge_predict()``.                |
+-------------------------------+--------------------------------------+

.. _details-3:

Details
-------

The URI scheme must be supported by MLForge - i.e. there has to be an
MLForge artifact repository corresponding to the scheme of the URI. The
content is expected to point to a directory containing MLmodel. The
following are examples of valid model uris:

-  ``file:///absolute/path/to/local/model``
-  ``file:relative/path/to/local/model``
-  ``s3://my_bucket/path/to/model``
-  ``runs:/<MLForge_run_id>/run-relative/path/to/model``
-  ``models:/<model_name>/<model_version>``
-  ``models:/<model_name>/<stage>``

For more information about supported URI schemes, see the Artifacts
Documentation at
https://www.MLForge.org/docs/latest/tracking.html#artifact-stores.

.. _examples-2:

Examples
--------

.. code:: r

   library(MLForge)

   # save simple model with constant prediction
   MLForge_save_model(function(df) 1, "MLForge_constant")

   # serve an existing model over a web interface
   MLForge_rfunc_serve("MLForge_constant")

   # request prediction from server
   httr::POST("http://127.0.0.1:8090/predict/")

``MLForge_run``
==============

Run an MLForge Project

Wrapper for the ``MLForge run`` CLI command. See
https://www.MLForge.org/docs/latest/cli.html#MLForge-run for more info.

.. code:: r

   MLForge_run(
     uri = ".",
     entry_point = NULL,
     version = NULL,
     parameters = NULL,
     experiment_id = NULL,
     experiment_name = NULL,
     backend = NULL,
     backend_config = NULL,
     env_manager = NULL,
     storage_dir = NULL
   )

.. _arguments-36:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``uri``                       | A directory containing modeling      |
|                               | scripts, defaults to the current     |
|                               | directory.                           |
+-------------------------------+--------------------------------------+
| ``entry_point``               | Entry point within project, defaults |
|                               | to ``main`` if not specified.        |
+-------------------------------+--------------------------------------+
| ``version``                   | Version of the project to run, as a  |
|                               | Git commit reference for Git         |
|                               | projects.                            |
+-------------------------------+--------------------------------------+
| ``parameters``                | A list of parameters.                |
+-------------------------------+--------------------------------------+
| ``experiment_id``             | ID of the experiment under which to  |
|                               | launch the run.                      |
+-------------------------------+--------------------------------------+
| ``experiment_name``           | Name of the experiment under which   |
|                               | to launch the run.                   |
+-------------------------------+--------------------------------------+
| ``backend``                   | Execution backend to use for run.    |
+-------------------------------+--------------------------------------+
| ``backend_config``            | Path to JSON file which will be      |
|                               | passed to the backend. For the       |
|                               | Databricks backend, it should        |
|                               | describe the cluster to use when     |
|                               | launching a run on Databricks.       |
+-------------------------------+--------------------------------------+
| ``env_manager``               | If specified, create an environment  |
|                               | for the project using the specified  |
|                               | environment manager. Available       |
|                               | options are ‘local’, ‘virtualenv’,   |
|                               | and ‘conda’.                         |
+-------------------------------+--------------------------------------+
| ``storage_dir``               | Valid only when ``backend`` is       |
|                               | local. MLForge downloads artifacts    |
|                               | from distributed URIs passed to      |
|                               | parameters of type ``path`` to       |
|                               | subdirectories of ``storage_dir``.   |
+-------------------------------+--------------------------------------+

.. _value-2:

Value
-----

The run associated with this run.

.. _examples-3:

Examples
--------

.. code:: r

   # This parametrized script trains a GBM model on the Iris dataset and can be run as an MLForge
   # project. You can run this script (assuming it's saved at /some/directory/params_example.R)
   # with custom parameters via:
   # MLForge_run(entry_point = "params_example.R", uri = "/some/directory",
   #   parameters = list(num_trees = 200, learning_rate = 0.1))
   install.packages("gbm")
   library(MLForge)
   library(gbm)
   # define and read input parameters
   num_trees <- MLForge_param(name = "num_trees", default = 200, type = "integer")
   lr <- MLForge_param(name = "learning_rate", default = 0.1, type = "numeric")
   # use params to fit a model
   ir.adaboost <- gbm(Species ~., data=iris, n.trees=num_trees, shrinkage=lr)

``MLForge_save_model.crate``
===========================

Save Model for MLForge

Saves model in MLForge format that can later be used for prediction and
serving. This method is generic to allow package authors to save custom
model types.

.. code:: r

   list(list("MLForge_save_model"), list("crate"))(model, path, model_spec = list(), ...)
   MLForge_save_model(model, path, model_spec = list(), ...)
   list(list("MLForge_save_model"), list("H2OModel"))(model, path, model_spec = list(), conda_env = NULL, ...)
   list(list("MLForge_save_model"), list("keras.engine.training.Model"))(model, path, model_spec = list(), conda_env = NULL, ...)
   list(list("MLForge_save_model"), list("xgb.Booster"))(model, path, model_spec = list(), conda_env = NULL, ...)

.. _arguments-37:

Arguments
---------

+----------------+----------------------------------------------------+
| Argument       | Description                                        |
+================+====================================================+
| ``model``      | The model that will perform a prediction.          |
+----------------+----------------------------------------------------+
| ``path``       | Destination path where this MLForge compatible      |
|                | model will be saved.                               |
+----------------+----------------------------------------------------+
| ``model_spec`` | MLForge model config this model flavor is being     |
|                | added to.                                          |
+----------------+----------------------------------------------------+
| ``...``        | Optional additional arguments.                     |
+----------------+----------------------------------------------------+
| ``conda_env``  | Path to Conda dependencies file.                   |
+----------------+----------------------------------------------------+

``MLForge_search_experiments``
=============================

Search Experiments

Search for experiments that satisfy specified criteria.

.. code:: r

   MLForge_search_experiments(
     filter = NULL,
     experiment_view_type = c("ACTIVE_ONLY", "DELETED_ONLY", "ALL"),
     max_results = 1000,
     order_by = list(),
     page_token = NULL,
     client = NULL
   )

.. _arguments-38:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``filter``                    | A filter expression used to identify |
|                               | specific experiments. The syntax is  |
|                               | a subset of SQL which allows only    |
|                               | ANDing together binary operations.   |
|                               | Examples: “attribute.name =          |
|                               | ‘MyExperiment’”, “tags.problem_type  |
|                               | = ‘iris_regression’”                 |
+-------------------------------+--------------------------------------+
| ``experiment_view_type``      | Experiment view type. Only           |
|                               | experiments matching this view type  |
|                               | are returned.                        |
+-------------------------------+--------------------------------------+
| ``max_results``               | Maximum number of experiments to     |
|                               | retrieve.                            |
+-------------------------------+--------------------------------------+
| ``order_by``                  | List of properties to order by.      |
|                               | Example: “attribute.name”.           |
+-------------------------------+--------------------------------------+
| ``page_token``                | Pagination token to go to the next   |
|                               | page based on a previous query.      |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_search_registered_models``
===================================

List registered models

Retrieves a list of registered models.

.. code:: r

   MLForge_search_registered_models(
     filter = NULL,
     max_results = 100,
     order_by = list(),
     page_token = NULL,
     client = NULL
   )

.. _arguments-39:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``filter``                    | A filter expression used to identify |
|                               | specific registered models. The      |
|                               | syntax is a subset of SQL which      |
|                               | allows only ANDing together binary   |
|                               | operations. Example: “name =         |
|                               | ‘my_model_name’ and tag.key =        |
|                               | ‘value1’”                            |
+-------------------------------+--------------------------------------+
| ``max_results``               | Maximum number of registered models  |
|                               | to retrieve.                         |
+-------------------------------+--------------------------------------+
| ``order_by``                  | List of registered model properties  |
|                               | to order by. Example: “name”.        |
+-------------------------------+--------------------------------------+
| ``page_token``                | Pagination token to go to the next   |
|                               | page based on a previous query.      |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_search_runs``
======================

Search Runs

Search for runs that satisfy expressions. Search expressions can use
Metric and Param keys.

.. code:: r

   MLForge_search_runs(
     filter = NULL,
     run_view_type = c("ACTIVE_ONLY", "DELETED_ONLY", "ALL"),
     experiment_ids = NULL,
     order_by = list(),
     client = NULL
   )

.. _arguments-40:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``filter``                    | A filter expression over params,     |
|                               | metrics, and tags, allowing          |
|                               | returning a subset of runs. The      |
|                               | syntax is a subset of SQL which      |
|                               | allows only ANDing together binary   |
|                               | operations between a                 |
|                               | param/metric/tag and a constant.     |
+-------------------------------+--------------------------------------+
| ``run_view_type``             | Run view type.                       |
+-------------------------------+--------------------------------------+
| ``experiment_ids``            | List of string experiment IDs (or a  |
|                               | single string experiment ID) to      |
|                               | search over. Attempts to use active  |
|                               | experiment if not specified.         |
+-------------------------------+--------------------------------------+
| ``order_by``                  | List of properties to order by.      |
|                               | Example: “metrics.acc DESC”.         |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_server``
=================

Run MLForge Tracking Server

Wrapper for ``MLForge server``.

.. code:: r

   MLForge_server(
     file_store = "mlruns",
     default_artifact_root = NULL,
     host = "127.0.0.1",
     port = 5000,
     workers = NULL,
     static_prefix = NULL,
     serve_artifacts = FALSE
   )

.. _arguments-41:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``file_store``                | The root of the backing file store   |
|                               | for experiment and run data.         |
+-------------------------------+--------------------------------------+
| ``default_artifact_root``     | Local or S3 URI to store artifacts   |
|                               | in, for newly created experiments.   |
+-------------------------------+--------------------------------------+
| ``host``                      | The network address to listen on     |
|                               | (default: 127.0.0.1).                |
+-------------------------------+--------------------------------------+
| ``port``                      | The port to listen on (default:      |
|                               | 5000).                               |
+-------------------------------+--------------------------------------+
| ``workers``                   | Number of gunicorn worker processes  |
|                               | to handle requests (default: 4).     |
+-------------------------------+--------------------------------------+
| ``static_prefix``             | A prefix which will be prepended to  |
|                               | the path of all static paths.        |
+-------------------------------+--------------------------------------+
| ``serve_artifacts``           | A flag specifying whether or not to  |
|                               | enable artifact serving (default:    |
|                               | FALSE).                              |
+-------------------------------+--------------------------------------+

``MLForge_set_experiment_tag``
=============================

Set Experiment Tag

Sets a tag on an experiment with the specified ID. Tags are experiment
metadata that can be updated.

.. code:: r

   MLForge_set_experiment_tag(key, value, experiment_id = NULL, client = NULL)

.. _arguments-42:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``key``                       | Name of the tag. All storage         |
|                               | backends are guaranteed to support   |
|                               | key values up to 250 bytes in size.  |
|                               | This field is required.              |
+-------------------------------+--------------------------------------+
| ``value``                     | String value of the tag being        |
|                               | logged. All storage backends are     |
|                               | guaranteed to support key values up  |
|                               | to 5000 bytes in size. This field is |
|                               | required.                            |
+-------------------------------+--------------------------------------+
| ``experiment_id``             | ID of the experiment.                |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_set_experiment``
=========================

Set Experiment

Sets an experiment as the active experiment. Either the name or ID of
the experiment can be provided. If the a name is provided but the
experiment does not exist, this function creates an experiment with
provided name. Returns the ID of the active experiment.

.. code:: r

   MLForge_set_experiment(
     experiment_name = NULL,
     experiment_id = NULL,
     artifact_location = NULL
   )

.. _arguments-43:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``experiment_name``           | Name of experiment to be activated.  |
+-------------------------------+--------------------------------------+
| ``experiment_id``             | ID of experiment to be activated.    |
+-------------------------------+--------------------------------------+
| ``artifact_location``         | Location where all artifacts for     |
|                               | this experiment are stored. If not   |
|                               | provided, the remote server will     |
|                               | select an appropriate default.       |
+-------------------------------+--------------------------------------+

``MLForge_set_model_version_tag``
================================

Set Model version tag

Set a tag for the model version. When stage is set, tag will be set for
latest model version of the stage. Setting both version and stage
parameter will result in error.

.. code:: r

   MLForge_set_model_version_tag(
     name,
     version = NULL,
     key = NULL,
     value = NULL,
     stage = NULL,
     client = NULL
   )

.. _arguments-44:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | Registered model name.               |
+-------------------------------+--------------------------------------+
| ``version``                   | Registered model version.            |
+-------------------------------+--------------------------------------+
| ``key``                       | Tag key to log. key is required.     |
+-------------------------------+--------------------------------------+
| ``value``                     | Tag value to log. value is required. |
+-------------------------------+--------------------------------------+
| ``stage``                     | Registered model stage.              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_set_tag``
==================

Set Tag

Sets a tag on a run. Tags are run metadata that can be updated during a
run and after a run completes.

.. code:: r

   MLForge_set_tag(key, value, run_id = NULL, client = NULL)

.. _arguments-45:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``key``                       | Name of the tag. Maximum size is 255 |
|                               | bytes. This field is required.       |
+-------------------------------+--------------------------------------+
| ``value``                     | String value of the tag being        |
|                               | logged. Maximum size is 500 bytes.   |
|                               | This field is required.              |
+-------------------------------+--------------------------------------+
| ``run_id``                    | Run ID.                              |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_set_tracking_uri``
===========================

Set Remote Tracking URI

Specifies the URI to the remote MLForge server that will be used to track
experiments.

.. code:: r

   MLForge_set_tracking_uri(uri)

.. _arguments-46:

Arguments
---------

======== ====================================
Argument Description
======== ====================================
``uri``  The URI to the remote MLForge server.
======== ====================================

``MLForge_source``
=================

Source a Script with MLForge Params

This function should not be used interactively. It is designed to be
called via ``Rscript`` from the terminal or through the MLForge CLI.

.. code:: r

   MLForge_source(uri)

.. _arguments-47:

Arguments
---------

======== ========================================================
Argument Description
======== ========================================================
``uri``  Path to an R script, can be a quoted or unquoted string.
======== ========================================================

``MLForge_start_run``
====================

Start Run

Starts a new run. If ``client`` is not provided, this function infers
contextual information such as source name and version, and also
registers the created run as the active run. If ``client`` is provided,
no inference is done, and additional arguments such as ``start_time``
can be provided.

.. code:: r

   MLForge_start_run(
     run_id = NULL,
     experiment_id = NULL,
     start_time = NULL,
     tags = NULL,
     client = NULL,
     nested = FALSE
   )

.. _arguments-48:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``run_id``                    | If specified, get the run with the   |
|                               | specified UUID and log metrics and   |
|                               | params under that run. The run’s end |
|                               | time is unset and its status is set  |
|                               | to running, but the run’s other      |
|                               | attributes remain unchanged.         |
+-------------------------------+--------------------------------------+
| ``experiment_id``             | Used only when ``run_id`` is         |
|                               | unspecified. ID of the experiment    |
|                               | under which to create the current    |
|                               | run. If unspecified, the run is      |
|                               | created under a new experiment with  |
|                               | a randomly generated name.           |
+-------------------------------+--------------------------------------+
| ``start_time``                | Unix timestamp of when the run       |
|                               | started in milliseconds. Only used   |
|                               | when ``client`` is specified.        |
+-------------------------------+--------------------------------------+
| ``tags``                      | Additional metadata for run in       |
|                               | key-value pairs. Only used when      |
|                               | ``client`` is specified.             |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+
| ``nested``                    | Controls whether the run to be       |
|                               | started is nested in a parent run.   |
|                               | ``TRUE`` creates a nest run.         |
+-------------------------------+--------------------------------------+

.. _examples-4:

Examples
--------

.. code:: r

   with(MLForge_start_run(), {
   MLForge_log_metric("test", 10)
   })

``MLForge_transition_model_version_stage``
=========================================

Transition ModelVersion Stage

Transition a model version to a different stage.

.. code:: r

   MLForge_transition_model_version_stage(
     name,
     version,
     stage,
     archive_existing_versions = FALSE,
     client = NULL
   )

.. _arguments-49:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | Name of the registered model.        |
+-------------------------------+--------------------------------------+
| ``version``                   | Model version number.                |
+-------------------------------+--------------------------------------+
| ``stage``                     | Transition ``model_version`` to this |
|                               | stage.                               |
+-------------------------------+--------------------------------------+
| ``archive_existing_versions`` | (Optional)                           |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_ui``
=============

Run MLForge User Interface

Launches the MLForge user interface.

.. code:: r

   MLForge_ui(client, ...)

.. _arguments-50:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+
| ``...``                       | Optional arguments passed to         |
|                               | ``MLForge_server()`` when ``x`` is a  |
|                               | path to a file store.                |
+-------------------------------+--------------------------------------+

.. _examples-5:

Examples
--------

.. code:: r

   library(MLForge)

   # launch MLForge ui locally
   MLForge_ui()

   # launch MLForge ui for existing MLForge server
   MLForge_set_tracking_uri("http://tracking-server:5000")
   MLForge_ui()

``MLForge_update_model_version``
===============================

Update model version

Updates a model version

.. code:: r

   MLForge_update_model_version(name, version, description, client = NULL)

.. _arguments-51:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | Name of the registered model.        |
+-------------------------------+--------------------------------------+
| ``version``                   | Model version number.                |
+-------------------------------+--------------------------------------+
| ``description``               | Description of this model version.   |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+

``MLForge_update_registered_model``
==================================

Update a registered model

Updates a model in the Model Registry.

.. code:: r

   MLForge_update_registered_model(name, description, client = NULL)

.. _arguments-52:

Arguments
---------

+-------------------------------+--------------------------------------+
| Argument                      | Description                          |
+===============================+======================================+
| ``name``                      | The name of the registered model.    |
+-------------------------------+--------------------------------------+
| ``description``               | The updated description for this     |
|                               | registered model.                    |
+-------------------------------+--------------------------------------+
| ``client``                    | (Optional) An MLForge client object   |
|                               | returned from                        |
|                               | `MLForge_client <#MLForge-client>`__ . |
|                               | If specified, MLForge will use the    |
|                               | tracking server associated with the  |
|                               | passed-in client. If unspecified     |
|                               | (the common case), MLForge will use   |
|                               | the tracking server associated with  |
|                               | the current tracking URI.            |
+-------------------------------+--------------------------------------+
