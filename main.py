"""
main.py - Interactive CLI for the Student Management System
"""

from student_manager import StudentManager


def print_menu():
    print("""
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
""")


def get_int(prompt: str) -> int | None:
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("⚠️   Please enter a valid number.")
        return None


def get_float(prompt: str) -> float | None:
    try:
        return float(input(prompt).strip())
    except ValueError:
        print("⚠️   Please enter a valid number.")
        return None


def add_student(mgr: StudentManager):
    print("\n── Add New Student ─────────────────────")
    name = input("  Name   : ").strip()
    age = get_int("  Age    : ")
    email = input("  Email  : ").strip()
    course = input("  Course : ").strip()
    if not all([name, age, email, course]):
        print("⚠️   All fields are required.")
        return
    try:
        mgr.add_student(name, age, email, course)
    except ValueError as e:
        print(f"❌  {e}")


def search_student(mgr: StudentManager):
    print("\n── Search Student ──────────────────────")
    keyword = input("  Enter name / email / course : ").strip()
    results = mgr.search(keyword)
    if results:
        for s in results:
            print(f"  {s}")
    else:
        print("  No matching records found.")


def update_student(mgr: StudentManager):
    print("\n── Update Student ──────────────────────")
    sid = get_int("  Enter Student ID : ")
    if sid is None:
        return
    student = mgr.find_by_id(sid)
    if not student:
        print(f"❌  No student with ID {sid}.")
        return
    print(f"  Editing: {student}")
    print("  (Leave blank to keep current value)")
    fields = {}
    name = input(f"  Name   [{student.name}]: ").strip()
    if name:
        fields["name"] = name
    age_str = input(f"  Age    [{student.age}]: ").strip()
    if age_str:
        try:
            fields["age"] = int(age_str)
        except ValueError:
            print("⚠️   Invalid age, skipping.")
    email = input(f"  Email  [{student.email}]: ").strip()
    if email:
        fields["email"] = email
    course = input(f"  Course [{student.course}]: ").strip()
    if course:
        fields["course"] = course
    if fields:
        mgr.update_student(sid, **fields)
    else:
        print("  No changes made.")


def add_grade(mgr: StudentManager):
    print("\n── Add / Update Grade ──────────────────")
    sid = get_int("  Student ID : ")
    if sid is None:
        return
    subject = input("  Subject    : ").strip()
    mark = get_float("  Mark (0–100): ")
    if mark is None or not subject:
        return
    mgr.add_grade(sid, subject, mark)


def view_grades(mgr: StudentManager):
    print("\n── Student Grades ──────────────────────")
    sid = get_int("  Student ID : ")
    if sid is None:
        return
    student = mgr.find_by_id(sid)
    if not student:
        print(f"❌  No student with ID {sid}.")
        return
    print(f"\n  Student  : {student.name}")
    print(f"  Course   : {student.course}")
    if not student.grades:
        print("  No grades recorded yet.")
    else:
        print(f"  {'Subject':<20} {'Mark':>6}")
        print(f"  {'─'*28}")
        for subject, mark in student.grades.items():
            print(f"  {subject:<20} {mark:>6.1f}")
        print(f"  {'─'*28}")
        print(f"  {'Average':<20} {student.get_average():>6.1f}  (Grade: {student.get_gpa()})")


def delete_student(mgr: StudentManager):
    print("\n── Delete Student ──────────────────────")
    sid = get_int("  Student ID : ")
    if sid is None:
        return
    student = mgr.find_by_id(sid)
    if not student:
        print(f"❌  No student with ID {sid}.")
        return
    confirm = input(f"  Delete '{student.name}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        mgr.delete_student(sid)
    else:
        print("  Cancelled.")


def top_students(mgr: StudentManager):
    print("\n── Top Performers ──────────────────────")
    n = get_int("  How many top students to show? : ") or 3
    top = mgr.top_students(n)
    if not top:
        print("  No students found.")
    else:
        for rank, s in enumerate(top, 1):
            print(f"  #{rank}  {s}")


def main():
    mgr = StudentManager()
    print("\n  Welcome to Student Management System! 🎓")

    while True:
        print_menu()
        choice = input("  ➤  Choose an option: ").strip()

        match choice:
            case "1":
                add_student(mgr)
            case "2":
                mgr.display_all()
            case "3":
                search_student(mgr)
            case "4":
                update_student(mgr)
            case "5":
                add_grade(mgr)
            case "6":
                view_grades(mgr)
            case "7":
                delete_student(mgr)
            case "8":
                top_students(mgr)
            case "9":
                mgr.statistics()
            case "0":
                print("\n  Bye! Keep learning 🚀\n")
                break
            case _:
                print("⚠️   Invalid option. Try again.")


if __name__ == "__main__":
    main()
