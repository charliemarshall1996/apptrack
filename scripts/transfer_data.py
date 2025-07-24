"""Script to transfer data from an old database to a new database using sqlite3."""

import sqlite3
from sqlite3 import OperationalError
from pathlib import Path
from graphlib import TopologicalSorter, CycleError
from typing import Dict, List, Tuple, Any

# Paths configuration
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "db.sqlite3"
OLD_DB_FILE = BASE_DIR / "db_old.sqlite3"


class DatabaseMigrator:
    def __init__(self):
        print("initialising migrator...")
        self.renamed_map: Dict[str, Dict[str, str]] = {}
        self.added_map: Dict[str, List[Tuple[str, str, str]]] = {}
        self.deleted_list: List[str] = []
        self.pk_mappings: Dict[str, Dict[Any, Any]] = {}

        # Initialize database connections with row factories
        self.old_db = sqlite3.connect(OLD_DB_FILE)
        self.old_db.row_factory = sqlite3.Row
        self.new_db = sqlite3.connect(DB_FILE)
        self.new_db.row_factory = sqlite3.Row
        self.new_db.execute("PRAGMA foreign_keys = ON;")

    def __del__(self):
        self.old_db.close()
        self.new_db.close()

    def get_user_input(self):
        print("collecting user input")
        """Collect user input about schema changes"""
        self.renamed_map = self._get_renamed_columns()
        self.added_map = self._get_added_columns()
        self.deleted_list = self._get_deleted_tables()

    def _get_added_columns(self) -> Dict[str, List[Tuple[str, str, str]]]:
        """Collect information about added columns"""
        added_map = {}
        while True:
            response = input("Have you added any columns? (y/[N]): ").lower()
            if response not in ('y', 'yes'):
                return added_map
            table = input("Table name of the added column: ").lower()
            name = input("Name of the added column: ").lower()
            data_type = input("Data type of the added column: ").lower()
            default = input(
                "Default value (SQL literal, e.g., NULL, 'default'): ").strip()
            added_map.setdefault(table, []).append((name, data_type, default))

    def _get_deleted_tables(self) -> List[str]:
        """Collect information about deleted tables"""
        deleted_list = []
        while True:
            response = input("Have you deleted any tables? (y/[N]): ").lower()
            if response not in ('y', 'yes'):
                return deleted_list
            table = input("Deleted table name: ").lower()
            deleted_list.append(table)

    def _get_renamed_columns(self) -> Dict[str, Dict[str, str]]:
        """Collect information about renamed columns"""
        renamed_map = {}
        while True:
            response = input("Have you renamed any columns? (y/[N]): ").lower()
            if response not in ('y', 'yes'):
                return renamed_map
            table = input("Table name of renamed column: ").lower()
            old_name = input("Old column name: ").lower()
            new_name = input("New column name: ").lower()
            renamed_map.setdefault(table, {})[old_name] = new_name

    def _get_processing_order(self) -> List[str]:
        print("getting processing order")
        """Get topologically sorted processing order based on foreign keys"""
        new_tables = self._get_new_tables()
        dependency_graph = self._build_dependency_graph(new_tables)

        try:
            ts = TopologicalSorter(dependency_graph)
            return list(ts.static_order())
        except CycleError:
            raise RuntimeError("Circular dependency detected in foreign keys")

    def _get_new_tables(self) -> List[str]:
        print("getting new tables...")
        """Get list of tables in new database"""
        cursor = self.new_db.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
        return [row[0] for row in cursor.fetchall()]

    def _build_dependency_graph(self, tables: List[str]) -> Dict[str, set]:
        print("building dependency graph...")
        """Build foreign key dependency graph"""
        dependency_graph = {}
        cursor = self.new_db.cursor()
        for table in tables:
            cursor.execute(f"PRAGMA foreign_key_list({table})")
            # Referenced table is index 3
            deps = {row[3] for row in cursor.fetchall()}
            dependency_graph[table] = deps
        return dependency_graph

    def _validate_table_exists(self, table: str) -> bool:
        print("validating table...")
        """Check if table exists in old database"""
        cursor = self.old_db.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
        return bool(cursor.fetchone())

    def _get_column_mapping(self, table: str) -> Tuple[List[str], List[str]]:
        print("getting column mapping...")
        """Generate column mapping between old and new schemas"""
        new_cols = self._get_table_columns(self.new_db, table)
        old_cols = self._get_table_columns(self.old_db, table)

        select_fields = []
        insert_fields = list(new_cols.keys())
        table_renames = self.renamed_map.get(table, {})

        for new_col in insert_fields:
            # Handle renamed columns
            old_col = next(
                (k for k, v in table_renames.items() if v == new_col), None)
            if old_col:
                if old_col in old_cols:
                    select_fields.append(f'"{old_col}" AS "{new_col}"')
                else:
                    raise ValueError(
                        f"Renamed column '{old_col}' not found in old table '{table}'")
            elif new_col in old_cols:
                select_fields.append(f'"{new_col}"')
            else:
                # Handle added columns
                added = next((c for c in self.added_map.get(
                    table, []) if c[0] == new_col), None)
                if added:
                    select_fields.append(f"{added[2]} AS \"{new_col}\"")
                else:
                    select_fields.append(f"NULL AS \"{new_col}\"")

        return select_fields, insert_fields

    def _get_table_columns(self, connection: sqlite3.Connection, table: str) -> Dict[str, dict]:
        print("getting table columns...")
        """Get column info using row factory"""
        cursor = connection.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        return {row['name']: dict(row) for row in cursor.fetchall()}

    def _get_foreign_keys(self, table: str) -> Dict[str, List[Dict]]:
        print("getting foreign keys...")
        """Get foreign keys using row factory"""
        cursor = self.new_db.cursor()
        cursor.execute(f"PRAGMA foreign_key_list({table})")
        return {
            table: [{
                'column': fk['from'],
                'reftable': fk['table'],
                'refcolumn': fk['to']
            } for fk in cursor.fetchall()]
        }

    def transfer_data(self):
        print("starting transfer...")
        """Main method to execute the data transfer"""
        processing_order = self._get_processing_order()

        for table in processing_order:
            if not self._validate_table_exists(table):
                print(f"Skipping {table} (not in old database)")
                continue
            if table in self.deleted_list:
                print(f"Skipping {table} (marked for deletion)")
                continue

            print(f"Transferring data for table: {table}")
            select_fields, insert_fields = self._get_column_mapping(table)
            self._transfer_table_data(table, select_fields, insert_fields)
        print("transfer complete.")

    def _get_primary_key(self, table: str) -> List[str]:
        print("getting primary key")
        """Get primary key column(s) using row factory"""
        cursor = self.new_db.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        return [row['name'] for row in cursor.fetchall() if row['pk'] > 0]

    def _transfer_table_data(self, table: str, select_fields: List[str], insert_fields: List[str]):
        print("transferring data...")
        """Transfer data with FK resolution using Row objects"""
        pk_columns = self._get_primary_key(table)
        if not pk_columns:
            raise ValueError(f"Table {table} has no primary key")

        # Build column position map
        col_positions = {col: idx for idx, col in enumerate(insert_fields)}
        fk_map = self._get_foreign_keys(table)

        # Prepare SQL statements
        select_sql = f"SELECT {', '.join(select_fields)} FROM \"{table}\""
        insert_sql = f"""
            INSERT OR IGNORE INTO "{table}"
            ({', '.join(f'"{f}"' for f in insert_fields)})
            VALUES ({', '.join(['?']*len(insert_fields))})
        """

        old_cursor = self.old_db.cursor()
        new_cursor = self.new_db.cursor()

        old_cursor.execute(select_sql)
        for row in old_cursor:
            # Convert Row object to ordered list of values
            new_row = [row[col] for col in insert_fields]

            # Replace foreign key values
            for fk in fk_map.get(table, []):
                col_idx = col_positions[fk['column']]
                ref_table = fk['reftable']
                old_fk_value = new_row[col_idx]

                if ref_table in self.pk_mappings:
                    new_row[col_idx] = self.pk_mappings[ref_table].get(
                        old_fk_value, None)
            self.new_db.commit()
            try:
                new_cursor.execute(insert_sql, new_row)
                self._update_pk_mapping(
                    table, pk_columns, row, new_cursor.lastrowid)
            except OperationalError as e:
                print(f"Skipped row in {table}: {e}")

        self.new_db.commit()

    def _update_pk_mapping(self, table: str, pk_columns: List[str], old_row: sqlite3.Row, new_rowid: int):
        """Update primary key mapping using Row objects"""
        cursor = self.new_db.cursor()
        if table not in self.pk_mappings:
            self.pk_mappings[table] = {}

        # Get old PK values from original row
        old_pk = tuple(old_row[col] for col in pk_columns)

        # Get new PK values (works for both single and composite keys)
        if len(pk_columns) == 1:
            if new_rowid or new_rowid == 0:
                new_pk = new_rowid
            else:
                statement = f"SELECT {pk_columns[0]} FROM {table} WHERE id = {new_rowid}"
                print(f"STATEMENT: {statement}")

                new_pk = cursor.execute(
                    statement).fetchone()[0]

            self.pk_mappings[table][old_pk[0]] = new_pk
        else:
            # For composite keys, we need to retrieve the actual inserted values
            where_clause = " AND ".join([f'"{col}" = ?' for col in pk_columns])
            new_pk_row = cursor.execute(
                f"SELECT {', '.join(pk_columns)} FROM {table} WHERE {where_clause}",
                old_pk
            ).fetchone()
            if new_pk_row:
                self.pk_mappings[table][old_pk] = tuple(
                    new_pk_row[col] for col in pk_columns)


def run():
    migrator = DatabaseMigrator()
    migrator.get_user_input()
    migrator.transfer_data()


if __name__ == "__main__":
    run()
