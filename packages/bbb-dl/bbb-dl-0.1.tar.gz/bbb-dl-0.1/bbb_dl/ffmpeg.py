# Python wrapper around the ffmpeg utility
# Original author: CreateWebinar.com

import os
import shutil
import subprocess

from youtube_dl import YoutubeDL

from youtube_dl.utils import (
    encodeArgument,
    encodeFilename,
    shell_quote,
)
from youtube_dl.postprocessor.ffmpeg import FFmpegPostProcessor, FFmpegPostProcessorError


class MyFFmpegPostProcessor(FFmpegPostProcessor):
    def run_ffmpeg_multiple_files(self, input_paths, out_path, opts, opts_before=[]):
        self.check_version()

        oldest_mtime = min(os.stat(encodeFilename(path)).st_mtime for path in input_paths)

        opts += self._configuration_args()

        files_cmd = []
        for path in input_paths:
            files_cmd.extend([encodeArgument('-i'), encodeFilename(self._ffmpeg_filename_argument(path), True)])
        cmd = [
            encodeFilename(self.executable, True),
            encodeArgument('-y'),
        ]  # without -y there is a error callen, if the file exists
        if self.basename == 'ffmpeg':
            cmd += [encodeArgument('-loglevel'), encodeArgument('repeat+info')]
        cmd += (
            [encodeArgument(o) for o in opts_before]
            + files_cmd
            + [encodeArgument(o) for o in opts]
            + [encodeFilename(self._ffmpeg_filename_argument(out_path), True)]
        )

        if self._downloader.params.get('verbose', False):
            self._downloader.to_screen('[debug] ffmpeg command line: %s' % shell_quote(cmd))
        p = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True
        )

        last_line = ''
        for line in p.stderr:
            # line = line.decode('utf-8', 'replace')
            if line.find('time=') > 0:
                print('\033[K' + line.replace('\n', '') + '\r', end='')
            last_line = line
        print('')

        std_out, std_err = p.communicate()
        if p.returncode != 0:
            msg = last_line.strip().split('\n')[-1]
            raise FFmpegPostProcessorError(msg)
        self.try_utime(out_path, oldest_mtime, oldest_mtime)

    def run_ffmpeg(self, path, out_path, opts, opts_before=[]):
        self.run_ffmpeg_multiple_files([path], out_path, opts, opts_before)


class FFMPEG:
    def __init__(self, ydl: YoutubeDL):
        self.pp = MyFFmpegPostProcessor(ydl)
        self.pp.check_version()

    def rescale_image(self, image, height, width):
        out_file = image + "-new.png"
        self.pp.run_ffmpeg(image, out_file, ["-vf", "pad=%s:%s:ow/2-iw/2:oh/2-ih/2" % (width, height)])
        shutil.move(out_file, image)

    def mux_slideshow_with_webcam(self, video_file, webcam_file, webcam_w, webcam_h, out_file):
        if os.path.isfile(out_file):
            return
        self.pp.run_ffmpeg_multiple_files(
            [webcam_file, video_file],
            out_file,
            [
                "-filter_complex",
                "[0:v]scale=%s:%s, setpts=PTS-STARTPTS,format=rgba,colorchannelmixer=aa=0.7 [ovrl];[1:v] fps=24,setpts=PTS-STARTPTS [bg]; [bg][ovrl] overlay=W-w:H-h:shortest=1"
                % (webcam_w, webcam_h),
                '-c:a',
                'copy',
                '-crf',
                '24',
                '-vsync',
                '0',
                '-r',
                '24',
            ],
        )

    def mux_slideshow(self, video_file, webcam_file, out_file):
        if os.path.isfile(out_file):
            return
        self.pp.run_ffmpeg_multiple_files(
            [webcam_file, video_file],
            out_file,
            [
                '-map',
                '0:a',
                '-c:a',
                'copy',
                '-map',
                '1:v',
                '-c:v',
                'copy',
                '-shortest',
            ],
        )

    def create_video_from_image(self, image, duration, out_file):
        if os.path.isfile(out_file):
            return
        self.pp.run_ffmpeg(
            image,
            out_file,
            [
                "-c:v",
                "libx264",
                "-t",
                str(duration),
                "-pix_fmt",
                "yuv420p",
                "-preset",
                "veryfast",
            ],
            [
                "-loop",
                "1",
                "-f",
                "image2",
                "-framerate",
                "1",
                "-r",
                "1",
            ],
        )

    def concat_videos(self, video_list, out_file):
        if os.path.isfile(out_file):
            return
        self.pp.run_ffmpeg(video_list, out_file, ["-c", "copy"], ["-f", "concat", "-safe", "0"])

    def webm_to_mp4(self, webm_file, mp4_file):
        if os.path.isfile(mp4_file):
            return
        self.pp.run_ffmpeg(webm_file, mp4_file, ["-qscale", "0"])

    def trim_video_by_seconds(self, video_file, start, duration, out_file):
        if os.path.isfile(out_file):
            return
        self.pp.run_ffmpeg(video_file, out_file, ["-ss", str(start), "-c", "copy", "-t", str(duration)])

    def mp4_to_ts(self, inp_file, out_file):
        if os.path.isfile(out_file):
            return
        self.pp.run_ffmpeg(inp_file, out_file, ["-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts"])
