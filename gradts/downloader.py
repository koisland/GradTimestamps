import os
import pytube
import tqdm

from config import Config
from gradts.logger import get_logger


log = get_logger()


def dl_multiple(video_list, output):
    # download multiple videos with pytube
    for url in video_list:
        dl = PytubeDl(url=url, output_dir=output, media_type="video_only", res="720p")
        grad_video = dl.download()

        # set date and fps
        date = dl.pytube_obj.publish_date
        yield f"{date.month}_{date.day}_{date.year}", dl.fps, grad_video


class PytubeDl(Config):

    def __init__(self, url, output_dir, media_type, res=None):
        self.url = url
        self.output_dir = output_dir
        self.media_type = media_type
        self.res = res
        self.progress_bar = None

    @property
    def res(self):
        return self._res

    @res.setter
    def res(self, res):
        if res not in self.VALID_RESOLUTIONS:
            raise Exception("Invalid resolution.")
        self._res = res

    @property
    def fps(self):
        return self.stream.fps

    @property
    def media_type(self):
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        if media_type not in ("both", "audio_only", "video_only"):
            raise Exception("Invalid media type.")
        self._media_type = media_type

    @property
    def pytube_obj(self):
        return pytube.YouTube(self.url, on_progress_callback=self._progress, on_complete_callback=self._finished)

    @property
    def output_dir(self):
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir):
        if not os.path.exists(output_dir):
            raise Exception("Invalid output directory.")

        self._output_dir = output_dir

    def _finished(self, *args):
        _, file_path = args
        print(f"\nFinished and saved file to {file_path}")
        log.info(f"File downloaded to {file_path}")

    def _progress(self, *args):
        (_, chunk, _) = args
        self.progress_bar.update(len(chunk))

    @property
    def stream(self):
        if self.media_type == "both":
            # highest res returns prog stream
            return self.pytube_obj.streams.get_highest_resolution()
        elif self.media_type == "audio_only":
            return self.pytube_obj.streams.get_audio_only()
        elif self.media_type == "video_only" and self.res:
            return self.pytube_obj.streams.filter(resolution=self.res, progressive=False).first()

    def download(self):
        self.progress_bar = tqdm.tqdm(total=self.stream.filesize, leave=True, position=0)
        output_file_path = os.path.join(self.output_dir, self.stream.default_filename)
        if os.path.exists(output_file_path):
            self.progress_bar.update(self.stream.filesize)
            return output_file_path
        return self.stream.download(output_path=self.output_dir)


if __name__ == "__main__":
    video = PytubeDl(Config.URLS[0], output_dir=Config.OUTPUT_DIR, media_type="video_only", res="1080p")
    video.download()