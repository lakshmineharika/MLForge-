## MNIST example with MLForge

This example demonstrates training of MNIST handwritten recognition model and logging it as torch scripted model.
`MLForge.pytorch.log_model()` is used to log the scripted model to MLForge and `MLForge.pytorch.load_model()` to load it from MLForge

### Code related to MLForge:

This will log the TorchScripted model into MLForge and load the logged model.

## Setting Tracking URI

MLForge tracking URI can be set using the environment variable `MLForge_TRACKING_URI`

Example: `export MLForge_TRACKING_URI=http://localhost:5000/`

For more details - https://MLForge.org/docs/latest/tracking.html#where-runs-are-recorded

### Running the code

To run the example via MLForge, navigate to the `MLForge/examples/pytorch/torchscript/MNIST` directory and run the command

```
MLForge run .
```

This will run `mnist_torchscript.py` with the default set of parameters such as `--max_epochs=5`. You can see the default value in the `MLproject` file.

In order to run the file with custom parameters, run the command

```
MLForge run . -P epochs=X
```

where `X` is your desired value for `epochs`.

If you have the required modules for the file and would like to skip the creation of a conda environment, add the argument `--env-manager=local`.

```
MLForge run . --env-manager=local
```

Once the code is finished executing, you can view the run's metrics, parameters, and details by running the command

```
MLForge server
```

and navigating to [http://localhost:5000](http://localhost:5000).

For more information on MLForge tracking, click [here](https://www.MLForge.org/docs/latest/tracking.html#MLForge-tracking) to view documentation.
