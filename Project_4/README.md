# Quick-Minutes-of-Meeting-using-ChatGPT

# MoM Generator

This project is an automated MoM (Minute of Meeting) generator. It takes in a video file and generates the MoM in form of bullet points.

## Features

- Upload video file and generate MoM
- Automatically converts video to audio
- Automatically transcribes audio file
- Automatically generates MoM in form of bullet points

# Explanation

## MoMResponse(BaseModel):
- This is a Pydantic model that defines the structure of the API's response. Pydantic is used for data validation and settings management. It ensures that the output returned by the API conforms to a specific format.
- It includes fields like title (string), date (string), participants (list of strings), key_points (list of strings), and action_items (list of strings).

## extract_audio(video_path: str, audio_path: str):
- This function extracts the audio from a video file using ffmpeg.
- It takes the path to the video file (video_path) and the desired path for the extracted audio file (audio_path) as input.
- It uses the subprocess.run() method to execute the ffmpeg command. The check=True argument raises an exception if the command fails.
ffmpeg is a command-line tool used for handling multimedia files. The command converts the video to an audio file.

```bash
ffmpeg -i input.mp4 -q:a 0 -map a output.mp3
```

*   `-i input.mp4`: Specifies the input video file.
*   `-q:a 0`:  Sets the audio quality to the highest.
*   `-map a`:  Specifies that only the audio stream should be extracted.
*   `output.mp3`: Specifies the output audio file.

## transcribe_audio(audio_path: str):
- This function transcribes an audio file into text using the Whisper model.
- It takes the path to the audio file (audio_path) as input.
whisper.load_model("small") loads a pre-trained Whisper model. The "small" model is specified for being a free model from Hugging Face.
- model.transcribe(audio_path) performs the transcription, and the function returns the transcribed text from the "text" key of the result.


## generate_title(summary_text: str):
- This function generates a title for a given summary text using a text-to-text generation pipeline.
- It takes the summary text (summary_text) as input.
- It initializes a text2text-generation pipeline using the t5-small model from Hugging Face.
- The pipeline is then used to generate a title from the summary text, with a specified maximum and minimum length. The function returns the generated title.


## extract_action_items(summary_text: str):
- This function extracts action items from a summary text using a text-to-text generation pipeline.
- It takes the summary text (summary_text) as input.
- It initializes a text2text-generation pipeline using the t5-small model from Hugging Face.
- The pipeline is used to extract action items from the summary text. The generated text is split into a list of items. The function returns a list of stripped action items.

## summarize_text(transcription: str):
- This function summarizes a given text transcription and extracts key information such as the title, action items, and key points.
- It takes the transcription text (transcription) as input.
- It initializes a summarization pipeline using the facebook/bart-large-cnn model.
- The pipeline is used to generate a summary of the transcription, with specified maximum and minimum lengths.
- It calls generate_title() and extract_action_items() to get the title and action items from the summary.
- It constructs a dictionary containing the title, date, participants, key points (split from the summary), and action items. The function returns this dictionary.

## generate_mom(file: UploadFile = File(...)):
- This is an API endpoint (defined using @app.post("/generate-mom")) that generates Minutes of Meeting (MoM) from an uploaded video file.
- It receives the uploaded file as an UploadFile object15. File(...) indicates that FastAPI will automatically parse the incoming request and extract the file data3.
- It saves the uploaded video file to a temporary location, extracts the audio from the video, transcribes the audio, summarizes the transcription, and then removes the temporary files.
- video_path = f"temp_{file.filename}" creates a temporary file name based on the original file name3.
- file: UploadFile = File(...) specifies that the file parameter is expected to be of type UploadFile, which is used to handle uploaded files3.
- It returns the generated MoM data as a MoMResponse object.

## home():
- This is a simple API endpoint (defined using @app.get("/")) that returns a welcome message.
- It simply returns a JSON response with a message indicating that the Minutes of Meeting (MoM) API is running.



# FastAPI and File Uploads:
1. The UploadFile class is used to receive files from the request.
2. python-multipart needs to be installed to support file uploads, as uploaded files are sent as "form data".
3. The @app.post decorator is a FastAPI decorator indicating that the following function will handle POST requests to the specified endpoint.