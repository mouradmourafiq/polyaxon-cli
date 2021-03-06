# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_schemas.data import DatasetConfig

from polyaxon_cli.client.base import PolyaxonClient
from polyaxon_cli.exceptions import (
    AuthenticationError,
    PolyaxonException,
    NotFoundError,
    BadRequestError,
)
from polyaxon_cli.logging import logger


class DatasetClient(PolyaxonClient):
    """Client to get datasets from the server"""
    ENDPOINT = "/datasets"

    def get_datasets(self):
        try:
            response = self.get(self._get_url())
            datasets_dict = response.json()
            return [DatasetConfig.from_dict(dataset)
                    for dataset in datasets_dict.get("datasets", [])]
        except PolyaxonException as e:
            if isinstance(e, AuthenticationError):
                # exit now since there is nothing we can do without login
                sys.exit(1)
            logger.info("Error while retrieving datasets: {}".format(e.message))
            return []

    def get_by_name(self, name):
        request_url = self._build_url(self.auth_config.username, name)
        request_url = self._get_url(request_url)
        try:
            response = self.get(request_url)
            return DatasetConfig.from_dict(response.json())
        except NotFoundError:
            return None

    def create_dataset(self, data):
        """
        Create a temporary directory for the tar file that will be removed at
        the end of the operation.
        """
        try:
            logger.info("Making create request to server...")
            post_body = data.to_dict()
            post_body["resumable"] = True
            response = self.post(self._get_url(), json=post_body)
            return response.json()
        except BadRequestError as e:
            if 'Dataset not found, ID' in e.message:
                logger.error(
                    "Data create: ERROR! "
                    "Please run 'polyaxon data init DATASET_NAME' before upload.")
            else:
                logger.error('Data create: ERROR! %s', e.message)
            return None
        except PolyaxonException as e:
            logger.error("Data create: ERROR! %s", e.message)
            return None

    def delete_dataset(self, data_id):
        request_url = self._get_url(data_id)
        try:
            # data delete is a synchronous process, it can take a long time
            self.delete(request_url, timeout=60)
            return True
        except PolyaxonException as e:
            logger.error("Data %s: ERROR! %s", data_id, e.message)
            return False
