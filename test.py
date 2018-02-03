import math
def isSquare(x):
	d = math.sqrt(x)
	m = math.floor(d)
	if m*m == x:
		return True
	return False

for i in range(10000):
	if isSquare(i+100) and isSquare(i+192):
		print(i)
