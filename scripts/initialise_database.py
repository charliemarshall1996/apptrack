"""Script which initialises the database ready for deployment.

Script removes all migrations and backs-up existing database.
"""

import logging
import os
import shutil
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "db.sqlite3"
OLD_DB_FILE = BASE_DIR / "db_old.sqlite3"


def backup_database():
    """Backup the existing database to a file named 'db_old.sqlite3' if it exists.

    If the database file exists, it is renamed to 'db_old.sqlite3'. If the file exists
    after the rename, it is deleted. If the file never existed, a message is printed
    to the console.
    """
    logger.info("Backing up database...")
    if DB_FILE.exists():
        logger.info("Database file found. Backing up...")
        shutil.move(str(DB_FILE), str(OLD_DB_FILE))
        logger.info("Database backup created as 'db_old.sqlite3'.")

        if DB_FILE.exists():
            logger.info("Database backup already exists. Deleting...")
            os.remove(DB_FILE)
            logger.info("Database backup deleted.")
    else:
        logger.warning("Database file not found.")

    logger.info("Database backup completed.")


def remove_migrations():
    """Remove all migrations from all apps in the project.

    This function iterates through every app in the project, and
    removes all migrations from the 'migrations' folder, except
    for '__init__.py'. If there is an error removing a migration,
    the error is logged. At the end of the function, a message is
    printed to the console, indicating which apps have had their
    migrations cleared.
    """
    logger.info("Removing migration files...")

    for app in BASE_DIR.iterdir():
        logger.info("Processing app: %s", app.name)
        migrations_folder = app / "migrations"
        if migrations_folder.exists():
            logger.info("Migrations found for app: %s", app.name)

            for file in migrations_folder.iterdir():
                if file.name != "__init__.py" and "__pycache__" not in file.name:
                    try:
                        logger.info("Removing migration: %s", file.name)
                        subprocess.call(shell=True, args=[
                                        "r", "-f", file.name])
                        logger.info("Migration removed: %s", file.name)
                    except subprocess.CalledProcessError as e:
                        logger.error(
                            "Error removing migration %s for app %s: %s",
                            file.name,
                            app.name,
                            e.output,
                        )
                    else:
                        file.unlink()
            logger.info("Cleared migrations for app: %s", app.name)

    logger.info("Migration files cleared.")


def run():
    """Script entry point.

    Backs up the existing database to a file named 'db_old.sqlite3',
    and removes all migrations from all apps in the project. If an error occurs removing
    a migration, the error is logged. At the end of the function, a message is printed
    to the console, indicating which apps have had their migrations cleared.
    """
    logger.info("Running initialise_deployment_migrations script...")

    backup_database()
    remove_migrations()

    logger.info("Script completed.")


if __name__ == "__main__":
    run()
