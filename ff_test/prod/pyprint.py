import json
import sys

if len(sys.argv) < 2:
  print('Specify the path of the parameter file')
  sys.exit()

# Read the parameters
file_parameter = sys.argv[1]
with open(file_parameter) as foo:
  pp = json.load(foo)

for key in pp:
  string = 'pp[\'%s\'] = %s' %(key, pp[key])
  print(string)
