import cv2

if __name__ == '__main__':
    PATH = input('Enter name of RGB file: ')
    img = cv2.imread(PATH, -1)
    img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(PATH, img_bw)
