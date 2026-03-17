#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
PROJECT  : Resume HTTPX (Automation Layer)
VERSION  : 1.2.1
DEVELOPER: Encrypter15 (encrypter15@gmail.com)
GITHUB   : https://github.com/encrypter15
--------------------------------------------------------------------------------
NOTES:
- Input Sanitization: Strips regex/wildcards from scope files before scanning.
- Logic-Driven: Uses strict timeouts (5s) to prevent thread-hangs on dead subnets.
- Post-Processing: Auto-sorts output by status code for rapid analysis.
--------------------------------------------------------------------------------
"""

import subprocess
import os
import sys
import re

# Configuration
INPUT_FILE = "filtered_assets.txt"
CLEAN_FILE = "clean_assets.txt"
OUTPUT_FILE = "live_bounty.txt"
RESUME_FILE = "resume.cfg"

# Network Aggression (Adjust for mobile/low-bandwidth if needed)
RATE_LIMIT = 50 
THREADS = 15
TIMEOUT = 5
RETRIES = 1

def sanitize_input():
    """Extracts valid FQDNs/IPs. Strips the junk causing 'hours' of delays."""
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Critical Error: {INPUT_FILE} is missing.")
        sys.exit(1)
        
    print(f"[*] Analyzing {INPUT_FILE} for valid targets...")
    
    # Matches standard hostnames and IPv4 addresses
    pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b|\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    with open(INPUT_FILE, 'r') as f:
        content = f.read().lower()
    
    matches = re.findall(pattern, content)
    clean_targets = sorted(set(matches))
    
    with open(CLEAN_FILE, 'w') as f:
        f.write("\n".join(clean_targets))
    
    print(f"[*] Sanitized {len(clean_targets)} targets.")
    return CLEAN_FILE

def sort_results():
    """Sorts live_bounty.txt so the hits (200 OK) are at the top."""
    if not os.path.exists(OUTPUT_FILE):
        print("[!] No output file found to sort.")
        return
        
    print(f"[*] Post-processing: Sorting results by status code...")
    
    with open(OUTPUT_FILE, 'r') as f:
        lines = f.readlines()
    
    def get_status_rank(line):
        match = re.search(r'\[(\d{3})\]', line)
        if match:
            code = match.group(1)
            # Prioritize 200, then 403, 401, then redirects
            if code == "200": return (0, code)
            if code in ["403", "401"]: return (1, code)
            return (2, code)
        return (3, "999")

    lines.sort(key=get_status_rank)
    
    with open(OUTPUT_FILE, 'w') as f:
        f.writelines(lines)
    print(f"[*] Finalized {OUTPUT_FILE}.")

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
        "-status-code", 
        "-silent" 
    ]

    if use_resume:
        cmd.extend(["-resume", RESUME_FILE])
        print(f"[*] Resuming scan from {RESUME_FILE}...")
    else:
        print("[*] Initiating fresh scan...")

    try:
        # Popen replaced with run for synchronous reliability
        subprocess.run(cmd, check=True)
        sort_results()
        print("[*] All processes complete.")
    except KeyboardInterrupt:
        print("\n[!] Execution paused. Resume config preserved.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] HTTPX Error: {e}")

if __name__ == "__main__":
    print(f"--- Resume HTTPX v1.2.1 | Dev: Encrypter15 ---")
    sanitized_file = sanitize_input()
    run_httpx(sanitized_file)
