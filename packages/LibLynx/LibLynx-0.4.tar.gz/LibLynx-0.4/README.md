# liblynx

Python Library to interact with LibLynx https://www.liblynx.com/

Usage example:

```
import liblynx

CLIENT_ID = "< your ID >"
CLIENT_SECRET = "< your SECRET >"
ll = liblynx.Connect(CLIENT_ID, CLIENT_SECRET)

# or just,
ll = liblynx.Connect()    # Then the ENV Variables LIBLYNX_CLIENT_ID and LIBLYNX_CLIENT_SECRET are used

print(ll.access_token)
print(ll.endpoint)
# Note how the .access_token and .endpoint attribute access results in a cached lookup

identification1 = ll.new_identification("127.0.0.127", "https://example.com/foo/", "Python-LibLynx-Testing/0.1")
```
