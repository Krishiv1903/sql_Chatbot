from app.db.db import get_connection

def create_appointment(name, date, desc):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Appointments (CustomerName, AppointmentDate, Description) VALUES (?, ?, ?)",
        (name, date, desc)
    )

    conn.commit()
    conn.close()

    return f"✅ Appointment created for {name} on {date} ({desc})"


def get_appointments(name=None, description=None, date=None, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Appointments WHERE 1=1"
    params = []

    if name:
        query += " AND LOWER(CustomerName) LIKE ?"
        params.append(f"%{name.lower()}%")

    if description:
        query += " AND LOWER(Description) LIKE ?"
        params.append(f"%{description.lower()}%")

    
    if date:
        query += " AND AppointmentDate LIKE ?"
        params.append(f"{date}%")


    if start_date and end_date:
        query += " AND AppointmentDate BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    query += " ORDER BY AppointmentDate DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No appointments found."

    result = []
    for row in rows:
        result.append({
            "name": row.CustomerName,
            "date": str(row.AppointmentDate),
            "desc": row.Description
        })

    return result