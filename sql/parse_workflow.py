import sqlite3
import logging
from datetime import date


logging.basicConfig(level=logging.INFO,\
                    format='%(asctime)s - %(levelname)s - %(message)s'\
                    )
logger = logging.getLogger(__name__)

class WorkflowReport:
    def __init__(self, cursor: sqlite3.Cursor, report_date: str = ''):
        self._cursor = cursor
        if report_date:
            self._report_date = date.fromisoformat(report_date)
            self._sql_parameters = (self._report_date.isoformat(),)
        else:
            self._report_date = ''
            self._sql_parameters = ()
    
    @property
    def report_date(self):
        return self._report_date
    
    @property
    def sql_parameters(self):
        return self._sql_parameters

    def get_failed_hubs(self) -> list[str]:
        instruction = """SELECT hub_id, status FROM hubs WHERE status = 'Failed'"""

        if self._report_date:
            instruction += ' AND production_date = (?)'

        self._cursor.execute(instruction, self._sql_parameters)
        failed_hubs = []
        for hub in self._cursor.fetchall():
            failed_hubs.append(f'{hub['hub_id']}')

        return failed_hubs
    
    def get_hub_2_plus(self)-> int:
        instruction = """SELECT COUNT(*) FROM hubs WHERE model = 'Hub 2 Plus'"""

        if self._report_date:
            instruction += ' AND production_date = (?)'

        self._cursor.execute(instruction, self._sql_parameters)
        return self._cursor.fetchone()[0]
    
    def get_hubs_made_by_workers(self) -> dict[str, str]:
        instruction = """SELECT hubs.hub_id, workers.name \
                       FROM hubs \
                       JOIN workers \
                       ON hubs.worker_id = workers.worker_id"""
        
        if self._report_date:
            instruction += ' WHERE hubs.production_date = (?)'
        
        self._cursor.execute(instruction, self._sql_parameters)
        hubs_by_workers = dict(self._cursor.fetchall())

        return hubs_by_workers
    
    def generate_report(self) -> str:
        if self._report_date:
            report_header = f'---Prod report for {self._report_date}---'
        else:
            report_header = '---Prod report for all time---'
        
        report = f'{report_header}\n'

        if self.get_hubs_made_by_workers():
            report += 'Created Hubs: ' + ', '.join(f'{hub}: {worker}' for hub, worker in self.get_hubs_made_by_workers().items()) + '\n'

        if self.get_failed_hubs():
            report += 'FAILED Hubs: ' + ' '.join(self.get_failed_hubs()) + '\n'
        
        if self.get_hub_2_plus():
            report += f'Hub 2 Plus Total: {self.get_hub_2_plus()}'

        return report

if __name__ == '__main__':   
    file_path = 'sql/src/workflow.db'
    report_date = '2026-02-12'
    try:
        conn = sqlite3.connect(file_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        report = WorkflowReport(cursor, report_date)
        logger.info('Generating report from prod')
        print(report.generate_report())

    except FileNotFoundError:
        logger.error(f'Could not find data file at path "{file_path}".')

    except sqlite3.Error as error:
        logger.error(f'DB error: {error}')

    except Exception as error:
        logger.critical(f'Unexpected error: {error}')