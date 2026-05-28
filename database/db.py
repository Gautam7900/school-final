import sqlite3, os
from flask import g

DATABASE = os.path.join(os.path.dirname(__file__), 'school.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = OFF")
    return db

def init_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.executescript('''
                  
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, subject TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
            email TEXT, phone TEXT, qualification TEXT,
            experience TEXT, bio TEXT, joining_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS teacher_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            class_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            UNIQUE(class_name, subject)
        );
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL, subject TEXT NOT NULL,
            marks REAL NOT NULL, max_marks REAL DEFAULT 100,
            exam_type TEXT DEFAULT "Unit Test",
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id, subject, exam_type)
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL, date TEXT NOT NULL, status TEXT NOT NULL,
            UNIQUE(student_id, date)
        );
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL, class_name TEXT NOT NULL,
            fee_month TEXT NOT NULL, fee_year TEXT DEFAULT "2024-25",
            tuition_fee REAL DEFAULT 0, other_fee REAL DEFAULT 0,
            total_fee REAL DEFAULT 0, paid_amount REAL DEFAULT 0,
            remaining REAL DEFAULT 0, paid_date TEXT,
            status TEXT DEFAULT "Pending", remarks TEXT,
            UNIQUE(student_id, fee_month)
        );
        CREATE TABLE IF NOT EXISTS fee_structure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT UNIQUE NOT NULL,
            tuition_fee REAL DEFAULT 0, activity_fee REAL DEFAULT 0,
            computer_fee REAL DEFAULT 0, other_fee REAL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL, subject TEXT NOT NULL,
            description TEXT NOT NULL, due_date TEXT NOT NULL,
            teacher_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, content TEXT NOT NULL,
            category TEXT DEFAULT "General",
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS admissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, dob TEXT, class_name TEXT NOT NULL,
            parent_name TEXT, contact TEXT, email TEXT, address TEXT,
            status TEXT DEFAULT "Pending",
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT, subject TEXT, message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS student_photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER UNIQUE NOT NULL,
            filename TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL, title TEXT NOT NULL,
            class_name TEXT NOT NULL, subject TEXT NOT NULL,
            duration INTEGER DEFAULT 30, total_marks INTEGER DEFAULT 10,
            status TEXT DEFAULT "Draft", created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL, question TEXT NOT NULL,
            option_a TEXT NOT NULL, option_b TEXT NOT NULL,
            option_c TEXT NOT NULL, option_d TEXT NOT NULL,
            correct TEXT NOT NULL, marks INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL, student_id INTEGER NOT NULL,
            score REAL DEFAULT 0, total INTEGER DEFAULT 0,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            answers TEXT, UNIQUE(quiz_id, student_id)
        );
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER, title TEXT NOT NULL, category TEXT NOT NULL,
            description TEXT, achievement_date TEXT, awarded_by TEXT,
            class_name TEXT, is_featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL, recipient TEXT NOT NULL, message TEXT NOT NULL,
            status TEXT DEFAULT "Pending", sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL, day TEXT NOT NULL, period INTEGER NOT NULL,
            subject TEXT NOT NULL, teacher_id INTEGER,
            start_time TEXT, end_time TEXT,
            UNIQUE(class_name, day, period)
        );
        CREATE TABLE IF NOT EXISTS exam_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL, subject TEXT NOT NULL,
            exam_date TEXT NOT NULL, day TEXT,
            start_time TEXT DEFAULT "10:00", end_time TEXT DEFAULT "13:00",
            exam_type TEXT DEFAULT "Unit Test", venue TEXT DEFAULT "Main Hall",
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL, class_name TEXT NOT NULL,
            subject TEXT NOT NULL, title TEXT NOT NULL,
            duration INTEGER DEFAULT 30, total_marks INTEGER DEFAULT 0,
            status TEXT DEFAULT "Draft", created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, quiz_id INTEGER NOT NULL,
            question TEXT NOT NULL, option_a TEXT NOT NULL, option_b TEXT NOT NULL,
            option_c TEXT NOT NULL, option_d TEXT NOT NULL,
            correct_ans TEXT NOT NULL, marks INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, quiz_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL, score INTEGER DEFAULT 0,
            total INTEGER DEFAULT 0, answers TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(quiz_id, student_id)
        );
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            student_name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT DEFAULT "Academic",
            achievement_date TEXT,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS whatsapp_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, recipient TEXT NOT NULL,
            message TEXT NOT NULL, status TEXT DEFAULT "Pending",
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS live_classes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id  INTEGER NOT NULL,
            class_name  TEXT NOT NULL,
            subject     TEXT NOT NULL,
            title       TEXT NOT NULL,
            meet_link   TEXT NOT NULL,
            platform    TEXT DEFAULT "Google Meet",
            scheduled_at TEXT NOT NULL,
            duration    INTEGER DEFAULT 60,
            status      TEXT DEFAULT "Upcoming",
            description TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS gallery_photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, category TEXT NOT NULL,
            filename TEXT NOT NULL, description TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
                     
        CREATE TABLE IF NOT EXISTS exam_patterns (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           type TEXT,
           title TEXT,
           description TEXT,
           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );

        CREATE TABLE IF NOT EXISTS syllabus (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           class_name TEXT,
           subject TEXT,
           title TEXT,
           file_name TEXT,
           uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );
       
      
                
  CREATE TABLE IF NOT EXISTS admissions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT,
    parent_name TEXT,
    class_name TEXT,
    contact TEXT,
    email TEXT,
    status TEXT DEFAULT 'Pending',
    applied_on TEXT,
    pdf_file TEXT

);



   CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    class_name TEXT,
    roll_number TEXT,
    parent_name TEXT,
    contact TEXT,
    password TEXT,
    aadhaar TEXT,
    address TEXT,
    photo TEXT

);

        ALTER TABLE admissions ADD COLUMN gender TEXT;

        ALTER TABLE admissions ADD COLUMN blood_group TEXT;

        ALTER TABLE admissions ADD COLUMN religion TEXT;

        ALTER TABLE admissions ADD COLUMN father_name TEXT;

        ALTER TABLE admissions ADD COLUMN mother_name TEXT;

        ALTER TABLE admissions ADD COLUMN occupation TEXT;

        ALTER TABLE admissions ADD COLUMN income TEXT;

        ALTER TABLE admissions ADD COLUMN city TEXT;

        ALTER TABLE admissions ADD COLUMN state TEXT;

        ALTER TABLE admissions ADD COLUMN pincode TEXT;

        ALTER TABLE admissions ADD COLUMN previous_school TEXT;

        ALTER TABLE admissions ADD COLUMN last_class TEXT;

        ALTER TABLE admissions ADD COLUMN percentage TEXT;

        ALTER TABLE admissions ADD COLUMN medical TEXT;

        ALTER TABLE admissions ADD COLUMN emergency_contact TEXT;
        
        
  

        ALTER TABLE students ADD COLUMN city TEXT;

        ALTER TABLE students ADD COLUMN state TEXT;

        ALTER TABLE students ADD COLUMN pincode TEXT;
       
             
       
        
       ALTER TABLE admissions
       ADD COLUMN form_pdf TEXT;
                     
    ''')
    
    if db.execute('SELECT COUNT(*) FROM students').fetchone()[0] == 0:
        db.executescript('''
            INSERT INTO teachers (name,subject,username,password,email,phone,qualification,experience,bio,joining_date) VALUES
                ("Mrs. Priya Sharma","Mathematics","priya","teacher123","priya@school.com","9811001001","M.Sc Mathematics, B.Ed","12 Years","Dedicated mathematics teacher with a passion for making numbers fun. Expert in CBSE curriculum.","2012-04-01"),
                ("Mr. Rakesh Verma","Science","rakesh","teacher123","rakesh@school.com","9811001002","M.Sc Physics, B.Ed","9 Years","Enthusiastic science teacher who believes in hands-on learning. Runs the school science club.","2015-06-01"),
                ("Ms. Anita Singh","English","anita","teacher123","anita@school.com","9811001003","M.A. English Literature, B.Ed","15 Years","English language expert with a love for literature and creative writing.","2009-04-01"),
                ("Mr. Suresh Yadav","Hindi","suresh","teacher123","suresh@school.com","9811001004","M.A. Hindi, B.Ed","8 Years","Hindi teacher who brings literature alive through storytelling.","2016-04-01"),
                ("Ms. Kavita Mishra","Social Science","kavita","teacher123","kavita@school.com","9811001005","M.A. History, B.Ed","11 Years","Social Science teacher passionate about history and geography.","2013-04-01"),
                ("Mr. Arun Tiwari","Computer","arun","teacher123","arun@school.com","9811001006","MCA, B.Ed","7 Years","Computer science teacher and tech enthusiast. Coaches students for coding competitions.","2017-04-01");

            INSERT INTO teacher_assignments (teacher_id,class_name,subject) VALUES
                (1,"Class 6","Mathematics"),(1,"Class 7","Mathematics"),(1,"Class 8","Mathematics"),(1,"Class 9","Mathematics"),(1,"Class 10","Mathematics"),
                (2,"Class 6","Science"),(2,"Class 7","Science"),(2,"Class 8","Science"),(2,"Class 9","Science"),(2,"Class 10","Science"),
                (3,"Class 6","English"),(3,"Class 7","English"),(3,"Class 8","English"),(3,"Class 9","English"),(3,"Class 10","English"),
                (4,"Class 6","Hindi"),(4,"Class 7","Hindi"),(4,"Class 8","Hindi"),(4,"Class 9","Hindi"),(4,"Class 10","Hindi"),
                (5,"Class 6","Social Science"),(5,"Class 7","Social Science"),(5,"Class 8","Social Science"),(5,"Class 9","Social Science"),(5,"Class 10","Social Science"),
                (6,"Class 6","Computer"),(6,"Class 7","Computer"),(6,"Class 8","Computer");

            INSERT INTO fee_structure (class_name,tuition_fee,activity_fee,computer_fee,other_fee) VALUES
                ("UKG",3000,200,0,300),("Class 1",3500,300,0,200),("Class 2",3500,300,0,200),
                ("Class 3",4000,300,200,200),("Class 4",4000,300,200,200),("Class 5",4000,300,200,200),
                ("Class 6",4500,400,300,200),("Class 7",4500,400,300,200),("Class 8",4500,400,300,200),
                ("Class 9",5500,500,300,200),("Class 10",5500,500,300,200);

            INSERT INTO students (name,class_name,roll_number,parent_name,contact,password) VALUES
                ("Aarav Kumar","Class 5","C5-001","Rajesh Kumar","9876543210","student123"),
                ("Priya Patel","Class 5","C5-002","Suresh Patel","9876543211","student123"),
                ("Rohan Sharma","Class 8","C8-001","Mohan Sharma","9876543212","student123"),
                ("Sneha Gupta","Class 10","C10-001","Dinesh Gupta","9876543213","student123");

            INSERT INTO marks (student_id,subject,marks,max_marks,exam_type) VALUES
                (1,"Mathematics",85,100,"Half Yearly"),(1,"Science",78,100,"Half Yearly"),
                (1,"English",92,100,"Half Yearly"),(1,"Hindi",80,100,"Half Yearly"),
                (2,"Mathematics",90,100,"Half Yearly"),(2,"Science",88,100,"Half Yearly");

            INSERT INTO attendance (student_id,date,status) VALUES
                (1,"2024-11-01","Present"),(1,"2024-11-02","Present"),(1,"2024-11-04","Absent"),
                (1,"2024-11-05","Present"),(1,"2024-11-06","Present"),(1,"2024-11-07","Late"),
                (1,"2024-11-08","Present"),(1,"2024-11-11","Present"),(1,"2024-11-12","Present"),
                (1,"2024-11-13","Present");

            INSERT INTO fees (student_id,class_name,fee_month,fee_year,tuition_fee,other_fee,total_fee,paid_amount,remaining,status,paid_date) VALUES
                (1,"Class 5","2024-04","2024-25",4000,700,4700,4700,0,"Paid","2024-04-05"),
                (1,"Class 5","2024-05","2024-25",4000,700,4700,4700,0,"Paid","2024-05-03"),
                (1,"Class 5","2024-06","2024-25",4000,700,4700,2000,2700,"Partial","2024-06-10"),
                (1,"Class 5","2024-07","2024-25",4000,700,4700,0,4700,"Pending",NULL),
                (2,"Class 5","2024-04","2024-25",4000,700,4700,4700,0,"Paid","2024-04-06"),
                (2,"Class 5","2024-05","2024-25",4000,700,4700,0,4700,"Overdue",NULL),
                (3,"Class 8","2024-04","2024-25",4500,900,5400,5400,0,"Paid","2024-04-04"),
                (4,"Class 10","2024-04","2024-25",5500,1000,6500,6500,0,"Paid","2024-04-02");

            INSERT INTO homework (class_name,subject,description,due_date,teacher_id) VALUES
                ("Class 5","Mathematics","Complete exercises 3.1 to 3.5","2024-11-20",1),
                ("Class 5","Science","Draw and label the digestive system","2024-11-18",2),
                ("Class 5","English","Write essay on My Favourite Festival","2024-11-19",3);

            INSERT INTO notices (title,content,category) VALUES
                ("Annual Sports Day","Annual Sports Day on 15th December 2024.","Events"),
                ("Winter Vacation","School closed 25th Dec to 5th Jan.","Holiday"),
                ("Parent-Teacher Meeting","PTM scheduled for 30th November.","Important"),
                ("Half-Yearly Results","Results declared on 20th November 2024.","Academic");
        ''')

    db.commit()
    db.close()
    print("✅ Database initialized with demo data.")
