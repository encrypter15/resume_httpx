# resume-httpx.py – Resumable HTTPX Scanner Wrapper for Termux/Android

A simple Python wrapper around **ProjectDiscovery's httpx** tool to make large-scale HTTP probing resumable, bandwidth-friendly, and phone-optimized.

Perfect for bug bounty hunters running recon on Android phones via Termux — scan thousands of targets (e.g., from payout-targets-data or Chaos) without losing progress when interrupted (battery low, Wi-Fi drop, Termux killed, etc.).

## Why This Script?

- httpx has built-in resume via `-resume resume.cfg`, but this wrapper adds:
  - Automatic resume detection
  - Progress display (total targets)
  - Easy tuning for low bandwidth/CPU/heat on mobile
  - Optional batching (future-proof)
- Avoids re-probing already-scanned hosts → saves data & time
- No extra dependencies beyond Python (pre-installed in Termux)

Tested with httpx v1.6+ (uses `-threads` flag).

## Features

- Resumes scans seamlessly after Ctrl+C or Termux restart
- Rate limiting (`-rl`) & concurrency (`-threads`) tuned for phones
- Retries, timeouts, and silent mode by default
- Works with large input lists (e.g., 7k+ domains from GitHub bounty repos)

## Requirements

- Termux on Android (with storage permission: `termux-setup-storage`)
- Python (pre-installed: `pkg install python`)
- httpx installed via Go:
  ```bash
  go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
  cp ~/go/bin/httpx $PREFIX/bin/
  ```

## Installation

1. Clone or download this repo:
   ```bash
   git clone https://github.com/encrypter15/resume_httpx
   cd resume-httpx
   ```

   (Or just save `resume_httpx.py` manually)

2. Prepare your target list (example from bounty repo):
   ```bash
   mkdir -p ~/bounty_targets && cd ~/bounty_targets
   wget https://raw.githubusercontent.com/osamahamad/payout-targets-data/main/assets.out
   grep -v '^*' assets.out | sort -u > filtered_assets.txt   # non-wildcards only
   ```

3. Copy or symlink the script to your working dir:
   ```bash
   cp /path/to/resume_httpx.py .
   ```

## Usage

Run in your targets folder:

```bash
python resume_httpx.py
```

- First run: Starts fresh scan
- Interrupt with **Ctrl+C** → httpx creates `resume.cfg`
- Re-run the same command → auto-resumes from `resume.cfg`

**Output example**:
```
Total targets: 7411
Resuming from resume.cfg   # or "Starting fresh scan"
```

The script runs httpx with safe mobile defaults:
- `-rl 20` (requests/sec)
- `-threads 5` (concurrency)
- `-retries 2`
- `-timeout 15`
- `-silent -o live_bounty.txt`

**Customize** (edit the script):
- Change `RATE_LIMIT = 10` or `THREADS = 3` for even lower impact
- Add flags like `-sc -title -tech-detect` or `-json` for richer output
- To start fresh: `rm resume.cfg && python resume_httpx.py`

## Tips for Termux/Android

- Use `termux-wake-lock` to prevent Android killing the process
- Run while charging + stable Wi-Fi
- Monitor heat: Lower `-rl` / `-threads` if phone gets hot
- After scan: `cat live_bounty.txt | nuclei -severity low,medium ...` for vuln checks
- Update list periodically: `wget -O assets.out ...` → re-filter & resume

## License

MIT License – feel free to fork, modify, and use in your bug bounty workflows.

## Author

- **Encrypter** (@Encrypter15 on X/Twitter)
- Email: encrypter15@gmail.com
- GitHub: https://github.com/encrypter15

Built for mobile recon hunters — drop a star or tag @Encrypter15 when you land a bounty using this! 🏆📱

Happy hunting! 🔍
