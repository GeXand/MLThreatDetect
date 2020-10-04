import io, sys, os
from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont

x = []

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


"""Detects labels in the file."""
def detect_labels(path, disp):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        description = label.description.lower()
        print(description)
        
        if ("gun" in description) or ("knife" in description) or ("firearm" in description):
            disp = True

    if response.error.message:
        print("Error: Failed to successfully analyze image.")
        # raise Exception(
        #     '{}\nFor more info on error messages, check: '
        #     'https://cloud.google.com/apis/design/errors'.format(
        #         response.error.message))
    return disp

def detect_safe_search(path, disp):
    """Detects unsafe features in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Safe search:')

    # print('adult: {}'.format(likelihood_name[safe.adult]))
    # print('medical: {}'.format(likelihood_name[safe.medical]))
    # print('spoofed: {}'.format(likelihood_name[safe.spoof]))
    print('violence: {}'.format(likelihood_name[safe.violence]))
    # print('racy: {}'.format(likelihood_name[safe.racy]))

    if safe.violence >= 3:
        disp = True

    if response.error.message:
        print("Error: Failed to successfully analyze image.")
        # raise Exception(
        #     '{}\nFor more info on error messages, check: '
        #     'https://cloud.google.com/apis/design/errors'.format(
        #         response.error.message))
    return disp

def localize_objects(path, disp):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    im = Image.open(io.BytesIO(content))

    disp2 = False

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('{} (confidence: {})'.format(object_.name, object_.score))

        # print('Normalized bounding polygon vertices: ')
        # for vertex in object_.bounding_poly.normalized_vertices:
        #     print(' - ({}, {})'.format(vertex.x, vertex.y))

        name = object_.name.lower()

        if ("gun" in name or "knife" in name or "firearm" in name):
            drawVertices(im, object_.bounding_poly.normalized_vertices, '{} (confidence: {:.2f})'.format(object_.name, object_.score))
            disp = True
            disp2 = True
            x.append(path)
            # x.append(os.path.basename(path))
        # drawVertices(path, object_.bounding_poly.normalized_vertices)

    if disp2:
        # im.show()
        im.save(os.path.join("/Users/Rish209/Programming/hackathons/automated-threat-recognition/labeled_images", os.path.basename(path)))

    return disp

def drawVertices(im, vertices, display_text=''):
    width, height = im.size
    points = [(point.x * width, point.y * height) for point in vertices]

    draw = ImageDraw.Draw(im)

    draw.polygon(points, fill = None, outline=(255,0,0))

    font = ImageFont.truetype('arial.ttf', 16)
    draw.text((points[0][0] + 10, points[0][1]),
              font=font, text=display_text, 
              fill=(255, 255, 255))
    # draw.line((vertices[0].x, vertices[0].y, vertices[0].x+10, vertices[0].y), fill=(0, 0, 0, 255), width = 10)
    # im.show()


def main():
    blockPrint() #Suppressing prints

    try:
        image_directory = os.getcwd()
        # image_directory = sys.argv[1]
        # extension = "." + sys.argv[2]

        for root, dirs, files in os.walk(image_directory):
            for filename in files:
                if filename.endswith(".jpg") or filename.endswith(".png"):
                # if filename.endswith(extension):
                    disp = False

                    path = os.path.join(root, filename)
                    print("File: " + filename)

                    disp = detect_labels(path, disp)
                    print()

                    disp = detect_safe_search(path, disp)
                    print()

                    disp = localize_objects(path, disp)
                    print()
                    # break
    # except:
    #     print("Error in ", path)
    finally:
        for path in x:
            print(path)

if __name__ == '__main__':
    main()