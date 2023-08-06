import logging
import os
import platform
import traceback
from functools import wraps
from subprocess import check_output

import zmtools

LOGGER = logging.getLogger(__name__)


def _create_issue(issue_title, issue_body, repo_owner, repo_name, issue_label="crashautoreport"):
    """Create an issue on GitHub's issues section for a specific repo

    Args:
        issue_title (str): The title of the issue to create
        issue_body (str): The body of the issue to create
        repo_owner (str): The username of the owner of the repo to create the issue for
        repo_name (str): The repo name to create the issue for
        issue_label (str, optional): The label to attach to the issue. Defaults to "crashautoreport".

    Returns:
        str: The URL of the created issue
    """
    return check_output(["gh", "issue", "create", "--title", issue_title, "--body", issue_body, "--label", issue_label, "-R", f"{repo_owner}/{repo_name}"])


def auto_create_issue(app_name=None, repo_owner=None, repo_name=None, exceptions=None):
    """Decorator to create a GitHub issue on exception throw

    Args:
        app_name (str, optional): The app name that relates to the repo. This is used to find the repo name and repo owner if they are not provided. Defaults to None.
        repo_owner (str): The username of the owner of the repo to create the issue for
        repo_name (str): The repo name to create the issue for
        exceptions (list[Exception], optional): The exception types to create an issue for. None means create te issue for any exception. Defaults to None.
    """
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                nonlocal app_name, repo_name, repo_owner, exceptions
                if not exceptions or any(isinstance(e, etype) for etype in exceptions):
                    if app_name is not None:
                        if platform.system() == "Darwin":
                            filename = os.path.join(os.sep, "Library", "Application Support", "ghinfo")
                        elif platform.system() == "Windows":
                            filename = os.path.join(os.environ["PROGRAMDATA"], "ghinfo")
                        else:
                            filename = os.path.join(
                                os.sep, "etc", "ghinfo", app_name)
                        with open(filename) as f:
                            repo_owner, repo_name = [
                                l.strip() for l in f.readlines()]
                    elif repo_owner is None or repo_name is None:
                        raise ValueError(
                            "No repo_owner ot repo_name specified")
                    tb = traceback.format_exc().strip()
                    issue_title = zmtools.truncate(
                        tb.split("\n")[-1], length=25)
                    issue_body = f"```python\n{tb}\n```"
                    issue = _create_issue(
                        issue_title, issue_body, repo_owner=repo_owner, repo_name=repo_name)
                    LOGGER.info(f"An issue was created at {issue}")
                raise e
        return wrapper
    return actual_decorator
