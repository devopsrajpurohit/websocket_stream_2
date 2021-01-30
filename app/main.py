# from fastapi import FastAPI
# #
# # app = FastAPI()
# #
# # @app.get("/")
# # def index():
# # 	return {"title": "hellooo"}
import json
import asyncio
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")

with open('measurements.json', 'r') as file:
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

# at last, the bottom of the file/module
if __name__ == "__main__":
	uvicorn.run(app)