"""
Run from school_final folder:
    python fix_db.py
"""
import sqlite3, os

db_path = os.path.join('database', 'school.db')
if not os.path.exists(db_path):
    print("ERROR: database/school.db not found!")
    print("Run: python app.py first to create it")
    exit(1)

db = sqlite3.connect(db_path)

print("Fixing achievements table...")

# Step 1: Add missing columns
for col, default in [('student_name','""'), ('photo','""')]:
    try:
        db.execute(f'ALTER TABLE achievements ADD COLUMN {col} TEXT DEFAULT {default}')
        print(f"  + Added column: {col}")
    except:
        print(f"  = Column already exists: {col}")

# Step 2: Add demo achievements (Class 5-10) for testing
db.executescript('''
    DELETE FROM achievements;

    INSERT INTO achievements (student_name,class_name,title,description,category,achievement_date) VALUES
        ("Aarav Kumar",    "Class 5",  "Mathematics Olympiad - Gold",   "Won Gold Medal in District Level Mathematics Olympiad 2024.",       "Academic", "2024-10-15"),
        ("Ananya Sharma",  "Class 5",  "Science Fair - Best Project",   "Best Project Award at State Level Science Exhibition.",             "Academic", "2024-09-20"),
        ("Rohan Gupta",    "Class 6",  "Chess Champion - State Level",  "Won First Place in State Level Chess Championship.",               "Sports",   "2024-08-12"),
        ("Priya Singh",    "Class 6",  "Painting Competition - Gold",   "National Level Painting Competition Gold Medal.",                  "Cultural", "2024-11-05"),
        ("Arjun Patel",    "Class 7",  "Cricket Team Captain",          "Led School Cricket Team to win District Championship 2024.",       "Sports",   "2024-09-30"),
        ("Meera Joshi",    "Class 7",  "English Essay - First Prize",   "Won First Prize in All India Essay Writing Competition by CBSE.",  "Academic", "2024-10-01"),
        ("Vikram Yadav",   "Class 8",  "Science Olympiad - Silver",     "Won Silver Medal at National Science Olympiad with 96 percentile.","Academic", "2024-11-10"),
        ("Sneha Verma",    "Class 8",  "Classical Dance Performance",   "Selected to perform at National Cultural Festival New Delhi.",     "Cultural", "2024-10-20"),
        ("Rahul Kumar",    "Class 9",  "Pre-Board Topper - 98%",        "Scored 98% in Pre-Board - Highest in School history for Class 9.","Academic", "2024-11-25"),
        ("Kavya Mishra",   "Class 9",  "Robotics - IIT Delhi Fest",     "Won First Prize in Robotics Competition at IIT Delhi Tech Fest.",  "Academic", "2024-10-08"),
        ("Sneha Gupta",    "Class 10", "CBSE Board Topper 2024",        "Scored 97.8% in CBSE Board Exams - District Rank 1, State Rank 8.","Academic","2024-03-25"),
        ("Aryan Tiwari",   "Class 10", "NTSE Scholar 2024",             "Cleared NTSE Stage 2 and qualified for JEE Advanced coaching.",    "Academic", "2024-09-15");
''')

db.commit()

# Verify
count = db.execute('SELECT COUNT(*) FROM achievements').fetchone()[0]
cols  = [c[1] for c in db.execute('PRAGMA table_info(achievements)').fetchall()]

print(f"\n  Total achievements: {count}")
print(f"  Columns: {cols}")
db.close()

print("\n" + "="*50)
print("DATABASE FIXED SUCCESSFULLY!")
print("="*50)
print("\nNow restart:  python app.py")
print("Then visit:   http://127.0.0.1:5000/achievers")