import openai
import google.generativeai as genai
from sqlalchemy.orm import Session
from crud import updateTranslationTask
from dotenv import load_dotenv

import os

load_dotenv()

#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


def perform_translation(task:int, text:str, languages:list, db:Session):
    translations = {}
    model = genai.GenerativeModel("gemini-1.5-flash")
    for lang in languages:
        try:
            messages = [
                {'role': "model", "parts": f"You are a helpful assistant that translates text into {lang}." },
                    {'role': "user", "parts": text},
                ],
            start_translation = model.generate_content(messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count = 1,
                    max_output_tokens=10000,
                    temperature=0.0,
                )
                )
            translations[lang] = start_translation.text
        except Exception as e:
            print(f"Error translating to {lang} : {e}")
            translations[lang] = f"Error : {e}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            translations[lang] = f"Unexpected Error: {e}"

                 
    updateTranslationTask(db, task, translations)


