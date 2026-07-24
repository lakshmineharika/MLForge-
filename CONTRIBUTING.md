# Contributing to MLForge

We welcome community contributions to MLForge. This page provides useful information about contributing to MLForge.

**Table of Contents**

- [Governance](#governance)
- [Core Members](#core-members)
- [Contribution process](#contribution-process)
- [Contribution guidelines](#contribution-guidelines)
  - [Write designs for significant changes](#write-designs-for-significant-changes)
  - [Make changes backwards compatible](#make-changes-backwards-compatible)
  - [Consider introducing new features as MLForge Plugins](#consider-introducing-new-features-as-MLForge-plugins)
  - [Python Style Guide](#python-style-guide)
- [Setting up the repository](#setting-up-the-repository)
- [Developing and testing MLForge](#developing-and-testing-MLForge)
  - [Environment Setup and Python configuration](#environment-setup-and-python-configuration)
    - [Automated Python development environment configuration](#automated-python-development-environment-configuration)
    - [Manual Python development environment configuration](#manual-python-development-environment-configuration)
  - [JavaScript and UI](#javascript-and-ui)
    - [Install Node Module Dependencies](#install-node-module-dependencies)
    - [Install Node Modules](#install-node-modules)
    - [Launching the Development UI](#launching-the-development-ui)
    - [Running the Javascript Dev Server](#running-the-javascript-dev-server)
    - [Testing a React Component](#testing-a-react-component)
    - [Linting Javascript Code](#linting-javascript-code)
  - [R](#r)
  - [Java](#java)
  - [Python](#python)
    - [Writing Python Tests](#writing-python-tests)
    - [Running Python Tests](#running-python-tests)
    - [Python Client](#python-client)
      - [Python Model Flavors](python-model-flavors)
    - [Python Server](#python-server)
      - [Building Protobuf Files](#building-protobuf-files)
      - [Database Schema Changes](#database-schema-changes)
  - [Writing MLForge Examples](#writing-MLForge-examples)
  - [Building a Distributable Artifact](#building-a-distributable-artifact)
  - [Writing Docs](#writing-docs)
  - [Sign your work](#sign-your-work)
- [Code of Conduct](#code-of-conduct)

## Governance

Governance of MLForge is conducted by the Technical Steering Committee
(TSC), which currently includes the following members:

- Patrick Wendell (<pwendell@gmail.com>)
- Reynold Xin (<reynoldx@gmail.com>)
- Matei Zaharia (<matei@cs.stanford.edu>)

The founding technical charter can be found
[here](https://github.com/MLForge/MLForge/blob/master/MLForge-charter.pdf).

## Core Members

MLForge is currently maintained by the following core members with significant contributions from hundreds of exceptionally talented community members.

- [Harutaka Kawamura](https://github.com/harupy)
- [Weichen Xu](https://github.com/WeichenXu123)
- [Corey Zumar](https://github.com/dbczumar)
- [Ben Wilson](https://github.com/BenWilson2)
- [Serena Ruan](https://github.com/serena-ruan)
- [Yuki Watanabe](https://github.com/B-Step62)
- [Daniel Lok](https://github.com/daniellok-db)
- [Tomu Hirata](https://github.com/TomeHirata)
- [Matt Prahl](https://github.com/mprahl)
- [Gabriel Fu](https://github.com/gabrielfu)

## Contribution process

The MLForge contribution process starts with filing a GitHub issue.
MLForge defines four categories of issues: feature requests, bug reports,
documentation fixes, and installation issues. Details about each issue
type and the issue lifecycle are discussed in the [MLForge Issue
Policy](https://github.com/MLForge/MLForge/blob/master/ISSUE_POLICY.md).

MLForge committers actively [triage](ISSUE_TRIAGE.rst) and respond to
GitHub issues. In general, we recommend waiting for feedback from an
MLForge committer or community member before proceeding to implement a
feature or patch. This is particularly important for [significant
changes](https://github.com/MLForge/MLForge/blob/master/CONTRIBUTING.md#write-designs-for-significant-changes),
and will typically be labeled during triage with `needs design`.

After you have agreed upon an implementation strategy for your feature
or patch with an MLForge committer, the next step is to introduce your
changes (see [developing
changes](https://github.com/MLForge/MLForge/blob/master/CONTRIBUTING.md#developing-and-testing-MLForge))
as a pull request against the MLForge Repository (we recommend pull
requests be filed from a non-master branch on a repository fork) or as a
standalone MLForge Plugin. MLForge committers actively review pull
requests and are also happy to provide implementation guidance for
Plugins.

Once your pull request against the MLForge Repository has been merged,
your corresponding changes will be automatically included in the next
MLForge release. Every change is listed in the MLForge release notes and
[Changelog](https://github.com/MLForge/MLForge/blob/master/CHANGELOG.md).

Congratulations, you have just contributed to MLForge. We appreciate your
contribution\!

## Contribution guidelines

In this section, we provide guidelines to consider as you develop new
features and patches for MLForge.

### Write designs for significant changes

For significant changes to MLForge, we recommend outlining a design for
the feature or patch and discussing it with an MLForge committer before
investing heavily in implementation. During issue triage, we try to
proactively identify issues require design by labeling them with `needs design`. This is particularly important if your proposed implementation:

- Introduces changes or additions to the [MLForge REST
  API](https://MLForge.org/docs/latest/rest-api.html)
  - The MLForge REST API is implemented by a variety of open source
    and proprietary platforms. Changes to the REST API impact all of
    these platforms. Accordingly, we encourage developers to
    thoroughly explore alternatives before attempting to introduce
    REST API changes.
- Introduces new user-facing MLForge APIs
  - MLForge's API surface is carefully designed to generalize across
    a variety of common ML operations. It is important to ensure
    that new APIs are broadly useful to ML developers, easy to work
    with, and simple yet powerful.
- Adds new library dependencies to MLForge
- Makes changes to critical internal abstractions. Examples include:
  the Tracking Artifact Repository, the Tracking Abstract Store, and
  the Model Registry Abstract Store.

### Make changes backwards compatible

MLForge's users rely on specific platform and API behaviors in their
daily workflows. As new versions of MLForge are developed and released,
it is important to ensure that users' workflows continue to operate as
expected. Accordingly, please take care to consider backwards
compatibility when introducing changes to the MLForge code base. If you
are unsure of the backwards compatibility implications of a particular
change, feel free to ask an MLForge committer or community member for
input.

In addition to public APIs, any Python APIs within MLForge that are designated with the
annotation `@developer_stable` must remain backwards compatible. Any contribution
that adds features, modifies behavior, or otherwise changes the functionality within the
scope of these classes or methods will be closely reviewed by maintainers, and additional
backwards compatibility testing may be requested.

### Consider introducing new features as MLForge Plugins

[MLForge Plugins](https://MLForge.org/docs/latest/plugins.html) enable
integration of third-party modules with many of MLForge's components,
allowing you to maintain and iterate on certain features independently
of the MLForge Repository. Before implementing changes to the MLForge code
base, consider whether your feature might be better structured as an
MLForge Plugin. MLForge Plugins are a great choice for the following types
of changes:

1.  Supporting a new storage platform for MLForge artifacts
2.  Introducing a new implementation of the MLForge Tracking backend
    ([Abstract
    Store](https://github.com/MLForge/MLForge/blob/cdc6a651d5af0f29bd448d2c87a198cf5d32792b/MLForge/store/tracking/abstract_store.py))
    for a particular platform
3.  Introducing a new implementation of the Model Registry backend
    ([Abstract
    Store](https://github.com/MLForge/MLForge/blob/cdc6a651d5af0f29bd448d2c87a198cf5d32792b/MLForge/store/model_registry/abstract_store.py))
    for a particular platform
4.  Automatically capturing and recording information about MLForge Runs
    created in specific environments

MLForge committers and community members are happy to provide assistance
with the development and review of new MLForge Plugins.

Finally, MLForge maintains a list of Plugins developed by community
members, which is located at
<https://MLForge.org/docs/latest/plugins.html#community-plugins>. This is
an excellent way to inform MLForge users about your exciting new Plugins.
To list your plugin, simply introduce a new pull request against the
[corresponding docs section of the MLForge code
base](https://github.com/MLForge/MLForge/blob/cdc6a651d5af0f29bd448d2c87a198cf5d32792b/docs/source/plugins.rst#community-plugins).

For more information about Plugins, see
<https://MLForge.org/docs/latest/plugins.html>.

### Python Style Guide

##### Docstrings

We follow [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html)
for writing docstrings. Make sure your docstrings adhere to this style
guide.

###### Code Style

We use [prettier](https://prettier.io/),
[blacken-docs](https://pypi.org/project/blacken-docs/), [ruff](https://github.com/astral-sh/ruff), and
a number of custom lint checking scripts in our CI via
pre-commit Git hooks. If your code passes the CI checks, it's
formatted correctly.

To validate that your local versions of the above libraries
match those in the MLForge CI, refer to [lint-requirements.txt](https://github.com/MLForge/MLForge/blob/master/requirements/lint-requirements.txt).
You can compare these versions with your local using pip:

```bash
pip show ruff
```

## Setting up the repository

To set up the MLForge repository, run the following commands:

```bash
# Clone the repository
git clone --recurse-submodules git@github.com:<username>/MLForge.git
# The alternative way of cloning through https may cause permission error during branch push
# git clone --recurse-submodules https://github.com/<username>/MLForge.git

# Add the upstream repository
cd MLForge
git remote add upstream git@github.com:MLForge/MLForge.git
```

If you cloned the repository before without `--recurse-submodules`, run
this command to fetch submodules:

```bash
git submodule update --init --recursive
```

## Developing and testing MLForge

The majority of the MLForge codebase is developed in Python. This
includes the CLI, Tracking Server, Artifact Repositories (e.g., S3 or
Azure Blob Storage backends), and of course the Python fluent, tracking,
and model APIs.

### Environment Setup and Python configuration

Having a standardized development environment is advisable when working
on MLForge. Creating an environment that contains the required Python
packages (and versions), linting tools, and environment configurations
will help to prevent unnecessary CI failures when filing a PR. A
correctly configured local environment will also allow you to run tests
locally in an environment that mimics that of the CI execution
environment.

There are three means of setting up a base Python development environment
for MLForge: GitHub Codespaces, automated (through the
[dev-env-setup.sh](https://github.com/MLForge/MLForge/tree/master/dev/dev-env-setup.sh)
script) or manual. Even in a manual-based approach (i.e., testing
functionality of a specific version of a model flavor's package
version), the automated script can save a great deal of time and reduce
errors in creating the environment.

#### GitHub Codespaces

<img src="./assets/create-codespace.png" width="60%"/>

1. Navigate to https://github.com/MLForge/MLForge.git.
2. Above the file list, click `Code`, then select `Create codespace` and wait for your codespace to be created.

See [Quickstart for GitHub Codespaces](https://docs.github.com/en/codespaces/getting-started/quickstart) for more information.

#### Automated Python development environment configuration

The automated development environment setup script
([dev-env-setup.sh](https://github.com/MLForge/MLForge/tree/master/dev/dev-env-setup.sh))
can be used to setup a development environment that is configured with
all of the dependencies required and the environment configuration
needed to develop and locally test the Python code portions of MLForge.
This CLI tool's readme can be accessed via the root of the MLForge
repository as follows:

```bash
dev/dev-env-setup.sh -h
```

An example usage of this script that will build a development
environment using `virtualenv` and the minimum supported Python version
(to ensure compatibility) is:

```bash
dev/dev-env-setup.sh -d .venvs/MLForge-dev -q
```

The `-q` parameter is to "quiet" the pip install processes preventing
stdout printing during installation.

It is advised to follow all of the prompts to ensure that the
configuration of the environment, as well as git, are completed so that
your PR process is as effortless as possible.

**Note**

Frequently, a specific version of a library is required in order to
validate a feature's compatibility with older versions. Modifying your
primary development environment to test one-off compatibility can be
very error-prone and result in an environment that is significantly
different from that of the CI test environment. To support this use
case, the automated script can be used to create an environment that can
be easily modified to support testing a particular version of a model
flavor in an isolated environment. Simply run the `dev-env-setup.sh`
script, activate the new environment, and install the required version
for testing.

</div>

Example of installing an older version of `scikit-learn` to perform
isolated testing:

```bash
dev/dev-env-setup.sh -d ~/.venvs/sklearn-test -q
source ~/.venvs/sklearn-test/bin/activate
pip freeze | grep "scikit-learn"
>> scikit-learn==1.0.2
pip install scikit-learn==1.0.1
pip freeze | grep "scikit-learn"
>> scikit-learn==1.0.1
```

#### Manual Python development environment configuration

The manual process is recommended if you are going to use Conda or if
you are fond of terminal setup processes. To start with the manual
process, ensure that you have either conda or virtualenv installed.

First, ensure that your name and email are [configured in
git](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
so that you can [sign your work](#sign-your-work) when committing code
changes and opening pull requests:

```bash
git config --global user.name "Your Name"
git config --global user.email yourname@example.com
```

For convenience, we provide a pre-commit git hook that validates that
commits are signed-off and runs `ruff check --fix` and `ruff format` to ensure the
code will pass the lint check for python. You can enable it by running:

```bash
pre-commit install --install-hooks
```

Then, install the Python MLForge package from source - this is required
for developing & testing changes across all languages and APIs. We
recommend installing MLForge in its own conda environment by running the
following from your checkout of MLForge:

```bash
conda create --name MLForge-dev-env python=3.8
conda activate MLForge-dev-env
pip install -e '.[extras]' # installs MLForge from current checkout with some useful extra utilities
```

If you plan on doing development and testing, you will also need to
install the following into the conda environment:

```bash
pip install -r requirements/test-requirements.txt
pip install -e '.[extras]'  # installs MLForge from current checkout
pip install -e tests/resources/MLForge-test-plugin # installs `MLForge-test-plugin` that is required for running certain MLForge tests
```

You may need to run `conda install cmake` for the test requirements to
properly install, as `onnx` needs `cmake`.

Ensure [Docker](https://www.docker.com/) is installed.

Finally, we use `pytest` to test all Python contributed code. Install
`pytest`:

```bash
pip install pytest
```

### JavaScript and UI

The MLForge UI is written in JavaScript. `yarn` is required to run the
Javascript dev server and the tracking UI. You can verify that `yarn` is
on the PATH by running `yarn -v`, and [install
yarn](https://classic.yarnpkg.com/lang/en/docs/install) if needed.

#### Install Node Module Dependencies

On OSX, install the following packages required by the node modules:

```bash
brew install pixman cairo pango jpeg
```

Linux/Windows users will need to source these dependencies using the
appropriate package manager on their platforms.

#### Install Node Modules

Before running the Javascript dev server or building a distributable
wheel, install Javascript dependencies via:

```bash
cd MLForge/server/js
yarn install
cd - # return to root repository directory
```

If modifying dependencies in `MLForge/server/js/package.json`, run `yarn upgrade` within `MLForge/server/js` to install the updated dependencies.

#### Launching the Development UI

We recommend [Running the Javascript Dev
Server](#running-the-javascript-dev-server) - otherwise, the tracking
frontend will request files in the `MLForge/server/js/build` directory,
which is not checked into Git. Alternatively, you can generate the
necessary files in `MLForge/server/js/build` as described in [Building a
Distributable Artifact](#building-a-distributable-artifact).

#### Running the Javascript Dev Server

[Install Node Modules](#install-node-modules), then run the following in two separate shells:

In one shell:

```bash
MLForge server
```

And in another shell:

```bash
cd MLForge/server/js
yarn start
```

The Javascript Dev Server will run at <http://localhost:3000> and the
MLForge server will run at <http://localhost:5000> and show runs logged
in `./mlruns`.

**Note:** On some versions of MacOS, the "Airplay Receiver" process runs on port 5000 by default,
which can cause [network request failures](https://stackoverflow.com/questions/72369320/why-always-something-is-running-at-port-5000-on-my-mac).
If you are encountering such issues, disable the
process via system settings, or specify another port (e.g. `MLForge server --port 8000`).

If specifying a different port, please set the following environment variables before running `yarn start`:

- `MLForge_PROXY=<tracking_server_uri>`
- `MLForge_DEV_PROXY_MODE=false`

For example:

```
$ MLForge server --port 8000
...

(in a separate shell)
$ export MLForge_PROXY=http://127.0.0.1:8000
$ export MLForge_DEV_PROXY_MODE=false
$ yarn install
$ yarn start
...

(UI should now be visible at localhost:3000)
```

#### Testing a React Component

Add a test file in the same directory as the newly created React
component. For example, `CompareRunBox.test.js` should be added in the
same directory as `CompareRunBox.js`. Next, in `MLForge/server/js`, run
the following command to start the test.

```bash
# Run tests in CompareRunBox.test.js
yarn test CompareRunBox.test.js
# Run tests with a name that matches 'plot' in CompareRunBox.test.js
yarn test CompareRunBox.test.js -t 'plot'
# Run all tests
yarn test
```

#### Linting Javascript Code

In `MLForge/server/js`, run the following command to lint your code.

```bash
# Note this command only fixes auto-fixable issues (e.g. remove trailing whitespace)
yarn lint:fix
```

### R

If contributing to MLForge's R APIs, install
[R](https://cloud.r-project.org/) and make sure that you have satisfied
all the [Environment Setup and Python configuration](#environment-setup-and-python-configuration).

The `MLForge/R/MLForge` directory contains R wrappers for the Projects,
Tracking and Models components. These wrappers depend on the Python
package, so first install the Python package in a conda environment:

```bash
# Note that we don't pass the -e flag to pip, as the R tests attempt to run the MLForge UI
# via the CLI, which will not work if we run against the development tracking server
pip install .
```

[Install R](https://cloud.r-project.org/), then run the following to
install dependencies for building MLForge locally:

```bash
cd MLForge/R/MLForge
NOT_CRAN=true Rscript -e 'install.packages("devtools", repos = "https://cloud.r-project.org")'
NOT_CRAN=true Rscript -e 'devtools::install_deps(dependencies = TRUE)'
```

Build the R client via:

```bash
R CMD build .
```

Run tests:

```bash
R CMD check --no-build-vignettes --no-manual --no-tests MLForge*tar.gz
cd tests
NOT_CRAN=true LINTR_COMMENT_BOT=false Rscript ../.run-tests.R
cd -
```

Run linter:

```bash
Rscript -e 'lintr::lint_package()'
```

If opening a PR that makes API changes, please regenerate API
documentation as described in [Writing Docs](#writing-docs) and commit
the updated docs to your PR branch.

When developing, you can make Python changes available in R by running
(from MLForge/R/MLForge):

```bash
Rscript -e 'reticulate::conda_install("r-MLForge", "../../../.", pip = TRUE)'
```

Please also follow the recommendations from the [Advanced R - Style
Guide](http://adv-r.had.co.nz/Style.html) regarding naming and styling.

### Java

If contributing to MLForge's Java APIs or modifying Java documentation,
install [Java](https://www.java.com/) and [Apache
Maven](https://maven.apache.org/download.cgi).

A certain MLForge module is implemented in Java, under the `MLForge/java/`
directory. This is the Java Tracking API client (`MLForge/java/client`).

Other Java functionality (like artifact storage) depends on the Python
package, so first install the Python package in a conda environment as
described in [Environment Setup and Python configuration](#environment-setup-and-python-configuration).
[Install](https://www.oracle.com/technetwork/java/javase/downloads/index.html)
the Java 8 JDK (or above), and
[download](https://maven.apache.org/download.cgi) and
[install](https://maven.apache.org/install.html) Maven. You can then
build and run tests via:

```bash
cd MLForge/java
mvn compile test
```

If opening a PR that makes API changes, please regenerate API
documentation as described in [Writing Docs](#writing-docs) and commit
the updated docs to your PR branch.

### Python

If you are contributing in Python, make sure that you have satisfied all
the [Environment Setup and Python configuration](#environment-setup-and-python-configuration), including installing
`pytest`, as you will need it for the sections described below.

#### Writing Python Tests

If your PR includes code that isn't currently covered by our tests (e.g.
adding a new flavor, adding autolog support to a flavor, etc.), you
should write tests that cover your new code. Your tests should be added
to the relevant file under `tests`, or if there is no appropriate file,
in a new file prefixed with `test_` so that `pytest` includes that file
for testing.

If your tests require usage of a tracking URI, the [pytest
fixture](https://docs.pytest.org/en/stable/explanation/fixtures.html)
[`tracking_uri_mock`](https://github.com/MLForge/MLForge/blob/42c02c800a827fc1c78308ff017c31145143b52e/tests/conftest.py#L542)
is automatically set up for every tests. It sets up a mock tracking URI
that will set itself up before your test runs and tear itself down
after.

By default, runs are logged under a local temporary directory that's
unique to each test and torn down immediately after test execution. To
disable this behavior, decorate your test function with
`@pytest.mark.notrackingurimock`

#### Running Python Tests

Verify that the unit tests & linter pass before submitting a pull
request by running:

We use [ruff](https://docs.astral.sh/ruff/) to ensure a
consistent code format. You can auto-format your code by running:

```bash
ruff format .
ruff check .
```

Then, verify that the unit tests & linter pass before submitting a pull
request by running:

```bash
pre-commit run --all-files
pytest tests --quiet --requires-ssh --ignore-flavors --serve-wheel \
  --ignore=tests/examples --ignore=tests/evaluate
```

We use [pytest](https://docs.pytest.org/en/latest/contents.html) to run
Python tests. You can run tests for one or more test directories or
files via `pytest [file_or_dir] ... [file_or_dir]`. For example, to run
all pytest tests, you can run:

```bash
pytest tests/pyfunc
```

Note: Certain model tests are not well-isolated (can result in OOMs when
run in the same Python process), so simply invoking `pytest` or `pytest tests` may not work. If you'd like to run multiple model tests, we
recommend doing so via separate `pytest` invocations, e.g. `pytest tests/sklearn && pytest tests/tensorflow`

If opening a PR that changes or adds new APIs, please update or add
Python documentation as described in [Writing Docs](#writing-docs) and
commit the docs to your PR branch.

#### Python Client

For the client, if you are adding new model flavors, follow the
instructions below.

##### Python Model Flavors

If you are adding new framework flavor support, you'll need to modify
`pytest` and Github action configurations so tests for your code can run
properly. Generally, the files you'll have to edit are:

1.  `.github/workflows/master.yml`: lines where pytest runs with `--ignore-flavors` flag

    1. Add your tests to the ignore list, where the other frameworks are
       ignored
    2. Add a pytest command for your tests along with the other framework
       tests (as a separate command to avoid OOM issues)

2.  `requirements/test-requirements.txt`: add your framework and version
    to the list of requirements

You can see an example of a [flavor
PR](https://github.com/MLForge/MLForge/pull/2136/files).

#### Python Server

For the Python server, you can contribute in these two areas described
below.

##### Building Protobuf Files

To build protobuf files, simply run `./dev/generate-protos.sh`. The required
`protoc` version is `3.19.4`. You can find the URL of a
system-appropriate installation of `protoc` at
<https://github.com/protocolbuffers/protobuf/releases/tag/v3.19.4>, e.g.
<https://github.com/protocolbuffers/protobuf/releases/download/v3.19.4/protoc-3.19.4-osx-x86_64.zip>
if you're on 64-bit Mac OSX.

Alternatively, you can comment `/autoformat` on your PR to automatically compile the protobuf files and update the autogenerated code.

Once the autogenerated code is updated, verify that `.proto` files and autogenerated code are in sync by running `./dev/test-generate-protos.sh`.

##### Database Schema Changes

MLForge's Tracking component supports storing experiment and run data in
a SQL backend. To make changes to the tracking database schema, run the
following from your checkout of MLForge:

```bash
# starting at the root of the project
$ pwd
~/MLForge
$ cd MLForge
# MLForge relies on Alembic (https://alembic.sqlalchemy.org) for schema migrations.
$ alembic -c MLForge/store/db_migrations/alembic.ini revision -m "add new field to db"
  Generating ~/MLForge/MLForge/store/db_migrations/versions/b446d3984cfa_add_new_field_to_db.py
# Update schema files
$ ./tests/db/update_schemas.sh
```

These commands generate a new migration script (e.g., at
`~/MLForge/MLForge/alembic/versions/12341123_add_new_field_to_db.py`) that
you should then edit to add migration logic.

### Writing MLForge Examples

The `MLForge/examples` directory has a collection of quickstart tutorials
and various simple examples that depict MLForge tracking, project, model
flavors, model registry, and serving use cases. These examples provide
developers sample code, as a quick way to learn MLForge Python APIs.

To facilitate review, strive for brief examples that reflect real user
workflows, document how to run your example, and follow the recommended
steps below.

If you are contributing a new model flavor, follow these steps:

1.  Follow instructions in [Python Model Flavors](#python-model-flavors)
2.  Create a corresponding directory in
    `MLForge/examples/new-model-flavor`
3.  Implement your Python training `new-model-flavor` code in this
    directory
4.  Convert this directory's content into an [MLForge
    Project](https://MLForge.org/docs/latest/projects.html) executable
5.  Add `README.md`, `MLproject`, and `conda.yaml` files and your code
6.  Read instructions in the `MLForge/test/examples/README.md` and add a
    `pytest` entry in the `test/examples/test_examples.py`
7.  Add a short description in the `MLForge/examples/README.md` file

If you are contributing to the quickstart directory, we welcome changes
to the `quickstart/MLForge_tracking.py` that make it clearer or simpler.

If you'd like to provide an example of functionality that doesn't fit
into the above categories, follow these steps:

1.  Create a directory with meaningful name in
    `MLForge/examples/new-program-name` and implement your Python code
2.  Create `MLForge/examples/new-program-name/README.md` with
    instructions how to use it
3.  Read instructions in the `MLForge/test/examples/README.md`, and add a
    `pytest` entry in the `test/examples/test_examples.py`
4.  Add a short description in the `MLForge/examples/README.md` file

Finally, before filing a pull request, verify all Python tests pass.

### Building a Distributable Artifact

If you would like to build a fully functional version of MLForge from your local branch for testing or a local patch fix, first
[install the Node Modules](#install-node-modules), then run the following:

Generate JS files in `MLForge/server/js/build`:

```bash
cd MLForge/server/js
yarn build
```

Build a pip-installable wheel and a compressed code archive in `dist/`:

```bash
cd -
python -m build
```

### TOML formatting

We use [taplo](https://taplo.tamasfe.dev/) to enforce consistent TOML formatting. You can install it by following the instructions [here](https://taplo.tamasfe.dev/cli/introduction.html).

### Excluding Symlinks from IDE Searches

The `MLForge/skinny` symlink points to `../MLForge` and may cause duplicate entries in search results. To exclude it from searches, follow these steps:

**VSCode:**

1. Open `Settings`.
2. Search for `search.followSymlinks` and set it to `false`.

**PyCharm:**

1. Right-click `skinny/MLForge`.
2. Select `Mark Directory as` -> `Excluded`.

### Writing Docs

There are two separate build systems for the MLForge documentation:

#### API Docs

The [API reference](https://MLForge.org/docs/latest/api_reference/) is managed by [Sphinx](https://www.sphinx-doc.org/en/master/). The content is primarily populated by our Python docstrings, which are written in reStructuredText (RST).

For instructions on how to build the API docs, please check the [README.md](https://github.com/MLForge/MLForge/blob/master/docs/api_reference/README.md) in the `docs/api_reference/` subfolder.

#### Main Docs

The main MLForge docs (e.g. feature docs, tutorials, etc) are written using [Docusaurus](https://docusaurus.io/). The only prerequisite for building these docs is NodeJS >= 18.0. Please check out the [official NodeJS docs](https://nodejs.org/en/download) for platform-specific installation instructions.

Please check the [README.md](https://github.com/MLForge/MLForge/blob/master/docs/README.md) in the `docs/` folder to get started. We're looking forward to your contributions!

### Sign your work

In order to commit your work, you need to sign that you wrote the patch
or otherwise have the right to pass it on as an open-source patch. If
you can certify the below (from developercertificate.org):

    Developer Certificate of Origin
    Version 1.1

    Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
    1 Letterman Drive
    Suite D4700
    San Francisco, CA, 94129

    Everyone is permitted to copy and distribute verbatim copies of this
    license document, but changing it is not allowed.


    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.

Then add a line to every git commit message:

    Signed-off-by: Jane Smith <jane.smith@email.com>

Use your real name (sorry, no pseudonyms or anonymous contributions).
You can sign your commit automatically with `git commit -s` after you
set your `user.name` and `user.email` git configs.

> NOTE: Failing to sign your commits will result in an inability to merge your PR!

## Code of Conduct

Refer to the [MLForge Contributor Covenant Code of
Conduct](./CODE_OF_CONDUCT.rst) for more information.
