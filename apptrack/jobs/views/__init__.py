"""Views for the jobs app, including a kanban board view and a calendar view."""

from .add import job_add_view
from .archive import JobArchiveView
from .assign import JobAssignView
from .board import board_view
from .delete import JobDeleteView
from .download import job_download_view
from .edit import job_edit_view
from .list import JobListView
from .settings import settings_view

__all__ = [
    "board_view",
    "job_add_view",
    "JobArchiveView",
    "JobAssignView",
    "JobDeleteView",
    "job_download_view",
    "job_edit_view",
    "JobListView",
    "settings_view",
]
