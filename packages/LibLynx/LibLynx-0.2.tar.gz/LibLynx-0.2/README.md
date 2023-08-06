# liblynx

Python Library to interact with LibLynx https://www.liblynx.com/

Usage example:

```
import liblynx

CLIENT_ID = "< your ID >"
CLIENT_SECRET = "< your SECRET >"

access_token = liblynx.access_token(CLIENT_ID, CLIENT_SECRET)
api = liblynx.endpoint(access_token)
assert "_links" in api

liblynx.new_identification(access_token, api, "127.0.0.127", "https://example.com/foo/", "Python-LibLynx-Testing/0.1")
```
