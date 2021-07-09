import os
import random
import asyncio
import youtube_dl
from datetime import datetime
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata


async def place_water_mark(input_file, output_file, water_mark_file):
    watermarked_file = output_file + ".watermark.png"
    metadata = extractMetadata(createParser(input_file))
    width = metadata.get("width")
    shrink_watermark_file_genertor_command = [
        "ffmpeg",
        "-i", water_mark_file,
        "-y -v quiet",
        "-vf",
        "scale={}*0.5:-1".format(width),
        watermarked_file
    ]
    process = await asyncio.create_subprocess_exec(
        *shrink_watermark_file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    commands_to_execute = [
        "ffmpeg",
        "-i", input_file,
        "-i", watermarked_file,
        "-filter_complex",
        "\"overlay=(main_w-overlay_w):(main_h-overlay_h)\"",
        output_file
    ]
    process = await asyncio.create_subprocess_exec(
        *commands_to_execute,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return output_file


async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = output_directory + \
                        "/" + str("thumb") + ".jpg"
    # out_put_file_name = output_directory + \
    #                     "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None


async def generate_screen_shots(video_file,
                                output_directory,
                                min_duration,
                                no_of_photos):
    metadata = extractMetadata(createParser(video_file))
    duration = 0
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    if duration > min_duration:
        images = []
        ttl_step = duration // no_of_photos
        if duration == ttl_step:
            current_ttl = ttl_step // random.randint(15, 30)
        else:
            current_ttl = ttl_step
        for looper in range(0, no_of_photos):
            ss_img = await take_screen_shot(video_file, output_directory, current_ttl)
            current_ttl = current_ttl + ttl_step
            images.append(ss_img)
        return images
    else:
        return None


def ytdl(function):
    def wrapper(url, out="./", custom=""):
        datos = function(url, out, custom)
        url = datos["url"]
        out = datos["out"]
        ext = datos["ext"]
        custom = datos["custom"]
        video_info = youtube_dl.YoutubeDL().extract_info(url, download=False)
        # Demás datos, title, ext
        if len(custom) > 0:
            _title = custom
        else:
            _title = video_info["title"]
        try:
            _ext = video_info["ext"]
        except KeyError:
            _ext = video_info["entries"][0]["formats"][0]["ext"]
        if _ext == "unknown_video":
            if len(ext) > 0:
                _ext = ext
            else:
                _ext = "mp4"
        # Options + Download
        options = {"format": "best",
                   "outtmpl": out + _title + "." + _ext}
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])
        # Filename
        out_ = out + _title + "." + _ext
        return out_
    return wrapper






