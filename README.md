## Project: gRPC & SQL Practice

This project contains tests and practice implementations for gRPC and SQL in Python.

### gRPC

A simple local gRPC server with two methods:

#### 1.count_signals

 - Accepts a list of signals.

- Returns a dictionary with the count of each signal type.

#### 2.fire_alarm

- Accepts a temperature value.

- Returns:

- "Alarm!" if temperature > 60

- "Calm" if temperature ≤ 60

### How to run

#### 1. Start the gRPC server:

`python3 grpc/mock_server.py`

2.Run tests with 

`pytest grpc/test_mock_client.py`

### SQL

A workflow report generator using SQLite:

- Generates reports showing:

- Total number of created hubs

- Failed hubs

- Which worker created each hub

**Can filter reports by a specific date or generate for all time.**

#### How to run

Run tests with pytest:

`pytest sql/test/test_workflow_report.py`

**The database is tested in memory, so no persistent setup is required.**

### Notes

**All tests use pytest fixtures to create isolated environments.**

**The project is structured for practice purposes, demonstrating gRPC server-client interactions and SQL report generation.**