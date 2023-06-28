import requests
from time import sleep

uberduck_auth = ("") #uberudck auth
print(requests.get("https://api.uberduck.ai/status").json())

voicemodel_uuid = "4bed3a85-946d-4e47-bd35-b3a2f51b3efa" #voice model uuid
text = "good morning char"
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



