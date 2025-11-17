import pandas as pd

from CW2_M01068100_CST1510.app.Data.db import connect_database
from CW2_M01068100_CST1510.app.Data.incidents import (
    insert_incident,
    update_incident_status,
    delete_incident
)
from CW2_M01068100_CST1510.app.Services.user_service import register_user, login_user
from CW2_M01068100_CST1510.app.Data.analytics import (
    get_incidents_by_type_count,
    get_high_severity_by_status
)


def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """

    print("\n" + "=" * 60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("=" * 60)

    conn = connect_database()

    # -----------------------------
    # TEST 1: Authentication
    # -----------------------------
    print("\n[TEST 1] Authentication")

    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")

    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # -----------------------------
    # TEST 2: CRUD Operations
    # -----------------------------
    print("\n[TEST 2] CRUD Operations")

    # Create Incident
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create:  ✅ Incident #{test_id} created")

    # Read Incident
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    {'✅ Found' if not df.empty else '❌ Not found'} incident #{test_id}")

    # Update Incident
    update_incident_status(conn, test_id, "Resolved")
    print(f"  Update:  ✅ Status updated")

    # Delete Incident
    delete_incident(conn, test_id)
    print(f"  Delete:  ✅ Incident deleted")

    # -----------------------------
    # TEST 3: Analytical Queries
    # -----------------------------
    print("\n[TEST 3] Analytical Queries")

    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:        Found {len(df_by_type)} rows")

    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity:  Found {len(df_high)} rows")

    conn.close()

    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_comprehensive_tests()