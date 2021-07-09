async def file_recognize(filename, out="./"):
    images = ["jpg", "png", "webp"]
    videos = ["mp4", "mkv", "webm"]
    songs = ["mp3", "FLAC", "m4a", "ogg"]
    documents = ["zip", "rar", "apk"]
    direcs = {
        "image": images,
        "video": videos,
        "song": songs,
        "document": documents}
    try:
        ext = filename.split(".")[-1]
        if ext in direcs["image"]:
            file_type = "image"
        elif ext in direcs["video"]:
            file_type = "video"
        elif ext in direcs["song"]:
            file_type = "song"
        else:
            file_type = "document"
    except Exception as e:
        print(e)
        file_type = None
        ext = None
    return file_type
