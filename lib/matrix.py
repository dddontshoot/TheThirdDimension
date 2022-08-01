import json

def buildMatrix(surface):
    print("Building matrix")
    matrix=dict()
    for item in surface:
        entityProperties=json.loads(item)
        entityProperties["x"]=entityProperties["x"]*(-1) # For some reason Blender universe is backwards to everything else.
        if str(entityProperties["x"]) in matrix.keys():
            line=json.loads(matrix[str(entityProperties["x"])])
            if str(entityProperties["y"]) in line.keys():
                print("duplicate entry in matrix",entityProperties["x"],entityProperties["y"])
            else:
                line[str(entityProperties["y"])]=json.dumps(entityProperties)
                matrix[str(entityProperties["x"])]=json.dumps(line)
        else:
            line=dict()
            line[str(entityProperties["y"])]=json.dumps(entityProperties)
            matrix[str(entityProperties["x"])]=json.dumps(line)
    return(matrix)


def getMatrix(matrix,x,y):
    fail=dict()
    if str(x) in matrix.keys():
        line=json.loads(matrix[str(x)])
        if str(y) in line.keys():
            cell=json.loads(line[str(y)])
            #print("The matrix has you!")
            return(cell)
        else:
            return(fail)
    else:
        return(fail)

def insert(matrix,entity):
    result=False
    if str(entity["x"]) in matrix.keys():
        # hit! continuing...
        y=json.loads(matrix[str(entity["x"])])
        if str(entity["y"]) in y.keys():
            # hit! Duplicate found!
            result=True
        else:
            # miss! entity cannot be a duplicate!")
            y[str(entity["y"])]=json.dumps(entity)
            matrix[str(entity["x"])]=json.dumps(y)
    else:
        # miss! entity cannot be a duplicate!
        y=dict()
        y[str(entity["y"])]=json.dumps(entity)
        matrix[str(entity["x"])]=json.dumps(y)
    # print("result=",result)
    return(matrix,result)
