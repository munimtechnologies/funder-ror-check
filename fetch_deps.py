# SPDX-License-Identifier: Apache-2.0
# Fetch funder_ror_check.py v0.1.0 (same repository, tagged release) into the working folder.
import urllib.request

URL = ("https://raw.githubusercontent.com/munimtechnologies/funder-ror-check/"
       "v0.1.0/funder_ror_check.py")
urllib.request.urlretrieve(URL, "funder_ror_check.py")
with open("funder_ror_check.py", encoding="utf-8") as f:
    text = f.read()
assert 'VERSION = "0.1.0"' in text, "unexpected funder_ror_check.py"
print("fetched funder_ror_check.py (%d bytes)" % len(text))
