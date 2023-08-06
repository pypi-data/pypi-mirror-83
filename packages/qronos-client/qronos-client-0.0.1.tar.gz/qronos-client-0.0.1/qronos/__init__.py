__version__ = "0.0.1"

import logging

import dateutil.parser
import requests

logger = logging.getLogger(__name__)


class QRonosError(Exception):
    """Generic exception for QRonos"""
    def __init__(self, msg):
        super().__init__()
        logger.error(f"[QRONOS API] - {msg}")


class QRonosClient(object):
    urls = {}
    headers = {}

    def __init__(self, host, token=None):
        self._set_urls(host)
        if token:
            self._set_headers(token)

    def _set_headers(self, token):
        self.headers = {"Authorization": f"Token {token}"}

    def _set_urls(self, host):
        prefix = f"https://{host}/api"  # TODO: Maybe use urllib.parse.urlparse to be more forgiving with host formats?
        self.urls = {
            'login': f"{prefix}/login/",
            'logout': f"{prefix}/logout/",
            'logoutall': f"{prefix}/logoutall/",
            'import_status': f"{prefix}/import_status/",
            'tracker_import': f"{prefix}/tracker_import/",
            'stage_import': f"{prefix}/stage_import/",
        }

    def _get(self, *args, **kwargs):
        if self.headers:
            kwargs.setdefault("headers", {}).update(self.headers)
        try:
            return requests.get(*args, **kwargs)
        except requests.exceptions.RequestException as err:
            raise QRonosError("Unable to connect") from err

    def _post(self, *args, **kwargs):
        if self.headers:
            kwargs.setdefault("headers", {}).update(self.headers)
        try:
            return requests.post(*args, **kwargs)
        except requests.exceptions.RequestException as err:
            raise QRonosError("Unable to connect") from err

    def login(self, username, password):
        """Login and fetch token"""
        response = self._post(self.urls['login'], data={'username': username, 'password': password})
        if not response.status_code == 200:
            raise QRonosError("Invalid credentials")
        try:
            response_json = response.json()
            token, expiry = response_json["token"], dateutil.parser.parse(response_json["expiry"])
        except Exception as err:
            raise QRonosError("Unable to get token") from err
        self._set_headers(token)
        return token, expiry

    def logout(self, all_tokens=False):
        """Logout (optionally to remove all tokens)"""
        logout_url = self.urls['logoutall'] if all_tokens else self.urls['logout']
        response = self._post(logout_url)
        if response.status_code == 204:
            return True
        raise QRonosError("Unable to logout")

    def import_status(self, job_id):
        """Get the status of an import"""
        response = self._get(self.urls['import_status'], params={'job_id': job_id})
        if response.status_code == 200:
            try:
                return response.json()["status"]
            except Exception as err:
                raise QRonosError("Unable to get status") from err
        elif response.status_code == 404:
            raise QRonosError(response.json()["job_id"])
        else:
            raise QRonosError(f"Bad Request - {response.json()}")

    def _run_import(self, url, post_data):
        """Helper function to post import and handle response"""
        response = self._post(url, json=post_data)
        if response.status_code == 202:
            try:
                return response.json()["job_id"]
            except Exception as err:
                raise QRonosError("Unable to get Job ID from Import request") from err
        raise QRonosError(f"Bad Import request - {response.content}")

    def tracker_import(self, tracker_id, tracker_importer_id, unique_columns, data):
        """
        Imports tracker (item) data.
        Please ensure you know the settings of the tracker importer in QRonos before sending any data.

        :param tracker_id: The ID of the Tracker
        :param tracker_importer_id: The ID of the Tracker Importer
        :param unique_columns: A list of the header fields
        :param data: The import data as a list of dictionaries (keys must match the headers from unique_columns parameter)
        :return: Job ID
        """
        return self._run_import(
            self.urls['tracker_import'],
            {
                'tracker': tracker_id,
                'tracker_importer': tracker_importer_id,
                'unique_columns': unique_columns,
                'data': data
            }
        )

    def stage_import(self, stage_id, stage_importer_id, data):
        """
        Imports stage data.
        Please ensure you know the settings of the stage importer in QRonos before sending any data.

        :param stage_id: The ID of the Stage
        :param stage_importer_id: The ID of the Stage Importer
        :param data: The import data as a list of dictionaries (keys must match headers set up in QRonos)
        :return: Job ID
        """
        return self._run_import(
            self.urls['stage_import'],
            {
                'stage': stage_id,
                'stage_importer': stage_importer_id,
                'data': data
            }
        )
