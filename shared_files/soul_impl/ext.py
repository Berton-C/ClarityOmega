import subprocess, sys
r = subprocess.run(["pdftotext", "/tmp/soul_impl/hyperseed_v7.pdf", "-"], capture_output=True, text=True)
if r.returncode == 0:
    t = r.stdout
    print("CHARS:", len(t))
    print(t[:8000])
else:
    print("PDFTOTEXT_FAIL")
    print(r.stderr)
    # fallback: raw extraction
    import re
    with open("/tmp/soul_impl/hyperseed_v7.pdf", "rb") as f:
        data = f.read()
    chunks = re.findall(rb"\(([\x20-\x7e]{20,})\)", data)
    result = b" ".join(chunks).decode("latin-1", errors="replace")
    print("RAW_CHARS:", len(result))
    print(result[:8000])