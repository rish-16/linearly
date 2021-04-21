class Matrix():
    def __init__(self, mat):
        """
        mat: 2-dimensional array representing matrix of size m x n
        """
        self.mat = mat
        
    def get_size(self):
        # get m x n
        return [len(self.mat), len(self.mat[0])]

    def get_entry(self, r, c):
        err_msg = "Coordinates must be within bounds. Given row must be within [0, {}) and given column must be within [0, {})".format(self.get_size()[0], self.get_size()[1])
        assert (r >= 0 and r < self.get_size()[0] and c >= 0 and c < self.get_size()[1]), err_msg

        return self.mat[r][c]
        
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

    def get_row(self, row):
        err_msg = "Coordinate must be within bounds. Given row must be within [0, {}).".format(self.get_size()[0])
        assert (row >= 0 and row < self.get_size()[0]), err_msg

        return self.mat[row]
        
    def get_col(self, arr, i):
        return [row[i] for row in arr]
        
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
            
        res = [[None for j in range(dim2)] for i in range(dim1)]
        
        for i in range(dim1):
            for j in range(dim2):
                res[i][j] = self._dot(self.mat[i], self.get_col(b.mat, j))
                
        return Matrix(res)
        
    def __pow__(self, m):
        """
        Only supports integer powers
        """
        cur = self
        for i in range(m-1):
            cur  = cur * self
        return cur
        
    def transpose(self):
        dim1 = self.get_size()[0]
        dim2 = self.get_size()[1]
        res = [[None for j in range(dim1)] for i in range(dim2)]
        for i in range(dim2):
            for j in range(dim1):
                res[i][j] = self.mat[j][i]
                
        return Matrix(res)
                
    def __str__(self):
        final = []
        for i in range(len(self.mat)):
            final.append(repr(self.mat[i]))
        return "\n".join(final)

    def __eq__(self, value):
        if (value.__eq__(self.mat)): # the object itself
            return True
        elif (isinstance(value, Matrix)):
            dim1 = self.get_size()[0]
            dim2 = self.get_size()[1]

            dim1_v = value.get_size()[0]
            dim2_v = value.get_size()[0]

            # check if dimensions match
            if (dim1 == dim1_v and dim2 == dim2_v):
                # element-wise comparison
                for i in range(dim1):
                    for j in range(dim2):
                        if (self.get_entry(i, j) != value.get_entry(i, j)):
                            return False

                return True

        return False

    def gjsolve(self):
        gjs = GaussJordonSolver(self)
        return gjs.solve()

    def is_RREF(self):
        gjs = GaussJordonSolver(self)
        return gjs.is_RREF()
        
class GaussJordonSolver:
    def __init__(self, mat):
        self.mat = mat
    
    def ero_type_1(self, i, k):
        """
        Type 1 ERO: non-zero scalar multiplication
        """
        self.mat[i] = [k * self.mat[i][j] for j in range(len(self.mat[i]))]
        
    def ero_type_2(self, i, j):
        """
        Type 2 ERO: row swapping
        """
        
        temp = self.mat[i]
        self.mat[i] = self.mat[j]
        self.mat[j] = temp
        
    def ero_type_3(self, i, j, k):
        """
        Type 3 ERO: addition of scalar multiple of row
        """
        self.mat[i] = [self.mat[i] + (k * self.mat[j][p]) for p in range(len(self.mat[j]))]

    def filter_zeros(self):
        return self.mat
        
    def is_RREF(self):
        '''
        Checks if a given matrix is in RREF. Conditions for RREF:

        1. First leading entry for all rows must be 1
        2. Leading entries should be shifted further right for every row down
        3. Any leading entry must be the only non-zero element in its column
        4. Any zero rows are placed at the bottom

        Returns True if matrix is in RREF, False otherwise

        [ 1 0 a 0 | b ]
        [ 0 1 c 0 | d ]
        [ 0 0 0 1 | e ]
        '''

        dim1 = self.mat.get_size()[0]
        dim2 = self.mat.get_size()[1]

        print (self.mat)

        def check_leading_entries():
            prev_le_idx = -1 # index of leading 1 per row

            le_idx = []

            for r in range(dim1):
                cur_le_idx = 0
                row = self.mat.get_row(r)

                if (row != Matrix([0 for _ in range(dim2)])):
                    # check leading entry per row
                    for k in range(len(row)):
                        if row[k] == 1:
                            cur_le_idx = k
                            break
                    
                    if (cur_le_idx < dim2 and cur_le_idx > prev_le_idx):
                        if (sum(row[:cur_le_idx+1]) != 1): # leading zeros
                            return [False, []]
                        else:
                            le_idx.append(cur_le_idx)
                    else:
                        return [False, []]

                    # cache the leading entry index from current row
                    prev_le_idx = cur_le_idx

            return [True, le_idx]

        def check_cols():
            [le_res, le_idxs] = check_leading_entries()
            
            if (le_res):
                for j in range(len(le_idxs)):
                    idx = le_idxs[j]
                    col = self.mat.get_col(self.mat.mat, idx)

                    # leading entry columns should only contain one "1"
                    if (sum(col) != 1):
                        return False

                return True

            return False

        def check_zero_rows():
            if (dim1 == 1):
                return self.mat.get_row(0) != Matrix([0 for _ in range(dim2)])
            if (dim1 > 1):
                # 0 or more zero rows
                n_zero_rows = 0
                
                for r in range(dim1):
                    row = self.mat.get_row(r)
                    if (row == Matrix([0 for _ in range(dim2)])):
                        n_zero_rows += 1

                n_zero_rows_back = 0
                for r in range(dim1, 0, -1):
                    row = self.mat.get_row(r)
                    if (row == Matrix([0 for _ in range(dim2)])):
                        n_zero_rows_back += 1

                '''
                If zero rows are stacked at the bottom, the number of zero rows
                from the bottom will be equal to the total number of zero rows
                '''
                if n_zero_rows == n_zero_rows_back:
                    # remove the zero rows
                    self.mat = self.filter_zeros()
                    return True
                else:
                    return False

        return check_zero_rows() and check_cols()

    def solve(self):
        return True