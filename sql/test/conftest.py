import sqlite3
import logging
import pytest


logging.basicConfig(level=logging.INFO,\
                    format='%(asctime)s - %(levelname)s - %(message)s'\
                    )
logger = logging.getLogger(__name__)

@pytest.fixture(scope='module')
def db_connection():
    try:
        path = ':memory:'
        script = '''
        CREATE TABLE IF NOT EXISTS workers (
            worker_id INTEGER PRIMARY KEY,
            name TEXT,
            shift TEXT
        );

        CREATE TABLE IF NOT EXISTS hubs (
            hub_id TEXT PRIMARY KEY,
            model TEXT,
            status TEXT,
            worker_id INTEGER,
            production_date DATE,
            FOREIGN KEY (worker_id) REFERENCES workers(worker_id)
        );

        INSERT OR IGNORE INTO workers VALUES (1, 'Ivan', 'Day'), (2, 'Olena', 'Night'), (3, 'Alex', 'Day');

        INSERT OR IGNORE INTO hubs VALUES 
        ('H101', 'Hub 2 Plus', 'Passed', 1, '2026-02-10'),
        ('H102', 'Hub 2', 'Failed', 1, '2026-02-10'),
        ('H103', 'Hub Hybrid', 'Passed', 2, '2026-02-11'),
        ('H104', 'Hub 2 Plus', 'Passed', 3, '2026-02-11'),
        ('H105', 'Hub 2 Plus', 'Failed', 1, '2026-02-12');
        '''

        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.executescript(script)

        logger.info('databse succesfully created')

        yield conn

        conn.rollback()
        conn.close()

    except sqlite3.Error as error:
        logger.error(f'DB error: {error}')
        
    except Exception as error:
        logger.critical(f'Unexpected error: {error}')


@pytest.fixture(scope='function')
def empty_db_cursor(db_connection: sqlite3.Connection):
    conn = db_connection
    cursor = conn.cursor()

    cursor.executescript('''DROP TABLE hubs;
                   
                      CREATE TABLE hubs (hub_id TEXT PRIMARY KEY,
                      model TEXT,
                      status TEXT,
                      worker_id INTEGER,
                      production_date DATE,
                      FOREIGN KEY (worker_id) REFERENCES workers(worker_id));
                   
                      DROP TABLE workers;
                      
                      CREATE TABLE workers (
                      worker_id INTEGER PRIMARY KEY,
                      name TEXT,
                      shift TEXT)
                    ''')
    yield cursor
    conn.rollback()
    cursor.close()