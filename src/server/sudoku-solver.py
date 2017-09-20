import cplex
import sys
import json

def main():
    """
    command line argument: 81-length characters representing a sudoku table
    like 01800...42803, left-to-right, top-to-bottom and row-by-row where 0 is a blank cell
    """
    if len(sys.argv) == 1 or len(sys.argv[1]) != 9 * 9:
        print("nope")
        return
    table = [int(c) for c in sys.argv[1]]
    table = [table[i * 9:i * 9 + 9] for i in range(9)]  # now table is a 9*9 matrix
    result = solve(table)
    print(json.dumps(result))

def solve(table):
    def v(i, j, k):
        """ return the variable index for row i, column j, number k
        """
        return i * 9 * 9 + j * 9 + k - 1

    vcount = 9 * 9 * 9
    variables = {
        "obj": [1.0] * vcount,                      # coefficients of the obj func
        "types": "B" * vcount,                      # variable types (integer or continuous)
                                                    #   specifying types makes the problem a MIP
        "names": ['x{}{}{}'.format(i, j, k) for i in range(9) for j in range(9) for k in range(9)],
    }
    inequal = []
    # cell constraints
    for row in range(9):
        for col in range(9):
            inequal.append([[v(row, col, num) for num in range(1, 10)], [1.0] * 9])
    # row constraints
    for row in range(9):
        for num in range(1, 10):
            inequal.append([[v(row, col, num) for col in range(9)], [1.0] * 9])
    # column constraints
    for col in range(9):
        for num in range(1, 10):
            inequal.append([[v(row, col, num) for row in range(9)], [1.0] * 9])
    # block constraints
    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            for num in range(1, 10):
                inequal.append(
                    [[v(row, col, num) for row in range(block_row, block_row + 3)
                        for col in range(block_col, block_col + 3)],
                    [1.0] * 9])
    # specified cells
    equal = []
    equal_rhs = []
    for row in range(9):
        for col in range(9):
            num = table[row][col]
            if num != 0:
                equal.append([[v(row, col, num)], [1.0]])
                equal_rhs.append(float(num))
    constraints = {
        "lin_expr": inequal + equal,
        "senses": "E" * len(inequal) + "E" * len(equal),
        "rhs": [1.0] * len(inequal) + equal_rhs,
        # "names": ["c1", "c2"],  # row names
    }
    # create a problem instance
    prob = cplex.Cplex()
    prob.set_error_stream(None)
    prob.set_log_stream(None)
    prob.set_results_stream(None)
    prob.set_warning_stream(None)
    # maximize the objective
    prob.objective.set_sense(prob.objective.sense.maximize)
    # add variables and constraints
    prob.variables.add(**variables)
    prob.linear_constraints.add(**constraints)

    prob.write('sudoku.mps')

    # solve!!!
    prob.solve()

    x = prob.solution.get_values()
    result = []
    for row in range(9):
        line = []
        for col in range(9):
            for num in range(1, 10):
                if x[v(row, col, num)] == 1.0:
                    line.append(num)
                    break
        result.append(line)
    
    return result

def printLPSolution(solution):
    print(solution.status[solution.get_status()])
    print("Solution value  = ", solution.get_objective_value())

    slack = solution.get_linear_slacks()
    pi = solution.get_dual_values()
    x = solution.get_values()
    dj = solution.get_reduced_costs()
    numrows = len(slack)
    numcols = len(x)

    for i in range(numrows):
        print("Row %d:  Slack = %10f  Pi = %10f" % (i, slack[i], pi[i]))
    for j in range(numcols):
        print("Column %d:  Value = %10f Reduced cost = %10f" %
              (j, x[j], dj[j]))

def printMIPSolution(solution):
    print(solution.status[solution.get_status()])
    print("Solution value  = ", solution.get_objective_value())

    slack = solution.get_linear_slacks()
    x = solution.get_values()
    numrows = len(slack)
    numcols = len(x)

    for j in range(numrows):
        print("Row %d:  Slack = %10f" % (j, slack[j]))
    for j in range(numcols):
        print("Column %d:  Value = %10f" % (j, x[j]))

if __name__ == "__main__":
    main()
