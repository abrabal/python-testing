import pytest
import grpc
from mock_client import MockServerClient


@pytest.fixture(scope='function', params=["localhost:50051"])
def grpc_channel(request):
    with grpc.insecure_channel(request.param) as channel:
        yield channel

@pytest.fixture(scope='function', params=["localhost:error"])
def grpc_bad_channel(request):
    with grpc.insecure_channel(request.param) as channel:
        yield channel

@pytest.fixture(scope='function', params=[5.0])
def grpc_client(request, grpc_channel):
    return MockServerClient(channel=grpc_channel, timeout=request.param)

@pytest.fixture(scope='function', params=[-5.0])
def grpc_bad_timeout_client(request, grpc_channel):
    return MockServerClient(channel=grpc_channel, timeout=request.param)

@pytest.fixture(scope='function', params=[5.0])
def grpc_bad_connection_client(request, grpc_bad_channel):
    return MockServerClient(channel=grpc_bad_channel, timeout=request.param)