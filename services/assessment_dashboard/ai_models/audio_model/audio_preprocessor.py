from pydub import AudioSegment
import subprocess
import shutil
import os

class AudioPreprocessor:

    def convert_to_wav(self, input_file, output_file):
        # Determine the format from the file extension
        file_format = input_file.split('.')[-1].lower()
        
        # Load the audio file
        audio = AudioSegment.from_file(input_file, format=file_format)
        
        # Export the audio as a wav file
        audio.export(output_file, format="wav")

    def clean_audio_with_demucs(self, input_file, output_file):
        # Run demucs using subprocess with the old default model
        subprocess.run(["demucs", "-n", "mdx_extra_q", input_file])

        # Move the vocal output to a target cleaned file
        vocals_path = f"separated/mdx_extra_q/{input_file.split('/')[-1].replace('.wav', '')}/vocals.wav"
        shutil.copy(vocals_path, output_file)

        # Delete the entire demucs output folder structure
        demucs_base_folder = "separated"
        if os.path.exists(demucs_base_folder):
            shutil.rmtree(demucs_base_folder, ignore_errors=True)

    def preprocess_and_clean(self, input_file_path):
        # Get input file directory and name
        input_dir = os.path.dirname(input_file_path)
        base_name = os.path.basename(input_file_path)
        name_without_ext = os.path.splitext(base_name)[0]

        # Convert to wav if necessary
        if not input_file_path.lower().endswith('.wav'):
            wav_file = os.path.join(input_dir, f"{name_without_ext}.wav")
            self.convert_to_wav(input_file_path, wav_file)
            # Delete the original non-wav file
            os.remove(input_file_path)
        else:
            wav_file = input_file_path

        # Clean the audio and save the vocals in same directory as input
        cleaned_vocals_path = os.path.join(input_dir, f"{name_without_ext}.wav")
        self.clean_audio_with_demucs(wav_file, cleaned_vocals_path)

        return cleaned_vocals_path
    
    def clean_audio_files(self, audio_file_paths):
        """
        Process multiple audio files and return list of cleaned file paths
        
        Args:
            audio_file_paths: List of paths to audio files
            output_directory: Directory to save processed files
            
        Returns:
            List of paths to cleaned audio files
        """
        cleaned_file_paths = []
        for audio_path in audio_file_paths:
            cleaned_path = self.preprocess_and_clean(audio_path)
            cleaned_file_paths.append(cleaned_path)
        return cleaned_file_paths


audio_preprocessor = AudioPreprocessor()