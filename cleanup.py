import os
import json

for i in os.listdir('svg'):
  if 'day' in i:
    content = open('svg/' + i).read()
    content = content.replace('fill="#F59E0B"', 'fill="#FBBF24"')
    open('svg/' + i, 'w').write(content)