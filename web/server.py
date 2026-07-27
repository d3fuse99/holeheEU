from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
import sys
import os
import json
import webbrowser
import threading
import time

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=current_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    file_path = os.path.join(current_dir, "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/scan")
async def get_scan_stream(email: str):
    async def event_generator():
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        run_script = os.path.join(base_dir, "run.py")
        cmd = [sys.executable, "-u", run_script, email, "d"]
        env = os.environ.copy()
        env["HOLEHE_WEB"] = "1"
        env["PYTHONPATH"] = base_dir
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=env
        )
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            line_str = line.decode("utf-8", errors="ignore").replace("\r", "").strip()
            
            if " | " in line_str and any(tag in line_str for tag in ["[+]", "[-]", "[L]"]):
                parts = line_str.split(" | ")
                status_part = parts[0].strip()
                status = "LIMIT"
                if "[+]" in status_part:
                    status = "EXISTS"
                elif "[-]" in status_part:
                    status = "not found"
                elif "[L]" in status_part:
                    status = "LIMIT"
                
                raw_name = status_part.replace("[+]", "").replace("[-]", "").replace("[L]", "").strip()
                name = raw_name.split()[-1] if raw_name else "Unknown"
                domain = parts[2].strip() if len(parts) > 2 else "N/A"
                
                payload = {
                    "type": "progress",
                    "name": name,
                    "status": status,
                    "domain": domain
                }
                yield f"data: {json.dumps(payload)}\n\n"
            elif line_str and not line_str.startswith("Scanning:") and not line_str.startswith("100%"):
                payload = {
                    "type": "info",
                    "message": line_str
                }
                yield f"data: {json.dumps(payload)}\n\n"
        
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)