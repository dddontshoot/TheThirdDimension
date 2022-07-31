import json

def buildMatrix(surface):
    print("Building matrix")
    matrix=dict()
    for item in surface:
        entityProperties=json.loads(item)
        entityProperties["x"]=entityProperties["x"]*(-1) # For some reason Blender universe is backwards to everything else.
        if entityProperties["x"] in matrix.keys():
            line=json.loads(matrix[entityProperties["x"]])
            if entityProperties["y"] in line.keys():
                print("duplicate entry in matrix",entityProperties["x"],entityProperties["y"])
            else:
                line[entityProperties["y"]]=json.dumps(entityProperties)
                matrix[entityProperties["x"]]=json.dumps(line)
        else:
            line=dict()
            line[entityProperties["y"]]=json.dumps(entityProperties)
            matrix[entityProperties["x"]]=json.dumps(line)
    return(matrix)


def getMatrix(matrix,x,y):
    fail=dict()
    if x in matrix.keys():
        line=json.loads(matrix[x])
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
    if entity["x"] in matrix.keys():
        # hit! continuing...
        y=json.loads(matrix[entity["x"]])
        if entity["y"] in y:
            # hit! Duplicate found!
            result=True
        else:
            # miss! entity cannot be a duplicate!
            y[entity["y"]]=json.dumps(entity)
            matrix[entity["x"]]=json.dumps(y)
    else:
        # miss! entity cannot be a duplicate!
        y=dict()
        y[entity["y"]]=json.dumps(entity)
        matrix[entity["x"]]=json.dumps(y)
    # print("result=",result)
    return(matrix,result)
