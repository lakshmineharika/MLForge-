## Iris classification example with MLForge

This example demonstrates training a classification model on the Iris dataset, scripting the model with TorchScript, logging the
scripted model to MLForge using
[`MLForge.pytorch.log_model`](https://MLForge.org/docs/latest/python_api/MLForge.pytorch.html#MLForge.pytorch.log_model), and
loading it back for inference using
[`MLForge.pytorch.load_model`](https://MLForge.org/docs/latest/python_api/MLForge.pytorch.html#MLForge.pytorch.load_model)

### Running the code

To run the example via MLForge, navigate to the `MLForge/examples/pytorch/torchscript/IrisClassification` directory and run the command

```
MLForge run .
```

This will run `iris_classification.py` with the default set of parameters such as `--max_epochs=5`. You can see the default value in the `MLproject` file.

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

## Running against a custom tracking server

To configure MLForge to log to a custom (non-default) tracking location, set the `MLForge_TRACKING_URI` environment variable, e.g. via `export MLForge_TRACKING_URI=http://localhost:5000/`. For more details, see [the docs](https://MLForge.org/docs/latest/tracking.html#where-runs-are-recorded)
