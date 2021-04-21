from linearly import Matrix

class Tester:
    def test(self, actual, exp):
        if actual != exp:
            raise Exception("Expected: {} | Actual: {}".format(actual, exp))

tester = Tester()

def test1(name):
    a = Matrix([
                [1],
                [2],
                [3]
            ])
            
    b = Matrix([
                [1],
                [2],
                [3]
            ])

    c = Matrix([
        [1, 2, 3]
    ])

    # reflexivity
    tester.test(a == a, True)
    tester.test(b == b, True)
    
    # symmetry & transitivity
    tester.test(a == b, True)
    tester.test(b == a, True)
    tester.test(b == c, False)
    tester.test(c == b, False)
    tester.test(a == c, False)
    tester.test(c == a, False)

    print ("{} passed.".format(name))

def test2(name):
    a = Matrix([
                [1],
                [2],
                [3]
            ])
            
    b = Matrix([
                [1],
                [2],
                [3]
            ])

    c = Matrix([
        [1, 2, 3]
    ])

    res_axc = Matrix([
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9]
    ])
    
    res_bxc = Matrix([
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9]
    ])

    tester.test(a * c, res_axc)
    tester.test(b * c, res_bxc)

    print ("{} passed.".format(name))

test1("Equality Test")
test2("Matmul Test")