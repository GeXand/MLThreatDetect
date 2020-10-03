import io, sys, os
from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont

"""Detects labels in the file."""
def detect_labels(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

    if response.error.message:
        print("Error: Failed to successfully analyze image.")
        # raise Exception(
        #     '{}\nFor more info on error messages, check: '
        #     'https://cloud.google.com/apis/design/errors'.format(
        #         response.error.message))

def detect_safe_search(path):
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

    if response.error.message:
        print("Error: Failed to successfully analyze image.")
        # raise Exception(
        #     '{}\nFor more info on error messages, check: '
        #     'https://cloud.google.com/apis/design/errors'.format(
        #         response.error.message))

def localize_objects(path):
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

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('{} (confidence: {})'.format(object_.name, object_.score))
        # print('Normalized bounding polygon vertices: ')
        # for vertex in object_.bounding_poly.normalized_vertices:
        #     print(' - ({}, {})'.format(vertex.x, vertex.y))

        if ("gun" in object_.name or "knife" in object_.name):
            drawVertices(im, object_.bounding_poly.normalized_vertices, '{} (confidence: {:.2f})'.format(object_.name, object_.score))
        # drawVertices(path, object_.bounding_poly.normalized_vertices)
    im.show()

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
    image_directory = sys.argv[1]
    extension = "." + sys.argv[2]

    for filename in os.listdir(image_directory):
        if filename.endswith(extension):
            path = os.path.join(image_directory, filename)
            print("File: " + filename)

            detect_labels(path)
            print()

            detect_safe_search(path)
            print()

            localize_objects(path)
            print()
            # break

if __name__ == '__main__':
    main()