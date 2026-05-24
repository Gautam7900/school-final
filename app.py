# from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# from database.db import init_db, get_db
# import os, uuid

# app = Flask(__name__)
# app.secret_key = 'brightmind_school_2024'

# with app.app_context():
#     init_db()

# # ── PUBLIC ─────────────────────────────────────────────────────────────────────
# @app.route('/')
# def home():
#     db = get_db()
#     notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC LIMIT 4').fetchall()
#     featured_achievers = db.execute(
#         """SELECT * FROM achievements
#            WHERE class_name IN ('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')
#            ORDER BY class_name, achievement_date DESC LIMIT 12"""
#     ).fetchall()
#     return render_template('home.html', notices=notices, featured_achievers=featured_achievers)

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/admissions', methods=['GET','POST'])
# def admissions():
#     if request.method == 'POST':
#         db = get_db()
#         db.execute('INSERT INTO admissions (name,dob,class_name,parent_name,contact,email,address,status) VALUES (?,?,?,?,?,?,?,?)',
#             (request.form['name'], request.form['dob'], request.form['class_name'],
#              request.form['parent_name'], request.form['contact'], request.form['email'],
#              request.form['address'], 'Pending'))
#         db.commit()
#         flash('Admission form submitted! We will contact you soon.', 'success')
#         return redirect('/admissions')
#     return render_template('admissions.html')

# @app.route('/academics')
# def academics():
#     return render_template('academics.html')

# @app.route('/notices')
# def notices():
#     db = get_db()
#     all_notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC').fetchall()
#     return render_template('notices.html', notices=all_notices)

# @app.route('/contact', methods=['GET','POST'])
# def contact():
#     if request.method == 'POST':
#         db = get_db()
#         db.execute('INSERT INTO contact_messages (name,email,subject,message) VALUES (?,?,?,?)',
#             (request.form['name'], request.form['email'], request.form['subject'], request.form['message']))
#         db.commit()
#         flash('Message sent! We will reply shortly.', 'success')
#         return redirect('/contact')
#     return render_template('contact.html')

# # ── TEACHERS PUBLIC ────────────────────────────────────────────────────────────
# @app.route('/teachers')
# def teachers_list():
#     db = get_db()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     return render_template('teachers.html', teachers=teachers)

# @app.route('/teachers/<int:teacher_id>')
# def teacher_profile(teacher_id):
#     db = get_db()
#     teacher = db.execute('SELECT * FROM teachers WHERE id=?', (teacher_id,)).fetchone()
#     if not teacher:
#         flash('Teacher not found.', 'error')
#         return redirect('/teachers')
#     assignments = db.execute(
#         'SELECT class_name, subject FROM teacher_assignments WHERE teacher_id=? ORDER BY class_name',
#         (teacher_id,)).fetchall()
#     return render_template('teacher_profile.html', teacher=teacher, assignments=assignments)

# # ── GALLERY PUBLIC ─────────────────────────────────────────────────────────────
# @app.route('/gallery')
# def gallery():
#     db = get_db()
#     sel_cat = request.args.get('category', 'All')
#     if sel_cat == 'All':
#         photos = db.execute('SELECT * FROM gallery_photos ORDER BY uploaded_at DESC').fetchall()
#     else:
#         photos = db.execute('SELECT * FROM gallery_photos WHERE category=? ORDER BY uploaded_at DESC', (sel_cat,)).fetchall()
#     categories = db.execute('SELECT DISTINCT category FROM gallery_photos ORDER BY category').fetchall()
#     return render_template('gallery.html', photos=photos, categories=categories, sel_cat=sel_cat)

# # ── STUDENT PORTAL ─────────────────────────────────────────────────────────────
# @app.route('/student/login', methods=['GET','POST'])
# def student_login():
#     if request.method == 'POST':
#         db = get_db()
#         s = db.execute('SELECT * FROM students WHERE roll_number=? AND password=?',
#             (request.form['roll_number'], request.form['password'])).fetchone()
#         if s:
#             session.update({'student_id':s['id'],'student_name':s['name'],'student_class':s['class_name'],'role':'student'})
#             return redirect('/student/dashboard')
#         flash('Invalid credentials.', 'error')
#     return render_template('student_login.html')

# @app.route('/student/dashboard')
# def student_dashboard():
#     if session.get('role') != 'student': return redirect('/student/login')
#     db  = get_db()
#     sid = session['student_id']
#     marks      = db.execute('SELECT * FROM marks WHERE student_id=?', (sid,)).fetchall()
#     attendance = db.execute('SELECT * FROM attendance WHERE student_id=? ORDER BY date DESC LIMIT 30', (sid,)).fetchall()
#     homework   = db.execute('SELECT * FROM homework WHERE class_name=? ORDER BY due_date DESC', (session['student_class'],)).fetchall()
#     fees       = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month', (sid,)).fetchall()
#     total   = len(attendance)
#     present = sum(1 for a in attendance if a['status'] == 'Present')
#     pct     = round((present/total*100) if total else 0, 1)
#     return render_template('student_dashboard.html',
#         marks=marks, attendance=attendance, homework=homework, fees=fees,
#         attend_pct=pct, total_days=total, present_days=present)

# @app.route('/student/logout')
# def student_logout():
#     session.clear(); return redirect('/')

# # ── TEACHER PORTAL ─────────────────────────────────────────────────────────────
# @app.route('/teacher/login', methods=['GET','POST'])
# def teacher_login():
#     if request.method == 'POST':
#         db = get_db()
#         t = db.execute('SELECT * FROM teachers WHERE username=? AND password=?',
#             (request.form['username'], request.form['password'])).fetchone()
#         if t:
#             session.update({'teacher_id':t['id'],'teacher_name':t['name'],'teacher_sub':t['subject'],'role':'teacher'})
#             return redirect('/teacher/dashboard')
#         flash('Invalid credentials.', 'error')
#     return render_template('teacher_login.html')

# @app.route('/teacher/dashboard')
# def teacher_dashboard():
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     classes  = db.execute('SELECT DISTINCT class_name FROM students ORDER BY class_name').fetchall()
#     students = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
#     homework = db.execute('SELECT h.*,t.name as tname FROM homework h JOIN teachers t ON h.teacher_id=t.id ORDER BY due_date DESC').fetchall()
#     return render_template('teacher_dashboard.html', classes=classes, students=students, homework=homework)

# @app.route('/teacher/upload_marks', methods=['POST'])
# def upload_marks():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('INSERT OR REPLACE INTO marks (student_id,subject,marks,max_marks,exam_type) VALUES (?,?,?,?,?)',
#         (d['student_id'],d['subject'],d['marks'],d['max_marks'],d['exam_type']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/attendance', methods=['POST'])
# def mark_attendance():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     for r in d['records']:
#         db.execute('INSERT OR REPLACE INTO attendance (student_id,date,status) VALUES (?,?,?)',
#             (r['student_id'],d['date'],r['status']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/upload_homework', methods=['POST'])
# def upload_homework():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('INSERT INTO homework (class_name,subject,description,due_date,teacher_id) VALUES (?,?,?,?,?)',
#         (d['class_name'],d['subject'],d['description'],d['due_date'],session['teacher_id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/logout')
# def teacher_logout():
#     session.clear(); return redirect('/')

# # ── ADMIN LOGIN ────────────────────────────────────────────────────────────────
# @app.route('/admin/login', methods=['GET','POST'])
# def admin_login():
#     if request.method == 'POST':
#         if request.form['username']=='admin' and request.form['password']=='admin123':
#             session['role'] = 'admin'; return redirect('/admin/dashboard')
#         flash('Wrong credentials.', 'error')
#     return render_template('admin_login.html')

# @app.route('/admin/logout')
# def admin_logout():
#     session.clear(); return redirect('/')

# # ── ADMIN DASHBOARD ────────────────────────────────────────────────────────────
# @app.route('/admin/dashboard')
# def admin_dashboard():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     stats = {
#         'students':   db.execute('SELECT COUNT(*) FROM students').fetchone()[0],
#         'teachers':   db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
#         'admissions': db.execute("SELECT COUNT(*) FROM admissions WHERE status='Pending'").fetchone()[0],
#         'notices':    db.execute('SELECT COUNT(*) FROM notices').fetchone()[0],
#     }
#     admissions  = db.execute('SELECT * FROM admissions ORDER BY created_at DESC').fetchall()
#     messages    = db.execute('SELECT * FROM contact_messages ORDER BY created_at DESC').fetchall()
#     students    = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
#     teachers    = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     all_notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC').fetchall()
#     return render_template('admin_dashboard.html',
#         stats=stats, admissions=admissions, messages=messages,
#         students=students, teachers=teachers, all_notices=all_notices)

# # ── ADMIN STUDENTS ─────────────────────────────────────────────────────────────
# @app.route('/admin/add_student', methods=['POST'])
# def add_student():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     try:
#         db.execute('INSERT INTO students (name,class_name,roll_number,parent_name,contact,password) VALUES (?,?,?,?,?,?)',
#             (request.form['name'],request.form['class_name'],request.form['roll_number'],
#              request.form['parent_name'],request.form['contact'],request.form['password']))
#         db.commit(); flash('Student added!', 'success')
#     except: flash('Error: Roll number may already exist.', 'error')
#     return redirect('/admin/dashboard')

# @app.route('/admin/delete_student/<int:sid>', methods=['POST'])
# def delete_student(sid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     for tbl in ['marks','attendance','fees']: db.execute(f'DELETE FROM {tbl} WHERE student_id=?', (sid,))
#     db.execute('DELETE FROM students WHERE id=?', (sid,)); db.commit()
#     return jsonify({'success':True})

# # ── ADMIN TEACHERS ─────────────────────────────────────────────────────────────
# @app.route('/admin/add_teacher', methods=['POST'])
# def add_teacher():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     try:
#         db.execute('INSERT INTO teachers (name,subject,username,password,email) VALUES (?,?,?,?,?)',
#             (request.form['name'],request.form['subject'],request.form['username'],
#              request.form['password'],request.form.get('email','')))
#         db.commit(); flash(f"Teacher '{request.form['name']}' added!", 'success')
#     except: flash('Error: Username already exists.', 'error')
#     return redirect('/admin/dashboard')

# @app.route('/admin/delete_teacher/<int:tid>', methods=['POST'])
# def delete_teacher(tid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM homework WHERE teacher_id=?', (tid,))
#     db.execute('DELETE FROM teacher_assignments WHERE teacher_id=?', (tid,))
#     db.execute('DELETE FROM teachers WHERE id=?', (tid,))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/teacher_edit/<int:tid>')
# def admin_teacher_edit(tid):
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     teacher = db.execute('SELECT * FROM teachers WHERE id=?', (tid,)).fetchone()
#     return render_template('admin_teacher_edit.html', teacher=teacher)

# @app.route('/admin/update_teacher_info', methods=['POST'])
# def update_teacher_info():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('UPDATE teachers SET phone=?,qualification=?,experience=?,bio=?,joining_date=? WHERE id=?',
#         (d.get('phone',''),d.get('qualification',''),d.get('experience',''),
#          d.get('bio',''),d.get('joining_date',''),d['id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/upload_teacher_photo/<int:tid>', methods=['POST'])
# def upload_teacher_photo(tid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
#     file = request.files['photo']
#     ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#     if ext not in {'png','jpg','jpeg','gif','webp'}: return jsonify({'error':'Invalid file type'}), 400
#     fname = f"teacher_{tid}_{uuid.uuid4().hex[:8]}.{ext}"
#     path  = os.path.join(app.root_path, 'static', 'uploads', 'teachers', fname)
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     file.save(path)
#     db = get_db()
#     db.execute('UPDATE teachers SET photo=? WHERE id=?', (fname, tid))
#     db.commit(); return jsonify({'success':True, 'filename':fname})

# # ── ADMIN NOTICES ──────────────────────────────────────────────────────────────
# @app.route('/admin/add_notice', methods=['POST'])
# def add_notice():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     db.execute('INSERT INTO notices (title,content,category) VALUES (?,?,?)',
#         (request.form['title'],request.form['content'],request.form['category']))
#     db.commit(); flash('Notice posted!', 'success'); return redirect('/admin/dashboard')

# @app.route('/admin/edit_notice', methods=['POST'])
# def edit_notice():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     db.execute('UPDATE notices SET title=?,content=?,category=? WHERE id=?',
#         (request.form['title'],request.form['content'],request.form['category'],request.form['notice_id']))
#     db.commit(); flash('Notice updated!', 'success'); return redirect('/admin/dashboard')

# @app.route('/admin/delete_notice/<int:nid>', methods=['POST'])
# def delete_notice(nid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM notices WHERE id=?', (nid,)); db.commit()
#     return jsonify({'success':True})

# # ── ADMIN ADMISSIONS ───────────────────────────────────────────────────────────
# @app.route('/admin/update_admission_status', methods=['POST'])
# def update_admission_status():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('UPDATE admissions SET status=? WHERE id=?', (d['status'],d['id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/delete_admission/<int:aid>', methods=['POST'])
# def delete_admission(aid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM admissions WHERE id=?', (aid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/delete_message/<int:mid>', methods=['POST'])
# def delete_message(mid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM contact_messages WHERE id=?', (mid,)); db.commit()
#     return jsonify({'success':True})

# # ── ADMIN TEACHER ASSIGNMENTS ──────────────────────────────────────────────────
# @app.route('/admin/teacher_assignments')
# def teacher_assignments_page():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     return render_template('teacher_assignments.html', teachers=teachers)

# @app.route('/admin/assign_teacher', methods=['POST'])
# def assign_teacher():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     try:
#         db.execute('INSERT OR REPLACE INTO teacher_assignments (teacher_id,class_name,subject) VALUES (?,?,?)',
#             (d['teacher_id'],d['class_name'],d['subject']))
#         db.commit(); return jsonify({'success':True})
#     except Exception as e: return jsonify({'error':str(e)}), 500

# @app.route('/admin/remove_assignment', methods=['POST'])
# def remove_assignment():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('DELETE FROM teacher_assignments WHERE id=?', (d['id'],))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/get_assignments')
# def get_assignments():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     rows = db.execute('''SELECT ta.id, ta.class_name, ta.subject, t.name as teacher_name, t.id as teacher_id
#         FROM teacher_assignments ta JOIN teachers t ON ta.teacher_id=t.id ORDER BY ta.class_name, ta.subject''').fetchall()
#     return jsonify([dict(r) for r in rows])

# # ── ADMIN GALLERY ──────────────────────────────────────────────────────────────
# @app.route('/admin/gallery')
# def admin_gallery():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     photos = db.execute('SELECT * FROM gallery_photos ORDER BY uploaded_at DESC').fetchall()
#     return render_template('admin_gallery.html', photos=photos)

# @app.route('/admin/upload_gallery_photo', methods=['POST'])
# def upload_gallery_photo():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
#     file     = request.files['photo']
#     title    = request.form.get('title','Photo')
#     category = request.form.get('category','General')
#     desc     = request.form.get('description','')
#     ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#     if ext not in {'png','jpg','jpeg','gif','webp'}: return jsonify({'error':'Invalid file type'}), 400
#     fname = f"gallery_{uuid.uuid4().hex[:10]}.{ext}"
#     path  = os.path.join(app.root_path, 'static', 'uploads', 'gallery', fname)
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     file.save(path)
#     db = get_db()
#     db.execute('INSERT INTO gallery_photos (title,category,filename,description) VALUES (?,?,?,?)',
#         (title,category,fname,desc))
#     db.commit(); return jsonify({'success':True, 'filename':fname})

# @app.route('/admin/delete_gallery_photo/<int:pid>', methods=['POST'])
# def delete_gallery_photo(pid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     p = db.execute('SELECT filename FROM gallery_photos WHERE id=?', (pid,)).fetchone()
#     if p:
#         path = os.path.join(app.root_path,'static','uploads','gallery',p['filename'])
#         if os.path.exists(path): os.remove(path)
#         db.execute('DELETE FROM gallery_photos WHERE id=?', (pid,)); db.commit()
#     return jsonify({'success':True})

# # ── ADMIN FEES ─────────────────────────────────────────────────────────────────
# @app.route('/admin/fees')
# def admin_fees():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','Class 5')
#     sel_month = request.args.get('month','')
#     sel_year  = request.args.get('year','2024-25')
#     fee_struct = db.execute('SELECT * FROM fee_structure WHERE class_name=?', (sel_class,)).fetchone()
#     q = 'SELECT f.*, s.name as student_name, s.roll_number FROM fees f JOIN students s ON f.student_id=s.id WHERE f.class_name=?'
#     p = [sel_class]
#     if sel_month: q += ' AND f.fee_month=?'; p.append(sel_month)
#     q += ' ORDER BY f.fee_month, s.roll_number'
#     fees = db.execute(q, p).fetchall()
#     total_due  = sum(f['total_fee'] for f in fees)
#     total_paid = sum(f['paid_amount'] for f in fees)
#     total_rem  = sum(f['remaining'] for f in fees)
#     months = db.execute('SELECT DISTINCT fee_month FROM fees WHERE class_name=? ORDER BY fee_month', (sel_class,)).fetchall()
#     students_summary = db.execute('''
#         SELECT s.id, s.name, s.roll_number,
#                COUNT(f.id) as total_months,
#                SUM(CASE WHEN f.status="Paid" THEN 1 ELSE 0 END) as paid_months,
#                SUM(f.total_fee) as total_due, SUM(f.paid_amount) as total_paid,
#                SUM(f.remaining) as total_remaining
#         FROM students s LEFT JOIN fees f ON s.id=f.student_id
#         WHERE s.class_name=? GROUP BY s.id ORDER BY s.roll_number
#     ''', (sel_class,)).fetchall()
#     return render_template('admin_fees.html',
#         classes=classes, sel_class=sel_class, sel_month=sel_month, sel_year=sel_year,
#         fee_struct=fee_struct, fees=fees, months=months,
#         total_due=total_due, total_paid=total_paid, total_rem=total_rem,
#         students_summary=students_summary)

# @app.route('/admin/fees/update', methods=['POST'])
# def update_fee():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     total = float(d.get('total_fee',0))
#     paid  = float(d.get('paid_amount',0))
#     rem   = max(0, total - paid)
#     status = 'Paid' if rem<=0 else ('Partial' if paid>0 else 'Pending')
#     db.execute('''INSERT INTO fees (student_id,class_name,fee_month,fee_year,tuition_fee,other_fee,total_fee,paid_amount,remaining,status,paid_date,remarks)
#         VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
#         ON CONFLICT(student_id,fee_month) DO UPDATE SET
#         total_fee=excluded.total_fee, paid_amount=excluded.paid_amount,
#         remaining=excluded.remaining, status=excluded.status,
#         paid_date=excluded.paid_date, remarks=excluded.remarks''',
#         (d['student_id'],d['class_name'],d['fee_month'],d.get('fee_year','2024-25'),
#          d.get('tuition_fee',0),d.get('other_fee',0),total,paid,rem,status,
#          d.get('paid_date') or None,d.get('remarks','')))
#     db.commit(); return jsonify({'success':True,'remaining':rem,'status':status})

# @app.route('/admin/fees/generate_monthly', methods=['POST'])
# def generate_monthly_fees():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     struct = db.execute('SELECT * FROM fee_structure WHERE class_name=?', (d['class_name'],)).fetchone()
#     if not struct: return jsonify({'error':'Fee structure not set'}), 400
#     total    = struct['tuition_fee']+struct['activity_fee']+struct['computer_fee']+struct['other_fee']
#     students = db.execute('SELECT id FROM students WHERE class_name=?', (d['class_name'],)).fetchall()
#     count = 0
#     for s in students:
#         try:
#             db.execute('''INSERT OR IGNORE INTO fees
#                 (student_id,class_name,fee_month,fee_year,tuition_fee,other_fee,total_fee,paid_amount,remaining,status)
#                 VALUES (?,?,?,?,?,?,?,0,?,?)''',
#                 (s['id'],d['class_name'],d['fee_month'],d.get('fee_year','2024-25'),
#                  struct['tuition_fee'],struct['activity_fee']+struct['computer_fee']+struct['other_fee'],
#                  total,total,'Pending'))
#             count += 1
#         except: pass
#     db.commit(); return jsonify({'success':True,'generated':count})

# @app.route('/admin/fees/update_structure', methods=['POST'])
# def update_fee_structure():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('''INSERT INTO fee_structure (class_name,tuition_fee,activity_fee,computer_fee,other_fee)
#         VALUES (?,?,?,?,?) ON CONFLICT(class_name) DO UPDATE SET
#         tuition_fee=excluded.tuition_fee, activity_fee=excluded.activity_fee,
#         computer_fee=excluded.computer_fee, other_fee=excluded.other_fee''',
#         (d['class_name'],d['tuition_fee'],d['activity_fee'],d['computer_fee'],d['other_fee']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/fees/student_detail/<int:sid>')
# def admin_student_fee_detail(sid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     fees = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month', (sid,)).fetchall()
#     return jsonify({'fees':[dict(f) for f in fees]})


# # ═══════════════════════════════════════════════
# # FEATURE 1: RESULT / REPORT CARD PDF DOWNLOAD
# # ═══════════════════════════════════════════════

# @app.route('/student/report_card')
# def student_report_card():
#     if session.get('role') != 'student': return redirect('/student/login')
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib import colors
#     from reportlab.lib.units import cm
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
#     from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#     from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
#     from io import BytesIO
#     from flask import make_response

#     db  = get_db()
#     sid = session['student_id']
#     student  = db.execute('SELECT * FROM students WHERE id=?', (sid,)).fetchone()
#     marks    = db.execute('SELECT * FROM marks WHERE student_id=? ORDER BY subject', (sid,)).fetchall()
#     attendance = db.execute('SELECT * FROM attendance WHERE student_id=?', (sid,)).fetchall()
#     total   = len(attendance)
#     present = sum(1 for a in attendance if a['status'] == 'Present')
#     att_pct = round((present/total*100) if total else 0, 1)

#     buffer = BytesIO()
#     doc    = SimpleDocTemplate(buffer, pagesize=A4,
#                                rightMargin=1.5*cm, leftMargin=1.5*cm,
#                                topMargin=1.5*cm, bottomMargin=1.5*cm)
#     styles = getSampleStyleSheet()
#     story  = []

#     NAVY  = colors.HexColor('#0d1b3e')
#     GOLD  = colors.HexColor('#c9a84c')
#     CREAM = colors.HexColor('#fdf8f0')
#     GREEN = colors.HexColor('#2e7d32')
#     RED   = colors.HexColor('#c62828')
#     ORANGE= colors.HexColor('#e65100')

#     # ── HEADER ──────────────────────────────────────────
#     header_data = [[
#         Paragraph('<font color="#0d1b3e"><b>🏫 BRIGHTMIND SCHOOL</b></font>', ParagraphStyle('h', fontSize=18, fontName='Helvetica-Bold', alignment=TA_CENTER)),
#     ]]
#     header_tbl = Table(header_data, colWidths=[17*cm])
#     header_tbl.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (-1,-1), CREAM),
#         ('TOPPADDING', (0,0), (-1,-1), 14),
#         ('BOTTOMPADDING', (0,0), (-1,-1), 4),
#         ('ROUNDEDCORNERS', [8]),
#     ]))
#     story.append(header_tbl)

#     sub_styles = ParagraphStyle('sub', fontSize=9, fontName='Helvetica', alignment=TA_CENTER, textColor=colors.HexColor('#555'))
#     story.append(Paragraph('Est. 1995 · CBSE Affiliated · Delhi – 110001', sub_styles))
#     story.append(Paragraph('Phone: +91 11 1234 5678 | Email: info@brightmindschool.edu.in', sub_styles))
#     story.append(Spacer(1, 10))

#     title_style = ParagraphStyle('title', fontSize=14, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=NAVY, spaceBefore=4, spaceAfter=4)
#     story.append(Paragraph('STUDENT PROGRESS REPORT CARD', title_style))
#     story.append(Paragraph('Academic Year: 2024–25', ParagraphStyle('ay', fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#777'))))
#     story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=10))

#     # ── STUDENT INFO ─────────────────────────────────────
#     info_data = [
#         ['Student Name:', student['name'],    'Roll Number:', student['roll_number']],
#         ['Class:',        student['class_name'], "Parent's Name:", student['parent_name'] or '—'],
#         ['Contact:',      student['contact'] or '—', 'Attendance:', f"{att_pct}% ({present}/{total} days)"],
#     ]
#     info_tbl = Table(info_data, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
#     info_tbl.setStyle(TableStyle([
#         ('FONTNAME',  (0,0), (0,-1), 'Helvetica-Bold'),
#         ('FONTNAME',  (2,0), (2,-1), 'Helvetica-Bold'),
#         ('FONTSIZE',  (0,0), (-1,-1), 9),
#         ('TEXTCOLOR', (0,0), (0,-1), NAVY),
#         ('TEXTCOLOR', (2,0), (2,-1), NAVY),
#         ('BACKGROUND',(0,0), (-1,-1), CREAM),
#         ('ROWBACKGROUNDS', (0,0), (-1,-1), [CREAM, colors.white]),
#         ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#ddd')),
#         ('TOPPADDING', (0,0), (-1,-1), 6),
#         ('BOTTOMPADDING', (0,0), (-1,-1), 6),
#         ('LEFTPADDING', (0,0), (-1,-1), 8),
#     ]))
#     story.append(info_tbl)
#     story.append(Spacer(1, 14))

#     # ── MARKS TABLE ──────────────────────────────────────
#     story.append(Paragraph('Academic Performance', ParagraphStyle('sec', fontSize=11, fontName='Helvetica-Bold', textColor=NAVY, spaceBefore=4, spaceAfter=6)))

#     if marks:
#         marks_header = [['S.No.', 'Subject', 'Exam Type', 'Marks Obtained', 'Max Marks', 'Percentage', 'Grade', 'Remarks']]
#         marks_rows   = []
#         total_marks = total_max = 0
#         for i, m in enumerate(marks, 1):
#             pct   = round(m['marks']/m['max_marks']*100, 1) if m['max_marks'] else 0
#             grade = 'A1' if pct>=90 else 'A2' if pct>=80 else 'B1' if pct>=70 else 'B2' if pct>=60 else 'C1' if pct>=50 else 'D'
#             rmk   = 'Excellent' if pct>=90 else 'Very Good' if pct>=80 else 'Good' if pct>=70 else 'Average' if pct>=50 else 'Needs Improvement'
#             total_marks += m['marks']; total_max += m['max_marks']
#             marks_rows.append([str(i), m['subject'], m['exam_type'],
#                                str(int(m['marks'])), str(int(m['max_marks'])),
#                                f"{pct}%", grade, rmk])

#         overall_pct = round(total_marks/total_max*100, 1) if total_max else 0
#         overall_grade = 'A1' if overall_pct>=90 else 'A2' if overall_pct>=80 else 'B1' if overall_pct>=70 else 'B2' if overall_pct>=60 else 'C1' if overall_pct>=50 else 'D'
#         marks_rows.append(['', 'TOTAL / OVERALL', '', f"{int(total_marks)}", f"{int(total_max)}", f"{overall_pct}%", overall_grade, ''])

#         all_rows = marks_header + marks_rows
#         marks_tbl = Table(all_rows, colWidths=[1*cm, 4*cm, 2.5*cm, 2.5*cm, 2*cm, 2*cm, 1.5*cm, 2.5*cm])
#         style = TableStyle([
#             ('BACKGROUND',  (0,0), (-1,0), NAVY),
#             ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
#             ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
#             ('FONTSIZE',    (0,0), (-1,-1), 8),
#             ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
#             ('ALIGN',       (1,0), (1,-1), 'LEFT'),
#             ('ALIGN',       (7,0), (7,-1), 'LEFT'),
#             ('GRID',        (0,0), (-1,-1), 0.3, colors.HexColor('#ccc')),
#             ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, CREAM]),
#             ('TOPPADDING',  (0,0), (-1,-1), 5),
#             ('BOTTOMPADDING',(0,0), (-1,-1), 5),
#             ('LEFTPADDING', (0,0), (-1,-1), 4),
#             ('FONTNAME',    (0,-1), (-1,-1), 'Helvetica-Bold'),
#             ('BACKGROUND',  (0,-1), (-1,-1), colors.HexColor('#e8f5e9')),
#             ('TEXTCOLOR',   (0,-1), (-1,-1), GREEN),
#         ])
#         marks_tbl.setStyle(style)
#         story.append(marks_tbl)
#     else:
#         story.append(Paragraph('No marks recorded yet.', styles['Normal']))

#     story.append(Spacer(1, 16))

#     # ── SUMMARY BOX ──────────────────────────────────────
#     if marks:
#         status = 'PASS ✓' if overall_pct >= 33 else 'FAIL ✗'
#         status_color = GREEN if overall_pct >= 33 else RED
#         summary_data = [
#             [Paragraph(f'<b>Overall Percentage:</b> {overall_pct}%', ParagraphStyle('s', fontSize=10)),
#              Paragraph(f'<b>Overall Grade:</b> {overall_grade}', ParagraphStyle('s', fontSize=10)),
#              Paragraph(f'<b>Result:</b> <font color="{"#2e7d32" if overall_pct>=33 else "#c62828"}">{status}</font>', ParagraphStyle('s', fontSize=10)),
#              Paragraph(f'<b>Attendance:</b> {att_pct}%', ParagraphStyle('s', fontSize=10))],
#         ]
#         sum_tbl = Table(summary_data, colWidths=[4.25*cm]*4)
#         sum_tbl.setStyle(TableStyle([
#             ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e3f2fd')),
#             ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#90caf9')),
#             ('TOPPADDING', (0,0), (-1,-1), 8),
#             ('BOTTOMPADDING', (0,0), (-1,-1), 8),
#             ('LEFTPADDING', (0,0), (-1,-1), 8),
#         ]))
#         story.append(sum_tbl)

#     story.append(Spacer(1, 20))

#     # ── GRADE SCALE ──────────────────────────────────────
#     grade_data = [['Grade Scale:','A1 (90-100)','A2 (80-89)','B1 (70-79)','B2 (60-69)','C1 (50-59)','D (Below 50)']]
#     grade_tbl  = Table(grade_data, colWidths=[2.5*cm]+[2.14*cm]*6)
#     grade_tbl.setStyle(TableStyle([
#         ('FONTNAME',  (0,0), (0,0), 'Helvetica-Bold'),
#         ('FONTSIZE',  (0,0), (-1,-1), 7.5),
#         ('BACKGROUND',(0,0), (-1,-1), CREAM),
#         ('GRID',      (0,0), (-1,-1), 0.3, colors.HexColor('#ddd')),
#         ('ALIGN',     (0,0), (-1,-1), 'CENTER'),
#         ('TOPPADDING',(0,0), (-1,-1), 4),
#         ('BOTTOMPADDING',(0,0),(-1,-1), 4),
#     ]))
#     story.append(grade_tbl)
#     story.append(Spacer(1, 20))

#     # ── SIGNATURES ───────────────────────────────────────
#     sig_data = [['Class Teacher', 'Examination Controller', 'Principal'],
#                 ['________________', '________________', '________________'],
#                 ['Date: ___________', 'Date: ___________', 'Date: ___________']]
#     sig_tbl  = Table(sig_data, colWidths=[5.67*cm]*3)
#     sig_tbl.setStyle(TableStyle([
#         ('ALIGN',   (0,0), (-1,-1), 'CENTER'),
#         ('FONTSIZE',(0,0), (-1,-1), 9),
#         ('FONTNAME',(0,0), (-1,0), 'Helvetica-Bold'),
#         ('TEXTCOLOR',(0,0),(-1,0), NAVY),
#         ('TOPPADDING',(0,0),(-1,-1), 4),
#     ]))
#     story.append(sig_tbl)

#     story.append(Spacer(1, 12))
#     story.append(HRFlowable(width="100%", thickness=1, color=GOLD))
#     footer_style = ParagraphStyle('ft', fontSize=7.5, alignment=TA_CENTER, textColor=colors.HexColor('#888'), spaceBefore=4)
#     story.append(Paragraph('This is a computer-generated report card. BrightMind School, Delhi – 110001', footer_style))

#     doc.build(story)
#     pdf = buffer.getvalue()
#     buffer.close()

#     response = make_response(pdf)
#     response.headers['Content-Type']        = 'application/pdf'
#     response.headers['Content-Disposition'] = f'attachment; filename=ReportCard_{student["roll_number"]}.pdf'
#     return response

# # ═══════════════════════════════════════════════
# # FEATURE 2: TIMETABLE MANAGEMENT
# # ═══════════════════════════════════════════════

# @app.route('/timetable')
# def timetable():
#     db = get_db()
#     classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name', session.get('student_class','Class 5'))
#     days      = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
#     periods   = list(range(1,7))

#     rows = db.execute(
#         'SELECT * FROM timetable WHERE class_name=? ORDER BY day, period', (sel_class,)
#     ).fetchall()

#     # Build dict: day -> {period -> row}
#     tt = {day: {} for day in days}
#     for r in rows:
#         tt[r['day']][r['period']] = r

#     period_times = {1:'8:00-8:45',2:'8:45-9:30',3:'9:30-10:15',
#                     4:'10:30-11:15',5:'11:15-12:00',6:'12:00-12:45'}

#     return render_template('timetable.html',
#         classes=classes, sel_class=sel_class, days=days,
#         periods=periods, tt=tt, period_times=period_times)

# @app.route('/admin/timetable')
# def admin_timetable():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','Class 5')
#     teachers  = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     days      = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
#     periods   = list(range(1,7))
#     rows = db.execute('SELECT * FROM timetable WHERE class_name=? ORDER BY day,period',(sel_class,)).fetchall()
#     tt   = {day:{} for day in days}
#     for r in rows: tt[r['day']][r['period']] = r
#     period_times = {1:'8:00-8:45',2:'8:45-9:30',3:'9:30-10:15',
#                     4:'10:30-11:15',5:'11:15-12:00',6:'12:00-12:45'}
#     return render_template('admin_timetable.html',
#         classes=classes, sel_class=sel_class, teachers=teachers,
#         days=days, periods=periods, tt=tt, period_times=period_times)

# @app.route('/admin/timetable/save', methods=['POST'])
# def save_timetable():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d  = request.json
#     db = get_db()
#     try:
#         db.execute('''INSERT INTO timetable (class_name,day,period,subject,teacher_id,start_time,end_time)
#             VALUES (?,?,?,?,?,?,?)
#             ON CONFLICT(class_name,day,period) DO UPDATE SET
#             subject=excluded.subject, teacher_id=excluded.teacher_id''',
#             (d['class_name'],d['day'],d['period'],d['subject'],
#              d.get('teacher_id') or None, d.get('start_time',''), d.get('end_time','')))
#         db.commit()
#         return jsonify({'success':True})
#     except Exception as e:
#         return jsonify({'error':str(e)}), 500

# @app.route('/admin/timetable/delete', methods=['POST'])
# def delete_timetable_entry():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d  = request.json
#     db = get_db()
#     db.execute('DELETE FROM timetable WHERE class_name=? AND day=? AND period=?',
#                (d['class_name'],d['day'],d['period']))
#     db.commit()
#     return jsonify({'success':True})

# # ═══════════════════════════════════════════════
# # FEATURE 3: ADMIN ANALYTICS DASHBOARD
# # ═══════════════════════════════════════════════

# @app.route('/admin/analytics')
# def admin_analytics():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()

#     # Fees analytics
#     fee_stats = db.execute('''
#         SELECT class_name,
#                SUM(total_fee) as total_due,
#                SUM(paid_amount) as total_paid,
#                SUM(remaining) as total_remaining,
#                COUNT(CASE WHEN status="Paid" THEN 1 END) as paid_count,
#                COUNT(CASE WHEN status="Pending" THEN 1 END) as pending_count,
#                COUNT(CASE WHEN status="Overdue" THEN 1 END) as overdue_count,
#                COUNT(*) as total_count
#         FROM fees GROUP BY class_name ORDER BY class_name
#     ''').fetchall()

#     # Monthly fee collection
#     monthly = db.execute('''
#         SELECT fee_month, SUM(paid_amount) as collected, SUM(remaining) as pending
#         FROM fees GROUP BY fee_month ORDER BY fee_month
#     ''').fetchall()

#     # Attendance stats per class
#     att_stats = db.execute('''
#         SELECT s.class_name,
#                COUNT(a.id) as total_records,
#                SUM(CASE WHEN a.status="Present" THEN 1 ELSE 0 END) as present_count
#         FROM students s LEFT JOIN attendance a ON s.id=a.student_id
#         GROUP BY s.class_name ORDER BY s.class_name
#     ''').fetchall()

#     # Top students by marks
#     top_students = db.execute('''
#         SELECT s.name, s.class_name, s.roll_number,
#                AVG(m.marks/m.max_marks*100) as avg_pct,
#                COUNT(m.id) as subjects
#         FROM students s JOIN marks m ON s.id=m.student_id
#         GROUP BY s.id HAVING subjects>=2
#         ORDER BY avg_pct DESC LIMIT 10
#     ''').fetchall()

#     # Overall summary
#     summary = {
#         'total_students': db.execute('SELECT COUNT(*) FROM students').fetchone()[0],
#         'total_teachers': db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
#         'total_fee_due':  db.execute('SELECT SUM(total_fee) FROM fees').fetchone()[0] or 0,
#         'total_fee_paid': db.execute('SELECT SUM(paid_amount) FROM fees').fetchone()[0] or 0,
#         'pending_admissions': db.execute("SELECT COUNT(*) FROM admissions WHERE status='Pending'").fetchone()[0],
#         'total_notices': db.execute('SELECT COUNT(*) FROM notices').fetchone()[0],
#     }
#     summary['collection_pct'] = round(summary['total_fee_paid']/summary['total_fee_due']*100 if summary['total_fee_due'] else 0, 1)

#     return render_template('admin_analytics.html',
#         fee_stats=fee_stats, monthly=monthly, att_stats=att_stats,
#         top_students=top_students, summary=summary)

# # ═══════════════════════════════════════════════
# # FEATURE 4: EXAM DATE SHEET
# # ═══════════════════════════════════════════════

# @app.route('/exam_schedule')
# def exam_schedule():
#     db = get_db()
#     exams = db.execute('SELECT * FROM exam_schedule ORDER BY exam_date, class_name').fetchall()
#     classes = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','All')
#     if sel_class != 'All':
#         exams = [e for e in exams if e['class_name']==sel_class]
#     return render_template('exam_schedule.html', exams=exams, classes=classes, sel_class=sel_class)

# @app.route('/admin/exam_schedule')
# def admin_exam_schedule():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     exams = db.execute('SELECT * FROM exam_schedule ORDER BY exam_date, class_name').fetchall()
#     classes = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     return render_template('admin_exam_schedule.html', exams=exams, classes=classes)

# @app.route('/admin/exam_schedule/add', methods=['POST'])
# def add_exam():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     db.execute('INSERT INTO exam_schedule (class_name,subject,exam_date,day,start_time,end_time,exam_type,venue) VALUES (?,?,?,?,?,?,?,?)',
#         (request.form['class_name'], request.form['subject'], request.form['exam_date'],
#          request.form.get('day',''), request.form.get('start_time','10:00'),
#          request.form.get('end_time','13:00'), request.form['exam_type'],
#          request.form.get('venue','Main Hall')))
#     db.commit()
#     flash('Exam added!', 'success')
#     return redirect('/admin/exam_schedule')

# @app.route('/admin/exam_schedule/delete/<int:eid>', methods=['POST'])
# def delete_exam(eid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM exam_schedule WHERE id=?', (eid,))
#     db.commit()
#     return jsonify({'success':True})

# # ═══════════════════════════════════════════════
# # FEATURE 5: PARENT PORTAL
# # ═══════════════════════════════════════════════

# @app.route('/parent/login', methods=['GET','POST'])
# def parent_login():
#     if request.method == 'POST':
#         db = get_db()
#         # Parent logs in with student's roll number + parent contact as password
#         student = db.execute('SELECT * FROM students WHERE roll_number=? AND contact=?',
#             (request.form['roll_number'], request.form['contact'])).fetchone()
#         if student:
#             session.update({'parent_student_id':student['id'],
#                            'parent_student_name':student['name'],
#                            'parent_student_class':student['class_name'],
#                            'parent_name':student['parent_name'],
#                            'role':'parent'})
#             return redirect('/parent/dashboard')
#         flash('Invalid Roll Number or Contact Number.', 'error')
#     return render_template('parent_login.html')

# @app.route('/parent/dashboard')
# def parent_dashboard():
#     if session.get('role') != 'parent': return redirect('/parent/login')
#     db  = get_db()
#     sid = session['parent_student_id']
#     student    = db.execute('SELECT * FROM students WHERE id=?',(sid,)).fetchone()
#     marks      = db.execute('SELECT * FROM marks WHERE student_id=? ORDER BY subject',(sid,)).fetchall()
#     attendance = db.execute('SELECT * FROM attendance WHERE student_id=? ORDER BY date DESC LIMIT 30',(sid,)).fetchall()
#     fees       = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month',(sid,)).fetchall()
#     homework   = db.execute('SELECT * FROM homework WHERE class_name=? ORDER BY due_date DESC LIMIT 10',(session['parent_student_class'],)).fetchall()
#     notices    = db.execute('SELECT * FROM notices ORDER BY created_at DESC LIMIT 5').fetchall()
#     total   = len(attendance)
#     present = sum(1 for a in attendance if a['status']=='Present')
#     pct     = round((present/total*100) if total else 0,1)
#     total_due  = sum(f['total_fee'] for f in fees)
#     total_paid = sum(f['paid_amount'] for f in fees)
#     return render_template('parent_dashboard.html',
#         student=student, marks=marks, attendance=attendance, fees=fees,
#         homework=homework, notices=notices,
#         attend_pct=pct, total_days=total, present_days=present,
#         total_due=total_due, total_paid=total_paid,
#         total_remaining=total_due-total_paid)

# @app.route('/parent/logout')
# def parent_logout():
#     session.clear(); return redirect('/')

# # ═══════════════════════════════════════════════
# # FEATURE 6: LIVE CLASS / VIDEO LINK
# # ═══════════════════════════════════════════════

# @app.route('/live_classes')
# def live_classes():
#     db = get_db()
#     sel_class = request.args.get('class_name', session.get('student_class', 'All'))
#     if sel_class and sel_class != 'All':
#         classes_data = db.execute(
#             'SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id WHERE lc.class_name=? ORDER BY lc.scheduled_at DESC',
#             (sel_class,)).fetchall()
#     else:
#         classes_data = db.execute(
#             'SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id ORDER BY lc.scheduled_at DESC'
#         ).fetchall()
#     all_classes = ['All', 'UKG'] + [f'Class {i}' for i in range(1, 11)]
#     return render_template('live_classes.html', classes_data=classes_data, all_classes=all_classes, sel_class=sel_class)

# @app.route('/teacher/live_classes')
# def teacher_live_classes():
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     my_classes = db.execute(
#         'SELECT * FROM live_classes WHERE teacher_id=? ORDER BY scheduled_at DESC',
#         (session['teacher_id'],)).fetchall()
#     all_classes = ['UKG'] + [f'Class {i}' for i in range(1, 11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit','Drawing','Physical Education']
#     return render_template('teacher_live_classes.html', my_classes=my_classes, all_classes=all_classes, subjects=subjects)

# @app.route('/teacher/add_live_class', methods=['POST'])
# def add_live_class():
#     if session.get('role') != 'teacher': return jsonify({'error': 'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     db.execute(
#         'INSERT INTO live_classes (teacher_id,class_name,subject,title,meet_link,platform,scheduled_at,duration,status,description) VALUES (?,?,?,?,?,?,?,?,?,?)',
#         (session['teacher_id'], d['class_name'], d['subject'], d['title'],
#          d['meet_link'], d['platform'], d['scheduled_at'], d.get('duration', 60),
#          'Upcoming', d.get('description', '')))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/teacher/update_live_class_status', methods=['POST'])
# def update_live_class_status():
#     if session.get('role') != 'teacher': return jsonify({'error': 'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     db.execute('UPDATE live_classes SET status=? WHERE id=? AND teacher_id=?',
#                (d['status'], d['id'], session['teacher_id']))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/teacher/delete_live_class/<int:lcid>', methods=['POST'])
# def delete_live_class(lcid):
#     if session.get('role') != 'teacher': return jsonify({'error': 'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM live_classes WHERE id=? AND teacher_id=?', (lcid, session['teacher_id']))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/api/live_classes')
# def api_live_classes():
#     db = get_db()
#     sel_class = request.args.get('class_name', '')
#     if sel_class:
#         rows = db.execute(
#             '''SELECT lc.*, t.name as teacher_name FROM live_classes lc
#                JOIN teachers t ON lc.teacher_id=t.id
#                WHERE lc.class_name=? AND lc.status != "Completed"
#                ORDER BY lc.status DESC, lc.scheduled_at ASC LIMIT 5''',
#             (sel_class,)).fetchall()
#     else:
#         rows = db.execute(
#             '''SELECT lc.*, t.name as teacher_name FROM live_classes lc
#                JOIN teachers t ON lc.teacher_id=t.id
#                WHERE lc.status != "Completed"
#                ORDER BY lc.status DESC, lc.scheduled_at ASC LIMIT 10''').fetchall()
#     return jsonify([dict(r) for r in rows])

# # ═══════════════════════════════════════════════
# # FEATURE: STUDENT ID CARD GENERATOR (PDF)
# # ═══════════════════════════════════════════════

# @app.route('/admin/id_cards')
# def admin_id_cards():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes  = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','All')
#     if sel_class == 'All':
#         students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id ORDER BY s.class_name, s.roll_number').fetchall()
#     else:
#         students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id WHERE s.class_name=? ORDER BY s.roll_number', (sel_class,)).fetchall()
#     return render_template('admin_id_cards.html', students=students, classes=classes, sel_class=sel_class)

# @app.route('/admin/upload_student_photo/<int:sid>', methods=['POST'])
# def upload_student_photo(sid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
#     file = request.files['photo']
#     ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#     if ext not in {'png','jpg','jpeg','webp'}: return jsonify({'error':'Invalid type'}), 400
#     fname = f"student_{sid}.{ext}"
#     path  = os.path.join(app.root_path,'static','uploads','students',fname)
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     file.save(path)
#     db = get_db()
#     db.execute('INSERT INTO student_photos (student_id,filename) VALUES (?,?) ON CONFLICT(student_id) DO UPDATE SET filename=excluded.filename', (sid,fname))
#     db.commit()
#     return jsonify({'success':True,'filename':fname})

# @app.route('/admin/generate_id_card/<int:sid>')
# def generate_id_card(sid):
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib import colors
#     from reportlab.lib.units import cm
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
#     from reportlab.lib.styles import ParagraphStyle
#     from reportlab.lib.enums import TA_CENTER, TA_LEFT
#     from io import BytesIO
#     from flask import make_response

#     db = get_db()
#     cls_filter = request.args.get('class_name', '')
#     if sid == 0:
#         if cls_filter:
#             students = db.execute('SELECT * FROM students WHERE class_name=? ORDER BY roll_number', (cls_filter,)).fetchall()
#         else:
#             students = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
#     else:
#         students = db.execute('SELECT * FROM students WHERE id=?', (sid,)).fetchall()

#     if not students:
#         flash('No students found.', 'error')
#         return redirect('/admin/id_cards')

#     NAVY  = colors.HexColor('#0d1b3e')
#     GOLD  = colors.HexColor('#c9a84c')
#     CREAM = colors.HexColor('#fdf8f0')
#     WHITE = colors.white

#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4,
#                             rightMargin=1*cm, leftMargin=1*cm,
#                             topMargin=1.5*cm, bottomMargin=1*cm)
#     story = []

#     title_style = ParagraphStyle('t', fontSize=12, fontName='Helvetica-Bold',
#                                  alignment=TA_CENTER, textColor=NAVY, spaceAfter=12)
#     story.append(Paragraph('BrightMind School — Student ID Cards 2024-25', title_style))

#     CARD_W = 8.5 * cm
#     CARD_H = 5.5 * cm

#     def make_card(s):
#         initial = s['name'][0].upper() if s['name'] else '?'
#         # Header row
#         hdr = Table([[Paragraph(f'<font color="white" size="7"><b>BRIGHTMIND SCHOOL · CBSE · 2024-25</b></font>',
#                                 ParagraphStyle('h', alignment=TA_CENTER, fontName='Helvetica-Bold'))]],
#                     colWidths=[CARD_W - 0.4*cm], rowHeights=[0.9*cm])
#         hdr.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
#                                   ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))

#         # Photo cell
#         photo = Table([[Paragraph(f'<font size="22" color="#c9a84c"><b>{initial}</b></font>',
#                                    ParagraphStyle('p', alignment=TA_CENTER))]],
#                       colWidths=[1.8*cm], rowHeights=[2.2*cm])
#         photo.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
#                                     ('ALIGN',(0,0),(-1,-1),'CENTER'),
#                                     ('VALIGN',(0,0),(-1,-1),'MIDDLE')]))

#         # Info
#         name_p  = Paragraph(f'<font size="9" color="#0d1b3e"><b>{s["name"]}</b></font>',
#                              ParagraphStyle('n', fontName='Helvetica-Bold'))
#         class_p = Paragraph(f'<font size="8" color="#0d1b3e">Class: <b>{s["class_name"]}</b></font>',
#                              ParagraphStyle('c'))
#         roll_p  = Paragraph(f'<font size="8" color="#0d1b3e">Roll No: <b>{s["roll_number"]}</b></font>',
#                              ParagraphStyle('r'))
#         sess_p  = Paragraph(f'<font size="7.5" color="#666">Session: 2024-25</font>',
#                              ParagraphStyle('s'))
#         info_rows = [[name_p],[class_p],[roll_p],[sess_p]]
#         info = Table(info_rows, colWidths=[CARD_W - 2.4*cm],
#                      rowHeights=[0.55*cm, 0.5*cm, 0.5*cm, 0.5*cm])
#         info.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),2),
#                                    ('BOTTOMPADDING',(0,0),(-1,-1),2),
#                                    ('LEFTPADDING',(0,0),(-1,-1),6)]))

#         body = Table([[photo, info]], colWidths=[1.9*cm, CARD_W - 2.3*cm], rowHeights=[2.4*cm])
#         body.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),
#                                    ('LEFTPADDING',(0,0),(-1,-1),4),
#                                    ('TOPPADDING',(0,0),(-1,-1),8),
#                                    ('BOTTOMPADDING',(0,0),(-1,-1),4)]))

#         footer = Table([[Paragraph('<font size="6.5" color="#888">Ph: +91 11 1234 5678 | Delhi-110001</font>',
#                                     ParagraphStyle('f', alignment=TA_CENTER))]],
#                        colWidths=[CARD_W - 0.4*cm], rowHeights=[0.55*cm])
#         footer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),CREAM),
#                                      ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))

#         card = Table([[hdr],[body],[footer]],
#                      colWidths=[CARD_W],
#                      rowHeights=[0.9*cm, CARD_H - 1.55*cm, 0.65*cm])
#         card.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.5,GOLD),
#                                    ('TOPPADDING',(0,0),(-1,-1),0),
#                                    ('BOTTOMPADDING',(0,0),(-1,-1),0),
#                                    ('LEFTPADDING',(0,0),(-1,-1),0),
#                                    ('RIGHTPADDING',(0,0),(-1,-1),0)]))
#         return card

#     # Layout: 2 cards per row
#     SPACER_W = 0.8*cm
#     pair_w   = [CARD_W + SPACER_W/2, CARD_W + SPACER_W/2]

#     i = 0
#     while i < len(students):
#         row_data = []
#         if i < len(students):     row_data.append(make_card(students[i]))
#         else:                      row_data.append(Paragraph('', ParagraphStyle('e')))
#         if i+1 < len(students):   row_data.append(make_card(students[i+1]))
#         else:                      row_data.append(Paragraph('', ParagraphStyle('e')))

#         row_tbl = Table([row_data], colWidths=pair_w, rowHeights=[CARD_H + 0.4*cm])
#         row_tbl.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
#                                       ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
#                                       ('TOPPADDING',(0,0),(-1,-1),4),
#                                       ('BOTTOMPADDING',(0,0),(-1,-1),4)]))
#         story.append(row_tbl)
#         i += 2

#     doc.build(story)
#     pdf  = buffer.getvalue()
#     buffer.close()

#     name = students[0]['name'] if len(students)==1 else f'{cls_filter or "All"}_Students'
#     resp = make_response(pdf)
#     resp.headers['Content-Type']        = 'application/pdf'
#     resp.headers['Content-Disposition'] = f'attachment; filename=ID_Cards_{name}.pdf'
#     return resp


# @app.route('/admin/generate_all_id_cards')
# def generate_all_id_cards():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib import colors
#     from reportlab.lib.units import cm
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
#     from reportlab.lib.styles import ParagraphStyle
#     from reportlab.lib.enums import TA_CENTER, TA_LEFT
#     from io import BytesIO
#     from flask import make_response

#     db = get_db()
#     cls = request.args.get('class_name','')
#     if cls:
#         students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id WHERE s.class_name=? ORDER BY s.roll_number',(cls,)).fetchall()
#     else:
#         students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id ORDER BY s.class_name, s.roll_number').fetchall()

#     NAVY=colors.HexColor('#0d1b3e'); GOLD=colors.HexColor('#c9a84c'); CREAM=colors.HexColor('#fdf8f0')
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1*cm, rightMargin=1*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
#     story = []; card_w=8.56*cm; card_h=5.4*cm

#     title_s = ParagraphStyle('t',fontSize=14,fontName='Helvetica-Bold',textColor=NAVY,alignment=TA_CENTER,spaceAfter=12)
#     story.append(Paragraph(f'BrightMind School — Student ID Cards {"(" + cls + ")" if cls else "(All Classes)"}', title_s))

#     cards = []
#     for student in students:
#         if student['photo']:
#             photo_path = os.path.join(app.root_path,'static','uploads','students',student['photo'])
#             photo_cell = RLImage(photo_path,width=1.8*cm,height=1.8*cm) if os.path.exists(photo_path) else Paragraph(student['name'][0], ParagraphStyle('i',fontSize=18,fontName='Helvetica-Bold',textColor=GOLD,alignment=TA_CENTER))
#         else:
#             photo_cell = Paragraph(student['name'][0], ParagraphStyle('i',fontSize=18,fontName='Helvetica-Bold',textColor=GOLD,alignment=TA_CENTER))

#         info = Table([
#             [Paragraph(f'<b>{student["name"]}</b>', ParagraphStyle('n',fontSize=7.5,fontName='Helvetica-Bold',textColor=NAVY,leading=10))],
#             [Paragraph(f'Class: <b>{student["class_name"]}</b>', ParagraphStyle('c',fontSize=6.5,leading=9))],
#             [Paragraph(f'Roll: <b>{student["roll_number"]}</b>', ParagraphStyle('r',fontSize=6.5,leading=9))],
#             [Paragraph('Session: 2024-25', ParagraphStyle('s',fontSize=6,textColor=colors.HexColor('#555'),leading=8))],
#         ], colWidths=[card_w-2.2*cm])
#         info.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))

#         header = Table([[Paragraph('<font color="white"><b>BRIGHTMIND SCHOOL</b></font>', ParagraphStyle('h',fontSize=6.5,fontName='Helvetica-Bold',alignment=TA_CENTER))]], colWidths=[card_w])
#         header.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
#         mid = Table([[photo_cell, info]], colWidths=[2*cm, card_w-2*cm])
#         mid.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BACKGROUND',(0,0),(-1,-1),CREAM)]))
#         footer = Table([[Paragraph(f'📞 {student["contact"] or "—"}', ParagraphStyle('f',fontSize=5.5,textColor=colors.white,alignment=TA_LEFT))]], colWidths=[card_w])
#         footer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),GOLD),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),6)]))

#         card = Table([[header],[mid],[footer]], colWidths=[card_w], rowHeights=[0.8*cm,3.8*cm,0.6*cm])
#         card.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.5,NAVY),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
#         cards.append(card)

#     # 2 cards per row
#     for i in range(0, len(cards), 2):
#         row = cards[i:i+2]
#         if len(row) == 1: row.append(Spacer(card_w,card_h))
#         story.append(Table([row], colWidths=[card_w+0.5*cm]*2))
#         story.append(Spacer(1,0.5*cm))

#     doc.build(story)
#     pdf=buffer.getvalue(); buffer.close()
#     resp=make_response(pdf)
#     resp.headers['Content-Type']='application/pdf'
#     resp.headers['Content-Disposition']=f'attachment; filename=IDCards_{cls or "All"}.pdf'
#     return resp

# # ═══════════════════════════════════════════════
# # FEATURE: WHATSAPP NOTIFICATION SYSTEM
# # ═══════════════════════════════════════════════

# @app.route('/admin/notifications')
# def admin_notifications():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     logs      = db.execute('SELECT * FROM notifications ORDER BY sent_at DESC LIMIT 50').fetchall()
#     students  = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id ORDER BY s.class_name').fetchall()
#     classes   = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     pending_fees = db.execute('''SELECT s.name, s.contact, s.class_name, f.fee_month, f.remaining
#         FROM fees f JOIN students s ON f.student_id=s.id
#         WHERE f.status IN ("Pending","Overdue") AND s.contact IS NOT NULL
#         ORDER BY f.status DESC, s.class_name''').fetchall()
#     return render_template('admin_notifications.html', logs=logs, students=students, classes=classes, pending_fees=pending_fees)

# @app.route('/admin/send_notification', methods=['POST'])
# def send_notification():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     recipients = []
#     msg_type = d.get('type','custom')
#     message  = d.get('message','')

#     if d.get('target') == 'all':
#         students = db.execute('SELECT * FROM students WHERE contact IS NOT NULL').fetchall()
#         recipients = [(s['name'], s['contact']) for s in students]
#     elif d.get('target') == 'class':
#         students = db.execute('SELECT * FROM students WHERE class_name=? AND contact IS NOT NULL',(d['class_name'],)).fetchall()
#         recipients = [(s['name'], s['contact']) for s in students]
#     elif d.get('target') == 'fee_pending':
#         rows = db.execute('''SELECT s.name, s.contact, s.class_name, f.fee_month, f.remaining
#             FROM fees f JOIN students s ON f.student_id=s.id
#             WHERE f.status IN ("Pending","Overdue") AND s.contact IS NOT NULL''').fetchall()
#         for r in rows:
#             msg = f"Dear Parent of {r['name']} ({r['class_name']}), Fee of ₹{int(r['remaining'])} for {r['fee_month']} is pending. Please pay at earliest. — BrightMind School"
#             recipients.append((r['name'], r['contact'], msg))
#     elif d.get('student_id'):
#         s = db.execute('SELECT * FROM students WHERE id=?',(d['student_id'],)).fetchone()
#         if s and s['contact']:
#             recipients = [(s['name'], s['contact'])]

#     sent = 0
#     for rec in recipients:
#         name    = rec[0]
#         contact = rec[1]
#         custom_msg = rec[2] if len(rec) > 2 else message.replace('{name}', name)

#         # Generate WhatsApp link (wa.me) — simulated
#         wa_link = f"https://wa.me/91{contact}?text={custom_msg.replace(' ','%20')}"

#         db.execute('INSERT INTO notifications (type,recipient,message,status) VALUES (?,?,?,?)',
#                    (msg_type, f"{name} ({contact})", custom_msg[:200], "Sent (WA Link)"))
#         sent += 1

#     db.commit()
#     return jsonify({'success':True, 'sent':sent})

# # ═══════════════════════════════════════════════
# # FEATURE: ONLINE TEST / QUIZ
# # ═══════════════════════════════════════════════

# @app.route('/teacher/quizzes')
# def teacher_quizzes():
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     quizzes = db.execute('SELECT q.*, COUNT(qq.id) as q_count FROM quizzes q LEFT JOIN quiz_questions qq ON q.id=qq.quiz_id WHERE q.teacher_id=? GROUP BY q.id ORDER BY q.created_at DESC',(session['teacher_id'],)).fetchall()
#     classes  = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit']
#     return render_template('teacher_quizzes.html', quizzes=quizzes, classes=classes, subjects=subjects)

# @app.route('/teacher/create_quiz', methods=['POST'])
# def create_quiz():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     cur = db.execute('INSERT INTO quizzes (teacher_id,title,class_name,subject,duration,total_marks,status) VALUES (?,?,?,?,?,?,?)',
#         (session['teacher_id'],d['title'],d['class_name'],d['subject'],d.get('duration',30),d.get('total_marks',10),'Draft'))
#     qid = cur.lastrowid
#     for q in d.get('questions',[]):
#         db.execute('INSERT INTO quiz_questions (quiz_id,question,option_a,option_b,option_c,option_d,correct,marks) VALUES (?,?,?,?,?,?,?,?)',
#             (qid,q['question'],q['a'],q['b'],q['c'],q['d'],q['correct'],q.get('marks',1)))
#     db.commit()
#     return jsonify({'success':True,'quiz_id':qid})

# @app.route('/teacher/publish_quiz/<int:qid>', methods=['POST'])
# def publish_quiz(qid):
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute("UPDATE quizzes SET status='Active' WHERE id=? AND teacher_id=?",(qid,session['teacher_id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/quiz_results/<int:qid>')
# def quiz_results(qid):
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     quiz    = db.execute('SELECT * FROM quizzes WHERE id=?',(qid,)).fetchone()
#     results = db.execute('SELECT qa.*, s.name, s.roll_number FROM quiz_attempts qa JOIN students s ON qa.student_id=s.id WHERE qa.quiz_id=? ORDER BY qa.score DESC',(qid,)).fetchall()
#     return render_template('quiz_results.html', quiz=quiz, results=results)

# @app.route('/student/quizzes')
# def student_quizzes():
#     if session.get('role') != 'student': return redirect('/student/login')
#     db = get_db()
#     sid = session['student_id']
#     quizzes = db.execute('''SELECT q.*, t.name as teacher_name,
#         (SELECT score FROM quiz_attempts WHERE quiz_id=q.id AND student_id=?) as my_score,
#         (SELECT submitted_at FROM quiz_attempts WHERE quiz_id=q.id AND student_id=?) as attempted_at
#         FROM quizzes q JOIN teachers t ON q.teacher_id=t.id
#         WHERE q.class_name=? AND q.status="Active" ORDER BY q.created_at DESC''',(sid,sid,session['student_class'])).fetchall()
#     return render_template('student_quizzes.html', quizzes=quizzes)

# @app.route('/student/attempt_quiz/<int:qid>')
# def attempt_quiz(qid):
#     if session.get('role') != 'student': return redirect('/student/login')
#     db = get_db()
#     sid = session['student_id']
#     attempted = db.execute('SELECT id FROM quiz_attempts WHERE quiz_id=? AND student_id=?',(qid,sid)).fetchone()
#     if attempted: return redirect('/student/quiz_result/'+str(qid))
#     quiz      = db.execute('SELECT * FROM quizzes WHERE id=? AND status="Active"',(qid,)).fetchone()
#     questions = db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
#     if not quiz: return redirect('/student/quizzes')
#     return render_template('attempt_quiz.html', quiz=quiz, questions=questions)

# @app.route('/student/submit_quiz/<int:qid>', methods=['POST'])
# def submit_quiz(qid):
#     if session.get('role') != 'student': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     sid = session['student_id']
#     questions = db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
#     score = 0; answers = {}
#     for q in questions:
#         ans = d.get(str(q['id']),'')
#         answers[q['id']] = ans
#         if ans.upper() == q['correct'].upper():
#             score += q['marks']
#     import json as json_lib
#     db.execute('INSERT OR IGNORE INTO quiz_attempts (quiz_id,student_id,score,total,answers) VALUES (?,?,?,?,?)',
#                (qid,sid,score,len(questions),json_lib.dumps(answers)))
#     db.commit()
#     return jsonify({'success':True,'score':score,'total':len(questions)})

# @app.route('/student/quiz_result/<int:qid>')
# def student_quiz_result(qid):
#     if session.get('role') != 'student': return redirect('/student/login')
#     db = get_db()
#     sid = session['student_id']
#     quiz     = db.execute('SELECT q.*, t.name as teacher_name FROM quizzes q JOIN teachers t ON q.teacher_id=t.id WHERE q.id=?',(qid,)).fetchone()
#     attempt  = db.execute('SELECT * FROM quiz_attempts WHERE quiz_id=? AND student_id=?',(qid,sid)).fetchone()
#     questions= db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
#     import json as json_lib
#     answers  = json_lib.loads(attempt['answers']) if attempt and attempt['answers'] else {}
#     return render_template('quiz_result.html', quiz=quiz, attempt=attempt, questions=questions, answers=answers)

# # ═══════════════════════════════════════════════
# # FEATURE: STUDENT ACHIEVEMENTS / AWARDS
# # ═══════════════════════════════════════════════

# @app.route('/achievements')

# def achievements():
#     db = get_db()
#     featured = []  # featured column removed
#     all_ach  = db.execute('SELECT a.*, s.name as student_name FROM achievements a LEFT JOIN students s ON a.student_id=s.id ORDER BY a.achievement_date DESC').fetchall()
#     categories = db.execute('SELECT DISTINCT category FROM achievements ORDER BY category').fetchall()
#     sel_cat  = request.args.get('category','All')
#     if sel_cat != 'All':
#         all_ach = [a for a in all_ach if a['category']==sel_cat]
#     return render_template('achievements.html', featured=featured, all_ach=all_ach, categories=categories, sel_cat=sel_cat)

# @app.route('/admin/achievements')
# def admin_achievements():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     ach      = db.execute('SELECT *, COALESCE(student_name,"") as student_name FROM achievements ORDER BY created_at DESC').fetchall()
#     students = db.execute('SELECT id, name, class_name FROM students ORDER BY class_name, name').fetchall()
#     return render_template('admin_achievements.html', achievements=ach, students=students)

# @app.route('/admin/add_achievement', methods=['POST'])
# def add_achievement():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     sid        = request.form.get('student_id') or None
#     sname      = request.form.get('student_name','').strip()
#     cls        = request.form.get('class_name','')
#     # If student selected from dropdown, get their name and class
#     if sid:
#         s = db.execute('SELECT name, class_name FROM students WHERE id=?',(sid,)).fetchone()
#         if s:
#             sname = s['name']
#             cls   = s['class_name']
#     # Handle photo upload
#     photo = None
#     if 'photo' in request.files and request.files['photo'].filename:
#         file = request.files['photo']
#         ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#         if ext in {'jpg','jpeg','png','gif','webp'}:
#             fname = f"ach_{uuid.uuid4().hex[:8]}.{ext}"
#             path  = os.path.join(app.root_path,'static','uploads','achievements',fname)
#             os.makedirs(os.path.dirname(path), exist_ok=True)
#             file.save(path)
#             photo = fname
#     db.execute('''INSERT INTO achievements
#         (student_id,student_name,class_name,title,category,description,achievement_date,is_featured,photo)
#         VALUES (?,?,?,?,?,?,?,?,?)''',
#         (sid, sname, cls,
#          request.form.get('title',''),
#          request.form.get('category','Academic'),
#          request.form.get('description',''),
#          request.form.get('achievement_date',''),
#          1 if request.form.get('is_featured') else 0,
#          photo))
#     db.commit()
#     flash('Achievement added!','success')
#     return redirect('/admin/achievements')

# @app.route('/admin/delete_achievement/<int:aid>', methods=['POST'])
# def delete_achievement(aid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM achievements WHERE id=?',(aid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/toggle_featured/<int:aid>', methods=['POST'])
# def toggle_featured(aid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     cur = db.execute('SELECT is_featured FROM achievements WHERE id=?',(aid,)).fetchone()
#     db.execute('UPDATE achievements SET is_featured=? WHERE id=?',(0 if cur['is_featured'] else 1, aid)); db.commit()
#     return jsonify({'success':True})

# # ═══════════════════════════════════════════════
# # FEATURE 7: ONLINE QUIZ / TEST
# # ═══════════════════════════════════════════════

# @app.route('/student/quizzes')
# @app.route('/student/quiz/<int:qid>')
# @app.route('/student/quiz/<int:qid>/submit', methods=['POST'])
# @app.route('/teacher/quizzes')
# @app.route('/teacher/quiz/create', methods=['POST'])
# @app.route('/teacher/quiz/<int:qid>/toggle', methods=['POST'])
# def toggle_quiz(qid):
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     q  = db.execute('SELECT status FROM quizzes WHERE id=? AND teacher_id=?',(qid,session['teacher_id'])).fetchone()
#     if not q: return jsonify({'error':'Not found'}), 404
#     new_status = 'Active' if q['status']=='Draft' else 'Draft'
#     db.execute('UPDATE quizzes SET status=? WHERE id=?',(new_status,qid))
#     db.commit()
#     return jsonify({'success':True,'status':new_status})

# @app.route('/teacher/quiz/<int:qid>/results')
# @app.route('/teacher/quiz/<int:qid>/delete', methods=['POST'])
# def delete_quiz(qid):
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM quiz_attempts WHERE quiz_id=?',(qid,))
#     db.execute('DELETE FROM quiz_questions WHERE quiz_id=?',(qid,))
#     db.execute('DELETE FROM quizzes WHERE id=? AND teacher_id=?',(qid,session['teacher_id']))
#     db.commit()
#     return jsonify({'success':True})

# # ═══════════════════════════════════════════════
# # FEATURE 9: ACHIEVEMENTS / AWARDS
# # ═══════════════════════════════════════════════

# # ═══════════════════════════════════════════════
# # FEATURE 10: STUDENT ID CARD PDF GENERATOR
# # ═══════════════════════════════════════════════

# # ═══════════════════════════════════════════════
# # FEATURE 2: WHATSAPP NOTIFICATION (Simulation)
# # ═══════════════════════════════════════════════


# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

# # ═══════════════════════════════════════════════
# # ADMIN — Live Classes Management
# # ═══════════════════════════════════════════════

# @app.route('/admin/live_classes')
# def admin_live_classes():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes_data = db.execute('''
#         SELECT lc.*, t.name as teacher_name
#         FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id
#         ORDER BY lc.status ASC, lc.scheduled_at DESC
#     ''').fetchall()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     all_classes = ['UKG'] + [f'Class {i}' for i in range(1, 11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit','Drawing','Physical Education']
#     # Stats
#     stats = {
#         'total':     len(classes_data),
#         'live':      sum(1 for lc in classes_data if lc['status']=='Live'),
#         'upcoming':  sum(1 for lc in classes_data if lc['status']=='Upcoming'),
#         'completed': sum(1 for lc in classes_data if lc['status']=='Completed'),
#     }
#     return render_template('admin_live_classes.html',
#         classes_data=classes_data, teachers=teachers,
#         all_classes=all_classes, subjects=subjects, stats=stats)

# @app.route('/admin/live_classes/add', methods=['POST'])
# def admin_add_live_class():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     db.execute('''INSERT INTO live_classes
#         (teacher_id,class_name,subject,title,meet_link,platform,scheduled_at,duration,status,description)
#         VALUES (?,?,?,?,?,?,?,?,?,?)''',
#         (d['teacher_id'], d['class_name'], d['subject'], d['title'],
#          d['meet_link'], d['platform'], d['scheduled_at'],
#          d.get('duration',60), d.get('status','Upcoming'), d.get('description','')))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/admin/live_classes/update_status', methods=['POST'])
# def admin_update_live_status():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     db.execute('UPDATE live_classes SET status=? WHERE id=?', (d['status'], d['id']))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/admin/live_classes/delete/<int:lcid>', methods=['POST'])
# def admin_delete_live_class(lcid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM live_classes WHERE id=?', (lcid,))
#     db.commit()
#     return jsonify({'success': True})

# # ═══════════════════════════════════════════════
# # ADMIN QUIZ MANAGER
# # ═══════════════════════════════════════════════

# @app.route('/admin/quiz_manager')
# def admin_quiz_manager():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     quizzes = db.execute('''
#         SELECT q.*, t.name as teacher_name,
#                COUNT(qa.id) as attempt_count,
#                AVG(CASE WHEN qa.total > 0 THEN qa.score*100.0/qa.total END) as avg_score
#         FROM quizzes q
#         LEFT JOIN teachers t ON q.teacher_id=t.id
#         LEFT JOIN quiz_attempts qa ON q.id=qa.quiz_id
#         GROUP BY q.id ORDER BY q.created_at DESC
#     ''').fetchall()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     classes  = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit']
#     return render_template('admin_quiz_manager.html',
#         quizzes=quizzes, teachers=teachers, classes=classes, subjects=subjects)

# @app.route('/admin/quiz/toggle/<int:qid>', methods=['POST'])
# def admin_toggle_quiz(qid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     q  = db.execute('SELECT status FROM quizzes WHERE id=?', (qid,)).fetchone()
#     if not q: return jsonify({'error':'Not found'}), 404
#     new_status = 'Active' if q['status'] == 'Draft' else 'Draft'
#     db.execute('UPDATE quizzes SET status=? WHERE id=?', (new_status, qid))
#     db.commit()
#     return jsonify({'success': True, 'status': new_status})

# @app.route('/admin/quiz/delete/<int:qid>', methods=['POST'])
# def admin_delete_quiz(qid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM quiz_attempts WHERE quiz_id=?', (qid,))
#     db.execute('DELETE FROM quiz_questions WHERE quiz_id=?', (qid,))
#     db.execute('DELETE FROM quizzes WHERE id=?', (qid,))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/admin/quiz/<int:qid>/results')
# def admin_quiz_results(qid):
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     quiz    = db.execute('SELECT q.*,t.name as tname FROM quizzes q JOIN teachers t ON q.teacher_id=t.id WHERE q.id=?',(qid,)).fetchone()
#     results = db.execute('''SELECT qa.*,s.name as student_name,s.roll_number,s.class_name
#         FROM quiz_attempts qa JOIN students s ON qa.student_id=s.id
#         WHERE qa.quiz_id=? ORDER BY qa.score DESC''',(qid,)).fetchall()
#     questions = db.execute('SELECT COUNT(*) FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchone()[0]
#     return render_template('admin_quiz_results.html', quiz=quiz, results=results, question_count=questions)

# @app.route('/achievers')
# def achievers_page():
#     db      = get_db()
#     sel_cat = request.args.get('category', 'All')
#     sel_cls = request.args.get('class_name', 'All')
#     classes = ['Class 5','Class 6','Class 7','Class 8','Class 9','Class 10']

#     query  = "SELECT *, COALESCE(student_name,'') as student_name FROM achievements WHERE class_name IN ('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')"
#     params = []
#     if sel_cat != 'All':
#         query += ' AND category=?'; params.append(sel_cat)
#     if sel_cls != 'All':
#         query += ' AND class_name=?'; params.append(sel_cls)
#     query += ' ORDER BY achievement_date DESC'

#     items    = db.execute(query, params).fetchall()
#     cats_raw = db.execute("SELECT DISTINCT category FROM achievements WHERE class_name IN ('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')").fetchall()
#     cats     = [r['category'] for r in cats_raw]

#     # Count per class for tab badges
#     class_counts = {}
#     for cls in classes:
#         n = db.execute("SELECT COUNT(*) FROM achievements WHERE class_name=?", (cls,)).fetchone()[0]
#         if n > 0:
#             class_counts[cls] = n

#     return render_template('achievers.html', items=items, cats=cats,
#                            sel_cat=sel_cat, sel_cls=sel_cls,
#                            classes=classes, class_counts=class_counts)

# @app.route('/achievers/<int:aid>')
# def achiever_detail(aid):
#     db   = get_db()
#     item = db.execute("SELECT *, COALESCE(student_name,'') as student_name FROM achievements WHERE id=?", (aid,)).fetchone()
#     if not item:
#         flash('Achievement not found.','error')
#         return redirect('/achievers')
#     # Get other achievements by same student
#     others = db.execute(
#         "SELECT *, COALESCE(student_name,'') as student_name FROM achievements WHERE class_name=? AND id!=? ORDER BY achievement_date DESC LIMIT 4",
#         (item['class_name'], aid)
#     ).fetchall()
#     return render_template('achiever_detail.html', item=item, others=others)

# # ── ALIAS ROUTES (fix 404 errors) ─────────────────────────────────────────────

# @app.route('/admin/achievements/add', methods=['POST'])
# def add_achievement_alias():
#     """Alias for /admin/add_achievement — fixes 404"""
#     return add_achievement()

# @app.route('/admin/achievements/delete/<int:aid>', methods=['POST'])
# def delete_achievement_alias(aid):
#     """Alias for /admin/delete_achievement/<id> — fixes 404"""
#     return delete_achievement(aid)















# from flask import Flask, render_template, request, redirect, session, flash, jsonify
# import sqlite3, os, uuid
# from werkzeug.utils import secure_filename   # ✅ ADD THIS

# from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# from database.db import init_db, get_db
# import os, uuid

# app = Flask(__name__)
# app.secret_key = 'brightmind_school_2024'

# with app.app_context():
#     init_db()

# # ── PUBLIC ─────────────────────────────────────────────────────────────────────
# @app.route('/')
# def home():
#     db = get_db()
#     notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC LIMIT 4').fetchall()
#     featured_achievers = db.execute(
#         """SELECT * FROM achievements
#            WHERE class_name IN ('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')
#            ORDER BY class_name, achievement_date DESC LIMIT 12"""
#     ).fetchall()
#     return render_template('home.html', notices=notices, featured_achievers=featured_achievers)

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/admissions', methods=['GET','POST'])
# def admissions():
#     if request.method == 'POST':
#         db = get_db()
#         db.execute('INSERT INTO admissions (name,dob,class_name,parent_name,contact,email,address,status) VALUES (?,?,?,?,?,?,?,?)',
#             (request.form['name'], request.form['dob'], request.form['class_name'],
#              request.form['parent_name'], request.form['contact'], request.form['email'],
#              request.form['address'], 'Pending'))
#         db.commit()
#         flash('Admission form submitted! We will contact you soon.', 'success')
#         return redirect('/admissions')
#     return render_template('admissions.html')

# @app.route('/academics')
# def academics():
#     return render_template('academics.html')

# @app.route('/notices')
# def notices():
#     db = get_db()
#     all_notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC').fetchall()
#     return render_template('notices.html', notices=all_notices)

# @app.route('/contact', methods=['GET','POST'])
# def contact():
#     if request.method == 'POST':
#         db = get_db()
#         db.execute('INSERT INTO contact_messages (name,email,subject,message) VALUES (?,?,?,?)',
#             (request.form['name'], request.form['email'], request.form['subject'], request.form['message']))
#         db.commit()
#         flash('Message sent! We will reply shortly.', 'success')
#         return redirect('/contact')
#     return render_template('contact.html')

# # ── TEACHERS PUBLIC ────────────────────────────────────────────────────────────
# @app.route('/teachers')
# def teachers_list():
#     db = get_db()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     return render_template('teachers.html', teachers=teachers)

# @app.route('/teachers/<int:teacher_id>')
# def teacher_profile(teacher_id):
#     db = get_db()
#     teacher = db.execute('SELECT * FROM teachers WHERE id=?', (teacher_id,)).fetchone()
#     if not teacher:
#         flash('Teacher not found.', 'error')
#         return redirect('/teachers')
#     assignments = db.execute(
#         'SELECT class_name, subject FROM teacher_assignments WHERE teacher_id=? ORDER BY class_name',
#         (teacher_id,)).fetchall()
#     return render_template('teacher_profile.html', teacher=teacher, assignments=assignments)

# # ── GALLERY PUBLIC ─────────────────────────────────────────────────────────────
# @app.route('/gallery')
# def gallery():
#     db = get_db()
#     sel_cat = request.args.get('category', 'All')
#     if sel_cat == 'All':
#         photos = db.execute('SELECT * FROM gallery_photos ORDER BY uploaded_at DESC').fetchall()
#     else:
#         photos = db.execute('SELECT * FROM gallery_photos WHERE category=? ORDER BY uploaded_at DESC', (sel_cat,)).fetchall()
#     categories = db.execute('SELECT DISTINCT category FROM gallery_photos ORDER BY category').fetchall()
#     return render_template('gallery.html', photos=photos, categories=categories, sel_cat=sel_cat)

# # ── STUDENT PORTAL ─────────────────────────────────────────────────────────────
# @app.route('/student/login', methods=['GET','POST'])
# def student_login():
#     if request.method == 'POST':
#         db = get_db()
#         s = db.execute('SELECT * FROM students WHERE roll_number=? AND password=?',
#             (request.form['roll_number'], request.form['password'])).fetchone()
#         if s:
#             session.update({'student_id':s['id'],'student_name':s['name'],'student_class':s['class_name'],'role':'student'})
#             return redirect('/student/dashboard')
#         flash('Invalid credentials.', 'error')
#     return render_template('student_login.html')

# @app.route('/student/dashboard')
# def student_dashboard():
#     if session.get('role') != 'student': return redirect('/student/login')
#     db  = get_db()
#     sid = session['student_id']
#     marks      = db.execute('SELECT * FROM marks WHERE student_id=?', (sid,)).fetchall()
#     attendance = db.execute('SELECT * FROM attendance WHERE student_id=? ORDER BY date DESC LIMIT 30', (sid,)).fetchall()
#     homework   = db.execute('SELECT * FROM homework WHERE class_name=? ORDER BY due_date DESC', (session['student_class'],)).fetchall()
#     fees       = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month', (sid,)).fetchall()
#     total   = len(attendance)
#     present = sum(1 for a in attendance if a['status'] == 'Present')
#     pct     = round((present/total*100) if total else 0, 1)
#     return render_template('student_dashboard.html',
#         marks=marks, attendance=attendance, homework=homework, fees=fees,
#         attend_pct=pct, total_days=total, present_days=present)

# @app.route('/student/logout')
# def student_logout():
#     session.clear(); return redirect('/')

# # ── TEACHER PORTAL ─────────────────────────────────────────────────────────────
# @app.route('/teacher/login', methods=['GET','POST'])
# def teacher_login():
#     if request.method == 'POST':
#         db = get_db()
#         t = db.execute('SELECT * FROM teachers WHERE username=? AND password=?',
#             (request.form['username'], request.form['password'])).fetchone()
#         if t:
#             session.update({'teacher_id':t['id'],'teacher_name':t['name'],'teacher_sub':t['subject'],'role':'teacher'})
#             return redirect('/teacher/dashboard')
#         flash('Invalid credentials.', 'error')
#     return render_template('teacher_login.html')

# @app.route('/teacher/dashboard')
# def teacher_dashboard():
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     classes  = db.execute('SELECT DISTINCT class_name FROM students ORDER BY class_name').fetchall()
#     students = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
#     homework = db.execute('SELECT h.*,t.name as tname FROM homework h JOIN teachers t ON h.teacher_id=t.id ORDER BY due_date DESC').fetchall()
#     return render_template('teacher_dashboard.html', classes=classes, students=students, homework=homework)

# @app.route('/teacher/upload_marks', methods=['POST'])
# def upload_marks():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('INSERT OR REPLACE INTO marks (student_id,subject,marks,max_marks,exam_type) VALUES (?,?,?,?,?)',
#         (d['student_id'],d['subject'],d['marks'],d['max_marks'],d['exam_type']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/attendance', methods=['POST'])
# def mark_attendance():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     for r in d['records']:
#         db.execute('INSERT OR REPLACE INTO attendance (student_id,date,status) VALUES (?,?,?)',
#             (r['student_id'],d['date'],r['status']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/upload_homework', methods=['POST'])
# def upload_homework():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('INSERT INTO homework (class_name,subject,description,due_date,teacher_id) VALUES (?,?,?,?,?)',
#         (d['class_name'],d['subject'],d['description'],d['due_date'],session['teacher_id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/logout')
# def teacher_logout():
#     session.clear(); return redirect('/')

# # ── ADMIN LOGIN ────────────────────────────────────────────────────────────────
# @app.route('/admin/login', methods=['GET','POST'])
# def admin_login():
#     if request.method == 'POST':
#         if request.form['username']=='admin' and request.form['password']=='admin123':
#             session['role'] = 'admin'; return redirect('/admin/dashboard')
#         flash('Wrong credentials.', 'error')
#     return render_template('admin_login.html')

# @app.route('/admin/logout')
# def admin_logout():
#     session.clear(); return redirect('/')

# # ── ADMIN DASHBOARD ────────────────────────────────────────────────────────────
# @app.route('/admin/dashboard')
# def admin_dashboard():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     stats = {
#         'students':   db.execute('SELECT COUNT(*) FROM students').fetchone()[0],
#         'teachers':   db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
#         'admissions': db.execute("SELECT COUNT(*) FROM admissions WHERE status='Pending'").fetchone()[0],
#         'notices':    db.execute('SELECT COUNT(*) FROM notices').fetchone()[0],
#     }
#     admissions  = db.execute('SELECT * FROM admissions ORDER BY created_at DESC').fetchall()
#     messages    = db.execute('SELECT * FROM contact_messages ORDER BY created_at DESC').fetchall()
#     students    = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
#     teachers    = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     all_notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC').fetchall()
#     return render_template('admin_dashboard.html',
#         stats=stats, admissions=admissions, messages=messages,
#         students=students, teachers=teachers, all_notices=all_notices)

# # ── ADMIN STUDENTS ─────────────────────────────────────────────────────────────
# @app.route('/admin/add_student', methods=['POST'])
# def add_student():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     try:
#         db.execute('INSERT INTO students (name,class_name,roll_number,parent_name,contact,password) VALUES (?,?,?,?,?,?)',
#             (request.form['name'],request.form['class_name'],request.form['roll_number'],
#              request.form['parent_name'],request.form['contact'],request.form['password']))
#         db.commit(); flash('Student added!', 'success')
#     except: flash('Error: Roll number may already exist.', 'error')
#     return redirect('/admin/dashboard')

# @app.route('/admin/delete_student/<int:sid>', methods=['POST'])
# def delete_student(sid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     for tbl in ['marks','attendance','fees']: db.execute(f'DELETE FROM {tbl} WHERE student_id=?', (sid,))
#     db.execute('DELETE FROM students WHERE id=?', (sid,)); db.commit()
#     return jsonify({'success':True})

# # ── ADMIN TEACHERS ─────────────────────────────────────────────────────────────
# @app.route('/admin/add_teacher', methods=['POST'])
# def add_teacher():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     try:
#         db.execute('INSERT INTO teachers (name,subject,username,password,email) VALUES (?,?,?,?,?)',
#             (request.form['name'],request.form['subject'],request.form['username'],
#              request.form['password'],request.form.get('email','')))
#         db.commit(); flash(f"Teacher '{request.form['name']}' added!", 'success')
#     except: flash('Error: Username already exists.', 'error')
#     return redirect('/admin/dashboard')

# @app.route('/admin/delete_teacher/<int:tid>', methods=['POST'])
# def delete_teacher(tid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM homework WHERE teacher_id=?', (tid,))
#     db.execute('DELETE FROM teacher_assignments WHERE teacher_id=?', (tid,))
#     db.execute('DELETE FROM teachers WHERE id=?', (tid,))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/teacher_edit/<int:tid>')
# def admin_teacher_edit(tid):
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     teacher = db.execute('SELECT * FROM teachers WHERE id=?', (tid,)).fetchone()
#     return render_template('admin_teacher_edit.html', teacher=teacher)

# @app.route('/admin/update_teacher_info', methods=['POST'])
# def update_teacher_info():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('UPDATE teachers SET phone=?,qualification=?,experience=?,bio=?,joining_date=? WHERE id=?',
#         (d.get('phone',''),d.get('qualification',''),d.get('experience',''),
#          d.get('bio',''),d.get('joining_date',''),d['id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/upload_teacher_photo/<int:tid>', methods=['POST'])
# def upload_teacher_photo(tid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
#     file = request.files['photo']
#     ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#     if ext not in {'png','jpg','jpeg','gif','webp'}: return jsonify({'error':'Invalid file type'}), 400
#     fname = f"teacher_{tid}_{uuid.uuid4().hex[:8]}.{ext}"
#     path  = os.path.join(app.root_path, 'static', 'uploads', 'teachers', fname)
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     file.save(path)
#     db = get_db()
#     db.execute('UPDATE teachers SET photo=? WHERE id=?', (fname, tid))
#     db.commit(); return jsonify({'success':True, 'filename':fname})

# # ── ADMIN NOTICES ──────────────────────────────────────────────────────────────
# @app.route('/admin/add_notice', methods=['POST'])
# def add_notice():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     db.execute('INSERT INTO notices (title,content,category) VALUES (?,?,?)',
#         (request.form['title'],request.form['content'],request.form['category']))
#     db.commit(); flash('Notice posted!', 'success'); return redirect('/admin/dashboard')

# @app.route('/admin/edit_notice', methods=['POST'])
# def edit_notice():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     db.execute('UPDATE notices SET title=?,content=?,category=? WHERE id=?',
#         (request.form['title'],request.form['content'],request.form['category'],request.form['notice_id']))
#     db.commit(); flash('Notice updated!', 'success'); return redirect('/admin/dashboard')

# @app.route('/admin/delete_notice/<int:nid>', methods=['POST'])
# def delete_notice(nid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM notices WHERE id=?', (nid,)); db.commit()
#     return jsonify({'success':True})

# # ── ADMIN ADMISSIONS ───────────────────────────────────────────────────────────
# @app.route('/admin/update_admission_status', methods=['POST'])
# def update_admission_status():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('UPDATE admissions SET status=? WHERE id=?', (d['status'],d['id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/delete_admission/<int:aid>', methods=['POST'])
# def delete_admission(aid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM admissions WHERE id=?', (aid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/delete_message/<int:mid>', methods=['POST'])
# def delete_message(mid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM contact_messages WHERE id=?', (mid,)); db.commit()
#     return jsonify({'success':True})

# # ── ADMIN TEACHER ASSIGNMENTS ──────────────────────────────────────────────────
# @app.route('/admin/teacher_assignments')
# def teacher_assignments_page():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     return render_template('teacher_assignments.html', teachers=teachers)

# @app.route('/admin/assign_teacher', methods=['POST'])
# def assign_teacher():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     try:
#         db.execute('INSERT OR REPLACE INTO teacher_assignments (teacher_id,class_name,subject) VALUES (?,?,?)',
#             (d['teacher_id'],d['class_name'],d['subject']))
#         db.commit(); return jsonify({'success':True})
#     except Exception as e: return jsonify({'error':str(e)}), 500

# @app.route('/admin/remove_assignment', methods=['POST'])
# def remove_assignment():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('DELETE FROM teacher_assignments WHERE id=?', (d['id'],))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/get_assignments')
# def get_assignments():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     rows = db.execute('''SELECT ta.id, ta.class_name, ta.subject, t.name as teacher_name, t.id as teacher_id
#         FROM teacher_assignments ta JOIN teachers t ON ta.teacher_id=t.id ORDER BY ta.class_name, ta.subject''').fetchall()
#     return jsonify([dict(r) for r in rows])

# # ── ADMIN GALLERY ──────────────────────────────────────────────────────────────
# @app.route('/admin/gallery')
# def admin_gallery():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     photos = db.execute('SELECT * FROM gallery_photos ORDER BY uploaded_at DESC').fetchall()
#     return render_template('admin_gallery.html', photos=photos)

# @app.route('/admin/upload_gallery_photo', methods=['POST'])
# def upload_gallery_photo():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
#     file     = request.files['photo']
#     title    = request.form.get('title','Photo')
#     category = request.form.get('category','General')
#     desc     = request.form.get('description','')
#     ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#     if ext not in {'png','jpg','jpeg','gif','webp'}: return jsonify({'error':'Invalid file type'}), 400
#     fname = f"gallery_{uuid.uuid4().hex[:10]}.{ext}"
#     path  = os.path.join(app.root_path, 'static', 'uploads', 'gallery', fname)
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     file.save(path)
#     db = get_db()
#     db.execute('INSERT INTO gallery_photos (title,category,filename,description) VALUES (?,?,?,?)',
#         (title,category,fname,desc))
#     db.commit(); return jsonify({'success':True, 'filename':fname})

# @app.route('/admin/delete_gallery_photo/<int:pid>', methods=['POST'])
# def delete_gallery_photo(pid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     p = db.execute('SELECT filename FROM gallery_photos WHERE id=?', (pid,)).fetchone()
#     if p:
#         path = os.path.join(app.root_path,'static','uploads','gallery',p['filename'])
#         if os.path.exists(path): os.remove(path)
#         db.execute('DELETE FROM gallery_photos WHERE id=?', (pid,)); db.commit()
#     return jsonify({'success':True})

# # ── ADMIN FEES ─────────────────────────────────────────────────────────────────
# @app.route('/admin/fees')
# def admin_fees():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','Class 5')
#     sel_month = request.args.get('month','')
#     sel_year  = request.args.get('year','2024-25')
#     fee_struct = db.execute('SELECT * FROM fee_structure WHERE class_name=?', (sel_class,)).fetchone()
#     q = 'SELECT f.*, s.name as student_name, s.roll_number FROM fees f JOIN students s ON f.student_id=s.id WHERE f.class_name=?'
#     p = [sel_class]
#     if sel_month: q += ' AND f.fee_month=?'; p.append(sel_month)
#     q += ' ORDER BY f.fee_month, s.roll_number'
#     fees = db.execute(q, p).fetchall()
#     total_due  = sum(f['total_fee'] for f in fees)
#     total_paid = sum(f['paid_amount'] for f in fees)
#     total_rem  = sum(f['remaining'] for f in fees)
#     months = db.execute('SELECT DISTINCT fee_month FROM fees WHERE class_name=? ORDER BY fee_month', (sel_class,)).fetchall()
#     students_summary = db.execute('''
#         SELECT s.id, s.name, s.roll_number,
#                COUNT(f.id) as total_months,
#                SUM(CASE WHEN f.status="Paid" THEN 1 ELSE 0 END) as paid_months,
#                SUM(f.total_fee) as total_due, SUM(f.paid_amount) as total_paid,
#                SUM(f.remaining) as total_remaining
#         FROM students s LEFT JOIN fees f ON s.id=f.student_id
#         WHERE s.class_name=? GROUP BY s.id ORDER BY s.roll_number
#     ''', (sel_class,)).fetchall()
#     return render_template('admin_fees.html',
#         classes=classes, sel_class=sel_class, sel_month=sel_month, sel_year=sel_year,
#         fee_struct=fee_struct, fees=fees, months=months,
#         total_due=total_due, total_paid=total_paid, total_rem=total_rem,
#         students_summary=students_summary)

# @app.route('/admin/fees/update', methods=['POST'])
# def update_fee():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     total = float(d.get('total_fee',0))
#     paid  = float(d.get('paid_amount',0))
#     rem   = max(0, total - paid)
#     status = 'Paid' if rem<=0 else ('Partial' if paid>0 else 'Pending')
#     db.execute('''INSERT INTO fees (student_id,class_name,fee_month,fee_year,tuition_fee,other_fee,total_fee,paid_amount,remaining,status,paid_date,remarks)
#         VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
#         ON CONFLICT(student_id,fee_month) DO UPDATE SET
#         total_fee=excluded.total_fee, paid_amount=excluded.paid_amount,
#         remaining=excluded.remaining, status=excluded.status,
#         paid_date=excluded.paid_date, remarks=excluded.remarks''',
#         (d['student_id'],d['class_name'],d['fee_month'],d.get('fee_year','2024-25'),
#          d.get('tuition_fee',0),d.get('other_fee',0),total,paid,rem,status,
#          d.get('paid_date') or None,d.get('remarks','')))
#     db.commit(); return jsonify({'success':True,'remaining':rem,'status':status})

# @app.route('/admin/fees/generate_monthly', methods=['POST'])
# def generate_monthly_fees():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     struct = db.execute('SELECT * FROM fee_structure WHERE class_name=?', (d['class_name'],)).fetchone()
#     if not struct: return jsonify({'error':'Fee structure not set'}), 400
#     total    = struct['tuition_fee']+struct['activity_fee']+struct['computer_fee']+struct['other_fee']
#     students = db.execute('SELECT id FROM students WHERE class_name=?', (d['class_name'],)).fetchall()
#     count = 0
#     for s in students:
#         try:
#             db.execute('''INSERT OR IGNORE INTO fees
#                 (student_id,class_name,fee_month,fee_year,tuition_fee,other_fee,total_fee,paid_amount,remaining,status)
#                 VALUES (?,?,?,?,?,?,?,0,?,?)''',
#                 (s['id'],d['class_name'],d['fee_month'],d.get('fee_year','2024-25'),
#                  struct['tuition_fee'],struct['activity_fee']+struct['computer_fee']+struct['other_fee'],
#                  total,total,'Pending'))
#             count += 1
#         except: pass
#     db.commit(); return jsonify({'success':True,'generated':count})

# @app.route('/admin/fees/update_structure', methods=['POST'])
# def update_fee_structure():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('''INSERT INTO fee_structure (class_name,tuition_fee,activity_fee,computer_fee,other_fee)
#         VALUES (?,?,?,?,?) ON CONFLICT(class_name) DO UPDATE SET
#         tuition_fee=excluded.tuition_fee, activity_fee=excluded.activity_fee,
#         computer_fee=excluded.computer_fee, other_fee=excluded.other_fee''',
#         (d['class_name'],d['tuition_fee'],d['activity_fee'],d['computer_fee'],d['other_fee']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/fees/student_detail/<int:sid>')
# def admin_student_fee_detail(sid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     fees = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month', (sid,)).fetchall()
#     return jsonify({'fees':[dict(f) for f in fees]})


# # ═══════════════════════════════════════════════
# # FEATURE 1: RESULT / REPORT CARD PDF DOWNLOAD
# # ═══════════════════════════════════════════════

# @app.route('/student/report_card')
# def student_report_card():
#     if session.get('role') != 'student': return redirect('/student/login')
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib import colors
#     from reportlab.lib.units import cm
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
#     from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#     from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
#     from io import BytesIO
#     from flask import make_response

#     db  = get_db()
#     sid = session['student_id']
#     student  = db.execute('SELECT * FROM students WHERE id=?', (sid,)).fetchone()
#     marks    = db.execute('SELECT * FROM marks WHERE student_id=? ORDER BY subject', (sid,)).fetchall()
#     attendance = db.execute('SELECT * FROM attendance WHERE student_id=?', (sid,)).fetchall()
#     total   = len(attendance)
#     present = sum(1 for a in attendance if a['status'] == 'Present')
#     att_pct = round((present/total*100) if total else 0, 1)

#     buffer = BytesIO()
#     doc    = SimpleDocTemplate(buffer, pagesize=A4,
#                                rightMargin=1.5*cm, leftMargin=1.5*cm,
#                                topMargin=1.5*cm, bottomMargin=1.5*cm)
#     styles = getSampleStyleSheet()
#     story  = []

#     NAVY  = colors.HexColor('#0d1b3e')
#     GOLD  = colors.HexColor('#c9a84c')
#     CREAM = colors.HexColor('#fdf8f0')
#     GREEN = colors.HexColor('#2e7d32')
#     RED   = colors.HexColor('#c62828')
#     ORANGE= colors.HexColor('#e65100')

#     # ── HEADER ──────────────────────────────────────────
#     header_data = [[
#         Paragraph('<font color="#0d1b3e"><b>🏫 BRIGHTMIND SCHOOL</b></font>', ParagraphStyle('h', fontSize=18, fontName='Helvetica-Bold', alignment=TA_CENTER)),
#     ]]
#     header_tbl = Table(header_data, colWidths=[17*cm])
#     header_tbl.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (-1,-1), CREAM),
#         ('TOPPADDING', (0,0), (-1,-1), 14),
#         ('BOTTOMPADDING', (0,0), (-1,-1), 4),
#         ('ROUNDEDCORNERS', [8]),
#     ]))
#     story.append(header_tbl)

#     sub_styles = ParagraphStyle('sub', fontSize=9, fontName='Helvetica', alignment=TA_CENTER, textColor=colors.HexColor('#555'))
#     story.append(Paragraph('Est. 1995 · CBSE Affiliated · Delhi – 110001', sub_styles))
#     story.append(Paragraph('Phone: +91 11 1234 5678 | Email: info@brightmindschool.edu.in', sub_styles))
#     story.append(Spacer(1, 10))

#     title_style = ParagraphStyle('title', fontSize=14, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=NAVY, spaceBefore=4, spaceAfter=4)
#     story.append(Paragraph('STUDENT PROGRESS REPORT CARD', title_style))
#     story.append(Paragraph('Academic Year: 2024–25', ParagraphStyle('ay', fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#777'))))
#     story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=10))

#     # ── STUDENT INFO ─────────────────────────────────────
#     info_data = [
#         ['Student Name:', student['name'],    'Roll Number:', student['roll_number']],
#         ['Class:',        student['class_name'], "Parent's Name:", student['parent_name'] or '—'],
#         ['Contact:',      student['contact'] or '—', 'Attendance:', f"{att_pct}% ({present}/{total} days)"],
#     ]
#     info_tbl = Table(info_data, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
#     info_tbl.setStyle(TableStyle([
#         ('FONTNAME',  (0,0), (0,-1), 'Helvetica-Bold'),
#         ('FONTNAME',  (2,0), (2,-1), 'Helvetica-Bold'),
#         ('FONTSIZE',  (0,0), (-1,-1), 9),
#         ('TEXTCOLOR', (0,0), (0,-1), NAVY),
#         ('TEXTCOLOR', (2,0), (2,-1), NAVY),
#         ('BACKGROUND',(0,0), (-1,-1), CREAM),
#         ('ROWBACKGROUNDS', (0,0), (-1,-1), [CREAM, colors.white]),
#         ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#ddd')),
#         ('TOPPADDING', (0,0), (-1,-1), 6),
#         ('BOTTOMPADDING', (0,0), (-1,-1), 6),
#         ('LEFTPADDING', (0,0), (-1,-1), 8),
#     ]))
#     story.append(info_tbl)
#     story.append(Spacer(1, 14))

#     # ── MARKS TABLE ──────────────────────────────────────
#     story.append(Paragraph('Academic Performance', ParagraphStyle('sec', fontSize=11, fontName='Helvetica-Bold', textColor=NAVY, spaceBefore=4, spaceAfter=6)))

#     if marks:
#         marks_header = [['S.No.', 'Subject', 'Exam Type', 'Marks Obtained', 'Max Marks', 'Percentage', 'Grade', 'Remarks']]
#         marks_rows   = []
#         total_marks = total_max = 0
#         for i, m in enumerate(marks, 1):
#             pct   = round(m['marks']/m['max_marks']*100, 1) if m['max_marks'] else 0
#             grade = 'A1' if pct>=90 else 'A2' if pct>=80 else 'B1' if pct>=70 else 'B2' if pct>=60 else 'C1' if pct>=50 else 'D'
#             rmk   = 'Excellent' if pct>=90 else 'Very Good' if pct>=80 else 'Good' if pct>=70 else 'Average' if pct>=50 else 'Needs Improvement'
#             total_marks += m['marks']; total_max += m['max_marks']
#             marks_rows.append([str(i), m['subject'], m['exam_type'],
#                                str(int(m['marks'])), str(int(m['max_marks'])),
#                                f"{pct}%", grade, rmk])

#         overall_pct = round(total_marks/total_max*100, 1) if total_max else 0
#         overall_grade = 'A1' if overall_pct>=90 else 'A2' if overall_pct>=80 else 'B1' if overall_pct>=70 else 'B2' if overall_pct>=60 else 'C1' if overall_pct>=50 else 'D'
#         marks_rows.append(['', 'TOTAL / OVERALL', '', f"{int(total_marks)}", f"{int(total_max)}", f"{overall_pct}%", overall_grade, ''])

#         all_rows = marks_header + marks_rows
#         marks_tbl = Table(all_rows, colWidths=[1*cm, 4*cm, 2.5*cm, 2.5*cm, 2*cm, 2*cm, 1.5*cm, 2.5*cm])
#         style = TableStyle([
#             ('BACKGROUND',  (0,0), (-1,0), NAVY),
#             ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
#             ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
#             ('FONTSIZE',    (0,0), (-1,-1), 8),
#             ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
#             ('ALIGN',       (1,0), (1,-1), 'LEFT'),
#             ('ALIGN',       (7,0), (7,-1), 'LEFT'),
#             ('GRID',        (0,0), (-1,-1), 0.3, colors.HexColor('#ccc')),
#             ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, CREAM]),
#             ('TOPPADDING',  (0,0), (-1,-1), 5),
#             ('BOTTOMPADDING',(0,0), (-1,-1), 5),
#             ('LEFTPADDING', (0,0), (-1,-1), 4),
#             ('FONTNAME',    (0,-1), (-1,-1), 'Helvetica-Bold'),
#             ('BACKGROUND',  (0,-1), (-1,-1), colors.HexColor('#e8f5e9')),
#             ('TEXTCOLOR',   (0,-1), (-1,-1), GREEN),
#         ])
#         marks_tbl.setStyle(style)
#         story.append(marks_tbl)
#     else:
#         story.append(Paragraph('No marks recorded yet.', styles['Normal']))

#     story.append(Spacer(1, 16))

#     # ── SUMMARY BOX ──────────────────────────────────────
#     if marks:
#         status = 'PASS ✓' if overall_pct >= 33 else 'FAIL ✗'
#         status_color = GREEN if overall_pct >= 33 else RED
#         summary_data = [
#             [Paragraph(f'<b>Overall Percentage:</b> {overall_pct}%', ParagraphStyle('s', fontSize=10)),
#              Paragraph(f'<b>Overall Grade:</b> {overall_grade}', ParagraphStyle('s', fontSize=10)),
#              Paragraph(f'<b>Result:</b> <font color="{"#2e7d32" if overall_pct>=33 else "#c62828"}">{status}</font>', ParagraphStyle('s', fontSize=10)),
#              Paragraph(f'<b>Attendance:</b> {att_pct}%', ParagraphStyle('s', fontSize=10))],
#         ]
#         sum_tbl = Table(summary_data, colWidths=[4.25*cm]*4)
#         sum_tbl.setStyle(TableStyle([
#             ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e3f2fd')),
#             ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#90caf9')),
#             ('TOPPADDING', (0,0), (-1,-1), 8),
#             ('BOTTOMPADDING', (0,0), (-1,-1), 8),
#             ('LEFTPADDING', (0,0), (-1,-1), 8),
#         ]))
#         story.append(sum_tbl)

#     story.append(Spacer(1, 20))

#     # ── GRADE SCALE ──────────────────────────────────────
#     grade_data = [['Grade Scale:','A1 (90-100)','A2 (80-89)','B1 (70-79)','B2 (60-69)','C1 (50-59)','D (Below 50)']]
#     grade_tbl  = Table(grade_data, colWidths=[2.5*cm]+[2.14*cm]*6)
#     grade_tbl.setStyle(TableStyle([
#         ('FONTNAME',  (0,0), (0,0), 'Helvetica-Bold'),
#         ('FONTSIZE',  (0,0), (-1,-1), 7.5),
#         ('BACKGROUND',(0,0), (-1,-1), CREAM),
#         ('GRID',      (0,0), (-1,-1), 0.3, colors.HexColor('#ddd')),
#         ('ALIGN',     (0,0), (-1,-1), 'CENTER'),
#         ('TOPPADDING',(0,0), (-1,-1), 4),
#         ('BOTTOMPADDING',(0,0),(-1,-1), 4),
#     ]))
#     story.append(grade_tbl)
#     story.append(Spacer(1, 20))

#     # ── SIGNATURES ───────────────────────────────────────
#     sig_data = [['Class Teacher', 'Examination Controller', 'Principal'],
#                 ['________________', '________________', '________________'],
#                 ['Date: ___________', 'Date: ___________', 'Date: ___________']]
#     sig_tbl  = Table(sig_data, colWidths=[5.67*cm]*3)
#     sig_tbl.setStyle(TableStyle([
#         ('ALIGN',   (0,0), (-1,-1), 'CENTER'),
#         ('FONTSIZE',(0,0), (-1,-1), 9),
#         ('FONTNAME',(0,0), (-1,0), 'Helvetica-Bold'),
#         ('TEXTCOLOR',(0,0),(-1,0), NAVY),
#         ('TOPPADDING',(0,0),(-1,-1), 4),
#     ]))
#     story.append(sig_tbl)

#     story.append(Spacer(1, 12))
#     story.append(HRFlowable(width="100%", thickness=1, color=GOLD))
#     footer_style = ParagraphStyle('ft', fontSize=7.5, alignment=TA_CENTER, textColor=colors.HexColor('#888'), spaceBefore=4)
#     story.append(Paragraph('This is a computer-generated report card. BrightMind School, Delhi – 110001', footer_style))

#     doc.build(story)
#     pdf = buffer.getvalue()
#     buffer.close()

#     response = make_response(pdf)
#     response.headers['Content-Type']        = 'application/pdf'
#     response.headers['Content-Disposition'] = f'attachment; filename=ReportCard_{student["roll_number"]}.pdf'
#     return response

# # ═══════════════════════════════════════════════
# # FEATURE 2: TIMETABLE MANAGEMENT
# # ═══════════════════════════════════════════════

# @app.route('/timetable')
# def timetable():
#     db = get_db()
#     classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name', session.get('student_class','Class 5'))
#     days      = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
#     periods   = list(range(1,7))

#     rows = db.execute(
#         'SELECT * FROM timetable WHERE class_name=? ORDER BY day, period', (sel_class,)
#     ).fetchall()

#     # Build dict: day -> {period -> row}
#     tt = {day: {} for day in days}
#     for r in rows:
#         tt[r['day']][r['period']] = r

#     period_times = {1:'8:00-8:45',2:'8:45-9:30',3:'9:30-10:15',
#                     4:'10:30-11:15',5:'11:15-12:00',6:'12:00-12:45'}

#     return render_template('timetable.html',
#         classes=classes, sel_class=sel_class, days=days,
#         periods=periods, tt=tt, period_times=period_times)

# @app.route('/admin/timetable')
# def admin_timetable():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','Class 5')
#     teachers  = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     days      = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
#     periods   = list(range(1,7))
#     rows = db.execute('SELECT * FROM timetable WHERE class_name=? ORDER BY day,period',(sel_class,)).fetchall()
#     tt   = {day:{} for day in days}
#     for r in rows: tt[r['day']][r['period']] = r
#     period_times = {1:'8:00-8:45',2:'8:45-9:30',3:'9:30-10:15',
#                     4:'10:30-11:15',5:'11:15-12:00',6:'12:00-12:45'}
#     return render_template('admin_timetable.html',
#         classes=classes, sel_class=sel_class, teachers=teachers,
#         days=days, periods=periods, tt=tt, period_times=period_times)

# @app.route('/admin/timetable/save', methods=['POST'])
# def save_timetable():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d  = request.json
#     db = get_db()
#     try:
#         db.execute('''INSERT INTO timetable (class_name,day,period,subject,teacher_id,start_time,end_time)
#             VALUES (?,?,?,?,?,?,?)
#             ON CONFLICT(class_name,day,period) DO UPDATE SET
#             subject=excluded.subject, teacher_id=excluded.teacher_id''',
#             (d['class_name'],d['day'],d['period'],d['subject'],
#              d.get('teacher_id') or None, d.get('start_time',''), d.get('end_time','')))
#         db.commit()
#         return jsonify({'success':True})
#     except Exception as e:
#         return jsonify({'error':str(e)}), 500

# @app.route('/admin/timetable/delete', methods=['POST'])
# def delete_timetable_entry():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d  = request.json
#     db = get_db()
#     db.execute('DELETE FROM timetable WHERE class_name=? AND day=? AND period=?',
#                (d['class_name'],d['day'],d['period']))
#     db.commit()
#     return jsonify({'success':True})

# # ═══════════════════════════════════════════════
# # FEATURE 3: ADMIN ANALYTICS DASHBOARD
# # ═══════════════════════════════════════════════

# @app.route('/admin/analytics')
# def admin_analytics():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()

#     # Fees analytics
#     fee_stats = db.execute('''
#         SELECT class_name,
#                SUM(total_fee) as total_due,
#                SUM(paid_amount) as total_paid,
#                SUM(remaining) as total_remaining,
#                COUNT(CASE WHEN status="Paid" THEN 1 END) as paid_count,
#                COUNT(CASE WHEN status="Pending" THEN 1 END) as pending_count,
#                COUNT(CASE WHEN status="Overdue" THEN 1 END) as overdue_count,
#                COUNT(*) as total_count
#         FROM fees GROUP BY class_name ORDER BY class_name
#     ''').fetchall()

#     # Monthly fee collection
#     monthly = db.execute('''
#         SELECT fee_month, SUM(paid_amount) as collected, SUM(remaining) as pending
#         FROM fees GROUP BY fee_month ORDER BY fee_month
#     ''').fetchall()

#     # Attendance stats per class
#     att_stats = db.execute('''
#         SELECT s.class_name,
#                COUNT(a.id) as total_records,
#                SUM(CASE WHEN a.status="Present" THEN 1 ELSE 0 END) as present_count
#         FROM students s LEFT JOIN attendance a ON s.id=a.student_id
#         GROUP BY s.class_name ORDER BY s.class_name
#     ''').fetchall()

#     # Top students by marks
#     top_students = db.execute('''
#         SELECT s.name, s.class_name, s.roll_number,
#                AVG(m.marks/m.max_marks*100) as avg_pct,
#                COUNT(m.id) as subjects
#         FROM students s JOIN marks m ON s.id=m.student_id
#         GROUP BY s.id HAVING subjects>=2
#         ORDER BY avg_pct DESC LIMIT 10
#     ''').fetchall()

#     # Overall summary
#     summary = {
#         'total_students': db.execute('SELECT COUNT(*) FROM students').fetchone()[0],
#         'total_teachers': db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
#         'total_fee_due':  db.execute('SELECT SUM(total_fee) FROM fees').fetchone()[0] or 0,
#         'total_fee_paid': db.execute('SELECT SUM(paid_amount) FROM fees').fetchone()[0] or 0,
#         'pending_admissions': db.execute("SELECT COUNT(*) FROM admissions WHERE status='Pending'").fetchone()[0],
#         'total_notices': db.execute('SELECT COUNT(*) FROM notices').fetchone()[0],
#     }
#     summary['collection_pct'] = round(summary['total_fee_paid']/summary['total_fee_due']*100 if summary['total_fee_due'] else 0, 1)

#     return render_template('admin_analytics.html',
#         fee_stats=fee_stats, monthly=monthly, att_stats=att_stats,
#         top_students=top_students, summary=summary)

# # ═══════════════════════════════════════════════
# # FEATURE 4: EXAM DATE SHEET
# # ═══════════════════════════════════════════════

# @app.route('/exam_schedule')
# def exam_schedule():
#     db = get_db()
#     exams = db.execute('SELECT * FROM exam_schedule ORDER BY exam_date, class_name').fetchall()
#     classes = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','All')
#     if sel_class != 'All':
#         exams = [e for e in exams if e['class_name']==sel_class]
#     return render_template('exam_schedule.html', exams=exams, classes=classes, sel_class=sel_class)

# @app.route('/admin/exam_schedule')
# def admin_exam_schedule():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     exams = db.execute('SELECT * FROM exam_schedule ORDER BY exam_date, class_name').fetchall()
#     classes = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     return render_template('admin_exam_schedule.html', exams=exams, classes=classes)

# @app.route('/admin/exam_schedule/add', methods=['POST'])
# def add_exam():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     db.execute('INSERT INTO exam_schedule (class_name,subject,exam_date,day,start_time,end_time,exam_type,venue) VALUES (?,?,?,?,?,?,?,?)',
#         (request.form['class_name'], request.form['subject'], request.form['exam_date'],
#          request.form.get('day',''), request.form.get('start_time','10:00'),
#          request.form.get('end_time','13:00'), request.form['exam_type'],
#          request.form.get('venue','Main Hall')))
#     db.commit()
#     flash('Exam added!', 'success')
#     return redirect('/admin/exam_schedule')

# @app.route('/admin/exam_schedule/delete/<int:eid>', methods=['POST'])
# def delete_exam(eid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM exam_schedule WHERE id=?', (eid,))
#     db.commit()
#     return jsonify({'success':True})

# # ═══════════════════════════════════════════════
# # FEATURE 5: PARENT PORTAL
# # ═══════════════════════════════════════════════

# @app.route('/parent/login', methods=['GET','POST'])
# def parent_login():
#     if request.method == 'POST':
#         db = get_db()
#         # Parent logs in with student's roll number + parent contact as password
#         student = db.execute('SELECT * FROM students WHERE roll_number=? AND contact=?',
#             (request.form['roll_number'], request.form['contact'])).fetchone()
#         if student:
#             session.update({'parent_student_id':student['id'],
#                            'parent_student_name':student['name'],
#                            'parent_student_class':student['class_name'],
#                            'parent_name':student['parent_name'],
#                            'role':'parent'})
#             return redirect('/parent/dashboard')
#         flash('Invalid Roll Number or Contact Number.', 'error')
#     return render_template('parent_login.html')

# @app.route('/parent/dashboard')
# def parent_dashboard():
#     if session.get('role') != 'parent': return redirect('/parent/login')
#     db  = get_db()
#     sid = session['parent_student_id']
#     student    = db.execute('SELECT * FROM students WHERE id=?',(sid,)).fetchone()
#     marks      = db.execute('SELECT * FROM marks WHERE student_id=? ORDER BY subject',(sid,)).fetchall()
#     attendance = db.execute('SELECT * FROM attendance WHERE student_id=? ORDER BY date DESC LIMIT 30',(sid,)).fetchall()
#     fees       = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month',(sid,)).fetchall()
#     homework   = db.execute('SELECT * FROM homework WHERE class_name=? ORDER BY due_date DESC LIMIT 10',(session['parent_student_class'],)).fetchall()
#     notices    = db.execute('SELECT * FROM notices ORDER BY created_at DESC LIMIT 5').fetchall()
#     total   = len(attendance)
#     present = sum(1 for a in attendance if a['status']=='Present')
#     pct     = round((present/total*100) if total else 0,1)
#     total_due  = sum(f['total_fee'] for f in fees)
#     total_paid = sum(f['paid_amount'] for f in fees)
#     return render_template('parent_dashboard.html',
#         student=student, marks=marks, attendance=attendance, fees=fees,
#         homework=homework, notices=notices,
#         attend_pct=pct, total_days=total, present_days=present,
#         total_due=total_due, total_paid=total_paid,
#         total_remaining=total_due-total_paid)

# @app.route('/parent/logout')
# def parent_logout():
#     session.clear(); return redirect('/')

# # ═══════════════════════════════════════════════
# # FEATURE 6: LIVE CLASS / VIDEO LINK
# # ═══════════════════════════════════════════════

# @app.route('/live_classes')
# def live_classes():
#     db = get_db()
#     sel_class = request.args.get('class_name', session.get('student_class', 'All'))
#     if sel_class and sel_class != 'All':
#         classes_data = db.execute(
#             'SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id WHERE lc.class_name=? ORDER BY lc.scheduled_at DESC',
#             (sel_class,)).fetchall()
#     else:
#         classes_data = db.execute(
#             'SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id ORDER BY lc.scheduled_at DESC'
#         ).fetchall()
#     all_classes = ['All', 'UKG'] + [f'Class {i}' for i in range(1, 11)]
#     return render_template('live_classes.html', classes_data=classes_data, all_classes=all_classes, sel_class=sel_class)

# @app.route('/teacher/live_classes')
# def teacher_live_classes():
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     my_classes = db.execute(
#         'SELECT * FROM live_classes WHERE teacher_id=? ORDER BY scheduled_at DESC',
#         (session['teacher_id'],)).fetchall()
#     all_classes = ['UKG'] + [f'Class {i}' for i in range(1, 11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit','Drawing','Physical Education']
#     return render_template('teacher_live_classes.html', my_classes=my_classes, all_classes=all_classes, subjects=subjects)

# @app.route('/teacher/add_live_class', methods=['POST'])
# def add_live_class():
#     if session.get('role') != 'teacher': return jsonify({'error': 'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     db.execute(
#         'INSERT INTO live_classes (teacher_id,class_name,subject,title,meet_link,platform,scheduled_at,duration,status,description) VALUES (?,?,?,?,?,?,?,?,?,?)',
#         (session['teacher_id'], d['class_name'], d['subject'], d['title'],
#          d['meet_link'], d['platform'], d['scheduled_at'], d.get('duration', 60),
#          'Upcoming', d.get('description', '')))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/teacher/update_live_class_status', methods=['POST'])
# def update_live_class_status():
#     if session.get('role') != 'teacher': return jsonify({'error': 'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     db.execute('UPDATE live_classes SET status=? WHERE id=? AND teacher_id=?',
#                (d['status'], d['id'], session['teacher_id']))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/teacher/delete_live_class/<int:lcid>', methods=['POST'])
# def delete_live_class(lcid):
#     if session.get('role') != 'teacher': return jsonify({'error': 'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM live_classes WHERE id=? AND teacher_id=?', (lcid, session['teacher_id']))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/api/live_classes')
# def api_live_classes():
#     db = get_db()
#     sel_class = request.args.get('class_name', '')
#     if sel_class:
#         rows = db.execute(
#             '''SELECT lc.*, t.name as teacher_name FROM live_classes lc
#                JOIN teachers t ON lc.teacher_id=t.id
#                WHERE lc.class_name=? AND lc.status != "Completed"
#                ORDER BY lc.status DESC, lc.scheduled_at ASC LIMIT 5''',
#             (sel_class,)).fetchall()
#     else:
#         rows = db.execute(
#             '''SELECT lc.*, t.name as teacher_name FROM live_classes lc
#                JOIN teachers t ON lc.teacher_id=t.id
#                WHERE lc.status != "Completed"
#                ORDER BY lc.status DESC, lc.scheduled_at ASC LIMIT 10''').fetchall()
#     return jsonify([dict(r) for r in rows])

# # ═══════════════════════════════════════════════
# # FEATURE: STUDENT ID CARD GENERATOR (PDF)
# # ═══════════════════════════════════════════════

# @app.route('/admin/id_cards')
# def admin_id_cards():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes  = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','All')
#     if sel_class == 'All':
#         students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id ORDER BY s.class_name, s.roll_number').fetchall()
#     else:
#         students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id WHERE s.class_name=? ORDER BY s.roll_number', (sel_class,)).fetchall()
#     return render_template('admin_id_cards.html', students=students, classes=classes, sel_class=sel_class)

# @app.route('/admin/upload_student_photo/<int:sid>', methods=['POST'])
# def upload_student_photo(sid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
#     file = request.files['photo']
#     ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#     if ext not in {'png','jpg','jpeg','webp'}: return jsonify({'error':'Invalid type'}), 400
#     fname = f"student_{sid}.{ext}"
#     path  = os.path.join(app.root_path,'static','uploads','students',fname)
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     file.save(path)
#     db = get_db()
#     db.execute('INSERT INTO student_photos (student_id,filename) VALUES (?,?) ON CONFLICT(student_id) DO UPDATE SET filename=excluded.filename', (sid,fname))
#     db.commit()
#     return jsonify({'success':True,'filename':fname})

# @app.route('/admin/generate_id_card/<int:sid>')
# def generate_id_card(sid):
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib import colors
#     from reportlab.lib.units import cm
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
#     from reportlab.lib.styles import ParagraphStyle
#     from reportlab.lib.enums import TA_CENTER, TA_LEFT
#     from io import BytesIO
#     from flask import make_response

#     db = get_db()
#     cls_filter = request.args.get('class_name', '')
#     if sid == 0:
#         if cls_filter:
#             students = db.execute('SELECT * FROM students WHERE class_name=? ORDER BY roll_number', (cls_filter,)).fetchall()
#         else:
#             students = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
#     else:
#         students = db.execute('SELECT * FROM students WHERE id=?', (sid,)).fetchall()

#     if not students:
#         flash('No students found.', 'error')
#         return redirect('/admin/id_cards')

#     NAVY  = colors.HexColor('#0d1b3e')
#     GOLD  = colors.HexColor('#c9a84c')
#     CREAM = colors.HexColor('#fdf8f0')
#     WHITE = colors.white

#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4,
#                             rightMargin=1*cm, leftMargin=1*cm,
#                             topMargin=1.5*cm, bottomMargin=1*cm)
#     story = []

#     title_style = ParagraphStyle('t', fontSize=12, fontName='Helvetica-Bold',
#                                  alignment=TA_CENTER, textColor=NAVY, spaceAfter=12)
#     story.append(Paragraph('BrightMind School — Student ID Cards 2024-25', title_style))

#     CARD_W = 8.5 * cm
#     CARD_H = 5.5 * cm

#     def make_card(s):
#         initial = s['name'][0].upper() if s['name'] else '?'
#         # Header row
#         hdr = Table([[Paragraph(f'<font color="white" size="7"><b>BRIGHTMIND SCHOOL · CBSE · 2024-25</b></font>',
#                                 ParagraphStyle('h', alignment=TA_CENTER, fontName='Helvetica-Bold'))]],
#                     colWidths=[CARD_W - 0.4*cm], rowHeights=[0.9*cm])
#         hdr.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
#                                   ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))

#         # Photo cell
#         photo = Table([[Paragraph(f'<font size="22" color="#c9a84c"><b>{initial}</b></font>',
#                                    ParagraphStyle('p', alignment=TA_CENTER))]],
#                       colWidths=[1.8*cm], rowHeights=[2.2*cm])
#         photo.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
#                                     ('ALIGN',(0,0),(-1,-1),'CENTER'),
#                                     ('VALIGN',(0,0),(-1,-1),'MIDDLE')]))

#         # Info
#         name_p  = Paragraph(f'<font size="9" color="#0d1b3e"><b>{s["name"]}</b></font>',
#                              ParagraphStyle('n', fontName='Helvetica-Bold'))
#         class_p = Paragraph(f'<font size="8" color="#0d1b3e">Class: <b>{s["class_name"]}</b></font>',
#                              ParagraphStyle('c'))
#         roll_p  = Paragraph(f'<font size="8" color="#0d1b3e">Roll No: <b>{s["roll_number"]}</b></font>',
#                              ParagraphStyle('r'))
#         sess_p  = Paragraph(f'<font size="7.5" color="#666">Session: 2024-25</font>',
#                              ParagraphStyle('s'))
#         info_rows = [[name_p],[class_p],[roll_p],[sess_p]]
#         info = Table(info_rows, colWidths=[CARD_W - 2.4*cm],
#                      rowHeights=[0.55*cm, 0.5*cm, 0.5*cm, 0.5*cm])
#         info.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),2),
#                                    ('BOTTOMPADDING',(0,0),(-1,-1),2),
#                                    ('LEFTPADDING',(0,0),(-1,-1),6)]))

#         body = Table([[photo, info]], colWidths=[1.9*cm, CARD_W - 2.3*cm], rowHeights=[2.4*cm])
#         body.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),
#                                    ('LEFTPADDING',(0,0),(-1,-1),4),
#                                    ('TOPPADDING',(0,0),(-1,-1),8),
#                                    ('BOTTOMPADDING',(0,0),(-1,-1),4)]))

#         footer = Table([[Paragraph('<font size="6.5" color="#888">Ph: +91 11 1234 5678 | Delhi-110001</font>',
#                                     ParagraphStyle('f', alignment=TA_CENTER))]],
#                        colWidths=[CARD_W - 0.4*cm], rowHeights=[0.55*cm])
#         footer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),CREAM),
#                                      ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))

#         card = Table([[hdr],[body],[footer]],
#                      colWidths=[CARD_W],
#                      rowHeights=[0.9*cm, CARD_H - 1.55*cm, 0.65*cm])
#         card.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.5,GOLD),
#                                    ('TOPPADDING',(0,0),(-1,-1),0),
#                                    ('BOTTOMPADDING',(0,0),(-1,-1),0),
#                                    ('LEFTPADDING',(0,0),(-1,-1),0),
#                                    ('RIGHTPADDING',(0,0),(-1,-1),0)]))
#         return card

#     # Layout: 2 cards per row
#     SPACER_W = 0.8*cm
#     pair_w   = [CARD_W + SPACER_W/2, CARD_W + SPACER_W/2]

#     i = 0
#     while i < len(students):
#         row_data = []
#         if i < len(students):     row_data.append(make_card(students[i]))
#         else:                      row_data.append(Paragraph('', ParagraphStyle('e')))
#         if i+1 < len(students):   row_data.append(make_card(students[i+1]))
#         else:                      row_data.append(Paragraph('', ParagraphStyle('e')))

#         row_tbl = Table([row_data], colWidths=pair_w, rowHeights=[CARD_H + 0.4*cm])
#         row_tbl.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
#                                       ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
#                                       ('TOPPADDING',(0,0),(-1,-1),4),
#                                       ('BOTTOMPADDING',(0,0),(-1,-1),4)]))
#         story.append(row_tbl)
#         i += 2

#     doc.build(story)
#     pdf  = buffer.getvalue()
#     buffer.close()

#     name = students[0]['name'] if len(students)==1 else f'{cls_filter or "All"}_Students'
#     resp = make_response(pdf)
#     resp.headers['Content-Type']        = 'application/pdf'
#     resp.headers['Content-Disposition'] = f'attachment; filename=ID_Cards_{name}.pdf'
#     return resp


# @app.route('/admin/generate_all_id_cards')
# def generate_all_id_cards():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib import colors
#     from reportlab.lib.units import cm
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
#     from reportlab.lib.styles import ParagraphStyle
#     from reportlab.lib.enums import TA_CENTER, TA_LEFT
#     from io import BytesIO
#     from flask import make_response

#     db = get_db()
#     cls = request.args.get('class_name','')
#     if cls:
#         students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id WHERE s.class_name=? ORDER BY s.roll_number',(cls,)).fetchall()
#     else:
#         students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id ORDER BY s.class_name, s.roll_number').fetchall()

#     NAVY=colors.HexColor('#0d1b3e'); GOLD=colors.HexColor('#c9a84c'); CREAM=colors.HexColor('#fdf8f0')
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1*cm, rightMargin=1*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
#     story = []; card_w=8.56*cm; card_h=5.4*cm

#     title_s = ParagraphStyle('t',fontSize=14,fontName='Helvetica-Bold',textColor=NAVY,alignment=TA_CENTER,spaceAfter=12)
#     story.append(Paragraph(f'BrightMind School — Student ID Cards {"(" + cls + ")" if cls else "(All Classes)"}', title_s))

#     cards = []
#     for student in students:
#         if student['photo']:
#             photo_path = os.path.join(app.root_path,'static','uploads','students',student['photo'])
#             photo_cell = RLImage(photo_path,width=1.8*cm,height=1.8*cm) if os.path.exists(photo_path) else Paragraph(student['name'][0], ParagraphStyle('i',fontSize=18,fontName='Helvetica-Bold',textColor=GOLD,alignment=TA_CENTER))
#         else:
#             photo_cell = Paragraph(student['name'][0], ParagraphStyle('i',fontSize=18,fontName='Helvetica-Bold',textColor=GOLD,alignment=TA_CENTER))

#         info = Table([
#             [Paragraph(f'<b>{student["name"]}</b>', ParagraphStyle('n',fontSize=7.5,fontName='Helvetica-Bold',textColor=NAVY,leading=10))],
#             [Paragraph(f'Class: <b>{student["class_name"]}</b>', ParagraphStyle('c',fontSize=6.5,leading=9))],
#             [Paragraph(f'Roll: <b>{student["roll_number"]}</b>', ParagraphStyle('r',fontSize=6.5,leading=9))],
#             [Paragraph('Session: 2024-25', ParagraphStyle('s',fontSize=6,textColor=colors.HexColor('#555'),leading=8))],
#         ], colWidths=[card_w-2.2*cm])
#         info.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))

#         header = Table([[Paragraph('<font color="white"><b>BRIGHTMIND SCHOOL</b></font>', ParagraphStyle('h',fontSize=6.5,fontName='Helvetica-Bold',alignment=TA_CENTER))]], colWidths=[card_w])
#         header.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
#         mid = Table([[photo_cell, info]], colWidths=[2*cm, card_w-2*cm])
#         mid.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BACKGROUND',(0,0),(-1,-1),CREAM)]))
#         footer = Table([[Paragraph(f'📞 {student["contact"] or "—"}', ParagraphStyle('f',fontSize=5.5,textColor=colors.white,alignment=TA_LEFT))]], colWidths=[card_w])
#         footer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),GOLD),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),6)]))

#         card = Table([[header],[mid],[footer]], colWidths=[card_w], rowHeights=[0.8*cm,3.8*cm,0.6*cm])
#         card.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.5,NAVY),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
#         cards.append(card)

#     # 2 cards per row
#     for i in range(0, len(cards), 2):
#         row = cards[i:i+2]
#         if len(row) == 1: row.append(Spacer(card_w,card_h))
#         story.append(Table([row], colWidths=[card_w+0.5*cm]*2))
#         story.append(Spacer(1,0.5*cm))

#     doc.build(story)
#     pdf=buffer.getvalue(); buffer.close()
#     resp=make_response(pdf)
#     resp.headers['Content-Type']='application/pdf'
#     resp.headers['Content-Disposition']=f'attachment; filename=IDCards_{cls or "All"}.pdf'
#     return resp

# # ═══════════════════════════════════════════════
# # FEATURE: WHATSAPP NOTIFICATION SYSTEM
# # ═══════════════════════════════════════════════

# @app.route('/admin/notifications')
# def admin_notifications():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     logs      = db.execute('SELECT * FROM notifications ORDER BY sent_at DESC LIMIT 50').fetchall()
#     students  = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id ORDER BY s.class_name').fetchall()
#     classes   = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     pending_fees = db.execute('''SELECT s.name, s.contact, s.class_name, f.fee_month, f.remaining
#         FROM fees f JOIN students s ON f.student_id=s.id
#         WHERE f.status IN ("Pending","Overdue") AND s.contact IS NOT NULL
#         ORDER BY f.status DESC, s.class_name''').fetchall()
#     return render_template('admin_notifications.html', logs=logs, students=students, classes=classes, pending_fees=pending_fees)

# @app.route('/admin/send_notification', methods=['POST'])
# def send_notification():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     recipients = []
#     msg_type = d.get('type','custom')
#     message  = d.get('message','')

#     if d.get('target') == 'all':
#         students = db.execute('SELECT * FROM students WHERE contact IS NOT NULL').fetchall()
#         recipients = [(s['name'], s['contact']) for s in students]
#     elif d.get('target') == 'class':
#         students = db.execute('SELECT * FROM students WHERE class_name=? AND contact IS NOT NULL',(d['class_name'],)).fetchall()
#         recipients = [(s['name'], s['contact']) for s in students]
#     elif d.get('target') == 'fee_pending':
#         rows = db.execute('''SELECT s.name, s.contact, s.class_name, f.fee_month, f.remaining
#             FROM fees f JOIN students s ON f.student_id=s.id
#             WHERE f.status IN ("Pending","Overdue") AND s.contact IS NOT NULL''').fetchall()
#         for r in rows:
#             msg = f"Dear Parent of {r['name']} ({r['class_name']}), Fee of ₹{int(r['remaining'])} for {r['fee_month']} is pending. Please pay at earliest. — BrightMind School"
#             recipients.append((r['name'], r['contact'], msg))
#     elif d.get('student_id'):
#         s = db.execute('SELECT * FROM students WHERE id=?',(d['student_id'],)).fetchone()
#         if s and s['contact']:
#             recipients = [(s['name'], s['contact'])]

#     sent = 0
#     for rec in recipients:
#         name    = rec[0]
#         contact = rec[1]
#         custom_msg = rec[2] if len(rec) > 2 else message.replace('{name}', name)

#         # Generate WhatsApp link (wa.me) — simulated
#         wa_link = f"https://wa.me/91{contact}?text={custom_msg.replace(' ','%20')}"

#         db.execute('INSERT INTO notifications (type,recipient,message,status) VALUES (?,?,?,?)',
#                    (msg_type, f"{name} ({contact})", custom_msg[:200], "Sent (WA Link)"))
#         sent += 1

#     db.commit()
#     return jsonify({'success':True, 'sent':sent})

# # ═══════════════════════════════════════════════
# # FEATURE: ONLINE TEST / QUIZ
# # ═══════════════════════════════════════════════

# @app.route('/teacher/quizzes')
# def teacher_quizzes():
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     quizzes = db.execute('SELECT q.*, COUNT(qq.id) as q_count FROM quizzes q LEFT JOIN quiz_questions qq ON q.id=qq.quiz_id WHERE q.teacher_id=? GROUP BY q.id ORDER BY q.created_at DESC',(session['teacher_id'],)).fetchall()
#     classes  = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit']
#     return render_template('teacher_quizzes.html', quizzes=quizzes, classes=classes, subjects=subjects)

# @app.route('/teacher/create_quiz', methods=['POST'])
# def create_quiz():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     cur = db.execute('INSERT INTO quizzes (teacher_id,title,class_name,subject,duration,total_marks,status) VALUES (?,?,?,?,?,?,?)',
#         (session['teacher_id'],d['title'],d['class_name'],d['subject'],d.get('duration',30),d.get('total_marks',10),'Draft'))
#     qid = cur.lastrowid
#     for q in d.get('questions',[]):
#         db.execute('INSERT INTO quiz_questions (quiz_id,question,option_a,option_b,option_c,option_d,correct,marks) VALUES (?,?,?,?,?,?,?,?)',
#             (qid,q['question'],q['a'],q['b'],q['c'],q['d'],q['correct'],q.get('marks',1)))
#     db.commit()
#     return jsonify({'success':True,'quiz_id':qid})

# @app.route('/teacher/publish_quiz/<int:qid>', methods=['POST'])
# def publish_quiz(qid):
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute("UPDATE quizzes SET status='Active' WHERE id=? AND teacher_id=?",(qid,session['teacher_id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/quiz_results/<int:qid>')
# def quiz_results(qid):
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     quiz    = db.execute('SELECT * FROM quizzes WHERE id=?',(qid,)).fetchone()
#     results = db.execute('SELECT qa.*, s.name, s.roll_number FROM quiz_attempts qa JOIN students s ON qa.student_id=s.id WHERE qa.quiz_id=? ORDER BY qa.score DESC',(qid,)).fetchall()
#     return render_template('quiz_results.html', quiz=quiz, results=results)

# @app.route('/student/quizzes')
# def student_quizzes():
#     if session.get('role') != 'student': return redirect('/student/login')
#     db = get_db()
#     sid = session['student_id']
#     quizzes = db.execute('''SELECT q.*, t.name as teacher_name,
#         (SELECT score FROM quiz_attempts WHERE quiz_id=q.id AND student_id=?) as my_score,
#         (SELECT submitted_at FROM quiz_attempts WHERE quiz_id=q.id AND student_id=?) as attempted_at
#         FROM quizzes q JOIN teachers t ON q.teacher_id=t.id
#         WHERE q.class_name=? AND q.status="Active" ORDER BY q.created_at DESC''',(sid,sid,session['student_class'])).fetchall()
#     return render_template('student_quizzes.html', quizzes=quizzes)

# @app.route('/student/attempt_quiz/<int:qid>')
# def attempt_quiz(qid):
#     if session.get('role') != 'student': return redirect('/student/login')
#     db = get_db()
#     sid = session['student_id']
#     attempted = db.execute('SELECT id FROM quiz_attempts WHERE quiz_id=? AND student_id=?',(qid,sid)).fetchone()
#     if attempted: return redirect('/student/quiz_result/'+str(qid))
#     quiz      = db.execute('SELECT * FROM quizzes WHERE id=? AND status="Active"',(qid,)).fetchone()
#     questions = db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
#     if not quiz: return redirect('/student/quizzes')
#     return render_template('attempt_quiz.html', quiz=quiz, questions=questions)

# @app.route('/student/submit_quiz/<int:qid>', methods=['POST'])
# def submit_quiz(qid):
#     if session.get('role') != 'student': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     sid = session['student_id']
#     questions = db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
#     score = 0; answers = {}
#     for q in questions:
#         ans = d.get(str(q['id']),'')
#         answers[q['id']] = ans
#         if ans.upper() == q['correct'].upper():
#             score += q['marks']
#     import json as json_lib
#     db.execute('INSERT OR IGNORE INTO quiz_attempts (quiz_id,student_id,score,total,answers) VALUES (?,?,?,?,?)',
#                (qid,sid,score,len(questions),json_lib.dumps(answers)))
#     db.commit()
#     return jsonify({'success':True,'score':score,'total':len(questions)})

# @app.route('/student/quiz_result/<int:qid>')
# def student_quiz_result(qid):
#     if session.get('role') != 'student': return redirect('/student/login')
#     db = get_db()
#     sid = session['student_id']
#     quiz     = db.execute('SELECT q.*, t.name as teacher_name FROM quizzes q JOIN teachers t ON q.teacher_id=t.id WHERE q.id=?',(qid,)).fetchone()
#     attempt  = db.execute('SELECT * FROM quiz_attempts WHERE quiz_id=? AND student_id=?',(qid,sid)).fetchone()
#     questions= db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
#     import json as json_lib
#     answers  = json_lib.loads(attempt['answers']) if attempt and attempt['answers'] else {}
#     return render_template('quiz_result.html', quiz=quiz, attempt=attempt, questions=questions, answers=answers)

# # ═══════════════════════════════════════════════
# # FEATURE: STUDENT ACHIEVEMENTS / AWARDS
# # ═══════════════════════════════════════════════


# # ── ACHIEVERS / ACHIEVEMENTS PUBLIC ─────────────────────────
# # from flask import Flask, render_template, request, redirect, session, flash, jsonify
# # import sqlite3, os, uuid
# from werkzeug.utils import secure_filename

# # ✅ ADD THIS HERE
# UPLOAD_FOLDER = os.path.join('static', 'uploads', 'achievements')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/achievers')
# @app.route('/achievements')
# def achievers_page():
#     db = get_db()

#     sel_cat = request.args.get('category', 'All')

#     items = db.execute("""
#         SELECT * FROM achievements
#         WHERE class_name IN ('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')
#         ORDER BY class_name, achievement_date DESC
#     """).fetchall()

#     # categories
#     cats_raw = db.execute("SELECT DISTINCT category FROM achievements").fetchall()
#     cats = [r['category'] for r in cats_raw]

#     # filter
#     if sel_cat != 'All':
#         items = [i for i in items if i['category'] == sel_cat]

#     return render_template('achievers.html', items=items, cats=cats, sel_cat=sel_cat)

# # @app.route('/achievements')
# # def achievements():
# #     db = get_db()
# #     featured = []  # featured column removed
# #     all_ach  = db.execute('SELECT a.*, s.name as student_name FROM achievements a LEFT JOIN students s ON a.student_id=s.id ORDER BY a.achievement_date DESC').fetchall()
# #     categories = db.execute('SELECT DISTINCT category FROM achievements ORDER BY category').fetchall()
# #     sel_cat  = request.args.get('category','All')
# #     if sel_cat != 'All':
# #         all_ach = [a for a in all_ach if a['category']==sel_cat]
# #     return render_template('achievements.html', featured=featured, all_ach=all_ach, categories=categories, sel_cat=sel_cat)

# @app.route('/admin/achievements')
# def admin_achievements():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     ach      = db.execute('SELECT a.*, s.name as student_name FROM achievements a LEFT JOIN students s ON a.student_id=s.id ORDER BY a.created_at DESC').fetchall()
#     students = db.execute('SELECT id, name, class_name FROM students ORDER BY class_name, name').fetchall()
#     return render_template('admin_achievements.html', achievements=ach, students=students)



# @app.route('/admin/add_achievement', methods=['POST'])
# def add_achievement():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     sid = request.form.get('student_id') or None
#     db.execute('INSERT INTO achievements (student_id,title,category,description,achievement_date,awarded_by,class_name,is_featured) VALUES (?,?,?,?,?,?,?,?)',
#         (sid, request.form['title'], request.form['category'],
#          request.form.get('description',''), request.form.get('achievement_date',''),
#          request.form.get('awarded_by',''), request.form.get('class_name',''),
#          1 if request.form.get('is_featured') else 0))
#     db.commit()
#     flash('Achievement added!','success')
#     return redirect('/admin/achievements')

# @app.route('/admin/delete_achievement/<int:aid>', methods=['POST'])
# def delete_achievement(aid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM achievements WHERE id=?',(aid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/toggle_featured/<int:aid>', methods=['POST'])
# def toggle_featured(aid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     cur = db.execute('SELECT is_featured FROM achievements WHERE id=?',(aid,)).fetchone()
#     db.execute('UPDATE achievements SET is_featured=? WHERE id=?',(0 if cur['is_featured'] else 1, aid)); db.commit()
#     return jsonify({'success':True})



# # ═══════════════════════════════════════════════
# # FEATURE 7: ONLINE QUIZ / TEST
# # ═══════════════════════════════════════════════

# @app.route('/student/quizzes')
# @app.route('/student/quiz/<int:qid>')
# @app.route('/student/quiz/<int:qid>/submit', methods=['POST'])
# @app.route('/teacher/quizzes')
# @app.route('/teacher/quiz/create', methods=['POST'])
# @app.route('/teacher/quiz/<int:qid>/toggle', methods=['POST'])
# def toggle_quiz(qid):
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     q  = db.execute('SELECT status FROM quizzes WHERE id=? AND teacher_id=?',(qid,session['teacher_id'])).fetchone()
#     if not q: return jsonify({'error':'Not found'}), 404
#     new_status = 'Active' if q['status']=='Draft' else 'Draft'
#     db.execute('UPDATE quizzes SET status=? WHERE id=?',(new_status,qid))
#     db.commit()
#     return jsonify({'success':True,'status':new_status})

# @app.route('/teacher/quiz/<int:qid>/results')
# @app.route('/teacher/quiz/<int:qid>/delete', methods=['POST'])
# def delete_quiz(qid):
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM quiz_attempts WHERE quiz_id=?',(qid,))
#     db.execute('DELETE FROM quiz_questions WHERE quiz_id=?',(qid,))
#     db.execute('DELETE FROM quizzes WHERE id=? AND teacher_id=?',(qid,session['teacher_id']))
#     db.commit()
#     return jsonify({'success':True})

# # ═══════════════════════════════════════════════
# # FEATURE 9: ACHIEVEMENTS / AWARDS
# # ═══════════════════════════════════════════════

# # ═══════════════════════════════════════════════
# # FEATURE 10: STUDENT ID CARD PDF GENERATOR
# # ═══════════════════════════════════════════════

# # ═══════════════════════════════════════════════
# # FEATURE 2: WHATSAPP NOTIFICATION (Simulation)
# # ═══════════════════════════════════════════════


# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

# # ═══════════════════════════════════════════════
# # ADMIN — Live Classes Management
# # ═══════════════════════════════════════════════

# @app.route('/admin/live_classes')
# def admin_live_classes():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes_data = db.execute('''
#         SELECT lc.*, t.name as teacher_name
#         FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id
#         ORDER BY lc.status ASC, lc.scheduled_at DESC
#     ''').fetchall()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     all_classes = ['UKG'] + [f'Class {i}' for i in range(1, 11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit','Drawing','Physical Education']
#     # Stats
#     stats = {
#         'total':     len(classes_data),
#         'live':      sum(1 for lc in classes_data if lc['status']=='Live'),
#         'upcoming':  sum(1 for lc in classes_data if lc['status']=='Upcoming'),
#         'completed': sum(1 for lc in classes_data if lc['status']=='Completed'),
#     }
#     return render_template('admin_live_classes.html',
#         classes_data=classes_data, teachers=teachers,
#         all_classes=all_classes, subjects=subjects, stats=stats)

# @app.route('/admin/live_classes/add', methods=['POST'])
# def admin_add_live_class():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     db.execute('''INSERT INTO live_classes
#         (teacher_id,class_name,subject,title,meet_link,platform,scheduled_at,duration,status,description)
#         VALUES (?,?,?,?,?,?,?,?,?,?)''',
#         (d['teacher_id'], d['class_name'], d['subject'], d['title'],
#          d['meet_link'], d['platform'], d['scheduled_at'],
#          d.get('duration',60), d.get('status','Upcoming'), d.get('description','')))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/admin/live_classes/update_status', methods=['POST'])
# def admin_update_live_status():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json
#     db = get_db()
#     db.execute('UPDATE live_classes SET status=? WHERE id=?', (d['status'], d['id']))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/admin/live_classes/delete/<int:lcid>', methods=['POST'])
# def admin_delete_live_class(lcid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM live_classes WHERE id=?', (lcid,))
#     db.commit()
#     return jsonify({'success': True})

# # ═══════════════════════════════════════════════
# # ADMIN QUIZ MANAGER
# # ═══════════════════════════════════════════════

# @app.route('/admin/quiz_manager')
# def admin_quiz_manager():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     quizzes = db.execute('''
#         SELECT q.*, t.name as teacher_name,
#                COUNT(qa.id) as attempt_count,
#                AVG(CASE WHEN qa.total > 0 THEN qa.score*100.0/qa.total END) as avg_score
#         FROM quizzes q
#         LEFT JOIN teachers t ON q.teacher_id=t.id
#         LEFT JOIN quiz_attempts qa ON q.id=qa.quiz_id
#         GROUP BY q.id ORDER BY q.created_at DESC
#     ''').fetchall()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     classes  = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit']
#     return render_template('admin_quiz_manager.html',
#         quizzes=quizzes, teachers=teachers, classes=classes, subjects=subjects)

# @app.route('/admin/quiz/toggle/<int:qid>', methods=['POST'])
# def admin_toggle_quiz(qid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     q  = db.execute('SELECT status FROM quizzes WHERE id=?', (qid,)).fetchone()
#     if not q: return jsonify({'error':'Not found'}), 404
#     new_status = 'Active' if q['status'] == 'Draft' else 'Draft'
#     db.execute('UPDATE quizzes SET status=? WHERE id=?', (new_status, qid))
#     db.commit()
#     return jsonify({'success': True, 'status': new_status})

# @app.route('/admin/quiz/delete/<int:qid>', methods=['POST'])
# def admin_delete_quiz(qid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM quiz_attempts WHERE quiz_id=?', (qid,))
#     db.execute('DELETE FROM quiz_questions WHERE quiz_id=?', (qid,))
#     db.execute('DELETE FROM quizzes WHERE id=?', (qid,))
#     db.commit()
#     return jsonify({'success': True})

# @app.route('/admin/quiz/<int:qid>/results')
# def admin_quiz_results(qid):
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     quiz    = db.execute('SELECT q.*,t.name as tname FROM quizzes q JOIN teachers t ON q.teacher_id=t.id WHERE q.id=?',(qid,)).fetchone()
#     results = db.execute('''SELECT qa.*,s.name as student_name,s.roll_number,s.class_name
#         FROM quiz_attempts qa JOIN students s ON qa.student_id=s.id
#         WHERE qa.quiz_id=? ORDER BY qa.score DESC''',(qid,)).fetchall()
#     questions = db.execute('SELECT COUNT(*) FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchone()[0]
#     return render_template('admin_quiz_results.html', quiz=quiz, results=results, question_count=questions)


# # @app.route('/achievers')
# # def achievers_page():
# #     db = get_db()
# #     sel_cat = request.args.get('category','All')
# #     cls_list = "('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')"
# #     if sel_cat == 'All':
# #         items = db.execute(
# #             f"SELECT * FROM achievements WHERE class_name IN {cls_list} ORDER BY class_name, achievement_date DESC"
# #         ).fetchall()
# #     else:
# #         items = db.execute(
# #             f"SELECT * FROM achievements WHERE category=? AND class_name IN {cls_list} ORDER BY class_name, achievement_date DESC",
# #             (sel_cat,)
# #         ).fetchall()
# #     cats_raw = db.execute(f"SELECT DISTINCT category FROM achievements WHERE class_name IN {cls_list}").fetchall()
# #     cats = [r['category'] for r in cats_raw]
# #     return render_template('achievers.html', items=items, cats=cats, sel_cat=sel_cat)

# # ── ALIAS ROUTES (fix 404 errors) ─────────────────────────────────────────────

# # @app.route('/admin/achievements/add', methods=['POST'])
# # def add_achievement_alias():
# #     """Alias for /admin/add_achievement — fixes 404"""
# #     return add_achievement()











from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database.db import init_db, get_db
import os, uuid

app = Flask(__name__)
app.secret_key = 'brightmind_school_2024'

with app.app_context():
    init_db()

# ── PUBLIC ─────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    db = get_db()
    notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC LIMIT 4').fetchall()
    featured_achievers = db.execute(
        """SELECT * FROM achievements
           WHERE class_name IN ('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')
           ORDER BY class_name, achievement_date DESC LIMIT 12"""
    ).fetchall()
    return render_template('home.html', notices=notices, featured_achievers=featured_achievers)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admissions', methods=['GET','POST'])
def admissions():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO admissions (name,dob,class_name,parent_name,contact,email,address,status) VALUES (?,?,?,?,?,?,?,?)',
            (request.form['name'], request.form['dob'], request.form['class_name'],
             request.form['parent_name'], request.form['contact'], request.form['email'],
             request.form['address'], 'Pending'))
        db.commit()
        flash('Admission form submitted! We will contact you soon.', 'success')
        return redirect('/admissions')
    return render_template('admissions.html')

@app.route('/academics')
def academics():
    return render_template('academics.html')

@app.route('/notices')
def notices():
    db = get_db()
    all_notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC').fetchall()
    return render_template('notices.html', notices=all_notices)

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO contact_messages (name,email,subject,message) VALUES (?,?,?,?)',
            (request.form['name'], request.form['email'], request.form['subject'], request.form['message']))
        db.commit()
        flash('Message sent! We will reply shortly.', 'success')
        return redirect('/contact')
    return render_template('contact.html')

# ── TEACHERS PUBLIC ────────────────────────────────────────────────────────────
@app.route('/teachers')
def teachers_list():
    db = get_db()
    teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
    return render_template('teachers.html', teachers=teachers)

@app.route('/teachers/<int:teacher_id>')
def teacher_profile(teacher_id):
    db = get_db()
    teacher = db.execute('SELECT * FROM teachers WHERE id=?', (teacher_id,)).fetchone()
    if not teacher:
        flash('Teacher not found.', 'error')
        return redirect('/teachers')
    assignments = db.execute(
        'SELECT class_name, subject FROM teacher_assignments WHERE teacher_id=? ORDER BY class_name',
        (teacher_id,)).fetchall()
    return render_template('teacher_profile.html', teacher=teacher, assignments=assignments)

# ── GALLERY PUBLIC ─────────────────────────────────────────────────────────────
@app.route('/gallery')
def gallery():
    db = get_db()
    sel_cat = request.args.get('category', 'All')
    if sel_cat == 'All':
        photos = db.execute('SELECT * FROM gallery_photos ORDER BY uploaded_at DESC').fetchall()
    else:
        photos = db.execute('SELECT * FROM gallery_photos WHERE category=? ORDER BY uploaded_at DESC', (sel_cat,)).fetchall()
    categories = db.execute('SELECT DISTINCT category FROM gallery_photos ORDER BY category').fetchall()
    return render_template('gallery.html', photos=photos, categories=categories, sel_cat=sel_cat)

# ── STUDENT PORTAL ─────────────────────────────────────────────────────────────
@app.route('/student/login', methods=['GET','POST'])
def student_login():
    if request.method == 'POST':
        db = get_db()
        s = db.execute('SELECT * FROM students WHERE roll_number=? AND password=?',
            (request.form['roll_number'], request.form['password'])).fetchone()
        if s:
            session.update({'student_id':s['id'],'student_name':s['name'],'student_class':s['class_name'],'role':'student'})
            return redirect('/student/dashboard')
        flash('Invalid credentials.', 'error')
    return render_template('student_login.html')

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student': return redirect('/student/login')
    db  = get_db()
    sid = session['student_id']
    marks      = db.execute('SELECT * FROM marks WHERE student_id=?', (sid,)).fetchall()
    attendance = db.execute('SELECT * FROM attendance WHERE student_id=? ORDER BY date DESC LIMIT 30', (sid,)).fetchall()
    homework   = db.execute('SELECT * FROM homework WHERE class_name=? ORDER BY due_date DESC', (session['student_class'],)).fetchall()
    fees       = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month', (sid,)).fetchall()
    total   = len(attendance)
    present = sum(1 for a in attendance if a['status'] == 'Present')
    pct     = round((present/total*100) if total else 0, 1)
    return render_template('student_dashboard.html',
        marks=marks, attendance=attendance, homework=homework, fees=fees,
        attend_pct=pct, total_days=total, present_days=present)

@app.route('/student/logout')
def student_logout():
    session.clear(); return redirect('/')

# ── TEACHER PORTAL ─────────────────────────────────────────────────────────────
@app.route('/teacher/login', methods=['GET','POST'])
def teacher_login():
    if request.method == 'POST':
        db = get_db()
        t = db.execute('SELECT * FROM teachers WHERE username=? AND password=?',
            (request.form['username'], request.form['password'])).fetchone()
        if t:
            session.update({'teacher_id':t['id'],'teacher_name':t['name'],'teacher_sub':t['subject'],'role':'teacher'})
            return redirect('/teacher/dashboard')
        flash('Invalid credentials.', 'error')
    return render_template('teacher_login.html')

@app.route('/teacher/dashboard')
def teacher_dashboard():
    if session.get('role') != 'teacher': return redirect('/teacher/login')
    db = get_db()
    classes  = db.execute('SELECT DISTINCT class_name FROM students ORDER BY class_name').fetchall()
    students = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
    homework = db.execute('SELECT h.*,t.name as tname FROM homework h JOIN teachers t ON h.teacher_id=t.id ORDER BY due_date DESC').fetchall()
    return render_template('teacher_dashboard.html', classes=classes, students=students, homework=homework)

@app.route('/teacher/upload_marks', methods=['POST'])
def upload_marks():
    if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    db.execute('INSERT OR REPLACE INTO marks (student_id,subject,marks,max_marks,exam_type) VALUES (?,?,?,?,?)',
        (d['student_id'],d['subject'],d['marks'],d['max_marks'],d['exam_type']))
    db.commit(); return jsonify({'success':True})

@app.route('/teacher/attendance', methods=['POST'])
def mark_attendance():
    if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    for r in d['records']:
        db.execute('INSERT OR REPLACE INTO attendance (student_id,date,status) VALUES (?,?,?)',
            (r['student_id'],d['date'],r['status']))
    db.commit(); return jsonify({'success':True})

@app.route('/teacher/upload_homework', methods=['POST'])
def upload_homework():
    if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    db.execute('INSERT INTO homework (class_name,subject,description,due_date,teacher_id) VALUES (?,?,?,?,?)',
        (d['class_name'],d['subject'],d['description'],d['due_date'],session['teacher_id']))
    db.commit(); return jsonify({'success':True})


@app.route('/teacher/logout')
def teacher_logout():
    session.clear(); return redirect('/')

# ── ADMIN LOGIN ────────────────────────────────────────────────────────────────
@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username']=='admin' and request.form['password']=='admin123':
            session['role'] = 'admin'; return redirect('/admin/dashboard')
        flash('Wrong credentials.', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear(); return redirect('/')

# ── ADMIN DASHBOARD ────────────────────────────────────────────────────────────
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    stats = {
        'students':   db.execute('SELECT COUNT(*) FROM students').fetchone()[0],
        'teachers':   db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
        'admissions': db.execute("SELECT COUNT(*) FROM admissions WHERE status='Pending'").fetchone()[0],
        'notices':    db.execute('SELECT COUNT(*) FROM notices').fetchone()[0],
    }
    admissions  = db.execute('SELECT * FROM admissions ORDER BY created_at DESC').fetchall()
    messages    = db.execute('SELECT * FROM contact_messages ORDER BY created_at DESC').fetchall()
    students    = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
    teachers    = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
    all_notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC').fetchall()
    return render_template('admin_dashboard.html',
        stats=stats, admissions=admissions, messages=messages,
        students=students, teachers=teachers, all_notices=all_notices)

# ── ADMIN STUDENTS ─────────────────────────────────────────────────────────────
@app.route('/admin/add_student', methods=['POST'])
def add_student():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    try:
        db.execute('INSERT INTO students (name,class_name,roll_number,parent_name,contact,password) VALUES (?,?,?,?,?,?)',
            (request.form['name'],request.form['class_name'],request.form['roll_number'],
             request.form['parent_name'],request.form['contact'],request.form['password']))
        db.commit(); flash('Student added!', 'success')
    except: flash('Error: Roll number may already exist.', 'error')
    return redirect('/admin/dashboard')

@app.route('/admin/delete_student/<int:sid>', methods=['POST'])
def delete_student(sid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    for tbl in ['marks','attendance','fees']: db.execute(f'DELETE FROM {tbl} WHERE student_id=?', (sid,))
    db.execute('DELETE FROM students WHERE id=?', (sid,)); db.commit()
    return jsonify({'success':True})

# ── ADMIN TEACHERS ─────────────────────────────────────────────────────────────
@app.route('/admin/add_teacher', methods=['POST'])
def add_teacher():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    try:
        db.execute('INSERT INTO teachers (name,subject,username,password,email) VALUES (?,?,?,?,?)',
            (request.form['name'],request.form['subject'],request.form['username'],
             request.form['password'],request.form.get('email','')))
        db.commit(); flash(f"Teacher '{request.form['name']}' added!", 'success')
    except: flash('Error: Username already exists.', 'error')
    return redirect('/admin/dashboard')

@app.route('/admin/delete_teacher/<int:tid>', methods=['POST'])
def delete_teacher(tid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    db.execute('DELETE FROM homework WHERE teacher_id=?', (tid,))
    db.execute('DELETE FROM teacher_assignments WHERE teacher_id=?', (tid,))
    db.execute('DELETE FROM teachers WHERE id=?', (tid,))
    db.commit(); return jsonify({'success':True})

@app.route('/admin/teacher_edit/<int:tid>')
def admin_teacher_edit(tid):
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    teacher = db.execute('SELECT * FROM teachers WHERE id=?', (tid,)).fetchone()
    return render_template('admin_teacher_edit.html', teacher=teacher)

@app.route('/admin/update_teacher_info', methods=['POST'])
def update_teacher_info():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    db.execute('UPDATE teachers SET phone=?,qualification=?,experience=?,bio=?,joining_date=? WHERE id=?',
        (d.get('phone',''),d.get('qualification',''),d.get('experience',''),
         d.get('bio',''),d.get('joining_date',''),d['id']))
    db.commit(); return jsonify({'success':True})

@app.route('/admin/upload_teacher_photo/<int:tid>', methods=['POST'])
def upload_teacher_photo(tid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
    file = request.files['photo']
    ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
    if ext not in {'png','jpg','jpeg','gif','webp'}: return jsonify({'error':'Invalid file type'}), 400
    fname = f"teacher_{tid}_{uuid.uuid4().hex[:8]}.{ext}"
    path  = os.path.join(app.root_path, 'static', 'uploads', 'teachers', fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)
    db = get_db()
    db.execute('UPDATE teachers SET photo=? WHERE id=?', (fname, tid))
    db.commit(); return jsonify({'success':True, 'filename':fname})

# ── ADMIN NOTICES ──────────────────────────────────────────────────────────────
@app.route('/admin/add_notice', methods=['POST'])
def add_notice():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    db.execute('INSERT INTO notices (title,content,category) VALUES (?,?,?)',
        (request.form['title'],request.form['content'],request.form['category']))
    db.commit(); flash('Notice posted!', 'success'); return redirect('/admin/dashboard')

@app.route('/admin/edit_notice', methods=['POST'])
def edit_notice():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    db.execute('UPDATE notices SET title=?,content=?,category=? WHERE id=?',
        (request.form['title'],request.form['content'],request.form['category'],request.form['notice_id']))
    db.commit(); flash('Notice updated!', 'success'); return redirect('/admin/dashboard')

@app.route('/admin/delete_notice/<int:nid>', methods=['POST'])
def delete_notice(nid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db(); db.execute('DELETE FROM notices WHERE id=?', (nid,)); db.commit()
    return jsonify({'success':True})

# ── ADMIN ADMISSIONS ───────────────────────────────────────────────────────────
@app.route('/admin/update_admission_status', methods=['POST'])
def update_admission_status():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    db.execute('UPDATE admissions SET status=? WHERE id=?', (d['status'],d['id']))
    db.commit(); return jsonify({'success':True})

@app.route('/admin/delete_admission/<int:aid>', methods=['POST'])
def delete_admission(aid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db(); db.execute('DELETE FROM admissions WHERE id=?', (aid,)); db.commit()
    return jsonify({'success':True})

@app.route('/admin/delete_message/<int:mid>', methods=['POST'])
def delete_message(mid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db(); db.execute('DELETE FROM contact_messages WHERE id=?', (mid,)); db.commit()
    return jsonify({'success':True})

# ── ADMIN TEACHER ASSIGNMENTS ──────────────────────────────────────────────────
@app.route('/admin/teacher_assignments')
def teacher_assignments_page():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
    return render_template('teacher_assignments.html', teachers=teachers)

@app.route('/admin/assign_teacher', methods=['POST'])
def assign_teacher():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    try:
        db.execute('INSERT OR REPLACE INTO teacher_assignments (teacher_id,class_name,subject) VALUES (?,?,?)',
            (d['teacher_id'],d['class_name'],d['subject']))
        db.commit(); return jsonify({'success':True})
    except Exception as e: return jsonify({'error':str(e)}), 500

@app.route('/admin/remove_assignment', methods=['POST'])
def remove_assignment():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    db.execute('DELETE FROM teacher_assignments WHERE id=?', (d['id'],))
    db.commit(); return jsonify({'success':True})

@app.route('/admin/get_assignments')
def get_assignments():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    rows = db.execute('''SELECT ta.id, ta.class_name, ta.subject, t.name as teacher_name, t.id as teacher_id
        FROM teacher_assignments ta JOIN teachers t ON ta.teacher_id=t.id ORDER BY ta.class_name, ta.subject''').fetchall()
    return jsonify([dict(r) for r in rows])

# ── ADMIN GALLERY ──────────────────────────────────────────────────────────────
@app.route('/admin/gallery')
def admin_gallery():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    photos = db.execute('SELECT * FROM gallery_photos ORDER BY uploaded_at DESC').fetchall()
    return render_template('admin_gallery.html', photos=photos)

@app.route('/admin/upload_gallery_photo', methods=['POST'])
def upload_gallery_photo():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
    file     = request.files['photo']
    title    = request.form.get('title','Photo')
    category = request.form.get('category','General')
    desc     = request.form.get('description','')
    ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
    if ext not in {'png','jpg','jpeg','gif','webp'}: return jsonify({'error':'Invalid file type'}), 400
    fname = f"gallery_{uuid.uuid4().hex[:10]}.{ext}"
    path  = os.path.join(app.root_path, 'static', 'uploads', 'gallery', fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)
    db = get_db()
    db.execute('INSERT INTO gallery_photos (title,category,filename,description) VALUES (?,?,?,?)',
        (title,category,fname,desc))
    db.commit(); return jsonify({'success':True, 'filename':fname})

@app.route('/admin/delete_gallery_photo/<int:pid>', methods=['POST'])
def delete_gallery_photo(pid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    p = db.execute('SELECT filename FROM gallery_photos WHERE id=?', (pid,)).fetchone()
    if p:
        path = os.path.join(app.root_path,'static','uploads','gallery',p['filename'])
        if os.path.exists(path): os.remove(path)
        db.execute('DELETE FROM gallery_photos WHERE id=?', (pid,)); db.commit()
    return jsonify({'success':True})

# ── ADMIN FEES ─────────────────────────────────────────────────────────────────
@app.route('/admin/fees')
def admin_fees():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
    sel_class = request.args.get('class_name','Class 5')
    sel_month = request.args.get('month','')
    sel_year  = request.args.get('year','2024-25')
    fee_struct = db.execute('SELECT * FROM fee_structure WHERE class_name=?', (sel_class,)).fetchone()
    q = 'SELECT f.*, s.name as student_name, s.roll_number FROM fees f JOIN students s ON f.student_id=s.id WHERE f.class_name=?'
    p = [sel_class]
    if sel_month: q += ' AND f.fee_month=?'; p.append(sel_month)
    q += ' ORDER BY f.fee_month, s.roll_number'
    fees = db.execute(q, p).fetchall()
    total_due  = sum(f['total_fee'] for f in fees)
    total_paid = sum(f['paid_amount'] for f in fees)
    total_rem  = sum(f['remaining'] for f in fees)
    months = db.execute('SELECT DISTINCT fee_month FROM fees WHERE class_name=? ORDER BY fee_month', (sel_class,)).fetchall()
    students_summary = db.execute('''
        SELECT s.id, s.name, s.roll_number,
               COUNT(f.id) as total_months,
               SUM(CASE WHEN f.status="Paid" THEN 1 ELSE 0 END) as paid_months,
               SUM(f.total_fee) as total_due, SUM(f.paid_amount) as total_paid,
               SUM(f.remaining) as total_remaining
        FROM students s LEFT JOIN fees f ON s.id=f.student_id
        WHERE s.class_name=? GROUP BY s.id ORDER BY s.roll_number
    ''', (sel_class,)).fetchall()
    return render_template('admin_fees.html',
        classes=classes, sel_class=sel_class, sel_month=sel_month, sel_year=sel_year,
        fee_struct=fee_struct, fees=fees, months=months,
        total_due=total_due, total_paid=total_paid, total_rem=total_rem,
        students_summary=students_summary)

@app.route('/admin/fees/update', methods=['POST'])
def update_fee():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    total = float(d.get('total_fee',0))
    paid  = float(d.get('paid_amount',0))
    rem   = max(0, total - paid)
    status = 'Paid' if rem<=0 else ('Partial' if paid>0 else 'Pending')
    db.execute('''INSERT INTO fees (student_id,class_name,fee_month,fee_year,tuition_fee,other_fee,total_fee,paid_amount,remaining,status,paid_date,remarks)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(student_id,fee_month) DO UPDATE SET
        total_fee=excluded.total_fee, paid_amount=excluded.paid_amount,
        remaining=excluded.remaining, status=excluded.status,
        paid_date=excluded.paid_date, remarks=excluded.remarks''',
        (d['student_id'],d['class_name'],d['fee_month'],d.get('fee_year','2024-25'),
         d.get('tuition_fee',0),d.get('other_fee',0),total,paid,rem,status,
         d.get('paid_date') or None,d.get('remarks','')))
    db.commit(); return jsonify({'success':True,'remaining':rem,'status':status})

@app.route('/admin/fees/generate_monthly', methods=['POST'])
def generate_monthly_fees():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    struct = db.execute('SELECT * FROM fee_structure WHERE class_name=?', (d['class_name'],)).fetchone()
    if not struct: return jsonify({'error':'Fee structure not set'}), 400
    total    = struct['tuition_fee']+struct['activity_fee']+struct['computer_fee']+struct['other_fee']
    students = db.execute('SELECT id FROM students WHERE class_name=?', (d['class_name'],)).fetchall()
    count = 0
    for s in students:
        try:
            db.execute('''INSERT OR IGNORE INTO fees
                (student_id,class_name,fee_month,fee_year,tuition_fee,other_fee,total_fee,paid_amount,remaining,status)
                VALUES (?,?,?,?,?,?,?,0,?,?)''',
                (s['id'],d['class_name'],d['fee_month'],d.get('fee_year','2024-25'),
                 struct['tuition_fee'],struct['activity_fee']+struct['computer_fee']+struct['other_fee'],
                 total,total,'Pending'))
            count += 1
        except: pass
    db.commit(); return jsonify({'success':True,'generated':count})

@app.route('/admin/fees/update_structure', methods=['POST'])
def update_fee_structure():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    db.execute('''INSERT INTO fee_structure (class_name,tuition_fee,activity_fee,computer_fee,other_fee)
        VALUES (?,?,?,?,?) ON CONFLICT(class_name) DO UPDATE SET
        tuition_fee=excluded.tuition_fee, activity_fee=excluded.activity_fee,
        computer_fee=excluded.computer_fee, other_fee=excluded.other_fee''',
        (d['class_name'],d['tuition_fee'],d['activity_fee'],d['computer_fee'],d['other_fee']))
    db.commit(); return jsonify({'success':True})

@app.route('/admin/fees/student_detail/<int:sid>')
def admin_student_fee_detail(sid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    fees = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month', (sid,)).fetchall()
    return jsonify({'fees':[dict(f) for f in fees]})


# ═══════════════════════════════════════════════
# FEATURE 1: RESULT / REPORT CARD PDF DOWNLOAD
# ═══════════════════════════════════════════════

@app.route('/student/report_card')
def student_report_card():
    if session.get('role') != 'student': return redirect('/student/login')
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from io import BytesIO
    from flask import make_response

    db  = get_db()
    sid = session['student_id']
    student  = db.execute('SELECT * FROM students WHERE id=?', (sid,)).fetchone()
    marks    = db.execute('SELECT * FROM marks WHERE student_id=? ORDER BY subject', (sid,)).fetchall()
    attendance = db.execute('SELECT * FROM attendance WHERE student_id=?', (sid,)).fetchall()
    total   = len(attendance)
    present = sum(1 for a in attendance if a['status'] == 'Present')
    att_pct = round((present/total*100) if total else 0, 1)

    buffer = BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=A4,
                               rightMargin=1.5*cm, leftMargin=1.5*cm,
                               topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = getSampleStyleSheet()
    story  = []

    NAVY  = colors.HexColor('#0d1b3e')
    GOLD  = colors.HexColor('#c9a84c')
    CREAM = colors.HexColor('#fdf8f0')
    GREEN = colors.HexColor('#2e7d32')
    RED   = colors.HexColor('#c62828')
    ORANGE= colors.HexColor('#e65100')

    # ── HEADER ──────────────────────────────────────────
    header_data = [[
        Paragraph('<font color="#0d1b3e"><b>🏫 BRIGHTMIND SCHOOL</b></font>', ParagraphStyle('h', fontSize=18, fontName='Helvetica-Bold', alignment=TA_CENTER)),
    ]]
    header_tbl = Table(header_data, colWidths=[17*cm])
    header_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CREAM),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROUNDEDCORNERS', [8]),
    ]))
    story.append(header_tbl)

    sub_styles = ParagraphStyle('sub', fontSize=9, fontName='Helvetica', alignment=TA_CENTER, textColor=colors.HexColor('#555'))
    story.append(Paragraph('Est. 1995 · CBSE Affiliated · Delhi – 110001', sub_styles))
    story.append(Paragraph('Phone: +91 11 1234 5678 | Email: info@brightmindschool.edu.in', sub_styles))
    story.append(Spacer(1, 10))

    title_style = ParagraphStyle('title', fontSize=14, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=NAVY, spaceBefore=4, spaceAfter=4)
    story.append(Paragraph('STUDENT PROGRESS REPORT CARD', title_style))
    story.append(Paragraph('Academic Year: 2024–25', ParagraphStyle('ay', fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#777'))))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=10))

    # ── STUDENT INFO ─────────────────────────────────────
    info_data = [
        ['Student Name:', student['name'],    'Roll Number:', student['roll_number']],
        ['Class:',        student['class_name'], "Parent's Name:", student['parent_name'] or '—'],
        ['Contact:',      student['contact'] or '—', 'Attendance:', f"{att_pct}% ({present}/{total} days)"],
    ]
    info_tbl = Table(info_data, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
    info_tbl.setStyle(TableStyle([
        ('FONTNAME',  (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',  (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE',  (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (0,-1), NAVY),
        ('TEXTCOLOR', (2,0), (2,-1), NAVY),
        ('BACKGROUND',(0,0), (-1,-1), CREAM),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [CREAM, colors.white]),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#ddd')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 14))

    # ── MARKS TABLE ──────────────────────────────────────
    story.append(Paragraph('Academic Performance', ParagraphStyle('sec', fontSize=11, fontName='Helvetica-Bold', textColor=NAVY, spaceBefore=4, spaceAfter=6)))

    if marks:
        marks_header = [['S.No.', 'Subject', 'Exam Type', 'Marks Obtained', 'Max Marks', 'Percentage', 'Grade', 'Remarks']]
        marks_rows   = []
        total_marks = total_max = 0
        for i, m in enumerate(marks, 1):
            pct   = round(m['marks']/m['max_marks']*100, 1) if m['max_marks'] else 0
            grade = 'A1' if pct>=90 else 'A2' if pct>=80 else 'B1' if pct>=70 else 'B2' if pct>=60 else 'C1' if pct>=50 else 'D'
            rmk   = 'Excellent' if pct>=90 else 'Very Good' if pct>=80 else 'Good' if pct>=70 else 'Average' if pct>=50 else 'Needs Improvement'
            total_marks += m['marks']; total_max += m['max_marks']
            marks_rows.append([str(i), m['subject'], m['exam_type'],
                               str(int(m['marks'])), str(int(m['max_marks'])),
                               f"{pct}%", grade, rmk])

        overall_pct = round(total_marks/total_max*100, 1) if total_max else 0
        overall_grade = 'A1' if overall_pct>=90 else 'A2' if overall_pct>=80 else 'B1' if overall_pct>=70 else 'B2' if overall_pct>=60 else 'C1' if overall_pct>=50 else 'D'
        marks_rows.append(['', 'TOTAL / OVERALL', '', f"{int(total_marks)}", f"{int(total_max)}", f"{overall_pct}%", overall_grade, ''])

        all_rows = marks_header + marks_rows
        marks_tbl = Table(all_rows, colWidths=[1*cm, 4*cm, 2.5*cm, 2.5*cm, 2*cm, 2*cm, 1.5*cm, 2.5*cm])
        style = TableStyle([
            ('BACKGROUND',  (0,0), (-1,0), NAVY),
            ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
            ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',    (0,0), (-1,-1), 8),
            ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
            ('ALIGN',       (1,0), (1,-1), 'LEFT'),
            ('ALIGN',       (7,0), (7,-1), 'LEFT'),
            ('GRID',        (0,0), (-1,-1), 0.3, colors.HexColor('#ccc')),
            ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, CREAM]),
            ('TOPPADDING',  (0,0), (-1,-1), 5),
            ('BOTTOMPADDING',(0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('FONTNAME',    (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('BACKGROUND',  (0,-1), (-1,-1), colors.HexColor('#e8f5e9')),
            ('TEXTCOLOR',   (0,-1), (-1,-1), GREEN),
        ])
        marks_tbl.setStyle(style)
        story.append(marks_tbl)
    else:
        story.append(Paragraph('No marks recorded yet.', styles['Normal']))

    story.append(Spacer(1, 16))

    # ── SUMMARY BOX ──────────────────────────────────────
    if marks:
        status = 'PASS ✓' if overall_pct >= 33 else 'FAIL ✗'
        status_color = GREEN if overall_pct >= 33 else RED
        summary_data = [
            [Paragraph(f'<b>Overall Percentage:</b> {overall_pct}%', ParagraphStyle('s', fontSize=10)),
             Paragraph(f'<b>Overall Grade:</b> {overall_grade}', ParagraphStyle('s', fontSize=10)),
             Paragraph(f'<b>Result:</b> <font color="{"#2e7d32" if overall_pct>=33 else "#c62828"}">{status}</font>', ParagraphStyle('s', fontSize=10)),
             Paragraph(f'<b>Attendance:</b> {att_pct}%', ParagraphStyle('s', fontSize=10))],
        ]
        sum_tbl = Table(summary_data, colWidths=[4.25*cm]*4)
        sum_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e3f2fd')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#90caf9')),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(sum_tbl)

    story.append(Spacer(1, 20))

    # ── GRADE SCALE ──────────────────────────────────────
    grade_data = [['Grade Scale:','A1 (90-100)','A2 (80-89)','B1 (70-79)','B2 (60-69)','C1 (50-59)','D (Below 50)']]
    grade_tbl  = Table(grade_data, colWidths=[2.5*cm]+[2.14*cm]*6)
    grade_tbl.setStyle(TableStyle([
        ('FONTNAME',  (0,0), (0,0), 'Helvetica-Bold'),
        ('FONTSIZE',  (0,0), (-1,-1), 7.5),
        ('BACKGROUND',(0,0), (-1,-1), CREAM),
        ('GRID',      (0,0), (-1,-1), 0.3, colors.HexColor('#ddd')),
        ('ALIGN',     (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',(0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
    ]))
    story.append(grade_tbl)
    story.append(Spacer(1, 20))

    # ── SIGNATURES ───────────────────────────────────────
    sig_data = [['Class Teacher', 'Examination Controller', 'Principal'],
                ['________________', '________________', '________________'],
                ['Date: ___________', 'Date: ___________', 'Date: ___________']]
    sig_tbl  = Table(sig_data, colWidths=[5.67*cm]*3)
    sig_tbl.setStyle(TableStyle([
        ('ALIGN',   (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE',(0,0), (-1,-1), 9),
        ('FONTNAME',(0,0), (-1,0), 'Helvetica-Bold'),
        ('TEXTCOLOR',(0,0),(-1,0), NAVY),
        ('TOPPADDING',(0,0),(-1,-1), 4),
    ]))
    story.append(sig_tbl)

    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD))
    footer_style = ParagraphStyle('ft', fontSize=7.5, alignment=TA_CENTER, textColor=colors.HexColor('#888'), spaceBefore=4)
    story.append(Paragraph('This is a computer-generated report card. BrightMind School, Delhi – 110001', footer_style))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type']        = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=ReportCard_{student["roll_number"]}.pdf'
    return response

# ═══════════════════════════════════════════════
# FEATURE 2: TIMETABLE MANAGEMENT
# ═══════════════════════════════════════════════

@app.route('/timetable')
def timetable():
    db = get_db()
    classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
    sel_class = request.args.get('class_name', session.get('student_class','Class 5'))
    days      = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    periods   = list(range(1,7))

    rows = db.execute(
        'SELECT * FROM timetable WHERE class_name=? ORDER BY day, period', (sel_class,)
    ).fetchall()

    # Build dict: day -> {period -> row}
    tt = {day: {} for day in days}
    for r in rows:
        tt[r['day']][r['period']] = r

    period_times = {1:'8:00-8:45',2:'8:45-9:30',3:'9:30-10:15',
                    4:'10:30-11:15',5:'11:15-12:00',6:'12:00-12:45'}

    return render_template('timetable.html',
        classes=classes, sel_class=sel_class, days=days,
        periods=periods, tt=tt, period_times=period_times)

@app.route('/admin/timetable')
def admin_timetable():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
    sel_class = request.args.get('class_name','Class 5')
    teachers  = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
    days      = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    periods   = list(range(1,7))
    rows = db.execute('SELECT * FROM timetable WHERE class_name=? ORDER BY day,period',(sel_class,)).fetchall()
    tt   = {day:{} for day in days}
    for r in rows: tt[r['day']][r['period']] = r
    period_times = {1:'8:00-8:45',2:'8:45-9:30',3:'9:30-10:15',
                    4:'10:30-11:15',5:'11:15-12:00',6:'12:00-12:45'}
    return render_template('admin_timetable.html',
        classes=classes, sel_class=sel_class, teachers=teachers,
        days=days, periods=periods, tt=tt, period_times=period_times)

@app.route('/admin/timetable/save', methods=['POST'])
def save_timetable():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d  = request.json
    db = get_db()
    try:
        db.execute('''INSERT INTO timetable (class_name,day,period,subject,teacher_id,start_time,end_time)
            VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(class_name,day,period) DO UPDATE SET
            subject=excluded.subject, teacher_id=excluded.teacher_id''',
            (d['class_name'],d['day'],d['period'],d['subject'],
             d.get('teacher_id') or None, d.get('start_time',''), d.get('end_time','')))
        db.commit()
        return jsonify({'success':True})
    except Exception as e:
        return jsonify({'error':str(e)}), 500

@app.route('/admin/timetable/delete', methods=['POST'])
def delete_timetable_entry():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d  = request.json
    db = get_db()
    db.execute('DELETE FROM timetable WHERE class_name=? AND day=? AND period=?',
               (d['class_name'],d['day'],d['period']))
    db.commit()
    return jsonify({'success':True})

# ═══════════════════════════════════════════════
# FEATURE 3: ADMIN ANALYTICS DASHBOARD
# ═══════════════════════════════════════════════

@app.route('/admin/analytics')
def admin_analytics():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()

    # Fees analytics
    fee_stats = db.execute('''
        SELECT class_name,
               SUM(total_fee) as total_due,
               SUM(paid_amount) as total_paid,
               SUM(remaining) as total_remaining,
               COUNT(CASE WHEN status="Paid" THEN 1 END) as paid_count,
               COUNT(CASE WHEN status="Pending" THEN 1 END) as pending_count,
               COUNT(CASE WHEN status="Overdue" THEN 1 END) as overdue_count,
               COUNT(*) as total_count
        FROM fees GROUP BY class_name ORDER BY class_name
    ''').fetchall()

    # Monthly fee collection
    monthly = db.execute('''
        SELECT fee_month, SUM(paid_amount) as collected, SUM(remaining) as pending
        FROM fees GROUP BY fee_month ORDER BY fee_month
    ''').fetchall()

    # Attendance stats per class
    att_stats = db.execute('''
        SELECT s.class_name,
               COUNT(a.id) as total_records,
               SUM(CASE WHEN a.status="Present" THEN 1 ELSE 0 END) as present_count
        FROM students s LEFT JOIN attendance a ON s.id=a.student_id
        GROUP BY s.class_name ORDER BY s.class_name
    ''').fetchall()

    # Top students by marks
    top_students = db.execute('''
        SELECT s.name, s.class_name, s.roll_number,
               AVG(m.marks/m.max_marks*100) as avg_pct,
               COUNT(m.id) as subjects
        FROM students s JOIN marks m ON s.id=m.student_id
        GROUP BY s.id HAVING subjects>=2
        ORDER BY avg_pct DESC LIMIT 10
    ''').fetchall()

    # Overall summary
    summary = {
        'total_students': db.execute('SELECT COUNT(*) FROM students').fetchone()[0],
        'total_teachers': db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
        'total_fee_due':  db.execute('SELECT SUM(total_fee) FROM fees').fetchone()[0] or 0,
        'total_fee_paid': db.execute('SELECT SUM(paid_amount) FROM fees').fetchone()[0] or 0,
        'pending_admissions': db.execute("SELECT COUNT(*) FROM admissions WHERE status='Pending'").fetchone()[0],
        'total_notices': db.execute('SELECT COUNT(*) FROM notices').fetchone()[0],
    }
    summary['collection_pct'] = round(summary['total_fee_paid']/summary['total_fee_due']*100 if summary['total_fee_due'] else 0, 1)

    return render_template('admin_analytics.html',
        fee_stats=fee_stats, monthly=monthly, att_stats=att_stats,
        top_students=top_students, summary=summary)

# ═══════════════════════════════════════════════
# FEATURE 4: EXAM DATE SHEET
# ═══════════════════════════════════════════════

@app.route('/exam_schedule')
def exam_schedule():
    db = get_db()
    exams = db.execute('SELECT * FROM exam_schedule ORDER BY exam_date, class_name').fetchall()
    classes = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
    sel_class = request.args.get('class_name','All')
    if sel_class != 'All':
        exams = [e for e in exams if e['class_name']==sel_class]
    return render_template('exam_schedule.html', exams=exams, classes=classes, sel_class=sel_class)

@app.route('/admin/exam_schedule')
def admin_exam_schedule():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    exams = db.execute('SELECT * FROM exam_schedule ORDER BY exam_date, class_name').fetchall()
    classes = ['UKG'] + [f'Class {i}' for i in range(1,11)]
    return render_template('admin_exam_schedule.html', exams=exams, classes=classes)

@app.route('/admin/exam_schedule/add', methods=['POST'])
def add_exam():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    db.execute('INSERT INTO exam_schedule (class_name,subject,exam_date,day,start_time,end_time,exam_type,venue) VALUES (?,?,?,?,?,?,?,?)',
        (request.form['class_name'], request.form['subject'], request.form['exam_date'],
         request.form.get('day',''), request.form.get('start_time','10:00'),
         request.form.get('end_time','13:00'), request.form['exam_type'],
         request.form.get('venue','Main Hall')))
    db.commit()
    flash('Exam added!', 'success')
    return redirect('/admin/exam_schedule')

@app.route('/admin/exam_schedule/delete/<int:eid>', methods=['POST'])
def delete_exam(eid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    db.execute('DELETE FROM exam_schedule WHERE id=?', (eid,))
    db.commit()
    return jsonify({'success':True})

# ═══════════════════════════════════════════════
# FEATURE 5: PARENT PORTAL
# ═══════════════════════════════════════════════

@app.route('/parent/login', methods=['GET','POST'])
def parent_login():
    if request.method == 'POST':
        db = get_db()
        # Parent logs in with student's roll number + parent contact as password
        student = db.execute('SELECT * FROM students WHERE roll_number=? AND contact=?',
            (request.form['roll_number'], request.form['contact'])).fetchone()
        if student:
            session.update({'parent_student_id':student['id'],
                           'parent_student_name':student['name'],
                           'parent_student_class':student['class_name'],
                           'parent_name':student['parent_name'],
                           'role':'parent'})
            return redirect('/parent/dashboard')
        flash('Invalid Roll Number or Contact Number.', 'error')
    return render_template('parent_login.html')

@app.route('/parent/dashboard')
def parent_dashboard():
    if session.get('role') != 'parent': return redirect('/parent/login')
    db  = get_db()
    sid = session['parent_student_id']
    student    = db.execute('SELECT * FROM students WHERE id=?',(sid,)).fetchone()
    marks      = db.execute('SELECT * FROM marks WHERE student_id=? ORDER BY subject',(sid,)).fetchall()
    attendance = db.execute('SELECT * FROM attendance WHERE student_id=? ORDER BY date DESC LIMIT 30',(sid,)).fetchall()
    fees       = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month',(sid,)).fetchall()
    homework   = db.execute('SELECT * FROM homework WHERE class_name=? ORDER BY due_date DESC LIMIT 10',(session['parent_student_class'],)).fetchall()
    notices    = db.execute('SELECT * FROM notices ORDER BY created_at DESC LIMIT 5').fetchall()
    total   = len(attendance)
    present = sum(1 for a in attendance if a['status']=='Present')
    pct     = round((present/total*100) if total else 0,1)
    total_due  = sum(f['total_fee'] for f in fees)
    total_paid = sum(f['paid_amount'] for f in fees)
    return render_template('parent_dashboard.html',
        student=student, marks=marks, attendance=attendance, fees=fees,
        homework=homework, notices=notices,
        attend_pct=pct, total_days=total, present_days=present,
        total_due=total_due, total_paid=total_paid,
        total_remaining=total_due-total_paid)

@app.route('/parent/logout')
def parent_logout():
    session.clear(); return redirect('/')

# ═══════════════════════════════════════════════
# FEATURE 6: LIVE CLASS / VIDEO LINK
# ═══════════════════════════════════════════════

@app.route('/live_classes')
def live_classes():
    db = get_db()
    sel_class = request.args.get('class_name', session.get('student_class', 'All'))
    if sel_class and sel_class != 'All':
        classes_data = db.execute(
            'SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id WHERE lc.class_name=? ORDER BY lc.scheduled_at DESC',
            (sel_class,)).fetchall()
    else:
        classes_data = db.execute(
            'SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id ORDER BY lc.scheduled_at DESC'
        ).fetchall()
    all_classes = ['All', 'UKG'] + [f'Class {i}' for i in range(1, 11)]
    return render_template('live_classes.html', classes_data=classes_data, all_classes=all_classes, sel_class=sel_class)

@app.route('/teacher/live_classes')
def teacher_live_classes():
    if session.get('role') != 'teacher': return redirect('/teacher/login')
    db = get_db()
    my_classes = db.execute(
        'SELECT * FROM live_classes WHERE teacher_id=? ORDER BY scheduled_at DESC',
        (session['teacher_id'],)).fetchall()
    all_classes = ['UKG'] + [f'Class {i}' for i in range(1, 11)]
    subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit','Drawing','Physical Education']
    return render_template('teacher_live_classes.html', my_classes=my_classes, all_classes=all_classes, subjects=subjects)

@app.route('/teacher/add_live_class', methods=['POST'])
def add_live_class():
    if session.get('role') != 'teacher': return jsonify({'error': 'Unauthorized'}), 401
    d = request.json
    db = get_db()
    db.execute(
        'INSERT INTO live_classes (teacher_id,class_name,subject,title,meet_link,platform,scheduled_at,duration,status,description) VALUES (?,?,?,?,?,?,?,?,?,?)',
        (session['teacher_id'], d['class_name'], d['subject'], d['title'],
         d['meet_link'], d['platform'], d['scheduled_at'], d.get('duration', 60),
         'Upcoming', d.get('description', '')))
    db.commit()
    return jsonify({'success': True})

@app.route('/teacher/update_live_class_status', methods=['POST'])
def update_live_class_status():
    if session.get('role') != 'teacher': return jsonify({'error': 'Unauthorized'}), 401
    d = request.json
    db = get_db()
    db.execute('UPDATE live_classes SET status=? WHERE id=? AND teacher_id=?',
               (d['status'], d['id'], session['teacher_id']))
    db.commit()
    return jsonify({'success': True})

@app.route('/teacher/delete_live_class/<int:lcid>', methods=['POST'])
def delete_live_class(lcid):
    if session.get('role') != 'teacher': return jsonify({'error': 'Unauthorized'}), 401
    db = get_db()
    db.execute('DELETE FROM live_classes WHERE id=? AND teacher_id=?', (lcid, session['teacher_id']))
    db.commit()
    return jsonify({'success': True})

@app.route('/api/live_classes')
def api_live_classes():
    db = get_db()
    sel_class = request.args.get('class_name', '')
    if sel_class:
        rows = db.execute(
            '''SELECT lc.*, t.name as teacher_name FROM live_classes lc
               JOIN teachers t ON lc.teacher_id=t.id
               WHERE lc.class_name=? AND lc.status != "Completed"
               ORDER BY lc.status DESC, lc.scheduled_at ASC LIMIT 5''',
            (sel_class,)).fetchall()
    else:
        rows = db.execute(
            '''SELECT lc.*, t.name as teacher_name FROM live_classes lc
               JOIN teachers t ON lc.teacher_id=t.id
               WHERE lc.status != "Completed"
               ORDER BY lc.status DESC, lc.scheduled_at ASC LIMIT 10''').fetchall()
    return jsonify([dict(r) for r in rows])

# ═══════════════════════════════════════════════
# FEATURE: STUDENT ID CARD GENERATOR (PDF)
# ═══════════════════════════════════════════════

@app.route('/admin/id_cards')
def admin_id_cards():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    classes  = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
    sel_class = request.args.get('class_name','All')
    if sel_class == 'All':
        students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id ORDER BY s.class_name, s.roll_number').fetchall()
    else:
        students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id WHERE s.class_name=? ORDER BY s.roll_number', (sel_class,)).fetchall()
    return render_template('admin_id_cards.html', students=students, classes=classes, sel_class=sel_class)

@app.route('/admin/upload_student_photo/<int:sid>', methods=['POST'])
def upload_student_photo(sid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
    file = request.files['photo']
    ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
    if ext not in {'png','jpg','jpeg','webp'}: return jsonify({'error':'Invalid type'}), 400
    fname = f"student_{sid}.{ext}"
    path  = os.path.join(app.root_path,'static','uploads','students',fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path)
    db = get_db()
    db.execute('INSERT INTO student_photos (student_id,filename) VALUES (?,?) ON CONFLICT(student_id) DO UPDATE SET filename=excluded.filename', (sid,fname))
    db.commit()
    return jsonify({'success':True,'filename':fname})

@app.route('/admin/generate_id_card/<int:sid>')
def generate_id_card(sid):
    if session.get('role') != 'admin': return redirect('/admin/login')
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from io import BytesIO
    from flask import make_response

    db = get_db()
    cls_filter = request.args.get('class_name', '')
    if sid == 0:
        if cls_filter:
            students = db.execute('SELECT * FROM students WHERE class_name=? ORDER BY roll_number', (cls_filter,)).fetchall()
        else:
            students = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
    else:
        students = db.execute('SELECT * FROM students WHERE id=?', (sid,)).fetchall()

    if not students:
        flash('No students found.', 'error')
        return redirect('/admin/id_cards')

    NAVY  = colors.HexColor('#0d1b3e')
    GOLD  = colors.HexColor('#c9a84c')
    CREAM = colors.HexColor('#fdf8f0')
    WHITE = colors.white

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=1*cm, leftMargin=1*cm,
                            topMargin=1.5*cm, bottomMargin=1*cm)
    story = []

    title_style = ParagraphStyle('t', fontSize=12, fontName='Helvetica-Bold',
                                 alignment=TA_CENTER, textColor=NAVY, spaceAfter=12)
    story.append(Paragraph('BrightMind School — Student ID Cards 2024-25', title_style))

    CARD_W = 8.5 * cm
    CARD_H = 5.5 * cm

    def make_card(s):
        initial = s['name'][0].upper() if s['name'] else '?'
        # Header row
        hdr = Table([[Paragraph(f'<font color="white" size="7"><b>BRIGHTMIND SCHOOL · CBSE · 2024-25</b></font>',
                                ParagraphStyle('h', alignment=TA_CENTER, fontName='Helvetica-Bold'))]],
                    colWidths=[CARD_W - 0.4*cm], rowHeights=[0.9*cm])
        hdr.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
                                  ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))

        # Photo cell
        photo = Table([[Paragraph(f'<font size="22" color="#c9a84c"><b>{initial}</b></font>',
                                   ParagraphStyle('p', alignment=TA_CENTER))]],
                      colWidths=[1.8*cm], rowHeights=[2.2*cm])
        photo.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),
                                    ('ALIGN',(0,0),(-1,-1),'CENTER'),
                                    ('VALIGN',(0,0),(-1,-1),'MIDDLE')]))

        # Info
        name_p  = Paragraph(f'<font size="9" color="#0d1b3e"><b>{s["name"]}</b></font>',
                             ParagraphStyle('n', fontName='Helvetica-Bold'))
        class_p = Paragraph(f'<font size="8" color="#0d1b3e">Class: <b>{s["class_name"]}</b></font>',
                             ParagraphStyle('c'))
        roll_p  = Paragraph(f'<font size="8" color="#0d1b3e">Roll No: <b>{s["roll_number"]}</b></font>',
                             ParagraphStyle('r'))
        sess_p  = Paragraph(f'<font size="7.5" color="#666">Session: 2024-25</font>',
                             ParagraphStyle('s'))
        info_rows = [[name_p],[class_p],[roll_p],[sess_p]]
        info = Table(info_rows, colWidths=[CARD_W - 2.4*cm],
                     rowHeights=[0.55*cm, 0.5*cm, 0.5*cm, 0.5*cm])
        info.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),2),
                                   ('BOTTOMPADDING',(0,0),(-1,-1),2),
                                   ('LEFTPADDING',(0,0),(-1,-1),6)]))

        body = Table([[photo, info]], colWidths=[1.9*cm, CARD_W - 2.3*cm], rowHeights=[2.4*cm])
        body.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                   ('LEFTPADDING',(0,0),(-1,-1),4),
                                   ('TOPPADDING',(0,0),(-1,-1),8),
                                   ('BOTTOMPADDING',(0,0),(-1,-1),4)]))

        footer = Table([[Paragraph('<font size="6.5" color="#888">Ph: +91 11 1234 5678 | Delhi-110001</font>',
                                    ParagraphStyle('f', alignment=TA_CENTER))]],
                       colWidths=[CARD_W - 0.4*cm], rowHeights=[0.55*cm])
        footer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),CREAM),
                                     ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))

        card = Table([[hdr],[body],[footer]],
                     colWidths=[CARD_W],
                     rowHeights=[0.9*cm, CARD_H - 1.55*cm, 0.65*cm])
        card.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.5,GOLD),
                                   ('TOPPADDING',(0,0),(-1,-1),0),
                                   ('BOTTOMPADDING',(0,0),(-1,-1),0),
                                   ('LEFTPADDING',(0,0),(-1,-1),0),
                                   ('RIGHTPADDING',(0,0),(-1,-1),0)]))
        return card

    # Layout: 2 cards per row
    SPACER_W = 0.8*cm
    pair_w   = [CARD_W + SPACER_W/2, CARD_W + SPACER_W/2]

    i = 0
    while i < len(students):
        row_data = []
        if i < len(students):     row_data.append(make_card(students[i]))
        else:                      row_data.append(Paragraph('', ParagraphStyle('e')))
        if i+1 < len(students):   row_data.append(make_card(students[i+1]))
        else:                      row_data.append(Paragraph('', ParagraphStyle('e')))

        row_tbl = Table([row_data], colWidths=pair_w, rowHeights=[CARD_H + 0.4*cm])
        row_tbl.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                                      ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                      ('TOPPADDING',(0,0),(-1,-1),4),
                                      ('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        story.append(row_tbl)
        i += 2

    doc.build(story)
    pdf  = buffer.getvalue()
    buffer.close()

    name = students[0]['name'] if len(students)==1 else f'{cls_filter or "All"}_Students'
    resp = make_response(pdf)
    resp.headers['Content-Type']        = 'application/pdf'
    resp.headers['Content-Disposition'] = f'attachment; filename=ID_Cards_{name}.pdf'
    return resp


@app.route('/admin/generate_all_id_cards')
def generate_all_id_cards():
    if session.get('role') != 'admin': return redirect('/admin/login')
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from io import BytesIO
    from flask import make_response

    db = get_db()
    cls = request.args.get('class_name','')
    if cls:
        students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id WHERE s.class_name=? ORDER BY s.roll_number',(cls,)).fetchall()
    else:
        students = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id ORDER BY s.class_name, s.roll_number').fetchall()

    NAVY=colors.HexColor('#0d1b3e'); GOLD=colors.HexColor('#c9a84c'); CREAM=colors.HexColor('#fdf8f0')
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=1*cm, rightMargin=1*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    story = []; card_w=8.56*cm; card_h=5.4*cm

    title_s = ParagraphStyle('t',fontSize=14,fontName='Helvetica-Bold',textColor=NAVY,alignment=TA_CENTER,spaceAfter=12)
    story.append(Paragraph(f'BrightMind School — Student ID Cards {"(" + cls + ")" if cls else "(All Classes)"}', title_s))

    cards = []
    for student in students:
        if student['photo']:
            photo_path = os.path.join(app.root_path,'static','uploads','students',student['photo'])
            photo_cell = RLImage(photo_path,width=1.8*cm,height=1.8*cm) if os.path.exists(photo_path) else Paragraph(student['name'][0], ParagraphStyle('i',fontSize=18,fontName='Helvetica-Bold',textColor=GOLD,alignment=TA_CENTER))
        else:
            photo_cell = Paragraph(student['name'][0], ParagraphStyle('i',fontSize=18,fontName='Helvetica-Bold',textColor=GOLD,alignment=TA_CENTER))

        info = Table([
            [Paragraph(f'<b>{student["name"]}</b>', ParagraphStyle('n',fontSize=7.5,fontName='Helvetica-Bold',textColor=NAVY,leading=10))],
            [Paragraph(f'Class: <b>{student["class_name"]}</b>', ParagraphStyle('c',fontSize=6.5,leading=9))],
            [Paragraph(f'Roll: <b>{student["roll_number"]}</b>', ParagraphStyle('r',fontSize=6.5,leading=9))],
            [Paragraph('Session: 2024-25', ParagraphStyle('s',fontSize=6,textColor=colors.HexColor('#555'),leading=8))],
        ], colWidths=[card_w-2.2*cm])
        info.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))

        header = Table([[Paragraph('<font color="white"><b>BRIGHTMIND SCHOOL</b></font>', ParagraphStyle('h',fontSize=6.5,fontName='Helvetica-Bold',alignment=TA_CENTER))]], colWidths=[card_w])
        header.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
        mid = Table([[photo_cell, info]], colWidths=[2*cm, card_w-2*cm])
        mid.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BACKGROUND',(0,0),(-1,-1),CREAM)]))
        footer = Table([[Paragraph(f'📞 {student["contact"] or "—"}', ParagraphStyle('f',fontSize=5.5,textColor=colors.white,alignment=TA_LEFT))]], colWidths=[card_w])
        footer.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),GOLD),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),6)]))

        card = Table([[header],[mid],[footer]], colWidths=[card_w], rowHeights=[0.8*cm,3.8*cm,0.6*cm])
        card.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.5,NAVY),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
        cards.append(card)

    # 2 cards per row
    for i in range(0, len(cards), 2):
        row = cards[i:i+2]
        if len(row) == 1: row.append(Spacer(card_w,card_h))
        story.append(Table([row], colWidths=[card_w+0.5*cm]*2))
        story.append(Spacer(1,0.5*cm))

    doc.build(story)
    pdf=buffer.getvalue(); buffer.close()
    resp=make_response(pdf)
    resp.headers['Content-Type']='application/pdf'
    resp.headers['Content-Disposition']=f'attachment; filename=IDCards_{cls or "All"}.pdf'
    return resp

# ═══════════════════════════════════════════════
# FEATURE: WHATSAPP NOTIFICATION SYSTEM
# ═══════════════════════════════════════════════

@app.route('/admin/notifications')
def admin_notifications():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    logs      = db.execute('SELECT * FROM notifications ORDER BY sent_at DESC LIMIT 50').fetchall()
    students  = db.execute('SELECT s.*, sp.filename as photo FROM students s LEFT JOIN student_photos sp ON s.id=sp.student_id ORDER BY s.class_name').fetchall()
    classes   = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
    pending_fees = db.execute('''SELECT s.name, s.contact, s.class_name, f.fee_month, f.remaining
        FROM fees f JOIN students s ON f.student_id=s.id
        WHERE f.status IN ("Pending","Overdue") AND s.contact IS NOT NULL
        ORDER BY f.status DESC, s.class_name''').fetchall()
    return render_template('admin_notifications.html', logs=logs, students=students, classes=classes, pending_fees=pending_fees)

@app.route('/admin/send_notification', methods=['POST'])
def send_notification():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json
    db = get_db()
    recipients = []
    msg_type = d.get('type','custom')
    message  = d.get('message','')

    if d.get('target') == 'all':
        students = db.execute('SELECT * FROM students WHERE contact IS NOT NULL').fetchall()
        recipients = [(s['name'], s['contact']) for s in students]
    elif d.get('target') == 'class':
        students = db.execute('SELECT * FROM students WHERE class_name=? AND contact IS NOT NULL',(d['class_name'],)).fetchall()
        recipients = [(s['name'], s['contact']) for s in students]
    elif d.get('target') == 'fee_pending':
        rows = db.execute('''SELECT s.name, s.contact, s.class_name, f.fee_month, f.remaining
            FROM fees f JOIN students s ON f.student_id=s.id
            WHERE f.status IN ("Pending","Overdue") AND s.contact IS NOT NULL''').fetchall()
        for r in rows:
            msg = f"Dear Parent of {r['name']} ({r['class_name']}), Fee of ₹{int(r['remaining'])} for {r['fee_month']} is pending. Please pay at earliest. — BrightMind School"
            recipients.append((r['name'], r['contact'], msg))
    elif d.get('student_id'):
        s = db.execute('SELECT * FROM students WHERE id=?',(d['student_id'],)).fetchone()
        if s and s['contact']:
            recipients = [(s['name'], s['contact'])]

    sent = 0
    for rec in recipients:
        name    = rec[0]
        contact = rec[1]
        custom_msg = rec[2] if len(rec) > 2 else message.replace('{name}', name)

        # Generate WhatsApp link (wa.me) — simulated
        wa_link = f"https://wa.me/91{contact}?text={custom_msg.replace(' ','%20')}"

        db.execute('INSERT INTO notifications (type,recipient,message,status) VALUES (?,?,?,?)',
                   (msg_type, f"{name} ({contact})", custom_msg[:200], "Sent (WA Link)"))
        sent += 1

    db.commit()
    return jsonify({'success':True, 'sent':sent})

# ═══════════════════════════════════════════════
# FEATURE: ONLINE TEST / QUIZ
# ═══════════════════════════════════════════════

@app.route('/teacher/quizzes')

def teacher_quizzes():
    if session.get('role') != 'teacher': return redirect('/teacher/login')
    db = get_db()
    quizzes = db.execute('SELECT q.*, COUNT(qq.id) as q_count FROM quizzes q LEFT JOIN quiz_questions qq ON q.id=qq.quiz_id WHERE q.teacher_id=? GROUP BY q.id ORDER BY q.created_at DESC',(session['teacher_id'],)).fetchall()
    classes  = ['UKG'] + [f'Class {i}' for i in range(1,11)]
    subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit']
    return render_template('teacher_quizzes.html', quizzes=quizzes, classes=classes, subjects=subjects)

@app.route('/teacher/create_quiz', methods=['POST'])
def create_quiz():
    if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    cur = db.execute('INSERT INTO quizzes (teacher_id,title,class_name,subject,duration,total_marks,status) VALUES (?,?,?,?,?,?,?)',
        (session['teacher_id'],d['title'],d['class_name'],d['subject'],d.get('duration',30),d.get('total_marks',10),'Draft'))
    qid = cur.lastrowid
    for q in d.get('questions',[]):
        db.execute('INSERT INTO quiz_questions (quiz_id,question,option_a,option_b,option_c,option_d,correct,marks) VALUES (?,?,?,?,?,?,?,?)',
            (qid,q['question'],q['a'],q['b'],q['c'],q['d'],q['correct'],q.get('marks',1)))
    db.commit()
    return jsonify({'success':True,'quiz_id':qid})

@app.route('/teacher/publish_quiz/<int:qid>', methods=['POST'])
def publish_quiz(qid):
    if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    db.execute("UPDATE quizzes SET status='Active' WHERE id=? AND teacher_id=?",(qid,session['teacher_id']))
    db.commit(); return jsonify({'success':True})

@app.route('/teacher/quiz_results/<int:qid>')
def quiz_results(qid):
    if session.get('role') != 'teacher': return redirect('/teacher/login')
    db = get_db()
    quiz    = db.execute('SELECT * FROM quizzes WHERE id=?',(qid,)).fetchone()
    results = db.execute('SELECT qa.*, s.name, s.roll_number FROM quiz_attempts qa JOIN students s ON qa.student_id=s.id WHERE qa.quiz_id=? ORDER BY qa.score DESC',(qid,)).fetchall()
    return render_template('quiz_results.html', quiz=quiz, results=results)

@app.route('/student/quizzes')
def student_quizzes():
    if session.get('role') != 'student': return redirect('/student/login')
    db = get_db()
    sid = session['student_id']
    quizzes = db.execute('''SELECT q.*, t.name as teacher_name,
        (SELECT score FROM quiz_attempts WHERE quiz_id=q.id AND student_id=?) as my_score,
        (SELECT submitted_at FROM quiz_attempts WHERE quiz_id=q.id AND student_id=?) as attempted_at
        FROM quizzes q JOIN teachers t ON q.teacher_id=t.id
        WHERE q.class_name=? AND q.status="Active" ORDER BY q.created_at DESC''',(sid,sid,session['student_class'])).fetchall()
    return render_template('student_quizzes.html', quizzes=quizzes)

@app.route('/student/attempt_quiz/<int:qid>')
def attempt_quiz(qid):
    if session.get('role') != 'student': return redirect('/student/login')
    db = get_db()
    sid = session['student_id']
    attempted = db.execute('SELECT id FROM quiz_attempts WHERE quiz_id=? AND student_id=?',(qid,sid)).fetchone()
    if attempted: return redirect('/student/quiz_result/'+str(qid))
    quiz      = db.execute('SELECT * FROM quizzes WHERE id=? AND status="Active"',(qid,)).fetchone()
    questions = db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
    if not quiz: return redirect('/student/quizzes')
    return render_template('attempt_quiz.html', quiz=quiz, questions=questions)

@app.route('/student/submit_quiz/<int:qid>', methods=['POST'])
def submit_quiz(qid):
    if session.get('role') != 'student': return jsonify({'error':'Unauthorized'}), 401
    d = request.json; db = get_db()
    sid = session['student_id']
    questions = db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
    score = 0; answers = {}
    for q in questions:
        ans = d.get(str(q['id']),'')
        answers[q['id']] = ans
        if ans.upper() == q['correct'].upper():
            score += q['marks']
    import json as json_lib
    db.execute('INSERT OR IGNORE INTO quiz_attempts (quiz_id,student_id,score,total,answers) VALUES (?,?,?,?,?)',
               (qid,sid,score,len(questions),json_lib.dumps(answers)))
    db.commit()
    return jsonify({'success':True,'score':score,'total':len(questions)})

@app.route('/student/quiz_result/<int:qid>')
def student_quiz_result(qid):
    if session.get('role') != 'student': return redirect('/student/login')
    db = get_db()
    sid = session['student_id']
    quiz     = db.execute('SELECT q.*, t.name as teacher_name FROM quizzes q JOIN teachers t ON q.teacher_id=t.id WHERE q.id=?',(qid,)).fetchone()
    attempt  = db.execute('SELECT * FROM quiz_attempts WHERE quiz_id=? AND student_id=?',(qid,sid)).fetchone()
    questions= db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
    import json as json_lib
    answers  = json_lib.loads(attempt['answers']) if attempt and attempt['answers'] else {}
    return render_template('quiz_result.html', quiz=quiz, attempt=attempt, questions=questions, answers=answers)

# ═══════════════════════════════════════════════
# FEATURE: STUDENT ACHIEVEMENTS / AWARDS
# ═══════════════════════════════════════════════


@app.route('/achievers')
@app.route('/achievements')
def achievers_page():
    db = get_db()

    sel_cat = request.args.get('category', 'All')

    items = db.execute("""
        SELECT * FROM achievements
        WHERE class_name IN ('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')
        ORDER BY class_name, achievement_date DESC
    """).fetchall()

    # categories
    cats_raw = db.execute("SELECT DISTINCT category FROM achievements").fetchall()
    cats = [r['category'] for r in cats_raw]

    # filter
    if sel_cat != 'All':
        items = [i for i in items if i['category'] == sel_cat]

    # return render_template('admin_achievements.html', achievements=ach, students=students)



@app.route('/achievements')
def admin_achievements():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    ach      = db.execute('SELECT *, COALESCE(student_name,"") as student_name FROM achievements ORDER BY created_at DESC').fetchall()
    students = db.execute('SELECT id, name, class_name FROM students ORDER BY class_name, name').fetchall()
    return render_template('admin_achievements.html', achievements=ach, students=students)

@app.route('/admin/add_achievement', methods=['POST'])
def add_achievement():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    sid        = request.form.get('student_id') or None
    sname      = request.form.get('student_name','').strip()
    cls        = request.form.get('class_name','')
    # If student selected from dropdown, get their name and class
    if sid:
        s = db.execute('SELECT name, class_name FROM students WHERE id=?',(sid,)).fetchone()
        if s:
            sname = s['name']
            cls   = s['class_name']
    # Handle photo upload
    photo = None
    if 'photo' in request.files and request.files['photo'].filename:
        file = request.files['photo']
        ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
        if ext in {'jpg','jpeg','png','gif','webp'}:
            fname = f"ach_{uuid.uuid4().hex[:8]}.{ext}"
            path  = os.path.join(app.root_path,'static','uploads','achievements',fname)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            file.save(path)
            photo = fname
    db.execute('''INSERT INTO achievements
        (student_id,student_name,class_name,title,category,description,achievement_date,is_featured,photo)
        VALUES (?,?,?,?,?,?,?,?,?)''',
        (sid, sname, cls,
         request.form.get('title',''),
         request.form.get('category','Academic'),
         request.form.get('description',''),
         request.form.get('achievement_date',''),
         1 if request.form.get('is_featured') else 0,
         photo))
    db.commit()
    flash('Achievement added!','success')
    return redirect('/admin/achievements')

@app.route('/achievers/<int:aid>')
def achiever_detail(aid):
    db = get_db()

    # current achiever
    item = db.execute("""
        SELECT * FROM achievements WHERE id=?
    """, (aid,)).fetchone()

    if not item:
        return "Not Found", 404

    # same class ke aur achievers
    others = db.execute("""
        SELECT * FROM achievements 
        WHERE class_name=? AND id!=?
        LIMIT 4
    """, (item['class_name'], aid)).fetchall()

    return render_template('achiever_detail.html', item=item, others=others)




@app.route('/admin/delete_achievement/<int:aid>', methods=['POST'])
def delete_achievement(aid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    db.execute('DELETE FROM achievements WHERE id=?',(aid,)); db.commit()
    return jsonify({'success':True})

@app.route('/admin/toggle_featured/<int:aid>', methods=['POST'])
def toggle_featured(aid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    cur = db.execute('SELECT is_featured FROM achievements WHERE id=?',(aid,)).fetchone()
    db.execute('UPDATE achievements SET is_featured=? WHERE id=?',(0 if cur['is_featured'] else 1, aid)); db.commit()
    return jsonify({'success':True})

# ═══════════════════════════════════════════════
# FEATURE 7: ONLINE QUIZ / TEST
# ═══════════════════════════════════════════════

@app.route('/student/quizzes')
@app.route('/student/quiz/<int:qid>')
@app.route('/student/quiz/<int:qid>/submit', methods=['POST'])
@app.route('/teacher/quizzes')
@app.route('/teacher/quiz/create', methods=['POST'])
@app.route('/teacher/quiz/<int:qid>/toggle', methods=['POST'])
def toggle_quiz(qid):
    if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    q  = db.execute('SELECT status FROM quizzes WHERE id=? AND teacher_id=?',(qid,session['teacher_id'])).fetchone()
    if not q: return jsonify({'error':'Not found'}), 404
    new_status = 'Active' if q['status']=='Draft' else 'Draft'
    db.execute('UPDATE quizzes SET status=? WHERE id=?',(new_status,qid))
    db.commit()
    return jsonify({'success':True,'status':new_status})

@app.route('/teacher/quiz/<int:qid>/results')
@app.route('/teacher/quiz/<int:qid>/delete', methods=['POST'])
def delete_quiz(qid):
    if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    db.execute('DELETE FROM quiz_attempts WHERE quiz_id=?',(qid,))
    db.execute('DELETE FROM quiz_questions WHERE quiz_id=?',(qid,))
    db.execute('DELETE FROM quizzes WHERE id=? AND teacher_id=?',(qid,session['teacher_id']))
    db.commit()
    return jsonify({'success':True})

# ═══════════════════════════════════════════════
# FEATURE 9: ACHIEVEMENTS / AWARDS
# ═══════════════════════════════════════════════

# ═══════════════════════════════════════════════
# FEATURE 10: STUDENT ID CARD PDF GENERATOR
# ═══════════════════════════════════════════════

# ═══════════════════════════════════════════════
# FEATURE 2: WHATSAPP NOTIFICATION (Simulation)
# ═══════════════════════════════════════════════




# ═══════════════════════════════════════════════
# ADMIN — Live Classes Management
# ═══════════════════════════════════════════════

@app.route('/admin/live_classes')
def admin_live_classes():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    classes_data = db.execute('''
        SELECT lc.*, t.name as teacher_name
        FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id
        ORDER BY lc.status ASC, lc.scheduled_at DESC
    ''').fetchall()
    teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
    all_classes = ['UKG'] + [f'Class {i}' for i in range(1, 11)]
    subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit','Drawing','Physical Education']
    # Stats
    stats = {
        'total':     len(classes_data),
        'live':      sum(1 for lc in classes_data if lc['status']=='Live'),
        'upcoming':  sum(1 for lc in classes_data if lc['status']=='Upcoming'),
        'completed': sum(1 for lc in classes_data if lc['status']=='Completed'),
    }
    return render_template('admin_live_classes.html',
        classes_data=classes_data, teachers=teachers,
        all_classes=all_classes, subjects=subjects, stats=stats)

@app.route('/admin/live_classes/add', methods=['POST'])
def admin_add_live_class():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json
    db = get_db()
    db.execute('''INSERT INTO live_classes
        (teacher_id,class_name,subject,title,meet_link,platform,scheduled_at,duration,status,description)
        VALUES (?,?,?,?,?,?,?,?,?,?)''',
        (d['teacher_id'], d['class_name'], d['subject'], d['title'],
         d['meet_link'], d['platform'], d['scheduled_at'],
         d.get('duration',60), d.get('status','Upcoming'), d.get('description','')))
    db.commit()
    return jsonify({'success': True})

@app.route('/admin/live_classes/update_status', methods=['POST'])
def admin_update_live_status():
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    d = request.json
    db = get_db()
    db.execute('UPDATE live_classes SET status=? WHERE id=?', (d['status'], d['id']))
    db.commit()
    return jsonify({'success': True})

@app.route('/admin/live_classes/delete/<int:lcid>', methods=['POST'])
def admin_delete_live_class(lcid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    db.execute('DELETE FROM live_classes WHERE id=?', (lcid,))
    db.commit()
    return jsonify({'success': True})

# ═══════════════════════════════════════════════
# ADMIN QUIZ MANAGER
# ═══════════════════════════════════════════════









# ── ADMIN QUIZ MANAGER ─────────────────────────────────────────
@app.route('/admin/quiz_manager')
def admin_quiz_manager():
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    quizzes = db.execute("""
        SELECT q.*, t.name as teacher_name,
               COUNT(qa.id) as attempt_count,
               AVG(CASE WHEN qa.total > 0 THEN qa.score*100.0/qa.total END) as avg_score
        FROM quizzes q
        LEFT JOIN teachers t ON q.teacher_id=t.id
        LEFT JOIN quiz_attempts qa ON q.id=qa.quiz_id
        GROUP BY q.id ORDER BY q.created_at DESC
    """).fetchall()
    return render_template('admin_quiz_manager.html', quizzes=quizzes)

@app.route('/admin/quiz/toggle/<int:qid>', methods=['POST'])
def admin_toggle_quiz(qid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    q  = db.execute('SELECT status FROM quizzes WHERE id=?',(qid,)).fetchone()
    if not q: return jsonify({'error':'Not found'}), 404
    new_status = 'Active' if q['status']=='Draft' else 'Draft'
    db.execute('UPDATE quizzes SET status=? WHERE id=?',(new_status,qid)); db.commit()
    return jsonify({'success':True,'status':new_status})

@app.route('/admin/quiz/delete/<int:qid>', methods=['POST'])
def admin_delete_quiz(qid):
    if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
    db = get_db()
    db.execute('DELETE FROM quiz_attempts WHERE quiz_id=?',(qid,))
    db.execute('DELETE FROM quiz_questions WHERE quiz_id=?',(qid,))
    db.execute('DELETE FROM quizzes WHERE id=?',(qid,)); db.commit()
    return jsonify({'success':True})

@app.route('/admin/quiz/<int:qid>/results')
def admin_quiz_results(qid):
    if session.get('role') != 'admin': return redirect('/admin/login')
    db = get_db()
    quiz     = db.execute('SELECT q.*,t.name as tname FROM quizzes q LEFT JOIN teachers t ON q.teacher_id=t.id WHERE q.id=?',(qid,)).fetchone()
    results  = db.execute('SELECT qa.*,s.name as student_name,s.roll_number,s.class_name FROM quiz_attempts qa JOIN students s ON qa.student_id=s.id WHERE qa.quiz_id=? ORDER BY qa.score DESC',(qid,)).fetchall()
    questions= db.execute('SELECT COUNT(*) FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchone()[0]
    return render_template('admin_quiz_results.html', quiz=quiz, results=results, question_count=questions)



if __name__ == "__main__":
    app.run(debug=True, port=5000)








# from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
# from database.db import init_db, get_db
# import os, uuid

# app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET_KEY', 'brightmind_school_2024_secret')

# with app.app_context():
#     init_db()

# # ═══════════════════════════════════════════════
# # PUBLIC ROUTES
# # ═══════════════════════════════════════════════

# @app.route('/')
# def home():
#     db = get_db()
#     notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC LIMIT 4').fetchall()
#     achievers = {}
#     for cls in ['Class 5','Class 6','Class 7','Class 8','Class 9','Class 10']:
#         rows = db.execute(
#             "SELECT *, COALESCE(student_name,'') as student_name FROM achievements WHERE class_name=? ORDER BY achievement_date DESC LIMIT 2",
#             (cls,)
#         ).fetchall()
#         if rows:
#             achievers[cls] = rows
#     return render_template('home.html', notices=notices, achievers=achievers)

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/admissions', methods=['GET','POST'])
# def admissions():
#     if request.method == 'POST':
#         db = get_db()
#         db.execute('INSERT INTO admissions (name,dob,class_name,parent_name,contact,email,address,status) VALUES (?,?,?,?,?,?,?,?)',
#             (request.form['name'], request.form['dob'], request.form['class_name'],
#              request.form['parent_name'], request.form['contact'], request.form['email'],
#              request.form['address'], 'Pending'))
#         db.commit()
#         flash('Admission form submitted! We will contact you soon.', 'success')
#         return redirect('/admissions')
#     return render_template('admissions.html')

# @app.route('/academics')
# def academics():
#     return render_template('academics.html')

# @app.route('/notices')
# def notices():
#     db = get_db()
#     all_notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC').fetchall()
#     return render_template('notices.html', notices=all_notices)

# @app.route('/contact', methods=['GET','POST'])
# def contact():
#     if request.method == 'POST':
#         db = get_db()
#         db.execute('INSERT INTO contact_messages (name,email,subject,message) VALUES (?,?,?,?)',
#             (request.form['name'], request.form['email'], request.form['subject'], request.form['message']))
#         db.commit()
#         flash('Message sent! We will reply shortly.', 'success')
#         return redirect('/contact')
#     return render_template('contact.html')

# @app.route('/teachers')
# def teachers_list():
#     db = get_db()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     return render_template('teachers.html', teachers=teachers)

# @app.route('/teachers/<int:teacher_id>')
# def teacher_profile(teacher_id):
#     db = get_db()
#     teacher = db.execute('SELECT * FROM teachers WHERE id=?', (teacher_id,)).fetchone()
#     if not teacher:
#         flash('Teacher not found.','error')
#         return redirect('/teachers')
#     assignments = db.execute(
#         'SELECT class_name, subject FROM teacher_assignments WHERE teacher_id=? ORDER BY class_name',
#         (teacher_id,)).fetchall()
#     return render_template('teacher_profile.html', teacher=teacher, assignments=assignments)

# @app.route('/gallery')
# def gallery():
#     db = get_db()
#     sel_cat = request.args.get('category','All')
#     if sel_cat == 'All':
#         photos = db.execute('SELECT * FROM gallery_photos ORDER BY uploaded_at DESC').fetchall()
#     else:
#         photos = db.execute('SELECT * FROM gallery_photos WHERE category=? ORDER BY uploaded_at DESC',(sel_cat,)).fetchall()
#     categories = db.execute('SELECT DISTINCT category FROM gallery_photos ORDER BY category').fetchall()
#     return render_template('gallery.html', photos=photos, categories=categories, sel_cat=sel_cat)

# @app.route('/timetable')
# def timetable():
#     db = get_db()
#     classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name', session.get('student_class','Class 5'))
#     days      = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
#     periods   = list(range(1,7))
#     rows = db.execute('SELECT * FROM timetable WHERE class_name=? ORDER BY day, period',(sel_class,)).fetchall()
#     tt = {day:{} for day in days}
#     for r in rows: tt[r['day']][r['period']] = r
#     period_times = {1:'8:00-8:45',2:'8:45-9:30',3:'9:30-10:15',
#                     4:'10:30-11:15',5:'11:15-12:00',6:'12:00-12:45'}
#     return render_template('timetable.html',
#         classes=classes, sel_class=sel_class, days=days,
#         periods=periods, tt=tt, period_times=period_times)

# @app.route('/exam_schedule')
# def exam_schedule():
#     db = get_db()
#     exams = db.execute('SELECT * FROM exam_schedule ORDER BY exam_date, class_name').fetchall()
#     classes = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','All')
#     if sel_class != 'All':
#         exams = [e for e in exams if e['class_name']==sel_class]
#     return render_template('exam_schedule.html', exams=exams, classes=classes, sel_class=sel_class)

# @app.route('/live_classes')
# def live_classes():
#     db = get_db()
#     sel_cat = request.args.get('class_name','All')
#     if sel_cat and sel_cat != 'All':
#         classes_data = db.execute(
#             'SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id WHERE lc.class_name=? ORDER BY lc.scheduled_at DESC',
#             (sel_cat,)).fetchall()
#     else:
#         classes_data = db.execute(
#             'SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id ORDER BY lc.scheduled_at DESC'
#         ).fetchall()
#     all_classes = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     return render_template('live_classes.html', classes_data=classes_data, all_classes=all_classes, sel_class=sel_cat)

# @app.route('/api/live_classes')
# def api_live_classes():
#     db = get_db()
#     sel_class = request.args.get('class_name','')
#     if sel_class:
#         rows = db.execute(
#             "SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id WHERE lc.class_name=? AND lc.status != 'Completed' ORDER BY lc.status DESC, lc.scheduled_at ASC LIMIT 5",
#             (sel_class,)).fetchall()
#     else:
#         rows = db.execute(
#             "SELECT lc.*, t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id WHERE lc.status != 'Completed' ORDER BY lc.status DESC, lc.scheduled_at ASC LIMIT 10"
#         ).fetchall()
#     return jsonify([dict(r) for r in rows])

# @app.route('/achievements')
# def achievements():
#     db = get_db()
#     sel_cat = request.args.get('category','All')
#     sel_cls = request.args.get('class_name','All')
#     query   = "SELECT *, COALESCE(student_name,'') as student_name FROM achievements WHERE 1=1"
#     params  = []
#     if sel_cat != 'All': query += ' AND category=?'; params.append(sel_cat)
#     if sel_cls != 'All': query += ' AND class_name=?'; params.append(sel_cls)
#     query += ' ORDER BY achievement_date DESC'
#     items    = db.execute(query, params).fetchall()
#     cats     = db.execute('SELECT DISTINCT category FROM achievements ORDER BY category').fetchall()
#     classes  = db.execute('SELECT DISTINCT class_name FROM achievements ORDER BY class_name').fetchall()
#     featured = db.execute("SELECT *, COALESCE(student_name,'') as student_name FROM achievements ORDER BY achievement_date DESC LIMIT 3").fetchall()
#     return render_template('achievements.html', items=items, cats=cats, sel_cat=sel_cat,
#                            sel_cls=sel_cls, classes=classes, featured=featured)

# @app.route('/achievers')
# def achievers_page():
#     db      = get_db()
#     sel_cat = request.args.get('category','All')
#     sel_cls = request.args.get('class_name','All')
#     classes = ['Class 5','Class 6','Class 7','Class 8','Class 9','Class 10']
#     query   = "SELECT *, COALESCE(student_name,'') as student_name FROM achievements WHERE class_name IN ('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')"
#     params  = []
#     if sel_cat != 'All': query += ' AND category=?'; params.append(sel_cat)
#     if sel_cls != 'All': query += ' AND class_name=?'; params.append(sel_cls)
#     query += ' ORDER BY achievement_date DESC'
#     items    = db.execute(query, params).fetchall()
#     cats_raw = db.execute("SELECT DISTINCT category FROM achievements WHERE class_name IN ('Class 5','Class 6','Class 7','Class 8','Class 9','Class 10')").fetchall()
#     cats     = [r['category'] for r in cats_raw]
#     class_counts = {}
#     for cls in classes:
#         n = db.execute('SELECT COUNT(*) FROM achievements WHERE class_name=?',(cls,)).fetchone()[0]
#         if n > 0: class_counts[cls] = n
#     return render_template('achievers.html', items=items, cats=cats,
#                            sel_cat=sel_cat, sel_cls=sel_cls,
#                            classes=classes, class_counts=class_counts)

# @app.route('/achievers/<int:aid>')
# def achiever_detail(aid):
#     db   = get_db()
#     item = db.execute("SELECT *, COALESCE(student_name,'') as student_name FROM achievements WHERE id=?", (aid,)).fetchone()
#     if not item:
#         flash('Not found.','error'); return redirect('/achievers')
#     others = db.execute(
#         "SELECT *, COALESCE(student_name,'') as student_name FROM achievements WHERE class_name=? AND id!=? ORDER BY achievement_date DESC LIMIT 4",
#         (item['class_name'], aid)).fetchall()
#     return render_template('achiever_detail.html', item=item, others=others)

# # ═══════════════════════════════════════════════
# # STUDENT PORTAL
# # ═══════════════════════════════════════════════

# @app.route('/student/login', methods=['GET','POST'])
# def student_login():
#     if request.method == 'POST':
#         db = get_db()
#         s = db.execute('SELECT * FROM students WHERE roll_number=? AND password=?',
#             (request.form['roll_number'], request.form['password'])).fetchone()
#         if s:
#             session.update({'student_id':s['id'],'student_name':s['name'],'student_class':s['class_name'],'role':'student'})
#             return redirect('/student/dashboard')
#         flash('Invalid credentials.','error')
#     return render_template('student_login.html')

# @app.route('/student/dashboard')
# def student_dashboard():
#     if session.get('role') != 'student': return redirect('/student/login')
#     db  = get_db()
#     sid = session['student_id']
#     marks      = db.execute('SELECT * FROM marks WHERE student_id=?',(sid,)).fetchall()
#     attendance = db.execute('SELECT * FROM attendance WHERE student_id=? ORDER BY date DESC LIMIT 30',(sid,)).fetchall()
#     homework   = db.execute('SELECT * FROM homework WHERE class_name=? ORDER BY due_date DESC',(session['student_class'],)).fetchall()
#     fees       = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month',(sid,)).fetchall()
#     total   = len(attendance)
#     present = sum(1 for a in attendance if a['status']=='Present')
#     pct     = round((present/total*100) if total else 0, 1)
#     return render_template('student_dashboard.html',
#         marks=marks, attendance=attendance, homework=homework, fees=fees,
#         attend_pct=pct, total_days=total, present_days=present)

# @app.route('/student/report_card')
# def student_report_card():
#     if session.get('role') != 'student': return redirect('/student/login')
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib import colors
#     from reportlab.lib.units import cm
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
#     from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#     from reportlab.lib.enums import TA_CENTER
#     from io import BytesIO
#     db  = get_db()
#     sid = session['student_id']
#     student  = db.execute('SELECT * FROM students WHERE id=?',(sid,)).fetchone()
#     marks    = db.execute('SELECT * FROM marks WHERE student_id=? ORDER BY subject',(sid,)).fetchall()
#     attendance = db.execute('SELECT * FROM attendance WHERE student_id=?',(sid,)).fetchall()
#     total   = len(attendance)
#     present = sum(1 for a in attendance if a['status']=='Present')
#     att_pct = round((present/total*100) if total else 0, 1)
#     buffer = BytesIO()
#     doc    = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
#     NAVY   = colors.HexColor('#0d1b3e')
#     GOLD   = colors.HexColor('#c9a84c')
#     CREAM  = colors.HexColor('#fdf8f0')
#     GREEN  = colors.HexColor('#2e7d32')
#     story  = []
#     styles = getSampleStyleSheet()
#     title_style = ParagraphStyle('t', fontSize=14, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=NAVY, spaceBefore=4, spaceAfter=4)
#     story.append(Paragraph('BRIGHTMIND SCHOOL — REPORT CARD', title_style))
#     story.append(Paragraph('Academic Year: 2024–25', ParagraphStyle('ay', fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#777'))))
#     story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=10))
#     info_data = [
#         ['Student Name:', student['name'], 'Roll Number:', student['roll_number']],
#         ['Class:', student['class_name'], 'Attendance:', f"{att_pct}% ({present}/{total} days)"],
#     ]
#     info_tbl = Table(info_data, colWidths=[3.5*cm,5*cm,3.5*cm,5*cm])
#     info_tbl.setStyle(TableStyle([
#         ('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTNAME',(2,0),(2,-1),'Helvetica-Bold'),
#         ('FONTSIZE',(0,0),(-1,-1),9),('BACKGROUND',(0,0),(-1,-1),CREAM),
#         ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#ddd')),
#         ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LEFTPADDING',(0,0),(-1,-1),8),
#     ]))
#     story.append(info_tbl); story.append(Spacer(1,14))
#     if marks:
#         marks_header = [['S.No.','Subject','Exam Type','Marks','Max','%','Grade']]
#         marks_rows   = []
#         total_m = total_max = 0
#         for i, m in enumerate(marks, 1):
#             pct   = round(m['marks']/m['max_marks']*100,1) if m['max_marks'] else 0
#             grade = 'A1' if pct>=90 else 'A2' if pct>=80 else 'B1' if pct>=70 else 'B2' if pct>=60 else 'C1' if pct>=50 else 'D'
#             total_m += m['marks']; total_max += m['max_marks']
#             marks_rows.append([str(i), m['subject'], m['exam_type'], str(int(m['marks'])), str(int(m['max_marks'])), f"{pct}%", grade])
#         overall_pct = round(total_m/total_max*100,1) if total_max else 0
#         marks_rows.append(['','TOTAL','', str(int(total_m)), str(int(total_max)), f"{overall_pct}%",
#                            'A1' if overall_pct>=90 else 'A2' if overall_pct>=80 else 'B1' if overall_pct>=70 else 'B2' if overall_pct>=60 else 'C1'])
#         all_rows = marks_header + marks_rows
#         marks_tbl = Table(all_rows, colWidths=[1*cm,4.5*cm,3*cm,2*cm,2*cm,2*cm,2*cm])
#         marks_tbl.setStyle(TableStyle([
#             ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
#             ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8.5),
#             ('ALIGN',(0,0),(-1,-1),'CENTER'),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#ccc')),
#             ('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,CREAM]),
#             ('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#e8f5e9')),
#             ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
#         ]))
#         story.append(marks_tbl)
#     doc.build(story)
#     pdf = buffer.getvalue(); buffer.close()
#     response = make_response(pdf)
#     response.headers['Content-Type']        = 'application/pdf'
#     response.headers['Content-Disposition'] = f'attachment; filename=ReportCard_{student["roll_number"]}.pdf'
#     return response

# @app.route('/student/quizzes')
# def student_quizzes():
#     if session.get('role') != 'student': return redirect('/student/login')
#     db  = get_db()
#     sid = session['student_id']
#     quizzes = db.execute('''
#         SELECT q.*, t.name as teacher_name,
#                (SELECT score FROM quiz_attempts WHERE quiz_id=q.id AND student_id=?) as my_score,
#                (SELECT submitted_at FROM quiz_attempts WHERE quiz_id=q.id AND student_id=?) as attempted_at
#         FROM quizzes q JOIN teachers t ON q.teacher_id=t.id
#         WHERE q.class_name=? ORDER BY q.created_at DESC
#     ''', (sid, sid, session['student_class'])).fetchall()
#     return render_template('student_quizzes.html', quizzes=quizzes)

# @app.route('/student/quiz/<int:qid>')
# def attempt_quiz(qid):
#     if session.get('role') != 'student': return redirect('/student/login')
#     db  = get_db()
#     sid = session['student_id']
#     quiz = db.execute('SELECT * FROM quizzes WHERE id=?',(qid,)).fetchone()
#     if not quiz: return redirect('/student/quizzes')
#     already = db.execute('SELECT * FROM quiz_attempts WHERE quiz_id=? AND student_id=?',(qid,sid)).fetchone()
#     if already: flash('Already attempted!','error'); return redirect('/student/quizzes')
#     if quiz['status'] != 'Active': flash('Quiz not active.','error'); return redirect('/student/quizzes')
#     questions = db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
#     return render_template('attempt_quiz.html', quiz=quiz, questions=questions)

# @app.route('/student/quiz/<int:qid>/submit', methods=['POST'])
# def submit_quiz(qid):
#     if session.get('role') != 'student': return redirect('/student/login')
#     db  = get_db()
#     sid = session['student_id']
#     already = db.execute('SELECT id FROM quiz_attempts WHERE quiz_id=? AND student_id=?',(qid,sid)).fetchone()
#     if already: return jsonify({'error':'Already submitted'}), 400
#     questions = db.execute('SELECT * FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchall()
#     answers   = request.json
#     score = 0; total = sum(q['marks'] for q in questions)
#     import json
#     result_detail = {}
#     for q in questions:
#         given = answers.get(str(q['id']),'')
#         correct = q['correct_ans']
#         if given == correct: score += q['marks']
#         result_detail[str(q['id'])] = {'given':given,'correct':correct,'got':q['marks'] if given==correct else 0}
#     db.execute('INSERT INTO quiz_attempts (quiz_id,student_id,score,total,answers) VALUES (?,?,?,?,?)',
#                (qid,sid,score,total,json.dumps(result_detail)))
#     db.commit()
#     return jsonify({'success':True,'score':score,'total':total,'pct':round(score/total*100,1) if total else 0})

# @app.route('/student/logout')
# def student_logout():
#     session.clear(); return redirect('/')

# # ═══════════════════════════════════════════════
# # TEACHER PORTAL
# # ═══════════════════════════════════════════════

# @app.route('/teacher/login', methods=['GET','POST'])
# def teacher_login():
#     if request.method == 'POST':
#         db = get_db()
#         t = db.execute('SELECT * FROM teachers WHERE username=? AND password=?',
#             (request.form['username'], request.form['password'])).fetchone()
#         if t:
#             session.update({'teacher_id':t['id'],'teacher_name':t['name'],'teacher_sub':t['subject'],'role':'teacher'})
#             return redirect('/teacher/dashboard')
#         flash('Invalid credentials.','error')
#     return render_template('teacher_login.html')

# @app.route('/teacher/dashboard')
# def teacher_dashboard():
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     classes  = db.execute('SELECT DISTINCT class_name FROM students ORDER BY class_name').fetchall()
#     students = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
#     homework = db.execute('SELECT h.*,t.name as tname FROM homework h JOIN teachers t ON h.teacher_id=t.id ORDER BY due_date DESC').fetchall()
#     return render_template('teacher_dashboard.html', classes=classes, students=students, homework=homework)

# @app.route('/teacher/upload_marks', methods=['POST'])
# def upload_marks():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('INSERT OR REPLACE INTO marks (student_id,subject,marks,max_marks,exam_type) VALUES (?,?,?,?,?)',
#         (d['student_id'],d['subject'],d['marks'],d['max_marks'],d['exam_type']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/attendance', methods=['POST'])
# def mark_attendance():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     for r in d['records']:
#         db.execute('INSERT OR REPLACE INTO attendance (student_id,date,status) VALUES (?,?,?)',
#             (r['student_id'],d['date'],r['status']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/upload_homework', methods=['POST'])
# def upload_homework():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('INSERT INTO homework (class_name,subject,description,due_date,teacher_id) VALUES (?,?,?,?,?)',
#         (d['class_name'],d['subject'],d['description'],d['due_date'],session['teacher_id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/quizzes')
# def teacher_quizzes():
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     quizzes = db.execute('''
#         SELECT q.*, COUNT(qa.id) as attempt_count, AVG(qa.score*100.0/qa.total) as avg_score
#         FROM quizzes q LEFT JOIN quiz_attempts qa ON q.id=qa.quiz_id
#         WHERE q.teacher_id=? GROUP BY q.id ORDER BY q.created_at DESC
#     ''', (session['teacher_id'],)).fetchall()
#     classes  = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit']
#     return render_template('teacher_quizzes.html', quizzes=quizzes, classes=classes, subjects=subjects)

# @app.route('/teacher/quiz/create', methods=['POST'])
# def create_quiz():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     cur = db.execute('INSERT INTO quizzes (teacher_id,class_name,subject,title,duration,total_marks,status) VALUES (?,?,?,?,?,?,?)',
#                      (session['teacher_id'],d['class_name'],d['subject'],d['title'],d.get('duration',30),0,'Draft'))
#     qid = cur.lastrowid; total = 0
#     for q in d.get('questions',[]):
#         db.execute('INSERT INTO quiz_questions (quiz_id,question,option_a,option_b,option_c,option_d,correct_ans,marks) VALUES (?,?,?,?,?,?,?,?)',
#                    (qid,q['question'],q['a'],q['b'],q['c'],q['d'],q['correct'],q.get('marks',1)))
#         total += q.get('marks',1)
#     db.execute('UPDATE quizzes SET total_marks=? WHERE id=?',(total,qid))
#     db.commit()
#     return jsonify({'success':True,'quiz_id':qid})

# @app.route('/teacher/quiz/<int:qid>/toggle', methods=['POST'])
# def toggle_quiz(qid):
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     q  = db.execute('SELECT status FROM quizzes WHERE id=? AND teacher_id=?',(qid,session['teacher_id'])).fetchone()
#     if not q: return jsonify({'error':'Not found'}), 404
#     new_status = 'Active' if q['status']=='Draft' else 'Draft'
#     db.execute('UPDATE quizzes SET status=? WHERE id=?',(new_status,qid))
#     db.commit()
#     return jsonify({'success':True,'status':new_status})

# @app.route('/teacher/quiz/<int:qid>/results')
# def quiz_results(qid):
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     quiz    = db.execute('SELECT * FROM quizzes WHERE id=?',(qid,)).fetchone()
#     results = db.execute('''SELECT qa.*,s.name as student_name,s.roll_number
#         FROM quiz_attempts qa JOIN students s ON qa.student_id=s.id
#         WHERE qa.quiz_id=? ORDER BY qa.score DESC''',(qid,)).fetchall()
#     return render_template('quiz_results.html', quiz=quiz, results=results)

# @app.route('/teacher/quiz/<int:qid>/delete', methods=['POST'])
# def delete_quiz(qid):
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM quiz_attempts WHERE quiz_id=?',(qid,))
#     db.execute('DELETE FROM quiz_questions WHERE quiz_id=?',(qid,))
#     db.execute('DELETE FROM quizzes WHERE id=? AND teacher_id=?',(qid,session['teacher_id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/live_classes')
# def teacher_live_classes():
#     if session.get('role') != 'teacher': return redirect('/teacher/login')
#     db = get_db()
#     my_classes = db.execute('SELECT * FROM live_classes WHERE teacher_id=? ORDER BY scheduled_at DESC',(session['teacher_id'],)).fetchall()
#     all_classes = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     subjects = ['Mathematics','Science','English','Hindi','Social Science','Computer','Sanskrit','Drawing','Physical Education']
#     return render_template('teacher_live_classes.html', my_classes=my_classes, all_classes=all_classes, subjects=subjects)

# @app.route('/teacher/add_live_class', methods=['POST'])
# def add_live_class():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('INSERT INTO live_classes (teacher_id,class_name,subject,title,meet_link,platform,scheduled_at,duration,status,description) VALUES (?,?,?,?,?,?,?,?,?,?)',
#         (session['teacher_id'],d['class_name'],d['subject'],d['title'],d['meet_link'],d['platform'],d['scheduled_at'],d.get('duration',60),'Upcoming',d.get('description','')))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/update_live_class_status', methods=['POST'])
# def update_live_class_status():
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('UPDATE live_classes SET status=? WHERE id=? AND teacher_id=?',(d['status'],d['id'],session['teacher_id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/delete_live_class/<int:lcid>', methods=['POST'])
# def delete_live_class(lcid):
#     if session.get('role') != 'teacher': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM live_classes WHERE id=? AND teacher_id=?',(lcid,session['teacher_id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/teacher/logout')
# def teacher_logout():
#     session.clear(); return redirect('/')

# # ═══════════════════════════════════════════════
# # PARENT PORTAL
# # ═══════════════════════════════════════════════

# @app.route('/parent/login', methods=['GET','POST'])
# def parent_login():
#     if request.method == 'POST':
#         db = get_db()
#         student = db.execute('SELECT * FROM students WHERE roll_number=? AND contact=?',
#             (request.form['roll_number'], request.form['contact'])).fetchone()
#         if student:
#             session.update({'parent_student_id':student['id'],'parent_student_name':student['name'],
#                            'parent_student_class':student['class_name'],'parent_name':student['parent_name'],'role':'parent'})
#             return redirect('/parent/dashboard')
#         flash('Invalid Roll Number or Contact Number.','error')
#     return render_template('parent_login.html')

# @app.route('/parent/dashboard')
# def parent_dashboard():
#     if session.get('role') != 'parent': return redirect('/parent/login')
#     db  = get_db()
#     sid = session['parent_student_id']
#     student    = db.execute('SELECT * FROM students WHERE id=?',(sid,)).fetchone()
#     marks      = db.execute('SELECT * FROM marks WHERE student_id=? ORDER BY subject',(sid,)).fetchall()
#     attendance = db.execute('SELECT * FROM attendance WHERE student_id=? ORDER BY date DESC LIMIT 30',(sid,)).fetchall()
#     fees       = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month',(sid,)).fetchall()
#     homework   = db.execute('SELECT * FROM homework WHERE class_name=? ORDER BY due_date DESC LIMIT 10',(session['parent_student_class'],)).fetchall()
#     notices    = db.execute('SELECT * FROM notices ORDER BY created_at DESC LIMIT 5').fetchall()
#     total   = len(attendance); present = sum(1 for a in attendance if a['status']=='Present')
#     pct     = round((present/total*100) if total else 0, 1)
#     total_due  = sum(f['total_fee'] for f in fees)
#     total_paid = sum(f['paid_amount'] for f in fees)
#     return render_template('parent_dashboard.html',
#         student=student, marks=marks, attendance=attendance, fees=fees,
#         homework=homework, notices=notices, attend_pct=pct,
#         total_days=total, present_days=present,
#         total_due=total_due, total_paid=total_paid, total_remaining=total_due-total_paid)

# @app.route('/parent/logout')
# def parent_logout():
#     session.clear(); return redirect('/')

# # ═══════════════════════════════════════════════
# # ADMIN
# # ═══════════════════════════════════════════════

# @app.route('/admin/login', methods=['GET','POST'])
# def admin_login():
#     if request.method == 'POST':
#         if request.form['username']=='admin' and request.form['password']=='admin123':
#             session['role'] = 'admin'; return redirect('/admin/dashboard')
#         flash('Wrong credentials.','error')
#     return render_template('admin_login.html')

# @app.route('/admin/logout')
# def admin_logout():
#     session.clear(); return redirect('/')

# @app.route('/admin/dashboard')
# def admin_dashboard():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     stats = {
#         'students':   db.execute('SELECT COUNT(*) FROM students').fetchone()[0],
#         'teachers':   db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
#         'admissions': db.execute("SELECT COUNT(*) FROM admissions WHERE status='Pending'").fetchone()[0],
#         'notices':    db.execute('SELECT COUNT(*) FROM notices').fetchone()[0],
#     }
#     admissions  = db.execute('SELECT * FROM admissions ORDER BY created_at DESC').fetchall()
#     messages    = db.execute('SELECT * FROM contact_messages ORDER BY created_at DESC').fetchall()
#     students    = db.execute('SELECT * FROM students ORDER BY class_name, roll_number').fetchall()
#     teachers    = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     all_notices = db.execute('SELECT * FROM notices ORDER BY created_at DESC').fetchall()
#     return render_template('admin_dashboard.html',
#         stats=stats, admissions=admissions, messages=messages,
#         students=students, teachers=teachers, all_notices=all_notices)

# @app.route('/admin/add_student', methods=['POST'])
# def add_student():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     try:
#         db.execute('INSERT INTO students (name,class_name,roll_number,parent_name,contact,password) VALUES (?,?,?,?,?,?)',
#             (request.form['name'],request.form['class_name'],request.form['roll_number'],
#              request.form['parent_name'],request.form['contact'],request.form['password']))
#         db.commit(); flash('Student added!','success')
#     except: flash('Error: Roll number may already exist.','error')
#     return redirect('/admin/dashboard')

# @app.route('/admin/delete_student/<int:sid>', methods=['POST'])
# def delete_student(sid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     for tbl in ['marks','attendance','fees']: db.execute(f'DELETE FROM {tbl} WHERE student_id=?',(sid,))
#     db.execute('DELETE FROM students WHERE id=?',(sid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/add_teacher', methods=['POST'])
# def add_teacher():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     try:
#         db.execute('INSERT INTO teachers (name,subject,username,password,email) VALUES (?,?,?,?,?)',
#             (request.form['name'],request.form['subject'],request.form['username'],
#              request.form['password'],request.form.get('email','')))
#         db.commit(); flash(f"Teacher added!",'success')
#     except: flash('Error: Username already exists.','error')
#     return redirect('/admin/dashboard')

# @app.route('/admin/delete_teacher/<int:tid>', methods=['POST'])
# def delete_teacher(tid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM homework WHERE teacher_id=?',(tid,))
#     db.execute('DELETE FROM teacher_assignments WHERE teacher_id=?',(tid,))
#     db.execute('DELETE FROM teachers WHERE id=?',(tid,))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/teacher_edit/<int:tid>')
# def admin_teacher_edit(tid):
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     teacher = db.execute('SELECT * FROM teachers WHERE id=?',(tid,)).fetchone()
#     return render_template('admin_teacher_edit.html', teacher=teacher)

# @app.route('/admin/update_teacher_info', methods=['POST'])
# def update_teacher_info():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('UPDATE teachers SET phone=?,qualification=?,experience=?,bio=?,joining_date=? WHERE id=?',
#         (d.get('phone',''),d.get('qualification',''),d.get('experience',''),
#          d.get('bio',''),d.get('joining_date',''),d['id']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/upload_teacher_photo/<int:tid>', methods=['POST'])
# def upload_teacher_photo(tid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
#     file = request.files['photo']
#     ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#     if ext not in {'png','jpg','jpeg','gif','webp'}: return jsonify({'error':'Invalid type'}), 400
#     fname = f"teacher_{tid}_{uuid.uuid4().hex[:8]}.{ext}"
#     path  = os.path.join(app.root_path,'static','uploads','teachers',fname)
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     file.save(path)
#     db = get_db(); db.execute('UPDATE teachers SET photo=? WHERE id=?',(fname,tid)); db.commit()
#     return jsonify({'success':True,'filename':fname})

# @app.route('/admin/add_notice', methods=['POST'])
# def add_notice():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     db.execute('INSERT INTO notices (title,content,category) VALUES (?,?,?)',
#         (request.form['title'],request.form['content'],request.form['category']))
#     db.commit(); flash('Notice posted!','success'); return redirect('/admin/dashboard')

# @app.route('/admin/edit_notice', methods=['POST'])
# def edit_notice():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     db.execute('UPDATE notices SET title=?,content=?,category=? WHERE id=?',
#         (request.form['title'],request.form['content'],request.form['category'],request.form['notice_id']))
#     db.commit(); flash('Notice updated!','success'); return redirect('/admin/dashboard')

# @app.route('/admin/delete_notice/<int:nid>', methods=['POST'])
# def delete_notice(nid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM notices WHERE id=?',(nid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/update_admission_status', methods=['POST'])
# def update_admission_status():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('UPDATE admissions SET status=? WHERE id=?',(d['status'],d['id'])); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/delete_admission/<int:aid>', methods=['POST'])
# def delete_admission(aid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM admissions WHERE id=?',(aid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/delete_message/<int:mid>', methods=['POST'])
# def delete_message(mid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM contact_messages WHERE id=?',(mid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/teacher_assignments')
# def teacher_assignments_page():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     teachers = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     return render_template('teacher_assignments.html', teachers=teachers)

# @app.route('/admin/assign_teacher', methods=['POST'])
# def assign_teacher():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     try:
#         db.execute('INSERT OR REPLACE INTO teacher_assignments (teacher_id,class_name,subject) VALUES (?,?,?)',
#             (d['teacher_id'],d['class_name'],d['subject']))
#         db.commit(); return jsonify({'success':True})
#     except Exception as e: return jsonify({'error':str(e)}), 500

# @app.route('/admin/remove_assignment', methods=['POST'])
# def remove_assignment():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('DELETE FROM teacher_assignments WHERE id=?',(d['id'],)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/get_assignments')
# def get_assignments():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     rows = db.execute('SELECT ta.id,ta.class_name,ta.subject,t.name as teacher_name,t.id as teacher_id FROM teacher_assignments ta JOIN teachers t ON ta.teacher_id=t.id ORDER BY ta.class_name,ta.subject').fetchall()
#     return jsonify([dict(r) for r in rows])

# @app.route('/admin/gallery')
# def admin_gallery():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     photos = db.execute('SELECT * FROM gallery_photos ORDER BY uploaded_at DESC').fetchall()
#     return render_template('admin_gallery.html', photos=photos)

# @app.route('/admin/upload_gallery_photo', methods=['POST'])
# def upload_gallery_photo():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     if 'photo' not in request.files: return jsonify({'error':'No file'}), 400
#     file = request.files['photo']
#     title = request.form.get('title','Photo'); category = request.form.get('category','General'); desc = request.form.get('description','')
#     ext = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#     if ext not in {'png','jpg','jpeg','gif','webp'}: return jsonify({'error':'Invalid type'}), 400
#     fname = f"gallery_{uuid.uuid4().hex[:10]}.{ext}"
#     path  = os.path.join(app.root_path,'static','uploads','gallery',fname)
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     file.save(path)
#     db = get_db(); db.execute('INSERT INTO gallery_photos (title,category,filename,description) VALUES (?,?,?,?)',(title,category,fname,desc)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/delete_gallery_photo/<int:pid>', methods=['POST'])
# def delete_gallery_photo(pid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     p = db.execute('SELECT filename FROM gallery_photos WHERE id=?',(pid,)).fetchone()
#     if p:
#         path = os.path.join(app.root_path,'static','uploads','gallery',p['filename'])
#         if os.path.exists(path): os.remove(path)
#         db.execute('DELETE FROM gallery_photos WHERE id=?',(pid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/fees')
# def admin_fees():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','Class 5')
#     sel_month = request.args.get('month','')
#     sel_year  = request.args.get('year','2024-25')
#     fee_struct = db.execute('SELECT * FROM fee_structure WHERE class_name=?',(sel_class,)).fetchone()
#     q = 'SELECT f.*,s.name as student_name,s.roll_number FROM fees f JOIN students s ON f.student_id=s.id WHERE f.class_name=?'
#     p = [sel_class]
#     if sel_month: q += ' AND f.fee_month=?'; p.append(sel_month)
#     q += ' ORDER BY f.fee_month,s.roll_number'
#     fees = db.execute(q, p).fetchall()
#     total_due = sum(f['total_fee'] for f in fees); total_paid = sum(f['paid_amount'] for f in fees); total_rem = sum(f['remaining'] for f in fees)
#     months = db.execute('SELECT DISTINCT fee_month FROM fees WHERE class_name=? ORDER BY fee_month',(sel_class,)).fetchall()
#     students_summary = db.execute('''SELECT s.id,s.name,s.roll_number,COUNT(f.id) as total_months,SUM(CASE WHEN f.status="Paid" THEN 1 ELSE 0 END) as paid_months,SUM(f.total_fee) as total_due,SUM(f.paid_amount) as total_paid,SUM(f.remaining) as total_remaining FROM students s LEFT JOIN fees f ON s.id=f.student_id WHERE s.class_name=? GROUP BY s.id ORDER BY s.roll_number''',(sel_class,)).fetchall()
#     return render_template('admin_fees.html', classes=classes, sel_class=sel_class, sel_month=sel_month, sel_year=sel_year, fee_struct=fee_struct, fees=fees, months=months, total_due=total_due, total_paid=total_paid, total_rem=total_rem, students_summary=students_summary)

# @app.route('/admin/fees/update', methods=['POST'])
# def update_fee():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     total = float(d.get('total_fee',0)); paid = float(d.get('paid_amount',0)); rem = max(0,total-paid)
#     status = 'Paid' if rem<=0 else ('Partial' if paid>0 else 'Pending')
#     db.execute('INSERT INTO fees (student_id,class_name,fee_month,fee_year,tuition_fee,other_fee,total_fee,paid_amount,remaining,status,paid_date,remarks) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(student_id,fee_month) DO UPDATE SET total_fee=excluded.total_fee,paid_amount=excluded.paid_amount,remaining=excluded.remaining,status=excluded.status,paid_date=excluded.paid_date,remarks=excluded.remarks',
#         (d['student_id'],d['class_name'],d['fee_month'],d.get('fee_year','2024-25'),d.get('tuition_fee',0),d.get('other_fee',0),total,paid,rem,status,d.get('paid_date') or None,d.get('remarks','')))
#     db.commit(); return jsonify({'success':True,'remaining':rem,'status':status})

# @app.route('/admin/fees/generate_monthly', methods=['POST'])
# def generate_monthly_fees():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     struct = db.execute('SELECT * FROM fee_structure WHERE class_name=?',(d['class_name'],)).fetchone()
#     if not struct: return jsonify({'error':'Fee structure not set'}), 400
#     total = struct['tuition_fee']+struct['activity_fee']+struct['computer_fee']+struct['other_fee']
#     students = db.execute('SELECT id FROM students WHERE class_name=?',(d['class_name'],)).fetchall()
#     count = 0
#     for s in students:
#         try:
#             db.execute('INSERT OR IGNORE INTO fees (student_id,class_name,fee_month,fee_year,tuition_fee,other_fee,total_fee,paid_amount,remaining,status) VALUES (?,?,?,?,?,?,?,0,?,?)',
#                 (s['id'],d['class_name'],d['fee_month'],d.get('fee_year','2024-25'),struct['tuition_fee'],struct['activity_fee']+struct['computer_fee']+struct['other_fee'],total,total,'Pending'))
#             count += 1
#         except: pass
#     db.commit(); return jsonify({'success':True,'generated':count})

# @app.route('/admin/fees/update_structure', methods=['POST'])
# def update_fee_structure():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('INSERT INTO fee_structure (class_name,tuition_fee,activity_fee,computer_fee,other_fee) VALUES (?,?,?,?,?) ON CONFLICT(class_name) DO UPDATE SET tuition_fee=excluded.tuition_fee,activity_fee=excluded.activity_fee,computer_fee=excluded.computer_fee,other_fee=excluded.other_fee',
#                (d['class_name'],d['tuition_fee'],d['activity_fee'],d['computer_fee'],d['other_fee']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/fees/student_detail/<int:sid>')
# def admin_student_fee_detail(sid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     fees = db.execute('SELECT * FROM fees WHERE student_id=? ORDER BY fee_month',(sid,)).fetchall()
#     return jsonify({'fees':[dict(f) for f in fees]})

# @app.route('/admin/achievements')
# def admin_achievements():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     ach      = db.execute("SELECT *, COALESCE(student_name,'') as student_name FROM achievements ORDER BY created_at DESC").fetchall()
#     students = db.execute('SELECT * FROM students ORDER BY class_name,name').fetchall()
#     classes  = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     return render_template('admin_achievements.html', items=ach, students=students, classes=classes)

# @app.route('/admin/achievements/add', methods=['POST'])
# def add_achievement():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     sid   = request.form.get('student_id') or None
#     sname = request.form.get('student_name','').strip()
#     cls   = request.form.get('class_name','')
#     if sid:
#         s = db.execute('SELECT name,class_name FROM students WHERE id=?',(sid,)).fetchone()
#         if s: sname = s['name']; cls = s['class_name']
#     photo = None
#     if 'photo' in request.files and request.files['photo'].filename:
#         file = request.files['photo']
#         ext  = file.filename.rsplit('.',1)[-1].lower() if '.' in file.filename else 'jpg'
#         if ext in {'jpg','jpeg','png','gif','webp'}:
#             fname = f"ach_{uuid.uuid4().hex[:8]}.{ext}"
#             path  = os.path.join(app.root_path,'static','uploads','achievements',fname)
#             os.makedirs(os.path.dirname(path), exist_ok=True)
#             file.save(path); photo = fname
#     db.execute('INSERT INTO achievements (student_id,student_name,class_name,title,category,description,achievement_date,is_featured,photo) VALUES (?,?,?,?,?,?,?,?,?)',
#         (sid,sname,cls,request.form.get('title',''),request.form.get('category','Academic'),
#          request.form.get('description',''),request.form.get('achievement_date',''),
#          1 if request.form.get('is_featured') else 0, photo))
#     db.commit(); flash('Achievement added!','success')
#     return redirect('/admin/achievements')

# @app.route('/admin/achievements/delete/<int:aid>', methods=['POST'])
# def delete_achievement(aid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     a  = db.execute('SELECT photo FROM achievements WHERE id=?',(aid,)).fetchone()
#     if a and a['photo']:
#         path = os.path.join(app.root_path,'static','uploads','achievements',a['photo'])
#         if os.path.exists(path): os.remove(path)
#     db.execute('DELETE FROM achievements WHERE id=?',(aid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/id_cards')
# def admin_id_cards():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_cls = request.args.get('class_name','All')
#     if sel_cls == 'All':
#         students = db.execute('SELECT * FROM students ORDER BY class_name,roll_number').fetchall()
#     else:
#         students = db.execute('SELECT * FROM students WHERE class_name=? ORDER BY roll_number',(sel_cls,)).fetchall()
#     return render_template('admin_id_cards.html', students=students, classes=classes, sel_cls=sel_cls)

# @app.route('/admin/id_card/<int:sid>/pdf')
# def generate_id_card(sid):
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib import colors
#     from reportlab.lib.units import cm
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
#     from reportlab.lib.styles import ParagraphStyle
#     from reportlab.lib.enums import TA_CENTER
#     from io import BytesIO
#     db = get_db()
#     if sid == 0:
#         students = db.execute('SELECT * FROM students ORDER BY class_name,roll_number').fetchall()
#     else:
#         students = db.execute('SELECT * FROM students WHERE id=?',(sid,)).fetchall()
#     buffer = BytesIO()
#     doc    = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
#     NAVY   = colors.HexColor('#0d1b3e'); GOLD = colors.HexColor('#c9a84c'); CREAM = colors.HexColor('#fdf8f0')
#     story  = []
#     card_w = 8.5*cm; rows = []; row = []
#     for s in students:
#         photo_cell = Paragraph(f'<font size="28" color="#c9a84c"><b>{s["name"][0].upper()}</b></font>', ParagraphStyle('p',alignment=TA_CENTER))
#         header = Table([[Paragraph('<font color="white" size="7"><b>BRIGHTMIND SCHOOL · 2024-25</b></font>', ParagraphStyle('h',alignment=TA_CENTER,fontName='Helvetica-Bold'))]], colWidths=[card_w-0.4*cm])
#         header.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
#         info = [[Paragraph(f'<b>{s["name"]}</b>', ParagraphStyle('n',fontSize=9,fontName='Helvetica-Bold',textColor=NAVY)),''],
#                 [Paragraph(f'Class: <b>{s["class_name"]}</b>', ParagraphStyle('c',fontSize=8,textColor=NAVY)),''],
#                 [Paragraph(f'Roll: <b>{s["roll_number"]}</b>', ParagraphStyle('r',fontSize=8,textColor=NAVY)),'']]
#         info_tbl = Table(info, colWidths=[card_w-2.5*cm,1.8*cm])
#         info_tbl.setStyle(TableStyle([('FONTSIZE',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
#         photo_box = Table([[photo_cell]], colWidths=[1.6*cm], rowHeights=[2.2*cm])
#         photo_box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
#         content_row = Table([[photo_box, info_tbl]], colWidths=[1.8*cm, card_w-2.2*cm])
#         content_row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
#         footer_tbl = Table([[Paragraph('<font size="6.5" color="#666">Ph: +91 11 1234 5678 | Delhi</font>', ParagraphStyle('f',alignment=TA_CENTER))]], colWidths=[card_w-0.4*cm])
#         footer_tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),CREAM),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
#         card = Table([[header],[content_row],[footer_tbl]], colWidths=[card_w], rowHeights=[1*cm, 2.8*cm, 0.6*cm])
#         card.setStyle(TableStyle([('BOX',(0,0),(-1,-1),1.5,GOLD),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
#         row.append(card)
#         if len(row) == 2: rows.append(row); row = []
#     if row:
#         while len(row) < 2: row.append(Paragraph('',ParagraphStyle('e')))
#         rows.append(row)
#     if rows:
#         all_cards = Table(rows, colWidths=[card_w+0.5*cm]*2, rowHeights=[5.1*cm]*len(rows))
#         all_cards.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
#         story.append(Paragraph('<b>STUDENT ID CARDS — BrightMind School 2024-25</b>', ParagraphStyle('t',fontSize=11,alignment=TA_CENTER,textColor=NAVY,fontName='Helvetica-Bold',spaceAfter=12)))
#         story.append(all_cards)
#     doc.build(story)
#     pdf = buffer.getvalue(); buffer.close()
#     name = students[0]['name'] if len(students)==1 else 'All_Students'
#     response = make_response(pdf)
#     response.headers['Content-Type']        = 'application/pdf'
#     response.headers['Content-Disposition'] = f'attachment; filename=ID_Card_{name}.pdf'
#     return response

# @app.route('/admin/notifications')
# def admin_notifications():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     logs         = db.execute('SELECT * FROM whatsapp_logs ORDER BY sent_at DESC LIMIT 50').fetchall()
#     students     = db.execute('SELECT * FROM students ORDER BY class_name,name').fetchall()
#     classes      = ['All','UKG'] + [f'Class {i}' for i in range(1,11)]
#     pending_fees = db.execute("SELECT s.name,s.contact,s.class_name,f.fee_month,f.remaining FROM fees f JOIN students s ON f.student_id=s.id WHERE f.status IN ('Pending','Overdue') AND s.contact IS NOT NULL ORDER BY s.class_name,s.name").fetchall()
#     return render_template('admin_notifications.html', logs=logs, students=students, classes=classes, pending_fees=pending_fees)

# @app.route('/admin/send_notification', methods=['POST'])
# def send_notification():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     recipients = []
#     if d.get('target') == 'all':
#         for s in db.execute('SELECT name,contact,class_name FROM students WHERE contact IS NOT NULL').fetchall():
#             recipients.append({'name':s['name'],'contact':s['contact'],'class':s['class_name']})
#     elif d.get('target') == 'class':
#         for s in db.execute('SELECT name,contact,class_name FROM students WHERE class_name=? AND contact IS NOT NULL',(d['class_name'],)).fetchall():
#             recipients.append({'name':s['name'],'contact':s['contact'],'class':s['class_name']})
#     elif d.get('target') == 'fees_pending':
#         for s in db.execute("SELECT DISTINCT s.name,s.contact,s.class_name FROM fees f JOIN students s ON f.student_id=s.id WHERE f.status IN ('Pending','Overdue') AND s.contact IS NOT NULL").fetchall():
#             recipients.append({'name':s['name'],'contact':s['contact'],'class':s['class_name']})
#     elif d.get('contact'):
#         recipients.append({'name':d.get('name','Student'),'contact':d['contact'],'class':''})
#     sent = 0; msg_template = d.get('message','')
#     for r in recipients:
#         msg = msg_template.replace('{name}',r['name']).replace('{class}',r['class'])
#         db.execute('INSERT INTO whatsapp_logs (recipient,message,status) VALUES (?,?,?)',(r['contact'],msg,'Sent (Simulated)'))
#         sent += 1
#     db.commit()
#     return jsonify({'success':True,'sent':sent,'wa_link':f"https://wa.me/?text={msg_template.replace(' ','%20')}" if recipients else ''})

# @app.route('/admin/analytics')
# def admin_analytics():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     fee_stats = db.execute('SELECT class_name,SUM(total_fee) as total_due,SUM(paid_amount) as total_paid,SUM(remaining) as total_remaining,COUNT(CASE WHEN status="Paid" THEN 1 END) as paid_count,COUNT(CASE WHEN status="Pending" THEN 1 END) as pending_count,COUNT(CASE WHEN status="Overdue" THEN 1 END) as overdue_count FROM fees GROUP BY class_name ORDER BY class_name').fetchall()
#     monthly    = db.execute('SELECT fee_month,SUM(paid_amount) as collected,SUM(remaining) as pending FROM fees GROUP BY fee_month ORDER BY fee_month').fetchall()
#     att_stats  = db.execute('SELECT s.class_name,COUNT(a.id) as total_records,SUM(CASE WHEN a.status="Present" THEN 1 ELSE 0 END) as present_count FROM students s LEFT JOIN attendance a ON s.id=a.student_id GROUP BY s.class_name ORDER BY s.class_name').fetchall()
#     top_students = db.execute('SELECT s.name,s.class_name,s.roll_number,AVG(m.marks/m.max_marks*100) as avg_pct,COUNT(m.id) as subjects FROM students s JOIN marks m ON s.id=m.student_id GROUP BY s.id HAVING subjects>=2 ORDER BY avg_pct DESC LIMIT 10').fetchall()
#     summary = {
#         'total_students': db.execute('SELECT COUNT(*) FROM students').fetchone()[0],
#         'total_teachers': db.execute('SELECT COUNT(*) FROM teachers').fetchone()[0],
#         'total_fee_due':  db.execute('SELECT SUM(total_fee) FROM fees').fetchone()[0] or 0,
#         'total_fee_paid': db.execute('SELECT SUM(paid_amount) FROM fees').fetchone()[0] or 0,
#         'pending_admissions': db.execute("SELECT COUNT(*) FROM admissions WHERE status='Pending'").fetchone()[0],
#         'total_notices': db.execute('SELECT COUNT(*) FROM notices').fetchone()[0],
#     }
#     summary['collection_pct'] = round(summary['total_fee_paid']/summary['total_fee_due']*100 if summary['total_fee_due'] else 0, 1)
#     return render_template('admin_analytics.html', fee_stats=fee_stats, monthly=monthly, att_stats=att_stats, top_students=top_students, summary=summary)

# @app.route('/admin/timetable')
# def admin_timetable():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes   = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     sel_class = request.args.get('class_name','Class 5')
#     teachers  = db.execute('SELECT * FROM teachers ORDER BY name').fetchall()
#     days      = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
#     periods   = list(range(1,7))
#     rows = db.execute('SELECT * FROM timetable WHERE class_name=? ORDER BY day,period',(sel_class,)).fetchall()
#     tt   = {day:{} for day in days}
#     for r in rows: tt[r['day']][r['period']] = r
#     period_times = {1:'8:00-8:45',2:'8:45-9:30',3:'9:30-10:15',4:'10:30-11:15',5:'11:15-12:00',6:'12:00-12:45'}
#     return render_template('admin_timetable.html', classes=classes, sel_class=sel_class, teachers=teachers, days=days, periods=periods, tt=tt, period_times=period_times)

# @app.route('/admin/timetable/save', methods=['POST'])
# def save_timetable():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     try:
#         db.execute('INSERT INTO timetable (class_name,day,period,subject,teacher_id,start_time,end_time) VALUES (?,?,?,?,?,?,?) ON CONFLICT(class_name,day,period) DO UPDATE SET subject=excluded.subject,teacher_id=excluded.teacher_id',
#             (d['class_name'],d['day'],d['period'],d['subject'],d.get('teacher_id') or None,d.get('start_time',''),d.get('end_time','')))
#         db.commit(); return jsonify({'success':True})
#     except Exception as e: return jsonify({'error':str(e)}), 500

# @app.route('/admin/timetable/delete', methods=['POST'])
# def delete_timetable_entry():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('DELETE FROM timetable WHERE class_name=? AND day=? AND period=?',(d['class_name'],d['day'],d['period']))
#     db.commit(); return jsonify({'success':True})

# @app.route('/admin/exam_schedule')
# def admin_exam_schedule():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     exams   = db.execute('SELECT * FROM exam_schedule ORDER BY exam_date,class_name').fetchall()
#     classes = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     return render_template('admin_exam_schedule.html', exams=exams, classes=classes)

# @app.route('/admin/exam_schedule/add', methods=['POST'])
# def add_exam():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     db.execute('INSERT INTO exam_schedule (class_name,subject,exam_date,day,start_time,end_time,exam_type,venue) VALUES (?,?,?,?,?,?,?,?)',
#         (request.form['class_name'],request.form['subject'],request.form['exam_date'],
#          request.form.get('day',''),request.form.get('start_time','10:00'),request.form.get('end_time','13:00'),
#          request.form['exam_type'],request.form.get('venue','Main Hall')))
#     db.commit(); flash('Exam added!','success'); return redirect('/admin/exam_schedule')

# @app.route('/admin/exam_schedule/delete/<int:eid>', methods=['POST'])
# def delete_exam(eid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM exam_schedule WHERE id=?',(eid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/live_classes')
# def admin_live_classes():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     classes_data = db.execute('SELECT lc.*,t.name as teacher_name FROM live_classes lc JOIN teachers t ON lc.teacher_id=t.id ORDER BY lc.scheduled_at DESC').fetchall()
#     all_classes  = ['UKG'] + [f'Class {i}' for i in range(1,11)]
#     return render_template('admin_live_classes.html', classes_data=classes_data, all_classes=all_classes)

# @app.route('/admin/live_classes/update_status', methods=['POST'])
# def admin_update_live_status():
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     d = request.json; db = get_db()
#     db.execute('UPDATE live_classes SET status=? WHERE id=?',(d['status'],d['id'])); db.commit()
#     return jsonify({'success':True})


# @app.route('/admin/live_classes/delete/<int:lcid>', methods=['POST'])
# def admin_delete_live_class(lcid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db(); db.execute('DELETE FROM live_classes WHERE id=?',(lcid,)); db.commit()
#     return jsonify({'success':True})

# # ── ADMIN QUIZ MANAGER ─────────────────────────────────────────
# @app.route('/admin/quiz_manager')
# def admin_quiz_manager():
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     quizzes = db.execute("""
#         SELECT q.*, t.name as teacher_name,
#                COUNT(qa.id) as attempt_count,
#                AVG(CASE WHEN qa.total > 0 THEN qa.score*100.0/qa.total END) as avg_score
#         FROM quizzes q
#         LEFT JOIN teachers t ON q.teacher_id=t.id
#         LEFT JOIN quiz_attempts qa ON q.id=qa.quiz_id
#         GROUP BY q.id ORDER BY q.created_at DESC
#     """).fetchall()
#     return render_template('admin_quiz_manager.html', quizzes=quizzes)

# @app.route('/admin/quiz/toggle/<int:qid>', methods=['POST'])
# def admin_toggle_quiz(qid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     q  = db.execute('SELECT status FROM quizzes WHERE id=?',(qid,)).fetchone()
#     if not q: return jsonify({'error':'Not found'}), 404
#     new_status = 'Active' if q['status']=='Draft' else 'Draft'
#     db.execute('UPDATE quizzes SET status=? WHERE id=?',(new_status,qid)); db.commit()
#     return jsonify({'success':True,'status':new_status})

# @app.route('/admin/quiz/delete/<int:qid>', methods=['POST'])
# def admin_delete_quiz(qid):
#     if session.get('role') != 'admin': return jsonify({'error':'Unauthorized'}), 401
#     db = get_db()
#     db.execute('DELETE FROM quiz_attempts WHERE quiz_id=?',(qid,))
#     db.execute('DELETE FROM quiz_questions WHERE quiz_id=?',(qid,))
#     db.execute('DELETE FROM quizzes WHERE id=?',(qid,)); db.commit()
#     return jsonify({'success':True})

# @app.route('/admin/quiz/<int:qid>/results')
# def admin_quiz_results(qid):
#     if session.get('role') != 'admin': return redirect('/admin/login')
#     db = get_db()
#     quiz     = db.execute('SELECT q.*,t.name as tname FROM quizzes q LEFT JOIN teachers t ON q.teacher_id=t.id WHERE q.id=?',(qid,)).fetchone()
#     results  = db.execute('SELECT qa.*,s.name as student_name,s.roll_number,s.class_name FROM quiz_attempts qa JOIN students s ON qa.student_id=s.id WHERE qa.quiz_id=? ORDER BY qa.score DESC',(qid,)).fetchall()
#     questions= db.execute('SELECT COUNT(*) FROM quiz_questions WHERE quiz_id=?',(qid,)).fetchone()[0]
#     return render_template('admin_quiz_results.html', quiz=quiz, results=results, question_count=questions)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

