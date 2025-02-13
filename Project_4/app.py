from fastapi import FastAPI, UploadFile, File
import subprocess
import whisper
import json
import os
from pydantic import BaseModel
from transformers import pipeline
from datetime import datetime

app = FastAPI()

# Define output model
class MoMResponse(BaseModel):
    title: str
    date: str
    participants: list
    key_points: list
    action_items: list

# Function to extract audio from video
def extract_audio(video_path: str, audio_path: str):
    command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path]
    subprocess.run(command, check=True)

# Function to transcribe audio
def transcribe_audio(audio_path: str):
    model = whisper.load_model("small")  # Use a free model from Hugging Face
    result = model.transcribe(audio_path)
    return result["text"]

# Function to generate a title based on summary
def generate_title(summary_text: str):
    title_generator = pipeline("text2text-generation", model="t5-small")
    title = title_generator(f"summarize: {summary_text}", max_length=15, min_length=5, do_sample=False)[0]["generated_text"]
    return title

# Function to extract action items dynamically
def extract_action_items(summary_text: str):
    action_item_generator = pipeline("text2text-generation", model="t5-small")
    action_items = action_item_generator(f"Extract action items: {summary_text}", max_length=50, min_length=10, do_sample=False)[0]["generated_text"].split(";")
    return [item.strip() for item in action_items if item.strip()]

# Function to summarize transcription dynamically
def summarize_text(transcription: str):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary_text = summarizer(transcription, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]
    
    title = generate_title(summary_text)
    action_items = extract_action_items(summary_text)
    
    summary = {
        "title": title,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "key_points": summary_text.split(".")[:-1],  # Splitting summary into key points
        "action_items": action_items if action_items else ["No specific action items identified"]
    }
    return summary

@app.post("/generate-mom", response_model=MoMResponse)
def generate_mom(file: UploadFile = File(...)):
    video_path = f"temp_{file.filename}"
    audio_path = video_path.replace(".mp4", ".mp3")
    
    with open(video_path, "wb") as f:
        f.write(file.file.read())
    
    extract_audio(video_path, audio_path)
    transcription = transcribe_audio(audio_path)
    mom = summarize_text(transcription)
    
    os.remove(video_path)
    os.remove(audio_path)
    
    return mom

@app.get("/")
def home():
    return {"message": "Minutes of Meeting (MoM) API is running!"}
