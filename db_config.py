import os
import sqlite3
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db_config")

# Database connection configuration defaults
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "pupqc_plant_db")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))

# Fallback SQLite DB path
SQLITE_DB_PATH = Path(__file__).parent / "pupqc_plant_db.sqlite"


def get_mysql_connection():
    """Attempt to establish a MySQL connection using pymysql."""
    try:
        import pymysql
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            connect_timeout=3
        )
        logger.info("Connected to MySQL database: %s", MYSQL_DB)
        return conn
    except Exception as e:
        logger.warning("MySQL connection failed (%s). Falling back to SQLite.", e)
        return None


def get_sqlite_connection():
    """Create or connect to fallback SQLite database and return a connection with dictionary cursor row factory."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_sqlite_db():
    """Initialize SQLite database with tables and sample plant records if not existing."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        common_name TEXT NOT NULL,
        scientific_name TEXT NOT NULL,
        family TEXT NOT NULL,
        category_id INTEGER,
        local_name TEXT,
        conservation_status TEXT DEFAULT 'Least Concern',
        location_in_campus TEXT NOT NULL,
        description TEXT,
        medicinal_uses TEXT,
        ecological_role TEXT,
        image_url TEXT DEFAULT '/static/images/plants/default_plant.jpg',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    );
    """)

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        logger.info("Seeding SQLite database with default categories...")
        categories = [
            (1, 'Native & Endemic Trees', 'Trees native or indigenous to the Philippines'),
            (2, 'Medicinal Plants', 'Plants known for therapeutic, herbal, and traditional health uses'),
            (3, 'Ornamental Plants', 'Decorative plants grown for aesthetic appeal around campus buildings'),
            (4, 'Shade & Canopy Trees', 'Large spread trees providing canopy shade in quadrangle and walkways')
        ]
        cursor.executemany("INSERT INTO categories (id, name, description) VALUES (?, ?, ?)", categories)

    cursor.execute("SELECT COUNT(*) FROM plants")
    if cursor.fetchone()[0] == 0:
        logger.info("Seeding SQLite database with default plant data...")
        plants = [
            ('Narra', 'Pterocarpus indicus', 'Fabaceae', 1, 'Narra', 'Vulnerable', 'Main Quadrangle & East Lawn',
             'The National Tree of the Philippines. A large timber tree producing bright yellow flowers and valuable reddish wood.',
             'Bark decoction used traditionally for astringent properties.',
             'Provides dense shade, nitrogen fixation in soil, and habitat for local birds.',
             'https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?auto=format&fit=crop&w=600&q=80'),

            ('Banaba', 'Lagerstroemia speciosa', 'Lythraceae', 2, 'Banaba', 'Least Concern', 'PUPQC Front Garden & Entrance Path',
             'A deciduous tropical tree known for its striking pink to purple crinkled blossoms and distinctive smooth bark.',
             'Leaves are widely boiled into herbal tea for blood sugar control and kidney health.',
             'Attracts pollinators like bees and butterflies during bloom season.',
             'https://images.unsplash.com/photo-1509100194014-d49809396daa?auto=format&fit=crop&w=600&q=80'),

            ('Sampaguita', 'Jasminum sambac', 'Oleaceae', 3, 'Sampaguita', 'Least Concern', 'Administration Building Courtyard',
             'The National Flower of the Philippines. A sweet-scented evergreen shrub with small star-shaped white flowers.',
             'Infusion of flowers used to soothe headaches and eye inflammation.',
             'Aromatic attraction for beneficial pollinators and urban floral beauty.',
             'https://images.unsplash.com/photo-1596073413225-300dd1d21616?auto=format&fit=crop&w=600&q=80'),

            ('Acacia / Rain Tree', 'Samanea saman', 'Fabaceae', 4, 'Akasya', 'Least Concern', 'Campus Perimeter & Open Grounds',
             'A massive canopy tree with a wide umbrella crown that folds its leaves during rainfall and at night.',
             'Bark and seeds contain mild traditional antimicrobial compounds.',
             'Crucial canopy shade reducer for ground temperature and atmospheric carbon capture.',
             'https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=600&q=80'),

            ('Katmon', 'Dillenia philippinensis', 'Dilleniaceae', 1, 'Katmon', 'Vulnerable', 'Eco-Park & Botanical Corner',
             'An endemic Philippine fruit tree with large white fragrant flowers and edible fleshy green sour fruit.',
             'Juice from fresh fruit used for cough relief and natural hair cleanser.',
             'Endemic food source for fruit bats and indigenous avian species.',
             'https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?auto=format&fit=crop&w=600&q=80'),

            ('Bougainvillea', 'Bougainvillea spectabilis', 'Nyctaginaceae', 3, 'Bogambilya', 'Least Concern', 'Student Center Fencing & Terraces',
             'A thorny ornamental vine/shrub with vibrant magenta, purple, and orange flower-like bracts.',
             'Bark and leaves used in folk remedies for cough and fever.',
             'Urban greenery aesthetic, soil erosion control on sloped garden margins.',
             'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=600&q=80'),

            ('Neem Tree', 'Azadirachta indica', 'Meliaceae', 2, 'Neem', 'Least Concern', 'Library Rear Pathway',
             'A fast-growing evergreen tree known for its natural insect-repellent properties and dense foliage.',
             'Leaves used for natural antiseptic wash, organic pest repellent, and skin remedies.',
             'Natural mosquito repellent and air purifier along campus walkways.',
             'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=600&q=80'),

            ('Snake Plant', 'Sansevieria trifasciata', 'Asparagaceae', 3, 'Espada', 'Least Concern', 'Academic Building Corridors',
             'An evergreen perennial plant with vertical sword-like leaves with yellow-green variegated borders.',
             'Leaves traditionally crushed for topical poultice on minor skin cuts.',
             'Air purifying plant absorbing toxins like benzene and formaldehyde.',
             'https://images.unsplash.com/photo-1509423350716-97f9360b4e09?auto=format&fit=crop&w=600&q=80')
        ]
        cursor.executemany("""
            INSERT INTO plants 
            (common_name, scientific_name, family, category_id, local_name, conservation_status, location_in_campus, description, medicinal_uses, ecological_role, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, plants)

    conn.commit()
    conn.close()


def get_db():
    """Returns an active database abstraction object with unified query execution methods."""
    mysql_conn = get_mysql_connection()
    if mysql_conn:
        return DatabaseWrapper(mysql_conn, is_mysql=True)
    
    # Initialize SQLite if fallback needed
    init_sqlite_db()
    sqlite_conn = get_sqlite_connection()
    return DatabaseWrapper(sqlite_conn, is_mysql=False)


class DatabaseWrapper:
    """Wrapper to handle differences between MySQL dict cursor and SQLite Row cursor."""
    def __init__(self, connection, is_mysql=True):
        self.conn = connection
        self.is_mysql = is_mysql

    def execute_query(self, sql_query, params=None):
        if params is None:
            params = ()
        
        # SQLite uses '?' placeholder while MySQL uses '%s'
        if not self.is_mysql:
            sql_query = sql_query.replace("%s", "?")
            cursor = self.conn.cursor()
            cursor.execute(sql_query, params)
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            self.conn.close()
            return result
        else:
            with self.conn.cursor() as cursor:
                cursor.execute(sql_query, params)
                result = cursor.fetchall()
            self.conn.close()
            return result

    def execute_insert(self, sql_query, params=None):
        if params is None:
            params = ()

        if not self.is_mysql:
            sql_query = sql_query.replace("%s", "?")
            cursor = self.conn.cursor()
            cursor.execute(sql_query, params)
            last_id = cursor.lastrowid
            self.conn.commit()
            self.conn.close()
            return last_id
        else:
            with self.conn.cursor() as cursor:
                cursor.execute(sql_query, params)
                last_id = cursor.lastrowid
            self.conn.close()
            return last_id

    def execute_update(self, sql_query, params=None):
        if params is None:
            params = ()

        if not self.is_mysql:
            sql_query = sql_query.replace("%s", "?")
            cursor = self.conn.cursor()
            cursor.execute(sql_query, params)
            affected = cursor.rowcount
            self.conn.commit()
            self.conn.close()
            return affected
        else:
            with self.conn.cursor() as cursor:
                cursor.execute(sql_query, params)
                affected = cursor.rowcount
            self.conn.close()
            return affected
