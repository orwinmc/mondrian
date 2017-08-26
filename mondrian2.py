# MONDRIAN SECTION
import copy

check=[]
grid=[]
minArea=float("inf")
maxArea=0
minDiff=float("inf")
ans=[]
SIZE=7

def initCheckAndGrid(num):
	global check
	global grid

	for i in range(num):
		checkList = []
		gridList = []
		for i in range(num):
			checkList.append(False)
			gridList.append(0)
		check.append(checkList);
		grid.append(gridList);

def nextLoc(num,x,y):
	global grid

	while (y<num):
		if grid[x][y]!=0:
			x+=1
			y+=x/num
			x%=num
		else:
			break
	return x,y

def fillSection(num,x,y,width,height,index):
	global check
	global grid

	i=x; j=y
	while (i<x+width and i<num):
		while (j<y+height and j<num):
			grid[i][j]=index
			j+=1
		j=y; i+=1
	check[width-1][height-1]=True
	check[height-1][width-1]=True

def unfillSection(num,x,y,width,height):
	global check
	global grid

	i=x; j=y
	while (i<x+width and i<num):
		while (j<y+height and j<num):
			grid[i][j]=0
			j+=1
		j=y; i+=1
	check[width-1][height-1]=False
	check[height-1][width-1]=False

def canFill(num,x,y,width,height):
	global grid

	i=x; j=y
	while (i<x+width and i<num):
		while (j<y+height and j<num):
			if grid[i][j]!=0:
				return False
			j+=1
		j=y; i+=1
	return True

def isCovered(num):
	global grid

	for i in range(num):
		for j in range(num):
			if (grid[i][j]==0):
				return False
	return True

def printGrid(grid):
	for i in range(len(grid)):
		print grid[i]

def mondrian(num,x,y,index):
	global check
	global grid
	global minArea
	global maxArea
	global minDiff
	global ans

	if (isCovered(num) and index>2):
		minDiff=maxArea-minArea
		ans=copy.deepcopy(grid)
	else:
		for width in range(1,num+1-x):
			for height in range(1,num+1-y):
				# Check if the rect is used and the space is available
				if (not check[width-1][height-1] and canFill(num,x,y,width,height)):
					# copies of areas
					minAreaCopy=minArea
					maxAreaCopy=maxArea
					# Computes min/max area
					area = width*height
					minArea = min(minArea,area)
					maxArea = max(maxArea,area)
					# if still better diff continue making mondrian
					if maxArea-minArea < minDiff:
						# create mondrian
						fillSection(num,x,y,width,height,index)
						xNew, yNew = nextLoc(num,x,y)
						mondrian(num,xNew,yNew,index+1)
						unfillSection(num,x,y,width,height)
					# reset areas
					minArea=minAreaCopy
					maxArea=maxAreaCopy

initCheckAndGrid(SIZE)
mondrian(SIZE,0,0,1)
printGrid(ans)

# DRAW IMAGES
import numpy as np
import matplotlib.pyplot as plt
import time

bufferWidth=10
blockWidth=80
numPixels=100
imageSize=SIZE*(blockWidth+bufferWidth)+bufferWidth

fig = plt.figure(figsize=(imageSize/100.0,imageSize/100.0))
Z = np.empty([imageSize, imageSize], dtype=float)

# Grid Inside
for i in range(SIZE):
	for j in range(SIZE):
		Z[(blockWidth+bufferWidth)*i+bufferWidth:(blockWidth+bufferWidth)*(i+1),
			(blockWidth+bufferWidth)*j+bufferWidth:(blockWidth+bufferWidth)*(j+1)] = ans[i][j]+SIZE/4

# Grid Border
for i in range(SIZE+1):
	for j in range(SIZE+1):
		Z[(blockWidth+bufferWidth)*i:(blockWidth+bufferWidth)*i+bufferWidth,
			(blockWidth+bufferWidth)*j:(blockWidth+bufferWidth)*j+bufferWidth] = 0

plt.set_cmap("jet")
im = fig.figimage(Z, xo=0, yo=0, origin='lower')

#fig.show()
fig.savefig('mondrian'+str(SIZE)+'.png',figsize=(SIZE*100,SIZE*100))
