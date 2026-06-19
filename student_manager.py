"""
student_manager.py - Manager class for CRUD operations + persistence
"""

import json
import os
from student import Student


class StudentManager:
    """
    Manages a collection of Student objects.
    Provides CRUD operations and JSON-based persistence.
    """

    def __init__(self, filepath: str = "students.json"):
        self.__students: list[Student] = []
        self.__filepath = filepath
        self._load_from_file()

    # ── Create ────────────────────────────────────────────────────────────────
    def add_student(self, name: str, age: int, email: str, course: str) -> Student:
        """Create and store a new student. Raises ValueError on duplicate email."""
        if self.find_by_email(email):
            raise ValueError(f"A student with email '{email}' already exists.")
        student = Student(name, age, email, course)
        self.__students.append(student)
        self._save_to_file()
        print(f"✅  Student '{name}' added successfully! (ID: {student.id})")
        return student

    # ── Read ──────────────────────────────────────────────────────────────────
    def get_all_students(self) -> list[Student]:
        return list(self.__students)

    def find_by_id(self, student_id: int) -> Student | None:
        for s in self.__students:
            if s.id == student_id:
                return s
        return None

    def find_by_email(self, email: str) -> Student | None:
        for s in self.__students:
            if s.email.lower() == email.lower():
                return s
        return None

    def search(self, keyword: str) -> list[Student]:
        """Search by name, course, or email (case-insensitive)."""
        kw = keyword.lower()
        return [
            s for s in self.__students
            if kw in s.name.lower()
            or kw in s.course.lower()
            or kw in s.email.lower()
        ]

    # ── Update ────────────────────────────────────────────────────────────────
    def update_student(self, student_id: int, **kwargs) -> bool:
        """
        Update one or more fields for a student.
        Valid kwargs: name, age, email, course
        """
        student = self.find_by_id(student_id)
        if not student:
            print(f"❌  No student found with ID {student_id}.")
            return False

        for field, value in kwargs.items():
            if hasattr(student, field):
                try:
                    setattr(student, field, value)
                except ValueError as e:
                    print(f"⚠️   {e}")
                    return False
            else:
                print(f"⚠️   '{field}' is not a valid field.")
                return False

        self._save_to_file()
        print(f"✅  Student ID {student_id} updated successfully.")
        return True

    def add_grade(self, student_id: int, subject: str, mark: float) -> bool:
        """Add or update a grade for a student."""
        student = self.find_by_id(student_id)
        if not student:
            print(f"❌  No student found with ID {student_id}.")
            return False
        try:
            student.add_grade(subject, mark)
            self._save_to_file()
            print(f"✅  Grade added: {subject} = {mark} for {student.name}")
            return True
        except ValueError as e:
            print(f"⚠️   {e}")
            return False

    # ── Delete ────────────────────────────────────────────────────────────────
    def delete_student(self, student_id: int) -> bool:
        student = self.find_by_id(student_id)
        if not student:
            print(f"❌  No student found with ID {student_id}.")
            return False
        self.__students.remove(student)
        self._save_to_file()
        print(f"🗑️   Student '{student.name}' (ID: {student_id}) deleted.")
        return True

    # ── Reports ───────────────────────────────────────────────────────────────
    def display_all(self):
        if not self.__students:
            print("📭  No students registered yet.")
            return
        print(f"\n{'─'*70}")
        print(f"  {'STUDENT RECORDS':^66}")
        print(f"{'─'*70}")
        for s in self.__students:
            print(f"  {s}")
        print(f"{'─'*70}\n")

    def top_students(self, n: int = 3) -> list[Student]:
        """Return top N students by average grade."""
        ranked = sorted(self.__students, key=lambda s: s.get_average(), reverse=True)
        return ranked[:n]

    def course_summary(self) -> dict:
        """Return count of students per course."""
        summary = {}
        for s in self.__students:
            summary[s.course] = summary.get(s.course, 0) + 1
        return summary

    def statistics(self):
        """Print overall statistics."""
        if not self.__students:
            print("📭  No data to compute statistics.")
            return
        averages = [s.get_average() for s in self.__students]
        print(f"\n📊  STATISTICS")
        print(f"   Total Students : {len(self.__students)}")
        print(f"   Class Average  : {round(sum(averages)/len(averages), 2)}%")
        print(f"   Highest Avg    : {max(averages)}%")
        print(f"   Lowest Avg     : {min(averages)}%")
        print(f"\n📚  COURSE BREAKDOWN")
        for course, count in self.course_summary().items():
            print(f"   {course:<25} → {count} student(s)")
        print()

    # ── Persistence ───────────────────────────────────────────────────────────
    def _save_to_file(self):
        data = [s.to_dict() for s in self.__students]
        with open(self.__filepath, "w") as f:
            json.dump(data, f, indent=4)

    def _load_from_file(self):
        if not os.path.exists(self.__filepath):
            return
        try:
            with open(self.__filepath, "r") as f:
                data = json.load(f)
            for item in data:
                s = Student(item["name"], item["age"], item["email"], item["course"])
                for subject, mark in item.get("grades", {}).items():
                    s.add_grade(subject, mark)
                self.__students.append(s)
                # Sync the class-level counter
                if s.id >= Student._id_counter:
                    Student._id_counter = s.id + 1
        except (json.JSONDecodeError, KeyError):
            print("⚠️   Could not load saved data. Starting fresh.")

    def __len__(self) -> int:
        return len(self.__students)

    def __repr__(self) -> str:
        return f"StudentManager(students={len(self.__students)})"
