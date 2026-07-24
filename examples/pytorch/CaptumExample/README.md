## Using Captum and MLForge to interpret Pytorch models

In this example, we will demonstrate the basic features of the [Captum](https://captum.ai/) interpretability,and logging those features using MLForge library through an example model trained on the Titanic survival data.
We will first train a deep neural network on the data using PyTorch and use Captum to understand which of the features were most important and how the network reached its prediction.

you can get more details about used attributions methods used in this example

1. [Titanic_Basic_Interpret](https://captum.ai/tutorials/Titanic_Basic_Interpret)
2. [integrated-gradients](https://captum.ai/docs/algorithms#primary-attribution)
3. [layer-attributions](https://captum.ai/docs/algorithms#layer-attribution)

### Running the code

To run the example via MLForge, navigate to the `MLForge/examples/pytorch/CaptumExample` directory and run the command

```
MLForge run .
```

This will run `Titanic_Captum_Interpret.py` with default parameter values, e.g. `--max_epochs=100` and `--use_pretrained_model False`. You can see the full set of parameters in the `MLproject` file within this directory.

In order to run the file with custom parameters, run the command

```
MLForge run . -P max_epochs=X
```

where `X` is your desired value for `max_epochs`.

If you have the required modules for the file and would like to skip the creation of a conda environment, add the argument `--env-manager=local`.

```
MLForge run . --env-manager=local
```

### Viewing results in the MLForge UI

Once the code is finished executing, you can view the run's metrics, parameters, and details by running the command

```
MLForge server
```

and navigating to [http://localhost:5000](http://localhost:5000).

For more details on MLForge tracking, see [the docs](https://www.MLForge.org/docs/latest/tracking.html#MLForge-tracking).

### Passing custom training parameters

The parameters can be overridden via the command line:

1. max_epochs - Number of epochs to train model. Training can be interrupted early via Ctrl+C
2. lr - Learning rate
3. use_pretrained_model - If want to use pretrained model

For example:

```
MLForge run . -P max_epochs=5 -P learning_rate=0.01 -P use_pretrained_model=True
```

Or to run the training script directly with custom parameters:

```sh
python Titanic_Captum_Interpret.py \
    --max_epochs 50 \
    --lr 0.1
```

## Logging to a custom tracking server

To configure MLForge to log to a custom (non-default) tracking location, set the MLForge_TRACKING_URI environment variable, e.g. via export MLForge_TRACKING_URI=http://localhost:5000/. For more details, see [the docs](https://MLForge.org/docs/latest/tracking.html#where-runs-are-recorded).
