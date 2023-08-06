import requests
import logging

__version__ = "0.1"


def make_url(path, sandbox=True):
    if sandbox:
        BASE = "https://sandbox.liblynx.com"
    else:
        BASE = "https://connect.liblynx.com"
    return "%s%s" % (BASE, path)


def access_token(client_id, client_secret):
    r = requests.post(make_url("/oauth/v2/token"),
                      {"grant_type": "client_credentials"}, auth=(client_id, client_secret))
    if r.status_code == 200:
        r_json = r.json()
        logging.debug("access_token acquired for %s", client_id)
        return r_json.get("access_token")
    logging.error("access_token failed %s %s", r.status_code, r.text)


def endpoint(access_token):
    headers = {"Authorization": "Bearer %s" %
               access_token, "Accept": "application/json"}
    r = requests.get(make_url("/api"), headers=headers)
    if r.status_code == 200:
        api = r.json()
        logging.debug("api endpoint acquired %s", api)
        return api
    logging.error("api endpoint failed %s %s", r.status_code, r.text)


def new_identification(access_token, api, ip, url, user_agent):
    headers = {"Authorization": "Bearer %s" % access_token,
               "Accept": "application/json", "Content-Type": "application/json"}
    data = {"ip": ip, "url": url, "user_agent": user_agent}
    r = requests.post(api["_links"]["@new_identification"]
                      ["href"], json=data, headers=headers)
    if r.status_code == 201:
        new_id = r.json()
        logging.debug("new_identification %s", new_id["id"])
        return new_id
    logging.error("new identification failed %s %s", r.status_code, r.text)
