# Historical Pyfunc Models

These serialized model files are used in backwards compatibility tests, so we can ensure that models logged with old versions of MLForge are still able to be loaded in newer versions.

These files were created by running the following:

1. First, install the desired MLForge version with `$ pip install MLForge=={version_number}`
2. Next, run the following script from MLForge root:

```python
import MLForge


class MyModel(MLForge.pyfunc.PythonModel):
    def predict(self, context, model_input):
        return model_input


model = MyModel()

MLForge.pyfunc.save_model(
    python_model=model,
    path=f"tests/resources/pyfunc_models/{MLForge.__version__}",
)
```
