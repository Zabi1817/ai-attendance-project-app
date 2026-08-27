import os
import streamlit as st
from supabase import create_client, Client

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "local_db.sqlite")
with open("C:\\Users\\mdzab\\.gemini\\antigravity-ide\\brain\\cab1355e-325a-4e03-9663-3941c906ebf3\\db_path.txt", "w") as f:
    f.write(DB_PATH)

def init_local_db(db_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        name TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        face_embedding TEXT,
        voice_embedding TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_code TEXT UNIQUE,
        name TEXT,
        section TEXT,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subject_students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        timestamp TEXT,
        is_present INTEGER,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )
    """)
    
    conn.commit()
    conn.close()

class LocalQueryBuilder:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name
        self.filters = []
        self.select_columns = "*"
        self.is_delete = False
        self.insert_data = None

    def select(self, columns):
        self.select_columns = columns
        return self

    def eq(self, column, value):
        self.filters.append((column, value))
        return self

    def limit(self, val):
        return self

    def delete(self):
        self.is_delete = True
        return self

    def insert(self, data):
        self.insert_data = data
        return self

    def execute(self):
        import sqlite3
        import json
        
        if self.insert_data is not None:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            inserted_rows = []
            rows_to_insert = self.insert_data if isinstance(self.insert_data, list) else [self.insert_data]
            
            for row in rows_to_insert:
                processed_row = {}
                for k, v in row.items():
                    if isinstance(v, list):
                        processed_row[k] = json.dumps(v)
                    elif isinstance(v, bool):
                        processed_row[k] = 1 if v else 0
                    else:
                        processed_row[k] = v
                
                columns = ", ".join(processed_row.keys())
                placeholders = ", ".join(["?"] * len(processed_row))
                values = list(processed_row.values())
                
                cursor.execute(f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})", values)
                last_id = cursor.lastrowid
                
                pk_col = "teacher_id" if self.table_name == "teachers" else \
                         "student_id" if self.table_name == "students" else \
                         "subject_id" if self.table_name == "subjects" else "id"
                
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE {pk_col} = ?", (last_id,))
                r = cursor.fetchone()
                if r:
                    inserted_rows.append(self._row_to_dict(r))
            
            conn.commit()
            conn.close()
            
            class Response:
                def __init__(self, data):
                    self.data = data
            return Response(inserted_rows)
            
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if self.is_delete:
            sql = f"DELETE FROM {self.table_name}"
            params = []
            if self.filters:
                where_clauses = [f"{col} = ?" for col, val in self.filters]
                sql += " WHERE " + " AND ".join(where_clauses)
                params = [val for col, val in self.filters]
            cursor.execute(sql, params)
            conn.commit()
            conn.close()
            
            class Response:
                def __init__(self):
                    self.data = []
            return Response()
            
        is_relation_subjects = "subjects(" in self.select_columns
        is_relation_students = "students(" in self.select_columns
        is_relation_count_studs = "subject_students(count)" in self.select_columns
        is_relation_logs_ts = "attendance_logs(timestamp)" in self.select_columns
        
        if self.table_name == "attendance_logs" and "subjects!inner(*)" in self.select_columns:
            sql = ("SELECT attendance_logs.*, subjects.name AS sub_name, "
                   "subjects.subject_code AS sub_code, subjects.section AS sub_section, "
                   "subjects.teacher_id AS sub_teacher_id FROM attendance_logs "
                   "JOIN subjects ON attendance_logs.subject_id = subjects.subject_id")
            params = []
            where_clauses = []
            for col, val in self.filters:
                if col == "subjects.teacher_id":
                    where_clauses.append("subjects.teacher_id = ?")
                    params.append(val)
                else:
                    where_clauses.append(f"attendance_logs.{col} = ?")
                    params.append(val)
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            data = []
            for r in rows:
                d = dict(r)
                d["subjects"] = {
                    "subject_id": r["subject_id"],
                    "name": r["sub_name"],
                    "subject_code": r["sub_code"],
                    "section": r["sub_section"],
                    "teacher_id": r["sub_teacher_id"]
                }
                d["is_present"] = bool(d.get("is_present"))
                data.append(d)
            conn.close()
            class Response:
                def __init__(self, data):
                    self.data = data
            return Response(data)
            
        sql = f"SELECT * FROM {self.table_name}"
        params = []
        if self.filters:
            where_clauses = [f"{col} = ?" for col, val in self.filters]
            sql += " WHERE " + " AND ".join(where_clauses)
            params = [val for col, val in self.filters]
            
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        data = []
        for r in rows:
            d = self._row_to_dict(r)
            
            if self.table_name == "subjects":
                if is_relation_count_studs:
                    cursor2 = conn.cursor()
                    cursor2.execute("SELECT COUNT(*) FROM subject_students WHERE subject_id = ?", (d["subject_id"],))
                    d["subject_students"] = [{"count": cursor2.fetchone()[0]}]
                if is_relation_logs_ts:
                    cursor2 = conn.cursor()
                    cursor2.execute("SELECT timestamp FROM attendance_logs WHERE subject_id = ?", (d["subject_id"],))
                    d["attendance_logs"] = [{"timestamp": row[0]} for row in cursor2.fetchall()]
            elif self.table_name == "subject_students":
                if is_relation_subjects:
                    cursor2 = conn.cursor()
                    cursor2.execute("SELECT * FROM subjects WHERE subject_id = ?", (d["subject_id"],))
                    sub_row = cursor2.fetchone()
                    d["subjects"] = dict(sub_row) if sub_row else None
                if is_relation_students:
                    cursor2 = conn.cursor()
                    cursor2.execute("SELECT * FROM students WHERE student_id = ?", (d["student_id"],))
                    stud_row = cursor2.fetchone()
                    if stud_row:
                        stud_d = dict(stud_row)
                        if stud_d.get("face_embedding"):
                            stud_d["face_embedding"] = json.loads(stud_d["face_embedding"])
                        if stud_d.get("voice_embedding"):
                            stud_d["voice_embedding"] = json.loads(stud_d["voice_embedding"])
                        d["students"] = stud_d
                    else:
                        d["students"] = None
            elif self.table_name == "attendance_logs":
                if is_relation_subjects:
                    cursor2 = conn.cursor()
                    cursor2.execute("SELECT * FROM subjects WHERE subject_id = ?", (d["subject_id"],))
                    sub_row = cursor2.fetchone()
                    d["subjects"] = dict(sub_row) if sub_row else None
            
            data.append(d)
            
        conn.close()
        class Response:
            def __init__(self, data):
                self.data = data
        return Response(data)

    def _row_to_dict(self, row):
        import json
        d = dict(row)
        for k in ["face_embedding", "voice_embedding"]:
            if k in d and d[k]:
                try:
                    d[k] = json.loads(d[k])
                except Exception:
                    pass
        for k in ["is_present"]:
            if k in d and d[k] is not None:
                d[k] = bool(d[k])
        return d

class LocalSupabaseClient:
    def __init__(self, db_path):
        self.db_path = db_path
        init_local_db(db_path)

    def table(self, table_name):
        return LocalQueryBuilder(self.db_path, table_name)


class DynamicSupabaseClient:
    def __init__(self, real_client, local_client):
        self.real_client = real_client
        self.local_client = local_client
        self.use_local = (real_client is None)

    def table(self, table_name):
        if self.use_local:
            return self.local_client.table(table_name)
        
        class DynamicQueryBuilder:
            def __init__(self, parent, real_builder, local_builder):
                self.parent = parent
                self.real_builder = real_builder
                self.local_builder = local_builder
                self.calls = []

            def __getattr__(self, name):
                def method(*args, **kwargs):
                    self.calls.append((name, args, kwargs))
                    if not self.parent.use_local:
                        try:
                            self.real_builder = getattr(self.real_builder, name)(*args, **kwargs)
                        except Exception:
                            pass
                    self.local_builder = getattr(self.local_builder, name)(*args, **kwargs)
                    return self
                return method

            def execute(self):
                if self.parent.use_local:
                    return self.local_builder.execute()
                
                try:
                    return self.real_builder.execute()
                except Exception as e:
                    import sys
                    print(f"[SnapClass Fallback] Supabase runtime error: {e}. Falling back to local database.", file=sys.stderr)
                    self.parent.use_local = True
                    rebuilt_builder = self.parent.local_client.table(self.local_builder.table_name)
                    for method_name, args, kwargs in self.calls:
                        rebuilt_builder = getattr(rebuilt_builder, method_name)(*args, **kwargs)
                    return rebuilt_builder.execute()
                    
        return DynamicQueryBuilder(self, self.real_client.table(table_name), self.local_client.table(table_name))


# Attempt to initialize real Supabase client
local_db_client = LocalSupabaseClient(DB_PATH)
real_db_client = None
USING_LOCAL_DB = False

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    real_db_client = create_client(url, key)
    # Test connection
    real_db_client.table("teachers").select("username").limit(1).execute()
except Exception as e:
    import sys
    print(f"[SnapClass Fallback] Failed to connect to Supabase: {e}. Falling back to local SQLite database.", file=sys.stderr)
    USING_LOCAL_DB = True

supabase = DynamicSupabaseClient(real_db_client if not USING_LOCAL_DB else None, local_db_client)