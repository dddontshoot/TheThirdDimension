import json
from lib.matrix import getMatrix

def go(e1,e2):
        #if not e2["x"] == e1["x"] and not e2["y"] == e1["y"]:
        # eliminated connecting to self
        if e2["x"] == e1["x"]-1 and e2["y"]==e1["y"]:
            return(4)
        if e2["x"] == e1["x"]+1 and e2["y"]==e1["y"]:
            return(8)
        if e2["y"] == e1["y"]-1 and e2["x"]==e1["x"]:
            return(2)
        if e2["y"] == e1["y"]+1 and e2["x"]==e1["x"]:
            return(6)
        return(-1)

def checkMatrix(matrix,x,y,connectorShortlist):
        orthagonals=list()
        neighbor1=(getMatrix(matrix,x-1,y))
        neighbor2=(getMatrix(matrix,x+1,y))
        neighbor3=(getMatrix(matrix,x,y-1))
        neighbor4=(getMatrix(matrix,x,y+1))
        if len(neighbor1)>0:
            neighbor1["ortho"]=4
            orthagonals.append(json.dumps(neighbor1))
        if len(neighbor2)>0:
            neighbor2["ortho"]=8
            orthagonals.append(json.dumps(neighbor2))
        if len(neighbor3)>0:
            neighbor3["ortho"]=2
            orthagonals.append(json.dumps(neighbor3))
        if len(neighbor4)>0:
            neighbor4["ortho"]=6
            orthagonals.append(json.dumps(neighbor4))
        return(orthagonals)
