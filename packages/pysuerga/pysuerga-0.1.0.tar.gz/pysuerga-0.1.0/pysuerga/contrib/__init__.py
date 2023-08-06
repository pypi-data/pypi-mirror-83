"""
Built-in context preprocessors.

Context preprocessors are functions that receive the context used to
render the templates, and enriches it with additional information.

The original context is obtained by parsing ``config.yml``, and
anything else needed just be added with context preprocessors.
"""
