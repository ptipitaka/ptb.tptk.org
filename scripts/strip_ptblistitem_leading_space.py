import re
from pathlib import Path
import sys

p = Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
t2 = re.sub(r'(<PtbListItem marker="[^"]+">) ', r"\1", t)
p.write_text(t2, encoding="utf-8")
print("done")
