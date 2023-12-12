from pydub import AudioSegment

def adjust_volume(input_file, output_file, target_dBFS):
    audio = AudioSegment.from_file(input_file)
    dbfs = audio.dBFS
    #print(f"dbfs_PRIOR: {dbfs}.")      #For debugging, etc.
    #print(f"dbfs/2: {dbfs/2}.")
    current_dBFS = audio.dBFS
    volume_change = target_dBFS - current_dBFS
    adjusted_audio = audio + volume_change
    file_extension = input_file.split('.')[-1].lower()
    supported_formats = ["wav", "mp3", "ogg", "flac", "aac", "m4a"]                     #All formats supported by pydub.
    export_format = file_extension if file_extension in supported_formats else "wav"    #.wav is the default.
    adjusted_audio.export(output_file, format=export_format)

#To test the function by itself (via python3 dbfs.py):
input_file = "AudioExample01.wav"
output_file = "processed_AudioExample01.wav"
target_dBFS = -40

adjust_volume(input_file, output_file, target_dBFS)

new_audio = AudioSegment.from_file(output_file)
new_loudness = new_audio.dBFS
#print(f"dbfs_AFTER: {new_loudness}.")      #For debugging, etc.

#uvicorn main:app --reload