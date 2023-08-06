"""
github workspace decorator.

"""

from functools import wraps

from github import Github, GithubException

DEFAULT_WORK_BRANCH = "ghworkspace"
DEFAULT_BASE_BRANCH = "master"


class WorkspaceError(Exception):
    """Base class for exceptions in this module."""

    pass


class InputParameterError(WorkspaceError):
    """Exceptions that occur when input parameters are missing.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class WorkInProgressError(WorkspaceError):
    """Exceptions that occur when a work branch is already in use.

    Attributes:
        branch -- a work branch name
    """

    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f"Working. [name: {self.branch}]"


class GithubError(WorkspaceError):
    """Exception raised for errors in the PyGithub.

    Attributes:
        expression -- input expression in which the error occurred
    """

    def __init__(self, expression):
        self.expression = expression


def workspace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs.get("token", None)
        if not token:
            token = args[0] if len(args) > 0 else None
            if not token:
                raise InputParameterError("Missing `token` parameter.")

        owner = kwargs.get("owner", None)
        if not owner:
            owner = args[1] if len(args) > 1 else None
            if not owner:
                raise InputParameterError("Missing `owner` parameter.")

        name = kwargs.get("name", None)
        if not name:
            name = args[2] if len(args) > 2 else None
            if not name:
                raise InputParameterError("Missing `name` parameter.")

        work_branch = kwargs.get("work_branch", None)
        if not work_branch:
            work_branch = args[3] if len(args) > 3 else None
            if not work_branch:
                work_branch = DEFAULT_WORK_BRANCH

        base_branch = kwargs["base_branch"] if "base_branch" in kwargs else DEFAULT_BASE_BRANCH

        # Preparing for Work branch
        try:
            gh = Github(token)
            repo = gh.get_repo(f"{owner}/{name}")
            branches = [b.name for b in repo.get_branches()]
            if work_branch in branches:
                raise WorkInProgressError(work_branch)

            if base_branch not in branches:
                raise InputParameterError(f"{base_branch} branch does not exist.")

            base_branch_ref = repo.get_git_ref(f"heads/{base_branch}")
            working_ref = repo.create_git_ref(
                f"refs/heads/{work_branch}", base_branch_ref.object.sha
            )
        except GithubException as e:
            raise GithubError(e)

        # Execution of the process
        try:
            if "work_branch" in kwargs:
                kwargs["work_branch"] = work_branch
            ret = func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            # Cleanup the work branch
            try:
                refs = [r.ref for r in repo.get_git_refs()]
                if working_ref.ref in refs:
                    working_ref.delete()
            except GithubException as e:
                raise GithubError(e)

        return ret

    return wrapper


from .__version__ import __version__
