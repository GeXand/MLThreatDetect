import sys, os, io
from google.cloud import videointelligence

"""Object tracking in a local video."""
def video_annotate(path):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.OBJECT_TRACKING]

    with io.open(path, "rb") as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        input_content=input_content, features=features
    )
    print("\nProcessing video for object annotations.")

    result = operation.result(timeout=300)
    print("\nFinished processing.\n")

    for r in result.annotation_results:

        # The first result is retrieved because a single video was processed.
        # object_annotations = result.annotation_results[0].object_annotations
        object_annotations = r.object_annotations

        # Get only the first annotation for demo purposes.
        for object_annotation in object_annotations:
        # object_annotation = object_annotations[0]
            print("Entity description: {}".format(object_annotation.entity.description))
            if object_annotation.entity.entity_id:
                print("Entity id: {}".format(object_annotation.entity.entity_id))

            print(
                "Segment: {}s to {}s".format(
                    object_annotation.segment.start_time_offset.seconds
                    + object_annotation.segment.start_time_offset.nanos / 1e9,
                    object_annotation.segment.end_time_offset.seconds
                    + object_annotation.segment.end_time_offset.nanos / 1e9,
                )
            )

            print("Confidence: {}".format(object_annotation.confidence))

            # Here we print only the bounding box of the first frame in this segment
            frame = object_annotation.frames[0]
            box = frame.normalized_bounding_box
            print(
                "Time offset of the first frame: {}s".format(
                    frame.time_offset.seconds + frame.time_offset.nanos / 1e9
                )
            )
            print("Bounding box position:")
            print("\tleft  : {}".format(box.left))
            print("\ttop   : {}".format(box.top))
            print("\tright : {}".format(box.right))
            print("\tbottom: {}".format(box.bottom))
            print("\n")

"""Detect labels given a file path."""
def video_label(path):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]

    with io.open(path, "rb") as movie:
        input_content = movie.read()

    operation = video_client.annotate_video(
        features=features, input_content=input_content
    )
    print("\nProcessing video for label annotations:")

    result = operation.result(timeout=90)
    print("\nFinished processing.")

    # Process video/segment level label annotations
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print("Video label description: {}".format(segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        for i, segment in enumerate(segment_label.segments):
            start_time = (
                segment.segment.start_time_offset.seconds
                + segment.segment.start_time_offset.nanos / 1e9
            )
            end_time = (
                segment.segment.end_time_offset.seconds
                + segment.segment.end_time_offset.nanos / 1e9
            )
            positions = "{}s to {}s".format(start_time, end_time)
            confidence = segment.confidence
            print("\tSegment {}: {}".format(i, positions))
            print("\tConfidence: {}".format(confidence))
        print("\n")

    # Process shot level label annotations
    shot_labels = result.annotation_results[0].shot_label_annotations
    for i, shot_label in enumerate(shot_labels):
        print("Shot label description: {}".format(shot_label.entity.description))
        for category_entity in shot_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        for i, shot in enumerate(shot_label.segments):
            start_time = (
                shot.segment.start_time_offset.seconds
                + shot.segment.start_time_offset.nanos / 1e9
            )
            end_time = (
                shot.segment.end_time_offset.seconds
                + shot.segment.end_time_offset.nanos / 1e9
            )
            positions = "{}s to {}s".format(start_time, end_time)
            confidence = shot.confidence
            print("\tSegment {}: {}".format(i, positions))
            print("\tConfidence: {}".format(confidence))
        print("\n")

    # Process frame level label annotations
    frame_labels = result.annotation_results[0].frame_label_annotations
    for i, frame_label in enumerate(frame_labels):
        print("Frame label description: {}".format(frame_label.entity.description))
        for category_entity in frame_label.category_entities:
            print(
                "\tLabel category description: {}".format(category_entity.description)
            )

        # Each frame_label_annotation has many frames,
        # here we print information only about the first frame.
        frame = frame_label.frames[0]
        time_offset = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
        print("\tFirst frame time offset: {}s".format(time_offset))
        print("\tFirst frame confidence: {}".format(frame.confidence))
        print("\n")

# only seems to detect pornography
def explicit_content(path):
    """ Detects explicit content from the GCS path to a video. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.EXPLICIT_CONTENT_DETECTION]

    with io.open(path, "rb") as movie:
        input_content = movie.read()
    operation = video_client.annotate_video(
            features=features, input_content=input_content
        )
    # operation = video_client.annotate_video(input_uri=path, features=features)
    print("\nProcessing video for explicit content annotations:")

    result = operation.result(timeout=90)
    print("\nFinished processing.")

    # Retrieve first result because a single video was processed
    for frame in result.annotation_results[0].explicit_annotation.frames:
        likelihood = videointelligence.enums.Likelihood(frame.pornography_likelihood)
        frame_time = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
        print("Time: {}s".format(frame_time))
        print("\npornography: {}".format(likelihood.name))

def main():
    # video_directory = "/Users/Rish209/Programming/hackathons/automated-threat-recognition/"
    # path = os.path.join(video_directory, "armed_robbery.mp4")
    # video_label(path)

    video_directory = sys.argv[1]
    extension = "." + sys.argv[2]

    for filename in os.listdir(video_directory):
        if filename.endswith(extension):
            path = os.path.join(video_directory, filename)
            print("File: " + filename)

            # video_annotate(path)
            # print()

            video_label(path)
            print()

            # explicit_content(path)
            # print()

            # break

if __name__ == '__main__':
    main()