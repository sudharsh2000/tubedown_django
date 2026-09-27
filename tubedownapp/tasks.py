import os
import tempfile

import yt_dlp
from celery import shared_task


@shared_task
def download_video( url, resolution):


        temp_dir = tempfile.mkdtemp()

        output_template = os.path.join(
            temp_dir,
            "%(title)s.%(ext)s"
        )

        ydl_opts = {
            "format": (
                f"bestvideo[height<={resolution}]"
                f"+bestaudio/best[height<={resolution}]"
            ),
            "outtmpl": output_template,
            "merge_output_format": "mp4",
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        video_files = [
            file
            for file in os.listdir(temp_dir)
            if file.lower().endswith(".mp4")
        ]

        if not video_files:
            raise Exception("Video file was not created.")

        file_path = os.path.join(
            temp_dir,
            video_files[0]
        )

        return {
            "file_path": file_path,
            "title": info.get("title", "video"),
        }


@shared_task
def download_audio( url):


            audio_quality = int(320)


            temp_dir = tempfile.mkdtemp()

            output_template = os.path.join(
                temp_dir,
                "%(title)s.%(ext)s",
            )

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_template,
                "noplaylist": True,

                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": str(audio_quality),
                    }
                ],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

            title = info.get("title", "audio")

            files = os.listdir(temp_dir)

            mp3_files = [
                file for file in files
                if file.lower().endswith(".mp3")
            ]

            if not mp3_files:
                raise Exception("MP3 file was not created.")

            file_path = os.path.join(
                temp_dir,
                mp3_files[0],
            )

            return {
                "file_path": file_path,
                "title": info.get("title", "audio")
            }