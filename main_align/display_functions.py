import cv2
import math
import numpy as np

def rotate_image(image, angle):
    image_size = (image.shape[1], image.shape[0])
    image_center = tuple(np.array(image_size) / 2)
    # Convert the OpenCV 3x2 rotation matrix to 3x3
    rot_mat = np.vstack(
        [cv2.getRotationMatrix2D(image_center, angle, 1.0), [0, 0, 1]]
    )
    rot_mat_notranslate = np.matrix(rot_mat[0:2, 0:2])
    image_w2 = image_size[0] * 0.5
    image_h2 = image_size[1] * 0.5
    # Obtain the rotated coordinates of the image corners
    rotated_coords = [
        (np.array([-image_w2,  image_h2]) * rot_mat_notranslate).A[0],
        (np.array([ image_w2,  image_h2]) * rot_mat_notranslate).A[0],
        (np.array([-image_w2, -image_h2]) * rot_mat_notranslate).A[0],
        (np.array([ image_w2, -image_h2]) * rot_mat_notranslate).A[0]
    ]

    # Find the size of the new image
    x_coords = [pt[0] for pt in rotated_coords]
    x_pos = [x for x in x_coords if x > 0]
    x_neg = [x for x in x_coords if x < 0]

    y_coords = [pt[1] for pt in rotated_coords]
    y_pos = [y for y in y_coords if y > 0]
    y_neg = [y for y in y_coords if y < 0]

    right_bound = max(x_pos)
    left_bound = min(x_neg)
    top_bound = max(y_pos)
    bot_bound = min(y_neg)

    new_w = int(abs(right_bound - left_bound))
    new_h = int(abs(top_bound - bot_bound))

    # We require a translation matrix to keep the image centred
    trans_mat = np.matrix([
        [1, 0, int(new_w * 0.5 - image_w2)],
        [0, 1, int(new_h * 0.5 - image_h2)],
        [0, 0, 1]
    ])

    # Compute the tranform for the combined rotation and translation
    affine_mat = (np.matrix(trans_mat) * np.matrix(rot_mat))[0:2, :]

    # Apply the transform
    result = cv2.warpAffine(
        image,
        affine_mat,
        (new_w, new_h),
        flags=cv2.INTER_LINEAR
    )
    return result


def largest_rotated_rect(w, h, angle):
    quadrant = int(math.floor(angle / (math.pi / 2))) & 3
    sign_alpha = angle if ((quadrant & 1) == 0) else math.pi - angle
    alpha = (sign_alpha % math.pi + math.pi) % math.pi

    bb_w = w * math.cos(alpha) + h * math.sin(alpha)
    bb_h = w * math.sin(alpha) + h * math.cos(alpha)

    gamma = math.atan2(bb_w, bb_w) if (w < h) else math.atan2(bb_w, bb_w)
    delta = math.pi - alpha - gamma
    length = h if (w < h) else w

    d = length * math.cos(alpha)
    a = d * math.sin(alpha) / math.sin(delta)

    y = a * math.cos(gamma)
    x = y * math.tan(gamma)

    return (
        bb_w - 2 * x,
        bb_h - 2 * y
    )


def crop_around_center(image, width, height):
    image_size = (image.shape[1], image.shape[0])
    image_center = (int(image_size[0] * 0.5), int(image_size[1] * 0.5))
    if(width > image_size[0]):
        width = image_size[0]
    if(height > image_size[1]):
        height = image_size[1]

    x1 = int(image_center[0] - width * 0.5)
    x2 = int(image_center[0] + width * 0.5)
    y1 = int(image_center[1] - height * 0.5)
    y2 = int(image_center[1] + height * 0.5)

    return image[y1:y2, x1:x2]


def size_and_straighten(img, angle = 0):
    img = cv2.resize(img, (1440, 1080))
    image_height, image_width = img.shape[0:2]
    rotated = rotate_image(np.copy(img), angle)
    img = crop_around_center(rotated, *largest_rotated_rect(image_width, image_height,math.radians(angle)))
    return cv2.resize(img, (1440, 1080))


def img_process_bw(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


def draw_buttons(source, temp_clicked, snspd, wvguide):
    can_align = (not snspd == None) and (not wvguide == None) and (not snspd[0] == None) and (not wvguide[0] == None)
    purple = (255,100,170)
    red = (51,51,255)
    blue = (255,128,0)
    green = (0,204,0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    font = cv2.FONT_HERSHEY_COMPLEX

    img = np.ndarray.copy(source)

    #clicked
    cv2.rectangle(img, (10, 10), (450, 100), white, -1)
    cv2.rectangle(img, (10, 10), (450, 100), purple, 2)
    cv2.rectangle(img, (10, 10), (200, 100), purple, -1)
    cv2.putText(img,'Clicked',(40,65), font, 1,white,2)
    if not temp_clicked == None:
        cv2.putText(img, str(temp_clicked), (220, 65), font, 1,black,2)

    #SNSPD
    cv2.rectangle(img, (10, 110), (450, 200), white, -1)
    cv2.rectangle(img, (10, 110), (450, 200), red, 2)
    cv2.rectangle(img, (10, 110), (200, 200), red, -1)
    cv2.putText(img,'SNSPD',(50,165), font, 1,white,2)
    if not snspd == None:
        cv2.putText(img, str(snspd), (220, 165), font, 1,black,2)

    #Waveguide
    cv2.rectangle(img, (10, 210), (450, 300), white, -1)
    cv2.rectangle(img, (10, 210), (450, 300), blue, 2)
    cv2.rectangle(img, (10, 210), (200, 300), blue, -1)
    cv2.putText(img,'Waveguide',(20,265), font, 1,white,2)
    if not wvguide == None:
        cv2.putText(img, str(wvguide), (220, 265), font, 1,black,2)

    #Align
    if can_align:
        cv2.rectangle(img, (200, 320), (450, 400), green, -1)
        cv2.rectangle(img, (200, 320), (450, 400), black, 5)
        #####TypeError: unsupported operand type(s) for -: 'NoneType' and 'NoneType'###############
        shift = wvguide[0] - snspd[0]
        cv2.putText(img, 'Align (' + str(shift) + ')', (220, 370), font, 1,black,2)

    #Straighten
    cv2.rectangle(img, (1240, 10), (1420, 60), black, -1)
    cv2.putText(img, 'reset angle', (1250, 40), font, 0.8, white, 1)

    #draw dots
    if temp_clicked:
        cv2.circle(img, temp_clicked, radius=2, color=purple, thickness=5)
    if wvguide:
        cv2.circle(img, wvguide, radius=2, color=blue, thickness=6)
    if snspd:
        cv2.circle(img, snspd, radius=2, color=red, thickness=6)
    return img

def straighten_draw_buttons(source, angle, coords):
    img = np.ndarray.copy(source)
    white = (255, 255, 255)
    black = (0, 0, 0)
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(img,'Click two points that determine the horizontal', (40,40) , font, 0.8, black, 2)
    cv2.putText(img,'Press the S key to set the rotation angle', (40,80) , font, 0.8, black, 2)
    try:
        cv2.putText(img,'Angle is currently ' + str(angle), (40, 120), font, 0.8, black, 2)
    except:
        cv2.putText(img,'no angle',(40, 120), font, 0.5, black, 1)
    
    try:
        cv2.circle(img, coords[-1], radius=2, color=white, thickness=5)
        try:
            cv2.circle(img, coords[-2], radius=2, color=white, thickness=5)
        except: pass
    except: pass

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
    if within(x, y, (1240, 10), (1420, 60)):
        return 'straighten'
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