from concurrent import futures
import logging
import grpc
import src.mock_server_pb2 as mock_server_pb2
import src.mock_server_pb2_grpc as mock_server_pb2_grpc


class CountSignals(mock_server_pb2_grpc.CountSignalsServicer):
    def Count(self, request, context):
        if context.time_remaining() < 0:
            context.abort(
                grpc.StatusCode.DEADLINE_EXCEEDED
            )

        dict_for_signals = {}
        for signal in request.signals:
            dict_for_signals[signal] = dict_for_signals.get(signal, 0) + 1
        return mock_server_pb2.DictOfSignals(count=dict_for_signals)
    
class FireAlarm(mock_server_pb2_grpc.FireAlarmServicer):
    def CheckTemperature(self, request, context):
        if context.time_remaining() < 0:
            context.abort(
                grpc.StatusCode.DEADLINE_EXCEEDED
            )

        if request.temperature > 60:
            return mock_server_pb2.StatusResponse(status='Alarm!')
        else:
            return mock_server_pb2.StatusResponse(status='Calm')

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mock_server_pb2_grpc.add_CountSignalsServicer_to_server(CountSignals(), server)
    mock_server_pb2_grpc.add_FireAlarmServicer_to_server(FireAlarm(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()