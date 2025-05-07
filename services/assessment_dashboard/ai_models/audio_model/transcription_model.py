import requests
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydub import AudioSegment
import pandas as pd
class AudioTranscriptionTranslator:
    def __init__(self):
        self.transcription_url = "https://api.openai.com/v1/audio/transcriptions"
        self.chat = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
        )
        self.translation_prompt = PromptTemplate.from_template(
            input_variables=["text"],
            template="Translate the following Urdu text to English: {text}"
        )

    def get_transcription(self, audio_file_path):
        """Get transcription from audio file"""
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        with open(audio_file_path, "rb") as audio_file:
            files = {
                "file": (audio_file_path, audio_file, "audio/wav")
            }
            data = {
                "model": "gpt-4o-transcribe"
            }

            response = requests.post(
                self.transcription_url, 
                headers=headers, 
                files=files, 
                data=data
            )

        if response.ok:
            return response.json().get("text", "No text found.")
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def translate_to_english(self, text):
        """Translate text to English"""
        messages = self.translation_prompt.format_messages(text=text)
        response = self.chat(messages)
        return response.content

    def get_audio_duration(self, audio_file_path):
        """
        Get duration of audio file in seconds
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Duration of audio in seconds
        """
        try:
            audio = AudioSegment.from_wav(audio_file_path)
            duration_seconds = len(audio) / 1000.0  # Convert milliseconds to seconds
            return duration_seconds
        except Exception as e:
            print(f"Error getting duration for {audio_file_path}: {str(e)}")
            return None


    def transcribe_and_translate(self, audio_file_path, image_id):
        """Get transcription and translation in one go"""'
        duration_in_seconds = self.get_audio_duration(audio_file_path)
        urdu_transcription = self.get_transcription(audio_file_path)
        english_translation_for_urdu_transcription = self.translate_to_english(urdu_transcription)
        return {
            "image_id": image_id,
            "urdu_transcription": urdu_transcription,
            "english_translation_for_urdu_transcription": english_translation_for_urdu_transcription,
            "duration_in_seconds": duration_in_seconds
        }
    
    def transcribe_and_translate_audio_files(self, audio_file_paths):
        """
        Process multiple audio files and return list of transcriptions with translations
        
        Args:
            audio_file_paths: List of paths to audio files
            
        Returns:
            DataFrame containing transcription and translation for each file
        """
        results = []
        for audio_path in audio_file_paths:
            try:
                image_id = audio_path.split("/")[-4].split("_")[0]
                result = self.transcribe_and_translate(audio_path, image_id)
                results.append(result)
            except Exception as e:
                print(f"Error processing {audio_path}: {str(e)}")
                results.append({
                    "image_id": image_id,
                    "urdu_transcription": None,
                    "english_translation_for_urdu_transcription": None,
                    "duration_in_seconds": None
                })
        
        # Convert results list to DataFrame
        df = pd.DataFrame(results)
        return df
    

transcription_model = AudioTranscriptionTranslator()