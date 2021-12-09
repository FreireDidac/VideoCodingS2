import os , sys
import subprocess, shlex
import wget
#sys.path.insert(0,'../')


class S2:

	standards = {
	"DVB": {
	"video":['mpeg2','h264'],
	"audio":['aac','ac-3','mp3']
		},
	"ISDB": {
	"video":['mpeg2','h264'],
	"audio":['aac']
		},
	"ATSC": {
	"video":['mpeg2','h264'],
	"audio":['AC-3']
		},
	"DTMB": {
	"video":['avs','avs+','mpeg2','h264'],
	"audio":['dra','mp2','aac','ac-3','mp3']
		},
	}
	def __init__(self):
		self.video = "cut_bbb.mp4"
		self.packaged_video = None
		self.seconds_to_cut = "60"
		
	def set_BBB_and_cut_video():
		self.video = input('enter the name of the bbb short video with the extension, this will later be used for the other excercices.')
		self.bbb = input('enter the name of the bbb complete video, this wil later be used for the other excercices.')
	def macroblocs_and_motionVectors(self):
		'''
		Function to get macroblocs and motion vectors of the video in the class
		'''
		os.system("ffmpeg -flags2 +export_mvs -i "+self.video+" -vf codecview=mv=pf+bf+bb macroblocks_motionvectors.mp4")

	def new_bbb_container(self):
		'''
		Function to generate a video container with two audio tracks and the same video encoding.
		Must have the "Big_Buck_Bunny.mp4" video to compile
		'''
	
		os.system("ffmpeg -i Big_Buck_Bunny.mp4 -ss 00:00:00 -t " + self.seconds_to_cut + " -async 1 cut_1min_bbb.mp4")
		os.system("ffmpeg -i cut_1min_bbb.mp4 -vn -acodec aac -b:a 100K output-audio1.aac")
		os.system("ffmpeg -i cut_1min_bbb.mp4 -vn -acodec mp3 -vcodec copy output-audio2.mp3")
		os.system("ffmpeg -i cut_1min_bbb.mp4 -i output-audio2.mp3 -i output-audio1.aac -map 0 -map 1 -map 2 -c copy packaged_video.mp4")
		self.packaged_video = 'packaged_video.mp4'

	def DVB_compatible(self,video):
		os.system("ffmpeg -i "+ video +" -vcodec libx264 -acodec aac dvb_compatible_video.mp4")
		print("converted video to DVB compatible")
		return "dvb_compatible_video.mp4"

	def get_audio_and_video_codecs(self,video = "packaged_video.mp4"):
		video_codecs_c = "ffprobe -v error -select_streams v -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "+ video#packaged_video.mp4"
		video_codecs_c = shlex.split(video_codecs_c)

		output_video_codecs = subprocess.run(video_codecs_c,stdout= subprocess.PIPE,universal_newlines=True).stdout

		audio_codecs_c = "ffprobe -v error -select_streams a -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "+ video#packaged_video.mp4"
		audio_codecs_c = shlex.split(audio_codecs_c)

		output_audio_codecs = subprocess.run(audio_codecs_c,stdout= subprocess.PIPE,universal_newlines=True).stdout

		#print(type(output_audio_codecs))
		audio_codecs_list = output_audio_codecs.split("\n")[:-1]
		print(audio_codecs_list)
		video_codecs_list = output_video_codecs.split('\n')[:-1]
		print(video_codecs_list)
		
		compatible_standards = self.get_standards(audio_codecs_list,video_codecs_list)
		if len(compatible_standards) > 0:
			print("your video is compatible with the standards: ", compatible_standards)
		else:
			self.DVB_compatible("packaged_video.mp4")


	def get_standards(self,audio_codecs,video_codecs):
		compatible_standards = []
		for standard in list(self.standards.keys()):
			compatible_video = False
			compatible_audio = False
			for audio_standard in self.standards[standard]['audio']:
				#print(audio_standard,'audio standard')
				if audio_standard in audio_codecs:
					compatible_audio = True
			for video_standard in self.standards[standard]['video']:
				#print(video_standard,'video standard')
				if video_standard in video_codecs:
					compatible_video = True
			if compatible_video == True and compatible_audio == True:
				compatible_standards.append(standard)
		return compatible_standards
		
		
		
	def download_and_burn_subtitles(self):
		wget.download("https://drive.google.com/uc?export=download&id=1bBQWBXskAimHqMq-lplyIpRvBvMdqrpA")
		os.system("ffmpeg -i Big_Buck_Bunny.mp4 -vf subtitles=subtitles.srt out.mp4")


	def main(self):
		loop = True
		while loop:
			option = input("Input the exercise number you want to execute:\n1- Get macroblocs and motion vectors\n2- Create the bbb container\n3- Get codecs from video and say which standard it fits, will convert to a compatible standard if it doesnt fit any \n4- Download and burn subtitles into video\nAny other number to exit\n")
			if option.strip() == "1":
				s.macroblocs_and_motionVectors()
			elif option.strip() == "2":
				s.new_bbb_container()
				#loop = False
			elif option.strip() == "3":
				s.get_audio_and_video_codecs("dvb_compatible_video.mp4")
			elif option.strip() == "4":
				s.download_and_burn_subtitles()
			else:
				loop = False
if __name__ == "__main__":
	#macroblocs_and_motionVectors()
	
	s = S2()
	s.main()
	pass
