import subprocess
r = subprocess.run(['pdftotext', '-f', '315', '-l', '340', '/PeTTa/repos/omegaclaw/soul/sources/hyperseed_v7.pdf', '-'], capture_output=True, text=True)
print(r.stdout[:8000])
