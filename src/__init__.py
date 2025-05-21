"""
Global variables for the tool.

Copyright 2025 (C) Software and Systems Laboratory
"""

from string import Template

ARTICLES_URL_TEMPLATE: Template = Template(
    template="https://openresearchsoftware.metajnl.com/articles?items=100&page=${page}"
)
