import json
import asyncio
from pathlib import Path

# import uvicorn  # UNUSED NOW
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates


TEMPLATES_FOLDER_NAME = 'templates'
MEASUREMENTS_FILE_NAME = 'measurements.json'
CURRENT_FOLDER = Path(__file__).parent
MEASUREMENTS_FILE = CURRENT_FOLDER / MEASUREMENTS_FILE_NAME


app = FastAPI(debug=True)

templates = Jinja2Templates(directory=CURRENT_FOLDER / TEMPLATES_FOLDER_NAME)

with MEASUREMENTS_FILE.open('r') as file:
	measurements = iter(json.loads(file.read()))


@app.get("/")
def read_root(request: Request):
	return templates.TemplateResponse("index.htm", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
	await websocket.accept()
	while True:
		await asyncio.sleep(0.1)
		payload = next(measurements)
		await websocket.send_json(payload)


# # at last, the bottom of the file/module
# if __name__ == "__main__":
# 	uvicorn.run(app)
