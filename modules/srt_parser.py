class SRTParser:
    def __init__(self) -> None:
        pass
    def extract_first_subtitle_info(self, srt_file):
        try:
            with open(srt_file, 'r', encoding="UTF-8", errors = "replace") as file:
                lines = file.readlines()

                # Initialize variables to store subtitle information
                current_subtitle_index = None
                current_subtitle_text = ""
                start_time = None
                end_time = None

                # Loop through each line in the SRT file
                for line in lines:
                    line = line.strip()

                    # If the line is a number, it indicates the subtitle index
                    if line.isdigit():
                        current_subtitle_index = int(line)

                        # Check if the subtitle index is 1 (first subtitle)
                        if current_subtitle_index == 1:
                            current_subtitle_text = ""
                    # If the line is empty, it indicates the end of a subtitle
                    elif not line:
                        # Check if the current subtitle index is 1
                        if current_subtitle_index == 1:
                            # Print the information of the first subtitle
                            return start_time, end_time, current_subtitle_text
                    # If the line contains a time range (00:00:00 --> 00:00:01)
                    elif "-->" in line:
                        # Extract start and end times
                        start, end = line.split(" --> ")
                        start_time = start.strip()
                        end_time = end.strip()
                    # Otherwise, it's part of the subtitle text
                    else:
                        # Concatenate the text of the current subtitle
                        current_subtitle_text += line + " "
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    def extract_all_subtitle_info(self, srt_file):
        subtitles = []
        try:
            with open(srt_file, 'r', encoding="UTF-8", errors = "replace") as file:
                lines = file.readlines()

                # Initialize variables to store subtitle information
                current_subtitle_index = None
                current_subtitle_text = ""
                start_time = None
                end_time = None

                # Loop through each line in the SRT file
                for line in lines:
                    line = line.strip()

                    # If the line is a number, it indicates the subtitle index
                    if line.isdigit():
                        current_subtitle_index = int(line)

                        # Check if the subtitle index is 1 (first subtitle)
                        if current_subtitle_index == 1:
                            current_subtitle_text = ""
                    # If the line is empty, it indicates the end of a subtitle
                    elif not line:
                        # Store subtitle information in a dictionary
                        subtitle_info = {
                            "start": start_time,
                            "end": end_time,
                            "text": current_subtitle_text.strip()  # Strip leading/trailing spaces
                        }
                        subtitles.append(subtitle_info)
                        # Reset subtitle text for the next subtitle
                        current_subtitle_text = ""
                    # If the line contains a time range (00:00:00 --> 00:00:01)
                    elif "-->" in line:
                        # Extract start and end times
                        start, end = line.split(" --> ")
                        start_time = start.strip()
                        end_time = end.strip()
                    # Otherwise, it's part of the subtitle text
                    else:
                        # Concatenate the text of the current subtitle
                        current_subtitle_text += line + " "

            # Add the last subtitle after the loop ends
            subtitle_info = {
                "start": start_time,
                "end": end_time,
                "text": current_subtitle_text.strip()  # Strip leading/trailing spaces
            }
            subtitles.append(subtitle_info)

            return subtitles
        except FileNotFoundError:
            print("File not found.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    def get_all_text(self, srt_file):
            all_data = self.extract_all_subtitle_info(srt_file=srt_file)
            return [sub["text"] for sub in all_data]