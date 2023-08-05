""" Util to handle network requests """
import requests

from buildkite_log_parse import util

API_ROOT = "https://api.buildkite.com/v2"


def builds(build_state, organization, pipeline, token, debug=False):
    """ Fetch builds from buildkite api """
    builds_url = f"{API_ROOT}/organizations/{organization}/pipelines/{pipeline}/builds"
    params = {"state": build_state}
    builds_response = requests.get(
        builds_url, params=params, headers=build_headers(token)
    )
    if debug:
        util.write_log(builds_response.text, "json", "builds")
    return builds_response.json()


def build_job_log(build, job, organization, pipeline, token, debug=False):
    """ Fetch log for the build's job from buildkite api """
    builds_url = f"{API_ROOT}/organizations/{organization}/pipelines/{pipeline}/builds"
    log_url = f"{builds_url}/{build['number']}/jobs/{job['id']}/log.txt"
    log_response = requests.get(log_url, headers=build_headers(token)).text
    if debug:
        util.write_log(log_response, "txt", "raw_log")
    return log_response


def build_headers(token):
    """ Build auth headers for network requests """
    return {"Authorization": f"Bearer {token}"}
