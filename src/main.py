from linearly import Matrix

a = Matrix([
    [1, 0, 4, 0, 0, 5],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 1, 4],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

print (a.is_RREF())