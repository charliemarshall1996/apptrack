"""Views for the jobs app, including a kanban board view and a calendar view."""
from .board import board_view
from .add import job_add_view
from .archive import JobArchiveView
from .assign import JobAssignView
from .delete import JobDeleteView
from .download import job_download_view
from .edit import job_edit_view
from .list import JobListView

__all__ = [
    "board_view",
    "job_add_view",
    "JobArchiveView",
    "JobAssignView",
    "JobDeleteView",
    "job_download_view",
    "job_edit_view",
    "JobListView",
]
