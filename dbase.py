import sqlite3
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = 'UserDetails.db'

@contextmanager
def get_connection():
    """Get database connection with context manager for automatic cleanup"""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def init_database():
    """Initialize database tables if they don't exist"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            
            # Create UserData table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS UserData
                         (userid TEXT PRIMARY KEY, 
                          phonenumber TEXT, 
                          name TEXT,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            # Create Admin table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS Admin
                         (adminid TEXT PRIMARY KEY,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            # Create UserLifetime table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS UserLifetime
                         (userid TEXT PRIMARY KEY, 
                          lifetime INTEGER DEFAULT 1,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")
        raise

def fetch_phonenumber(userid):
    """Fetch phone number for a user"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT phonenumber FROM UserData WHERE userid = ?", (str(userid),))
            result = c.fetchone()
            if result:
                return result[0]
            return None
    except sqlite3.Error as e:
        logger.error(f"Error fetching phone number for user {userid}: {e}")
        return None

def fetch_UserData_table():
    """Fetch all user data"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM UserData")
            result = c.fetchall()
            return [dict(row) for row in result]  # Convert to list of dicts
    except sqlite3.Error as e:
        logger.error(f"Error fetching user data: {e}")
        return []

def check_admin(adminid):
    """Check if admin exists"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT adminid FROM Admin WHERE adminid = ?", (str(adminid),))
            result = c.fetchone()
            return result is not None
    except sqlite3.Error as e:
        logger.error(f"Error checking admin {adminid}: {e}")
        return False

def create_admin(adminid):
    """Create a new admin"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO Admin (adminid) VALUES (?)", (str(adminid),))
            logger.info(f"Admin {adminid} created successfully")
            return True
    except sqlite3.IntegrityError:
        logger.warning(f"Admin {adminid} already exists")
        return False
    except sqlite3.Error as e:
        logger.error(f"Error creating admin {adminid}: {e}")
        return False

def create_user_lifetime(userid):
    """Create user lifetime entry"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO UserLifetime (userid, lifetime) VALUES (?, ?)", 
                     (str(userid), 1))
            logger.info(f"User lifetime created for {userid}")
            return True
    except sqlite3.Error as e:
        logger.error(f"Error creating user lifetime for {userid}: {e}")
        return False

def add_user(userid, phonenumber=None, name=None):
    """Add or update a user in the database"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO UserData (userid, phonenumber, name)
                         VALUES (?, ?, ?)''', 
                     (str(userid), phonenumber, name))
            logger.info(f"User {userid} added/updated successfully")
            return True
    except sqlite3.Error as e:
        logger.error(f"Error adding user {userid}: {e}")
        return False

def get_user(userid):
    """Get user data by userid"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM UserData WHERE userid = ?", (str(userid),))
            result = c.fetchone()
            if result:
                return dict(result)
            return None
    except sqlite3.Error as e:
        logger.error(f"Error getting user {userid}: {e}")
        return None

def save_call_mapping(call_sid, userid):
    """Save mapping between Twilio CallSid and userid"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            # Create Calls table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS Calls
                         (call_sid TEXT PRIMARY KEY,
                          userid TEXT,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            c.execute("INSERT OR REPLACE INTO Calls (call_sid, userid) VALUES (?, ?)",
                     (str(call_sid), str(userid)))
            logger.info(f"Call mapping saved: {call_sid} -> {userid}")
            return True
    except sqlite3.Error as e:
        logger.error(f"Error saving call mapping: {e}")
        return False

def get_userid_from_call(call_sid):
    """Get userid from Twilio CallSid"""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT userid FROM Calls WHERE call_sid = ?", (str(call_sid),))
            result = c.fetchone()
            if result:
                return result[0]
            return None
    except sqlite3.Error as e:
        logger.error(f"Error getting userid from call {call_sid}: {e}")
        return None

# Initialize database on import
init_database()

