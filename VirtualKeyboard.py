import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
cap.set(10, 200)

detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M", " "]]
finalText = ""      # for displaying the final text on the screen

keyboard = Controller()


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []             # appending the keys
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    img = drawAll(img, buttonList)

    lmList1 = []
    lmList2 = []

    if hands:
        hands1 = hands[0]
        lmList1 = hands1["lmList"]
        bbox1 = hands1["bbox"]

    if lmList1:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (80, 80, 80), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)
                print(l)

                if l<30:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (255, 255, 255), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_COMPLEX, 4, (255, 255, 255), 4)
                    finalText +=button.text


    cv2.rectangle(img, (50, 350), (700, 450), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, (0, 0, 0), 5)

    cv2.imshow("output", img)
    cv2.waitKey(1)
