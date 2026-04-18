with open('/PeTTa/repos/omegaclaw/src/loop.metta') as f:
    content = f.read()
opens = content.count('(')
closes = content.count(')')
print('OPEN=' + str(opens) + ' CLOSE=' + str(closes) + ' BALANCED=' + str(opens == closes))