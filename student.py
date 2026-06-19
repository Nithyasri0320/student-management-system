"""
student.py - Student entity class with encapsulation
"""


class Student:
    """Represents a single student with personal and academic details."""

    _id_counter = 1  # Class-level auto-increment ID

    def __init__(self, name: str, age: int, email: str, course: str):
        self.__id = Student._id_counter
        Student._id_counter += 1
        self.__name = name
        self.__age = age
        self.__email = email
        self.__course = course
        self.__grades: dict[str, float] = {}

    # ── Getters ──────────────────────────────────────────────────────────────
    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def age(self) -> int:
        return self.__age

    @property
    def email(self) -> str:
        return self.__email

    @property
    def course(self) -> str:
        return self.__course

    @property
    def grades(self) -> dict:
        return dict(self.__grades)

    # ── Setters ──────────────────────────────────────────────────────────────
    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self.__name = value.strip()

    @age.setter
    def age(self, value: int):
        if not (1 <= value <= 120):
            raise ValueError("Age must be between 1 and 120.")
        self.__age = value

    @email.setter
    def email(self, value: str):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address.")
        self.__email = value.strip()

    @course.setter
    def course(self, value: str):
        if not value.strip():
            raise ValueError("Course cannot be empty.")
        self.__course = value.strip()

    # ── Grade methods ─────────────────────────────────────────────────────────
    def add_grade(self, subject: str, mark: float):
        """Add or update a grade for a subject (0–100)."""
        if not (0 <= mark <= 100):
            raise ValueError("Grade must be between 0 and 100.")
        self.__grades[subject] = mark

    def get_average(self) -> float:
        """Return the average grade, or 0 if no grades exist."""
        if not self.__grades:
            return 0.0
        return round(sum(self.__grades.values()) / len(self.__grades), 2)

    def get_gpa(self) -> str:
        """Return letter-grade equivalent based on average."""
        avg = self.get_average()
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"

    # ── Dunder methods ────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return (
            f"[ID: {self.__id}] {self.__name} | Age: {self.__age} | "
            f"Email: {self.__email} | Course: {self.__course} | "
            f"Avg: {self.get_average()}% ({self.get_gpa()})"
        )

    def __repr__(self) -> str:
        return f"Student(id={self.__id}, name={self.__name!r})"

    def to_dict(self) -> dict:
        """Serialize student to a dictionary (for JSON storage)."""
        return {
            "id": self.__id,
            "name": self.__name,
            "age": self.__age,
            "email": self.__email,
            "course": self.__course,
            "grades": self.__grades,
        }
