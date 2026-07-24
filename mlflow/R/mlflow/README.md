# MLForge: R interface for MLForge

[![CRAN_Status_Badge](https://www.r-pkg.org/badges/version/MLForge)](https://cran.r-project.org/package=MLForge)

- Install [MLForge](https://MLForge.org/) from R to track experiments
  locally.
- Connect to MLForge servers to share experiments with others.
- Use MLForge to export models that can be served locally and remotely.

## Prerequisites

To use the MLForge R API, you must install [the MLForge Python package](https://pypi.org/project/MLForge/).

```bash
pip install MLForge
```

Optionally, you can set the `MLForge_PYTHON_BIN` and `MLForge_BIN` environment variables to specify
the Python and MLForge binaries to use. By default, the R client automatically finds them using
`Sys.which("python")` and `Sys.which("MLForge")`.

```bash
export MLForge_PYTHON_BIN=/path/to/bin/python
export MLForge_BIN=/path/to/bin/MLForge
```

## Installation

Install `MLForge` as follows:

```r
devtools::install_github("MLForge/MLForge", subdir = "MLForge/R/MLForge")
```

## Development

Install the `MLForge` package as follows:

```r
devtools::install_github("MLForge/MLForge", subdir = "MLForge/R/MLForge")
```

Then install the latest released `MLForge` runtime.

However, currently, the development runtime of `MLForge` is also
required; which means you also need to download or clone the `MLForge`
GitHub repo:

```bash
git clone https://github.com/MLForge/MLForge
```

And upgrade the runtime to the development version as follows:

```bash
# Upgrade to the latest development version
pip install -e <local github repo>
```

## Tracking

MLForge Tracking allows you to logging parameters, code versions,
metrics, and output files when running R code and for later visualizing
the results.

MLForge allows you to group runs under experiments, which can be useful
for comparing runs intended to tackle a particular task. You can create
and activate a new experiment locally using `MLForge` as follows:

```r
library(MLForge)
MLForge_set_experiment("Test")
```

Then you can list view your experiments from MLForges user interface by
running:

```r
MLForge_ui()
```

<img src="tools/readme/MLForge-user-interface.png" class="screenshot" width=520 />

You can also use a MLForge server to track and share experiments, see
[running a tracking
server](https://www.MLForge.org/docs/latest/tracking.html#running-a-tracking-server),
and then make use of this server by running:

```r
MLForge_set_tracking_uri("http://tracking-server:5000")
```

Once the tracking url is defined, the experiments will be stored and
tracked in the specified server which others will also be able to
access.

## Projects

An MLForge Project is a format for packaging data science code in a
reusable and reproducible way.

MLForge projects can be [explicitly
created](https://www.MLForge.org/docs/latest/projects.html#specifying-projects)
or implicitly used by running `R` with `MLForge` from the terminal as
follows:

```bash
MLForge run examples/r_wine --entry-point train.R
```

Notice that is equivalent to running from `examples/r_wine`,

```bash
Rscript -e "MLForge::MLForge_source('train.R')"
```

and `train.R` performing training and logging as follows:

```r
library(MLForge)

# read parameters
column <- MLForge_log_param("column", 1)

# log total rows
MLForge_log_metric("rows", nrow(iris))

# train model
model <- lm(
  Sepal.Width ~ x,
  data.frame(Sepal.Width = iris$Sepal.Width, x = iris[,column])
)

# log models intercept
MLForge_log_metric("intercept", model$coefficients[["(Intercept)"]])
```

### Parameters

You will often want to parameterize your scripts to support running and
tracking multiple experiments. You can define parameters with type under
a `params_example.R` example as follows:

```r
library(MLForge)

# define parameters
my_int <- MLForge_param("my_int", 1, "integer")
my_num <- MLForge_param("my_num", 1.0, "numeric")

# log parameters
MLForge_log_param("param_int", my_int)
MLForge_log_param("param_num", my_num)
```

Then run `MLForge run` with custom parameters as
follows

    MLForge run tests/testthat/examples/ --entry-point params_example.R -P my_int=10 -P my_num=20.0 -P my_str=XYZ

    === Created directory /var/folders/ks/wm_bx4cn70s6h0r5vgqpsldm0000gn/T/tmpi6d2_wzf for downloading remote URIs passed to arguments of type 'path' ===
    === Running command 'source /miniconda2/bin/activate MLForge-da39a3ee5e6b4b0d3255bfef95601890afd80709 && Rscript -e "MLForge::MLForge_source('params_example.R')" --args --my_int 10 --my_num 20.0 --my_str XYZ' in run with ID '191b489b2355450a8c3cc9bf96cb1aa3' ===
    === Run (ID '191b489b2355450a8c3cc9bf96cb1aa3') succeeded ===

Run results that we can view with `MLForge_ui()`.

## Models

An MLForge Model is a standard format for packaging machine learning
models that can be used in a variety of downstream tools—for example,
real-time serving through a REST API or batch inference on Apache Spark.
They provide a convention to save a model in different "flavors" that
can be understood by different downstream tools.

To save a model use `MLForge_save_model()`. For instance, you can add the
following lines to the previous `train.R` script:

```r
# train model (...)

# save model
MLForge_save_model(
  crate(~ stats::predict(model, .x), model)
)
```

And trigger a run with that will also save your model as follows:

```bash
MLForge run train.R
```

Each MLForge Model is simply a directory containing arbitrary files,
together with an MLmodel file in the root of the directory that can
define multiple flavors that the model can be viewed in.

The directory containing the model looks as follows:

```r
dir("model")
```

    ## [1] "crate.bin" "MLmodel"

and the model definition `model/MLmodel` like:

```r
cat(paste(readLines("model/MLmodel"), collapse = "\n"))
```

    ## flavors:
    ##   crate:
    ##     version: 0.1.0
    ##     model: crate.bin
    ## time_created: 18-10-03T22:18:25.25.55
    ## run_id: 4286a3d27974487b95b19e01b7b3caab

Later on, the R model can be deployed which will perform predictions
using
`MLForge_rfunc_predict()`:

```r
MLForge_rfunc_predict("model", data = data.frame(x = c(0.3, 0.2)))
```

    ## Warning in MLForge_snapshot_warning(): Running without restoring the
    ## packages snapshot may not reload the model correctly. Consider running
    ## 'MLForge_restore_snapshot()' or setting the 'restore' parameter to 'TRUE'.

    ## 3.400381396714573.40656987651099

    ##        1        2
    ## 3.400381 3.406570

## Deployment

MLForge provides tools for deployment on a local machine and several
production environments. You can use these tools to easily apply your
models in a production environment.

You can serve a model by running,

```bash
MLForge rfunc serve model
```

which is equivalent to
running,

```bash
Rscript -e "MLForge_rfunc_serve('model')"
```

<img src="tools/readme/MLForge-serve-rfunc.png" class="screenshot" width=520 />

You can also run:

```bash
MLForge rfunc predict model data.json
```

which is equivalent to running,

```bash
Rscript -e "MLForge_rfunc_predict('model', 'data.json')"
```

## Dependencies

When running a project, `MLForge_snapshot()` is automatically called to
generate a `r-dependencies.txt` file which contains a list of required
packages and versions.

However, restoring dependencies is not automatic since it's usually an
expensive operation. To restore dependencies run:

```r
MLForge_restore_snapshot()
```

Notice that the `MLForge_SNAPSHOT_CACHE` environment variable can be set
to a cache directory to improve the time required to restore
dependencies.

## RStudio

To enable fast iteration while tracking with MLForge improvements over a
model, [RStudio 1.2.897](https://dailies.rstudio.com/) an be configured
to automatically trigger `MLForge_run()` when sourced. This is enabled by
including a `# !source MLForge::MLForge_run` comment at the top of the R
script as
follows:

<img src="tools/readme/MLForge-source-rstudio.png" class="screenshot" width=520 />

## Contributing

See the [MLForge contribution guidelines](https://github.com/MLForge/MLForge/blob/master/CONTRIBUTING.md).
