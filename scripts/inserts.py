import faker
import time
from collections import defaultdict
import random
import os
fake = faker.Faker()
DEBUG_MODE = False # Set to True to print debug info, False to skip. Should be False as default for performance reasons
NUM_LECTURERS = 150
NUM_COURSES = 500
NUM_STUDENTS = 100000
NUM_ADMINS = 10
NUM_USERS = NUM_LECTURERS + NUM_STUDENTS + NUM_ADMINS
MAX_COURSES_PER_STUDENT = 6
MIN_STUDENTS_PER_COURSE = 9
MIN_COURSES_PER_TEACHER = 1
MAX_COURSES_PER_TEACHER = 5
MAX_TEACHERS_PER_COURSE = 1
MIN_COURSES_PER_STUDENT = 3

def gen_users():
    users = []
    for user_id in range(1, NUM_USERS + 1):
        # Append the user_id to guarantee 100% uniqueness, faker will generate duplicates when creating 100k entries, so we combine it with the username to ensure uniqueness while keeping it realistic.
        raw_username = f"{fake.user_name()}_{user_id}"
        raw_password = fake.password()
        # Escape backslashes and single quotes for SQL safety
        username = raw_username.replace('\\', '\\\\').replace("'", "''")
        password = raw_password.replace('\\', '\\\\').replace("'", "''")
        
        users.append((user_id, username, password))
    return users

def gen_admins(users):

    admins = []
    for admin_id in range(1, NUM_ADMINS + 1):
        first_name = fake.first_name().replace("'", "''")
        last_name = fake.last_name().replace("'", "''")
        admins.append((admin_id, first_name, last_name, users[admin_id-1][0]))
    return admins

def gen_courses():
    courses = []
    
    # Use of a dictionary to and corse creation loop to get realistic & suitable course names
    prefixes = [
        "Introduction to", "Advanced", "Principles of", "Fundamentals of", 
        "Applied", "Topics in", "Foundations of", "Contemporary", 
        "Modern", "Theoretical", "Experimental", "Survey of", 
        "Issues in", "Perspectives on", "Research Methods in", "Seminar in"
    ]
    
    #Subjects (Grouped by Faculty)
    subjects = [
        # Tech & Engineering
        "Computer Science", "Software Engineering", "Artificial Intelligence", "Machine Learning", 
        "Data Structures", "Algorithm Analysis", "Operating Systems", "Computer Networks", 
        "Database Systems", "Cybersecurity", "Web Development", "Cloud Computing", 
        "Human-Computer Interaction", "Robotics", "Cryptography", "Information Systems",
        # Math & Sciences
        "Calculus", "Linear Algebra", "Discrete Mathematics", "Differential Equations", 
        "Statistics", "Probability", "Quantum Mechanics", "Organic Chemistry", 
        "Molecular Biology", "Genetics", "Astrophysics", "Thermodynamics", 
        "Ecology", "Earth Science", "Oceanography", "Environmental Science",
        # Business & Economics
        "Microeconomics", "Macroeconomics", "Financial Accounting", "Marketing Management", 
        "Business Ethics", "Corporate Finance", "Business Law", "Entrepreneurship", 
        "Supply Chain Management", "Organizational Behavior", "Human Resource Management",
        # Humanities & Social Sciences
        "Psychology", "Sociology", "Anthropology", "Political Science", "International Relations", 
        "Philosophy", "Ethics", "World History", "European History", "Creative Writing", 
        "Linguistics", "Literature", "Art History", "Music Theory", "Cognitive Science",
        # Health & Applied
        "Public Health", "Anatomy", "Physiology", "Neuroscience", "Nutrition", 
        "Kinesiology", "Epidemiology", "Pharmacology", "Nursing Practice", 
        "Physical Therapy", "Occupational Therapy", "Sports Medicine", 
        "Biomechanics", "Immunology", "Pathology", "Health Informatics", 
        "Bioethics", "Toxicology", "Gerontology", "Medical Imaging"
    ]
    
    suffixes = ["I", "II", "III", "IV", "Lab", "Seminar", "Practicum", "Workshop", "Independent Study"]

    # Tracking for what has already been used to ensure uniqueness
    used_names = set()
    used_codes = set() 

    for course_id in range(1, NUM_COURSES + 1):
        # --- Generate Unique Course Name ---
        while True:
            subject = random.choice(subjects)
            name_format = random.choice([1, 2, 3])
            
            if name_format == 1:
                course_name = f"{random.choice(prefixes)} {subject}"
            elif name_format == 2:
                course_name = f"{subject} {random.choice(suffixes)}"
            else:
                course_name = f"{subject} {random.randint(100, 599)}" 
                
            if course_name not in used_names:
                used_names.add(course_name)
                break

        # Generate Realistic, Unique Course Code ---
        # Strip spaces/punctuation, grab the first 4 letters, and uppercase them
        # "Machine Learning" -> "MACH", "Computer Science" -> "COMP"
        subject_prefix = "".join([char for char in subject if char.isalpha()])[:4].upper()
        
        while True:
            # Combine the 4-letter prefix with a random 4-digit number
            course_code = f"{subject_prefix}{random.randint(1000, 9999)}"
            
            # Ensure we haven't accidentally generated this exact code before
            if course_code not in used_codes:
                used_codes.add(course_code)
                break
        
        courses.append((course_id, course_name, course_code))
        
    return courses

def gen_students(users):
    s_id_counter = 1
    students = []
    for student_id in range(NUM_ADMINS + 1, NUM_ADMINS + NUM_STUDENTS + 1):
        student_fname = fake.first_name().replace("'", "''")
        student_lname = fake.last_name().replace("'", "''")
        students.append((s_id_counter, student_fname, student_lname, users[student_id-1][0]))
        s_id_counter += 1
    return students

def gen_lecturers(users):
    l_id_counter = 1
    lecturers = []
    for lecturer_id in range(NUM_ADMINS + NUM_STUDENTS + 1, NUM_ADMINS + NUM_STUDENTS + NUM_LECTURERS + 1):
        lecturer_fname = fake.first_name().replace("'", "''")
        lecturer_lname = fake.last_name().replace("'", "''")
        lecturers.append((l_id_counter, lecturer_fname, lecturer_lname, users[lecturer_id-1][0]))
        l_id_counter += 1
    return lecturers

def gen_teachers(lecturers, courses):
    # --- Step 1: build capacity pool ---
    lecturer_pool = []
    for lecturer in lecturers:
        lecturer_pool.extend([lecturer[0]] * MAX_COURSES_PER_TEACHER)

    # Shuffle for randomness
    random.shuffle(lecturer_pool)

    # --- Step 2: assign courses ---
    teachers = []
    for i, course in enumerate(courses):
        if i >= len(lecturer_pool):
            raise ValueError("Not enough lecturer capacity for all courses")

        teachers.append((course[0], lecturer_pool[i]))

    # --- Step 3: ensure each lecturer has at least one course ---
    assigned = set(lid for _, lid in teachers)
    unassigned = [l[0] for l in lecturers if l[0] not in assigned]

    if unassigned:
        # find lecturers with extra load to donate courses
        from collections import Counter
        counts = Counter(lid for _, lid in teachers)

        donors = [l for l in counts if counts[l] > 1]

        for lecturer_id in unassigned:
            if not donors:
                break

            donor = random.choice(donors)

            # transfer one course
            for i, (course_id, lid) in enumerate(teachers):
                if lid == donor:
                    teachers[i] = (course_id, lecturer_id)
                    counts[donor] -= 1
                    counts[lecturer_id] += 1

                    if counts[donor] <= 1:
                        donors.remove(donor)
                    break

    return teachers

def gen_enrollments(students, courses):
    enrollments = []

    # Track counts
    course_counts = defaultdict(int)
    student_counts = defaultdict(int)

    # Track what each student is already in (avoid duplicates)
    student_courses = defaultdict(set)

    # Step 1: initial random assignment
    for student in students:
        student_id = student[0]
        num_courses = random.randint(MIN_COURSES_PER_STUDENT, MAX_COURSES_PER_STUDENT)

        selected_courses = random.sample(courses, num_courses)

        for course in selected_courses:
            course_id = course[0]

            enrollments.append((student_id, course_id))
            course_counts[course_id] += 1
            student_counts[student_id] += 1
            student_courses[student_id].add(course_id)

    # --- Step 2: fix underfilled courses efficiently ---
    # Build a list of students who can still take more courses
    available_students = set(s[0] for s in students if student_counts[s[0]] < MAX_COURSES_PER_STUDENT)

    for course in courses:
        course_id = course[0]

        while course_counts[course_id] < MIN_STUDENTS_PER_COURSE:
            if not available_students:
                # No valid students left, stop safely
                break

            # Pick a valid student
            student_id = random.choice(tuple(available_students))

            # Skip if already enrolled
            if course_id in student_courses[student_id]:
                continue

            # Add enrollment
            enrollments.append((student_id, course_id))
            course_counts[course_id] += 1
            student_counts[student_id] += 1
            student_courses[student_id].add(course_id)

            # If student reached max, remove from pool
            if student_counts[student_id] >= MAX_COURSES_PER_STUDENT:
                available_students.discard(student_id)

    return enrollments

def generate_sql_files(directory, users, admins, courses, students, lecturers, teachers, enrollments):
    os.makedirs(directory, exist_ok=True)
    print(f"Saving SQL files to ./{directory}...")

    # Helper functions to wrap SQL in high-performance transactions
    def write_header(f):
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n")
        f.write("SET UNIQUE_CHECKS = 0;\n")
        f.write("SET AUTOCOMMIT = 0;\n\n")

    def write_footer(f):
        f.write("\nCOMMIT;\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
        f.write("SET UNIQUE_CHECKS = 1;\n")
        f.write("SET AUTOCOMMIT = 1;\n")

    # 01-USERS (Chunked & ID Explicit)
    with open(os.path.join(directory, "01-users.sql"), "w", encoding="utf-8") as f:
        write_header(f)
        for i, user in enumerate(users):
            # Added 'id' to columns and {user[0]} to values
            f.write(f"INSERT IGNORE INTO users (id, username, password) VALUES ({user[0]}, '{user[1]}', '{user[2]}');\n")
            if (i + 1) % 5000 == 0:
                f.write("COMMIT;\n")
        write_footer(f)

    # 02-STUDENTS
    with open(os.path.join(directory, "02-students.sql"), "w", encoding="utf-8") as f:
        write_header(f)
        for student in students:
            f.write(f"INSERT IGNORE INTO students (first_name, last_name, user_id) VALUES ('{student[1]}', '{student[2]}', {student[3]});\n")
        write_footer(f)

    # 03-ADMINISTRATORS
    with open(os.path.join(directory, "03-administrators.sql"), "w", encoding="utf-8") as f:
        write_header(f)
        for admin in admins:
            f.write(f"INSERT IGNORE INTO administrators (first_name, last_name, user_id) VALUES ('{admin[1]}', '{admin[2]}', {admin[3]});\n")
        write_footer(f)

    # 04-LECTURERS
    with open(os.path.join(directory, "04-lecturers.sql"), "w", encoding="utf-8") as f:
        write_header(f)
        for lecturer in lecturers:
            f.write(f"INSERT IGNORE INTO lecturers (first_name, last_name, user_id) VALUES ('{lecturer[1]}', '{lecturer[2]}', {lecturer[3]});\n")
        write_footer(f)

    # 05-COURSES (Updated to use 'name' as requested)
    with open(os.path.join(directory, "05-courses.sql"), "w", encoding="utf-8") as f:
        write_header(f)
        for course in courses:
            # We use 'name' here to match your schema exactly
            f.write(f"INSERT IGNORE INTO courses (name, course_code) VALUES ('{course[1]}', '{course[2]}');\n")
        write_footer(f)

    # 06-TEACHES
    with open(os.path.join(directory, "06-teaches.sql"), "w", encoding="utf-8") as f:
        write_header(f)
        for teacher in teachers:
            f.write(f"INSERT IGNORE INTO teaches (lecturer_id, course_id) VALUES ({teacher[1]}, {teacher[0]});\n")
        write_footer(f)

    # 07-ENROLLMENTS
    with open(os.path.join(directory, "07-enrollments.sql"), "w", encoding="utf-8") as f:
        write_header(f)
        for enrollment in enrollments:
            f.write(f"INSERT IGNORE INTO enrollments (student_id, course_id) VALUES ({enrollment[0]}, {enrollment[1]});\n")
        write_footer(f)

    print("All SQL files generated successfully with transaction wrappers!")

if __name__ == "__main__":
    start_time = time.time()
    
    # Generate the data
    print("Generating insert statements...")
    users = gen_users()
    admins = gen_admins(users)
    courses = gen_courses()
    students = gen_students(users)
    lecturers = gen_lecturers(users)
    teachers = gen_teachers(lecturers, courses)
    enrollments = gen_enrollments(students, courses)
    
    
    TARGET_FOLDER = "../database" #Output folder set as database folder
    
    # generate files
    generate_sql_files(TARGET_FOLDER, users, admins, courses, students, lecturers, teachers, enrollments)
    # If DEBUG_MODE is True, it prints everything. If False, it skips it instantly.
    if DEBUG_MODE:
        print(f"Number of users: {len(users)}")
        print(f"Number of admins: {len(admins)}")
        print(f"Number of courses: {len(courses)}")
        print(f"Number of students: {len(students)}")
        print(f"Number of lecturers: {len(lecturers)}")
        print(f"Number of teachers assigned to courses: {len(teachers)}")
        print(f"Number of enrollments: {len(enrollments)}")
        
        print("\n--- Sample Data ---")
        print("Last User:", users[-1])
        print("Last Admin:", admins[-1])
        print("Last Course:", courses[-1])
        print("Last Student:", students[-1])
        print("Last Lecturer:", lecturers[-1])
        print("Last Teacher:", teachers[-1])
        print("Last Enrollment:", enrollments[-1])
        print("First Course:", courses[0])

        lst_of_teachers = [teacher[1] for teacher in teachers]
        print(f"\nNumber of teachers assigned to courses: {len(lst_of_teachers)}")
        
        for lecturer in lecturers:
            if lecturer[0] not in lst_of_teachers:
                print(f"Lecturer {lecturer[0]} is not assigned to any course.")
            # else:
            #     print(f"Lecturer {lecturer[0]} is assigned to this many courses: {lst_of_teachers.count(lecturer[0])}")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")