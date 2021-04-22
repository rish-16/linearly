from collections import deque
import random, copy

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

class GJState:
    def __init__(self, state):
        self.state = state

    def ero_type_1(self, i, k):
        """
        Type 1 ERO: non-zero scalar multiplication
        """
        self.state.mat[i] = [k * self.state.mat[i][j] for j in range(len(self.state.mat[i]))]
        
    def ero_type_2(self, i, j):
        """
        Type 2 ERO: row swapping
        """
        temp = self.state.mat[i]
        self.state.mat[i] = self.state.mat[j]
        self.state.mat[j] = temp
        
    def ero_type_3(self, i, j, k):
        """
        Type 3 ERO: addition of scalar multiple of row
        """
        self.state.mat[i] = [self.state.mat[i] + (k * self.state.mat[j][p]) for p in range(len(self.state.mat[j]))]        

    def get_children(self):
        children = []

        ORIGINAL = copy.deepcopy(self.state)

        dim1 = self.state.get_size()[0]
        dim2 = self.state.get_size()[1]

        i, j = random.randint(0, dim1), random.randint(0, dim1)
        while (i == j):
            i, j = random.randint(0, dim1), random.randint(0, dim1)

        ero1 = self.ero_type_1(i, j)
        children.append(ero1)

        self.state = ORIGINAL
        

        return children

        
class GaussJordonSolver:
    def __init__(self, mat):
        self.mat = mat

    def get_nonzero_row_count(self):
        dim1 = self.mat.get_size()[0]
        dim2 = self.mat.get_size()[1]

        nz_count = 0 # number of non zero rows
        for r in range(dim1):
            row = self.mat.get_row(r)
            if (row != [0 for _ in range(dim2)]):
                nz_count += 1

        return nz_count
        
    def is_RREF(self):
        '''
        Checks if a given matrix is in RREF. Conditions for RREF:

        1. First leading entry for all rows must be 1
        2. Leading entries should be shifted further right for every row down
        3. Any leading entry must be the only non-zero element in its column
        4. Any zero rows are placed at the bottom

        Returns True if matrix is in RREF, False otherwise

        [ 1 0 a 0 0 | b ]
        [ 0 1 c 0 0 | d ]
        [ 0 0 0 1 1 | e ]
        [ 0 0 0 0 0 | 0 ]
        '''

        dim1 = self.mat.get_size()[0]
        dim2 = self.mat.get_size()[1]

        def _check_leading_entries():
            prev_le_idx = -1 # index of leading 1 per row
            le_idx = []

            new_dim1 = self.get_nonzero_row_count()

            for r in range(new_dim1):
                cur_le_idx = 0
                row = self.mat.get_row(r)

                if (row != [0 for _ in range(dim2)]):
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
            [le_res, le_idxs] = _check_leading_entries()
            
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
                return self.mat.get_row(0) != [0 for _ in range(dim2)]
            if (dim1 > 1):
                # 0 or more zero rows
                n_zero_rows = 0
                
                for r in range(dim1):
                    row = self.mat.get_row(r)
                    if (row == [0 for _ in range(dim2)]):
                        n_zero_rows += 1

                n_zero_rows_back = 0
                for r in range(dim1-1, n_zero_rows-1, -1):
                    row = self.mat.get_row(r)
                    if (row == [0 for _ in range(dim2)]):
                        n_zero_rows_back += 1

                '''
                If zero rows are stacked at the bottom, the number of zero rows
                from the bottom will be equal to the total number of zero rows
                '''
                return n_zero_rows == n_zero_rows_back

        def check_aug_col():
            aug_col = self.mat.get_col(self.mat.mat, dim2-1)
            n_non_zero_rows = self.get_nonzero_row_count()
            
            # check each row for inconsistency (zeros with non-zero augmentation)
            for r in range(n_non_zero_rows-1, dim1):
                row = self.mat.get_row(r)
                aug_element = row[-1]
                prefix = row[:dim2-1]

                if (prefix == [0 for _ in range(dim2-1)]) and aug_element != 0:
                    return False

            return True

        return check_zero_rows() and check_cols() and check_aug_col()

    def solve(self, solve_limit=200):
        '''
        Treats the Gauss-Jordan Elimination process as Graph Theory problem.
        Performs Breadth First Search (BFS) on all possible states until one
        with the appropriate RREF representation is encountered. Graph nodes 
        represent the state of the matrix after the Elementary Row Ops have been
        performed on it. Edges are unweighted state transitions between matrices.

        Returns the RREF matrix for a given matrix if it exists.

        If not solvable within `stop_limit` steps, stop the process.
        '''
        visited = dict()
        start_node = GJState(self)
        visited[start_node] = True
        STEPS = 0

        frontier = deque()
        frontier.append(start_node)

        while (not len(frontier) == 0 and STEPS <= solve_limit):
            new_state = frontier.popleft()

            if (new_state.state.is_RREF()):
                return new_state.state

            for child_state in new_state.get_children(): # all possible EROs applied to current state
                if (not visited.has_key(child_state)):
                    visited[child_state] = True
                    STEPS += 1
                    frontier.append(child_state)