import subprocess
import os
import sys

INPUT_FILE = "filtered_assets.txt"
OUTPUT_FILE = "live_bounty.txt"
RESUME_FILE = "resume.cfg"
RATE_LIMIT = 25
THREADS = 8

def run_httpx():
    # Check if we should resume
    use_resume = os.path.exists(RESUME_FILE)
    
    cmd = [
        "httpx",
        "-l", INPUT_FILE,
        "-o", OUTPUT_FILE,
        "-rl", str(RATE_LIMIT),
        "-threads", str(THREADS),
        "-retries", "2",
        "-timeout", "10",
        "-v" # Added for visibility
    ]

    if use_resume:
        cmd.extend(["-resume", RESUME_FILE])
        print(f"[*] Resuming from {RESUME_FILE}")
    else:
        print("[*] Starting fresh scan")

    try:
        # Using run() instead of Popen for synchronous execution
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n[!] Interrupted. Resume config saved.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        sys.exit(1)
        
    run_httpx()
