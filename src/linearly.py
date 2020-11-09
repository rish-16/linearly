class Matrix(list):
    def __init__(self, array):
        self.mat = array
        
    def get_size(self):
        return (len(self.mat), len(self.mat[0]))
        
    def __add__(self, b):
        err_msg = "Matrices must be of the same sizes. Attempted to operate on matrices of size {} and {}.".format(self.get_size(), b.get_size())
        assert self.get_size() == b.get_size(), err_msg
        
        res = [[None for j in range(len(self.mat[i]))] for i in range(len(self.mat))]
        for i in range(len(b.mat)):
            for j in range(len(b.mat[i])):
                res[i][j] = self.mat[i][j] + b.mat[i][j]
            
        return Matrix(res)
        
    def __sub__(self, b):
        err_msg = "Matrices must be of the same sizes. Attempted to operate on matrices of size {} and {}.".format(self.get_size(), b.get_size())
        assert self.get_size() == b.get_size(), err_msg
        
        res = [[None for j in range(len(self.mat[i]))] for i in range(len(self.mat))]
        for i in range(len(b.mat)):
            for j in range(len(b.mat[i])):
                res[i][j] = self.mat[i][j] - b.mat[i][j]
            
        return Matrix(res)
        
    def dot(self, b):
        err_msg = "Dot product can only work on (n x 1) vectors. Attempted to operate on matrix of size {} and {}".format(self.get_size(), b.get_size())
        assert self.get_size()[1] == 1 and b.get_size()[1] == 1, err_msg
        
        res = sum([self.mat[i][0] * b.mat[i][0] for i in range(len(self.mat[i]))])
        return res
        
    def _dot_mm(self, a, b):
        res = [a[i] * b[i] for i in range(len(a))]
        res = sum(res)
        return res
        
    def __mul__(self, b):
        err_msg = "Dimensions must coincide for Matrix Multiplication. Attempted to operate on matrices of size {} and {}.".format(self.get_size(), b.get_size())
        assert self.get_size()[1] == b.get_size()[0], err_msg
        
        dim1 = self.get_size()[0]
        dim2 = b.get_size()[1]
        res = [[None for j in range(dim2)] for i in range(dim1)]
        
        def column(matrix, i):
            return [row[i] for row in matrix]
        
        for i in range(dim1):
            row = self.mat[i]
            for j in range(dim2):
                col = column(b.mat, j)
                res[i][j] = self._dot_mm(row, col)
        
        return Matrix(res)
                
    def __str__(self):
        final = ""
        for i in range(len(self.mat)):
            row = "\t".join(list(map(str, self.mat[i])))
            final += row
        return "\n".join(final)