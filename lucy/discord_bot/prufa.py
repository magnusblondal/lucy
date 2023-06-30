import requests

LUCY_URL = "http://127.0.0.1:8000"

response = requests.get(LUCY_URL + "/bot")

# Step 4: Check the status of the response
if response.status_code == 200:
    # Step 5: Extract the data from the response
    data = response.json()
    # print(data)
    bots = data["data"]
    resp = [f"{b['name']} {b['capital']} {b['entry_size']} {b['so_size']} {b['id']}\n" for b in bots]
    print(resp)
else:
    print(f"Request failed with status code {response.status_code}")
