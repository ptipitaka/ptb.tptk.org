from pathlib import Path
from collections import Counter
import re

lines = Path("Initial_source/html5/07.html").read_text(encoding="utf-8").splitlines()
chunk = "\n".join(lines[1154:1508])
ctr = Counter(re.findall(r'<p class="([^"]+)"', chunk))
for k, v in sorted(ctr.items(), key=lambda x: -x[1]):
    print(v, k)
