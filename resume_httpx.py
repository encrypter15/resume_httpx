import subprocess
import os
import sys
import re

# Configuration
INPUT_FILE = "filtered_assets.txt"
CLEAN_FILE = "clean_assets.txt"
OUTPUT_FILE = "live_bounty.txt"
RESUME_FILE = "resume.cfg"

# Optimized for speed and mobile stability
RATE_LIMIT = 50 
THREADS = 15
TIMEOUT = 5
RETRIES = 1

def sanitize_input():
    """Strips regex, wildcards, and paths to give httpx clean targets."""
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Error: {INPUT_FILE} not found.")
        sys.exit(1)
        
    print(f"[*] Sanitizing {INPUT_FILE}...")
    # Matches FQDNs and IPv4s only
    pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b|\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    with open(INPUT_FILE, 'r') as f:
        content = f.read().lower()
    
    clean_targets = sorted(set(re.findall(pattern, content)))
    
    with open(CLEAN_FILE, 'w') as f:
        f.write("\n".join(clean_targets))
    
    print(f"[*] Cleaned {len(clean_targets)} targets. Ready to scan.")
    return CLEAN_FILE

def run_httpx(target_list):
    use_resume = os.path.exists(RESUME_FILE)
    
    cmd = [
        "httpx",
        "-l", target_list,
        "-o", OUTPUT_FILE,
        "-rl", str(RATE_LIMIT),
        "-threads", str(THREADS),
        "-timeout", str(TIMEOUT),
        "-retries", str(RETRIES),
        "-status-code", # Shows 200/403/etc so you see progress
        "-silent" 
    ]

    if use_resume:
        cmd.extend(["-resume", RESUME_FILE])
        print(f"[*] Resuming scan from {RESUME_FILE}...")
    else:
        print("[*] Starting fresh scan...")

    try:
        # Using subprocess.run for better stability
        subprocess.run(cmd, check=True)
        print(f"[*] Scan complete. Results in {OUTPUT_FILE}")
    except KeyboardInterrupt:
        print("\n[!] Interrupted. Resume data saved to resume.cfg.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Execution Error: {e}")

if __name__ == "__main__":
    # 1. Clean the junk
    sanitized_file = sanitize_input()
    
    # 2. Run the scan
    run_httpx(sanitized_file)
