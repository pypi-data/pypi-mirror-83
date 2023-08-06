from pyarrow.flight import (
    ClientAuthHandler,
    FlightClient,
    FlightDescriptor,
    FlightInfo,
    Ticket,
)

from tktl.core.clients import Client
from tktl.core.serializers import deserialize_arrow, serialize_arrow


class ApiKeyClientAuthHandler(ClientAuthHandler):
    """An example implementation of authentication via ApiKey."""

    def __init__(self, api_key: str):
        super(ApiKeyClientAuthHandler, self).__init__()
        self.api_key = api_key

    def authenticate(self, outgoing, incoming):
        outgoing.write(self.api_key)
        self.api_key = incoming.read()

    def get_token(self):
        return self.api_key


class ArrowFlightClient(Client):
    def list_endpoints(self):
        pass

    def list_deployments(self):
        pass

    def get_sample_data(self):
        pass

    framework = "Arrow Flight RPC"
    scheme = "grpc+tcp"

    def __init__(self, host, port, api_key: str):
        super().__init__(api_key)
        self.location = f"{self.scheme}://{host}:{port}"
        self.client = FlightClient(self.location)

    def list_commands(self):
        return self.client.list_actions()

    def predict(self, inputs, endpoint_name: str):
        table = serialize_arrow(inputs)
        descriptor = self.get_flight_info(command_name=str.encode(endpoint_name))
        writer, reader = self.client.do_exchange(descriptor)
        with writer:
            writer.begin(table.schema)
            writer.write_table(table)
            writer.done_writing()
            table = reader.read_all()
        return deserialize_arrow(table)

    def sample_data(self, command_name: str):
        x_info = self.client.do_get(Ticket(ticket=str.encode(f"{command_name}__X")))
        y_info = self.client.do_get(Ticket(ticket=str.encode(f"{command_name}__y")))
        return (
            deserialize_arrow(x_info.read_all()),
            deserialize_arrow(y_info.read_all()),
        )

    def get_schema(self, command_name: str):
        info = self.get_flight_info(str.encode(command_name))
        return info.schema

    def get_flight_info(self, command_name: bytes) -> FlightInfo:
        descriptor = FlightDescriptor.for_command(command_name)
        return self.client.get_flight_info(descriptor)
