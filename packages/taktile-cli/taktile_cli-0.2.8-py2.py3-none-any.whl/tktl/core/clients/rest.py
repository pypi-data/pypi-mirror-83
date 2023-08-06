import json
import os

from openapi_schema_pydantic import OpenAPI

from tktl.core.clients import Client
from tktl.core.clients.http_client import API
from tktl.core.schemas.repository import _format_http_url
from tktl.core.t import ServiceT


class RestClient(Client):
    def get_schema(self, *args, **kwargs):
        pass

    TRANSPORT = ServiceT.REST

    def __init__(self, api_key: str, repository_name: str, local: bool = False):
        super().__init__(api_key=api_key, repository_name=repository_name)
        self._location = None
        self._endpoint = None
        self._client = None
        self.local = local

    def predict(self, inputs):
        response = self.client.post(
            url=f"model/{self.endpoint}", data=json.dumps(inputs)
        )
        return response.json()

    def list_endpoints(self):
        return {
            e["endpoint"].name: _format_http_url(e["deployment"].public_docs_url)
            for e in self.taktile_client.get_endpoints_for_repository(
                repository=self.repository_name
            )
        }

    def __set_endpoint_and_location(self, endpoint_name: str):
        self.endpoint = endpoint_name
        if self.local:
            self.location = self.local_endpoint
        else:
            self.location = self.list_endpoints()[endpoint_name]

    def authenticate(self, endpoint_name: str):
        self.__set_endpoint_and_location(endpoint_name)
        client = API(api_url=self.location)
        self.client = client

    @property
    def client(self) -> API:
        return self._client

    @client.setter
    def client(self, client: API):
        self._client = client

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
    def local_endpoint(self):
        return "http://0.0.0.0:8080"

    def list_deployments(self):
        pass

    def get_sample_data(self):
        schema = self.client.get(url="openapi.json")
        openapi = OpenAPI.parse_obj(schema.json())
        request_reference, response_reference = get_endpoint_model_reference(
            openapi, endpoint=self.endpoint
        )
        sample_input = openapi.components.schemas[request_reference].example
        if not sample_input:
            self.logger.warning("No sample input found for endpoint")
        sample_output = openapi.components.schemas[response_reference].example
        if not sample_output:
            self.logger.warning("No sample output found for endpoint")
        return sample_input, sample_output


def get_endpoint_model_reference(openapi: OpenAPI, endpoint: str):
    for k in openapi.paths.keys():
        if f"/model/{endpoint}" == k:
            request_ref = (
                openapi.paths[k]
                .post.requestBody.content["application/json"]
                .media_type_schema.ref
            )
            response_ref = (
                openapi.paths[k]
                .post.responses["200"]
                .content["application/json"]
                .media_type_schema.ref
            )
            return os.path.basename(request_ref), os.path.basename(response_ref)
    return None
