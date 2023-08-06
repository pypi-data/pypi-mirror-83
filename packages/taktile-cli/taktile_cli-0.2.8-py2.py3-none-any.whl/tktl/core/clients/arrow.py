from pyarrow.flight import (
    ClientAuthHandler,
    FlightClient,
    FlightDescriptor,
    FlightInfo,
    Ticket,
)

from tktl.core.clients import Client
from tktl.core.exceptions import AuthenticationError
from tktl.core.schemas.repository import _format_grpc_url
from tktl.core.serializers import deserialize_arrow, serialize_arrow
from tktl.core.t import ServiceT


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

    TRANSPORT = ServiceT.GRPC

    def __init__(self, api_key: str, repository_name: str, local: bool = False):
        super().__init__(api_key=api_key, repository_name=repository_name)
        self._location = None
        self._endpoint = None
        self._client = None
        self.local = local

    def list_endpoints(self):
        return {
            e["endpoint"].name: _format_grpc_url(e["deployment"].public_docs_url)
            for e in self.taktile_client.get_endpoints_for_repository(
                repository=self.repository_name
            )
        }

    @property
    def local_endpoint(self):
        return "grpc+tcp://0.0.0.0:5005"

    def list_deployments(self):
        pass

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client: FlightClient):
        self._client = client

    def list_commands(self):
        return self.client.list_actions()

    def __set_endpoint_and_location(self, endpoint_name: str):
        self.endpoint = endpoint_name
        if self.local:
            self.location = self.local_endpoint
        else:
            self.location = self.list_endpoints()[endpoint_name]

    def authenticate(self, endpoint_name: str):
        self.__set_endpoint_and_location(endpoint_name)
        client = FlightClient(location=self.location)
        client.authenticate(
            ApiKeyClientAuthHandler(api_key=self.taktile_client.api_key)
        )
        self.client = client

    def predict(self, inputs):
        table = serialize_arrow(inputs)
        descriptor = self.get_flight_info(command_name=str.encode(self.endpoint))
        writer, reader = self.client.do_exchange(descriptor.descriptor)
        with writer:
            writer.begin(table.schema)
            writer.write_table(table)
            writer.done_writing()
            table = reader.read_all()
            return deserialize_arrow(table)

    def get_sample_data(self):
        if not self.endpoint:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        x_info = self.client.do_get(Ticket(ticket=str.encode(f"{self.endpoint}__X")))
        y_info = self.client.do_get(Ticket(ticket=str.encode(f"{self.endpoint}__y")))
        return (
            deserialize_arrow(x_info.read_all()),
            deserialize_arrow(y_info.read_all()),
        )

    def get_schema(self):
        if not self.endpoint:
            raise AuthenticationError(
                "Please authenticate against a specific endpoint first"
            )
        info = self.get_flight_info(str.encode(self.endpoint))
        return info.schema

    def get_flight_info(self, command_name: bytes) -> FlightInfo:
        descriptor = FlightDescriptor.for_command(command_name)
        return self.client.get_flight_info(descriptor)
