"""Streamlit entrypoint that dynamically loads all custom pages.

This version scans the ``frontend/custom_pages`` directory for any ``*_ui.py``
modules and exposes their ``render`` function as a sidebar menu item.  New page
modules can be added without modifying this file.
"""

import importlib
import os
import streamlit as st

# Directory that contains the page modules
PAGES_DIR = os.path.join(os.path.dirname(__file__), "custom_pages")

def discover_pages():
    """Discover all page modules with a ``render`` callable."""
    pages = {}
    for fname in os.listdir(PAGES_DIR):
        if not fname.endswith("_ui.py"):
            continue
        module_name = fname[:-3]  # strip ``.py``
        module = importlib.import_module(f"custom_pages.{module_name}")
        render_fn = getattr(module, "render", None)
        if callable(render_fn):
            # Make a pretty title from the filename
            title = module_name.replace("_ui", "").replace("_", " ").title()
            pages[title] = render_fn
    return pages

PAGES = discover_pages()

st.sidebar.title("AI 문서 QA 시스템")
page_name = st.sidebar.radio("메뉴 선택", list(PAGES.keys()))

# Render the selected page
PAGES[page_name]()
