"""
Your task is to find which diagonal is "larger": which diagonal has a bigger sum of their elements.

    If the principal diagonal is larger, return "Principal Diagonal win!"
    If the secondary diagonal is larger, return "Secondary Diagonal win!"
    If they are equal, return "Draw!"
"""


def compare_diagonal(matrix):
    if any(len(matrix) != len(matrix[i]) for i in range(len(matrix))):
        raise ValueError('Matrices must be the same dimension')

    principal_diagonal_sum = sum([matrix[i][i] for i in range(len(matrix))])
    secondary_diagonal_sum = sum([matrix[i][len(matrix) - 1 - i] for i in range(len(matrix))])

    if principal_diagonal_sum > secondary_diagonal_sum:
        answer = 'Principal diagonal win!'
    elif principal_diagonal_sum < secondary_diagonal_sum:
        answer = 'Secondary diagonal win!'
    else:
        answer = 'Draw!'
    return answer
