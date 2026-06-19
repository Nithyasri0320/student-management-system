"""
test_student_system.py - Unit tests for Student Management System
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from student import Student
from student_manager import StudentManager


class TestStudent(unittest.TestCase):

    def setUp(self):
        Student._id_counter = 100  # Reset to avoid conflicts
        self.student = Student("Arjun Kumar", 20, "arjun@example.com", "Computer Science")

    def test_creation(self):
        self.assertEqual(self.student.name, "Arjun Kumar")
        self.assertEqual(self.student.age, 20)
        self.assertEqual(self.student.email, "arjun@example.com")
        self.assertEqual(self.student.course, "Computer Science")

    def test_add_grade_valid(self):
        self.student.add_grade("Math", 85)
        self.assertIn("Math", self.student.grades)
        self.assertEqual(self.student.grades["Math"], 85)

    def test_add_grade_invalid(self):
        with self.assertRaises(ValueError):
            self.student.add_grade("Math", 150)

    def test_average_no_grades(self):
        self.assertEqual(self.student.get_average(), 0.0)

    def test_average_with_grades(self):
        self.student.add_grade("Math", 90)
        self.student.add_grade("Science", 80)
        self.assertEqual(self.student.get_average(), 85.0)

    def test_gpa_grades(self):
        self.student.add_grade("Math", 95)
        self.assertEqual(self.student.get_gpa(), "A")
        self.student.add_grade("English", 50)
        # avg = 72.5 → C
        self.assertEqual(self.student.get_gpa(), "C")

    def test_invalid_age(self):
        with self.assertRaises(ValueError):
            self.student.age = -5

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            self.student.email = "notanemail"

    def test_to_dict(self):
        self.student.add_grade("Math", 90)
        d = self.student.to_dict()
        self.assertEqual(d["name"], "Arjun Kumar")
        self.assertIn("Math", d["grades"])

    def test_str_repr(self):
        self.assertIn("Arjun Kumar", str(self.student))
        self.assertIn("Student(", repr(self.student))


class TestStudentManager(unittest.TestCase):

    TEST_FILE = "test_students.json"

    def setUp(self):
        Student._id_counter = 200
        self.mgr = StudentManager(filepath=self.TEST_FILE)

    def tearDown(self):
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_add_student(self):
        s = self.mgr.add_student("Priya", 22, "priya@example.com", "AI/ML")
        self.assertEqual(len(self.mgr), 1)
        self.assertEqual(s.name, "Priya")

    def test_duplicate_email(self):
        self.mgr.add_student("Priya", 22, "priya@example.com", "AI/ML")
        with self.assertRaises(ValueError):
            self.mgr.add_student("Ravi", 21, "priya@example.com", "Data Science")

    def test_find_by_id(self):
        s = self.mgr.add_student("Karthik", 19, "karthik@example.com", "Mech")
        found = self.mgr.find_by_id(s.id)
        self.assertEqual(found.name, "Karthik")

    def test_find_by_email(self):
        self.mgr.add_student("Ananya", 21, "ananya@example.com", "Civil")
        found = self.mgr.find_by_email("ananya@example.com")
        self.assertIsNotNone(found)

    def test_search(self):
        self.mgr.add_student("Rohit", 20, "rohit@example.com", "EEE")
        results = self.mgr.search("rohit")
        self.assertEqual(len(results), 1)

    def test_update_student(self):
        s = self.mgr.add_student("Meena", 23, "meena@example.com", "IT")
        self.mgr.update_student(s.id, name="Meena Raj", age=24)
        updated = self.mgr.find_by_id(s.id)
        self.assertEqual(updated.name, "Meena Raj")
        self.assertEqual(updated.age, 24)

    def test_add_grade(self):
        s = self.mgr.add_student("Dev", 20, "dev@example.com", "CS")
        self.mgr.add_grade(s.id, "OS", 88)
        self.assertEqual(s.grades["OS"], 88)

    def test_delete_student(self):
        s = self.mgr.add_student("Sam", 21, "sam@example.com", "BCA")
        self.mgr.delete_student(s.id)
        self.assertIsNone(self.mgr.find_by_id(s.id))
        self.assertEqual(len(self.mgr), 0)

    def test_top_students(self):
        s1 = self.mgr.add_student("A", 20, "a@x.com", "CS")
        s2 = self.mgr.add_student("B", 21, "b@x.com", "CS")
        s1.add_grade("Math", 90)
        s2.add_grade("Math", 70)
        top = self.mgr.top_students(1)
        self.assertEqual(top[0].name, "A")

    def test_persistence(self):
        self.mgr.add_student("Persist", 22, "persist@x.com", "Data")
        mgr2 = StudentManager(filepath=self.TEST_FILE)
        self.assertEqual(len(mgr2), 1)
        self.assertEqual(mgr2.get_all_students()[0].name, "Persist")


if __name__ == "__main__":
    unittest.main(verbosity=2)
