# AI Assisted Faculty Evaluation System​

## Table of Contents

- Introduction
- Features
- Transcript generation

## Introduction

The AI Assisted Faculty Evaluation System is a software application designed to streamline and enhance the process of evaluating faculty members in educational institutions. Leveraging artificial intelligence (AI) technologies, this system aims to provide more accurate, efficient, and data-driven assessments of faculty performance.

## Features

Automated Evaluation: The system automates various aspects of faculty evaluation, reducing manual effort and saving time for administrators.

Data Analysis: Utilizes AI algorithms to analyze various data points such as student feedback, academic achievements, research publications, teaching methodologies, and peer reviews to generate comprehensive evaluations.

Performance Metrics: Generates detailed performance metrics for each faculty member based on predefined criteria, providing a holistic view of their contributions and effectiveness.

Feedback Mechanism: Facilitates the collection of feedback from students, colleagues, and administrators, allowing for continuous improvement and assessment of faculty performance.

Customizable Evaluation Criteria: Administrators can customize evaluation criteria based on institutional objectives, departmental requirements, or specific accreditation standards.

Reporting and Visualization: Generates visual reports and dashboards to present evaluation results in a clear and accessible manner, enabling stakeholders to make informed decisions.

## Setup Instructions

### Step 1:  Install python `3.12.2`

### Step 2: Install all its dependencies by the following command
```
pip install -r requirements.txt
```

### Step 3: Install Imagepick from the following website

### For Windows
``` 
https://imagemagick.org/script/download.php#windows
```

### For Linux
``` 
https://imagemagick.org/script/download.php#linux
```

### For Mac
``` 
https://imagemagick.org/script/download.php#macosx
```


### Step-4 Get the `.env` file shared with the code instructions or from the following url and paste in the root directory

```
https://drive.google.com/file/d/1_uQR5VC33LKKDJR3aT727R7uN_1VqscG/view?usp=sharing
```
## Run the Code

### Video Translation

Go to the `video_translator.py` file, update the input path of the input video and run
```
python video_translator.py
```

### Question Generation
Go to the `question_generator.py` file, update the input path of the input video
```
python question_generator.py
```
### Summary Generation
Go to the `summarizer.py` file, update the input path of the input video
```
python summarizer.py
```

## Transcript Generation

 ### Modules
  - __init__  : 
    1. The modules used in this collectively facilitate various tasks in audio and video processing, including merging, extracting, converting, transcribing, and organizing multimedia files. 
    2. They can be valuable in multimedia content creation, data processing, and automation workflows.
  - __attach_audio_to_video.py__ : 
    1. Imports: It imports necessary modules from the moviepy.editor package, including VideoFileClip, AudioFileClip, and concatenate_audioclips.
    2. VideoAttacher Class: It defines a class named VideoAttacher.
    3. attach_audio_to_video Method: This method takes three parameters: video_path (path to the video file), audio_path (path to the audio file), and output_path (path where the resulting video with attached audio will be saved).
    4. Load Clips: It loads the video and audio clips using VideoFileClip and AudioFileClip from the provided paths.
    5. Extend Audio Clip: If the duration of the audio clip is shorter than the duration of the video clip, it extends the audio clip with silence to match the video duration.
    6. Set Audio to Video: It sets the audio of the video clip to the loaded audio clip.
    7. Write Modified Video: It writes the modified video clip (with attached audio) to the output path using specified codecs (libx264 for video and aac for audio) and frame rate.
    
    Example Usage: The if __name__ == "__main__": block demonstrates an example usage of the VideoAttacher class by attaching audio to a video file specified by video_path, with audio from audio_path, and saving the resulting video to output_path.
  - __audio_extractor__ : 
    1. Imports: The code imports necessary modules from the moviepy.editor library for working with video files and from the built-in os module.

    2. AudioExtractor Class: The AudioExtractor class is defined, but the __init__ method is left empty.

    3. extract_audio_to_mp3 Method: This method takes two parameters: video_path (the path to the input video file) and output_path (the path where the extracted audio will be saved as an MP3 file).

    4. Load Video Clip: It loads the video clip from the provided video_path using VideoFileClip.

    5. Extract Audio: It extracts the audio from the video clip using the .audio attribute.

    6. Save as MP3: It saves the extracted audio as an MP3 file at the specified output_path using the .write_audiofile method, specifying the codec as 'mp3'.

    
  - __file_organizer__ 
    1. create_folder_if_not_exists(self, folder_path): Checks if a folder exists at the specified path, and if not, creates it. It takes a folder_path parameter representing the path of the folder to be checked/created.

    2. extract_file_name_from_path(self, file_path): Extracts the file name from a given file path. It takes a file_path parameter representing the path of the file and returns the file name.

    3. get_file_name_without_extension(self, file_name): Extracts the file name without the extension from the given file name. It takes a file_name parameter and returns the file name without the extension.

    4. get_file_name_without_extension_from_path(self, file_path): Combines the functionality of the previous two methods. It extracts the file name without the extension from the given file path. It takes a file_path parameter representing the path of the file and returns the file name without the extension.

    5. initialize(self, video_file_name: str): Initializes the file organizer by creating an output folder based on the video file name without the extension. It takes a video_file_name parameter representing the name of the video file. It creates a folder named after the video file in the "output" directory and returns the path of the created folder.

    6. The FileOrganizer class provides functionality to manage files and folders, including creating folders, extracting file names, and initializing the file organization structure for a given video file.
  - __mergedmp3__ :
    1. merge_mp3_files Method: This method takes a folder_path parameter representing the path to the folder containing MP3 files to be merged.

    2. Collect MP3 Files: It collects all MP3 files in the specified folder.

    3. Check MP3 Files: If no MP3 files are found, it prints a message and returns.

    4. Sort MP3 Files: It sorts the list of MP3 files alphabetically.

    5. Create Destination File: It creates a destination file named 'merged.mp3' in the parent directory of the specified folder.

    6. Merge MP3 Files: It iterates over each MP3 file, reads its content, and appends it to the destination file.

    7. Print Result: It prints a message indicating the number of MP3 files merged and the path of the destination file.

    
  - __split_audios.py__ :
    1. Imports: The code imports necessary modules from the PyDub library and the built-in os module.

    2. split_mp3_to_wav Function: This function takes three parameters:

        - input_file_path: Path to the input MP3 file.

        - output_dir: Directory to save the output WAV files.

        - segment_duration_ms: Duration of each segment in milliseconds (default is 10,000ms for 10 seconds).

    3. Load MP3 File: It loads the input MP3 file using PyDub's AudioSegment.from_mp3 method.

    4. Ensure Output Directory: It checks if the specified output directory exists, and if not, creates it using os.makedirs.

    5. Split the Audio: It iterates over the MP3 audio, slicing it into segments of the specified duration. Each segment is then exported to a WAV file using chunk.export.

    6. Return Output Files: It returns a list of file paths to the generated WAV files.
  - __transcribe.py__ :
    
    This code is useful for automating the transcription and translation of audio and subtitle files, which can be valuable for creating multilingual content or improving accessibility for non-native speakers.
    1. **mp3_to_translated_srt(self, mp3_file, destination_language='es')**: 
    - This method transcribes an MP3 audio file using the `WhisperModel` from the `faster_whisper` library.
    - The transcribed text is then translated into a specified language (default is Spanish) using the Google Translate service provided by the `deep_translator` library.
    - The original subtitles and the translated subtitles are written to SRT files.
     - The method returns the path to the translated SRT file.

    2. **`srt_translate(self, srt_file, destination_language)`**:
    - This method translates an existing SRT file into a specified language using the Google Translate service.
    - The translated subtitles are written to a new SRT file.
   
    3. **`__init__(self)`**:
    - The constructor initializes the `WhisperModel` for transcribing audio and retrieves the supported languages for translation from Google Translate.

    4. **Example Usage**:
    - The `if __name__ == "__main__":` block demonstrates an example usage of the `TrascribeSRT` class by transcribing an MP3 file named 'demo4.mp3' into Spanish, and then translating an SRT file ('es_3.srt') into Spanish.

   ## __main.py__ 

   
      from modules import AudioExtractor
      from modules import FileOrganizer
      from modules import TrascribeSRT
      from modules import SRTToAudioConverter
      from modules import MP3Merger
      from modules import VideoAttacher
      import os


      audio_extractor = AudioExtractor()
      file_organizer = FileOrganizer()
      transcriber = TrascribeSRT()
      audio_generator = SRTToAudioConverter()
      mp3_merger = MP3Merger()
      video_attacher = VideoAttacher()
      if __name__ == "__main__": 

      path_to_video = "demo.mp4"
   
      output_path_folder = file_organizer.initialize(path_to_video)
      output_path = os.path.join(output_path_folder, file_organizer.get_file_name_without_extension_from_path(path_to_video) + ".mp3")
      output_path_video = os.path.join(output_path_folder,  file_organizer.get_file_name_without_extension_from_path(path_to_video) + "_translated" +  ".mp4")

    
    # Step 1 is to extract the audio
    output_path = audio_extractor.extract_audio_to_mp3(path_to_video, output_path)

    # Step 2 Transcribe the audio
    srt_file = transcriber.mp3_to_translated_srt(output_path) 

    # Step-3 Convert SRT files to Audio
    output_folder = audio_generator.convert_srt_to_audio(srt_file, output_path_folder, lang = "es") 
        
    # Step-4 Merge all mp3 files
    merged_file = mp3_merger.merge_mp3_files(output_folder)

    # Step-5 Attach new audio to video

    video_attacher.attach_audio_to_video(path_to_video, r"output\demo\merged.mp3", output_path_video)


    
  __Audio Extraction :__

  - The script imports an AudioExtractor module.
  - It initializes an AudioExtractor object.
  - It extracts audio from a video file specified by path_to_video and saves it as an MP3 file.
      
  __File Organization:__

  - The script imports a FileOrganizer module.
  - It initializes a FileOrganizer object.
  - It organizes the output files into a folder specified by output_path_folder.
    
  __Transcription:__

  - The script imports a TranscribeSRT module.
  - It initializes a TranscribeSRT object.
  - It transcribes the extracted audio into a SubRip subtitle (SRT) file.
      
  __SRT to Audio Conversion:__

  - The script imports an SRTToAudioConverter module.
  - It initializes an SRTToAudioConverter object.
  - It converts the transcribed SRT file into audio files, likely in a different language, as specified by the lang parameter.
      
  __MP3 Merging:__

  - The script imports an MP3Merger module.
  - It initializes an MP3Merger object.
  - It merges all the MP3 files generated in the previous step into a single MP3 file.
      
  __Video Processing:__

  - The script imports a VideoAttacher module.
  - It initializes a VideoAttacher object.
  - It attaches the newly generated audio to the original video, creating a new video file with the translated audio.

  __The if __name__ == "__main__": block ensures that the script runs only when it's executed directly, not when imported as a module.__ 



## Dependencies

1. __MoviePy:__ This library is used for video editing tasks such as extracting audio from video files, attaching audio to video files, and manipulating video files.

2. __PyDub:__ PyDub is a Python library used for audio manipulation. It's used in this code for splitting MP3 files into segments.

3. __os:__ This is a built-in Python module used for interacting with the operating system. It's used for file operations such as creating directories and checking file paths.

4. __faster_whisper:__ This appears to be a custom library or module used for transcribing audio. The WhisperModel is mentioned in the TranscribeSRT class for transcribing MP3 files.

5. __deep_translator:__ This library seems to be used for translation purposes. It's mentioned in the TranscribeSRT class for translating text, likely the transcribed subtitles, into a specified language.

6. __init:__ This module seems to be a custom module created for the project, as indicated by the from modules imports. It contains various classes and methods used for audio and video processing tasks.



