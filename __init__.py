import logging
import azure.functions as func
import openai
import io
import os


API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "Your_api_key")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "your_endpoint")
API_VERSION = "your_api_version"
model_name = "your_model_name"  
version = "your_version"


openai.api_type = "your_api_type"
openai.api_base = ENDPOINT
openai.api_key = API_KEY
openai.api_version = API_VERSION

def main(inputBlob: func.InputStream, outputBlob: func.Out[str]):
    logging.info(f"Processing file: {inputBlob.name}")

    try:
       
        if not inputBlob.name.endswith(".mp3"):
            logging.error("Invalid file format. Only MP3 files are supported.")
            return

        
        audio_data = inputBlob.read()
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "audio.mp3"  

        
        response = openai.audio.transcriptions.create(
            model=model_name,
            file=audio_file
        )


        try:
            transcribed_text = response.text
        except AttributeError:
            logging.error("Error extracting transcription from response.")
            return

      
        outputBlob.set(transcribed_text)
        logging.info(f"✅ Transcription saved: {transcribed_text[:100]}...")  

    except Exception as e:
        logging.error(f"❌ Error processing file: {str(e)}")
