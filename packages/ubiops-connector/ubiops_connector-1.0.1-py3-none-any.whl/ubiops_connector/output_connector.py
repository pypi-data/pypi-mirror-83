import json
import logging
import os

from .exceptions import ConnectorError


logger = logging.getLogger('Connector')


class OutputConnector:

    def __init__(self, base_directory, context):
        """
        Initialisation method for the connector

        :param str base_directory: absolute path to the directory where the model file is located
        :param dict context: a dictionary containing details of the model deployment that might be useful in your code
        """

        self.base_directory = base_directory
        self.context = context

    def request(self, data):
        """
        Method for requests, called separately for each individual request. Map the input fields, if necessary, and
        insert the given input data into the database.

        :param dict data: input data for the connector
        """

        data = self.map_data(data)
        self.insert(data=data)

    def insert(self, data):
        """
        Insert given data into the database. This method must be implemented in each connector class.

        :param dict data: input data for the connector
        """

        raise NotImplementedError

    @staticmethod
    def map_data(data):
        """
        Map data, in case the fields in the connector are different from its input fields. The environment variable
        `MAPPING` is used to specify the input fields to actual columns in the database.

        Mapping only works for structured connectors.

        :param dict data: input data
        :return dict: mapped data
        """

        # Map data
        mapping = os.environ.get('MAPPING', None)

        if mapping:
            mapping = json.loads(mapping)

            for old_field in data.keys():
                if old_field in mapping:
                    data[mapping[old_field]] = data.pop(old_field)

        return data

    @staticmethod
    def get_variable(variable_name, default_value=None):
        """
        Get the environment variable with the given name. If the variable is not set and a default value is passed, use
        this value.

        :param str variable_name: the name of the variable
        :param str default_value: the default value of the variable in case it is not set
        :return: the value for the given environment variable
        """

        if variable_name in os.environ:
            return os.environ[variable_name]
        elif default_value:
            return default_value

        raise ConnectorError(f"Environment variable {variable_name} is not set")

    def stop(self):
        """
        Stop the connector by closing the connection to the data source
        """

        pass
