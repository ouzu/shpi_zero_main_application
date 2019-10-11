from requests import get, post

url = 'http://10.0.1.172:8123/api/services/light/toggle'
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI4MGQ0NjA4YjlkMWY0MTkwOGIwNGUxMDZiMzY4MmQxMiIsImlhdCI6MTU3MDgxNzYxNiwiZXhwIjoxODg2MTc3NjE2fQ.rWoJeWwFkQgX726L_-wIYMt3bXXnay8HPMH1UTJec28',
    'content-type': 'application/json',
}

response = post(url, headers=headers, data='{"entity_id": "light.wohnzimmer"}')
print(response.text)