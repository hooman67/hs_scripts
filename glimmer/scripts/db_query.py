#!/usr/bin/env python3
"""
Simple PostgreSQL connection script for running queries.
Usage: python db_query.py
"""

from __future__ import annotations

import sys

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("psycopg2 not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2
    from psycopg2.extras import RealDictCursor

# Database connection string
DATABASE_URL = "postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-queue-db.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer"


def run_query(conn, query: str) -> list[dict]:
    """Execute a query and return results as a list of dictionaries."""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query)
        if cursor.description:  # Query returns results
            return [dict(row) for row in cursor.fetchall()]
        else:  # Query doesn't return results (INSERT, UPDATE, etc.)
            conn.commit()
            return []


def interactive_mode(conn):
    """Interactive query mode."""
    print("\n=== PostgreSQL Interactive Query Tool ===")
    print("Enter your SQL queries (or 'quit' to exit, 'tables' to list tables)")
    print("=" * 50)

    while True:
        try:
            query = input("\nSQL> ").strip()

            if not query:
                continue

            if query.lower() == 'quit':
                break

            if query.lower() == 'tables':
                query = """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """

            results = run_query(conn, query)

            if results:
                print(f"\nReturned {len(results)} row(s):")
                for i, row in enumerate(results, 1):
                    print(f"\nRow {i}:")
                    for key, value in row.items():
                        print(f"  {key}: {value}")
            else:
                print("Query executed successfully (no results returned)")

        except psycopg2.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main entry point."""
    print("Connecting to database...")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected successfully!")

        # Example: List all tables
        print("\n=== Available Tables ===")
        tables = run_query(conn, """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        if tables:
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print("  (no tables found)")

        # Enter interactive mode
        interactive_mode(conn)

    except psycopg2.Error as e:
        print(f"Failed to connect to database: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()

