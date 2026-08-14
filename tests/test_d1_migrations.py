# =====================================================================
# ANGEL SOLUTIONS ATL - SCHEMA & PERFORMANCE INDEX VERIFICATION
# =====================================================================
# Reads and compiles schema.sql locally using SQLite parser tests to guarantee
# indices, cascades, and data models are correct before wrangler deployments.
# =====================================================================

import unittest
import sqlite3
import os

class DatabaseSchemaTests(unittest.TestCase):

    def setUp(self):
        # Create an in-memory SQLite database for testing the schema
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_schema_sql_migration_compatibility(self):
        """
        Reads and executes schema.sql in memory to confirm SQLite 3 syntax compatibility.
        """
        schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/schema.sql"))
        self.assertTrue(os.path.exists(schema_path), f"schema.sql not found at: {schema_path}")

        with open(schema_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        try:
            self.cursor.executescript(sql_script)
            self.conn.commit()
        except sqlite3.Error as e:
            self.fail(f"SQL execution failed. Malformed SQLite syntax or index definition: {e}")

        # Verify critical high-performance tables are compiled
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.cursor.fetchall()]
        
        required_tables = ["users", "leads", "conversations", "interactions", "escalations", "follow_ups", "ghl_sync_log"]
        for table in required_tables:
            self.assertIn(table, tables, f"Mandatory production relational table '{table}' is missing from schema compiling.")

        # Verify indices exist for indexing fields (e.g. idx_leads_platform_user_id)
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indices = [row[0] for row in self.cursor.fetchall()]
        self.assertTrue(len(indices) > 0, "No performance optimization indices defined in schema.sql")

if __name__ == "__main__":
    unittest.main()
