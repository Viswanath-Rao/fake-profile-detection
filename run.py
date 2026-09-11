import os
import sys
import time
import webbrowser
import threading
import uvicorn

BANNER = r"""
========================================================================
   __      __        _ _____            __ _ _         ___  _____ 
   \ \    / /       (_)  __ \          / _(_) |       / _ \|_   _|
    \ \  / /__ _ __  _| |__) | __ ___ | |_ _| | ___  / /_\ \ | |  
     \ \/ / _ \ '__| |  ___/ '__/ _ \|  _| | |/ _ \ |  _  | | |  
      \  /  __/ |  | | |   | | | (_) | | | | |  __/ | | | |_| |_ 
       \/ \___|_|  |_|_|   |_|  \___/|_| |_|_|\___| \_| |_/_____|
                                                                  
   Deepfake & Fake Profile Forensics Intelligence Suite
========================================================================
"""

def open_browser():
    time.sleep(1.2)
    url = "http://localhost:8000"
    print(f"\n[+] Launching VeriProfile AI in your default browser: {url}\n")
    webbrowser.open(url)

if __name__ == "__main__":
    print(BANNER)
    # Ensure model is ready
    from core.detector import ProfileForensicEngine
    print("[*] Initializing Forensic Engine & Validating Cascade Classifiers...")
    _ = ProfileForensicEngine()
    print("[*] Core System Ready.")

    # Start browser opener in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start Uvicorn Server
    print("[*] Starting ASGI Server on http://127.0.0.1:8000 ... (Press Ctrl+C to stop)")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="info", reload=False)
