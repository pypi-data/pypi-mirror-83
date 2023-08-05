from transcripts import YoutubeChannelTranscripts

getter = YoutubeChannelTranscripts('Every Frame a Painting', 'AIzaSyBZ7Ky1KHWzy9xuGePiTyowP93ZMaqV8Sc')
print(getter.video)

getter.write_transcripts(file_path='/home/dcliu95/GitRepos/youtube-channel-transcript-api/Every_Frame_a_Painting/')
