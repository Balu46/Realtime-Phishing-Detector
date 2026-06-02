import requests
try:
    r = requests.get("https://crt.sh/?q=%paypal%&output=json", timeout=15)
    print(len(r.json()), "results found")
except Exception as e:
    print("Error:", e)
