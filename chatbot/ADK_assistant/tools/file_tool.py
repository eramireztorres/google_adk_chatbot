import os
from typing import Optional, Dict, Any, List

from pathlib import Path
# BASE_DIR = os.getenv("BASE_DIR", "/home/erick/repo")
BASE_DIR = os.getenv(
    "BASE_DIR",
    str(Path(__file__).resolve().parents[4])  # go up 4 levels
)

# ---- Helpers ---------------------------------------------------------------

def _safe_path(path: str) -> str:
    """
    Resolve and validate a path so it cannot escape ``BASE_DIR``.

    This function converts ``path`` to an absolute path and checks that it is
    located inside ``BASE_DIR`` (or equals ``BASE_DIR`` itself). If the path
    attempts to traverse outside (via absolute paths, symlinks already
    resolved by the OS, or ``..`` segments), a ``ValueError`` is raised.

    Parameters
    ----------
    path : str
        A file or directory path. May be absolute or relative to BASE_DIR.

    Returns
    -------
    str
        The absolute, validated path.

    Raises
    ------
    ValueError
        If the resolved path is outside ``BASE_DIR``.
    """
    # If given a relative path, make it relative to BASE_DIR for convenience.
    if not os.path.isabs(path):
        path = os.path.join(BASE_DIR, path)

    p = os.path.abspath(path)
    base = os.path.abspath(BASE_DIR)

    # Ensure either p == base or p is within base + os.sep prefix
    if not (p == base or p.startswith(base + os.sep)):
        raise ValueError(f"Path escapes BASE_DIR: {p}")

    return p


# ---- Public API ------------------------------------------------------------

def list_dir(path: str) -> Dict[str, Any]:
    """
    List immediate entries (non-recursive) in a directory under ``BASE_DIR``.

    Parameters
    ----------
    path : str
        Directory to list. Can be absolute (must be inside BASE_DIR) or
        relative to ``BASE_DIR`` (e.g., ".", "subdir").

    Returns
    -------
    Dict[str, Any]
        On success:
            {
              "ok": True,
              "entries": [{"name": <str>, "type": "dir"|"file"}, ...],
              "path": <absolute_dir_path>
            }
        On error (e.g., not found, not a directory, permission issues):
            {
              "ok": False,
              "path": <absolute_dir_path>,
              "error": <message>
            }

    Notes
    -----
    - The listing is **non-recursive** by design.
    - Parent directories are not created; the path must already exist.

    Examples
    --------
    >>> list_dir(".")["ok"]
    True
    >>> list_dir("missing")["ok"]
    False
    """
    p = _safe_path(path)
    try:
        entries: List[Dict[str, str]] = []
        for name in os.listdir(p):
            full = os.path.join(p, name)
            entries.append({"name": name, "type": "dir" if os.path.isdir(full) else "file"})
        return {"ok": True, "entries": entries, "path": p}
    except Exception as e:
        return {"ok": False, "path": p, "error": str(e)}


def read_file(path: str, encoding: Optional[str] = "utf-8") -> Dict[str, Any]:
    """
    Read a text file under ``BASE_DIR``.

    Parameters
    ----------
    path : str
        Path to the file. Absolute (inside BASE_DIR) or relative to BASE_DIR.
    encoding : Optional[str], default "utf-8"
        Text encoding to use when reading.

    Returns
    -------
    Dict[str, Any]
        On success:
            {"ok": True, "path": <absolute_path>, "content": <str>}
        On error:
            {"ok": False, "path": <absolute_path>, "error": <code_or_message>}

        The special error code "ENOENT" is returned for a missing file.

    Examples
    --------
    >>> res = read_file("notes/todo.txt")
    >>> res["ok"]
    True
    >>> isinstance(res["content"], str)
    True
    """
    p = _safe_path(path)
    try:
        with open(p, "r", encoding=encoding) as f:
            return {"ok": True, "path": p, "content": f.read()}
    except FileNotFoundError:
        return {"ok": False, "path": p, "error": "ENOENT"}
    except Exception as e:
        return {"ok": False, "path": p, "error": str(e)}


def write_file(
    path: str,
    content: str,
    mode: str = "w",
    encoding: Optional[str] = "utf-8",
) -> Dict[str, Any]:
    """
    Write (or append) text to a file under ``BASE_DIR``, creating parents.

    Parameters
    ----------
    path : str
        Destination path (absolute inside BASE_DIR or relative to BASE_DIR).
    content : str
        Text to write.
    mode : str, default "w"
        File mode: "w" to truncate/create, "a" to append.
    encoding : Optional[str], default "utf-8"
        Text encoding used to write the file.

    Returns
    -------
    Dict[str, Any]
        {"ok": True, "path": <absolute_path>, "bytes": <int_bytes_written>}

    Raises
    ------
    ValueError
        If ``mode`` is not "w" or "a".
    ValueError
        If the resolved path escapes ``BASE_DIR``.

    Notes
    -----
    - Parent directories are created with ``exist_ok=True``.
    - This function does not lock files; concurrent writes are not coordinated.

    Examples
    --------
    >>> write_file("logs/run.txt", "started\\n")["ok"]
    True
    >>> write_file("logs/run.txt", "more\\n", mode="a")["ok"]
    True
    """
    try:
        if mode not in ("w", "a"):
            return {"ok": False, "path": "", "error": "EINVAL: mode must be 'w' or 'a'"}

        p = _safe_path(path)  # may raise -> we catch below
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, mode, encoding=encoding) as f:
            written = f.write(content)
        return {"ok": True, "path": p, "bytes": written}
    except Exception as e:
        # If _safe_path failed, p may be undefined; include best-effort path
        abs_path = os.path.abspath(os.path.join(BASE_DIR, path)) if not os.path.isabs(path) else os.path.abspath(path)
        return {"ok": False, "path": abs_path, "error": str(e)}


def create_file(path: str, content: str = "", encoding: Optional[str] = "utf-8") -> Dict[str, Any]:
    """
    Create (or overwrite) a text file under ``BASE_DIR`` with optional content.

    This is a convenience wrapper around ``write_file(..., mode="w")``.

    Parameters
    ----------
    path : str
        Destination path (absolute inside BASE_DIR or relative to BASE_DIR).
    content : str, default ""
        Initial file contents.
    encoding : Optional[str], default "utf-8"
        Text encoding used to write the file.

    Returns
    -------
    Dict[str, Any]
        {"ok": True, "path": <absolute_path>, "bytes": <int_bytes_written>}

    Examples
    --------
    >>> create_file("reports/summary.txt", "hello")["ok"]
    True
    """
    return write_file(path, content, mode="w", encoding=encoding)
