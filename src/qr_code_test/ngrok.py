import requests

def get_ngrok_base_url() -> str | None:
    try:
        r = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=2)
        tunnels = r.json().get("tunnels", [])
        
        for t in tunnels:
            if t.get("proto") == "https":
                return t["public_url"]    
        return None
     
    except Exception:
        return None
    
