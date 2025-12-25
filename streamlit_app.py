from __future__ import annotations

import importlib.util
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List

import streamlit as st

APP_ROOT = Path(os.environ.get("APP_ROOT", "/apps")).resolve()
DEFAULT_APP = os.environ.get("DEFAULT_APP")


@dataclass
class DiscoveredApp:
    label: str
    path: Path


def discover_apps(app_root: Path) -> List[DiscoveredApp]:
    apps: List[DiscoveredApp] = []
    if not app_root.exists():
        return apps

    for entry in sorted(app_root.iterdir()):
        if entry.name.startswith("."):
            continue
        if entry.is_file() and entry.suffix == ".py":
            apps.append(DiscoveredApp(label=entry.stem, path=entry))
            continue
        if entry.is_dir():
            for candidate in ("streamlit_app.py", "app.py", "main.py"):
                candidate_path = entry / candidate
                if candidate_path.is_file():
                    apps.append(DiscoveredApp(label=entry.name, path=candidate_path))
                    break
    return apps


def load_app_module(app: DiscoveredApp):
    spec = importlib.util.spec_from_file_location(f"apps.{app.label}", app.path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module for {app.label}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_app_runner(module) -> Callable | None:
    for attr in ("main", "app"):
        candidate = getattr(module, attr, None)
        if callable(candidate):
            return candidate
    return None


def render():
    st.set_page_config(page_title="Streamlit Hub", layout="wide")
    st.title("Streamlit Hub")
    st.caption(f"Scanning apps in: {APP_ROOT}")

    apps = discover_apps(APP_ROOT)
    if not apps:
        st.info("No apps found. Add a .py file or an app folder inside the mounted APP_ROOT.")
        st.stop()

    choices = {app.label: app for app in apps}
    default_index = 0
    if DEFAULT_APP and DEFAULT_APP in choices:
        default_index = list(choices.keys()).index(DEFAULT_APP)

    selected_label = st.selectbox("Choose an app to run", list(choices.keys()), index=default_index)
    selected_app = choices[selected_label]

    try:
        module = load_app_module(selected_app)
        runner = get_app_runner(module)
        if runner is None:
            st.error("The selected app does not define a callable main() or app() function.")
            return
        with st.spinner(f"Running {selected_label}..."):
            runner()
    except Exception as exc:  # noqa: BLE001
        st.exception(exc)

    with st.expander("How do I add more apps?", expanded=False):
        st.markdown(
            """
            1. Drop a new `.py` file (with a `main()` or `app()` function) into the mounted `APP_ROOT` folder, **or**
               create a folder containing `app.py`, `main.py`, or `streamlit_app.py`.
            2. Wait a moment for Streamlit to reload, or restart the container.
            3. Pick your app from the dropdown above.
            """
        )


if __name__ == "__main__":
    render()
