import json
from pprint import pprint
import sys

USER = "user_id"
BIZ = "business_id"

if len(sys.argv) != 2:
  print "Usage: python preprocess.py filename.json"
  sys.exit(-1)

fname = sys.argv[1]

if fname[-5:] != ".json":
  print "file must have extension '.json'"
  sys.exit(-2)

fprefix = fname[:-5]



print "Constructing map - reviewer: business"
# user_id: business_id
dct = {}
# because Yelp doesn't have properly formatted json files
# it's not completely garbage but it kind of is
with open(fname) as f:
  for line in f:
    data = json.loads(line)
    user = data[USER]
    business = data[BIZ]
    if user not in dct:
        dct[user] = []
    dct[user].append(business)


print "Constructing map - business: business, weight"
# b1: {b2: weight2, b3:weight3}
bizzes = {}
# collate results
for _, blist in dct.iteritems():
  for b1 in blist:
    for b2 in blist:
      # document pair (b1, b2)
      if b1 == b2:
        continue
      if b1 not in bizzes:
        bizzes[b1] = {}
      if b2 not in bizzes[b1]:
        bizzes[b1][b2] = 0
      bizzes[b1][b2] += 1

print "Writing to file"
# write to file
with open(fprefix + ".txt",'w') as f:
  # header for weighted graph
  f.write("1\n")
  for b1, b_dict in bizzes.iteritems():
     f.write(b1)
     for b2, w2 in b_dict.iteritems():
       f.write(" " + b2 + " " + str(w2))
     f.write("\n")
