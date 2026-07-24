MLForge REST API Example
-----------------------
This simple example shows how you could use MLForge REST API to create new
runs inside an experiment to log parameters/metrics.

To run this example code do the following:

Open a terminal and navigate to the ``/tmp`` directory and start the MLForge tracking server::

  MLForge server

In another terminal window navigate to the ``MLForge/examples/rest_api`` directory.  Run the example code
with this command::

  python MLForge_tracking_rest_api.py

Program options::

  usage: MLForge_tracking_rest_api.py [-h] [--hostname HOSTNAME] [--port PORT]
                                   [--experiment-id EXPERIMENT_ID]

  MLForge REST API Example

  optional arguments:
    -h, --help            show this help message and exit
    --hostname HOSTNAME   MLForge server hostname/ip (default: localhost)
    --port PORT           MLForge server port number (default: 5000)
    --experiment-id EXPERIMENT_ID
                            Experiment ID (default: 0)
