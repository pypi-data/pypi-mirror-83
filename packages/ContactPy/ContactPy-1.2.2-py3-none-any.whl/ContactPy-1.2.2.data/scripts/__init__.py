import json
import os

fdata = {"IMAGE":{"type": "image","id": "Nan"},"PDF":{"type": "application","id": "octet-stream"}}
if os.path.isfile("types.json"):
	pass
else:
	f = open("types.json", w)
	f.write(json.dumps(fdata))
	f.close()

__version__ = "1.2.2"