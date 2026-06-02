import requests
response = requests.get("https://urlscan.io/api/v1/search/?q=date:>now-1h", timeout=10)
print(response.status_code)
if response.status_code == 200:
    data = response.json()
    print("Found", len(data.get("results", [])), "results")
else:
    print(response.text)
