import pytest
import grpc
from mock_client import MockServerClient

@pytest.mark.parametrize("signals, expected_signals", [
                                                       pytest.param(["online", "alarm", "online", "alarm", "alarm"], {"online":2, "alarm":3}),
                                                       pytest.param(["online", "online"], {"online":2}),
                                                       pytest.param(["alarm","alarm", "alarm"], {"alarm":3})
                                                       ])
def test_mock_count_signals(grpc_client: MockServerClient, signals: list, expected_signals: dict):

    assert grpc_client.count_signals(signals).count == expected_signals


@pytest.mark.parametrize("temperature, expected_status", [
                                                          pytest.param(50, 'Calm'),
                                                          pytest.param(60, 'Calm'),
                                                          pytest.param(70, 'Alarm!')
                                                          ])
def test_mock_fire_alarm(grpc_client: MockServerClient, temperature: int, expected_status: str):
    
    assert grpc_client.fire_alarm_check(temperature).status == expected_status


def test_connection_errors(grpc_bad_connection_client: MockServerClient):
    with pytest.raises(grpc.RpcError) as grpc_error:
        grpc_bad_connection_client.fire_alarm_check(25)

    assert grpc_error.value.code() == grpc.StatusCode.UNAVAILABLE


def test_timeout_errors(grpc_bad_timeout_client: MockServerClient):
    with pytest.raises(grpc.RpcError) as grpc_error:
        grpc_bad_timeout_client.fire_alarm_check(25)
        
    assert grpc_error.value.code() == grpc.StatusCode.DEADLINE_EXCEEDED