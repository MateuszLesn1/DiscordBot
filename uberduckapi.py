import requests
from time import sleep
import vlc




uberduck_auth = ("pub_lzybtvvnnzrsssvstb", "pk_77ba8c6f-899e-4bd2-a2d8-a99bbc53dd75") #uberudck auth
print(requests.get("https://api.uberduck.ai/status").json())

voicemodel_uuid = "de6d0d66-5501-472e-a0e0-31bfe7fe2c75" #voice model uuid
text = "Hello i'm a test bot"

audio_uuid = requests.post(
    "https://api.uberduck.ai/speak",
    json=dict(speech=text, voicemodel_uuid=voicemodel_uuid),
    auth=uberduck_auth,
    ).json()["uuid"]

for t in range(10):
    sleep(1) # check status every second for 10 seconds.
    output = requests.get(
        "https://api.uberduck.ai/speak-status",
        params=dict(uuid=audio_uuid),
        auth=uberduck_auth,
        ).json()
    if "path" in output:
        audio_url = output["path"]
        print(audio_url)
        break

p = vlc.MediaPlayer(audio_url)


