import pathlib
from typing import (
    IO,
    Generator,
)

import cv2

from config import VIDEO_DIR


def init_video_dir():
    pathlib.Path(VIDEO_DIR).mkdir(exist_ok=True)


def video_frames_generator(video: IO) -> Generator[bytes, None, None]:
    vidcap = cv2.VideoCapture(video)

    while True:
        success_read, frame = vidcap.read()
        if not success_read:
            continue

        success_encode, encoded_frame = cv2.imencode(".jpg", frame)
        if not success_encode:
            continue

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" +
               bytearray(encoded_frame) + b"\r\n")
