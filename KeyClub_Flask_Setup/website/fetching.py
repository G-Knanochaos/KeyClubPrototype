from flask import url_for
import requests
import json
from datetime import date
import os
from time import time

requests_map = {
    "events":"https://script.google.com/macros/s/AKfycbzQFrs5AnxX-JjJuBOt_B41QoHLyc2iUmREIcJzIql6nzWW7VOxiTMNJchRK6Ptltjwlg/exec",
    "images":"https://script.google.com/macros/s/AKfycbzdLT7ZYBBf50gHiWll_qUatXHToagXeSqRsra7U1gitvEkDpgsUVXm-dr311D6BYzZ/exec",
    "Sheets":"https://script.google.com/macros/s/AKfycbxYbxTPG8IGwCpWVFbpTxi1Jx8Kk8WK3KTP_Vd9oiBMRElh4MSGAsYPR9A6FLYcu9MLSw/exec",
    "Misc":"https://script.google.com/macros/s/AKfycbzmioExdkHHboQDNtZUjMjAlgcKrYutKkjZrJv3DpT0q-ruQI3tzo-wtChISbxLAnM/exec",
}
#n: number of objects to fetch, #s: number multiple
def fetch(typ,payload={},json_name=None,override=False):#if override is set to True, changes won't be fetched until next day and changes will completely overwrite past state
    start = time()
    json_name = json_name if json_name else typ
    n = payload.get("n",4)
    print(f"Fetching {typ}!")
    url = url_for("static", filename = f"json/{json_name}.json")
    today = date.today().strftime("%m%d%y")
    with open(os.path.join(os.path.dirname(__file__),url[1:]), "r") as file:
        try: 
            f = json.load(file)
        except Exception as e:
            print("File JSON parsing error, emptying file and refetching data")
            print(e)
            f = {"date":None,typ:[]}
    if f.get("date",None) == today:
        if override or len(f[typ]) >= n:
            return f[typ] if payload.get("all") else f[typ][:n]
    
    n = n-len(f.get(typ,[]))

    r = requests.get(requests_map[typ],params = payload).text

    print(r)
    j = json.loads(r)
    j["date"] = today
    j[typ] = (f[typ] if not override else [])+j[typ]
    with open(os.path.join(os.path.dirname(__file__),url[1:]), "w") as file:
        file.write(json.dumps(j))

    print(f"Fetched {typ} in {time()-start}")
    return j[typ]

