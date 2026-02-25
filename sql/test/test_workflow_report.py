import sqlite3
from datetime import date
import pytest
from parse_workflow import WorkflowReport


REPORT_MARKERS = {
                'full report':[
                      '---Prod report for all time---',
                      'Created Hubs: H101: Ivan, H102: Ivan, H103: Olena, H104: Alex, H105: Ivan',
                      'FAILED Hubs: H102 H105',
                      'Hub 2 Plus Total: 3'
    ],
                '2026-02-10 report':[
                      '---Prod report for 2026-02-10---',
                      'Created Hubs: H101: Ivan, H102: Ivan',
                      'FAILED Hubs: H102',
                      'Hub 2 Plus Total: 1'
    ],
                '2026-02-11 report':[
                      '---Prod report for 2026-02-11---',
                      'Created Hubs: H103: Olena, H104: Alex',
                      'Hub 2 Plus Total: 1'
    ],
                '2026-02-12 report':[
                      '---Prod report for 2026-02-12---',
                      'Created Hubs: H105: Ivan',
                      'FAILED Hubs: H105',
                      'Hub 2 Plus Total: 1'
    ]
               }

def test_init_with_date(db_connection: sqlite3.Connection):
    report_date = '2026-02-10'
    cursor = db_connection.cursor()

    report = WorkflowReport(cursor, report_date)
    
    assert report.report_date == date.fromisoformat(report_date)
    assert report.sql_parameters == (date.isoformat(report.report_date),)


def test_init_without_date(db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()

    report = WorkflowReport(cursor)
    
    assert report.report_date == ''
    assert report.sql_parameters == ()


def test_init_invalid_date(db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()

    with pytest.raises(ValueError):
        WorkflowReport(cursor, report_date='invalid input') 


def test_get_failed_hubs_without_date(db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()

    failed_hubs = WorkflowReport(cursor).get_failed_hubs()

    assert failed_hubs == ['H102', 'H105']


@pytest.mark.parametrize('report_date, expected_hubs', [
                                                        pytest.param('2026-02-10', ['H102']),
                                                        pytest.param('2026-02-12', ['H105']),
                                                        pytest.param('2026-02-11', [])
                                                        ])
def test_get_failed_hubs_with_date(db_connection: sqlite3.Connection, report_date: str, expected_hubs: list[str]):
    cursor = db_connection.cursor()

    failed_hubs = WorkflowReport(cursor, report_date).get_failed_hubs()

    assert failed_hubs == expected_hubs


def test_get_hub_2_plus_without_date(db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()

    hub_2_plus = WorkflowReport(cursor).get_hub_2_plus()

    assert hub_2_plus == 3


@pytest.mark.parametrize('report_date, expected_amount', [
                                                        pytest.param('2026-02-10', 1),
                                                        pytest.param('2026-02-12', 1),
                                                        pytest.param('2026-02-11', 1)
                                                        ])
def test_get_hub_2_plus_with_date(db_connection: sqlite3.Connection, report_date: str, expected_amount: int):
    cursor = db_connection.cursor()

    hub_2_plus = WorkflowReport(cursor, report_date).get_hub_2_plus()

    assert hub_2_plus == expected_amount
    

def test_get_hubs_made_by_workers_without_date(db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()

    hubs_by_workers = WorkflowReport(cursor).get_hubs_made_by_workers()

    assert hubs_by_workers == {'H101':'Ivan', 'H102':'Ivan', 'H103':'Olena', 'H104':'Alex', 'H105':'Ivan'}


@pytest.mark.parametrize('report_date, expected_dict', [
                                                        pytest.param('2026-02-10', {'H101': 'Ivan', 'H102': 'Ivan'}),
                                                        pytest.param('2026-02-11', {'H103': 'Olena', 'H104': 'Alex'}),
                                                        pytest.param('2026-02-12', {'H105': 'Ivan'})
                                                        ])
def test_get_hubs_made_by_workers_with_date(db_connection: sqlite3.Connection, report_date, expected_dict):
    cursor = db_connection.cursor()

    hubs_by_workers = WorkflowReport(cursor, report_date).get_hubs_made_by_workers()

    assert hubs_by_workers == expected_dict


def test_generate_report_without_date(db_connection: sqlite3.Connection):
    cursor = db_connection.cursor()

    report = WorkflowReport(cursor).generate_report()

    assert report.splitlines() == REPORT_MARKERS['full report']



@pytest.mark.parametrize('report_date, expected_report_markers', [
                                                          pytest.param('2026-02-10', REPORT_MARKERS['2026-02-10 report']),
                                                          pytest.param('2026-02-11', REPORT_MARKERS['2026-02-11 report']),  
                                                          pytest.param('2026-02-12', REPORT_MARKERS['2026-02-12 report']),            
                                                         ])
def test_generate_report_with_date(db_connection: sqlite3.Connection, report_date: str, expected_report_markers: str):
    cursor = db_connection.cursor()

    report = WorkflowReport(cursor, report_date).generate_report()

    assert len(report.splitlines()) == len(expected_report_markers)
    assert report.splitlines() == expected_report_markers


def test_empty_report_without_date(empty_db_cursor: sqlite3.Cursor):
    
    report = WorkflowReport(empty_db_cursor).generate_report()


    assert report == '---Prod report for all time---\n'


@pytest.mark.parametrize('report_date, expected_report', [
                                                         pytest.param('2026-02-10', '---Prod report for 2026-02-10---\n'),
                                                         pytest.param('2026-02-11', '---Prod report for 2026-02-11---\n'),
                                                         pytest.param('2026-02-12', '---Prod report for 2026-02-12---\n')  
                                                        ])
def test_empty_report_with_date(empty_db_cursor: sqlite3.Cursor, report_date: str, expected_report: str):
    
    report = WorkflowReport(empty_db_cursor, report_date).generate_report()

    assert report == expected_report