from app.db.db import get_connection

def get_doctors_by_department(dept_name):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT d.DocName, dep.DeptName
    FROM Doctors d
    JOIN Departments dep ON d.DeptId = dep.DeptId
    WHERE LOWER(dep.DeptName) = ?
    """

    cursor.execute(query, (dept_name.lower(),))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No doctors found for this department."

    result = []
    for row in rows:
        result.append({
            "name": row.DocName,
            "date": f"Department: {row.DeptName}",
            "desc": "Doctor"

        })

    return result

def get_doctors_by_patient(name: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT TOP 1 a.Description
    FROM Appointments a
    WHERE LOWER(a.CustomerName) = ?
    ORDER BY a.AppointmentDate DESC
    """

    cursor.execute(query, (name.lower(),))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return "No appointment found for this patient."

    description = row.Description.lower()

    # Now get doctors using description
    query2 = """
    SELECT d.DocName, dep.DeptName
    FROM Doctors d
    JOIN Departments dep ON d.DeptId = dep.DeptId
    WHERE LOWER(dep.DeptName) = ?
    """

    cursor.execute(query2, (description,))
    doctors = cursor.fetchall()

    conn.close()

    if not doctors:
        return "No doctors found for this patient's department."

    result = []
    for doc in doctors:
        result.append({
            "name": doc.DocName,
            "date": f"Department: {doc.DeptName}",
            "desc": f"Patient: {name}"
        })

    return result

def get_all_doctors():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT d.DocName, dep.DeptName
    FROM Doctors d
    JOIN Departments dep ON d.DeptId = dep.DeptId
    ORDER BY dep.DeptName
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No doctors found."

    result = []
    for row in rows:
        result.append({
            "name": row.DocName,
            "date": f"Department: {row.DeptName}",
            "desc": "Doctor"
        })

    return result