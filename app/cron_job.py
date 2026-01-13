import datetime
import os
from totp_utils import generate_totp

SEED_PATH = "/data/seed.txt"
LOG_PATH = "/cron/last_code.txt"

def run_cron():
    if not os.path.exists(SEED_PATH):
        return
    with open(SEED_PATH, "r") as f:
        seed = f.read().strip()
    
    code, _ = generate_totp(seed)
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} 2FA Code: {code}\n"
    
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(log_entry)

if __name__ == "__main__":
    run_cron()