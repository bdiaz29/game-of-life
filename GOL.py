import numpy as np
import random
import time
import cv2

dimensional = 100


def track(board):
    global dimensional
    return_track = np.zeros((dimensional, dimensional), dtype=int)
    for i in range(dimensional):
        for j in range(dimensional):
            xmin = max(0, j - 1)
            ymin = max(0, i - 1)
            xmax = min(dimensional - 1, j + 1)
            ymax = min(dimensional - 1, i + 1)
            chunk = np.uint8(board[ymin:ymax + 1, xmin:xmax + 1])
            return_track[i, j] = np.sum(chunk) - int(board[i, j])
    return return_track


def update(board):
    global dimensional
    neighbor_track = track(board)
    board_copy = np.zeros((dimensional, dimensional), dtype=bool)
    for i in range(dimensional):
        for j in range(dimensional):
            temp = neighbor_track[i, j]
            if board[i, j]:
                if temp == 3 or temp == 2:
                    board_copy[i, j] = True
                else:
                    board_copy[i, j] = False
            else:
                if temp == 3:
                    board_copy[i, j] = True
                else:
                    board_copy[i, j] = False
    return board_copy


# initialize board
board = np.zeros((dimensional, dimensional), dtype=bool)
for i in range(dimensional):
    for j in range(dimensional):
        chance = random.randint(0, 100)
        if chance < 50:
            board[i, j] = True

while (True):
    full_image = np.uint8(board * 255)
    dim = dimensional * 5
    full_image = cv2.resize(full_image, (dim, dim), interpolation=cv2.INTER_NEAREST)
    cv2.imshow('window', full_image)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    board = update(board)
