import sqlite3
import logging


logging.basicConfig(level=logging.INFO,\
                    format='%(asctime)s - %(levelname)s - %(message)s'\
                    )
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    file_path = 'sql/src/prod_workflow.db'
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        cursor.executescript('''
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
        ''')
        conn.commit()
        logger.info('databse succesfully created')

    except FileNotFoundError:
        logger.error(f'Could not find data file at path "{file_path}".')

    except sqlite3.Error as error:
        logger.error(f'DB error: {error}')
        
    except Exception as error:
        logger.critical(f'Unexpected error: {error}')