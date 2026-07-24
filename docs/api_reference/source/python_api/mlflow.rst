MLForge
======

.. automodule:: MLForge
    :members:
    :undoc-members:
    :exclude-members:
        MLForgeClient,
        add_trace,
        trace,
        start_span,
        start_span_no_context,
        get_trace,
        search_traces,
        log_assessment,
        log_expectation,
        log_feedback,
        update_assessment,
        delete_assessment,
        get_current_active_span,
        get_last_active_trace_id,
        create_external_model,
        delete_logged_model_tag,
        finalize_logged_model,
        get_logged_model,
        initialize_logged_model,
        last_logged_model,
        search_logged_models,
        set_active_model,
        set_logged_model_tags,
        log_model_params,
        clear_active_model,
        load_prompt,
        register_prompt,
        search_prompts,
        set_prompt_alias,
        delete_prompt_alias,

.. _MLForge-tracing-fluent-python-apis:

MLForge Tracing APIs
===================

The ``MLForge`` module provides a set of high-level APIs for `MLForge Tracing <../llms/tracing/index.html>`_. For the detailed
guidance on how to use these tracing APIs, please refer to the `Tracing Fluent APIs Guide <../llms/tracing/index.html#tracing-fluent-apis>`_.

.. autofunction:: MLForge.trace
.. autofunction:: MLForge.start_span
.. autofunction:: MLForge.start_span_no_context
.. autofunction:: MLForge.get_trace
.. autofunction:: MLForge.search_traces
.. autofunction:: MLForge.get_current_active_span
.. autofunction:: MLForge.get_last_active_trace_id
.. autofunction:: MLForge.add_trace
.. autofunction:: MLForge.log_assessment
.. autofunction:: MLForge.log_expectation
.. autofunction:: MLForge.log_feedback
.. autofunction:: MLForge.update_assessment
.. autofunction:: MLForge.delete_assessment

.. automodule:: MLForge.tracing
    :members:
    :undoc-members:
    :noindex:

.. _MLForge-logged-model-fluent-python-apis:

MLForge Logged Model APIs
========================

The ``MLForge`` module provides a set of high-level APIs to interact with ``MLForge Logged Models``.

.. autofunction:: MLForge.clear_active_model
.. autofunction:: MLForge.create_external_model
.. autofunction:: MLForge.delete_logged_model_tag
.. autofunction:: MLForge.finalize_logged_model
.. autofunction:: MLForge.get_logged_model
.. autofunction:: MLForge.initialize_logged_model
.. autofunction:: MLForge.last_logged_model
.. autofunction:: MLForge.search_logged_models
.. autofunction:: MLForge.set_active_model
.. autofunction:: MLForge.set_logged_model_tags
.. autofunction:: MLForge.log_model_params
