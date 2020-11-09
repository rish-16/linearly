class Matrix(list):
    def __init__(self, array):
        self.mat = array
        
    def get_size(self):
        return (len(self.mat), len(self.mat[0]))
        
    def __add__(self, b):
        assert self.get_size() == b.get_size(), "Matrices must be of the same sizes. Attempted to add matrices of size {} and {}".format(self.get_size(), b.get_size())
        
        res = [[None for j in range(len(self.mat[i]))] for i in range(len(self.mat))]
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                print ("mat: {}".format(self.mat[i][j]))
                print ("b: {}".format(b[i][j]))
                res[i][j] = self.mat[i][j] + b[i][j]
            
        return res
                
    def __str__(self):
        final = ["["]
        for i in range(len(self.mat)):
            row = self.mat[i]
            final.append(repr(row))
        final.append("]")
        return "\n".join(final) + "\n"