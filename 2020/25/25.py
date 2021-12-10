x = 1

pubKeys = set()
pubKeys.add(11404017)
pubKeys.add(13768789)

loops = 0
while x not in pubKeys:
    x = x * 7
    x = x % 20201227
    loops += 1

print("public key:", x)
print("private loop size:", loops)

pubKeys.remove(x)

while x not in pubKeys:
    x = x * 7
    x = x % 20201227
    loops += 1

print("public key:", x)
print("private loop size:", loops)

x = 1
subjectNumber = 13768789
for i in range(11710225):
    x = x * subjectNumber
    x = x % 20201227

print("enc key 1", x)

x = 1
subjectNumber = 11404017
for i in range(8516638):
    x = x * subjectNumber
    x = x % 20201227

print("enc key 2", x)