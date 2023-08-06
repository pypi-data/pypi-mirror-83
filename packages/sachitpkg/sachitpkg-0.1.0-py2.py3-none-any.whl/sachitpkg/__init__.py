__version__ = '0.1.0'

import requests

def myfunc():
    uri = "https://api.postalpincode.in/pincode/110088"
    response = requests.get(uri).json()
    #json_obj = json.loads(response.text)
    print(response)

myfunc()
