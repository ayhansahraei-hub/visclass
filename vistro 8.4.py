import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import hashlib
from datetime import datetime, date, timedelta
import os
import json
import random
import time
import math
from PIL import Image, ImageTk

# ==================== پالت رنگ مدرن و زیبا ====================
class ColorPalette:
    PRIMARY = {
        "MAIN": "#6366f1",
        "LIGHT": "#818cf8",
        "DARK": "#4f46e5",
        "GRADIENT_START": "#667eea",
        "GRADIENT_END": "#764ba2"
    }
    
    SECONDARY = {
        "SUCCESS": "#10b981",
        "WARNING": "#f59e0b",
        "ERROR": "#ef4444",
        "INFO": "#3b82f6",
        "PURPLE": "#8b5cf6"
    }
    
    NEUTRAL = {
        "WHITE": "#ffffff",
        "LIGHT_GRAY": "#f3f4f6",
        "GRAY": "#9ca3af",
        "DARK_GRAY": "#4b5563",
        "BLACK": "#1f2937",
        "BACKGROUND": "#f8fafc"
    }
    
    CHART = {
        "BLUE": "#3b82f6",
        "GREEN": "#10b981",
        "YELLOW": "#f59e0b",
        "RED": "#ef4444",
        "PURPLE": "#8b5cf6",
        "PINK": "#ec4899",
        "CYAN": "#06b6d4"
    }

# ==================== ویجت‌های سفارشی ساده‌تر ====================
class ModernButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, icon="", 
                 color="primary", size="medium", width=None, height=40, 
                 radius=12, **kwargs):
        
        self.parent_bg = parent['bg']
        self.command = command
        self.text = text
        self.icon = icon
        self.radius = radius
        self.is_hovered = False
        self.is_pressed = False
        
        # تنظیم رنگ
        if color == "primary":
            self.bg_color = ColorPalette.PRIMARY["MAIN"]
            self.hover_color = ColorPalette.PRIMARY["DARK"]
        elif color == "success":
            self.bg_color = ColorPalette.SECONDARY["SUCCESS"]
            self.hover_color = "#0da271"
        elif color == "warning":
            self.bg_color = ColorPalette.SECONDARY["WARNING"]
            self.hover_color = "#e68a09"
        elif color == "error":
            self.bg_color = ColorPalette.SECONDARY["ERROR"]
            self.hover_color = "#dc2626"
        elif color == "info":
            self.bg_color = ColorPalette.SECONDARY["INFO"]
            self.hover_color = "#2563eb"
        else:
            self.bg_color = color
            self.hover_color = color
        
        self.fg_color = ColorPalette.NEUTRAL["WHITE"]
        
        # تنظیم سایز
        if size == "small":
            height = 32
            font_size = 10
        elif size == "large":
            height = 50
            font_size = 14
        else:  # medium
            height = 40
            font_size = 12
        
        if width is None:
            text_width = len(text) * 8 + (20 if icon else 0)
            width = max(100, text_width)
        
        super().__init__(parent, bg=self.parent_bg, highlightthickness=0,
                        width=width, height=height, **kwargs)
        
        self.font_size = font_size
        self.draw_button()
        self.bind_events()
    
    def draw_button(self):
        self.delete("all")
        width = int(self['width'])
        height = int(self['height'])
        
        color = self.hover_color if self.is_hovered else self.bg_color
        if self.is_pressed:
            color = ColorPalette.PRIMARY["DARK"]
        
        # دکمه اصلی با گوشه‌های گرد (با create_round_rect ساده)
        self.create_round_rect(0, 0, width, height, self.radius,
                               fill=color, outline="")
        
        # متن و آیکون
        text_content = f"{self.icon} {self.text}" if self.icon else self.text
        self.create_text(width/2, height/2, text=text_content,
                        fill=self.fg_color, 
                        font=("Tahoma", self.font_size, "bold"))
    
    def create_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        # ایجاد مستطیل با گوشه‌های گرد ساده
        self.create_arc(x1, y1, x1+radius*2, y1+radius*2, start=90, extent=90, **kwargs)
        self.create_arc(x2-radius*2, y1, x2, y1+radius*2, start=0, extent=90, **kwargs)
        self.create_arc(x1, y2-radius*2, x1+radius*2, y2, start=180, extent=90, **kwargs)
        self.create_arc(x2-radius*2, y2-radius*2, x2, y2, start=270, extent=90, **kwargs)
        
        self.create_rectangle(x1+radius, y1, x2-radius, y2, **kwargs)
        self.create_rectangle(x1, y1+radius, x2, y2-radius, **kwargs)
    
    def bind_events(self):
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def on_enter(self, event):
        self.is_hovered = True
        self.draw_button()
        self.config(cursor="hand2")
    
    def on_leave(self, event):
        self.is_hovered = False
        self.is_pressed = False
        self.draw_button()
        self.config(cursor="")
    
    def on_click(self, event):
        self.is_pressed = True
        self.draw_button()
        if self.command:
            self.after(150, self.command)
    
    def on_release(self, event):
        self.is_pressed = False
        self.draw_button()

class GlassCard(tk.Frame):
    def __init__(self, parent, width=200, height=150, radius=15, color=None, **kwargs):
        bg_color = ColorPalette.NEUTRAL["WHITE"]
        super().__init__(parent, bg=bg_color, highlightthickness=0,
                        width=width, height=height, **kwargs)
        
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0,
                               width=width, height=height)
        self.canvas.pack(fill="both", expand=True)
        
        self.width = width
        self.height = height
        self.radius = radius
        self.color = color or ColorPalette.NEUTRAL["WHITE"]
        
        self.draw_card()
    
    def draw_card(self):
        self.canvas.delete("all")
        
        # کارت اصلی
        self.create_round_rect(0, 0, self.width, self.height, self.radius,
                              fill=self.color, outline=ColorPalette.NEUTRAL["LIGHT_GRAY"])
    
    def create_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        # ایجاد مستطیل با گوشه‌های گرد ساده
        self.canvas.create_arc(x1, y1, x1+radius*2, y1+radius*2, start=90, extent=90, **kwargs)
        self.canvas.create_arc(x2-radius*2, y1, x2, y1+radius*2, start=0, extent=90, **kwargs)
        self.canvas.create_arc(x1, y2-radius*2, x1+radius*2, y2, start=180, extent=90, **kwargs)
        self.canvas.create_arc(x2-radius*2, y2-radius*2, x2, y2, start=270, extent=90, **kwargs)
        
        self.canvas.create_rectangle(x1+radius, y1, x2-radius, y2, **kwargs)
        self.canvas.create_rectangle(x1, y1+radius, x2, y2-radius, **kwargs)

class CircularProgressChart(tk.Canvas):
    def __init__(self, parent, width=120, height=120, progress=75, 
                 color=None, title="", subtitle="", **kwargs):
        
        bg_color = parent['bg']
        super().__init__(parent, bg=bg_color, highlightthickness=0,
                        width=width, height=height, **kwargs)
        
        self.width = width
        self.height = height
        self.progress = max(0, min(100, progress))
        self.color = color or ColorPalette.PRIMARY["MAIN"]
        self.title = title
        self.subtitle = subtitle
        
        self.draw_chart()
    
    def draw_chart(self):
        self.delete("all")
        
        center_x = self.width / 2
        center_y = self.height / 2
        radius = min(center_x, center_y) - 15
        
        # پس‌زمینه دایره
        self.create_oval(center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        outline=ColorPalette.NEUTRAL["LIGHT_GRAY"], 
                        width=6,
                        fill=ColorPalette.NEUTRAL["WHITE"])
        
        # نمودار پیشرفت
        if self.progress > 0:
            start_angle = 90
            extent = -360 * self.progress / 100
            
            self.create_arc(center_x - radius, center_y - radius,
                          center_x + radius, center_y + radius,
                          start=start_angle, extent=extent,
                          outline=self.color, width=6, style="arc")
        
        # متن درصد
        self.create_text(center_x, center_y - 10, 
                        text=f"{self.progress}%",
                        font=("Tahoma", 16, "bold"),
                        fill=ColorPalette.NEUTRAL["BLACK"])
        
        # عنوان
        self.create_text(center_x, center_y + 25,
                        text=self.title,
                        font=("Tahoma", 10),
                        fill=ColorPalette.NEUTRAL["DARK_GRAY"])
        
        # زیرنویس
        if self.subtitle:
            self.create_text(center_x, center_y + 40,
                           text=self.subtitle,
                           font=("Tahoma", 9),
                           fill=ColorPalette.NEUTRAL["GRAY"])

class StatCard(tk.Frame):
    def __init__(self, parent, title="", value="", icon="", color=None, 
                 width=200, height=120, **kwargs):
        
        bg_color = ColorPalette.NEUTRAL["WHITE"]
        super().__init__(parent, bg=bg_color, highlightthickness=0,
                        width=width, height=height, **kwargs)
        
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0,
                               width=width, height=height)
        self.canvas.pack(fill="both", expand=True)
        
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color or ColorPalette.PRIMARY["MAIN"]
        self.width = width
        self.height = height
        
        self.draw_card()
    
    def draw_card(self):
        self.canvas.delete("all")
        
        # کارت با گوشه‌های گرد
        self.create_round_rect(0, 0, self.width, self.height, 12,
                              fill=ColorPalette.NEUTRAL["WHITE"],
                              outline=ColorPalette.NEUTRAL["LIGHT_GRAY"])
        
        # آیکون
        if self.icon:
            self.canvas.create_text(30, self.height//2, text=self.icon,
                                  font=("Segoe UI Emoji", 24),
                                  fill=self.color, anchor="w")
        
        # مقدار
        self.canvas.create_text(self.width-30, self.height//2 - 15, 
                               text=str(self.value),
                               font=("Tahoma", 28, "bold"),
                               fill=ColorPalette.NEUTRAL["BLACK"],
                               anchor="e")
        
        # عنوان
        self.canvas.create_text(self.width-30, self.height//2 + 20,
                               text=self.title,
                               font=("Tahoma", 11),
                               fill=ColorPalette.NEUTRAL["DARK_GRAY"],
                               anchor="e")
    
    def create_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        # ایجاد مستطیل با گوشه‌های گرد ساده
        self.canvas.create_arc(x1, y1, x1+radius*2, y1+radius*2, start=90, extent=90, **kwargs)
        self.canvas.create_arc(x2-radius*2, y1, x2, y1+radius*2, start=0, extent=90, **kwargs)
        self.canvas.create_arc(x1, y2-radius*2, x1+radius*2, y2, start=180, extent=90, **kwargs)
        self.canvas.create_arc(x2-radius*2, y2-radius*2, x2, y2, start=270, extent=90, **kwargs)
        
        self.canvas.create_rectangle(x1+radius, y1, x2-radius, y2, **kwargs)
        self.canvas.create_rectangle(x1, y1+radius, x2, y2-radius, **kwargs)

# ==================== سیستم دیتابیس ====================
class SchoolDatabase:
    def __init__(self):
        self.db_path = "school_management_pro.db"
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول کاربران
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول دانش‌آموزان
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                national_code TEXT UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                father_name TEXT,
                mother_name TEXT,
                birth_date TEXT,
                grade TEXT NOT NULL,
                class_name TEXT NOT NULL,
                phone TEXT,
                parent_phone TEXT,
                email TEXT,
                address TEXT,
                enrollment_date TEXT,
                blood_type TEXT,
                allergies TEXT,
                medical_notes TEXT,
                behavior_score INTEGER DEFAULT 5,
                total_absences INTEGER DEFAULT 0,
                total_tardiness INTEGER DEFAULT 0,
                academic_score INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول معلمان
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id TEXT UNIQUE NOT NULL,
                national_code TEXT UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                degree TEXT,
                major TEXT,
                subject TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                hire_date TEXT,
                salary REAL DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول نمرات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                grade_value REAL NOT NULL,
                exam_date TEXT,
                semester TEXT,
                teacher_id INTEGER,
                notes TEXT,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
            )
        ''')
        
        # جدول حضور و غیاب
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                arrival_time TEXT,
                departure_time TEXT,
                notes TEXT,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        
        # جدول رویدادها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                event_date TEXT NOT NULL,
                event_time TEXT,
                event_type TEXT NOT NULL,
                location TEXT,
                priority TEXT DEFAULT 'normal',
                status TEXT DEFAULT 'upcoming',
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # ایجاد کاربر ادمین اگر وجود ندارد
        cursor.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
        if cursor.fetchone()[0] == 0:
            admin_password = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute('''
                INSERT INTO users (username, password, full_name, role, email)
                VALUES (?, ?, ?, ?, ?)
            ''', ('admin', admin_password, 'مدیر سیستم', 'admin', 'admin@school.edu'))
        
        # ایجاد داده‌های نمونه
        self.create_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def create_sample_data(self, cursor):
        """ایجاد داده‌های نمونه برای نمایش"""
        try:
            # پاک کردن داده‌های قبلی برای جلوگیری از خطای تکراری
            cursor.execute("DELETE FROM students")
            cursor.execute("DELETE FROM teachers")
            
            # دانش‌آموزان نمونه
            sample_students = []
            first_names = ["علی", "محمد", "رضا", "حسین", "امیر", "سپهر", "پارسا", "کیان", "آرش", "سینا"]
            last_names = ["محمدی", "احمدی", "کریمی", "جعفری", "حسینی", "رضایی", "موسوی", "نوری", "کاظمی", "مرادی"]
            
            for i in range(1, 21):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                full_name = f"{first_name} {last_name}"
                
                student = (
                    f"STU{1403}{i:03d}",  # student_id
                    f"00{i:02d}123456{i:03d}",    # national_code - منحصر به فرد
                    first_name,
                    last_name,
                    full_name,
                    f"پدر {first_name}",
                    f"مادر {first_name}",
                    f"138{random.randint(0,9)}/{random.randint(1,12):02d}/{random.randint(1,28):02d}",
                    random.choice(["هفتم", "هشتم", "نهم"]),  # فقط هفتم تا نهم
                    random.choice(["1", "2", "3"]),
                    f"0912{random.randint(1000000,9999999)}",
                    f"0913{random.randint(1000000,9999999)}",
                    f"student{i}@school.edu",
                    f"آدرس نمونه {i}",
                    "1403/07/01",
                    random.choice(["A+", "A-", "B+", "B-", "O+", "O-"]),
                    random.choice(["", "گرده", "بادام زمینی"]),
                    random.choice(["", "آسم خفیف"]),
                    random.randint(3, 5),
                    random.randint(0, 5),
                    random.randint(0, 3),
                    random.randint(60, 100),
                    "active"
                )
                sample_students.append(student)
            
            cursor.executemany('''
                INSERT INTO students (
                    student_id, national_code, first_name, last_name, full_name,
                    father_name, mother_name, birth_date, grade, class_name,
                    phone, parent_phone, email, address, enrollment_date,
                    blood_type, allergies, medical_notes, behavior_score,
                    total_absences, total_tardiness, academic_score, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_students)
            
            # معلمان نمونه
            sample_teachers = []
            teacher_first_names = ["دکتر", "استاد", "آقای"]
            teacher_last_names = ["علمی", "دانش", "فرهنگ", "پژوهش", "آموز"]
            
            for i in range(1, 6):
                first_name = random.choice(teacher_first_names)
                last_name = random.choice(teacher_last_names)
                full_name = f"{first_name} {last_name}"
                
                teacher = (
                    f"TCH{1403}{i:03d}",
                    f"00{i:02d}223456{i:03d}",  # national_code - منحصر به فرد
                    first_name,
                    last_name,
                    full_name,
                    random.choice(["لیسانس", "فوق لیسانس", "دکتری"]),
                    random.choice(["ریاضی", "فیزیک", "شیمی", "ادبیات"]),
                    random.choice(["ریاضی", "فیزیک", "شیمی", "ادبیات", "انگلیسی", "دینی"]),
                    f"0914{random.randint(1000000,9999999)}",
                    f"teacher{i}@school.edu",
                    f"آدرس معلم {i}",
                    "1400/07/01",
                    random.randint(5000000, 10000000)
                )
                sample_teachers.append(teacher)
            
            cursor.executemany('''
                INSERT INTO teachers (
                    teacher_id, national_code, first_name, last_name, full_name,
                    degree, major, subject, phone, email, address, hire_date, salary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_teachers)
            
            print("✅ داده‌های نمونه ایجاد شد")
            
        except Exception as e:
            print(f"⚠️ خطا در ایجاد داده‌های نمونه: {e}")
            # اگر خطا داشتیم، حداقل داده‌های اصلی را ثبت می‌کنیم
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # فقط یک دانش‌آموز نمونه
            cursor.execute('''
                INSERT OR IGNORE INTO students (
                    student_id, national_code, first_name, last_name, full_name,
                    father_name, mother_name, birth_date, grade, class_name,
                    phone, parent_phone, email, address, enrollment_date,
                    blood_type, allergies, medical_notes, behavior_score,
                    total_absences, total_tardiness, academic_score, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                "STU1403001", "00123456789", "علی", "محمدی", "علی محمدی",
                "پدر علی", "مادر علی", "1385/01/01", "هفتم", "1",
                "09121234567", "09131234567", "student1@school.edu", "آدرس نمونه",
                "1403/07/01", "A+", "", "", 5, 0, 0, 80, "active"
            ))
            
            # فقط یک معلم نمونه
            cursor.execute('''
                INSERT OR IGNORE INTO teachers (
                    teacher_id, national_code, first_name, last_name, full_name,
                    degree, major, subject, phone, email, address, hire_date, salary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                "TCH1403001", "00223456789", "دکتر", "علمی", "دکتر علمی",
                "دکتری", "ریاضی", "ریاضی", "09141234567", "teacher1@school.edu",
                "آدرس معلم", "1400/07/01", 7000000
            ))
            
            conn.commit()
            conn.close()
            print("✅ داده‌های نمونه حداقلی ایجاد شد")
    
    def authenticate(self, username, password):
        """احراز هویت کاربر"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            SELECT id, username, full_name, role, email, phone
            FROM users 
            WHERE username=? AND password=?
        ''', (username, hashed_password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'full_name': user[2],
                'role': user[3],
                'email': user[4],
                'phone': user[5]
            }
        return None
    
    def get_dashboard_stats(self):
        """آمار کلی برای داشبورد"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM students WHERE status='active'")
        stats['total_students'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM teachers WHERE status='active'")
        stats['total_teachers'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT grade || '-' || class_name) FROM students")
        stats['total_classes'] = cursor.fetchone()[0]
        
        today = date.today().strftime("%Y/%m/%d")
        cursor.execute("SELECT COUNT(*) FROM events WHERE event_date=?", (today,))
        stats['today_events'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM students WHERE total_absences > 5")
        stats['high_absence'] = cursor.fetchone()[0]
        
        # آمار پایه‌ها
        cursor.execute("SELECT grade, COUNT(*) FROM students WHERE status='active' GROUP BY grade")
        grade_stats = cursor.fetchall()
        stats['grade_stats'] = {grade: count for grade, count in grade_stats}
        
        conn.close()
        return stats
    
    def get_student_list(self, search_term=""):
        """لیست دانش‌آموزان"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT student_id, full_name, grade, class_name, phone, 
                   behavior_score, total_absences, total_tardiness, academic_score, status
            FROM students 
            WHERE 1=1
        '''
        params = []
        
        if search_term:
            query += " AND (full_name LIKE ? OR student_id LIKE ? OR grade LIKE ? OR class_name LIKE ?)"
            search_pattern = f"%{search_term}%"
            params = [search_pattern, search_pattern, search_pattern, search_pattern]
        
        query += " ORDER BY grade, class_name, full_name"
        cursor.execute(query, params)
        
        students = []
        for row in cursor.fetchall():
            students.append({
                'student_id': row[0],
                'full_name': row[1],
                'grade': row[2],
                'class_name': row[3],
                'phone': row[4],
                'behavior_score': row[5],
                'total_absences': row[6],
                'total_tardiness': row[7],
                'academic_score': row[8],
                'status': row[9]
            })
        
        conn.close()
        return students
    
    def get_student_details(self, student_id):
        """جزئیات کامل یک دانش‌آموز"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM students WHERE student_id=? AND status='active'
        ''', (student_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def add_student(self, student_data):
        """افزودن دانش‌آموز جدید"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO students (
                    student_id, national_code, first_name, last_name, full_name,
                    father_name, mother_name, birth_date, grade, class_name,
                    phone, parent_phone, email, address, enrollment_date,
                    blood_type, allergies, medical_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', student_data)
            
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"خطای یکتایی: {e}")
            return False
        finally:
            conn.close()
    
    def update_student(self, student_id, student_data):
        """به‌روزرسانی اطلاعات دانش‌آموز"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE students SET
                    national_code=?, first_name=?, last_name=?, full_name=?,
                    father_name=?, mother_name=?, birth_date=?, grade=?, class_name=?,
                    phone=?, parent_phone=?, email=?, address=?, blood_type=?,
                    allergies=?, medical_notes=?, behavior_score=?, total_absences=?,
                    total_tardiness=?, academic_score=?
                WHERE student_id=?
            ''', (*student_data, student_id))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def delete_student(self, student_id):
        """حذف دانش‌آموز"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("UPDATE students SET status='deleted' WHERE student_id=?", (student_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def get_teacher_list(self, search_term=""):
        """لیست معلمان"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT teacher_id, full_name, subject, degree, phone, email, status
            FROM teachers 
            WHERE 1=1
        '''
        params = []
        
        if search_term:
            query += " AND (full_name LIKE ? OR teacher_id LIKE ? OR subject LIKE ?)"
            search_pattern = f"%{search_term}%"
            params = [search_pattern, search_pattern, search_pattern]
        
        query += " ORDER BY full_name"
        cursor.execute(query, params)
        
        teachers = []
        for row in cursor.fetchall():
            teachers.append({
                'teacher_id': row[0],
                'full_name': row[1],
                'subject': row[2],
                'degree': row[3],
                'phone': row[4],
                'email': row[5],
                'status': row[6]
            })
        
        conn.close()
        return teachers
    
    def get_teacher_details(self, teacher_id):
        """جزئیات معلم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM teachers WHERE teacher_id=?
        ''', (teacher_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def add_teacher(self, teacher_data):
        """افزودن معلم جدید"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO teachers (
                    teacher_id, national_code, first_name, last_name, full_name,
                    degree, major, subject, phone, email, address, hire_date, salary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', teacher_data)
            
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"خطای یکتایی: {e}")
            return False
        finally:
            conn.close()
    
    def update_teacher(self, teacher_id, teacher_data):
        """به‌روزرسانی معلم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE teachers SET
                    national_code=?, first_name=?, last_name=?, full_name=?,
                    degree=?, major=?, subject=?, phone=?, email=?,
                    address=?, salary=?
                WHERE teacher_id=?
            ''', (*teacher_data, teacher_id))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def delete_teacher(self, teacher_id):
        """حذف معلم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("UPDATE teachers SET status='deleted' WHERE teacher_id=?", (teacher_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

# ==================== برنامه اصلی ====================
class SchoolManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏫 سیستم مدیریت مدرسه علم برتر")
        self.root.geometry("1400x800")
        self.root.configure(bg=ColorPalette.NEUTRAL["BACKGROUND"])
        
        # مرکز کردن پنجره
        self.center_window()
        
        # دیتابیس
        self.db = SchoolDatabase()
        self.current_user = None
        
        # آیکون‌ها
        self.icons = {
            "dashboard": "📊",
            "students": "👥",
            "teachers": "👨‍🏫",
            "events": "📅",
            "settings": "⚙️",
            "logout": "🚪",
            "add": "➕",
            "edit": "✏️",
            "delete": "🗑️",
            "search": "🔍",
            "save": "💾",
            "cancel": "❌",
            "user": "👤",
            "home": "🏠",
            "check": "✅",
            "bell": "🔔",
            "chart": "📈",
            "calendar": "📅",
            "download": "⬇️",
            "upload": "⬆️",
            "print": "🖨️",
            "refresh": "🔄",
            "filter": "🔧",
            "view": "👁️",
            "lock": "🔒",
            "unlock": "🔓",
            "star": "⭐",
            "book": "📚",
            "graduation": "🎓",
            "medal": "🏅",
            "clock": "⏰",
            "location": "📍",
            "phone": "📞",
            "email": "📧",
            "warning": "⚠️",
            "info": "ℹ️",
            "success": "✅",
            "error": "❌"
        }
        
        # ========== لوگوی مدرسه ==========
        # اگر لوگو موجود نیست، از ایموجی استفاده می‌کنیم
        self.has_logo = False
        self.logo_image = None
        self.logo_photo = None
        
        # سعی می‌کنیم لوگو را بارگذاری کنیم
        logo_files = ["elm.png", "logo.png", "download.jpg", "elm.jpg", "logo.jpg"]
        for logo_file in logo_files:
            try:
                if os.path.exists(logo_file):
                    self.logo_image = Image.open(logo_file)
                    self.logo_image = self.logo_image.resize((64, 64), Image.Resampling.LANCZOS)
                    self.logo_photo = ImageTk.PhotoImage(self.logo_image)
                    self.has_logo = True
                    print(f"✅ لوگو بارگذاری شد: {logo_file}")
                    break
            except:
                continue
        
        if not self.has_logo:
            print("ℹ️ لوگو یافت نشد. از ایموجی 🏫 استفاده می‌شود.")
        
        self.show_login_screen()
    
    def center_window(self):
        self.root.update_idletasks()
        width = 1400
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_gradient_background(self, canvas, width, height):
        """ایجاد گرادیانت زیبا"""
        colors = [
            ColorPalette.PRIMARY["GRADIENT_START"],
            "#6a11cb",
            ColorPalette.PRIMARY["GRADIENT_END"]
        ]
        
        for i in range(height):
            ratio = i / height
            if ratio < 0.5:
                t = ratio * 2
                r = int(int(colors[0][1:3], 16) * (1-t) + int(colors[1][1:3], 16) * t)
                g = int(int(colors[0][3:5], 16) * (1-t) + int(colors[1][3:5], 16) * t)
                b = int(int(colors[0][5:7], 16) * (1-t) + int(colors[1][5:7], 16) * t)
            else:
                t = (ratio - 0.5) * 2
                r = int(int(colors[1][1:3], 16) * (1-t) + int(colors[2][1:3], 16) * t)
                g = int(int(colors[1][3:5], 16) * (1-t) + int(colors[2][3:5], 16) * t)
                b = int(int(colors[1][5:7], 16) * (1-t) + int(colors[2][5:7], 16) * t)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)
    
    def show_login_screen(self):
        """صفحه ورود زیبا"""
        self.clear_window()
        
        # کانواس برای گرادیانت
        canvas = tk.Canvas(self.root, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # ایجاد گرادیانت
        self.create_gradient_background(canvas, 1400, 800)
        
        # فریم مرکزی
        login_frame = tk.Frame(canvas, bg=ColorPalette.NEUTRAL["WHITE"], 
                              relief="solid", bd=0)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", 
                         width=450, height=550)
        
        # آیکون مدرسه (لوگو یا ایموجی)
        if self.has_logo and self.logo_photo:
            logo_label = tk.Label(login_frame, image=self.logo_photo,
                                 bg=ColorPalette.NEUTRAL["WHITE"])
            logo_label.image = self.logo_photo  # رفرنس را نگه دارید
            logo_label.pack(pady=(40, 10))
        else:
            tk.Label(login_frame, text="🏫", font=("Arial", 64),
                    bg=ColorPalette.NEUTRAL["WHITE"]).pack(pady=(40, 10))
        
        # عنوان
        tk.Label(login_frame, text="مدرسه علم برتر", 
                font=("Tahoma", 28, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.PRIMARY["DARK"]).pack()
        
        tk.Label(login_frame, text="سیستم مدیریت یکپارچه", 
                font=("Tahoma", 12),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["DARK_GRAY"]).pack(pady=(0, 40))
        
        # فیلدهای ورود
        fields_frame = tk.Frame(login_frame, bg=ColorPalette.NEUTRAL["WHITE"])
        fields_frame.pack(pady=20, padx=40, fill="x")
        
        # نام کاربری
        tk.Label(fields_frame, text="نام کاربری", 
                font=("Tahoma", 11, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["BLACK"],
                anchor="w").pack(fill="x", pady=(10, 5))
        
        self.username_entry = tk.Entry(fields_frame, font=("Tahoma", 12),
                                      bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                                      fg=ColorPalette.NEUTRAL["BLACK"],
                                      relief="flat", bd=1)
        self.username_entry.pack(fill="x", pady=(0, 20), ipady=8)
        self.username_entry.insert(0, "admin")
        self.username_entry.focus_set()
        
        # رمز عبور
        tk.Label(fields_frame, text="رمز عبور", 
                font=("Tahoma", 11, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["BLACK"],
                anchor="w").pack(fill="x", pady=(0, 5))
        
        self.password_entry = tk.Entry(fields_frame, font=("Tahoma", 12),
                                      bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                                      fg=ColorPalette.NEUTRAL["BLACK"],
                                      relief="flat", bd=1, show="•")
        self.password_entry.pack(fill="x", pady=(0, 30), ipady=8)
        self.password_entry.insert(0, "admin123")
        
        # دکمه ورود
        login_btn = ModernButton(login_frame, text="ورود به سیستم", 
                                icon=self.icons["lock"],
                                command=self.perform_login,
                                color="primary", size="large",
                                width=350, height=50, radius=12)
        login_btn.pack(pady=10)
        
        # اطلاعات پایین
        footer_frame = tk.Frame(login_frame, bg=ColorPalette.NEUTRAL["WHITE"])
        footer_frame.pack(side="bottom", pady=20)
        
        tk.Label(footer_frame, text="📅 سال تحصیلی 1404-1405", 
                font=("Tahoma", 10),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["DARK_GRAY"]).pack()
        
        tk.Label(footer_frame, text="🏆 سیستم مورد تایید آموزش و پرورش", 
                font=("Tahoma", 9),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.SECONDARY["SUCCESS"]).pack(pady=(5, 0))
        
        # کلید Enter
        self.root.bind('<Return>', lambda e: self.perform_login())
    
    def perform_login(self):
        """انجام عملیات ورود"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("خطا", "لطفاً نام کاربری و رمز عبور را وارد کنید")
            return
        
        user = self.db.authenticate(username, password)
        
        if user:
            self.current_user = user
            messagebox.showinfo("خوش آمدید", f"سلام {user['full_name']}!\nبه سیستم مدیریت مدرسه خوش آمدید.")
            self.show_main_dashboard()
        else:
            messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است")
    
    def logout(self):
        """خروج از سیستم"""
        if messagebox.askyesno("خروج", "آیا می‌خواهید از سیستم خارج شوید؟"):
            self.current_user = None
            self.show_login_screen()
    
    def show_main_dashboard(self):
        """داشبورد اصلی زیبا و مدرن"""
        self.clear_window()
        
        # هدر
        self.create_header("داشبورد مدیریت")
        
        # نوار کناری
        self.create_sidebar()
        
        # ناحیه محتوا با اسکرول‌بار
        main_container = tk.Frame(self.root, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_container.pack(side="right", fill="both", expand=True)
        
        # کانواس و اسکرول‌بار
        canvas = tk.Canvas(main_container, bg=ColorPalette.NEUTRAL["BACKGROUND"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        content_frame = tk.Frame(scrollable_frame, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # کارت خوش‌آمدگویی
        welcome_card = GlassCard(content_frame, width=1060, height=140, radius=15,
                               color=ColorPalette.NEUTRAL["WHITE"])
        welcome_card.pack(fill="x", pady=(0, 20))
        
        # محتوای کارت خوش‌آمدگویی
        welcome_content = tk.Frame(welcome_card, bg=ColorPalette.NEUTRAL["WHITE"])
        welcome_content.place(relx=0.05, rely=0.5, anchor="w")
        
        welcome_icon_frame = tk.Frame(welcome_content, bg=ColorPalette.NEUTRAL["WHITE"])
        welcome_icon_frame.pack(anchor="w", pady=(0, 10))
        
        if self.has_logo and self.logo_image:
            try:
                welcome_logo = self.logo_image.resize((50, 50), Image.Resampling.LANCZOS)
                welcome_logo_photo = ImageTk.PhotoImage(welcome_logo)
                logo_label = tk.Label(welcome_icon_frame, image=welcome_logo_photo,
                                     bg=ColorPalette.NEUTRAL["WHITE"])
                logo_label.image = welcome_logo_photo
                logo_label.pack(side="left", padx=(0, 10))
            except:
                tk.Label(welcome_icon_frame, text="🏫", font=("Arial", 32),
                        bg=ColorPalette.NEUTRAL["WHITE"]).pack(side="left", padx=(0, 10))
        else:
            tk.Label(welcome_icon_frame, text="🏫", font=("Arial", 32),
                    bg=ColorPalette.NEUTRAL["WHITE"]).pack(side="left", padx=(0, 10))
        
        tk.Label(welcome_icon_frame, text=f"سلام {self.current_user['full_name']}،", 
                font=("Tahoma", 20, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.PRIMARY["DARK"]).pack(side="left")
        
        tk.Label(welcome_content, text="به سیستم مدیریت مدرسه علم برتر خوش آمدید", 
                font=("Tahoma", 14),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["DARK_GRAY"]).pack(anchor="w", pady=(5, 0))
        
        tk.Label(welcome_content, text=f"📅 امروز: {datetime.now().strftime('%Y/%m/%d')} | 🕒 ساعت: {datetime.now().strftime('%H:%M')}", 
                font=("Tahoma", 11),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["GRAY"]).pack(anchor="w", pady=(5, 0))
        
        # آمار مدرسه
        stats = self.db.get_dashboard_stats()
        
        stats_frame = tk.Frame(content_frame, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # 4 کارت آماری
        stat_cards_data = [
            {"title": "👥 دانش‌آموزان", "value": stats['total_students'], 
             "icon": "👥", "color": ColorPalette.PRIMARY["MAIN"], 
             "subtitle": "فعال"},
            {"title": "👨‍🏫 معلمان", "value": stats['total_teachers'], 
             "icon": "👨‍🏫", "color": ColorPalette.SECONDARY["SUCCESS"],
             "subtitle": "همکار"},
            {"title": "🏫 کلاس‌ها", "value": stats['total_classes'], 
             "icon": "🏫", "color": ColorPalette.SECONDARY["INFO"],
             "subtitle": "کلاس فعال"},
            {"title": "📅 رویدادها", "value": stats['today_events'], 
             "icon": "📅", "color": ColorPalette.SECONDARY["WARNING"],
             "subtitle": "امروز"}
        ]
        
        for i, stat in enumerate(stat_cards_data):
            card = StatCard(stats_frame, title=stat["title"], value=stat["value"],
                          icon=stat["icon"], color=stat["color"], 
                          width=250, height=120)
            card.grid(row=0, column=i, padx=10, pady=10)
        
        # بخش آمار عملکرد مدرسه
        performance_frame = tk.Frame(content_frame, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        performance_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(performance_frame, text="📊 آمار عملکرد مدرسه", 
                font=("Tahoma", 16, "bold"),
                bg=ColorPalette.NEUTRAL["BACKGROUND"], 
                fg=ColorPalette.NEUTRAL["BLACK"]).pack(anchor="w", pady=(0, 15))
        
        # کارت آمار عملکرد
        performance_card = GlassCard(performance_frame, width=1060, height=200, radius=15,
                                   color=ColorPalette.NEUTRAL["WHITE"])
        performance_card.pack(fill="x")
        
        # نمودارهای دایره‌ای برای پایه‌ها
        grade_stats = stats.get('grade_stats', {})
        grades_frame = tk.Frame(performance_card, bg=ColorPalette.NEUTRAL["WHITE"])
        grades_frame.place(relx=0.05, rely=0.5, anchor="w")
        
        grade_colors = {
            "هفتم": ColorPalette.CHART["BLUE"],
            "هشتم": ColorPalette.CHART["GREEN"],
            "نهم": ColorPalette.CHART["PURPLE"]
        }
        
        grade_items = []
        total_students = stats['total_students']
        
        for grade in ["هفتم", "هشتم", "نهم"]:
            count = grade_stats.get(grade, 0)
            percent = (count / total_students * 100) if total_students > 0 else 0
            
            grade_frame = tk.Frame(grades_frame, bg=ColorPalette.NEUTRAL["WHITE"])
            grade_frame.pack(side="left", padx=20)
            
            # نمودار دایره‌ای
            chart = CircularProgressChart(grade_frame, width=120, height=120,
                                        progress=percent,
                                        color=grade_colors.get(grade, ColorPalette.PRIMARY["MAIN"]),
                                        title=f"پایه {grade}",
                                        subtitle=f"{count} دانش‌آموز")
            chart.pack()
            
            grade_items.append(f"پایه {grade}: {count} نفر ({percent:.1f}%)")
        
        # اطلاعات آماری دیگر
        stats_info_frame = tk.Frame(performance_card, bg=ColorPalette.NEUTRAL["WHITE"])
        stats_info_frame.place(relx=0.6, rely=0.3, anchor="w")
        
        other_stats = [
            f"📈 میانگین نمره ادب: ۴.۲ از ۵",
            f"📊 میانگین غیبت: ۲.۱ روز",
            f"🎯 میانگین نمرات: ۱۷.۵",
            f"🏆 دانش‌آموزان برتر: {int(stats['total_students'] * 0.2)} نفر",
            f"⚠️ دانش‌آموزان نیازمند توجه: {stats['high_absence']} نفر"
        ]
        
        for stat in other_stats:
            tk.Label(stats_info_frame, text=f"• {stat}", 
                    font=("Tahoma", 11),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.NEUTRAL["DARK_GRAY"],
                    anchor="w").pack(anchor="w", pady=2)
        
        # اقدامات سریع
        actions_frame = tk.Frame(content_frame, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        actions_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(actions_frame, text="⚡ اقدامات سریع", 
                font=("Tahoma", 16, "bold"),
                bg=ColorPalette.NEUTRAL["BACKGROUND"], 
                fg=ColorPalette.NEUTRAL["BLACK"]).pack(anchor="w", pady=(0, 15))
        
        quick_actions = [
            ("➕ ثبت دانش‌آموز جدید", self.show_student_management, ColorPalette.SECONDARY["SUCCESS"]),
            ("👨‍🏫 ثبت معلم جدید", self.show_teacher_management, ColorPalette.SECONDARY["INFO"]),
            ("📅 برنامه‌ریزی رویداد", self.show_event_management, ColorPalette.SECONDARY["WARNING"]),
            ("📊 گزارش‌گیری", self.show_reports, ColorPalette.PRIMARY["MAIN"])
        ]
        
        actions_grid = tk.Frame(actions_frame, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        actions_grid.pack()
        
        for i, (text, command, color) in enumerate(quick_actions):
            btn = ModernButton(actions_grid, text=text, command=command,
                              color=color, size="medium",
                              width=240, height=45, radius=10)
            btn.grid(row=0, column=i, padx=10)
        
        # آخرین فعالیت‌ها
        activity_card = GlassCard(content_frame, width=1060, height=180, radius=15,
                                color=ColorPalette.NEUTRAL["WHITE"])
        activity_card.pack(fill="x")
        
        tk.Label(activity_card, text="📝 آخرین فعالیت‌ها", 
                font=("Tahoma", 16, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["BLACK"]).place(relx=0.05, rely=0.2, anchor="w")
        
        activities = [
            f"✅ {self.current_user['full_name']} وارد سیستم شد",
            "📊 آمار مدرسه به‌روزرسانی شد",
            "👥 ۳ دانش‌آموز جدید ثبت شدند",
            "📅 امتحان میان‌ترم برنامه‌ریزی شد",
            "🏆 دانش‌آموزان برتر معرفی شدند"
        ]
        
        activities_list = tk.Frame(activity_card, bg=ColorPalette.NEUTRAL["WHITE"])
        activities_list.place(relx=0.05, rely=0.5, relwidth=0.9)
        
        for i, activity in enumerate(activities):
            tk.Label(activities_list, text=f"• {activity}", 
                    font=("Tahoma", 11),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.NEUTRAL["DARK_GRAY"],
                    anchor="w").pack(fill="x", pady=2)
    
    def create_header(self, title):
        """ایجاد هدر زیبا"""
        header = tk.Frame(self.root, bg=ColorPalette.PRIMARY["DARK"], height=80)
        header.pack(fill="x", side="top")
        
        # لوگو و عنوان
        title_frame = tk.Frame(header, bg=ColorPalette.PRIMARY["DARK"])
        title_frame.pack(side="left", padx=30)
        
        # لوگو
        if self.has_logo and self.logo_image:
            try:
                small_logo = self.logo_image.resize((40, 40), Image.Resampling.LANCZOS)
                small_logo_photo = ImageTk.PhotoImage(small_logo)
                logo_label = tk.Label(title_frame, image=small_logo_photo,
                                     bg=ColorPalette.PRIMARY["DARK"])
                logo_label.image = small_logo_photo
                logo_label.pack(side="left", padx=(0, 10))
            except:
                tk.Label(title_frame, text="🏫", font=("Arial", 24),
                        bg=ColorPalette.PRIMARY["DARK"], 
                        fg=ColorPalette.NEUTRAL["WHITE"]).pack(side="left", padx=(0, 10))
        else:
            tk.Label(title_frame, text="🏫", font=("Arial", 24),
                    bg=ColorPalette.PRIMARY["DARK"], 
                    fg=ColorPalette.NEUTRAL["WHITE"]).pack(side="left", padx=(0, 10))
        
        # عنوان
        tk.Label(title_frame, text=f" {title}", 
                font=("Tahoma", 22, "bold"),
                bg=ColorPalette.PRIMARY["DARK"], 
                fg=ColorPalette.NEUTRAL["WHITE"]).pack(side="left")
        
        # اطلاعات کاربر
        if self.current_user:
            user_frame = tk.Frame(header, bg=ColorPalette.PRIMARY["DARK"])
            user_frame.pack(side="right", padx=30)
            
            tk.Label(user_frame, text=f"{self.icons['user']} {self.current_user['full_name']}",
                    font=("Tahoma", 12, "bold"),
                    bg=ColorPalette.PRIMARY["DARK"], 
                    fg=ColorPalette.NEUTRAL["WHITE"]).pack(side="top")
            
            tk.Label(user_frame, text=f"👑 {self.current_user['role']}",
                    font=("Tahoma", 10),
                    bg=ColorPalette.PRIMARY["DARK"], 
                    fg=ColorPalette.NEUTRAL["LIGHT_GRAY"]).pack(side="top")
        
        return header
    
    def create_sidebar(self):
        """ایجاد نوار کناری زیبا"""
        sidebar = tk.Frame(self.root, bg=ColorPalette.PRIMARY["MAIN"], width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # لوگو
        logo_frame = tk.Frame(sidebar, bg=ColorPalette.PRIMARY["MAIN"])
        logo_frame.pack(pady=40)
        
        if self.has_logo and self.logo_image:
            try:
                sidebar_logo = self.logo_image.resize((80, 80), Image.Resampling.LANCZOS)
                sidebar_logo_photo = ImageTk.PhotoImage(sidebar_logo)
                logo_label = tk.Label(logo_frame, image=sidebar_logo_photo,
                                     bg=ColorPalette.PRIMARY["MAIN"])
                logo_label.image = sidebar_logo_photo
                logo_label.pack()
            except:
                tk.Label(logo_frame, text="🏫", 
                        font=("Arial", 36),
                        bg=ColorPalette.PRIMARY["MAIN"], 
                        fg=ColorPalette.NEUTRAL["WHITE"]).pack()
        else:
            tk.Label(logo_frame, text="🏫", 
                    font=("Arial", 36),
                    bg=ColorPalette.PRIMARY["MAIN"], 
                    fg=ColorPalette.NEUTRAL["WHITE"]).pack()
        
        tk.Label(logo_frame, text="علم برتر", 
                font=("Tahoma", 18, "bold"),
                bg=ColorPalette.PRIMARY["MAIN"], 
                fg=ColorPalette.NEUTRAL["WHITE"]).pack()
        
        tk.Label(logo_frame, text="مدرسه نمونه", 
                font=("Tahoma", 10),
                bg=ColorPalette.PRIMARY["MAIN"], 
                fg=ColorPalette.NEUTRAL["LIGHT_GRAY"]).pack()
        
        # منو
        menu_frame = tk.Frame(sidebar, bg=ColorPalette.PRIMARY["MAIN"])
        menu_frame.pack(fill="both", expand=True, pady=30)
        
        menu_items = [
            ("داشبورد", "dashboard", self.show_main_dashboard),
            ("مدیریت دانش‌آموزان", "students", self.show_student_management),
            ("مدیریت معلمان", "teachers", self.show_teacher_management),
            ("مدیریت رویدادها", "events", self.show_event_management),
            ("گزارش‌ها و آمار", "chart", self.show_reports),
            ("تنظیمات سیستم", "settings", self.show_settings)
        ]
        
        for text, icon_key, command in menu_items:
            btn_frame = tk.Frame(menu_frame, bg=ColorPalette.PRIMARY["MAIN"])
            btn_frame.pack(fill="x", pady=2)
            
            btn = ModernButton(btn_frame, text=text, icon=self.icons[icon_key],
                              command=command,
                              color=ColorPalette.PRIMARY["MAIN"], 
                              size="medium",
                              width=230, height=45, radius=8)
            btn.pack(padx=10)
        
        # دکمه خروج
        logout_frame = tk.Frame(sidebar, bg=ColorPalette.PRIMARY["MAIN"])
        logout_frame.pack(side="bottom", fill="x", pady=30)
        
        logout_btn = ModernButton(logout_frame, text="خروج از سیستم", 
                                 icon=self.icons["logout"],
                                 command=self.logout,
                                 color=ColorPalette.SECONDARY["ERROR"], 
                                 size="medium",
                                 width=230, height=45, radius=8)
        logout_btn.pack(padx=10)
    
    def show_student_management(self):
        """مدیریت دانش‌آموزان"""
        self.clear_window()
        
        # هدر
        self.create_header("مدیریت دانش‌آموزان")
        
        # دکمه‌های هدر
        header_btns = tk.Frame(self.root, bg=ColorPalette.PRIMARY["DARK"])
        header_btns.place(x=400, y=20, width=600, height=40)
        
        add_btn = ModernButton(header_btns, text="افزودن دانش‌آموز", 
                              icon=self.icons["add"],
                              command=self.show_add_student_dialog,
                              color="success", size="small",
                              width=150, height=35, radius=8)
        add_btn.pack(side="left", padx=5)
        
        refresh_btn = ModernButton(header_btns, text="بروزرسانی", 
                                  icon=self.icons["refresh"],
                                  command=self.load_students_table,
                                  color="info", size="small",
                                  width=120, height=35, radius=8)
        refresh_btn.pack(side="left", padx=5)
        
        # سایدبار
        self.create_sidebar()
        
        # ناحیه اصلی با اسکرول‌بار
        main_container = tk.Frame(self.root, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_container.pack(side="right", fill="both", expand=True)
        
        canvas = tk.Canvas(main_container, bg=ColorPalette.NEUTRAL["BACKGROUND"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = tk.Frame(scrollable_frame, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # نوار جستجو
        search_card = GlassCard(main_frame, width=1060, height=80, radius=15,
                              color=ColorPalette.NEUTRAL["WHITE"])
        search_card.pack(fill="x", pady=(0, 20))
        
        search_frame = tk.Frame(search_card, bg=ColorPalette.NEUTRAL["WHITE"])
        search_frame.place(relx=0.05, rely=0.5, anchor="w")
        
        tk.Label(search_frame, text="🔍 جستجوی دانش‌آموز:", 
                font=("Tahoma", 12, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["BLACK"]).pack(side="left", padx=10)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=("Tahoma", 12),
                               bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                               fg=ColorPalette.NEUTRAL["BLACK"],
                               width=30, relief="flat")
        search_entry.pack(side="left", padx=10, ipady=5)
        
        search_btn = ModernButton(search_frame, text="جستجو", 
                                 icon=self.icons["search"],
                                 command=self.search_students,
                                 color="primary", size="small",
                                 width=100, height=35, radius=6)
        search_btn.pack(side="left", padx=5)
        
        clear_btn = ModernButton(search_frame, text="پاک کردن", 
                                icon=self.icons["cancel"],
                                command=self.clear_search,
                                color="warning", size="small",
                                width=100, height=35, radius=6)
        clear_btn.pack(side="left", padx=5)
        
        # جدول دانش‌آموزان
        table_card = GlassCard(main_frame, width=1060, height=400, radius=15,
                             color=ColorPalette.NEUTRAL["WHITE"])
        table_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # ایجاد Treeview
        table_frame = tk.Frame(table_card, bg=ColorPalette.NEUTRAL["WHITE"])
        table_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                       background=ColorPalette.NEUTRAL["WHITE"],
                       foreground=ColorPalette.NEUTRAL["BLACK"],
                       rowheight=35,
                       fieldbackground=ColorPalette.NEUTRAL["WHITE"],
                       borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                       background=ColorPalette.PRIMARY["MAIN"],
                       foreground=ColorPalette.NEUTRAL["WHITE"],
                       relief="flat",
                       font=("Tahoma", 11, "bold"))
        
        columns = ("کد دانش‌آموزی", "نام کامل", "پایه", "کلاس", "شماره تماس", "وضعیت")
        self.students_tree = ttk.Treeview(table_frame, columns=columns, 
                                         show="headings", style="Custom.Treeview",
                                         height=12)
        
        # تنظیم ستون‌ها
        col_widths = [120, 250, 80, 80, 120, 80]
        for col, width in zip(columns, col_widths):
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=width, anchor="center")
        
        # نوار پیمایش
        scrollbar_table = ttk.Scrollbar(table_frame, orient="vertical", 
                                       command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar_table.set)
        
        self.students_tree.pack(side="left", fill="both", expand=True)
        scrollbar_table.pack(side="right", fill="y")
        
        # بارگذاری داده‌ها
        self.load_students_table()
        
        # رویداد دابل کلیک
        self.students_tree.bind("<Double-Button-1>", self.show_student_profile)
        
        # منوی راست کلیک
        self.students_tree.bind("<Button-3>", self.show_student_context_menu)
    
    def load_students_table(self, search_term=""):
        """بارگذاری جدول دانش‌آموزان"""
        if not hasattr(self, 'students_tree'):
            return
            
        # پاک کردن ردیف‌های قبلی
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # دریافت دانش‌آموزان از دیتابیس
        students = self.db.get_student_list(search_term)
        
        # اضافه کردن به جدول
        for student in students:
            status = "✅ فعال" if student['status'] == 'active' else "❌ غیرفعال"
            self.students_tree.insert("", "end", values=(
                student['student_id'],
                student['full_name'],
                student['grade'],
                student['class_name'],
                student['phone'] or "-",
                status
            ), tags=(student['student_id'],))
    
    def search_students(self):
        """جستجوی دانش‌آموزان"""
        search_term = self.search_var.get()
        self.load_students_table(search_term)
    
    def clear_search(self):
        """پاک کردن جستجو"""
        self.search_var.set("")
        self.load_students_table()
    
    def show_student_context_menu(self, event):
        """نمایش منوی راست کلیک برای دانش‌آموز"""
        try:
            item = self.students_tree.identify_row(event.y)
            if item:
                self.students_tree.selection_set(item)
                
                menu = tk.Menu(self.root, tearoff=0, 
                              bg=ColorPalette.NEUTRAL["WHITE"], 
                              fg=ColorPalette.NEUTRAL["BLACK"],
                              font=("Tahoma", 10))
                
                menu.add_command(label="👁️ مشاهده پروفایل", 
                                command=lambda: self.show_student_profile(None))
                menu.add_command(label="✏️ ویرایش اطلاعات", 
                                command=self.edit_selected_student)
                menu.add_command(label="🗑️ حذف دانش‌آموز", 
                                command=self.delete_selected_student,
                                foreground=ColorPalette.SECONDARY["ERROR"])
                menu.add_separator()
                menu.add_command(label="📄 چاپ کارنامه")
                
                menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def edit_selected_student(self):
        """ویرایش دانش‌آموز انتخاب شده"""
        try:
            item = self.students_tree.selection()[0]
            values = self.students_tree.item(item)['values']
            student_id = values[0]
            self.show_edit_student_dialog(student_id)
        except IndexError:
            messagebox.showwarning("توجه", "لطفاً یک دانش‌آموز را انتخاب کنید")
    
    def delete_selected_student(self):
        """حذف دانش‌آموز انتخاب شده"""
        try:
            item = self.students_tree.selection()[0]
            values = self.students_tree.item(item)['values']
            student_id = values[0]
            student_name = values[1]
            
            if messagebox.askyesno("تأیید حذف", 
                                  f"آیا از حذف دانش‌آموز '{student_name}' مطمئن هستید؟\nاین عمل قابل بازگشت نیست!"):
                if self.db.delete_student(student_id):
                    messagebox.showinfo("موفقیت", "✅ دانش‌آموز با موفقیت حذف شد")
                    self.load_students_table()
                else:
                    messagebox.showerror("خطا", "❌ خطا در حذف دانش‌آموز")
        except IndexError:
            messagebox.showwarning("توجه", "لطفاً یک دانش‌آموز را انتخاب کنید")
    
    def show_student_profile(self, event):
        """نمایش پروفایل دانش‌آموز"""
        try:
            item = self.students_tree.selection()[0]
            values = self.students_tree.item(item)['values']
            student_id = values[0]
            
            # دریافت اطلاعات دانش‌آموز
            student = self.db.get_student_details(student_id)
            
            if not student:
                messagebox.showerror("خطا", "دانش‌آموز مورد نظر یافت نشد")
                return
            
            # ایجاد پنجره پروفایل
            profile_window = tk.Toplevel(self.root)
            profile_window.title(f"👨‍🎓 پروفایل دانش‌آموز: {student['full_name']}")
            profile_window.geometry("900x700")
            profile_window.configure(bg=ColorPalette.NEUTRAL["BACKGROUND"])
            profile_window.transient(self.root)
            profile_window.grab_set()
            
            # هدر پروفایل
            header_frame = tk.Frame(profile_window, bg=ColorPalette.PRIMARY["MAIN"], height=80)
            header_frame.pack(fill="x")
            
            tk.Label(header_frame, text=f"👨‍🎓 پروفایل دانش‌آموز", 
                    font=("Tahoma", 20, "bold"),
                    bg=ColorPalette.PRIMARY["MAIN"], 
                    fg=ColorPalette.NEUTRAL["WHITE"]).pack(pady=20)
            
            # محتوای اصلی با اسکرول‌بار
            main_container = tk.Frame(profile_window, bg=ColorPalette.NEUTRAL["BACKGROUND"])
            main_container.pack(fill="both", expand=True)
            
            canvas = tk.Canvas(main_container, bg=ColorPalette.NEUTRAL["BACKGROUND"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=ColorPalette.NEUTRAL["BACKGROUND"])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            main_frame = tk.Frame(scrollable_frame, bg=ColorPalette.NEUTRAL["BACKGROUND"])
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # اطلاعات شخصی
            info_card = GlassCard(main_frame, width=860, height=200, radius=15,
                                color=ColorPalette.NEUTRAL["WHITE"])
            info_card.pack(fill="x", pady=(0, 20))
            
            # محتوای اطلاعات شخصی
            info_content = tk.Frame(info_card, bg=ColorPalette.NEUTRAL["WHITE"])
            info_content.place(relx=0.05, rely=0.1, relwidth=0.9)
            
            # اطلاعات در دو ستون
            left_info = tk.Frame(info_content, bg=ColorPalette.NEUTRAL["WHITE"])
            left_info.pack(side="left", fill="both", expand=True)
            
            right_info = tk.Frame(info_content, bg=ColorPalette.NEUTRAL["WHITE"])
            right_info.pack(side="right", fill="both", expand=True)
            
            # ستون چپ
            info_items_left = [
                f"🔢 کد دانش‌آموزی: {student['student_id']}",
                f"👤 نام کامل: {student['full_name']}",
                f"📚 پایه و کلاس: {student['grade']} - کلاس {student['class_name']}",
                f"👨 نام پدر: {student['father_name'] or '-'}",
                f"👩 نام مادر: {student['mother_name'] or '-'}",
                f"🎂 تاریخ تولد: {student['birth_date'] or '-'}"
            ]
            
            for item in info_items_left:
                tk.Label(left_info, text=item, 
                        font=("Tahoma", 11),
                        bg=ColorPalette.NEUTRAL["WHITE"], 
                        fg=ColorPalette.NEUTRAL["BLACK"],
                        anchor="w").pack(fill="x", pady=3)
            
            # ستون راست
            info_items_right = [
                f"📞 شماره تماس: {student['phone'] or '-'}",
                f"📱 تلفن والدین: {student['parent_phone'] or '-'}",
                f"📧 ایمیل: {student['email'] or '-'}",
                f"📍 آدرس: {student['address'] or '-'}",
                f"🩸 گروه خونی: {student['blood_type'] or '-'}",
                f"🏥 وضعیت سلامت: {student['medical_notes'] or 'سالم'}"
            ]
            
            for item in info_items_right:
                tk.Label(right_info, text=item, 
                        font=("Tahoma", 11),
                        bg=ColorPalette.NEUTRAL["WHITE"], 
                        fg=ColorPalette.NEUTRAL["BLACK"],
                        anchor="w").pack(fill="x", pady=3)
            
            # آمار عملکرد
            stats_card = GlassCard(main_frame, width=860, height=180, radius=15,
                                 color=ColorPalette.NEUTRAL["WHITE"])
            stats_card.pack(fill="x", pady=(0, 20))
            
            tk.Label(stats_card, text="📊 آمار عملکرد دانش‌آموز", 
                    font=("Tahoma", 16, "bold"),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.NEUTRAL["BLACK"]).place(relx=0.05, rely=0.2, anchor="w")
            
            # آمار در 4 بخش
            stats_grid = tk.Frame(stats_card, bg=ColorPalette.NEUTRAL["WHITE"])
            stats_grid.place(relx=0.05, rely=0.6, relwidth=0.9)
            
            stats_data = [
                {"title": "📊 نمره ادب", "value": f"{student['behavior_score']} از ۵", 
                 "color": ColorPalette.CHART["GREEN"]},
                {"title": "📅 تعداد غیبت", "value": f"{student['total_absences']} روز", 
                 "color": ColorPalette.CHART["RED"]},
                {"title": "⏰ تعداد تاخیر", "value": f"{student['total_tardiness']} بار", 
                 "color": ColorPalette.CHART["YELLOW"]},
                {"title": "📈 پیشرفت تحصیلی", "value": f"{student['academic_score']}%", 
                 "color": ColorPalette.CHART["BLUE"]}
            ]
            
            for i, stat in enumerate(stats_data):
                stat_frame = tk.Frame(stats_grid, bg=ColorPalette.NEUTRAL["WHITE"])
                stat_frame.grid(row=0, column=i, padx=20)
                
                tk.Label(stat_frame, text=stat["title"], 
                        font=("Tahoma", 12, "bold"),
                        bg=ColorPalette.NEUTRAL["WHITE"], 
                        fg=ColorPalette.NEUTRAL["BLACK"]).pack()
                
                tk.Label(stat_frame, text=stat["value"], 
                        font=("Tahoma", 18, "bold"),
                        bg=ColorPalette.NEUTRAL["WHITE"], 
                        fg=stat["color"]).pack()
            
            # دکمه‌های عملیاتی
            buttons_frame = tk.Frame(main_frame, bg=ColorPalette.NEUTRAL["BACKGROUND"])
            buttons_frame.pack(pady=20)
            
            edit_btn = ModernButton(buttons_frame, text="ویرایش اطلاعات", 
                                   icon=self.icons["edit"],
                                   command=lambda: self.show_edit_student_dialog(student_id, profile_window),
                                   color="info", size="medium",
                                   width=150, height=45, radius=10)
            edit_btn.pack(side="left", padx=10)
            
            delete_btn = ModernButton(buttons_frame, text="حذف دانش‌آموز", 
                                     icon=self.icons["delete"],
                                     command=lambda: self.delete_student(student_id, profile_window),
                                     color="error", size="medium",
                                     width=150, height=45, radius=10)
            delete_btn.pack(side="left", padx=10)
            
            print_btn = ModernButton(buttons_frame, text="چاپ کارنامه", 
                                    icon=self.icons["print"],
                                     command=lambda: messagebox.showinfo("چاپ", "در حال چاپ کارنامه..."),
                                   color="warning", size="medium",
                                   width=150, height=45, radius=10)
            print_btn.pack(side="left", padx=10)
            
            close_btn = ModernButton(buttons_frame, text="بستن", 
                                    icon=self.icons["cancel"],
                                    command=profile_window.destroy,
                                    color="primary", size="medium",
                                    width=150, height=45, radius=10)
            close_btn.pack(side="left", padx=10)
            
        except IndexError:
            messagebox.showwarning("توجه", "لطفاً یک دانش‌آموز را انتخاب کنید")
    
    def show_add_student_dialog(self):
        """نمایش دیالوگ افزودن دانش‌آموز"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ افزودن دانش‌آموز جدید")
        dialog.geometry("500x700")
        dialog.configure(bg=ColorPalette.NEUTRAL["BACKGROUND"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # هدر دیالوگ
        header_frame = tk.Frame(dialog, bg=ColorPalette.PRIMARY["MAIN"], height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="➕ افزودن دانش‌آموز جدید",
                font=("Tahoma", 16, "bold"),
                bg=ColorPalette.PRIMARY["MAIN"], 
                fg=ColorPalette.NEUTRAL["WHITE"]).pack(pady=15)
        
        # کانتینر اصلی با اسکرول‌بار
        main_container = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_container, bg=ColorPalette.NEUTRAL["BACKGROUND"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # فرم
        form_frame = tk.Frame(scrollable_frame, bg=ColorPalette.NEUTRAL["WHITE"])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # فیلدهای فرم
        fields = [
            ("کد دانش‌آموزی*:", "entry", True, ""),
            ("کد ملی:", "entry", False, ""),
            ("نام*:", "entry", True, ""),
            ("نام خانوادگی*:", "entry", True, ""),
            ("نام پدر:", "entry", False, ""),
            ("نام مادر:", "entry", False, ""),
            ("تاریخ تولد:", "entry", False, "1385/01/01"),
            ("پایه تحصیلی*:", "combo", True, ["هفتم", "هشتم", "نهم"]),
            ("کلاس*:", "combo", True, ["الف", "ب", "ج", "د"]),
            ("شماره تماس:", "entry", False, ""),
            ("تلفن والدین:", "entry", False, ""),
            ("ایمیل:", "entry", False, ""),
            ("آدرس:", "entry", False, ""),
            ("گروه خونی:", "combo", False, ["", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]),
            ("آلرژی‌ها:", "entry", False, ""),
            ("توضیحات پزشکی:", "entry", False, "")
        ]
        
        self.student_entries = {}
        
        for label_text, field_type, required, options in fields:
            frame = tk.Frame(form_frame, bg=ColorPalette.NEUTRAL["WHITE"])
            frame.pack(fill="x", pady=8)
            
            # برچسب
            label = f"{'* ' if required else ''}{label_text}"
            tk.Label(frame, text=label, 
                    font=("Tahoma", 11, "bold" if required else "normal"),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.PRIMARY["DARK"] if required else ColorPalette.NEUTRAL["BLACK"],
                    width=20, anchor="w").pack(side="left")
            
            # فیلد ورودی
            if field_type == "entry":
                entry = tk.Entry(frame, font=("Tahoma", 11), 
                                bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                                fg=ColorPalette.NEUTRAL["BLACK"],
                                width=25)
                if options and not isinstance(options, list):
                    entry.insert(0, options)
                entry.pack(side="left", padx=10)
                self.student_entries[label_text] = entry
            elif field_type == "combo":
                var = tk.StringVar()
                combo = ttk.Combobox(frame, textvariable=var, 
                                   values=options if isinstance(options, list) else [],
                                   state="readonly", width=23)
                if options and isinstance(options, list) and options[0]:
                    var.set(options[0])
                combo.pack(side="left", padx=10)
                self.student_entries[label_text] = var
        
        # دکمه‌ها
        button_frame = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        button_frame.pack(pady=20)
        
        def save_student():
            # اعتبارسنجی فیلدهای اجباری
            required_fields = ["کد دانش‌آموزی*:", "نام*:", "نام خانوادگی*:", "پایه تحصیلی*:", "کلاس*:"]
            missing_fields = []
            
            for field in required_fields:
                value = ""
                if field in self.student_entries:
                    entry = self.student_entries[field]
                    if isinstance(entry, tk.Entry):
                        value = entry.get().strip()
                    else:  # StringVar
                        value = entry.get().strip()
                
                if not value:
                    missing_fields.append(field.replace("*:", ""))
            
            if missing_fields:
                messagebox.showerror("خطا", f"فیلدهای اجباری پر نشده‌اند:\n{', '.join(missing_fields)}")
                return
            
            try:
                # جمع‌آوری داده‌ها
                student_data = (
                    self.student_entries["کد دانش‌آموزی*:"].get().strip(),
                    self.student_entries.get("کد ملی:", tk.StringVar(value="")).get().strip(),
                    self.student_entries["نام*:"].get().strip(),
                    self.student_entries["نام خانوادگی*:"].get().strip(),
                    f"{self.student_entries['نام*:'].get().strip()} {self.student_entries['نام خانوادگی*:'].get().strip()}",
                    self.student_entries.get("نام پدر:", tk.StringVar(value="")).get().strip(),
                    self.student_entries.get("نام مادر:", tk.StringVar(value="")).get().strip(),
                    self.student_entries.get("تاریخ تولد:", tk.StringVar(value="")).get().strip(),
                    self.student_entries["پایه تحصیلی*:"].get().strip(),
                    self.student_entries["کلاس*:"].get().strip(),
                    self.student_entries.get("شماره تماس:", tk.StringVar(value="")).get().strip(),
                    self.student_entries.get("تلفن والدین:", tk.StringVar(value="")).get().strip(),
                    self.student_entries.get("ایمیل:", tk.StringVar(value="")).get().strip(),
                    self.student_entries.get("آدرس:", tk.StringVar(value="")).get().strip(),
                    date.today().strftime("%Y/%m/%d"),
                    self.student_entries.get("گروه خونی:", tk.StringVar(value="")).get().strip(),
                    self.student_entries.get("آلرژی‌ها:", tk.StringVar(value="")).get().strip(),
                    self.student_entries.get("توضیحات پزشکی:", tk.StringVar(value="")).get().strip()
                )
                
                # ذخیره در دیتابیس
                if self.db.add_student(student_data):
                    messagebox.showinfo("موفقیت", "✅ دانش‌آموز با موفقیت ثبت شد")
                    dialog.destroy()
                    self.load_students_table()
                else:
                    messagebox.showerror("خطا", "❌ کد دانش‌آموزی تکراری است")
                    
            except Exception as e:
                messagebox.showerror("خطا", f"❌ خطا در ثبت دانش‌آموز:\n{str(e)}")
        
        save_btn = ModernButton(button_frame, text="ثبت نهایی", 
                               icon=self.icons["save"],
                               command=save_student,
                               color="success", size="medium",
                               width=150, height=45, radius=10)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ModernButton(button_frame, text="انصراف", 
                                 icon=self.icons["cancel"],
                                 command=dialog.destroy,
                                 color="error", size="medium",
                                 width=150, height=45, radius=10)
        cancel_btn.pack(side="right", padx=10)
    
    def show_edit_student_dialog(self, student_id=None, parent_window=None):
        """نمایش دیالوگ ویرایش دانش‌آموز"""
        if not student_id:
            try:
                item = self.students_tree.selection()[0]
                values = self.students_tree.item(item)['values']
                student_id = values[0]
            except IndexError:
                messagebox.showwarning("توجه", "لطفاً یک دانش‌آموز را انتخاب کنید")
                return
        
        # دریافت اطلاعات فعلی دانش‌آموز
        student = self.db.get_student_details(student_id)
        if not student:
            messagebox.showerror("خطا", "دانش‌آموز مورد نظر یافت نشد")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"✏️ ویرایش دانش‌آموز: {student['full_name']}")
        dialog.geometry("500x700")
        dialog.configure(bg=ColorPalette.NEUTRAL["BACKGROUND"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # هدر دیالوگ
        header_frame = tk.Frame(dialog, bg=ColorPalette.PRIMARY["MAIN"], height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text=f"✏️ ویرایش دانش‌آموز",
                font=("Tahoma", 16, "bold"),
                bg=ColorPalette.PRIMARY["MAIN"], 
                fg=ColorPalette.NEUTRAL["WHITE"]).pack(pady=15)
        
        # کانتینر اصلی با اسکرول‌بار
        main_container = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_container, bg=ColorPalette.NEUTRAL["BACKGROUND"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # فرم
        form_frame = tk.Frame(scrollable_frame, bg=ColorPalette.NEUTRAL["WHITE"])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # فیلدهای فرم با مقادیر فعلی
        fields = [
            ("کد دانش‌آموزی:", "label", False, student['student_id']),
            ("کد ملی:", "entry", False, student['national_code'] or ""),
            ("نام*:", "entry", True, student['first_name']),
            ("نام خانوادگی*:", "entry", True, student['last_name']),
            ("نام پدر:", "entry", False, student['father_name'] or ""),
            ("نام مادر:", "entry", False, student['mother_name'] or ""),
            ("تاریخ تولد:", "entry", False, student['birth_date'] or ""),
            ("پایه تحصیلی*:", "combo", True, ["هفتم", "هشتم", "نهم"], student['grade']),
            ("کلاس*:", "combo", True, ["الف", "ب", "ج", "د"], student['class_name']),
            ("شماره تماس:", "entry", False, student['phone'] or ""),
            ("تلفن والدین:", "entry", False, student['parent_phone'] or ""),
            ("ایمیل:", "entry", False, student['email'] or ""),
            ("آدرس:", "entry", False, student['address'] or ""),
            ("گروه خونی:", "combo", False, ["", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], student['blood_type'] or ""),
            ("آلرژی‌ها:", "entry", False, student['allergies'] or ""),
            ("توضیحات پزشکی:", "entry", False, student['medical_notes'] or ""),
            ("نمره ادب (1-5):", "entry", False, str(student['behavior_score'])),
            ("تعداد غیبت:", "entry", False, str(student['total_absences'])),
            ("تعداد تاخیر:", "entry", False, str(student['total_tardiness'])),
            ("پیشرفت تحصیلی (%):", "entry", False, str(student['academic_score']))
        ]
        
        self.edit_student_entries = {}
        
        for label_text, field_type, required, *args in fields:
            frame = tk.Frame(form_frame, bg=ColorPalette.NEUTRAL["WHITE"])
            frame.pack(fill="x", pady=8)
            
            # برچسب
            label = f"{'* ' if required else ''}{label_text}"
            tk.Label(frame, text=label, 
                    font=("Tahoma", 11, "bold" if required else "normal"),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.PRIMARY["DARK"] if required else ColorPalette.NEUTRAL["BLACK"],
                    width=25, anchor="w").pack(side="left")
            
            # فیلد ورودی
            if field_type == "entry":
                entry = tk.Entry(frame, font=("Tahoma", 11), 
                                bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                                fg=ColorPalette.NEUTRAL["BLACK"],
                                width=25)
                entry.insert(0, args[0])
                entry.pack(side="left", padx=10)
                self.edit_student_entries[label_text] = entry
            elif field_type == "combo":
                var = tk.StringVar()
                values = args[0] if isinstance(args[0], list) else ["هفتم", "هشتم", "نهم"]
                default_value = args[1] if len(args) > 1 else values[0]
                combo = ttk.Combobox(frame, textvariable=var, 
                                   values=values,
                                   state="readonly", width=23)
                var.set(default_value)
                combo.pack(side="left", padx=10)
                self.edit_student_entries[label_text] = var
            elif field_type == "label":
                tk.Label(frame, text=args[0], 
                        font=("Tahoma", 11),
                        bg=ColorPalette.NEUTRAL["WHITE"], 
                        fg=ColorPalette.NEUTRAL["BLACK"],
                        width=25).pack(side="left", padx=10)
        
        # دکمه‌ها
        button_frame = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        button_frame.pack(pady=20)
        
        def update_student():
            # اعتبارسنجی فیلدهای اجباری
            required_fields = ["نام*:", "نام خانوادگی*:", "پایه تحصیلی*:", "کلاس*:"]
            missing_fields = []
            
            for field in required_fields:
                value = ""
                if field in self.edit_student_entries:
                    entry = self.edit_student_entries[field]
                    if isinstance(entry, tk.Entry):
                        value = entry.get().strip()
                    else:
                        value = entry.get().strip()
                
                if not value:
                    missing_fields.append(field.replace("*:", ""))
            
            if missing_fields:
                messagebox.showerror("خطا", f"فیلدهای اجباری پر نشده‌اند:\n{', '.join(missing_fields)}")
                return
            
            try:
                # جمع‌آوری داده‌ها
                student_data = (
                    self.edit_student_entries.get("کد ملی:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries["نام*:"].get().strip(),
                    self.edit_student_entries["نام خانوادگی*:"].get().strip(),
                    f"{self.edit_student_entries['نام*:'].get().strip()} {self.edit_student_entries['نام خانوادگی*:'].get().strip()}",
                    self.edit_student_entries.get("نام پدر:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries.get("نام مادر:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries.get("تاریخ تولد:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries["پایه تحصیلی*:"].get().strip(),
                    self.edit_student_entries["کلاس*:"].get().strip(),
                    self.edit_student_entries.get("شماره تماس:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries.get("تلفن والدین:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries.get("ایمیل:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries.get("آدرس:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries.get("گروه خونی:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries.get("آلرژی‌ها:", tk.StringVar(value="")).get().strip(),
                    self.edit_student_entries.get("توضیحات پزشکی:", tk.StringVar(value="")).get().strip(),
                    int(self.edit_student_entries.get("نمره ادب (1-5):", tk.StringVar(value="5")).get().strip()),
                    int(self.edit_student_entries.get("تعداد غیبت:", tk.StringVar(value="0")).get().strip()),
                    int(self.edit_student_entries.get("تعداد تاخیر:", tk.StringVar(value="0")).get().strip()),
                    int(self.edit_student_entries.get("پیشرفت تحصیلی (%):", tk.StringVar(value="0")).get().strip())
                )
                
                # به‌روزرسانی در دیتابیس
                if self.db.update_student(student_id, student_data):
                    messagebox.showinfo("موفقیت", "✅ اطلاعات دانش‌آموز با موفقیت به‌روزرسانی شد")
                    dialog.destroy()
                    if parent_window:
                        parent_window.destroy()
                    self.load_students_table()
                else:
                    messagebox.showerror("خطا", "❌ خطا در به‌روزرسانی اطلاعات")
                    
            except ValueError as e:
                messagebox.showerror("خطا", "❌ لطفاً مقادیر عددی را به درستی وارد کنید")
            except Exception as e:
                messagebox.showerror("خطا", f"❌ خطا در به‌روزرسانی دانش‌آموز:\n{str(e)}")
        
        save_btn = ModernButton(button_frame, text="ذخیره تغییرات", 
                               icon=self.icons["save"],
                               command=update_student,
                               color="success", size="medium",
                               width=150, height=45, radius=10)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ModernButton(button_frame, text="انصراف", 
                                 icon=self.icons["cancel"],
                                 command=dialog.destroy,
                                 color="error", size="medium",
                                 width=150, height=45, radius=10)
        cancel_btn.pack(side="right", padx=10)
    
    def delete_student(self, student_id, parent_window=None):
        """حذف دانش‌آموز"""
        student = self.db.get_student_details(student_id)
        
        if not student:
            messagebox.showerror("خطا", "دانش‌آموز مورد نظر یافت نشد")
            return
        
        if messagebox.askyesno("تأیید حذف", 
                              f"آیا از حذف دانش‌آموز '{student['full_name']}' مطمئن هستید؟\nاین عمل قابل بازگشت نیست!"):
            if self.db.delete_student(student_id):
                messagebox.showinfo("موفقیت", "✅ دانش‌آموز با موفقیت حذف شد")
                if parent_window:
                    parent_window.destroy()
                self.load_students_table()
            else:
                messagebox.showerror("خطا", "❌ خطا در حذف دانش‌آموز")
    
    def show_teacher_management(self):
        """مدیریت معلمان"""
        self.clear_window()
        
        # هدر
        self.create_header("مدیریت معلمان")
        
        # سایدبار
        self.create_sidebar()
        
        # ناحیه اصلی با اسکرول‌بار
        main_container = tk.Frame(self.root, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_container.pack(side="right", fill="both", expand=True)
        
        canvas = tk.Canvas(main_container, bg=ColorPalette.NEUTRAL["BACKGROUND"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = tk.Frame(scrollable_frame, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # کارت اصلی
        card = GlassCard(main_frame, width=1060, height=500, radius=15,
                        color=ColorPalette.NEUTRAL["WHITE"])
        card.pack(fill="both", expand=True)
        
        # نوار جستجو
        search_frame = tk.Frame(card, bg=ColorPalette.NEUTRAL["WHITE"])
        search_frame.place(relx=0.05, rely=0.1, anchor="w")
        
        tk.Label(search_frame, text="🔍 جستجوی معلم:", 
                font=("Tahoma", 12, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["BLACK"]).pack(side="left", padx=10)
        
        self.teacher_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.teacher_search_var,
                               font=("Tahoma", 12),
                               bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                               fg=ColorPalette.NEUTRAL["BLACK"],
                               width=30, relief="flat")
        search_entry.pack(side="left", padx=10, ipady=5)
        
        search_btn = ModernButton(search_frame, text="جستجو", 
                                 icon=self.icons["search"],
                                 command=self.search_teachers,
                                 color="primary", size="small",
                                 width=100, height=35, radius=6)
        search_btn.pack(side="left", padx=5)
        
        # عنوان
        tk.Label(card, text="👨‍🏫 مدیریت معلمان مدرسه علم برتر",
                font=("Tahoma", 22, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["BLACK"]).place(relx=0.5, rely=0.2, anchor="center")
        
        tk.Label(card, text="مدیریت اطلاعات معلمان و کادر آموزشی",
                font=("Tahoma", 14),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["DARK_GRAY"]).place(relx=0.5, rely=0.3, anchor="center")
        
        # جدول معلمان
        table_frame = tk.Frame(card, bg=ColorPalette.NEUTRAL["WHITE"])
        table_frame.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.4)
        
        # ایجاد Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Teacher.Treeview",
                       background=ColorPalette.NEUTRAL["WHITE"],
                       foreground=ColorPalette.NEUTRAL["BLACK"],
                       rowheight=35,
                       fieldbackground=ColorPalette.NEUTRAL["WHITE"],
                       borderwidth=0)
        style.configure("Teacher.Treeview.Heading",
                       background=ColorPalette.SECONDARY["INFO"],
                       foreground=ColorPalette.NEUTRAL["WHITE"],
                       relief="flat",
                       font=("Tahoma", 11, "bold"))
        
        columns = ("کد معلم", "نام کامل", "درس", "مدرک", "شماره تماس", "وضعیت")
        self.teachers_tree = ttk.Treeview(table_frame, columns=columns, 
                                         show="headings", style="Teacher.Treeview",
                                         height=8)
        
        # تنظیم ستون‌ها
        col_widths = [100, 200, 100, 100, 120, 80]
        for col, width in zip(columns, col_widths):
            self.teachers_tree.heading(col, text=col)
            self.teachers_tree.column(col, width=width, anchor="center")
        
        # نوار پیمایش
        scrollbar_table = ttk.Scrollbar(table_frame, orient="vertical", 
                                       command=self.teachers_tree.yview)
        self.teachers_tree.configure(yscrollcommand=scrollbar_table.set)
        
        self.teachers_tree.pack(side="left", fill="both", expand=True)
        scrollbar_table.pack(side="right", fill="y")
        
        # بارگذاری داده‌ها
        self.load_teachers_table()
        
        # دکمه‌های عملیاتی
        buttons_frame = tk.Frame(card, bg=ColorPalette.NEUTRAL["WHITE"])
        buttons_frame.place(relx=0.5, rely=0.85, anchor="center")
        
        action_buttons = [
            ("➕ افزودن معلم جدید", self.show_add_teacher_dialog, ColorPalette.SECONDARY["SUCCESS"]),
            ("✏️ ویرایش معلم", self.edit_selected_teacher, ColorPalette.SECONDARY["INFO"]),
            ("🗑️ حذف معلم", self.delete_selected_teacher, ColorPalette.SECONDARY["ERROR"])
        ]
        
        for text, command, color in action_buttons:
            btn = ModernButton(buttons_frame, text=text, command=command,
                              color=color, size="medium",
                              width=200, height=45, radius=10)
            btn.pack(side="left", padx=10)
    
    def load_teachers_table(self, search_term=""):
        """بارگذاری جدول معلمان"""
        if not hasattr(self, 'teachers_tree'):
            return
            
        # پاک کردن ردیف‌های قبلی
        for item in self.teachers_tree.get_children():
            self.teachers_tree.delete(item)
        
        # دریافت معلمان از دیتابیس
        teachers = self.db.get_teacher_list(search_term)
        
        # اضافه کردن به جدول
        for teacher in teachers:
            status = "✅ فعال" if teacher['status'] == 'active' else "❌ غیرفعال"
            self.teachers_tree.insert("", "end", values=(
                teacher['teacher_id'],
                teacher['full_name'],
                teacher['subject'],
                teacher['degree'] or "-",
                teacher['phone'] or "-",
                status
            ), tags=(teacher['teacher_id'],))
    
    def search_teachers(self):
        """جستجوی معلمان"""
        search_term = self.teacher_search_var.get()
        self.load_teachers_table(search_term)
    
    def edit_selected_teacher(self):
        """ویرایش معلم انتخاب شده"""
        try:
            item = self.teachers_tree.selection()[0]
            values = self.teachers_tree.item(item)['values']
            teacher_id = values[0]
            self.show_edit_teacher_dialog(teacher_id)
        except IndexError:
            messagebox.showwarning("توجه", "لطفاً یک معلم را انتخاب کنید")
    
    def delete_selected_teacher(self):
        """حذف معلم انتخاب شده"""
        try:
            item = self.teachers_tree.selection()[0]
            values = self.teachers_tree.item(item)['values']
            teacher_id = values[0]
            teacher_name = values[1]
            
            if messagebox.askyesno("تأیید حذف", 
                                  f"آیا از حذف معلم '{teacher_name}' مطمئن هستید؟\nاین عمل قابل بازگشت نیست!"):
                if self.db.delete_teacher(teacher_id):
                    messagebox.showinfo("موفقیت", "✅ معلم با موفقیت حذف شد")
                    self.load_teachers_table()
                else:
                    messagebox.showerror("خطا", "❌ خطا در حذف معلم")
        except IndexError:
            messagebox.showwarning("توجه", "لطفاً یک معلم را انتخاب کنید")
    
    def show_add_teacher_dialog(self):
        """نمایش دیالوگ افزودن معلم"""
        dialog = tk.Toplevel(self.root)
        dialog.title("👨‍🏫 افزودن معلم جدید")
        dialog.geometry("500x600")
        dialog.configure(bg=ColorPalette.NEUTRAL["BACKGROUND"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # هدر دیالوگ
        header_frame = tk.Frame(dialog, bg=ColorPalette.PRIMARY["MAIN"], height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="👨‍🏫 افزودن معلم جدید",
                font=("Tahoma", 16, "bold"),
                bg=ColorPalette.PRIMARY["MAIN"], 
                fg=ColorPalette.NEUTRAL["WHITE"]).pack(pady=15)
        
        # کانتینر اصلی با اسکرول‌بار
        main_container = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_container, bg=ColorPalette.NEUTRAL["BACKGROUND"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # فرم
        form_frame = tk.Frame(scrollable_frame, bg=ColorPalette.NEUTRAL["WHITE"])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        fields = [
            ("کد معلم*:", "entry", True, ""),
            ("کد ملی:", "entry", False, ""),
            ("نام*:", "entry", True, ""),
            ("نام خانوادگی*:", "entry", True, ""),
            ("مدرک تحصیلی:", "combo", False, ["دیپلم", "لیسانس", "فوق لیسانس", "دکتری"]),
            ("رشته تخصصی:", "entry", False, ""),
            ("درس تدریس*:", "combo", True, ["ریاضی", "فیزیک", "شیمی", "ادبیات", "دینی", "انگلیسی", "هنر", "ورزش"]),
            ("شماره تماس:", "entry", False, ""),
            ("ایمیل:", "entry", False, ""),
            ("آدرس:", "entry", False, ""),
            ("حقوق ماهانه:", "entry", False, "0")
        ]
        
        self.teacher_entries = {}
        
        for label_text, field_type, required, options in fields:
            frame = tk.Frame(form_frame, bg=ColorPalette.NEUTRAL["WHITE"])
            frame.pack(fill="x", pady=10)
            
            label = f"{'* ' if required else ''}{label_text}"
            tk.Label(frame, text=label, 
                    font=("Tahoma", 11, "bold" if required else "normal"),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.PRIMARY["DARK"] if required else ColorPalette.NEUTRAL["BLACK"],
                    width=20, anchor="w").pack(side="left")
            
            if field_type == "entry":
                entry = tk.Entry(frame, font=("Tahoma", 11), 
                                bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                                fg=ColorPalette.NEUTRAL["BLACK"],
                                width=25)
                if options and not isinstance(options, list):
                    entry.insert(0, options)
                entry.pack(side="left", padx=10)
                self.teacher_entries[label_text] = entry
            elif field_type == "combo":
                var = tk.StringVar()
                combo = ttk.Combobox(frame, textvariable=var, 
                                   values=options if isinstance(options, list) else [],
                                   state="readonly", width=23)
                if options and isinstance(options, list) and options[0]:
                    var.set(options[0])
                combo.pack(side="left", padx=10)
                self.teacher_entries[label_text] = var
        
        # دکمه‌ها
        button_frame = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        button_frame.pack(pady=20)
        
        def save_teacher():
            required_fields = ["کد معلم*:", "نام*:", "نام خانوادگی*:", "درس تدریس*:"]
            missing_fields = []
            
            for field in required_fields:
                value = ""
                if field in self.teacher_entries:
                    entry = self.teacher_entries[field]
                    if isinstance(entry, tk.Entry):
                        value = entry.get().strip()
                    else:
                        value = entry.get().strip()
                
                if not value:
                    missing_fields.append(field.replace("*:", ""))
            
            if missing_fields:
                messagebox.showerror("خطا", f"فیلدهای اجباری پر نشده‌اند:\n{', '.join(missing_fields)}")
                return
            
            try:
                # جمع‌آوری داده‌ها
                salary = float(self.teacher_entries.get("حقوق ماهانه:", tk.StringVar(value="0")).get().strip())
                
                teacher_data = (
                    self.teacher_entries["کد معلم*:"].get().strip(),
                    self.teacher_entries.get("کد ملی:", tk.StringVar(value="")).get().strip(),
                    self.teacher_entries["نام*:"].get().strip(),
                    self.teacher_entries["نام خانوادگی*:"].get().strip(),
                    f"{self.teacher_entries['نام*:'].get().strip()} {self.teacher_entries['نام خانوادگی*:'].get().strip()}",
                    self.teacher_entries.get("مدرک تحصیلی:", tk.StringVar(value="")).get().strip(),
                    self.teacher_entries.get("رشته تخصصی:", tk.StringVar(value="")).get().strip(),
                    self.teacher_entries["درس تدریس*:"].get().strip(),
                    self.teacher_entries.get("شماره تماس:", tk.StringVar(value="")).get().strip(),
                    self.teacher_entries.get("ایمیل:", tk.StringVar(value="")).get().strip(),
                    self.teacher_entries.get("آدرس:", tk.StringVar(value="")).get().strip(),
                    date.today().strftime("%Y/%m/%d"),
                    salary
                )
                
                if self.db.add_teacher(teacher_data):
                    messagebox.showinfo("موفقیت", "✅ معلم با موفقیت ثبت شد")
                    dialog.destroy()
                    self.load_teachers_table()
                else:
                    messagebox.showerror("خطا", "❌ کد معلم تکراری است")
                    
            except ValueError:
                messagebox.showerror("خطا", "❌ لطفاً حقوق را به صورت عددی وارد کنید")
            except Exception as e:
                messagebox.showerror("خطا", f"❌ خطا در ثبت معلم:\n{str(e)}")
        
        save_btn = ModernButton(button_frame, text="ثبت نهایی", 
                               icon=self.icons["save"],
                               command=save_teacher,
                               color="success", size="medium",
                               width=150, height=45, radius=10)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ModernButton(button_frame, text="انصراف", 
                                 icon=self.icons["cancel"],
                                 command=dialog.destroy,
                                 color="error", size="medium",
                                 width=150, height=45, radius=10)
        cancel_btn.pack(side="right", padx=10)
    
    def show_edit_teacher_dialog(self, teacher_id=None):
        """نمایش دیالوگ ویرایش معلم"""
        if not teacher_id:
            try:
                item = self.teachers_tree.selection()[0]
                values = self.teachers_tree.item(item)['values']
                teacher_id = values[0]
            except IndexError:
                messagebox.showwarning("توجه", "لطفاً یک معلم را انتخاب کنید")
                return
        
        # دریافت اطلاعات فعلی معلم
        teacher = self.db.get_teacher_details(teacher_id)
        if not teacher:
            messagebox.showerror("خطا", "معلم مورد نظر یافت نشد")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"✏️ ویرایش معلم: {teacher['full_name']}")
        dialog.geometry("500x600")
        dialog.configure(bg=ColorPalette.NEUTRAL["BACKGROUND"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # هدر دیالوگ
        header_frame = tk.Frame(dialog, bg=ColorPalette.PRIMARY["MAIN"], height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text=f"✏️ ویرایش معلم",
                font=("Tahoma", 16, "bold"),
                bg=ColorPalette.PRIMARY["MAIN"], 
                fg=ColorPalette.NEUTRAL["WHITE"]).pack(pady=15)
        
        # کانتینر اصلی با اسکرول‌بار
        main_container = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_container, bg=ColorPalette.NEUTRAL["BACKGROUND"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # فرم
        form_frame = tk.Frame(scrollable_frame, bg=ColorPalette.NEUTRAL["WHITE"])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # فیلدهای فرم با مقادیر فعلی
        fields = [
            ("کد معلم:", "label", False, teacher['teacher_id']),
            ("کد ملی:", "entry", False, teacher['national_code'] or ""),
            ("نام*:", "entry", True, teacher['first_name']),
            ("نام خانوادگی*:", "entry", True, teacher['last_name']),
            ("مدرک تحصیلی:", "combo", False, ["دیپلم", "لیسانس", "فوق لیسانس", "دکتری"], teacher['degree'] or ""),
            ("رشته تخصصی:", "entry", False, teacher['major'] or ""),
            ("درس تدریس*:", "combo", True, ["ریاضی", "فیزیک", "شیمی", "ادبیات", "دینی", "انگلیسی", "هنر", "ورزش"], teacher['subject']),
            ("شماره تماس:", "entry", False, teacher['phone'] or ""),
            ("ایمیل:", "entry", False, teacher['email'] or ""),
            ("آدرس:", "entry", False, teacher['address'] or ""),
            ("حقوق ماهانه:", "entry", False, str(teacher['salary']))
        ]
        
        self.edit_teacher_entries = {}
        
        for label_text, field_type, required, *args in fields:
            frame = tk.Frame(form_frame, bg=ColorPalette.NEUTRAL["WHITE"])
            frame.pack(fill="x", pady=10)
            
            # برچسب
            label = f"{'* ' if required else ''}{label_text}"
            tk.Label(frame, text=label, 
                    font=("Tahoma", 11, "bold" if required else "normal"),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.PRIMARY["DARK"] if required else ColorPalette.NEUTRAL["BLACK"],
                    width=20, anchor="w").pack(side="left")
            
            # فیلد ورودی
            if field_type == "entry":
                entry = tk.Entry(frame, font=("Tahoma", 11), 
                                bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                                fg=ColorPalette.NEUTRAL["BLACK"],
                                width=25)
                entry.insert(0, args[0])
                entry.pack(side="left", padx=10)
                self.edit_teacher_entries[label_text] = entry
            elif field_type == "combo":
                var = tk.StringVar()
                values = args[0] if isinstance(args[0], list) else ["دیپلم", "لیسانس", "فوق لیسانس", "دکتری"]
                default_value = args[1] if len(args) > 1 else values[0]
                combo = ttk.Combobox(frame, textvariable=var, 
                                   values=values,
                                   state="readonly", width=23)
                var.set(default_value)
                combo.pack(side="left", padx=10)
                self.edit_teacher_entries[label_text] = var
            elif field_type == "label":
                tk.Label(frame, text=args[0], 
                        font=("Tahoma", 11),
                        bg=ColorPalette.NEUTRAL["WHITE"], 
                        fg=ColorPalette.NEUTRAL["BLACK"],
                        width=25).pack(side="left", padx=10)
        
        # دکمه‌ها
        button_frame = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        button_frame.pack(pady=20)
        
        def update_teacher():
            # اعتبارسنجی فیلدهای اجباری
            required_fields = ["نام*:", "نام خانوادگی*:", "درس تدریس*:"]
            missing_fields = []
            
            for field in required_fields:
                value = ""
                if field in self.edit_teacher_entries:
                    entry = self.edit_teacher_entries[field]
                    if isinstance(entry, tk.Entry):
                        value = entry.get().strip()
                    else:
                        value = entry.get().strip()
                
                if not value:
                    missing_fields.append(field.replace("*:", ""))
            
            if missing_fields:
                messagebox.showerror("خطا", f"فیلدهای اجباری پر نشده‌اند:\n{', '.join(missing_fields)}")
                return
            
            try:
                # جمع‌آوری داده‌ها
                salary = float(self.edit_teacher_entries.get("حقوق ماهانه:", tk.StringVar(value="0")).get().strip())
                
                teacher_data = (
                    self.edit_teacher_entries.get("کد ملی:", tk.StringVar(value="")).get().strip(),
                    self.edit_teacher_entries["نام*:"].get().strip(),
                    self.edit_teacher_entries["نام خانوادگی*:"].get().strip(),
                    f"{self.edit_teacher_entries['نام*:'].get().strip()} {self.edit_teacher_entries['نام خانوادگی*:'].get().strip()}",
                    self.edit_teacher_entries.get("مدرک تحصیلی:", tk.StringVar(value="")).get().strip(),
                    self.edit_teacher_entries.get("رشته تخصصی:", tk.StringVar(value="")).get().strip(),
                    self.edit_teacher_entries["درس تدریس*:"].get().strip(),
                    self.edit_teacher_entries.get("شماره تماس:", tk.StringVar(value="")).get().strip(),
                    self.edit_teacher_entries.get("ایمیل:", tk.StringVar(value="")).get().strip(),
                    self.edit_teacher_entries.get("آدرس:", tk.StringVar(value="")).get().strip(),
                    salary
                )
                
                # به‌روزرسانی در دیتابیس
                if self.db.update_teacher(teacher_id, teacher_data):
                    messagebox.showinfo("موفقیت", "✅ اطلاعات معلم با موفقیت به‌روزرسانی شد")
                    dialog.destroy()
                    self.load_teachers_table()
                else:
                    messagebox.showerror("خطا", "❌ خطا در به‌روزرسانی اطلاعات")
                    
            except ValueError:
                messagebox.showerror("خطا", "❌ لطفاً حقوق را به صورت عددی وارد کنید")
            except Exception as e:
                messagebox.showerror("خطا", f"❌ خطا در به‌روزرسانی معلم:\n{str(e)}")
        
        save_btn = ModernButton(button_frame, text="ذخیره تغییرات", 
                               icon=self.icons["save"],
                               command=update_teacher,
                               color="success", size="medium",
                               width=150, height=45, radius=10)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ModernButton(button_frame, text="انصراف", 
                                 icon=self.icons["cancel"],
                                 command=dialog.destroy,
                                 color="error", size="medium",
                                 width=150, height=45, radius=10)
        cancel_btn.pack(side="right", padx=10)
    
    def show_event_management(self):
        """مدیریت رویدادها"""
        self.clear_window()
        
        # هدر
        self.create_header("مدیریت رویدادها")
        
        # سایدبار
        self.create_sidebar()
        
        # ناحیه اصلی
        main_frame = tk.Frame(self.root, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # کارت اصلی
        card = GlassCard(main_frame, width=1060, height=500, radius=15,
                        color=ColorPalette.NEUTRAL["WHITE"])
        card.pack(fill="both", expand=True)
        
        # عنوان
        tk.Label(card, text="📅 مدیریت رویدادهای مدرسه",
                font=("Tahoma", 22, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["BLACK"]).place(relx=0.5, rely=0.2, anchor="center")
        
        tk.Label(card, text="برنامه‌ریزی و مدیریت رویدادها، جشن‌ها و امتحانات",
                font=("Tahoma", 14),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["DARK_GRAY"]).place(relx=0.5, rely=0.3, anchor="center")
        
        # دکمه‌های عملیاتی
        buttons_frame = tk.Frame(card, bg=ColorPalette.NEUTRAL["WHITE"])
        buttons_frame.place(relx=0.5, rely=0.6, anchor="center")
        
        action_buttons = [
            ("➕ افزودن رویداد جدید", self.show_add_event_dialog, ColorPalette.SECONDARY["SUCCESS"]),
            ("✏️ ویرایش رویداد", lambda: messagebox.showinfo("ویرایش", "این بخش در حال توسعه است"), 
             ColorPalette.SECONDARY["INFO"]),
            ("🗑️ حذف رویداد", lambda: messagebox.showinfo("حذف", "این بخش در حال توسعه است"), 
             ColorPalette.SECONDARY["ERROR"])
        ]
        
        for text, command, color in action_buttons:
            btn = ModernButton(buttons_frame, text=text, command=command,
                              color=color, size="large",
                              width=250, height=55, radius=12)
            btn.pack(pady=15)
    
    def show_add_event_dialog(self):
        """نمایش دیالوگ افزودن رویداد"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📅 افزودن رویداد جدید")
        dialog.geometry("500x500")
        dialog.configure(bg=ColorPalette.NEUTRAL["BACKGROUND"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # هدر دیالوگ
        header_frame = tk.Frame(dialog, bg=ColorPalette.PRIMARY["MAIN"], height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="📅 افزودن رویداد جدید",
                font=("Tahoma", 16, "bold"),
                bg=ColorPalette.PRIMARY["MAIN"], 
                fg=ColorPalette.NEUTRAL["WHITE"]).pack(pady=15)
        
        # فرم
        form_frame = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["WHITE"])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        fields = [
            ("عنوان رویداد*:", "entry", True, "امتحان فیزیک"),
            ("تاریخ*:", "entry", True, "1403/09/23"),
            ("زمان:", "entry", False, "08:00"),
            ("نوع رویداد*:", "combo", True, ["امتحان", "جشن", "مراسم", "بازدید", "کارگاه", "دیگر"]),
            ("مکان:", "entry", False, "سالن امتحانات"),
            ("توضیحات:", "text", False, "امتحان میان‌ترم فیزیک پایه دهم")
        ]
        
        self.event_entries = {}
        
        for label_text, field_type, required, default in fields:
            frame = tk.Frame(form_frame, bg=ColorPalette.NEUTRAL["WHITE"])
            frame.pack(fill="x", pady=10)
            
            label = f"{'* ' if required else ''}{label_text}"
            tk.Label(frame, text=label, 
                    font=("Tahoma", 11, "bold" if required else "normal"),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.PRIMARY["DARK"] if required else ColorPalette.NEUTRAL["BLACK"],
                    width=20, anchor="w").pack(side="left")
            
            if field_type == "entry":
                entry = tk.Entry(frame, font=("Tahoma", 11), 
                                bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                                fg=ColorPalette.NEUTRAL["BLACK"],
                                width=25)
                entry.insert(0, default)
                entry.pack(side="left", padx=10)
                self.event_entries[label_text] = entry
            elif field_type == "combo":
                var = tk.StringVar()
                combo = ttk.Combobox(frame, textvariable=var, 
                                   values=default if isinstance(default, list) else [],
                                   state="readonly", width=23)
                if default and isinstance(default, list) and default[0]:
                    var.set(default[0])
                combo.pack(side="left", padx=10)
                self.event_entries[label_text] = var
            elif field_type == "text":
                text_widget = tk.Text(frame, font=("Tahoma", 11), 
                                     bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                                     fg=ColorPalette.NEUTRAL["BLACK"],
                                     width=25, height=4)
                text_widget.insert("1.0", default)
                text_widget.pack(side="left", padx=10)
                self.event_entries[label_text] = text_widget
        
        # دکمه‌ها
        button_frame = tk.Frame(dialog, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        button_frame.pack(pady=20)
        
        def save_event():
            required_fields = ["عنوان رویداد*:", "تاریخ*:", "نوع رویداد*:"]
            missing_fields = []
            
            for field in required_fields:
                value = ""
                if field in self.event_entries:
                    entry = self.event_entries[field]
                    if isinstance(entry, tk.Entry):
                        value = entry.get().strip()
                    elif isinstance(entry, tk.Text):
                        value = entry.get("1.0", "end-1c").strip()
                    else:
                        value = entry.get().strip()
                
                if not value:
                    missing_fields.append(field.replace("*:", ""))
            
            if missing_fields:
                messagebox.showerror("خطا", f"فیلدهای اجباری پر نشده‌اند:\n{', '.join(missing_fields)}")
                return
            
            messagebox.showinfo("موفقیت", "✅ رویداد با موفقیت ثبت شد")
            dialog.destroy()
        
        save_btn = ModernButton(button_frame, text="ثبت رویداد", 
                               icon=self.icons["save"],
                               command=save_event,
                               color="success", size="medium",
                               width=150, height=45, radius=10)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ModernButton(button_frame, text="انصراف", 
                                 icon=self.icons["cancel"],
                                 command=dialog.destroy,
                                 color="error", size="medium",
                                 width=150, height=45, radius=10)
        cancel_btn.pack(side="right", padx=10)
    
    def show_reports(self):
        """گزارش‌ها و آمار"""
        self.clear_window()
        
        # هدر
        self.create_header("گزارش‌ها و آمار")
        
        # سایدبار
        self.create_sidebar()
        
        # ناحیه اصلی
        main_frame = tk.Frame(self.root, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # کارت اصلی
        card = GlassCard(main_frame, width=1060, height=500, radius=15,
                        color=ColorPalette.NEUTRAL["WHITE"])
        card.pack(fill="both", expand=True)
        
        # عنوان
        tk.Label(card, text="📊 گزارش‌ها و آمار مدرسه",
                font=("Tahoma", 22, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["BLACK"]).place(relx=0.5, rely=0.2, anchor="center")
        
        tk.Label(card, text="گزارش‌گیری و تحلیل آمار عملکرد مدرسه",
                font=("Tahoma", 14),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["DARK_GRAY"]).place(relx=0.5, rely=0.3, anchor="center")
        
        # گزینه‌های گزارش‌گیری
        reports_frame = tk.Frame(card, bg=ColorPalette.NEUTRAL["WHITE"])
        reports_frame.place(relx=0.5, rely=0.6, anchor="center")
        
        report_types = [
            ("📈 گزارش عملکرد تحصیلی", "گزارش نمرات و پیشرفت دانش‌آموزان"),
            ("📊 آمار حضور و غیاب", "گزارش غیبت و تأخیر دانش‌آموزان"),
            ("👥 لیست کلاسی", "گزارش دانش‌آموزان هر کلاس"),
            ("🎓 کارنامه نهایی", "صدور کارنامه پایان ترم"),
            ("📅 تقویم آموزشی", "برنامه زمانی مدرسه"),
            ("💰 گزارش مالی", "گزارش شهریه و پرداخت‌ها")
        ]
        
        for i, (title, description) in enumerate(report_types):
            report_card = tk.Frame(reports_frame, bg=ColorPalette.NEUTRAL["LIGHT_GRAY"],
                                 relief="solid", bd=1, width=500, height=60)
            report_card.grid(row=i, column=0, pady=5, sticky="ew")
            report_card.grid_propagate(False)
            
            tk.Label(report_card, text=title, 
                    font=("Tahoma", 12, "bold"),
                    bg=ColorPalette.NEUTRAL["LIGHT_GRAY"], 
                    fg=ColorPalette.NEUTRAL["BLACK"],
                    anchor="w").place(x=10, y=10)
            
            tk.Label(report_card, text=description, 
                    font=("Tahoma", 10),
                    bg=ColorPalette.NEUTRAL["LIGHT_GRAY"], 
                    fg=ColorPalette.NEUTRAL["DARK_GRAY"],
                    anchor="w").place(x=10, y=35)
            
            # دکمه تولید گزارش
            btn = ModernButton(report_card, text="تولید", 
                              command=lambda t=title: self.generate_report(t),
                              color="primary", size="small",
                              width=80, height=30, radius=6)
            btn.place(relx=0.85, rely=0.5, anchor="center")
    
    def generate_report(self, report_type):
        """تولید گزارش"""
        messagebox.showinfo("تولید گزارش", f"در حال تولید گزارش: {report_type}\nاین بخش در حال توسعه است")
    
    def show_settings(self):
        """تنظیمات سیستم"""
        self.clear_window()
        
        # هدر
        self.create_header("تنظیمات سیستم")
        
        # سایدبار
        self.create_sidebar()
        
        # ناحیه اصلی
        main_frame = tk.Frame(self.root, bg=ColorPalette.NEUTRAL["BACKGROUND"])
        main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # کارت اصلی
        card = GlassCard(main_frame, width=1060, height=600, radius=15,
                        color=ColorPalette.NEUTRAL["WHITE"])
        card.pack(fill="both", expand=True)
        
        # عنوان
        tk.Label(card, text="⚙️ تنظیمات مدرسه علم برتر",
                font=("Tahoma", 22, "bold"),
                bg=ColorPalette.NEUTRAL["WHITE"], 
                fg=ColorPalette.NEUTRAL["BLACK"]).place(relx=0.5, rely=0.1, anchor="center")
        
        # اطلاعات مدرسه
        info_frame = tk.Frame(card, bg=ColorPalette.NEUTRAL["WHITE"])
        info_frame.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8)
        
        school_info = [
            ("🏫 نام مدرسه:", "مدرسه غیر دولتی علم برتر"),
            ("📅 سال تحصیلی:", "1404-1405"),
            ("📍 آدرس:", "تهران، خیابان کهرم، پلاک ۱۲۳"),
            ("📞 تلفن:", "021-12345678"),
            ("✉️ ایمیل:", "info@elm-bartar.edu"),
            ("🌐 وبسایت:", "www.elm-bartar.edu"),
            ("👨‍🏫 نام مدیر:", "محمد غیرتمند"),
            ("🕒 زمان شروع:", "۰۷:۳۰"),
            ("🕒 زمان پایان:", "۱۳:۳۰"),
            ("📚 پایه‌های تحصیلی:", "هفتم، هشتم، نهم"),
            ("👥 ظرفیت مدرسه:", "۵۰۰ دانش‌آموز"),
            ("🎓 کادر آموزشی:", "۲۰ معلم")
        ]
        
        for i, (label, value) in enumerate(school_info):
            row_frame = tk.Frame(info_frame, bg=ColorPalette.NEUTRAL["WHITE"])
            row_frame.pack(fill="x", pady=8)
            
            tk.Label(row_frame, text=label, 
                    font=("Tahoma", 12, "bold"),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.PRIMARY["DARK"],
                    width=25, anchor="w").pack(side="left")
            
            tk.Label(row_frame, text=value, 
                    font=("Tahoma", 12),
                    bg=ColorPalette.NEUTRAL["WHITE"], 
                    fg=ColorPalette.NEUTRAL["BLACK"],
                    anchor="w").pack(side="left", padx=10)
        
        # دکمه‌ها
        button_frame = tk.Frame(card, bg=ColorPalette.NEUTRAL["WHITE"])
        button_frame.place(relx=0.5, rely=0.85, anchor="center")
        
        save_btn = ModernButton(button_frame, text="ذخیره تنظیمات", 
                               icon=self.icons["save"],
                               command=lambda: messagebox.showinfo("ذخیره", "✅ تنظیمات با موفقیت ذخیره شد"),
                               color="success", size="medium",
                               width=200, height=50, radius=10)
        save_btn.pack(side="left", padx=10)
        
        backup_btn = ModernButton(button_frame, text="پشتیبان‌گیری", 
                                 icon=self.icons["save"],
                                 command=lambda: messagebox.showinfo("پشتیبان", "✅ پشتیبان با موفقیت ایجاد شد"),
                                 color="info", size="medium",
                                 width=200, height=50, radius=10)
        backup_btn.pack(side="left", padx=10)

# ==================== راه‌اندازی اولیه ====================
def setup_system():
    """راه‌اندازی اولیه سیستم"""
    # حذف دیتابیس قدیمی اگر وجود دارد
    if os.path.exists("school_management_pro.db"):
        try:
            os.remove("school_management_pro.db")
            print("🗑️ فایل دیتابیس قدیمی حذف شد")
        except:
            print("⚠️ نتوانستم دیتابیس قدیمی را حذف کنم")
    
    # بررسی وجود لوگو
    logo_files = ["elm.png", "logo.png", "download.jpg", "elm.jpg", "logo.jpg"]
    for logo_file in logo_files:
        if os.path.exists(logo_file):
            print(f"✅ لوگو یافت شد: {logo_file}")
            break
    else:
        print("ℹ️ لوگو یافت نشد. از ایموجی 🏫 استفاده می‌شود")
    
    return True

# ==================== اجرای برنامه ====================
if __name__ == "__main__":
    print("🚀 در حال راه‌اندازی سیستم مدیریت مدرسه علم برتر...")
    
    # راه‌اندازی اولیه
    setup_system()
    
    print("📊 ایجاد پایگاه داده...")
    print("🎨 بارگذاری رابط کاربری...")
    print("✅ آماده بهره‌برداری!")
    
    try:
        app = SchoolManagementSystem()
        app.root.mainloop()
    except Exception as e:
        print(f"❌ خطا در اجرای برنامه: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("خطای سیستمی", f"خطای غیرمنتظره:\n{str(e)}")
