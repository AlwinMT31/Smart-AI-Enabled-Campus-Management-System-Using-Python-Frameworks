import os
import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

from flask import Flask, render_template, request, redirect, url_for, flash


APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "campus.db")
UPLOAD_DIR = os.path.join(APP_DIR, "uploads")

app = Flask(__name__)
app.secret_key = "dev-secret"


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            parent_contact TEXT,
            class_id TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            UNIQUE(student_id, date),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            message TEXT NOT NULL,
            recipient TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
        """
    )
    conn.commit()
    # Seed demo data if students table is empty
    cur.execute("SELECT COUNT(*) AS c FROM students")
    if cur.fetchone()["c"] == 0:
        demo_students = [
            ("1001", "Aman Sharma", "parent_1001@example.com", "CSE-101"),
            ("1002", "Bhavna Singh", "parent_1002@example.com", "CSE-101"),
            ("1003", "Chirag Gupta", "parent_1003@example.com", "CSE-101"),
            ("2001", "Divya Kaur", "parent_2001@example.com", "ECE-201"),
            ("2002", "Eshan Mehta", "parent_2002@example.com", "ECE-201"),
        ]
        cur.executemany(
            "INSERT INTO students(roll_no, name, parent_contact, class_id) VALUES(?, ?, ?, ?)",
            demo_students,
        )
        conn.commit()
    conn.close()


def get_classes() -> List[str]:
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT class_id FROM students ORDER BY class_id").fetchall()
    conn.close()
    return [row["class_id"] for row in rows]


def get_students_by_class(class_id: str) -> List[sqlite3.Row]:
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM students WHERE class_id = ? ORDER BY roll_no", (class_id,)
    ).fetchall()
    conn.close()
    return rows


def mark_attendance(student_ids: List[int], date_str: str, status: str):
    conn = get_db()
    cur = conn.cursor()
    for sid in student_ids:
        cur.execute(
            "INSERT OR REPLACE INTO attendance(student_id, date, status) VALUES(?, ?, ?)",
            (sid, date_str, status),
        )
    conn.commit()
    conn.close()


def get_attendance_for_class(class_id: str, date_str: str) -> List[sqlite3.Row]:
    conn = get_db()
    rows = conn.execute(
        """
        SELECT s.id AS student_id, s.roll_no, s.name,
               COALESCE(a.status, 'N/A') AS status
        FROM students s
        LEFT JOIN attendance a ON a.student_id = s.id AND a.date = ?
        WHERE s.class_id = ?
        ORDER BY s.roll_no
        """,
        (date_str, class_id),
    ).fetchall()
    conn.close()
    return rows


def send_absent_notifications(absent_student_ids: List[int], date_str: str):
    conn = get_db()
    cur = conn.cursor()
    for sid in absent_student_ids:
        cur.execute(
            "INSERT INTO notifications(student_id, date, message, recipient) VALUES(?, ?, ?, ?)",
            (sid, date_str, "You are marked ABSENT today.", "student"),
        )
        cur.execute(
            "INSERT INTO notifications(student_id, date, message, recipient) VALUES(?, ?, ?, ?)",
            (sid, date_str, "Your ward is marked ABSENT today.", "parent"),
        )
    conn.commit()
    conn.close()


def parse_recognized_rollnos_from_filename(filename: str) -> List[str]:
    base = os.path.splitext(os.path.basename(filename))[0]
    parts = base.replace("-", "_").split("_")
    rollnos = [p for p in parts if p.isdigit()]
    return rollnos


@app.route("/")
def dashboard():
    classes = get_classes()
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    notifications = conn.execute(
        """
        SELECT n.id, s.roll_no, s.name, n.message, n.recipient, n.date
        FROM notifications n
        JOIN students s ON s.id = n.student_id
        ORDER BY n.id DESC
        LIMIT 10
        """
    ).fetchall()
    conn.close()
    return render_template("dashboard.html", classes=classes, today=today, notifications=notifications)


@app.route("/faculty/attendance", methods=["GET", "POST"])
def faculty_attendance():
    class_id = request.args.get("class_id") or request.form.get("class_id") or ""
    today = datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        action = request.form.get("action")
        students = get_students_by_class(class_id)
        all_ids = [int(s["id"]) for s in students]
        selected_ids = [int(sid) for sid in request.form.getlist("student_ids")]
        present_ids: List[int] = []
        if action == "mark_all":
            present_ids = all_ids
        elif action == "mark_selected":
            present_ids = selected_ids
        elif action == "mark_absent_selected":
            mark_attendance(selected_ids, today, "A")
            flash(f"Marked {len(selected_ids)} selected students ABSENT for {today}.")
            return redirect(url_for("attendance_today", class_id=class_id))
        if present_ids:
            mark_attendance(present_ids, today, "P")
        attendance_rows = get_attendance_for_class(class_id, today)
        present_set = {row["student_id"] for row in attendance_rows if row["status"] == "P"}
        absent_ids = [row["student_id"] for row in attendance_rows if row["student_id"] not in present_set]
        mark_attendance(absent_ids, today, "A")
        send_absent_notifications(absent_ids, today)
        flash(
            f"Attendance updated for class {class_id}. Present: {len(present_set)}, Absent: {len(absent_ids)}. Notifications queued."
        )
        return redirect(url_for("attendance_today", class_id=class_id))

    classes = get_classes()
    students: List[sqlite3.Row] = get_students_by_class(class_id) if class_id else []
    return render_template(
        "faculty_attendance.html",
        classes=classes,
        selected_class=class_id,
        students=students,
        today=today,
    )


@app.route("/attendance/today")
def attendance_today():
    class_id = request.args.get("class_id") or ""
    today = datetime.now().strftime("%Y-%m-%d")
    rows = get_attendance_for_class(class_id, today) if class_id else []
    return render_template(
        "attendance_today.html",
        class_id=class_id,
        today=today,
        rows=rows,
    )


@app.route("/attendance/recognize", methods=["POST"])
def attendance_recognize():
    class_id = request.form.get("class_id") or ""
    file = request.files.get("image")
    today = datetime.now().strftime("%Y-%m-%d")
    recognized_rollnos: List[str] = []
    if file and class_id:
        safe_name = file.filename
        saved_path = os.path.join(UPLOAD_DIR, safe_name)
        file.save(saved_path)
        recognized_rollnos = parse_recognized_rollnos_from_filename(safe_name)
    students = get_students_by_class(class_id)
    roll_to_id = {s["roll_no"]: int(s["id"]) for s in students}
    recognized_ids = [roll_to_id[r] for r in recognized_rollnos if r in roll_to_id]
    if recognized_ids:
        mark_attendance(recognized_ids, today, "P")
    attendance_rows = get_attendance_for_class(class_id, today)
    present_set = {row["student_id"] for row in attendance_rows if row["status"] == "P"}
    absent_ids = [row["student_id"] for row in attendance_rows if row["student_id"] not in present_set]
    mark_attendance(absent_ids, today, "A")
    send_absent_notifications(absent_ids, today)
    flash(
        f"Image processed for {class_id}. Recognized present: {len(recognized_ids)}. Absent: {len(absent_ids)}. Notifications queued."
    )
    return redirect(url_for("attendance_today", class_id=class_id))


@app.route("/notifications")
def notifications():
    conn = get_db()
    rows = conn.execute(
        """
        SELECT n.id, s.roll_no, s.name, n.message, n.recipient, n.date
        FROM notifications n
        JOIN students s ON s.id = n.student_id
        ORDER BY n.id DESC
        LIMIT 100
        """
    ).fetchall()
    conn.close()
    return render_template("notifications.html", rows=rows)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

