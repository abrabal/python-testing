import logging
import grpc
import src.mock_server_pb2 as count_signals_pb2
import src.mock_server_pb2_grpc as count_signals_pb2_grpc


class MockServerClient():
    def __init__(self, timeout :int, channel :object):
        self.count_stub = count_signals_pb2_grpc.CountSignalsStub(channel)
        self.fire_alarm_stub = count_signals_pb2_grpc.FireAlarmStub(channel)
        self.timeout = timeout
    
    def count_signals(self, signals :list) -> object:
        return self.count_stub.Count(count_signals_pb2.ListOfSignals(signals=signals), timeout=self.timeout)
    
    def fire_alarm_check(self, temperature :int) -> object:
        return self.fire_alarm_stub.CheckTemperature(count_signals_pb2.TemperatureRequest(temperature=temperature), timeout=self.timeout)
    

def run_mock_server(signals :list, temperature :int):
    with grpc.insecure_channel("localhost:50051") as channel:
        client = MockServerClient(timeout=5.0, channel=channel)
        print(client.count_signals(signals).count)
        print(client.fire_alarm_check(temperature).status)

if __name__ == "__main__":
    logging.basicConfig()
    run_mock_server(signals=["online", "alarm", "online", "alarm", "alarm"], temperature=70)