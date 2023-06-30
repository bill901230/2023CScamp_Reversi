direct = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]


def isOnBoard(x, y):
    """
    --------------------------------------------------------
    #### 功能 : 判斷輸入的x、y值的位置是否在棋盤上
    --------------------------------------------------------
    #### 參數
    - x : 棋盤的x軸座標
    - y : 棋盤的y軸座標
    --------------------------------------------------------
    #### 回傳值
    - 如果(x, y)在棋盤範圍內, 回傳True ; 否則回傳False
    --------------------------------------------------------
    """
    return 7 >= x and x >= 0 and 7 >= y and y >= 0


def isValidMove(board, side, x, y):
    """
    --------------------------------------------------------
    #### 功能 : 判斷黑或白棋能否下在棋盤的(x, y)處
    --------------------------------------------------------
    #### 參數
    - board : 棋盤
    - side : 棋子顏色
    - x : 棋盤的x軸座標
    - y : 棋盤的y軸座標
    --------------------------------------------------------
    #### 回傳值
    - 如果棋子能下在(x, y), 回傳True ; 否則回傳False
    --------------------------------------------------------
    """
    if not isOnBoard(x, y) or board[x][y] != "none" or len(getFlipDisks(board, side, x, y)) == 0:
        return False
    return True


def getValidMoves(board, side):
    """
    --------------------------------------------------------
    #### 功能 : 獲得可以下的所有位置
    --------------------------------------------------------
    #### 參數
    - board : 棋盤
    - side : 棋子顏色
    --------------------------------------------------------
    #### 回傳值
    - 回傳所有可以下的位置 (資料型態 : 二維陣列)
    --------------------------------------------------------
    """
    valid = []
    for x in range(8):
        for y in range(8):
            """
            Q1. 將以下判斷式中的"?"替換成某個function
            Todo : 判斷(x, y)的位置是否可以下
            Hint : 使用前面提過的函式
                    1. isOnBoard -> 可判斷輸入的x、y值的位置是否在棋盤上
                    2. isValidMove -> 判斷黑或白棋能否下在棋盤的(x, y)處
            """
            if "__fill_in__":
                valid.append([x, y])
    return valid


def getScore(board):
    """
    --------------------------------------------------------
    #### 功能 : 計算棋盤上黑棋和白棋的數量
    --------------------------------------------------------
    #### 參數
    - board : 棋盤
    --------------------------------------------------------
    #### 回傳值
    - 黑棋和白棋的分數 (資料型態 : 字典)
    --------------------------------------------------------
    """
    bscore = 0  # 黑棋分數
    wscore = 0  # 白棋分數
    for x in range(8):
        for y in range(8):
            if board[x][y] == "black":  # 黑棋分數+1
                bscore += 1
            elif board[x][y] == "white":  # 白棋分數+1
                wscore += 1
    return {"black": bscore, "white": wscore}


def getFlipDisks(board, side, xstart, ystart):
    """
    --------------------------------------------------------
    #### 功能 : 找到哪些棋子要被翻轉
    --------------------------------------------------------
    #### 參數
    - board : 棋盤
    - side : 棋子顏色
    - xstart : 棋盤的x軸座標
    - ystart : 棋盤的y軸座標
    --------------------------------------------------------
    #### 回傳值
    - 回傳所有會被翻轉的棋子的位置 (資料型態 : 二維陣列)
    --------------------------------------------------------
    """
    board[xstart][ystart] = side
    otherside = "white"
    if side == "white":
        otherside = "black"
    flipped_disks = []

    # 從(xstart, ystart)往8個方位找要被翻轉的棋子
    for xdirect, ydirect in direct:
        x, y = xstart + xdirect, ystart + ydirect
        temp = []
        while isOnBoard(x, y) and board[x][y] != "none":
            if board[x][y] == otherside:  # 如果找到的棋子顏色是對方的，繼續往下找
                """
                Q2. 將底下的pass改成正確答案
                Todo : 如果找到的棋子顏色是對方的，把棋子的位置存下來並繼續往下找
                Hint :
                1. 將x和y用陣列的形式儲存在temp陣列中
                2. x和y繼續分別往xdirect和ydirect找
                """
                # Q2 begin your code here
                pass
                # Q2 end your code

            elif board[x][y] == side:  # 如果找到的棋子顏色是我方的，停止往下找
                flipped_disks += temp
                break
    board[xstart][ystart] = "none"
    return flipped_disks


def flip(board, side, xstart, ystart):
    """
    --------------------------------------------------------
    #### 功能 : 翻轉棋子
    --------------------------------------------------------
    #### 參數
    - board : 棋盤
    - side : 棋子顏色
    - xstart : 棋盤的x軸座標
    - ystart : 棋盤的y軸座標
    --------------------------------------------------------
    #### 回傳值
    - 無
    --------------------------------------------------------
    """
    # 程式碼開始處
    """
    Q3. 將下面的"?"替換成某個function
    Todo : 取得要被翻轉的棋子
    Hint : 使用前面提到過的函式
            1. isOnBoard -> 可判斷輸入的x、y值的位置是否在棋盤上
            2. isValidMove -> 判斷黑或白棋能否下在棋盤的(x, y)處
            3. getValidMove -> 獲得可以下的所有位置
            4. getScore -> 計算棋盤上黑棋和白棋的數量
            5. getFlipDisk -> 找到哪些棋子會被翻轉
    """
    disks = "__fill_in__"
    board[xstart][ystart] = side  # 在(xstart, ystart)的地方下棋

    # 翻轉棋子顏色
    for x, y in disks:
        board[x][y] = side


def noMoreMove(board):
    """
    --------------------------------------------------------
    #### 功能 : 判斷棋局是否結束
    --------------------------------------------------------
    #### 參數
    - board : 棋盤
    --------------------------------------------------------
    #### 回傳值
    - 若遊戲結束, 回傳True ; 否則回傳False
    --------------------------------------------------------
    """
    return not getValidMoves(board, "white") and not getValidMoves(board, "black")


def getBoardCopy(board):
    """
    --------------------------------------------------------
    #### 功能 : 複製一個8*8一模一樣的棋盤
    --------------------------------------------------------
    #### 參數
    - board : 棋盤
    --------------------------------------------------------
    #### 回傳值
    - 回傳複製後的8*8棋盤
    --------------------------------------------------------
    """
    copied = []
    for _ in range(8):
        copied.append(["none"] * 8)
    for x in range(8):
        for y in range(8):
            copied[x][y] = board[x][y]
    return copied
