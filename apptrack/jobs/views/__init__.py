"""Views for the jobs app, including a kanban board view and a calendar view."""
from .board import board_view
from .job_add import job_add_view
from .job_archive import JobArchiveView
from .job_assign import JobAssignView
from .job_delete import JobDeleteView
from .job_download import job_download_view
from .job_edit import job_edit_view
from .job_list import JobListView

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
