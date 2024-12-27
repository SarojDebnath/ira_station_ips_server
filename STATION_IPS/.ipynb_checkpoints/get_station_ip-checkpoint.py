from fastapi import FastAPI, Request
import uvicorn
import json
from pathlib import Path
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Define template directory
templates = Jinja2Templates(directory="templates")  # Ensure the path is correct
data_file = Path("ip_addresses.json")

# Load IP data from file if it exists
if data_file.exists():
    with open(data_file, "r") as f:
        ip_data = json.load(f)
else:
    ip_data = {}

@app.post("/register_ip/{pc_name}")
async def register_ip(pc_name: str, request: Request):
    client_ip = request.client.host
    ip_data[pc_name] = client_ip
    with open(data_file, "w") as f:
        json.dump(ip_data, f)
    return {"message": f"IP registered for {pc_name}", "ip": client_ip}

@app.get("/get_ips")
async def get_ips(request: Request):
    # Format data for easy display in table
    formatted_data = [
        {"StationID": key.split("_")[0], "Name": key.split("_")[1], "IP": value}
        for key, value in ip_data.items()
    ]
    return templates.TemplateResponse("ips_table.html", {"request": request, "ips": formatted_data})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
