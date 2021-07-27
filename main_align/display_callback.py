import cv2

def draw_buttons(img, temp_clicked, snspd, wvguide):
    can_align = not snspd == None and not wvguide == None
    purple = (250,230,230)
    red = (0,0,140)
    blue = (230,200,120)
    green = (0,252,124)

    #draw rectangles
    cv2.rectangle(img, (10, 10), (250, 80), purple, 2)
    cv2.rectangle(img, (10, 10), (100, 80), purple, -1)

    cv2.rectangle(img, (10, 110), (250, 180), red, 2)
    cv2.rectangle(img, (10, 110), (100, 180), red, -1)

    cv2.rectangle(img, (10, 210), (250, 280), blue, 2)
    cv2.rectangle(img, (10, 210), (100, 280), blue, -1)

    if can_align:
        cv2.rectangle(img, (100, 380), (250, 380), green, -1)

    #put on words

    return img


def live_feed_click(event, x, y, flags, param):
    return


if __name__ == "__main__":
    cv2.