import bin.lib.ffmpeg

ffmpeg = bin.lib.ffmpeg


class MetaDataParser:
    def __init__(self):
        pass

    def get_metadata(self, filepath):
        return ffmpeg.probe(str(filepath))["streams"]


videometa = MetaDataParser().get_metadata("/mnt/storage/SORTED/Videos/OBS_Rec/Behalten/2019-12-19 18-21-36.mp4").pop(0)
duration = videometa.get("duration")
frames = videometa.get("nb_frames")
framerate = float(frames) / float(duration)
print(framerate)
print(videometa)
