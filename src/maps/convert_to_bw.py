import cv2

PATH = 'OBSTACLES.png'

if __name__ == '__main__':
    img = cv2.imread(PATH, -1)
    img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(PATH, img_bw)
