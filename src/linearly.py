class Matrix(list):
    def __init__(self, mat):
        """
        mat: 2-dimensional array representing matrix of size m x n
        """
        self.mat = mat
        
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
        
    def _dot(self, a, b):
        n_cols = len(a)
        n_rows = len(b)
        
        assert n_cols == n_rows, "Dimensions do not match for dot product. Operating on vectors of size {} and {}".format(n_cols, n_rows)
        return sum([a[i] * b[i] for i in range(n_cols)])
        
    def __mul__(self, b):
        err_msg = "Dim[1] and Dim[0] must be the same for multiplication. Attempted to operate on matrices of size {} and {}.".format(self.get_size(), b.get_size())
        assert self.get_size()[1] == b.get_size()[0], err_msg
        
        dim1 = self.get_size()[0]
        dim2 = b.get_size()[1]
        
        def get_col(arr, i):
            return [row[i] for row in arr]
            
        res = [[None for j in range(dim2)] for i in range(dim1)]
        
        for i in range(dim1):
            for j in range(dim2):
                res[i][j] = self._dot(self.mat[i], get_col(b.mat, j))
                
        return Matrix(res)
        
    def __pow__(self, m):
        """
        Only supports integer powers
        """
        cur = self
        for i in range(m-1):
            cur  = cur * self
        return cur
                
    def __str__(self):
        final = []
        for i in range(len(self.mat)):
            final.append(repr(self.mat[i]))
        return "\n".join(final)