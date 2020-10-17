import json
import getpass
from pathlib import Path
from pprint import pprint

from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError


cache_file = Path("test_token.cache")


def token_updated(token):
    cache_file.write_text(json.dumps(token))


def otp_callback():
    auth_code = input("2FA code: ")
    return auth_code


def expires_at_to_datetime(expires_at=1602956389.7934):
    from datetime import datetime
    ts = int(expires_at)
    print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))


def main():
    if cache_file.is_file():
        auth = Auth("Ringer/1.0", json.loads(cache_file.read_text()), token_updated)
    else:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        auth = Auth("Ringer/1.0", None, token_updated)
        try:
            auth.fetch_token(username, password)
        except MissingTokenError:
            auth.fetch_token(username, password, otp_callback())

    ring = Ring(auth)
    ring.update_data()

    devices = ring.devices()
    pprint(devices)

    doorbell = devices['doorbots'][0]
    id = doorbell.history(limit=100, kind='motion')[0]['id']
    print(f"doorbell id = {id}")
    # doorbell.history(limit=100, kind='motion')[0]['id'],
    doorbell.recording_download(
        id,
        filename=f'doorbell_motion_{id}.mp4',
        override=True)

    cams = devices['stickup_cams']
    for i, cam in enumerate(cams):
        id = cam.history(limit=100, kind='motion')[i]['id']
        print(f"cam[{i}] id = {id}")
        # cam.history(limit=100, kind='motion')[i]['id'],
        cam.recording_download(
            id,
            filename=f'cam_motion_{id}.mp4',
            override=True)


if __name__ == "__main__":
    main()