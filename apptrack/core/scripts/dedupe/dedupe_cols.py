from django.db import transaction
from jobs.models import Columns  # Replace 'your_app' with your app name

# Using a transaction to ensure database consistency


def dedupe_columns():
    with transaction.atomic():
        # Find all unique combinations of board, name, and position
        seen = set()

        # Loop through all columns, ordered by id to retain the first occurrence
        for column in Columns.objects.order_by('id'):
            identifier = (column.board_id, column.name, column.position)

            if identifier in seen:
                # If the combination already exists, delete the duplicate
                column.delete()
            else:
                # Otherwise, mark this combination as seen
                seen.add(identifier)


def run():
    dedupe_columns()
