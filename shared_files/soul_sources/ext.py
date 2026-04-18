import re, sys
fp = str(sys.argv[1])
with open(fp, chr(114)+chr(98)) as f:
    data = f.read()
chunks = re.findall(rb"\x28([\x20-\x7e]{10,})\x29", data)
result = b" ".join(chunks).decode("latin-1", errors="replace")
print("TOTAL_CHARS:", len(result))
for i in range(0, min(len(result), 48000), 8000):
    print("=== CHUNK", i//8000, "===")
    print(result[i:i+8000])