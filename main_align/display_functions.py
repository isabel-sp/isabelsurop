import cv2

def draw_buttons(img, temp_clicked, snspd, wvguide):
    can_align = not snspd == None and not wvguide == None
    purple = (255,100,170)
    red = (51,51,255)
    blue = (255,128,0)
    green = (0,204,0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    font = cv2.FONT_HERSHEY_COMPLEX

    #clicked
    cv2.rectangle(img, (10, 10), (450, 100), white, -1)
    cv2.rectangle(img, (10, 10), (450, 100), black, 2)
    cv2.rectangle(img, (10, 10), (200, 100), black, -1)
    cv2.putText(img,'Clicked',(40,65), font, 1,white,2)
    if not temp_clicked == None:
        cv2.putText(img, str(temp_clicked), (220, 65), font, 1,black,2)

    #SNSPD
    cv2.rectangle(img, (10, 110), (450, 200), white, -1)
    cv2.rectangle(img, (10, 110), (450, 200), black, 2)
    cv2.rectangle(img, (10, 110), (200, 200), black, -1)
    cv2.putText(img,'SNSPD',(50,165), font, 1,white,2)
    if not snspd == None:
        cv2.putText(img, str(snspd), (220, 165), font, 1,black,2)

    #Waveguide
    cv2.rectangle(img, (10, 210), (450, 300), white, -1)
    cv2.rectangle(img, (10, 210), (450, 300), black, 2)
    cv2.rectangle(img, (10, 210), (200, 300), black, -1)
    cv2.putText(img,'Waveguide',(20,265), font, 1,white,2)
    if not wvguide == None:
        cv2.putText(img, str(wvguide), (220, 265), font, 1,black,2)

    #Align
    if can_align:
        cv2.rectangle(img, (200, 320), (450, 400), white, -1)
        cv2.rectangle(img, (200, 320), (450, 400), black, 5)
        #fill in left or right
        cv2.putText(img, 'Align ' + '(right)', (220, 370), font, 1,black,2)

    #draw dots
    if temp_clicked:
        cv2.circle(img, temp_clicked, radius=2, color=black, thickness=2)
    if wvguide:
        cv2.circle(img, wvguide, radius=2, color=black, thickness=2)
    if snspd:
        cv2.circle(img, snspd, radius=2, color=black, thickness=2)
    return img

def within(x, y, corner1, corner2):
    return x < corner2[0] and x > corner1[0] and y < corner2[1] and y > corner1[1]

def button_clicked(x, y):
    '''
    returns the button the click was in - if not, returns false
    '''
    if within(x, y, (10, 110), (450, 200)):
        return 'snspd'
    if within(x, y, (10, 210), (450, 300)):
        return 'wvguide'
    if within(x, y, (200, 320), (450, 400)):
        return 'align'
    return False

def test_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        print(button_clicked(x, y))
        cv2.imshow("display", img)



if __name__ == "__main__":
    img = cv2.imread('test_14401080.png')
    button_img = draw_buttons(img, (1000, 1000), (500, 1000), (500, 500))
    cv2.imshow('display', button_img)
    cv2.setMouseCallback("display", test_function)
    cv2.waitKey(0)
    cv2.destroyAllWindows()