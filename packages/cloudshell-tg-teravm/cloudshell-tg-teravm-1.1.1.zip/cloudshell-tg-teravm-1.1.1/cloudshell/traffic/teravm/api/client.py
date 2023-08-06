import datetime
from functools import wraps
import httplib

import requests


BASIC_AUTH_TOKEN = "Basic dGVyYXZtOnRlcmF2bQ=="


def auth_required(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        """

        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        if self._token_expires_at is None:
            self._obtain_access_token()

        if self._token_expires_at < datetime.datetime.now() + datetime.timedelta(minutes=30):
            self._refresh_access_token()

        return func(self, *args, **kwargs)

        # try:
        #     return func(self, *args, **kwargs)
        # except Exception as e:  # todo: catch token expired exception
        #     self._obtain_access_token()
        #     return func(self, *args, **kwargs)

    return wrapped


class TeraVMClient(object):
    def __init__(self, address, user, password, scheme="https", port=443, verify_ssl=False):
        """

        :param str address: controller IP address
        :param str user: controller username
        :param str password: controller password
        :param str scheme: protocol (http|https)
        :param int port: controller port
        :param bool verify_ssl: whether SSL cert will be verified or not
        """
        self._base_url = "{}://{}:{}".format(scheme, address, port)
        self._user = user
        self._password = password
        self._headers = {
            "Accept": "application/vnd.cobham.v1+json"
        }
        self._verify_ssl = verify_ssl
        self._refresh_token = None
        self._access_token = None
        self._token_expires_at = None

    @property
    def _auth_headers(self):
        return {
            "Authorization": "Bearer {}".format(self._access_token)
        }

    def _obtain_access_token(self):
        """

        :return:
        """
        data = {
            "grant_type": "password",
            "username": self._user,
            "password": self._password
        }

        resp = self._do_post(path="authservice/oauth/token",
                             headers={"Authorization": BASIC_AUTH_TOKEN,
                                      "Content-Type": "application/x-www-form-urlencoded"},
                             data=data)

        resp_data = resp.json()
        self._token_expires_at = datetime.datetime.now() + datetime.timedelta(seconds=resp_data["expires_in"])
        self._access_token = resp_data["access_token"]
        self._refresh_token = resp_data["refresh_token"]

    def _refresh_access_token(self):
        """
        :return:
        """
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
        }

        resp = self._do_post(path="authservice/oauth/token",
                             headers={"Authorization": BASIC_AUTH_TOKEN,
                                      "Content-Type": "application/x-www-form-urlencoded"},
                             data=data)

        resp_data = resp.json()
        self._token_expires_at = datetime.datetime.now() + datetime.timedelta(seconds=resp_data["expires_in"])
        self._access_token = resp_data["access_token"]
        self._refresh_token = resp_data["refresh_token"]

    def _do_get(self, path, raise_for_status=True, **kwargs):
        """Basic GET request client method

        :param str path: path for the request
        :param dict kwargs: additional kwarg that would be passed to the requests lib
        :rtype: requests.Response
        """
        url = "{}/{}".format(self._base_url, path)
        kwargs.update({"verify": self._verify_ssl})
        kwargs.setdefault("headers", {}).update(self._headers)
        resp = requests.get(url=url, **kwargs)
        raise_for_status and resp.raise_for_status()
        return resp

    def _do_post(self, path, raise_for_status=True, **kwargs):
        """Basic POST request client method

        :param str path: path for the request
        :param dict kwargs: additional kwarg that would be passed to the requests lib
        :rtype: requests.Response
        """
        url = "{}/{}".format(self._base_url, path)
        kwargs.update({"verify": self._verify_ssl})
        kwargs.setdefault("headers", {}).update(self._headers)
        resp = requests.post(url=url, **kwargs)
        raise_for_status and resp.raise_for_status()
        return resp

    def _do_put(self, path, raise_for_status=True, **kwargs):
        """Basic PUT request client method

        :param str path: path for the request
        :param dict kwargs: additional kwarg that would be passed to the requests lib
        :rtype: requests.Response
        """
        url = "{}/{}".format(self._base_url, path)
        kwargs.update({"verify": self._verify_ssl})
        kwargs.setdefault("headers", {}).update(self._headers)
        resp = requests.put(url=url, **kwargs)
        raise_for_status and resp.raise_for_status()
        return resp

    def _do_delete(self, path, raise_for_status=True, **kwargs):
        """Basic DELETE request client method

        :param str path: path for the request
        :param dict kwargs: additional kwarg that would be passed to the requests lib
        :rtype: requests.Response
        """
        url = "{}/{}".format(self._base_url, path)
        kwargs.update({"verify": self._verify_ssl})
        kwargs.setdefault("headers", {}).update(self._headers)
        resp = requests.delete(url=url, **kwargs)
        raise_for_status and resp.raise_for_status()
        return resp

    @auth_required
    def get_modules_info(self):
        """Get test modules and ports information

        :return:
        """
        response = self._do_get(path="v1/poolmanager/testModules", headers=self._auth_headers)
        if response.status_code == httplib.NO_CONTENT:
            return []

        data = response.json()
        return data["testModules"]

    def check_if_service_is_deployed(self, logger):
        """

        :return:
        """
        try:
            resp = self._do_get(path="v1/legacy-ui/application/details", raise_for_status=False)
        except requests.exceptions.ConnectionError:
            logger.info("API Service did not started yet", exc_info=True)
            return False

        return resp.status_code == httplib.OK

    @auth_required
    def configure_executive_server(self, ip_addr):
        """"""
        data = {
            "executiveMachineIP": ip_addr
        }

        resp = self._do_post(path="v1/legacy-ui/application/settings/executive-ip", data=data)
        return resp


if __name__ == "__main__":
    cl = TeraVMClient(address="192.168.42.217", user="nomatter", password="nomatter")
    cl.get_modules_info()
