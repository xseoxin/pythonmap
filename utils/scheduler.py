import schedule
import time
import threading
import logging
from datetime import datetime, timedelta
from typing import Callable, Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CheckScheduler:
    """Scheduler for automatic position checks."""

    def __init__(self):
        self.running = False
        self.thread: threading.Thread = None
        self.jobs: Dict[int, Any] = {}  # project_id -> job

    def start(self):
        """Start the scheduler thread."""
        if self.running:
            logger.warning("Scheduler already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Scheduler stopped")

    def _run_scheduler(self):
        """Run the scheduler loop."""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def schedule_project_check(self, project_id: int, frequency_hours: int,
                               check_function: Callable[[int], None]):
        """
        Schedule automatic checks for a project.

        Args:
            project_id: Project ID
            frequency_hours: Check frequency in hours
            check_function: Function to call for checking (receives project_id)
        """
        # Cancel existing job if any
        self.cancel_project_check(project_id)

        # Create new job
        if frequency_hours < 1:
            frequency_hours = 1

        job = schedule.every(frequency_hours).hours.do(
            check_function,
            project_id
        )

        self.jobs[project_id] = job
        logger.info(f"Scheduled checks for project {project_id} every {frequency_hours} hours")

    def cancel_project_check(self, project_id: int):
        """Cancel scheduled checks for a project."""
        if project_id in self.jobs:
            schedule.cancel_job(self.jobs[project_id])
            del self.jobs[project_id]
            logger.info(f"Cancelled scheduled checks for project {project_id}")

    def get_next_run(self, project_id: int) -> datetime:
        """Get next scheduled run time for a project."""
        if project_id in self.jobs:
            job = self.jobs[project_id]
            if job.next_run:
                return job.next_run
        return None

    def is_project_scheduled(self, project_id: int) -> bool:
        """Check if a project has scheduled checks."""
        return project_id in self.jobs

    def get_all_scheduled_projects(self) -> List[int]:
        """Get list of all project IDs with scheduled checks."""
        return list(self.jobs.keys())
