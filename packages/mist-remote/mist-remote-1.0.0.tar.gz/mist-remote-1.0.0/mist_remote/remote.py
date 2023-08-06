import json
import time
import os.path as op
import urllib.request

class MissingParameter(Exception):
    pass

def msg(message: str, quiet: bool, new_line: bool = True):
    if not quiet:
        print(
            f" -> {message}",
            end='\n' if new_line else '',
            flush=True
        )

def run_in_mist_server(server: str,
                       playbook: str,
                       quiet: bool = True,
                       parameters: dict = None) -> str or MissingParameter:
    """
    This function runs a playbook in a remote MIST server
    """
    if not server.startswith("http"):
        raise ValueError("'server' must starts with 'http://' or 'https://'")
    if server.endswith("/"):
        server = server[:-1]


    if op.exists(playbook):
        msg("Reading playbook from local disk", quiet)

        with open(playbook, "r") as f:
            content = f.read()
    elif playbook.startswith("http"):
        msg("Downloading playbook", quiet)

        content = urllib.request.urlopen(playbook).read()

        try:
            content = content.decode()
        except AttributeError:
            pass
    else:
        content = playbook

    if parameters:
        if type(parameters) is not dict:
            raise ValueError("Parameters must be a dict")

    msg("Creating job at MIST server", quiet)

    req = urllib.request.Request(f"{server}/run")
    req.add_header('Content-Type', 'application/json')

    response = urllib.request.urlopen(
        req,
        data=json.dumps({
            "content": content,
            "parameters": parameters
        }).encode()
    )

    try:
        jobId = json.loads(response.read().decode())["jobId"]

        msg(f"Got JobId: {jobId}", quiet)

    except Exception as e:
        raise Exception from e

    #
    # Wait for ending
    #
    msg(f"Waiting that job finishes", quiet, new_line=False)
    while 1:

        response = urllib.request.urlopen(
            f"{server}/run/{jobId}/status"
        )
        status = json.loads(response.read().decode())["status"]

        if status == "finished":
            break
        else:
            if not quiet:
                print(".", end='', flush=True)
            time.sleep(1)

    if not quiet:
        print("Ok!", flush=True)

    #
    # Download report
    #
    msg("Recovering results", quiet)

    response = urllib.request.urlopen(
        f"{server}/run/{jobId}"
    )

    response_data = json.loads(
        response.read().decode()
    ).get("message", "")

    if "error" in response_data:
        raise MissingParameter(response_data["error"])

    return response_data

__all__ = ("run_in_mist_server", "MissingParameter")
