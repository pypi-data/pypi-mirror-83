from __future__ import absolute_import
from typing import List
from aoa.api.base_api import BaseApi

import requests
import uuid
import os


class TrainedModelArtefactsApi(BaseApi):

    def list_artefacts(self, trained_model_id: uuid):
        """
        returns all trained models

        Parameters:
           trained_model_id (uuid): Trained Model Id

        Returns:
            (list): all trained model artefacts
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept(['application/json'])]
        header_params = self.generate_params(header_vars, header_vals)

        return self.aoa_client.get_request(
            "/api/trainedModels/{}/artefacts/listObjects".format(trained_model_id),
            header_params,
            query_params=None)["objects"]

    def get_signed_download_url(self, trained_model_id: uuid, artefact: str):
        """
        returns a signed url for the artefact

        Parameters:
           trained_model_id (uuid): Trained Model Id
           artefact (str): The artefact to generate the signed url for

        Returns:
            (str): the signed url
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept(['application/json'])]
        header_params = self.generate_params(header_vars, header_vals)
        query_params = self.generate_params(['objectKey'], [artefact])

        response = self.aoa_client.get_request(
            "/api/trainedModels/{}/artefacts/signedDownloadUrl".format(trained_model_id),
            header_params,
            query_params)

        return response["endpoint"]

    def get_signed_upload_url(self, trained_model_id: uuid, artefact: str):
        """
        returns a signed url for the artefact

        Parameters:
           trained_model_id (uuid): Trained Model Id
           artefact (str): The artefact to generate the signed url for

        Returns:
            (str): the signed url
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept(['application/json'])]
        header_params = self.generate_params(header_vars, header_vals)
        query_params = self.generate_params(['objectKey'], [artefact])

        response = self.aoa_client.get_request(
            "/api/trainedModels/{}/artefacts/signedUploadUrl".format(trained_model_id),
            header_params,
            query_params)

        return response["url"]

    def download_artefacts(self, trained_model_id: uuid, path: str = "."):
        """
        downloads all artefacts for the given trained model

        Parameters:
           trained_model_id (uuid): Trained Model Id
           path (str): the path to download the artefacts to (default cwd)

        Returns:
            None
        """

        for artefact in self.list_artefacts(trained_model_id):
            response = requests.get(self.get_signed_download_url(trained_model_id, artefact), auth=self.aoa_client.auth)

            with open("{}/{}".format(path, artefact), "wb") as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    f.write(chunk)

    def upload_artefacts(self, trained_model_id: uuid, artefacts: List):
        """
        uploads artefacts for the given trained model

        Parameters:
           trained_model_id (uuid): Trained Model Id
           artefacts (List): The artefact paths to upload

        Returns:
            None
        """

        for artefact in artefacts:
            query_params = {
                'objectKey': "{}".format(os.path.basename(artefact))
            }
            header_params = {
                'AOA-Project-ID': "{}".format(self.aoa_client.project_id)
            }
            signed_url = self.aoa_client.get_request("/api/trainedModels/{}/artefacts/signedUploadUrl"
                                                     .format(trained_model_id), header_params, query_params)

            upload_resp = requests.put(signed_url['endpoint'], data=open(artefact, 'rb'))
            upload_resp.raise_for_status()
