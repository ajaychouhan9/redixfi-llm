"""Offline proofs for kaggle_run.py's project-location resolution.

WHAT THIS GUARDS AGAINST
-------------------------
A real Kaggle run reached STEP 4 with `ModuleNotFoundError: No module named
'app'`. Root cause: the script unconditionally trusted a hardcoded
`/kaggle/working/LLM` path, assuming a manual staging cell had extracted the
project there first. When the attached dataset's internal layout changed
(an already-extracted `llm_project/` directory instead of a
`llm_project.tar.gz`), that staging cell silently extracted nothing —
`/kaggle/working/LLM` existed (from `mkdir -p`) but was EMPTY — and nothing
caught it until the first `from app...` import, three steps later.

These tests exercise the fix — `_find_project_root` / `_resolve_project_root`
— entirely offline, using temp directories in place of `/kaggle/...` paths
(monkeypatched via the module's `_INPUT_PREFIX` / `_STAGING_DIR` /
`_SEARCH_BASES` constants, since real `/kaggle/...` paths do not exist off
Kaggle).

NOT PROVEN HERE — needs the real Kaggle run: that the auto-detected root
actually matches wherever THIS SPECIFIC dataset mounts on THIS SPECIFIC
notebook, and that the model still loads after this fix. Only a real run on
Kaggle can confirm that; see deployment/kaggle/RUNBOOK_STEP4.md.

`kaggle_run.py` is a standalone script, not part of the `app` package (it
runs `python kaggle_run.py`, never `import app...`), so it is loaded here by
file path rather than by package import.
"""
from __future__ import annotations

import importlib.util
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "deployment", "kaggle", "kaggle_run.py")


def _load_module():
    """Imports kaggle_run.py by path. Safe: main() only runs under
    `if __name__ == "__main__"`, which is False for an imported module, so
    nothing executes beyond function/constant definitions."""
    spec = importlib.util.spec_from_file_location("kaggle_run_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def kr():
    return _load_module()


def _make_project(base) -> str:
    """Builds a fake llm_project tree containing the one file the resolver
    actually checks for."""
    marker_dir = os.path.join(base, "app", "models")
    os.makedirs(marker_dir, exist_ok=True)
    with open(os.path.join(marker_dir, "registry.py"), "w") as fh:
        fh.write("# fake registry\n")
    return base


def _load_isolated_copy(tmp_path, name="isolated"):
    """Loads a COPY of kaggle_run.py from a directory with no sibling `app/`
    package, so the "this script's own location" candidate genuinely misses
    and only the mechanism under test can succeed. This is what makes these
    tests prove the SEARCH/STAGING logic specifically, rather than always
    passing because the real C:\\LLM checkout happens to be findable."""
    script_dir = tmp_path / name / "deployment" / "kaggle"
    script_dir.mkdir(parents=True)
    copy_path = script_dir / "kaggle_run.py"
    copy_path.write_text(open(SCRIPT, encoding="utf-8").read(), encoding="utf-8")
    spec = importlib.util.spec_from_file_location(f"kaggle_run_{name}", str(copy_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------
# _has_app — the concrete check, not "the directory exists"
# --------------------------------------------------------------------------
def test_has_app_requires_the_real_marker_file(kr, tmp_path):
    empty = tmp_path / "empty_dir"
    empty.mkdir()
    assert kr._has_app(str(empty)) is False   # the exact failure mode: dir exists, empty

    real = _make_project(str(tmp_path / "real"))
    assert kr._has_app(real) is True

    assert kr._has_app(None) is False
    assert kr._has_app("") is False
    assert kr._has_app(str(tmp_path / "does_not_exist_at_all")) is False


# --------------------------------------------------------------------------
# _find_project_root — the priority order
# --------------------------------------------------------------------------
def test_finds_this_scripts_own_location_when_nothing_else_is_given(kr):
    """kaggle_run.py lives at <root>/deployment/kaggle/kaggle_run.py — two
    parents up IS the real llm_project root whenever the script runs in
    place. This must resolve to the real C:\\LLM checkout."""
    found = kr._find_project_root(None)
    assert found is not None
    assert os.path.isfile(os.path.join(found, "app", "models", "registry.py"))
    assert os.path.abspath(found) == os.path.abspath(ROOT)


def test_explicit_repo_dir_is_used_when_valid(kr, tmp_path):
    project = _make_project(str(tmp_path / "explicit"))
    found = kr._find_project_root(project)
    assert os.path.abspath(found) == os.path.abspath(project)


def test_explicit_repo_dir_is_rejected_when_invalid_not_trusted_blindly(kr, tmp_path):
    """The exact bug class this fix closes: a path that EXISTS but has no
    `app` package must not be silently accepted. It should fall through to
    a real location instead — here, this script's own real root."""
    empty = tmp_path / "empty_staging_dir"
    empty.mkdir()
    found = kr._find_project_root(str(empty))
    assert found is not None
    assert os.path.abspath(found) != os.path.abspath(str(empty))
    assert kr._has_app(found)


def test_staging_dir_is_tried_when_script_location_lacks_the_marker(tmp_path, monkeypatch):
    """Simulates running a COPY of kaggle_run.py from somewhere with no
    sibling `app/` package (so the "own location" candidate fails), with a
    valid project sitting at the documented staging path."""
    staged = _make_project(str(tmp_path / "staged"))
    isolated = _load_isolated_copy(tmp_path)
    monkeypatch.setattr(isolated, "_STAGING_DIR", staged)
    monkeypatch.setattr(isolated, "_SEARCH_BASES", (str(tmp_path / "nowhere"),))

    found = isolated._find_project_root(None)
    assert os.path.abspath(found) == os.path.abspath(staged)


def test_falls_back_to_recursive_search_as_a_last_resort(tmp_path, monkeypatch):
    """The scenario that actually broke: neither an explicit path, this
    script's own location, nor the staging dir has the project — but it
    genuinely exists somewhere findable (a nested Kaggle dataset mount).
    Proves the REAL _find_project_root finds it via search, not that a
    hand-rolled glob loop does."""
    fake_input = tmp_path / "kaggle_input"
    nested = fake_input / "datasets" / "someone" / "some-dataset-name" / "llm_project"
    _make_project(str(nested))

    isolated = _load_isolated_copy(tmp_path)
    monkeypatch.setattr(isolated, "_STAGING_DIR", str(tmp_path / "empty_staging"))
    monkeypatch.setattr(isolated, "_SEARCH_BASES",
                        (str(fake_input), str(tmp_path / "kaggle_working")))

    found = isolated._find_project_root(None)
    assert found is not None
    assert os.path.abspath(found) == os.path.abspath(str(nested))


def test_returns_none_when_genuinely_nowhere_to_be_found(tmp_path, monkeypatch):
    """Every candidate genuinely misses — using the isolated-copy technique
    so "this script's own location" (the real C:\\LLM checkout) cannot
    rescue the test. Must return None, not raise and not guess."""
    isolated = _load_isolated_copy(tmp_path)
    monkeypatch.setattr(isolated, "_STAGING_DIR", str(tmp_path / "nope1"))
    monkeypatch.setattr(isolated, "_SEARCH_BASES",
                        (str(tmp_path / "nope2"), str(tmp_path / "nope3")))

    found = isolated._find_project_root(str(tmp_path / "bad_explicit"))
    assert found is None


# --------------------------------------------------------------------------
# _resolve_project_root — the read-only-mount copy behaviour
# --------------------------------------------------------------------------
def test_resolve_copies_off_a_readonly_input_mount(kr, tmp_path, monkeypatch):
    """The other half of the real failure mode: even once located, a path
    under /kaggle/input cannot be written to, and the benchmark step writes
    results under evaluation/*/runs relative to the chdir'd root. Proves
    the copy happens and the copy is verified."""
    fake_input_root = tmp_path / "kaggle_input" / "datasets" / "me" / "ds" / "llm_project"
    _make_project(str(fake_input_root))
    writable_target = tmp_path / "kaggle_working" / "LLM"

    monkeypatch.setattr(kr, "_INPUT_PREFIX", str(tmp_path / "kaggle_input"))
    monkeypatch.setattr(kr, "_STAGING_DIR", str(writable_target))

    resolved = kr._resolve_project_root(str(fake_input_root))

    assert os.path.abspath(resolved) == os.path.abspath(str(writable_target))
    assert kr._has_app(resolved)
    # The original mount is untouched — this project is read-only in reality;
    # a real /kaggle/input write would raise, so leaving it alone is correct.
    assert kr._has_app(str(fake_input_root))


def test_resolve_does_not_copy_when_already_writable(kr, tmp_path, monkeypatch):
    writable = _make_project(str(tmp_path / "already_writable"))
    monkeypatch.setattr(kr, "_INPUT_PREFIX", str(tmp_path / "kaggle_input_unused"))

    resolved = kr._resolve_project_root(writable)
    assert os.path.abspath(resolved) == os.path.abspath(writable)


def test_resolve_dies_clearly_when_nothing_is_found(tmp_path, monkeypatch):
    """Before this fix, a bad path produced a cryptic ModuleNotFoundError
    three steps later. Now it must die immediately (step 0) with a message
    naming every place it looked."""
    isolated = _load_isolated_copy(tmp_path, name="isolated_die")
    monkeypatch.setattr(isolated, "_STAGING_DIR", str(tmp_path / "nope1"))
    monkeypatch.setattr(isolated, "_SEARCH_BASES", (str(tmp_path / "nope2"),))

    with pytest.raises(SystemExit) as exc_info:
        isolated._resolve_project_root(str(tmp_path / "bad_explicit_path"))
    assert exc_info.value.code == 1
    assert isolated.STATE["fatal"]["step"] == 0
    assert "could not locate" in isolated.STATE["fatal"]["error"]


# --------------------------------------------------------------------------
# CLI surface — --repo-dir defaults to auto-detect, not a hardcoded path
# --------------------------------------------------------------------------
def test_repo_dir_flag_defaults_to_none_not_a_hardcoded_path(kr):
    """The regression this whole fix closes: --repo-dir used to default to
    the literal string "/kaggle/working/LLM", which the script then trusted
    unconditionally. It must now default to None so auto-detection runs."""
    import argparse
    import inspect

    src = inspect.getsource(kr.main)
    assert 'default="/kaggle/working/LLM"' not in src, (
        "a hardcoded /kaggle/working/LLM default has crept back into --repo-dir"
    )
    assert "_resolve_project_root(args.repo_dir)" in src


# --------------------------------------------------------------------------
# --fixtures validation — the other half of "verify before trusting a path"
# --------------------------------------------------------------------------
def test_main_validates_fixtures_before_expensive_steps(kr):
    """A wrong --fixtures path must not be allowed to silently "succeed"
    with zero cases in every category (the benchmark loop only warn()s and
    skips a missing file) after the model has already been loaded. The
    check must exist in main() before STEP 1."""
    import inspect
    src = inspect.getsource(kr.main)
    assert "annual_report_sample15.json" in src.split("STEP 1")[0], (
        "fixtures existence is not checked before step 1 in main()"
    )
    assert "args.skip_benchmark" in src.split("STEP 1")[0]


# --------------------------------------------------------------------------
# Regression: the EXACT reported failure — stale-code chdir into a path
# that was never created.
# --------------------------------------------------------------------------
def test_never_chdirs_into_a_nonexistent_working_dir_with_the_reported_dataset(
    tmp_path, monkeypatch,
):
    """Reproduces the founder's exact report, literally:

      dataset path : /kaggle/input/datasets/ajaychouhan9/
                      redixfi-llm-evaluation-2026/llm_project
      failure      : FileNotFoundError: No such file or directory:
                      '/kaggle/working/LLM'

    Critically, /kaggle/working/LLM is NOT created anywhere in this test —
    no `mkdir -p` step, matching the current runbook's self-locating one-cell
    invocation, which stages nothing. If _resolve_project_root ever again
    returned an unresolved/hardcoded path instead of the located one, this
    test would fail with FileNotFoundError on the os.chdir call below, the
    same way the real run did.
    """
    fake_input = tmp_path / "kaggle" / "input"
    nested = (fake_input / "datasets" / "ajaychouhan9" /
             "redixfi-llm-evaluation-2026" / "llm_project")
    _make_project(str(nested))

    working = tmp_path / "kaggle" / "working"
    working.mkdir(parents=True)
    staging_dir = working / "LLM"
    assert not staging_dir.exists(), "test setup error: staging dir must NOT pre-exist"

    isolated = _load_isolated_copy(tmp_path, name="isolated_regression")
    monkeypatch.setattr(isolated, "_INPUT_PREFIX", str(fake_input))
    monkeypatch.setattr(isolated, "_STAGING_DIR", str(staging_dir))
    monkeypatch.setattr(isolated, "_SEARCH_BASES", (str(fake_input), str(working)))

    # No --repo-dir passed, exactly like the runbook's one-liner cell.
    resolved = isolated._resolve_project_root(None)

    # The actual assertion this whole bug is about: the resolved path must
    # exist BEFORE anything tries to chdir into it.
    assert os.path.isdir(resolved), (
        f"_resolve_project_root returned {resolved!r}, which does not exist — "
        "this is precisely the condition that caused the reported "
        "FileNotFoundError"
    )
    os.chdir(resolved)  # must not raise

    # And it must have landed in the writable staging dir (copied off the
    # read-only-shaped input mount), not stayed on the "read-only" nested
    # dataset path.
    assert os.path.abspath(resolved) == os.path.abspath(str(staging_dir))
    assert isolated._has_app(resolved)


def test_main_guards_chdir_with_an_explicit_existence_check(kr):
    """Defense in depth: even though _resolve_project_root cannot currently
    return a nonexistent path, main() must not hand a bare os.chdir() a
    value it has not itself verified — a future regression (or, as
    happened, code drift between what's committed and what actually runs
    on Kaggle) must die() with a clear message, not a raw traceback."""
    import inspect
    src = inspect.getsource(kr.main)
    before_chdir = src.split("os.chdir(repo_dir)")[0]
    assert "os.path.isdir(repo_dir)" in before_chdir, (
        "main() no longer verifies repo_dir exists immediately before chdir'ing into it"
    )
