from PIL import Image, ImageOps


def check_in_point(img, pattern, x, y):
    for pattern_x in range(pattern.size[0]):
        if pattern_x + x > img.size[0]:
            return False

        for pattern_y in range(pattern.size[1]):
            if pattern_y + y > img.size[1]:
                return False
            
            img_pixel = img.getpixel((x + pattern_x, y + pattern_y))
            if img_pixel not in (0, 255):
                print(img_pixel)
                raise Excception()
            if img_pixel == 255:
                continue
            pattern_pixel = pattern.getpixel((pattern_x, pattern_y))
            if img_pixel != pattern_pixel:
                return False
    return True

def check_image(img, pattern):
    x_size = img.size[0] - pattern.size[0] + 1
    y_size = img.size[1] - pattern.size[1] + 1

    for x in range(x_size):
        for y in range(y_size):
            if check_in_point(img, pattern, x, y):
                print('MAM!!:', x, y)
                print(kat)
                print(flipper)
                print(invert)

kat = ''
flipper = ''
trans = ''
invert = ''

def image_variations(pattern):
    global kat, flipper, trans, invert
    for angle in (0, 90, 180, 270):
        for flip in (None, Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM):
            pat = pattern.rotate(angle)
            if flip is not None:
                pat = pat.transpose(flip)
            kat = angle
            flipper = flip
            invert = False
            yield pat
            invert = True
            yield ImageOps.invert(pat)

if __name__ == '__main__': 
    codes = Image.open('images3_cleaned.png')
    #codes = Image.open('test.png')
    pattern = Image.open('pattern3_cleaned.png')

    for new_pattern in image_variations(pattern):
        check_image(codes, new_pattern)


