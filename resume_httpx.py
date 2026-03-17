import subprocess
import time
import sys
import os

INPUT_FILE = "filtered_assets.txt"
OUTPUT_FILE = "live_bounty.txt"
RESUME_FILE = "resume.cfg"
BATCH_SIZE = 5000          # Process \~5000 hosts, then pause/resume
RATE_LIMIT = 25            # req/sec
THREADS = 8   # or lower like 5 for phone

def run_httpx(use_resume=False):
    cmd = [
        "httpx",
        "-l", INPUT_FILE,
        "-silent",
        "-o", OUTPUT_FILE,
        "-rl", str(RATE_LIMIT),
        "-threads", str(THREADS),
        "-retries", "2",
        "-timeout", "15"
    ]
    if use_resume and os.path.exists(RESUME_FILE):
        cmd.extend(["-resume", RESUME_FILE])
        print(f"Resuming from {RESUME_FILE}")
    else:
        print("Starting fresh scan")

    # Run and wait
    process = subprocess.Popen(cmd)
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nInterrupted — httpx should have created resume.cfg")
        sys.exit(1)

# Optional: Simple batching (if you want manual pauses)
lines = sum(1 for _ in open(INPUT_FILE))
print(f"Total targets: {lines}")

# But since httpx resumes natively, just run once — interrupt as needed
run_httpx(use_resume=True)  # Change to False for fresh start

# Or loop with pauses (less needed):
# for i in range(0, lines, BATCH_SIZE):
#     print(f"Batch {i//BATCH_SIZE + 1}")
#     run_httpx(use_resume=True)
#     time.sleep(300)  # 5 min pause — or manual Ctrl+C3
