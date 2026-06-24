from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, g
<<<<<<< HEAD
import psycopg2
import psycopg2.extras
import psycopg2.errors
=======
import sqlite3
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
import os
from datetime import datetime, timedelta
import yagmail
import base64
import json
import re
import math
import functools
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = os.environ.get('SECRET_KEY', 'lf_secret_tech_titans_2025')

<<<<<<< HEAD
class ChainedCursor(psycopg2.extras.DictCursor):
    def execute(self, query, vars=None):
        super().execute(query, vars)
        return self

=======
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
# ─── SQLite per-request setup (replacing global conn/cursor) ───
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
<<<<<<< HEAD
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            raise Exception("DATABASE_URL environment variable is not set")
        db = g._database = psycopg2.connect(db_url, cursor_factory=ChainedCursor)
=======
        db = g._database = sqlite3.connect("lost_found.db", check_same_thread=False)
        db.row_factory = sqlite3.Row
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
<<<<<<< HEAD
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        return
    db = psycopg2.connect(db_url, cursor_factory=ChainedCursor)
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
=======
    db = sqlite3.connect("lost_found.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
            type TEXT,
            name TEXT,
            description TEXT,
            location TEXT,
            contact TEXT,
            image TEXT,
            date TEXT
        )
    """)
    db.commit()

    _new_item_cols = [
        ("category",       "TEXT DEFAULT 'Other'"),
        ("is_emergency",   "INTEGER DEFAULT 0"),
        ("status",         "TEXT DEFAULT 'Active'"),
        ("view_count",     "INTEGER DEFAULT 0"),
        ("event_id",       "INTEGER DEFAULT NULL"),
        ("item_condition", "TEXT DEFAULT 'Unknown'"),
        ("tags",           "TEXT DEFAULT ''"),
        ("item_name",      "TEXT DEFAULT ''"),
    ]
    for _col, _def in _new_item_cols:
        try:
            cursor.execute(f"ALTER TABLE items ADD COLUMN {_col} {_def}")
            db.commit()
<<<<<<< HEAD
        except Exception as e:
            db.rollback()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_timeline (
        id SERIAL PRIMARY KEY,
=======
        except Exception:
            pass

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS item_timeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        item_id INTEGER,
        event TEXT,
        details TEXT,
        timestamp TEXT
    );
    CREATE TABLE IF NOT EXISTS claims (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        item_id INTEGER,
        claimant_name TEXT,
        claimant_contact TEXT,
        claim_description TEXT,
        status TEXT DEFAULT 'Pending',
        submitted_at TEXT
    );
    CREATE TABLE IF NOT EXISTS storage (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        item_id INTEGER,
        rack_number TEXT,
        shelf_number TEXT,
        assigned_date TEXT,
        expiry_date TEXT,
        collected INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS audit_log (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        action TEXT,
        details TEXT,
        contact TEXT,
        timestamp TEXT
    );
    CREATE TABLE IF NOT EXISTS announcements (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        title TEXT,
        message TEXT,
        type TEXT DEFAULT 'info',
        created_at TEXT,
        expires_at TEXT,
        active INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS events (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        name TEXT,
        event_type TEXT,
        location TEXT,
        start_date TEXT,
        end_date TEXT,
        description TEXT,
        active INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS volunteers (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        name TEXT,
        contact TEXT,
        role TEXT DEFAULT 'Helper',
        registered_at TEXT,
        contribution_count INTEGER DEFAULT 0,
        active INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS success_stories (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        item_id INTEGER,
        title TEXT,
        story TEXT,
        recovery_days INTEGER,
        submitted_by TEXT,
        submitted_at TEXT,
        approved INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS feedback (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        item_id INTEGER,
        name TEXT,
        rating INTEGER,
        comment TEXT,
        submitted_at TEXT
    );
    CREATE TABLE IF NOT EXISTS badges (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        contact TEXT,
        badge_name TEXT,
        badge_icon TEXT,
        earned_at TEXT
    );
    CREATE TABLE IF NOT EXISTS appointments (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        item_id INTEGER,
        name TEXT,
        contact TEXT,
        appointment_date TEXT,
        time_slot TEXT,
        status TEXT DEFAULT 'Scheduled',
        created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS item_tags (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        item_id INTEGER,
        tag TEXT
    );
    CREATE TABLE IF NOT EXISTS staff_emails (
<<<<<<< HEAD
        id SERIAL PRIMARY KEY,
=======
        id INTEGER PRIMARY KEY AUTOINCREMENT,
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        email TEXT UNIQUE NOT NULL
    );
    """)
    db.commit()

    # Seed default staff emails if table is empty
    cursor.execute("SELECT COUNT(*) FROM staff_emails")
    if cursor.fetchone()[0] == 0:
        recipients_str = os.environ.get("RECIPIENTS", "kksselva0312@gmail.com")
        recipients_list = [email.strip() for email in recipients_str.split(",") if email.strip()]
        for r_email in recipients_list:
            try:
<<<<<<< HEAD
                cursor.execute("INSERT INTO staff_emails (email) VALUES (%s) ON CONFLICT (email) DO NOTHING", (r_email,))
            except Exception as e:
                db.rollback()
=======
                cursor.execute("INSERT OR IGNORE INTO staff_emails (email) VALUES (?)", (r_email,))
            except Exception:
                pass
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        db.commit()

    db.close()

# Run migrations once on start
init_db()

# ─── Gmail Setup (loaded from environment variables) ─────────────────────────
sender_email = os.environ.get("SENDER_EMAIL", "lostandfound.act@gmail.com")
app_password = os.environ.get("EMAIL_APP_PASSWORD", "")
admin_password_raw = os.environ.get("ADMIN_PASSWORD", "admin123")

def get_recipients():
    try:
        db = get_db()
        cursor = db.cursor()
        rows = cursor.execute("SELECT email FROM staff_emails").fetchall()
        emails = [row['email'] for row in rows if row['email'].strip()]
        if emails:
            return emails
    except Exception as e:
        print(f"Error fetching staff emails: {e}")
    # fallback to env
    recipients_str = os.environ.get("RECIPIENTS", "kksselva0312@gmail.com")
    return [email.strip() for email in recipients_str.split(",") if email.strip()]


# ─── Helpers ─────────────────────────────────────────────────────────────────

def log_audit(action, details, contact="System"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
<<<<<<< HEAD
        "INSERT INTO audit_log (action, details, contact, timestamp) VALUES (%s,%s,%s,%s)",
=======
        "INSERT INTO audit_log (action, details, contact, timestamp) VALUES (?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (action, details, contact, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    db.commit()


def add_timeline_event(item_id, event, details=""):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
<<<<<<< HEAD
        "INSERT INTO item_timeline (item_id, event, details, timestamp) VALUES (%s,%s,%s,%s)",
=======
        "INSERT INTO item_timeline (item_id, event, details, timestamp) VALUES (?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (item_id, event, details, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    db.commit()


def check_and_award_badges(contact):
    """Award badges based on contribution thresholds."""
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    cursor.execute("SELECT COUNT(*) FROM items WHERE contact=%s", (contact,))
=======
    cursor.execute("SELECT COUNT(*) FROM items WHERE contact=?", (contact,))
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    count = cursor.fetchone()[0]

    badge_rules = [
        (1,  "First Reporter",    "fa-star"),
        (5,  "Active Finder",     "fa-search"),
        (10, "Community Hero",    "fa-shield-alt"),
        (20, "Top Contributor",   "fa-trophy"),
        (50, "Legend",            "fa-crown"),
    ]
    for threshold, badge_name, badge_icon in badge_rules:
        if count >= threshold:
            existing = cursor.execute(
<<<<<<< HEAD
                "SELECT id FROM badges WHERE contact=%s AND badge_name=%s",
=======
                "SELECT id FROM badges WHERE contact=? AND badge_name=?",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
                (contact, badge_name)
            ).fetchone()
            if not existing:
                cursor.execute(
<<<<<<< HEAD
                    "INSERT INTO badges (contact, badge_name, badge_icon, earned_at) VALUES (%s,%s,%s,%s)",
=======
                    "INSERT INTO badges (contact, badge_name, badge_icon, earned_at) VALUES (?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
                    (contact, badge_name, badge_icon, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
    db.commit()


def get_stats():
    db = get_db()
    cursor = db.cursor()
    stats = {}
    stats['total']    = cursor.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    stats['lost']     = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Lost'").fetchone()[0]
    stats['found']    = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Found'").fetchone()[0]
    stats['recovered']= cursor.execute("SELECT COUNT(*) FROM items WHERE status='Recovered'").fetchone()[0]
    stats['claims']   = cursor.execute("SELECT COUNT(*) FROM claims WHERE status='Pending'").fetchone()[0]
    stats['emergency']= cursor.execute("SELECT COUNT(*) FROM items WHERE is_emergency=1 AND status='Active'").fetchone()[0]
    stats['storage']  = cursor.execute("SELECT COUNT(*) FROM storage WHERE collected=0").fetchone()[0]
    stats['volunteers']= cursor.execute("SELECT COUNT(*) FROM volunteers WHERE active=1").fetchone()[0]
    return stats


def get_active_announcements():
    db = get_db()
    cursor = db.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return cursor.execute(
<<<<<<< HEAD
        "SELECT * FROM announcements WHERE active=1 AND (expires_at IS NULL OR expires_at > %s) ORDER BY created_at DESC LIMIT 3",
=======
        "SELECT * FROM announcements WHERE active=1 AND (expires_at IS NULL OR expires_at > ?) ORDER BY created_at DESC LIMIT 3",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (now,)
    ).fetchall()


def get_matches(item_name, category, location, description, target_type='Found'):
    db = get_db()
    cursor = db.cursor()
    candidates = cursor.execute(
<<<<<<< HEAD
        "SELECT * FROM items WHERE type=%s AND status='Active'", (target_type,)
=======
        "SELECT * FROM items WHERE type=? AND status='Active'", (target_type,)
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    ).fetchall()
    matches = []
    
    def clean_words(text):
        if not text:
            return set()
        return set(re.findall(r'\w+', text.lower()))
        
    input_words = clean_words(item_name) | clean_words(description)
    
    for cand in candidates:
        score = 0
        if cand['category'] and category and cand['category'].lower() == category.lower():
            score += 5
        if cand['location'] and location and cand['location'].lower() == location.lower():
            score += 3
        elif cand['location'] and location and (location.lower() in cand['location'].lower() or cand['location'].lower() in location.lower()):
            score += 1
            
        cand_words = clean_words(cand['item_name']) | clean_words(cand['description'])
        overlap = input_words.intersection(cand_words)
        score += len(overlap) * 2
        
        if score >= 4:
            matches.append((cand, score))
            
    matches.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matches[:5]]


def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("Admin login required.", "warning")
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ─── Email (preserved from original) ─────────────────────────────────────────

def send_notification_email(name, description, location, contact, item_type, image_filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    body = f"""<html><body style="font-family: Times New Roman, sans-serif; line-height:1; font-size:18px; color:#000000;">
<div style="font-weight:bold;font-size:16px;">Hello,</div>
<div style="margin:0; padding-bottom:2px; font-size:16px;">
A new item has been reported in the Lost &amp; Found portal.
</div>
<table style="border-collapse: collapse; border-spacing:0; margin:4px 0; font-size:16px; width:100%;">
<tr>
  <td style="padding:2px 6px; font-weight:bold; text-align:left;">Product Category (Lost/Found)</td>
  <td style="padding:2px 6px; text-align:center; width:10px;">:</td>
  <td style="padding:2px 6px; text-align:left;">{item_type}</td>
</tr>
<tr>
  <td style="padding:2px 6px; font-weight:bold; text-align:left;">Name of the Person</td>
  <td style="padding:2px 6px; text-align:center; width:10px;">:</td>
  <td style="padding:2px 6px; text-align:left;">{name}</td>
</tr>
<tr>
  <td style="padding:2px 6px; font-weight:bold; text-align:left;">Description</td>
  <td style="padding:2px 6px; text-align:center; width:10px;">:</td>
  <td style="padding:2px 6px; text-align:left;">{description}</td>
</tr>
<tr>
  <td style="padding:2px 6px; font-weight:bold; text-align:left;">Location</td>
  <td style="padding:2px 6px; text-align:center; width:10px;">:</td>
  <td style="padding:2px 6px; text-align:left;">{location}</td>
</tr>
<tr>
  <td style="padding:2px 6px; font-weight:bold; text-align:left;">Person to be Contacted</td>
  <td style="padding:2px 6px; text-align:center; width:10px;">:</td>
  <td style="padding:2px 6px; text-align:left;">{contact}</td>
</tr>
</table>
"""
    if os.path.exists(image_path):
        body += f"""
<div style="margin-top:10px; text-align:center; font-size:16px; color:#555;">
Thanks,<br>Lost &amp; Found System</div>
<div style="margin:10px 0; font-weight:bold; font-size:16px; text-align:left;">Item Image:</div>
<img src="cid:{image_filename}" style="max-width:400px; height:auto; border:1px solid #ccc; border-radius:6px;" />
</body></html>
"""
    else:
        body += """
<div style="margin-top:10px; text-align:center; font-size:16px; color:#555;">
Thanks,<br>Lost &amp; Found System</div>
</body></html>
"""
    contents = [yagmail.inline(image_path)] if os.path.exists(image_path) else []
    contents.insert(0, body)
    try:
        yag = yagmail.SMTP(sender_email, app_password)
        yag.send(to=get_recipients(), subject=f"Lost & Found Notification - {item_type}", contents=contents)
    except Exception as e:
        print(f"Email error: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
#  ORIGINAL ROUTES (preserved exactly, with minor audit enhancements)
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    stats = get_stats()
    announcements = get_active_announcements()
    # Recent items for news feed
    recent_items = cursor.execute(
        "SELECT * FROM items ORDER BY date DESC LIMIT 8"
    ).fetchall()
    # Emergency items
    emergency_items = cursor.execute(
        "SELECT * FROM items WHERE is_emergency=1 AND status='Active' ORDER BY date DESC LIMIT 5"
    ).fetchall()
    # Success stories
    stories = cursor.execute(
        "SELECT s.*, i.description, i.category FROM success_stories s "
        "LEFT JOIN items i ON s.item_id=i.id WHERE s.approved=1 ORDER BY s.submitted_at DESC LIMIT 3"
    ).fetchall()
    # Recent activity feed
    feed = cursor.execute(
        "SELECT action, details, timestamp FROM audit_log ORDER BY timestamp DESC LIMIT 10"
    ).fetchall()
    
    # Retrieve auto-match suggestions if any from submission
    last_submit_matches = session.pop('last_submit_matches', None)
    
    return render_template('index.html',
        stats=stats, announcements=announcements,
        recent_items=recent_items, emergency_items=emergency_items,
        stories=stories, feed=feed, last_submit_matches=last_submit_matches)


@app.route('/lost', methods=['GET', 'POST'])
def lost():
    db = get_db()
    cursor = db.cursor()
    events = cursor.execute("SELECT * FROM events WHERE active=1 ORDER BY start_date DESC").fetchall()
    if request.method == 'POST':
        name        = request.form['name']
        description = request.form['description']
        location    = request.form['location']
        contact     = request.form['contact']
        category    = request.form.get('category', 'Other')
        item_name   = request.form.get('item_name', '')
        is_emergency= 1 if request.form.get('is_emergency') else 0
        event_id    = request.form.get('event_id') or None
        tags        = request.form.get('tags', '')

        # ✅ Handle both file upload and camera capture (preserved & sanitized)
        if 'camera_image' in request.form and request.form['camera_image']:
            img_data = request.form['camera_image'].split(",")[1]
            filename = f"camera_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(img_data))
        else:
            image    = request.files['image']
            if image and image.filename:
                orig_filename = secure_filename(image.filename)
                base, ext = os.path.splitext(orig_filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{base}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
            else:
                filename = ""

        cursor.execute(
            "INSERT INTO items (type, name, description, location, contact, image, date, "
            "category, is_emergency, status, event_id, tags, item_name) "
<<<<<<< HEAD
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id",
=======
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
            ('Lost', name, description, location, contact, filename,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             category, is_emergency, 'Active', event_id, tags, item_name)
        )
<<<<<<< HEAD
        new_id = cursor.fetchone()['id']
        db.commit()
=======
        db.commit()
        new_id = cursor.lastrowid
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b

        add_timeline_event(new_id, "Reported Lost", f"Reported by {name} at {location}")
        log_audit("Report Lost", f"Item '{item_name or description[:30]}' reported lost by {name}", contact)
        check_and_award_badges(contact)

        # Check for auto-matches on found items
        matches = get_matches(item_name, category, location, description, 'Found')
        if matches:
            session['last_submit_matches'] = [dict(m) for m in matches]

        send_notification_email(name, description, location, contact, "Lost", filename)
        flash("Lost item reported successfully! Notification sent.", "success")
        return redirect(url_for('index'))

    return render_template('lost.html', events=events)


@app.route('/found', methods=['GET', 'POST'])
def found():
    db = get_db()
    cursor = db.cursor()
    events = cursor.execute("SELECT * FROM events WHERE active=1 ORDER BY start_date DESC").fetchall()
    if request.method == 'POST':
        name           = request.form['name']
        description    = request.form['description']
        location       = request.form['location']
        contact        = request.form['contact']
        category       = request.form.get('category', 'Other')
        item_name      = request.form.get('item_name', '')
        item_condition = request.form.get('item_condition', 'Unknown')
        event_id       = request.form.get('event_id') or None
        tags           = request.form.get('tags', '')

        # ✅ Handle both file upload and camera capture (preserved & sanitized)
        if 'camera_image' in request.form and request.form['camera_image']:
            img_data = request.form['camera_image'].split(",")[1]
            filename = f"camera_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(img_data))
        else:
            image    = request.files['image']
            if image and image.filename:
                orig_filename = secure_filename(image.filename)
                base, ext = os.path.splitext(orig_filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{base}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
            else:
                filename = ""

        cursor.execute(
            "INSERT INTO items (type, name, description, location, contact, image, date, "
            "category, status, event_id, tags, item_name, item_condition) "
<<<<<<< HEAD
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id",
=======
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
            ('Found', name, description, location, contact, filename,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             category, 'Active', event_id, tags, item_name, item_condition)
        )
<<<<<<< HEAD
        new_id = cursor.fetchone()['id']
        db.commit()
=======
        db.commit()
        new_id = cursor.lastrowid
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b

        add_timeline_event(new_id, "Reported Found", f"Found by {name} at {location}")
        log_audit("Report Found", f"Item '{item_name or description[:30]}' found by {name}", contact)
        check_and_award_badges(contact)

        # Check for auto-matches on lost items
        matches = get_matches(item_name, category, location, description, 'Lost')
        if matches:
            session['last_submit_matches'] = [dict(m) for m in matches]

        send_notification_email(name, description, location, contact, "Found", filename)
        flash("Found item reported successfully! Notification sent.", "success")
        return redirect(url_for('index'))

    return render_template('found.html', events=events)
@app.route('/view')
def view_items():
    db = get_db()
    cursor = db.cursor()
    
    type_filter     = request.args.get('type', '')
    category_filter = request.args.get('category', '')
    location_filter = request.args.get('location', '')
    status_filter   = request.args.get('status', '')
    search_q        = request.args.get('q', '')
    date_from       = request.args.get('date_from', '')
    date_to         = request.args.get('date_to', '')
    
    page = int(request.args.get('page', 1))
    per_page = 12
    offset = (page - 1) * per_page

    query  = "SELECT * FROM items WHERE 1=1"
    params = []
    if type_filter:
<<<<<<< HEAD
        query += " AND type=%s"; params.append(type_filter)
    if category_filter:
        query += " AND category=%s"; params.append(category_filter)
    if status_filter:
        query += " AND status=%s"; params.append(status_filter)
    if location_filter:
        query += " AND location LIKE %s"; params.append(f"%{location_filter}%")
    if search_q:
        query += " AND (description LIKE %s OR item_name LIKE %s OR location LIKE %s OR name LIKE %s)"
        params += [f"%{search_q}%"] * 4
    if date_from:
        query += " AND date >= %s"
        params.append(f"{date_from} 00:00:00")
    if date_to:
        query += " AND date <= %s"
=======
        query += " AND type=?"; params.append(type_filter)
    if category_filter:
        query += " AND category=?"; params.append(category_filter)
    if status_filter:
        query += " AND status=?"; params.append(status_filter)
    if location_filter:
        query += " AND location LIKE ?"; params.append(f"%{location_filter}%")
    if search_q:
        query += " AND (description LIKE ? OR item_name LIKE ? OR location LIKE ? OR name LIKE ?)"
        params += [f"%{search_q}%"] * 4
    if date_from:
        query += " AND date >= ?"
        params.append(f"{date_from} 00:00:00")
    if date_to:
        query += " AND date <= ?"
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        params.append(f"{date_to} 23:59:59")

    # Get total count for pagination
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    total_items = cursor.execute(count_query, params).fetchone()[0]
    total_pages = math.ceil(total_items / per_page)

<<<<<<< HEAD
    query += " ORDER BY date DESC LIMIT %s OFFSET %s"
=======
    query += " ORDER BY date DESC LIMIT ? OFFSET ?"
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    items = cursor.execute(query, params + [per_page, offset]).fetchall()
    
    categories = [r[0] for r in cursor.execute("SELECT DISTINCT category FROM items WHERE category IS NOT NULL").fetchall()]
    locations  = [r[0] for r in cursor.execute("SELECT DISTINCT location FROM items ORDER BY location").fetchall()]
    stats = get_stats()
    
    return render_template('view_items.html',
        items=items, categories=categories, locations=locations,
        stats=stats,
        type_filter=type_filter, category_filter=category_filter,
        status_filter=status_filter, location_filter=location_filter, search_q=search_q,
        date_from=date_from, date_to=date_to,
        page=page, total_pages=total_pages)


@app.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_item(id):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    result = cursor.execute("SELECT image, name, contact FROM items WHERE id=%s", (id,)).fetchone()
=======
    result = cursor.execute("SELECT image, name, contact FROM items WHERE id=?", (id,)).fetchone()
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    if result:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], result['image'])
        if os.path.exists(image_path) and result['image']:
            try:
                os.remove(image_path)
<<<<<<< HEAD
            except Exception as e:
                db.rollback()
        cursor.execute("DELETE FROM items WHERE id=%s", (id,))
        cursor.execute("DELETE FROM item_timeline WHERE item_id=%s", (id,))
        cursor.execute("DELETE FROM item_tags WHERE item_id=%s", (id,))
=======
            except Exception:
                pass
        cursor.execute("DELETE FROM items WHERE id=?", (id,))
        cursor.execute("DELETE FROM item_timeline WHERE item_id=?", (id,))
        cursor.execute("DELETE FROM item_tags WHERE item_id=?", (id,))
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        db.commit()
        log_audit("Delete Item", f"Item ID {id} '{result['name']}' deleted", result['contact'])
    return redirect(url_for('view_items'))

# ═══════════════════════════════════════════════════════════════════════════════
#  NEW ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/item/<int:id>')
def item_detail(id):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    item = cursor.execute("SELECT * FROM items WHERE id=%s", (id,)).fetchone()
=======
    item = cursor.execute("SELECT * FROM items WHERE id=?", (id,)).fetchone()
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    if not item:
        flash("Item not found.", "danger")
        return redirect(url_for('view_items'))
    # Increment view count
<<<<<<< HEAD
    cursor.execute("UPDATE items SET view_count = COALESCE(view_count,0)+1 WHERE id=%s", (id,))
    db.commit()
    timeline = cursor.execute(
        "SELECT * FROM item_timeline WHERE item_id=%s ORDER BY timestamp ASC", (id,)
    ).fetchall()
    claims = cursor.execute(
        "SELECT * FROM claims WHERE item_id=%s ORDER BY submitted_at DESC", (id,)
    ).fetchall()
    storage_info = cursor.execute(
        "SELECT * FROM storage WHERE item_id=%s ORDER BY id DESC LIMIT 1", (id,)
    ).fetchone()
    feedback_list = cursor.execute(
        "SELECT * FROM feedback WHERE item_id=%s ORDER BY submitted_at DESC", (id,)
    ).fetchall()
    # Nearby similar items (same category or location)
    nearby = cursor.execute(
        "SELECT * FROM items WHERE id!=%s AND (category=%s OR location=%s) AND status='Active' LIMIT 4",
=======
    cursor.execute("UPDATE items SET view_count = COALESCE(view_count,0)+1 WHERE id=?", (id,))
    db.commit()
    timeline = cursor.execute(
        "SELECT * FROM item_timeline WHERE item_id=? ORDER BY timestamp ASC", (id,)
    ).fetchall()
    claims = cursor.execute(
        "SELECT * FROM claims WHERE item_id=? ORDER BY submitted_at DESC", (id,)
    ).fetchall()
    storage_info = cursor.execute(
        "SELECT * FROM storage WHERE item_id=? ORDER BY id DESC LIMIT 1", (id,)
    ).fetchone()
    feedback_list = cursor.execute(
        "SELECT * FROM feedback WHERE item_id=? ORDER BY submitted_at DESC", (id,)
    ).fetchall()
    # Nearby similar items (same category or location)
    nearby = cursor.execute(
        "SELECT * FROM items WHERE id!=? AND (category=? OR location=?) AND status='Active' LIMIT 4",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (id, item['category'], item['location'])
    ).fetchall()
    tags = item['tags'].split(',') if item['tags'] else []
    log_audit("View Item", f"Item ID {id} viewed", "Anonymous")
    
    # Send now variable for min date
    now = datetime.now().strftime("%Y-%m-%d")
    
    return render_template('item_detail.html',
        item=item, timeline=timeline, claims=claims,
        storage_info=storage_info, feedback_list=feedback_list,
        nearby=nearby, tags=tags, now=now)


@app.route('/claim/<int:id>', methods=['POST'])
def submit_claim(id):
    db = get_db()
    cursor = db.cursor()
    claimant_name    = request.form['claimant_name']
    claimant_contact = request.form['claimant_contact']
    claim_desc       = request.form['claim_description']

    cursor.execute(
        "INSERT INTO claims (item_id, claimant_name, claimant_contact, claim_description, status, submitted_at) "
<<<<<<< HEAD
        "VALUES (%s,%s,%s,%s,%s,%s)",
=======
        "VALUES (?,?,?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (id, claimant_name, claimant_contact, claim_desc, 'Pending',
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    db.commit()
    add_timeline_event(id, "Claim Requested", f"Claim submitted by {claimant_name}")
<<<<<<< HEAD
    cursor.execute("UPDATE items SET status='Claimed' WHERE id=%s AND status='Active'", (id,))
=======
    cursor.execute("UPDATE items SET status='Claimed' WHERE id=? AND status='Active'", (id,))
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    db.commit()
    log_audit("Submit Claim", f"Claim for item {id} by {claimant_name}", claimant_contact)
    flash("Claim submitted successfully! Admin will verify.", "success")
    return redirect(url_for('item_detail', id=id))


@app.route('/claim/approve/<int:claim_id>', methods=['POST'])
@admin_required
def approve_claim(claim_id):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    claim = cursor.execute("SELECT * FROM claims WHERE id=%s", (claim_id,)).fetchone()
    if claim:
        cursor.execute("UPDATE claims SET status='Approved' WHERE id=%s", (claim_id,))
        cursor.execute("UPDATE items SET status='Recovered' WHERE id=%s", (claim['item_id'],))
=======
    claim = cursor.execute("SELECT * FROM claims WHERE id=?", (claim_id,)).fetchone()
    if claim:
        cursor.execute("UPDATE claims SET status='Approved' WHERE id=?", (claim_id,))
        cursor.execute("UPDATE items SET status='Recovered' WHERE id=?", (claim['item_id'],))
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        db.commit()
        add_timeline_event(claim['item_id'], "Claim Approved", f"Approved for {claim['claimant_name']}")
        add_timeline_event(claim['item_id'], "Item Recovered", "Item successfully returned to owner")
        log_audit("Approve Claim", f"Claim {claim_id} approved, item {claim['item_id']} recovered", "Admin")
        flash("Claim approved and item marked as Recovered!", "success")
    return redirect(url_for('dashboard'))


@app.route('/claim/reject/<int:claim_id>', methods=['POST'])
@admin_required
def reject_claim(claim_id):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    claim = cursor.execute("SELECT * FROM claims WHERE id=%s", (claim_id,)).fetchone()
    if claim:
        cursor.execute("UPDATE claims SET status='Rejected' WHERE id=%s", (claim_id,))
        cursor.execute("UPDATE items SET status='Active' WHERE id=%s", (claim['item_id'],))
=======
    claim = cursor.execute("SELECT * FROM claims WHERE id=?", (claim_id,)).fetchone()
    if claim:
        cursor.execute("UPDATE claims SET status='Rejected' WHERE id=?", (claim_id,))
        cursor.execute("UPDATE items SET status='Active' WHERE id=?", (claim['item_id'],))
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        db.commit()
        add_timeline_event(claim['item_id'], "Claim Rejected", f"Claim by {claim['claimant_name']} rejected")
        log_audit("Reject Claim", f"Claim {claim_id} rejected", "Admin")
        flash("Claim rejected.", "warning")
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
@admin_required
def dashboard():
    db = get_db()
    cursor = db.cursor()
    stats = get_stats()
    # Monthly data for charts (last 6 months)
    months_data = []
    for i in range(5, -1, -1):
        d = datetime.now() - timedelta(days=30 * i)
        month_str = d.strftime("%Y-%m")
        month_label = d.strftime("%b %Y")
<<<<<<< HEAD
        lost_c  = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Lost' AND date LIKE %s",
                                 (f"{month_str}%",)).fetchone()[0]
        found_c = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Found' AND date LIKE %s",
                                 (f"{month_str}%",)).fetchone()[0]
        rec_c   = cursor.execute("SELECT COUNT(*) FROM items WHERE status='Recovered' AND date LIKE %s",
=======
        lost_c  = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Lost' AND date LIKE ?",
                                 (f"{month_str}%",)).fetchone()[0]
        found_c = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Found' AND date LIKE ?",
                                 (f"{month_str}%",)).fetchone()[0]
        rec_c   = cursor.execute("SELECT COUNT(*) FROM items WHERE status='Recovered' AND date LIKE ?",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
                                 (f"{month_str}%",)).fetchone()[0]
        months_data.append({'label': month_label, 'lost': lost_c, 'found': found_c, 'recovered': rec_c})

    # Category breakdown (Row converted to list)
    cat_data_rows = cursor.execute(
        "SELECT category, COUNT(*) as cnt FROM items GROUP BY category ORDER BY cnt DESC LIMIT 8"
    ).fetchall()
    cat_data = [list(row) for row in cat_data_rows]

    # Pending claims
    pending_claims = cursor.execute(
        "SELECT c.*, i.description, i.category, i.type FROM claims c "
        "JOIN items i ON c.item_id=i.id WHERE c.status='Pending' ORDER BY c.submitted_at DESC"
    ).fetchall()

    # Storage expiry alerts
    now = datetime.now()
    expiry_30 = cursor.execute(
        "SELECT s.*, i.description, i.category FROM storage s JOIN items i ON s.item_id=i.id "
<<<<<<< HEAD
        "WHERE s.collected=0 AND s.expiry_date <= %s AND s.expiry_date > %s",
=======
        "WHERE s.collected=0 AND s.expiry_date <= ? AND s.expiry_date > ?",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        ((now + timedelta(days=30)).strftime("%Y-%m-%d"),
         now.strftime("%Y-%m-%d"))
    ).fetchall()

    # Recent activity feed
    feed = cursor.execute(
        "SELECT action, details, contact, timestamp FROM audit_log ORDER BY timestamp DESC LIMIT 15"
    ).fetchall()

    # Top categories by recovery (Row converted to list)
    top_cats_rows = cursor.execute(
        "SELECT category, COUNT(*) as cnt FROM items WHERE status='Recovered' "
        "GROUP BY category ORDER BY cnt DESC LIMIT 5"
    ).fetchall()
    top_cats = [list(row) for row in top_cats_rows]

    # Recent items
    recent_items = cursor.execute(
        "SELECT * FROM items ORDER BY date DESC LIMIT 5"
    ).fetchall()

    staff_emails = cursor.execute("SELECT * FROM staff_emails ORDER BY email").fetchall()

    return render_template('dashboard.html',
        stats=stats, months_data=months_data, cat_data=cat_data,
        pending_claims=pending_claims, expiry_30=expiry_30,
        feed=feed, top_cats=top_cats, recent_items=recent_items,
        staff_emails=staff_emails)


@app.route('/admin/staff-emails/add', methods=['POST'])
@admin_required
def add_staff_email():
    email = request.form.get('email', '').strip()
    if email:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.", "danger")
        else:
            db = get_db()
            cursor = db.cursor()
            try:
<<<<<<< HEAD
                cursor.execute("INSERT INTO staff_emails (email) VALUES (%s)", (email,))
                db.commit()
                log_audit("Add Staff Email", f"Added '{email}'", "Admin")
                flash(f"Staff email '{email}' added successfully.", "success")
            except psycopg2.errors.UniqueViolation:
=======
                cursor.execute("INSERT INTO staff_emails (email) VALUES (?)", (email,))
                db.commit()
                log_audit("Add Staff Email", f"Added '{email}'", "Admin")
                flash(f"Staff email '{email}' added successfully.", "success")
            except sqlite3.IntegrityError:
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
                flash("Email already exists.", "warning")
    else:
        flash("Email is required.", "danger")
    return redirect(url_for('dashboard'))


@app.route('/admin/staff-emails/delete/<int:id>', methods=['POST'])
@admin_required
def delete_staff_email(id):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    row = cursor.execute("SELECT email FROM staff_emails WHERE id=%s", (id,)).fetchone()
    if row:
        cursor.execute("DELETE FROM staff_emails WHERE id=%s", (id,))
=======
    row = cursor.execute("SELECT email FROM staff_emails WHERE id=?", (id,)).fetchone()
    if row:
        cursor.execute("DELETE FROM staff_emails WHERE id=?", (id,))
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        db.commit()
        log_audit("Delete Staff Email", f"Deleted '{row['email']}'", "Admin")
        flash(f"Staff email '{row['email']}' removed.", "info")
    return redirect(url_for('dashboard'))



@app.route('/admin/storage')
@admin_required
def storage():
    db = get_db()
    cursor = db.cursor()
    items_in_storage = cursor.execute(
        "SELECT s.*, i.description, i.category, i.type, i.date, i.contact "
        "FROM storage s JOIN items i ON s.item_id=i.id ORDER BY s.assigned_date DESC"
    ).fetchall()
    # Items not in storage yet (found items that are active)
    unassigned = cursor.execute(
        "SELECT i.* FROM items i LEFT JOIN storage s ON i.id=s.item_id "
        "WHERE s.id IS NULL AND i.type='Found' AND i.status='Active'"
    ).fetchall()
    now = datetime.now()
    return render_template('admin/storage.html',
        items_in_storage=items_in_storage,
        unassigned=unassigned,
        now=now)


@app.route('/admin/storage/assign', methods=['POST'])
@admin_required
def assign_storage():
    db = get_db()
    cursor = db.cursor()
    item_id   = request.form['item_id']
    rack      = request.form['rack_number']
    shelf     = request.form['shelf_number']
    days      = int(request.form.get('expiry_days', 90))
    exp_date  = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    cursor.execute(
<<<<<<< HEAD
        "INSERT INTO storage (item_id, rack_number, shelf_number, assigned_date, expiry_date) VALUES (%s,%s,%s,%s,%s)",
=======
        "INSERT INTO storage (item_id, rack_number, shelf_number, assigned_date, expiry_date) VALUES (?,?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (item_id, rack, shelf, datetime.now().strftime("%Y-%m-%d"), exp_date)
    )
    db.commit()
    add_timeline_event(int(item_id), "Assigned to Storage", f"Rack {rack}, Shelf {shelf}. Expires {exp_date}")
    log_audit("Assign Storage", f"Item {item_id} → Rack {rack} / Shelf {shelf}", "Admin")
    flash(f"Item assigned to Rack {rack}, Shelf {shelf}. Expires in {days} days.", "success")
    return redirect(url_for('storage'))


@app.route('/admin/storage/collect/<int:storage_id>', methods=['POST'])
@admin_required
def mark_collected(storage_id):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    row = cursor.execute("SELECT item_id FROM storage WHERE id=%s", (storage_id,)).fetchone()
    if row:
        cursor.execute("UPDATE storage SET collected=1 WHERE id=%s", (storage_id,))
        cursor.execute("UPDATE items SET status='Collected' WHERE id=%s", (row['item_id'],))
=======
    row = cursor.execute("SELECT item_id FROM storage WHERE id=?", (storage_id,)).fetchone()
    if row:
        cursor.execute("UPDATE storage SET collected=1 WHERE id=?", (storage_id,))
        cursor.execute("UPDATE items SET status='Collected' WHERE id=?", (row['item_id'],))
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        db.commit()
        add_timeline_event(row['item_id'], "Collected", "Item collected from storage")
        log_audit("Mark Collected", f"Storage {storage_id}, item {row['item_id']}", "Admin")
        flash("Item marked as collected.", "success")
    return redirect(url_for('storage'))


@app.route('/admin/analytics')
@admin_required
def analytics():
    db = get_db()
    cursor = db.cursor()
    stats = get_stats()
    # Monthly trend (12 months)
    monthly = []
    for i in range(11, -1, -1):
        d = datetime.now() - timedelta(days=30 * i)
        month_str = d.strftime("%Y-%m")
        month_label = d.strftime("%b %Y")
<<<<<<< HEAD
        lost_c  = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Lost'  AND date LIKE %s", (f"{month_str}%",)).fetchone()[0]
        found_c = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Found' AND date LIKE %s", (f"{month_str}%",)).fetchone()[0]
        rec_c   = cursor.execute("SELECT COUNT(*) FROM items WHERE status='Recovered' AND date LIKE %s", (f"{month_str}%",)).fetchone()[0]
=======
        lost_c  = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Lost'  AND date LIKE ?", (f"{month_str}%",)).fetchone()[0]
        found_c = cursor.execute("SELECT COUNT(*) FROM items WHERE type='Found' AND date LIKE ?", (f"{month_str}%",)).fetchone()[0]
        rec_c   = cursor.execute("SELECT COUNT(*) FROM items WHERE status='Recovered' AND date LIKE ?", (f"{month_str}%",)).fetchone()[0]
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        monthly.append({'label': month_label, 'lost': lost_c, 'found': found_c, 'recovered': rec_c})

    # Category stats
    cat_stats = cursor.execute(
        "SELECT category, "
        "SUM(CASE WHEN type='Lost' THEN 1 ELSE 0 END) as lost_cnt, "
        "SUM(CASE WHEN type='Found' THEN 1 ELSE 0 END) as found_cnt, "
        "SUM(CASE WHEN status='Recovered' THEN 1 ELSE 0 END) as rec_cnt "
        "FROM items GROUP BY category ORDER BY (lost_cnt+found_cnt) DESC"
    ).fetchall()

    # Location stats
    loc_stats = cursor.execute(
        "SELECT location, COUNT(*) as cnt, "
        "SUM(CASE WHEN status='Recovered' THEN 1 ELSE 0 END) as recovered "
        "FROM items GROUP BY location ORDER BY cnt DESC LIMIT 10"
    ).fetchall()

    # Most viewed items
    popular = cursor.execute(
        "SELECT * FROM items ORDER BY view_count DESC LIMIT 5"
    ).fetchall()

    return render_template('admin/analytics.html',
        stats=stats, monthly=monthly, cat_stats=cat_stats,
        loc_stats=loc_stats, popular=popular)


@app.route('/admin/audit')
@admin_required
def audit_log_view():
    db = get_db()
    cursor = db.cursor()
    page = int(request.args.get('page', 1))
    per_page = 25
    offset   = (page - 1) * per_page
    action_filter = request.args.get('action', '')
    query = "SELECT * FROM audit_log"
    params = []
    if action_filter:
<<<<<<< HEAD
        query += " WHERE action LIKE %s"
        params.append(f"%{action_filter}%")
    query += " ORDER BY timestamp DESC LIMIT %s OFFSET %s"
=======
        query += " WHERE action LIKE ?"
        params.append(f"%{action_filter}%")
    query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    params += [per_page, offset]
    logs = cursor.execute(query, params).fetchall()
    total = cursor.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
    return render_template('admin/audit.html',
        logs=logs, page=page, per_page=per_page,
        total=total, action_filter=action_filter)


@app.route('/admin/announcements', methods=['GET', 'POST'])
@admin_required
def announcements():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        title    = request.form['title']
        message  = request.form['message']
        ann_type = request.form.get('type', 'info')
        expires  = request.form.get('expires_at') or None
        cursor.execute(
<<<<<<< HEAD
            "INSERT INTO announcements (title, message, type, created_at, expires_at) VALUES (%s,%s,%s,%s,%s)",
=======
            "INSERT INTO announcements (title, message, type, created_at, expires_at) VALUES (?,?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
            (title, message, ann_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), expires)
        )
        db.commit()
        log_audit("Post Announcement", f"'{title}'", "Admin")
        flash("Announcement posted.", "success")
        return redirect(url_for('announcements'))
    anns = cursor.execute("SELECT * FROM announcements ORDER BY created_at DESC").fetchall()
    return render_template('admin/announcements.html', announcements=anns)


@app.route('/admin/announcements/delete/<int:id>', methods=['POST'])
@admin_required
def delete_announcement(id):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    cursor.execute("UPDATE announcements SET active=0 WHERE id=%s", (id,))
=======
    cursor.execute("UPDATE announcements SET active=0 WHERE id=?", (id,))
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    db.commit()
    log_audit("Deactivate Announcement", f"ID {id}", "Admin")
    flash("Announcement deactivated.", "info")
    return redirect(url_for('announcements'))


@app.route('/admin/items/<int:id>/status', methods=['POST'])
@admin_required
def update_item_status(id):
    db = get_db()
    cursor = db.cursor()
    new_status = request.form['status']
<<<<<<< HEAD
    cursor.execute("UPDATE items SET status=%s WHERE id=%s", (new_status, id))
=======
    cursor.execute("UPDATE items SET status=? WHERE id=?", (new_status, id))
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    db.commit()
    add_timeline_event(id, f"Status → {new_status}", f"Updated by Admin")
    log_audit("Update Status", f"Item {id} → {new_status}", "Admin")
    flash(f"Item status updated to {new_status}.", "success")
    return redirect(url_for('item_detail', id=id))


@app.route('/events', methods=['GET', 'POST'])
def events():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        # Protect POST only with admin check
        if not session.get('is_admin'):
            flash("Admin login required.", "warning")
            return redirect(url_for('admin_login'))
            
        name       = request.form['name']
        event_type = request.form['event_type']
        location   = request.form['location']
        start_date = request.form['start_date']
        end_date   = request.form['end_date']
        desc       = request.form.get('description', '')
        cursor.execute(
<<<<<<< HEAD
            "INSERT INTO events (name, event_type, location, start_date, end_date, description) VALUES (%s,%s,%s,%s,%s,%s)",
=======
            "INSERT INTO events (name, event_type, location, start_date, end_date, description) VALUES (?,?,?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
            (name, event_type, location, start_date, end_date, desc)
        )
        db.commit()
        log_audit("Create Event", f"'{name}' ({event_type})", "Admin")
        flash("Event created successfully.", "success")
        return redirect(url_for('events'))

    all_events = cursor.execute("SELECT * FROM events ORDER BY start_date DESC").fetchall()
    # Count items per event
    event_items = {}
    for ev in all_events:
<<<<<<< HEAD
        cnt = cursor.execute("SELECT COUNT(*) FROM items WHERE event_id=%s", (ev['id'],)).fetchone()[0]
=======
        cnt = cursor.execute("SELECT COUNT(*) FROM items WHERE event_id=?", (ev['id'],)).fetchone()[0]
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        event_items[ev['id']] = cnt
    return render_template('events.html', events=all_events, event_items=event_items)


@app.route('/volunteers', methods=['GET', 'POST'])
def volunteers():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        name    = request.form['name']
        contact = request.form['contact']
        role    = request.form.get('role', 'Helper')
        # Check if already registered
        existing = cursor.execute(
<<<<<<< HEAD
            "SELECT id FROM volunteers WHERE contact=%s", (contact,)
=======
            "SELECT id FROM volunteers WHERE contact=?", (contact,)
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        ).fetchone()
        if existing:
            flash("You are already registered as a volunteer!", "warning")
        else:
            cursor.execute(
<<<<<<< HEAD
                "INSERT INTO volunteers (name, contact, role, registered_at) VALUES (%s,%s,%s,%s)",
=======
                "INSERT INTO volunteers (name, contact, role, registered_at) VALUES (?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
                (name, contact, role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            db.commit()
            log_audit("Register Volunteer", f"{name} as {role}", contact)
            flash("Thank you for volunteering!", "success")
        return redirect(url_for('volunteers'))

    vols = cursor.execute(
        "SELECT * FROM volunteers WHERE active=1 ORDER BY contribution_count DESC"
    ).fetchall()
    return render_template('volunteers.html', volunteers=vols)


@app.route('/success-stories', methods=['GET'])
def success_stories():
    db = get_db()
    cursor = db.cursor()
    stories = cursor.execute(
        "SELECT s.*, i.description, i.category, i.type, i.location "
        "FROM success_stories s LEFT JOIN items i ON s.item_id=i.id "
        "WHERE s.approved=1 ORDER BY s.submitted_at DESC"
    ).fetchall()
    stats = get_stats()
    return render_template('success_stories.html', stories=stories, stats=stats)


@app.route('/success-stories/add', methods=['POST'])
def add_story():
    db = get_db()
    cursor = db.cursor()
    item_id      = request.form.get('item_id')
    title        = request.form['title']
    story        = request.form['story']
    rec_days     = request.form.get('recovery_days', 0)
    submitted_by = request.form['submitted_by']
    cursor.execute(
        "INSERT INTO success_stories (item_id, title, story, recovery_days, submitted_by, submitted_at, approved) "
<<<<<<< HEAD
        "VALUES (%s,%s,%s,%s,%s,%s,1)",
=======
        "VALUES (?,?,?,?,?,?,1)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (item_id, title, story, rec_days, submitted_by,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    db.commit()
    if item_id:
        add_timeline_event(int(item_id), "Success Story Added", title)
    log_audit("Add Success Story", title, submitted_by)
    flash("Success story submitted!", "success")
    return redirect(url_for('success_stories'))


@app.route('/profile/<contact>')
def profile(contact):
    db = get_db()
    cursor = db.cursor()
    submitted_items = cursor.execute(
<<<<<<< HEAD
        "SELECT * FROM items WHERE contact=%s ORDER BY date DESC", (contact,)
    ).fetchall()
    claims_made = cursor.execute(
        "SELECT c.*, i.description, i.type FROM claims c "
        "JOIN items i ON c.item_id=i.id WHERE c.claimant_contact=%s ORDER BY c.submitted_at DESC",
        (contact,)
    ).fetchall()
    user_badges = cursor.execute(
        "SELECT * FROM badges WHERE contact=%s ORDER BY earned_at DESC", (contact,)
    ).fetchall()
    feedbacks   = cursor.execute(
        "SELECT * FROM feedback WHERE name=%s ORDER BY submitted_at DESC", (contact,)
=======
        "SELECT * FROM items WHERE contact=? ORDER BY date DESC", (contact,)
    ).fetchall()
    claims_made = cursor.execute(
        "SELECT c.*, i.description, i.type FROM claims c "
        "JOIN items i ON c.item_id=i.id WHERE c.claimant_contact=? ORDER BY c.submitted_at DESC",
        (contact,)
    ).fetchall()
    user_badges = cursor.execute(
        "SELECT * FROM badges WHERE contact=? ORDER BY earned_at DESC", (contact,)
    ).fetchall()
    feedbacks   = cursor.execute(
        "SELECT * FROM feedback WHERE name=? ORDER BY submitted_at DESC", (contact,)
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    ).fetchall()
    # Stats
    user_stats = {
        'total_reported': len(submitted_items),
        'lost_reported': sum(1 for i in submitted_items if i['type'] == 'Lost'),
        'found_reported': sum(1 for i in submitted_items if i['type'] == 'Found'),
        'recovered': sum(1 for i in submitted_items if i['status'] == 'Recovered'),
        'badges_earned': len(user_badges),
    }
    check_and_award_badges(contact)
    return render_template('profile.html',
        contact=contact, submitted_items=submitted_items,
        claims_made=claims_made, user_badges=user_badges,
        feedbacks=feedbacks, user_stats=user_stats)


@app.route('/feedback/<int:id>', methods=['POST'])
def submit_feedback(id):
    db = get_db()
    cursor = db.cursor()
    name    = request.form['name']
    rating  = request.form['rating']
    comment = request.form['comment']
    cursor.execute(
<<<<<<< HEAD
        "INSERT INTO feedback (item_id, name, rating, comment, submitted_at) VALUES (%s,%s,%s,%s,%s)",
=======
        "INSERT INTO feedback (item_id, name, rating, comment, submitted_at) VALUES (?,?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (id, name, rating, comment, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    db.commit()
    log_audit("Submit Feedback", f"Rating {rating}/5 for item {id}", name)
    flash("Thank you for your feedback!", "success")
    return redirect(url_for('item_detail', id=id))


@app.route('/appointments', methods=['POST'])
def book_appointment():
    db = get_db()
    cursor = db.cursor()
    item_id   = request.form['item_id']
    name      = request.form['name']
    contact   = request.form['contact']
    appt_date = request.form['appointment_date']
    time_slot = request.form['time_slot']
    cursor.execute(
<<<<<<< HEAD
        "INSERT INTO appointments (item_id, name, contact, appointment_date, time_slot, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
=======
        "INSERT INTO appointments (item_id, name, contact, appointment_date, time_slot, created_at) VALUES (?,?,?,?,?,?)",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (item_id, name, contact, appt_date, time_slot,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    db.commit()
    add_timeline_event(int(item_id), "Collection Appointment", f"{name} booked slot {appt_date} {time_slot}")
    log_audit("Book Appointment", f"Item {item_id} by {name} on {appt_date} {time_slot}", contact)
    flash("Collection appointment booked!", "success")
    return redirect(url_for('item_detail', id=item_id))


# ─── Auth Routes ─────────────────────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == admin_password_raw:
            session['is_admin'] = True
            log_audit("Admin Login", "Logged in successfully", "Admin")
            flash("Logged in successfully as Admin.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid password.", "danger")
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('index'))


# ─── Contact Proxy Route ──────────────────────────────────────────────────────
@app.route('/contact/<int:id>', methods=['GET', 'POST'])
def contact_reporter(id):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    item = cursor.execute("SELECT * FROM items WHERE id=%s", (id,)).fetchone()
=======
    item = cursor.execute("SELECT * FROM items WHERE id=?", (id,)).fetchone()
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    if not item:
        flash("Item not found.", "danger")
        return redirect(url_for('view_items'))
        
    if request.method == 'POST':
        viewer_name = request.form['viewer_name']
        viewer_contact = request.form['viewer_contact']
        viewer_message = request.form['viewer_message']
        
        log_audit("Contact Request", f"{viewer_name} requested contact for item {id}", viewer_contact)
        
        # Save flag in session to unlock reporter info for item
        session[f'show_contact_{id}'] = True
        
        flash("Contact info unlocked! You can now contact the reporter directly.", "success")
        return redirect(url_for('item_detail', id=id))
        
    return render_template('contact_reporter.html', item=item)


# ─── Dynamic QR Code PNG Endpoint ─────────────────────────────────────────────
@app.route('/qrcode/<int:id>')
def generate_qrcode(id):
    import qrcode
    import io
    from flask import send_file
    url = url_for('item_detail', id=id, _external=True)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


# ─── CSV/PDF Export Routes ────────────────────────────────────────────────────
@app.route('/export/csv')
@admin_required
def export_csv():
    import csv
    import io
    from flask import Response
    
    db = get_db()
    cursor = db.cursor()
    items = cursor.execute("SELECT * FROM items ORDER BY date DESC").fetchall()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Type', 'Item Name', 'Category', 'Description', 'Location', 'Status', 'Date', 'Contact'])
    
    for item in items:
        writer.writerow([
            item['id'],
            item['type'],
            item['item_name'],
            item['category'],
            item['description'],
            item['location'],
            item['status'],
            item['date'],
            item['contact']
        ])
        
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=lost_found_items.csv"}
    )


@app.route('/export/pdf')
@admin_required
def export_pdf():
    from fpdf import FPDF
    from flask import make_response
    
    db = get_db()
    cursor = db.cursor()
    items = cursor.execute("SELECT * FROM items ORDER BY date DESC").fetchall()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Lost & Found Items Report", ln=1, align="C")
    pdf.ln(10)
    
    # Table headers
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(10, 8, "ID", 1)
    pdf.cell(15, 8, "Type", 1)
    pdf.cell(40, 8, "Item Name", 1)
    pdf.cell(30, 8, "Category", 1)
    pdf.cell(45, 8, "Location", 1)
    pdf.cell(25, 8, "Status", 1)
    pdf.cell(25, 8, "Date", 1)
    pdf.ln()
    
    # Table rows
    pdf.set_font("Arial", size=9)
    for item in items:
        name = str(item['item_name'] or '')[:20].encode('latin-1', 'replace').decode('latin-1')
        category = str(item['category'] or '')[:15].encode('latin-1', 'replace').decode('latin-1')
        location = str(item['location'] or '')[:20].encode('latin-1', 'replace').decode('latin-1')
        status = str(item['status'] or '')[:10].encode('latin-1', 'replace').decode('latin-1')
        date_str = str(item['date'] or '')[:10]
        
        pdf.cell(10, 8, str(item['id']), 1)
        pdf.cell(15, 8, str(item['type']), 1)
        pdf.cell(40, 8, name, 1)
        pdf.cell(30, 8, category, 1)
        pdf.cell(45, 8, location, 1)
        pdf.cell(25, 8, status, 1)
        pdf.cell(25, 8, date_str, 1)
        pdf.ln()
        
    response = make_response(pdf.output(dest='S'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=lost_found_items.pdf'
    return response


# ═══════════════════════════════════════════════════════════════════════════════
#  API ENDPOINTS (JSON)
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())


@app.route('/api/feed')
def api_feed():
    db = get_db()
    cursor = db.cursor()
    feed = cursor.execute(
        "SELECT action, details, contact, timestamp FROM audit_log ORDER BY timestamp DESC LIMIT 20"
    ).fetchall()
    return jsonify([dict(f) for f in feed])


@app.route('/api/items/search')
def api_search():
    db = get_db()
    cursor = db.cursor()
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    results = cursor.execute(
        "SELECT id, type, item_name, description, location, category, status "
<<<<<<< HEAD
        "FROM items WHERE description LIKE %s OR item_name LIKE %s OR location LIKE %s "
=======
        "FROM items WHERE description LIKE ? OR item_name LIKE ? OR location LIKE ? "
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        "ORDER BY date DESC LIMIT 10",
        (f"%{q}%", f"%{q}%", f"%{q}%")
    ).fetchall()
    return jsonify([dict(r) for r in results])


@app.route('/api/nearby/<int:id>')
def api_nearby(id):
    db = get_db()
    cursor = db.cursor()
<<<<<<< HEAD
    item = cursor.execute("SELECT category, location FROM items WHERE id=%s", (id,)).fetchone()
=======
    item = cursor.execute("SELECT category, location FROM items WHERE id=?", (id,)).fetchone()
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
    if not item:
        return jsonify([])
    nearby = cursor.execute(
        "SELECT id, type, item_name, description, location, category, image "
<<<<<<< HEAD
        "FROM items WHERE id!=%s AND (category=%s OR location=%s) AND status='Active' LIMIT 4",
=======
        "FROM items WHERE id!=? AND (category=? OR location=?) AND status='Active' LIMIT 4",
>>>>>>> 675eecd2dbde899c0446afec0365b5b27fe8759b
        (id, item['category'], item['location'])
    ).fetchall()
    return jsonify([dict(n) for n in nearby])


@app.route('/api/items')
def api_items():
    db = get_db()
    cursor = db.cursor()
    items = cursor.execute(
        "SELECT id, type, item_name, description, location, category, status, date, is_emergency "
        "FROM items ORDER BY date DESC LIMIT 50"
    ).fetchall()
    return jsonify([dict(i) for i in items])


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
