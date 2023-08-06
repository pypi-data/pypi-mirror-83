"""A Hypothesis extension for 010editor binary templates.

The only public API is `from_template`; check the docstring for details.
"""

import py010parser
from hypothesis import strategies as st

__version__ = "0.0.1"
__all__ = ["from_template"]


def from_template(template: str) -> st.SearchStrategy[bytes]:
    """Parse the given template into a strategy."""
    ast = py010parser.parse_string(template)
    assert ast is True, "we know we don't actually handle templates yet"
    return st.just(b"")
