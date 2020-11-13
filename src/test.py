from linearly import Matrix, GaussJordanSolver

a = Matrix([
            [1],
            [2],
            [3]
        ])
        
b = Matrix([
            [1, 2, 3]
        ])
        
gjs = GaussJordanSolver(a)