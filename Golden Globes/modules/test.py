import re

result = ''
with open('test.txt') as f:
    for line in f:
        match = re.search(r'(\w+).+UTC([+-])(\S+)', line)
        if match:
            if match.group(2) == '+':
                result += '(\'' + match.group(1) + '\', ' + match.group(3) + ', False), '
            else:
                result += '(\'' + match.group(1) + '\', -' + match.group(3) + ', False), '
print result