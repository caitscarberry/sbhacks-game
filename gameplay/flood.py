from queue import Queue

def connected(board):
    size = len(board)
    visit = [[0] * size for _ in range(size)]

    start = None
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                start = (i, j)
                break
        if start is not None:
            break

    if start is None:
        return False

    check = Queue()
    check.put(start)
    while not check.empty():
        curr = check.get()
        visit[curr[0]][curr[1]] = 1
        to_check = [
            (curr[0] - 1, curr[1]),
            (curr[0] + 1, curr[1]),
            (curr[0], curr[1] - 1),
            (curr[0], curr[1] + 1)
        ]
        for cell in to_check:
            if cell[0] < 0 or cell[0] >= size or cell[1] < 0 or cell[1] >= size:
                continue
            if visit[cell[0]][cell[1]] == 0 and board[cell[0]][cell[1]] != 0:
                check.put(cell)

    for i in range(size):
        for j in range(size):
            if(visit[i][j] != board[i][j]):
                return False
    return True
