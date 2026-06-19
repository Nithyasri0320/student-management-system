# 🎓 OOP-Based Student Management System

A clean, fully object-oriented **Student Management System** built in Python — with CRUD operations, grade tracking, search, statistics, and JSON-based persistence.

---

## 📁 Project Structure

```
student_management_system/
├── student.py            # Student class (encapsulation, properties)
├── student_manager.py    # StudentManager class (CRUD + persistence)
├── main.py               # CLI entry point
├── test_student_system.py# Unit tests (unittest)
├── students.json         # Auto-generated data store
└── README.md
```

---

## 🧠 OOP Concepts Used

| Concept | Where Applied |
|---|---|
| **Encapsulation** | Private attributes with `@property` getters/setters in `Student` |
| **Abstraction** | `StudentManager` hides all data logic behind clean methods |
| **Data Hiding** | `__name`, `__grades`, etc. are truly private |
| **Class Variables** | `_id_counter` for auto-incrementing IDs |
| **Dunder Methods** | `__str__`, `__repr__`, `__len__` |
| **Serialization** | `to_dict()` + JSON file persistence |

---

## ✨ Features

- ✅ Add, View, Update, Delete students
- 🔍 Search by name, email, or course
- 📊 Add grades per subject with auto-calculated average & GPA (A–F)
- 🏆 Top performers leaderboard
- 📈 Class statistics and course breakdown
- 💾 Auto-save to `students.json` — data persists across runs
- 🧪 Unit tests with full coverage

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+

### Run the App

```bash
git clone https://github.com/your-username/student-management-system.git
cd student-management-system
python main.py
```

### Run Tests

```bash
python -m pytest test_student_system.py -v
# or
python test_student_system.py
```

---

## 🖥️ CLI Menu

```
╔══════════════════════════════════════════╗
║      🎓  STUDENT MANAGEMENT SYSTEM       ║
╠══════════════════════════════════════════╣
║  1. Add New Student                      ║
║  2. View All Students                    ║
║  3. Search Student                       ║
║  4. Update Student Details               ║
║  5. Add / Update Grade                   ║
║  6. View Student Grades                  ║
║  7. Delete Student                       ║
║  8. Top Performers                       ║
║  9. Statistics & Course Summary          ║
║  0. Exit                                 ║
╚══════════════════════════════════════════╝
```

---

## 📦 Sample Data Flow

```python
manager = StudentManager()

# Add students
manager.add_student("Arjun", 20, "arjun@mail.com", "Computer Science")
manager.add_student("Priya", 22, "priya@mail.com", "AI/ML")

# Add grades
manager.add_grade(1, "Math", 92)
manager.add_grade(1, "OS", 88)

# View all
manager.display_all()

# Statistics
manager.statistics()
```

---

## 📊 Grade Scale

| Average | Grade |
|---------|-------|
| 90–100  | A     |
| 80–89   | B     |
| 70–79   | C     |
| 60–69   | D     |
| Below 60| F     |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

---

## 📄 License

MIT License — free to use and modify.
