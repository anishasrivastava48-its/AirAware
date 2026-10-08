"""
AirAware Unified Services Launcher
----------------------------------
Starts the FastAPI REST API (port 8000) and the Streamlit Dashboard (port 8501)
concurrently or independently.

Usage:
    python start_services.py          # Starts both API and Dashboard
    python start_services.py --api    # Starts only FastAPI backend
    python start_services.py --ui     # Starts only Streamlit frontend
"""

import sys
import time
import subprocess
import argparse

def start_both():
    print("=" * 70)
    print("AIRAWARE: Starting Unified Services Architecture")
    print("=" * 70)
    print("1. Launching FastAPI REST Backend at http://localhost:8000 ...")
    api_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "api:app",
        "--host", "0.0.0.0", "--port", "8000"
    ])

    time.sleep(2)

    print("2. Launching Streamlit Interactive Dashboard at http://localhost:8501 ...")
    ui_proc = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501"
    ])

    print("\n" + "=" * 70)
    print("Both services are running!")
    print("  * Streamlit Dashboard : http://localhost:8501")
    print("  * REST API & Swagger  : http://localhost:8000/docs")
    print("  * ReDoc Specification : http://localhost:8000/redoc")
    print("=" * 70)
    print("Press Ctrl+C to terminate both services.\n")

    try:
        api_proc.wait()
        ui_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down AirAware services...")
        api_proc.terminate()
        ui_proc.terminate()
        print("Services stopped.")

def main():
    parser = argparse.ArgumentParser(description="AirAware Services Launcher")
    parser.add_argument("--api", action="store_true", help="Launch only FastAPI backend")
    parser.add_argument("--ui", action="store_true", help="Launch only Streamlit dashboard")
    args = parser.parse_args()

    if args.api:
        print("Launching FastAPI REST API on http://localhost:8000 ...")
        subprocess.run([sys.executable, "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"])
    elif args.ui:
        print("Launching Streamlit Dashboard on http://localhost:8501 ...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"])
    else:
        start_both()

if __name__ == "__main__":
    main()
