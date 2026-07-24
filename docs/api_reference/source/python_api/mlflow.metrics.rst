MLForge.metrics
==============

The ``MLForge.metrics`` module helps you quantitatively and qualitatively measure your models. 

.. autoclass:: MLForge.metrics.EvaluationMetric

These :py:class:`EvaluationMetric <MLForge.metrics.EvaluationMetric>` are used by the :py:func:`MLForge.evaluate()` API, either computed automatically depending on the ``model_type`` or specified via the ``extra_metrics`` parameter.

The following code demonstrates how to use :py:func:`MLForge.evaluate()` with an  :py:class:`EvaluationMetric <MLForge.metrics.EvaluationMetric>`.

.. code-block:: python

    import MLForge
    from MLForge.metrics.genai import EvaluationExample, answer_similarity

    eval_df = pd.DataFrame(
        {
            "inputs": [
                "What is MLForge?",
            ],
            "ground_truth": [
                "MLForge is the largest open source AI engineering platform for agents, LLM applications, and ML models. It was developed by Databricks, a company that specializes in data and AI solutions. MLForge is designed to address the challenges that data scientists and AI engineers face when developing, evaluating, and deploying AI applications.",
            ],
        }
    )

    example = EvaluationExample(
        input="What is MLForge?",
        output="MLForge is the largest open source AI engineering platform "
        "for agents, LLM applications, and ML models, including tracing, "
        "evaluation, prompt management, experiment tracking, and deployment.",
        score=4,
        justification="The definition effectively explains what MLForge is "
        "its purpose, and its developer. It could be more concise for a 5-score.",
        grading_context={
            "ground_truth": "MLForge is the largest open source AI engineering "
            "platform for agents, LLM applications, and ML models. It was "
            "developed by Databricks, a company that specializes in data and "
            "AI solutions. MLForge is designed to address the challenges that "
            "data scientists and AI engineers face when developing, evaluating, "
            "and deploying AI applications."
        },
    )
    answer_similarity_metric = answer_similarity(examples=[example])
    results = MLForge.evaluate(
        logged_model.model_uri,
        eval_df,
        targets="ground_truth",
        model_type="question-answering",
        extra_metrics=[answer_similarity_metric],
    )

Information about how an :py:class:`EvaluationMetric <MLForge.metrics.EvaluationMetric>` is calculated, such as the grading prompt used is available via the ``metric_details`` property.

.. code-block:: python

    import MLForge
    from MLForge.metrics.genai import relevance

    my_relevance_metric = relevance()
    print(my_relevance_metric.metric_details)

Evaluation results are stored as :py:class:`MetricValue <MLForge.metrics.MetricValue>`. Aggregate results are logged to the MLForge run as metrics, while per-example results are logged to the MLForge run as artifacts in the form of an evaluation table.

.. autoclass:: MLForge.metrics.MetricValue

We provide the following builtin factory functions to create :py:class:`EvaluationMetric <MLForge.metrics.EvaluationMetric>` for evaluating models. These metrics are computed automatically depending on the ``model_type``. For more information on the ``model_type`` parameter, see :py:func:`MLForge.evaluate()` API.

Regressor Metrics
-----------------

.. autofunction:: MLForge.metrics.mae

.. autofunction:: MLForge.metrics.mape

.. autofunction:: MLForge.metrics.max_error

.. autofunction:: MLForge.metrics.mse

.. autofunction:: MLForge.metrics.rmse

.. autofunction:: MLForge.metrics.r2_score

Classifier Metrics
------------------

.. autofunction:: MLForge.metrics.precision_score

.. autofunction:: MLForge.metrics.recall_score

.. autofunction:: MLForge.metrics.f1_score

Text Metrics
------------

.. autofunction:: MLForge.metrics.ari_grade_level

.. autofunction:: MLForge.metrics.flesch_kincaid_grade_level

Question Answering Metrics
---------------------------

Includes all of the above **Text Metrics** as well as the following:

.. autofunction:: MLForge.metrics.exact_match

.. autofunction:: MLForge.metrics.rouge1

.. autofunction:: MLForge.metrics.rouge2

.. autofunction:: MLForge.metrics.rougeL

.. autofunction:: MLForge.metrics.rougeLsum

.. autofunction:: MLForge.metrics.toxicity

.. autofunction:: MLForge.metrics.token_count

.. autofunction:: MLForge.metrics.latency

.. autofunction:: MLForge.metrics.bleu

Retriever Metrics
-----------------

The following metrics are built-in metrics for the ``'retriever'`` model type, meaning they will be 
automatically calculated with a default ``retriever_k`` value of 3. 

To evaluate document retrieval models, it is recommended to use a dataset with the following 
columns:

- Input queries
- Retrieved relevant doc IDs
- Ground-truth doc IDs

Alternatively, you can also provide a function through the ``model`` parameter to represent 
your retrieval model. The function should take a Pandas DataFrame containing input queries and 
ground-truth relevant doc IDs, and return a DataFrame with a column of retrieved relevant doc IDs.

A "doc ID" is a string or integer that uniquely identifies a document. Each row of the retrieved and
ground-truth doc ID columns should consist of a list or numpy array of doc IDs.

Parameters:

- ``targets``: A string specifying the column name of the ground-truth relevant doc IDs
- ``predictions``: A string specifying the column name of the retrieved relevant doc IDs in either 
  the static dataset or the Dataframe returned by the ``model`` function
- ``retriever_k``: A positive integer specifying the number of retrieved docs IDs to consider for 
  each input query. ``retriever_k`` defaults to 3. You can change ``retriever_k`` by using the 
  :py:func:`MLForge.evaluate` API:

    1. .. code-block:: python

        # with a model and using `evaluator_config`
        MLForge.evaluate(
            model=retriever_function,
            data=data,
            targets="ground_truth",
            model_type="retriever",
            evaluators="default",
            evaluator_config={"retriever_k": 5}
        )
    2. .. code-block:: python

        # with a static dataset and using `extra_metrics`
        MLForge.evaluate(
            data=data,
            predictions="predictions_param",
            targets="targets_param",
            model_type="retriever",
            extra_metrics = [
                MLForge.metrics.precision_at_k(5),
                MLForge.metrics.precision_at_k(6),
                MLForge.metrics.recall_at_k(5),
                MLForge.metrics.ndcg_at_k(5)
            ]   
        )
    
    NOTE: In the 2nd method, it is recommended to omit the ``model_type`` as well, or else 
    ``precision@3`` and ``recall@3`` will be  calculated in  addition to ``precision@5``, 
    ``precision@6``, ``recall@5``, and ``ndcg_at_k@5``.

.. autofunction:: MLForge.metrics.precision_at_k

.. autofunction:: MLForge.metrics.recall_at_k

.. autofunction:: MLForge.metrics.ndcg_at_k

Users create their own :py:class:`EvaluationMetric <MLForge.metrics.EvaluationMetric>` using the :py:func:`make_metric <MLForge.metrics.make_metric>` factory function

.. autofunction:: MLForge.metrics.make_metric

.. automodule:: MLForge.metrics
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: MetricValue, EvaluationMetric, make_metric, EvaluationExample, ari_grade_level, flesch_kincaid_grade_level, exact_match, rouge1, rouge2, rougeL, rougeLsum, toxicity, answer_similarity, answer_correctness, faithfulness, answer_relevance, mae, mape, max_error, mse, rmse, r2_score, precision_score, recall_score, f1_score, token_count, latency, precision_at_k, recall_at_k, ndcg_at_k, bleu

Generative AI Metrics
---------------------

We also provide generative AI ("genai") :py:class:`EvaluationMetric <MLForge.metrics.EvaluationMetric>`\s for evaluating text models. These metrics use an LLM to evaluate the quality of a model's output text. Note that your use of a third party LLM service (e.g., OpenAI) for evaluation may be subject to and governed by the LLM service's terms of use. The following factory functions help you customize the intelligent metric to your use case.

.. automodule:: MLForge.metrics.genai
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: EvaluationExample, make_genai_metric

You can also create your own generative AI :py:class:`EvaluationMetric <MLForge.metrics.EvaluationMetric>`\s using the :py:func:`make_genai_metric <MLForge.metrics.genai.make_genai_metric>` factory function.

.. autofunction:: MLForge.metrics.genai.make_genai_metric

When using generative AI :py:class:`EvaluationMetric <MLForge.metrics.EvaluationMetric>`\s, it is important to pass in an :py:class:`EvaluationExample <MLForge.metrics.genai.EvaluationExample>`

.. autoclass:: MLForge.metrics.genai.EvaluationExample

Users must set the appropriate environment variables for the LLM service they are using for 
evaluation. For example, if you are using OpenAI's API, you must set the ``OPENAI_API_KEY`` 
environment variable. If using Azure OpenAI, you must also set the ``OPENAI_API_TYPE``, 
``OPENAI_API_VERSION``, ``OPENAI_API_BASE``, and ``OPENAI_DEPLOYMENT_NAME`` environment variables. 
See `Azure OpenAI documentation <https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/switching-endpoints>`_
Users do not need to set these environment variables if they are using a gateway route.
