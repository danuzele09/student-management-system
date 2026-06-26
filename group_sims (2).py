"""
Student Information Management System (SIMS)

"""

import os  # Added for file existence checking

# ==================== DATA STORAGE ====================
# Student data
student_names = []
student_ages = []
student_departments = []
student_marks = []
student_grades = []

# User data files
USER_FILE = "users.txt"
current_user = None
current_role = None

# ==================== USER AUTHENTICATION FUNCTIONS ====================
def load_users():
    """Load users from file into a dictionary."""
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            for line in file:
                if ',' in line:
                    username, password, role = line.strip().split(',')
                    users[username] = {'password': password, 'role': role}
    return users

def save_users(users):
    """Save users dictionary to file."""
    with open(USER_FILE, 'w') as file:
        for username, info in users.items():
            file.write(f"{username},{info['password']},{info['role']}\n")

def user_login():
    """Handle user login with username and password."""
    print("\n" + "="*50)
    print("USER LOGIN")
    print("="*50)
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    users = load_users()
    
    if username not in users:
        print("❌ Wrong username.")
        return None, None
    elif users[username]['password'] != password:
        print("❌ Wrong password.")
        return None, None
    else:
        print(f"\n✅ Login successful! Welcome {username}")
        return username, users[username]['role']

def user_registration():
    """Handle new user registration."""
    print("\n" + "="*50)
    print("USER REGISTRATION")
    print("="*50)
    
    # Check if user is already logged in
    if current_user:
        print("You are already logged in!")
        print("Please logout first to register a new account.")
        return
    
    # Get username
    username = input("Enter username: ").strip()
    
    users = load_users()
    
    # Check if username exists
    if username in users:
        print("❌ Username already exists!")
        return
    
    # Check if username is empty
    if username == "":
        print("❌ Name cannot be empty.")
        return
    
    # Age validation
    while True:
        try:
            age = int(input("Enter age: "))
            if age >= 15:
                break
            print("❌ Age must be at least 15.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Check age restriction
    if age < 15:
        print("\n" + "!"*50)
        print("ERROR: You must be 15 or older to register.")
        print("Exiting program...")
        print("!"*50)
        
        # Save any existing data before exiting
        save_student_data()
        exit()
    
    # Get password
    password = input("Enter password: ").strip()
    
    # Check if admin exists
    admin_exists = False
    for user_info in users.values():
        if user_info['role'] == 'admin':
            admin_exists = True
            break
    
    # Role selection
    if not admin_exists:
        # First registration can be admin
        print("\nSelect your role:")
        print("1. Admin (full access)")
        print("2. Teacher (can manage students)")
        print("3. Student (view only)")
        
        while True:
            role_choice = input("Enter choice (1-3): ").strip()
            if role_choice == '1':
                role = 'admin'
                break
            elif role_choice == '2':
                role = 'teacher'
                break
            elif role_choice == '3':
                role = 'student'
                break
            else:
                print("❗ Invalid choice. Enter 1, 2, or 3.")
    else:
        # Subsequent registrations
        print("\nSelect your role:")
        print("1. Teacher (can manage students)")
        print("2. Student (view only)")
        
        while True:
            role_choice = input("Enter choice (1-2): ").strip()
            if role_choice == '1':
                role = 'teacher'
                break
            elif role_choice == '2':
                role = 'student'
                break
            else:
                print("❗ Invalid choice. Enter 1 or 2.")
    
    # Add new user
    users[username] = {'password': password, 'role': role}
    save_users(users)
    
    print(f"\n ✅ User '{username}' registered successfully as {role}!")
    print("\nYou can now login with your new account.")

# ==================== HELPER FUNCTIONS ====================
def get_grade_from_mark(mark):
    """Converts a numerical mark into a letter grade."""
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"

def save_student_data():
    """Saves student data to file."""
    with open("students.txt", "w") as file:
        for i in range(len(student_names)):
            file.write(f"{student_names[i]},{student_ages[i]},{student_departments[i]},{student_marks[i]},{student_grades[i]}\n")

def load_student_data():
    """Loads student data from file."""
    global student_names, student_ages, student_departments, student_marks, student_grades
    
    try:
        with open("students.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    student_names.append(parts[0])
                    student_ages.append(int(parts[1]))
                    student_departments.append(parts[2])
                    student_marks.append(float(parts[3]))
                    student_grades.append(parts[4])
        print("☑️ Student data loaded.")
    except:
        print("No existing student data found. Starting fresh.")

# ==================== STUDENT MANAGEMENT FUNCTIONS ====================
def add_new_students():
    """Registers multiple students with input validation."""
    print("\n" + "="*50)
    print("REGISTER NEW STUDENTS")
    print("="*50)
    
    # Check permission
    if current_role not in ["admin", "teacher"]:
        print("❌ Access denied. Only admins and teachers can add students.")
        return
    
    # Get number of students to register
    while True:
        try:
            student_count = int(input("How many students do you want to add? "))
            if student_count > 0:
                break
            else:
                print("Please enter a positive number.")
        except:
            print("Invalid input. Please enter a number.")
    
    # Register each student
    for student_num in range(1, student_count + 1):
        print(f"\n--- Student {student_num} of {student_count} ---")
        
        # Get and validate name
        while True:
            name = input("Full Name: ").strip()
            if name:
                break
            print("Name cannot be empty. Try again.")
            continue  # Using continue
        
        # Get and validate age
        while True:
            try:
                age = int(input("Age: "))
                if age >= 15:
                    break
                else:
                    print("Age must be 15 or older.")
            except:
                print("Please enter a valid age (number).")
        
        # Get and validate department
        while True:
            department = input("Department: ").strip()
            if department:
                break
            print("Department cannot be empty.")
        
        # Get and validate mark
        while True:
            try:
                mark = float(input("Mark (0-100): "))
                if 0 <= mark <= 100:
                    break
                else:
                    print("Mark must be between 0 and 100.")
            except:
                print("Please enter a valid mark (number).")
        
        # Calculate grade based on mark
        grade = get_grade_from_mark(mark)
        
        # Store all student data
        student_names.append(name)
        student_ages.append(age)
        student_departments.append(department)
        student_marks.append(mark)
        student_grades.append(grade)
        
        print(f"✅ Student '{name}' added successfully with grade {grade}")
    
    save_student_data()
    print(f"\n✅ {student_count} student(s) registered successfully!")

def display_all_students():
    """Shows all registered students in a formatted table."""
    print("\n" + "="*50)
    print("ALL STUDENT RECORDS")
    print("="*50)
    
    if len(student_names) == 0:
        print("No students registered yet.")
        return
    
    # Create formatted header
    print(f"{'No.':<4} {'Name':<20} {'Age':<5} {'Department':<15} {'Mark':<6} {'Grade':<6}")
    print("-" * 60)
    
    # Display each student with their details
    for i in range(len(student_names)):
        print(f"{i+1:<4} {student_names[i]:<20} {student_ages[i]:<5} "
              f"{student_departments[i]:<15} {student_marks[i]:<6.1f} {student_grades[i]:<6}")

def find_best_student():
    """Finds and displays the student with the highest mark."""
    print("\n" + "="*50)
    print("📚TOP PERFORMING STUDENT")
    print("="*50)
    
    if len(student_marks) == 0:
        print("No students registered yet.")
        return
    
    # Find the index of the highest mark
    highest_mark = max(student_marks)
    top_index = student_marks.index(highest_mark)
    
    print(f"🏆 Top Student: {student_names[top_index]}")
    print(f"   Department: {student_departments[top_index]}")
    print(f"   Mark: {student_marks[top_index]:.1f}")
    print(f"   Grade: {student_grades[top_index]}")

def calculate_class_average():
    """Calculates and displays the average mark of all students."""
    print("\n" + "="*50)
    print("CLASS PERFORMANCE STATISTICS 📊")
    print("="*50)
    
    if len(student_marks) == 0:
        print("No students registered yet.")
        return
    
    # Calculate average
    total_marks = sum(student_marks)
    average = total_marks / len(student_marks)
    
    print(f"Total Students: {len(student_names)}")
    print(f"Total Marks: {total_marks:.1f}")
    print(f"Average Mark: {average:.2f}")
    
    # Show grade distribution
    print("\nGrade Distribution:")
    for grade in ['A', 'B', 'C', 'D', 'F']:
        count = student_grades.count(grade)
        print(f"  {grade}: {count} student(s)")

def show_student_table():
    """BONUS: Displays a formatted grade table."""
    print("\n" + "="*50)
    print("STUDENT GRADE TABLE")
    print("="*50)
    
    if len(student_names) == 0:
        print("No students to display.")
        return
    
    # Create table header
    header = f"{'Name':<20}{'Age':<6}{'Dept':<15}{'Mark':<8}{'Grade':<6}"
    print(header)
    print("-" * 55)
    
    # Display each student's information
    for i in range(len(student_names)):
        row = f"{student_names[i]:<20}{student_ages[i]:<6}" \
              f"{student_departments[i]:<15}{student_marks[i]:<8.1f}{student_grades[i]:<6}"
        print(row)

def display_patterns():
    """BONUS: Shows two different patterns using nested loops."""
    print("\n" + "="*50)
    print("PATTERN DISPLAY")
    print("="*50)
    
    print("\nPattern 1: Increasing Stars")
    for row in range(1, 6):
        for star in range(row):
            print("📜", end="")
        print()
    
    print("\nPattern 2: Number Pyramid")
    for row in range(1, 6):
        for number in range(row):
            print(row, end="")
        print()

# ==================== ROLE-BASED MENUS ====================
def admin_menu():
    """Menu for admin users."""
    global current_user, current_role
    
    while True:
        print("\n" + "="*50)
        print(f"ADMIN PANEL - Logged in as: {current_user}")
        print("="*50)
        print("1️⃣. Register New Students")
        print("2️⃣. View All Students")
        print("3️⃣. View Top Student")
        print("4️⃣. View Class Average")
        print("5️⃣. Student Grade Table")
        print("6️⃣. Display Patterns")
        print("7️⃣. Register New User")
        print("8️⃣. Logout")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            add_new_students()
        elif choice == "2":
            display_all_students()
        elif choice == "3":
            find_best_student()
        elif choice == "4":
            calculate_class_average()
        elif choice == "5":
            show_student_table()
        elif choice == "6":
            display_patterns()
        elif choice == "7":
            user_registration()
        elif choice == "8":
            print(f"\nLogging out {current_user}...")
            current_user = None
            current_role = None
            print("✓ Logged out successfully!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

def teacher_menu():
    """Menu for teacher users."""
    global current_user, current_role
    
    while True:
        print("\n" + "="*50)
        print(f"TEACHER PANEL - Logged in as: {current_user}")
        print("="*50)
        print("1️⃣. Register New Students")
        print("2️⃣. View All Students")
        print("3️⃣. View Top Student")
        print("4️⃣. View Class Average")
        print("5️⃣. Student Grade Table")
        print("6️⃣. Display Patterns")
        print("7️⃣. Logout")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            add_new_students()
        elif choice == "2":
            display_all_students()
        elif choice == "3":
            find_best_student()
        elif choice == "4":
            calculate_class_average()
        elif choice == "5":
            show_student_table()
        elif choice == "6":
            display_patterns()
        elif choice == "7":
            print(f"\nLogging out {current_user}...")
            current_user = None
            current_role = None
            print("✅ Logged out successfully!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

def student_menu():
    """Menu for student users."""
    global current_user, current_role
    
    while True:
        print("\n" + "="*50)
        print(f"STUDENT PANEL - Logged in as: {current_user}")
        print("="*50)
        print("1️⃣. View All Students")
        print("2️⃣. View Top Student")
        print("3️⃣. View Class Average")
        print("4️⃣. Logout")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            display_all_students()
        elif choice == "2":
            find_best_student()
        elif choice == "3":
            calculate_class_average()
        elif choice == "4":
            print(f"\nLogging out {current_user}...")
            current_user = None
            current_role = None
            print("☑️ Logged out successfully!")
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 4.")

def guest_menu():
    """Menu for guests (no login required)."""
    while True:
        print("\n" + "="*50)
        print("GUEST ACCESS")
        print("="*50)
        print("1️⃣. View All Students")
        print("2️⃣. View Top Student")
        print("3️⃣. View Class Average")
        print("4️⃣. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            display_all_students()
        elif choice == "2":
            find_best_student()
        elif choice == "3":
            calculate_class_average()
        elif choice == "4":
            break  # Using break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

# ==================== MAIN PROGRAM ====================
def run_program():
    """Main program loop with authentication system."""
    global current_user, current_role
    
    # Load existing data
    load_student_data()
    
    # Create default accounts if no users exist
    users = load_users()
    if not users:
        print("\nNo users found. Creating default accounts...♻️♻️♻️")
        users['admin'] = {'password': 'admin123', 'role': 'admin'}
        users['teacher'] = {'password': 'teacher123', 'role': 'teacher'}
        users['student'] = {'password': 'student123', 'role': 'student'}
        save_users(users)
        print(" ✅Default accounts created:")
        print("  - admin / admin123 (Admin)")
        print("  - teacher / teacher123 (Teacher)")
        print("  - student / student123 (Student)")
    
    print("\n" + "="*60)
    print("👩‍🎓👩‍🎓👩‍🎓STUDENT INFORMATION MANAGEMENT SYSTEM👨‍🎓👨‍🎓👨‍🎓")
    print("="*60)
    
    while True:
        # Show login status
        if current_user:
            print(f"\nCurrently logged in as: {current_user} ({current_role})")
            print("-" * 40)
        
        # Main menu

        print(f"\n📖📖📖WELCOME📖📖📖")
        print("1. Login")
        print("2. Register New Account")
        print("3. Continue as Guest")
        print("4. Exit Program")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            username, role = user_login()
            if username:
                current_user = username
                current_role = role
                
                # Go to appropriate menu based on role
                if role == "admin":
                    admin_menu()
                elif role == "teacher":
                    teacher_menu()
                elif role == "student":
                    student_menu()
        
        elif choice == "2":
            user_registration()
        
        elif choice == "3":
            guest_menu()
        
        elif choice == "4":
            print("\nThank you for using the Student Management System!")
            print("Saving data...")
            save_student_data()
            print("👋Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

# Start the program
if __name__ == "__main__":
    run_program()