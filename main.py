import cv2
import kociemba

stickers_position = {
    'crosshair': [
        [200, 120], [300, 120], [400, 120],
        [200, 220], [300, 220], [400, 220],
        [200, 320], [300, 320], [400, 320]
    ],
    'preview': [
        [20, 20], [54, 20], [88, 20],
        [20, 54], [54, 54], [88, 54],
        [20, 88], [54, 88], [88, 88]
    ]
}

color = {
    'red': (0, 0, 255),
    'orange': (0, 165, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'white': (255, 255, 255),
    'yellow': (0, 255, 255)
}

check_state = []
solution = []
solved = False


def draw_stickers(frame, stickers, name):
    for x, y in stickers[name]:
        cv2.rectangle(frame, (x, y), (x + 30, y + 30), (255, 255, 255), 2)


def color_detect(h, s, v):
    if (h <= 10 or h >= 170) and s >= 100 and v >= 100:
        return 'red'
    elif h <= 25 and s >= 100 and v >= 100:
        return 'orange'
    elif h <= 35 and s >= 100 and v >= 100:
        return 'yellow'
    elif h <= 80 and s >= 100 and v >= 100:
        return 'green'
    elif h <= 130 and s >= 100 and v >= 100:
        return 'blue'
    elif s <= 25 and v >= 200:
        return 'white'
    return 'white'


state = {
    'up': ['white'] * 9,
    'right': ['white'] * 9,
    'front': ['white'] * 9,
    'down': ['white'] * 9,
    'left': ['white'] * 9,
    'back': ['white'] * 9,
}

sign_conv = {
    'green': 'F',
    'white': 'U',
    'blue': 'B',
    'red': 'R',
    'orange': 'L',
    'yellow': 'D'
}


def solve(faces):
    raw = ''
    for i in faces:
        for j in faces[i]:
            raw += sign_conv[j]
    print('Answer: ', kociemba.solve(raw))
    return kociemba.solve(raw)


def main():
    # Open the default camera
    cap = cv2.VideoCapture(0)

    while True:
        hsv = []
        current_state = []

        # Capture frame-by-frame
        ret, img = cap.read()
        # img = cv2.flip(img, 1)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Draw the crosshair and preview
        draw_stickers(img, stickers_position, 'crosshair')
        draw_stickers(img, stickers_position, 'preview')

        for i in range(9):
            hsv.append(frame[stickers_position['crosshair'][i][1] + 10][stickers_position['crosshair'][i][0] + 10])

        a = 0
        for x, y in stickers_position['preview']:
            color_name = color_detect(hsv[a][0], hsv[a][1], hsv[a][2])
            cv2.rectangle(img, (x, y), (x + 30, y + 30), color[color_name], -1)
            a += 1
            current_state.append(color_name)

        # Append new state on key press and try to solve
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k == ord('u'):
            state['up'] = current_state
            print('up: ' + str(current_state))
            check_state.append('u')
        elif k == ord('r'):
            check_state.append('r')
            print('right: ' + str(current_state))
            state['right'] = current_state
        elif k == ord('l'):
            check_state.append('l')
            print('left: ' + str(current_state))
            state['left'] = current_state
        elif k == ord('d'):
            check_state.append('d')
            print('down: ' + str(current_state))
            state['down'] = current_state
        elif k == ord('f'):
            check_state.append('f')
            print('front: ' + str(current_state))
            state['front'] = current_state
        elif k == ord('b'):
            check_state.append('b')
            print('back: ' + str(current_state))
            state['back'] = current_state
        elif k == ord('\r'):
            if len(set(check_state)) == 6:
                try:
                    solve(state)
                except ValueError:
                    print('Error in side detection. Invalid configuration.')
            else:
                print('Incomplete scan.')
                print('Sides left to scan: ' + str(6 - len(set(check_state))) + '.')

        # Display the resulting frame
        cv2.imshow('Rubik\'s Cube Solver (c) Vlad Ursache', img)

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
