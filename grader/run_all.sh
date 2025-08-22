#DO NOT CHANGE THIS FILE

#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
bash "$HERE/test_case_01.sh"
bash "$HERE/test_case_02.sh"
bash "$HERE/test_case_03.sh"
bash "$HERE/test_case_04.sh"
echo "All tests passed."