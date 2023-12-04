from flask import url_for
import requests
import json
import datetime
import os
from time import time

requests_map = {
    "events":"https://script.google.com/macros/s/AKfycbzQFrs5AnxX-JjJuBOt_B41QoHLyc2iUmREIcJzIql6nzWW7VOxiTMNJchRK6Ptltjwlg/exec",
    "images":"https://script.google.com/macros/s/AKfycbz8Rjt2zxK97BEDWuy3iSiVOCCEI5fYmQX61RhLfLbLs1n1ebcNUEWwz1yCl00wmMBZ/exec",
    "Sheets":"https://script.google.com/macros/s/AKfycbz_FP0mj05nt9jmiirhTaYN0-K3y-KNqMwu_rHXeB0KjCSPKRriC-kEd7qoAjKEokBu9g/exec",
    "Misc":"https://script.google.com/macros/s/AKfycbzmioExdkHHboQDNtZUjMjAlgcKrYutKkjZrJv3DpT0q-ruQI3tzo-wtChISbxLAnM/exec",
    "past_photos":"https://script.google.com/macros/s/AKfycbyEkmydKArw2hU-zfQe_uwqj3rgbTKjXJQz_J0f8Tw/dev"

}
#n: number of objects to fetch, #s: number multiple
def fetch(typ,payload={},json_name=None,override=False,interval=1): #if override is set to True, changes won't be fetched until next day and changes will completely overwrite past state
    start = time()
    add = override
    json_name = json_name if json_name else typ
    n = payload.get("n",-1)
    print(f"Fetching {typ}!")
    url = url_for("static", filename = f"json/{json_name}.json")
    today = int(datetime.datetime.now().strftime("%Y%m%d"))
    with open(os.path.join(os.path.dirname(__file__),url[1:]), "r") as file:
        try: 
            f = json.load(file)
        except Exception as e:
            print("File JSON parsing error, emptying file and refetching data")
            print(e)
            f = {"date":None,typ:[]}
    try:
        if (today - f.get("date",None)) < interval:
            print(len(f[typ]),n)
            if len(f[typ]) >= n:
                return f[typ]
            add = True
            print("add is now true")
    except Exception as e:
        print(e)
    
    n = n-len(f.get(typ,[]))

    print("Sending request to proxy")
    r = requests.get(requests_map[typ],params = payload).text

    print(r)
    j = json.loads(r)
    j["date"] = int(today)
    if add and not override:j[typ] += f[typ]
    with open(os.path.join(os.path.dirname(__file__),url[1:]), "w") as file:
        file.write(json.dumps(j))

    print(f"Fetched {typ} in {time()-start}")
    return j[typ]
