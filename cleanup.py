import os
import json

data = json.load(open('weathers.json'))
data = sum([[i['dayIcon'], i['nightIcon']] for i in data], [])
icons = [i.split('.').pop(0) for i in os.listdir("svg")]
print([os.remove("svg/"+i+'.svg') for i in icons if i not in data])