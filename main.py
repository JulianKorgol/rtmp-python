from vidgear.gears import CamGear
from vidgear.gears import WriteGear
import os
# sudo apt install ffmpeg

video_catalog = './videos/'

# Count videos in the catalog
video_count = len([name for name in os.listdir(video_catalog) if os.path.isfile(os.path.join(video_catalog, name))])

output_params = {
    "-clones": ["-f", "lavfi", "-i", "anullsrc"],
    "-vcodec": "libx264",
    "-preset": "medium",
    "-b:v": "4500k",
    "-bufsize": "512k",
    "-pix_fmt": "yuv420p",
    "-f": "flv",
}

youtube_stream_key = "xxxx-xxxx-xxxx-xxxx-xxxx"

writer = WriteGear(
    output="rtmp://a.rtmp.youtube.com/live2/{}".format(youtube_stream_key),
    logging=True,
    **output_params
)

while True:
    for i in range(video_count):
        # Define video source
        stream = CamGear(source=video_catalog + str(i) + '.mp4', logging=True).start()

        while True:
            # read frames from stream
            frame = stream.read()

            # check for frame if Nonetype
            if frame is None:
                break

            # {do something with the frame here}

            # write frame to writer
            writer.write(frame)

        # safely close video stream
        stream.stop()
writer.close()
