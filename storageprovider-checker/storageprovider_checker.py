"""
Helpscript to verify if storage provider is reqdy
"""
import requests
import time


def _is_storage_provider_ready():
    try:
        response = requests.get('http://storageprovider:6544')
        if response.status_code == 200:
            return True
    except:
        print("Unable to connect to storage provider")
    return False


if __name__ == '__main__':
    max_attempts = 20
    attempts = 0
    while not _is_storage_provider_ready() or attempts > max_attempts:
        print("storage provider not ready, waiting..")
        attempts += 1
        time.sleep(10)

    if attempts > max_attempts:
        raise Exception("storage provider not ready giving up")