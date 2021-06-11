import os
import pytube
import tqdm

from config import Config


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
        return pytube.YouTube(self.url, on_progress_callback=self._progress)

    @property
    def output_dir(self):
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir):
        if not os.path.exists(output_dir):
            raise Exception("Invalid output directory.")

        self._output_dir = output_dir

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
        self.progress_bar = tqdm.tqdm(total=self.stream.filesize, leave=False)
        output_file_path = os.path.join(self.output_dir, self.stream.default_filename)
        if os.path.exists(output_file_path):
            self.progress_bar.update(self.stream.filesize)
            return output_file_path
        return self.stream.download(output_path=self.output_dir)


if __name__ == "__main__":
    video = PytubeDl(Config.URLS[0], output_dir=Config.OUTPUT_DIR, media_type="video_only", res="1080p")
    video.download()