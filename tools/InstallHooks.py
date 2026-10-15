"""Nối kiểm tra dữ liệu vào hook cục bộ được hook toàn cục gọi."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
HOOK_CONTENT = '''#!/bin/sh
set -eu
cd "$(git rev-parse --show-toplevel)"
exec python3 tools/VerifyData.py
'''

if __name__ == "__main__":
    git_dir = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
    hook = Path(git_dir) / "hooks" / "pre-commit"
    if not hook.is_absolute():
        hook = ROOT / hook
    if hook.exists() and hook.read_text() != HOOK_CONTENT:
        sys.exit("Đã có hook khác; dừng để không ghi đè cấu hình hiện hữu.")
    hook.write_text(HOOK_CONTENT)
    hook.chmod(0o755)
    print("Đã nối kiểm tra 50 phiếu và báo cáo vào pre-commit cục bộ.")
