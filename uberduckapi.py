from IPython.display import Audio
import requests
from time import sleep

uberduck_auth = ("uberduck api")
print(requests.get("https://api.uberduck.ai/status").json())

voicemodel_uuid = "778e27be-877f-4b61-aefc-4eb2ff88ec11"
text = "War is cruelty, and you cannot refine it; and those who brought war into our country deserve all the curses and maledictions a people can pour out. I know I had no hand in making this war, and I know I will make more sacrifices to-day than any of you to secure peace."
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
        break
print(audio_url)


