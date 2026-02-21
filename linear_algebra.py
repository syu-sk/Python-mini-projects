from collections import defaultdict
import math
import sympy as sp
def print_matrix(matrix):
    try:
        for row in matrix:
            print(row)
    except:
        print('Invalid Format')
def pivot_position(row):
    if all(element == 0 for element in row):
        return -1
    pos = 0
    for i in row:
        if i != 0: break
        pos += 1
    return pos
def replace(ref_row, target_row):
    pivot = pivot_position(ref_row)     #important to take pivot for reference row.
    k = (-1)*(target_row[pivot] / ref_row[pivot])
    for i in range(len(ref_row)):
        target_row[i] += k*ref_row[i]
    return target_row
def scale(row, normalise=False):
    if normalise:
        k = 1/row[pivot_position(row)]
        for i in range(len(row)):
            row[i] *= k
        return row
def magnitude(vector):
    return sum([i**2 for i in vector])**0.5
def dot(left, right):
    if len(left) != len(right):
        raise TypeError(f'Invalid dot product between different length vectors {left} and {right}')
    return sum([left[i] * right[i] for i in range(len(left))])
def vector_sum(vectors):
    for i in vectors[1:]:
        if len(i) != len(vectors[0]):
            raise TypeError(f'Cannot add different length vector {i}')
    result_vector = [0 for i in vectors[0]]
    for i in range(len(vectors)):
        for element in range(len(vectors[0])):
            result_vector[element] += vectors[i][element]
    return result_vector
def projection(vector, basis, single=True):
    coefficients = []
    for v in range(len(basis)):
        coefficients.append(round(dot(vector,basis[v]) / magnitude(basis[v])**2,2))
    if not single:
        return list(zip(coefficients, basis))
    for v in range(len(basis)):
        for element in range(len(basis[0])):
            basis[v][element] *= coefficients[v]
    print(basis)
    return vector_sum(basis)
print(projection([1,2,3],[[1,1,0],[1,0,1]]))


def echelon(matrix, reduced=False, show=False):
    '''
    Docstring for echelon
    
    :param matrix: Input matrix, list of lists
    :param reduced: Returns reduced echelon form, Boolean value.
    '''

    # sorting
    result_dict = dict()
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            if pivot_position(matrix[row]) == col:
                result_dict['R' + str(row)] = matrix[row]
    for row in range(len(matrix)):  #catch any additional zero rows, since pivot_position would return -1
        if all(element == 0 for element in matrix[row]):
            result_dict['R' + str(row)] = matrix[row]
    rows = list(result_dict.keys())
    result_matrix = list(result_dict.values())
    print(f'Sorting complete...\nRow Order: {rows}')
    print(f'Sorted Matrix:')
    print_matrix(result_matrix)
    #by this point, matrix should be sorted in ascending depth of pivot

    #hence, first row to have the lowest index pivot
    column = 0
    for i in range(len(result_matrix)-1):
        pivot_pos = pivot_position(result_matrix[i])
        #try finding next nearest pivot -- steps ascending columns to find nonzero values. if there is, swap with immediate next row
        for col in range(column, pivot_pos):
            for row in range(i+1,len(result_matrix)):
                if result_matrix[row][col] != 0:
                    pivot_pos = col
                    result_matrix[i], result_matrix[row] = result_matrix[row], result_matrix[i]
                    print(f'Optimisation Interchange: R{i+1} <-> R{row+1}, for a lower pivot of [{pivot_pos}]')
                    if show: print(result_matrix)
        for j in range(i+1, len(result_matrix)):
            if result_matrix[j][pivot_pos] != 0:
                result_matrix[j] = replace(result_matrix[i], result_matrix[j])
                print(f'Replacement: R{i+1} on R{j+1}')
                if show: print(result_matrix)
    
    def reduce(matrix):
        for i in range(-1, (-1)*len(matrix)-1, -1):   #step 1 by 1 backwards from the end
            if all(element == 0 for element in matrix[i]):
                continue
            matrix[i] = scale(matrix[i], normalise=True)
            rref_pivot = pivot_position(matrix[i])
            for j in range(i-1, (-1)*len(matrix)-1, -1):
                if matrix[j][rref_pivot] != 0:
                    matrix[j] = replace(matrix[i], matrix[j])
                    print(f'[RREF] Replacement: R{i+len(matrix)+1} on R{j+len(matrix)+1}')
                    if show: print(matrix)
        return matrix
    if reduced:
        result_matrix = reduce(result_matrix)
    #cleaning up
    for row in result_matrix:
        for i in range(len(row)):
            row[i] = round(row[i],2)
    return result_matrix

# print_matrix(echelon([
#     [3,2,-4,3],
#     [2,3,3,15],
#     [5,-3,1,14]
#     ], reduced=True, show=True))

def transpose(matrix):
    result_matrix = [[] for i in matrix[0]] #no. of rows in transpose = length of rows in original
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            result_matrix[j].append(matrix[i][j])
    return result_matrix

# print_matrix(transpose([
#     [1,2,3,4],
#     [5,6,7,8],
#     [9,10,11,12]
#     ]))

def inverse(matrix):
    if len(matrix) != len(matrix[0]):
        return None
    identity = [[0 for i in matrix[0]] for i in matrix]
    for i in range(len(matrix)):
        identity[i][i] = 1
    augmented = matrix
    for i in range(len(matrix)):
        augmented[i] += identity[i]
    
    rref = echelon(augmented, reduced=True)
    test = [i[:3] for i in rref]
    if test != identity:
        raise TypeError('Matrix has no inverse.')
    inv = [row[(-1)*len(matrix):] for row in rref]
    return inv

# print_matrix(inverse([
#     [1,2,3],
#     [4,5,6],
#     [7,8,9]
# ]))

def det(matrix):
    if len(matrix[0]) == len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    
    #optimisation -- reduce recursion
    def zero_count(row):
        count=0
        for i in row:
            if i == 0:
                count += 1
        return count
    zero_row = None
    for num in range(len(matrix[0]),-1,-1):
        for row in range(len(matrix)):
            if zero_count(matrix[row]) == num:
                zero_row = row
                break
        if zero_row:
            break
    print(f'Zero Row obtained: [{zero_row}]')
    
    #matrix creation
    def matrix_shrinker(matrix, exclude_row, exclude_col):
        result_matrix = [[] for i in range(len(matrix)-1)]
        result_row = 0
        for row in range(len(matrix)):
            if row == exclude_row:
                continue
            result_matrix[result_row] = matrix[row][:exclude_col] + matrix[row][exclude_col+1:]
            result_row += 1
            #otherwise, index error caused when entering last row. only add upon finishing a row (excluded on not included)
        print_matrix(result_matrix)
        return result_matrix
    
    #computing determinant
    determinant = 0
    for col in range(1,len(matrix[0])+1):
        #THIS COL IS OFFSET BY 1 -- odd numbered columns are positive
        if matrix[zero_row][col-1] == 0:    #optimisation
            print('Coefficient = 0. Skipping evaluation...')
            continue
        det_component = det(matrix_shrinker(matrix,zero_row,col-1))
        product = matrix[zero_row][col-1]*det_component
        #if even, positive. if odd, negative.
        if (zero_row+1+col)%2==0:
            determinant += product
        else:
            determinant -= product
    return determinant
    
# print(det([
#     [0,1,2,1],
#     [1,0,3,0],
#     [2,1,0,2],
#     [1,1,1,1]
# ]))

def matrix_product(left,right):
    if len(left[0]) != len(right):
        return None
    result_matrix = [[] for i in left] #no. of rows = no. of rows on left. no. of columns = no. of columns on right.
    for row in range(len(left)):
        for column in range(len(right[0])):
            col = [i[column] for i in right]
            element = sum([math.prod(i) for i in zip(left[row],col)])
            result_matrix[row].append(element)
    return result_matrix

# print_matrix(matrix_product([
#     [1,2,3],
#     [4,5,6],
#     [7,8,9]
# ],[
#     [1,4],
#     [2,5],
#     [3,6]
#     ]))

def matrix_equation_solver(A, b):   #to solve Ax = b. b is just a list.
    if len(b) != len(A):
        return None
    augmented = [A[i] + [b[i]] for i in range(len(A))]
    rref = echelon(augmented, reduced=True, show=True)
    print_matrix(rref)

    ### solver algorithm
    #first -- get dictionary of all columns, assigning non-pivots to free variables first.
    #second -- for each row from back to front, start solving for variables
    def solver(matrix):
        x = dict()
        for col in range(len(rref[0][:-1])):
            x[col] = sp.symbols('x'+str(col+1))   #create free variable -- sympy module
        for row in rref:
            pivot = pivot_position(row[:-1])    #constant no count
            if pivot != -1:
                x[pivot] = None
        print(x)
        order = matrix[::-1]
        for row in order:
            if all(element==0 for element in row[:-1]) and row[-1] != 0:
                raise ZeroDivisionError('Inconsistent Matrix')
            elif all(element==0 for element in row):
                continue
            value = row[-1]
            for col in range(len(row)):
                if row[col] == 0:
                    continue
                for num in range(col+1,len(row)-1):
                    value -= row[num]*x[num]  #coefficient * x-value
                break
            x[col] = value  #finally, fix x[col]'s value. could place this before the break as well.
        return list(x.values())
    return solver(rref)

# print(matrix_equation_solver([
#     [1,2],
#     [3,4],
#     [5,6]
# ],
#     [5,11,17]
# ))

def basis_dimension(basis):
    #basis - list of column vectors
    matrix = [[] for i in basis[0]]
    for vector in range(len(basis)):
        for element in range(len(basis[0])):
            matrix[element].append(basis[vector][element])
    ech = echelon(matrix)   #non-reduced for optimisation
    pivots = set()
    for row in ech:
        pivot = pivot_position(row)
        if pivot != -1:
            pivots.add(pivot)
    return len(pivots)

#print(basis_dimension([[1,0,0],[2,0,0],[3,0,0]]))

def transition_matrix(S,T):
    if len(S) != len(T) or len(S[0]) != len(T[0]):
        raise TypeError('S and T are not of the same dimension/space!')
    augmented = [S[i] + T[i] for i in range(len(S))]
    print(augmented)

    identity = [[0 for i in S[0]] for i in S[0]]
    for i in range(len(S[0])):
        identity[i][i] = 1
    print(identity)
    rref = echelon(augmented, reduced=True)
    if [i[:len(S[0])] for i in rref[:len(S[0])]] != identity:   #S basis validity test
        raise TypeError('Invalid Basis S!')
    
    #return top right P
    return [i[len(S[0]):] for i in rref[:len(S[0])]]

#print(transition_matrix([[1,1,1],[0,1,1],[0,0,1]],[[1,0,0],[2,1,0],[1,1,1]]))

def evaluate(A):
    rref = echelon(A, reduced=True)
    pivots = set()
    for row in rref:
        if pivot_position(row) != -1:
            pivots.add(pivot_position(row))
    space = len(A)
    rank = len(pivots)
    nullity = len(A[0]) - rank
    print(f'Space: R{space}\nRank: {rank}\nNullity: {nullity}')

def gramschmidt(S):
    pass

print_matrix(echelon([[3,0,3,0,3],[0,3,1,2,4],[3,1,4,0,-9],[0,2,0,2,2]],reduced=True,show=True))