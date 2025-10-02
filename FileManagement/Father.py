
import os
import re
import joblib
import pandas as pd
from sentence_transformers import SentenceTransformer

from ArabicDataAnalysis import settings

def load_model(model_file_path):  
    # تحقق مما إذا كان النموذج موجودًا بالفعل كملف  
    if os.path.isfile(model_file_path):  
        print(f"Loading model from {model_file_path}")  
        model = SentenceTransformer(model_file_path)  
    else:  
        print(f"Model not found at {model_file_path}. Preparing to download...")  
        model = load_and_save_model(model_file_path)  
    return model  


def load_and_save_model(save_path):  
    model_name = 'silma-ai/silma-embeddding-matryoshka-v0.1'  
    print(f"Loading model: {model_name}")  
    model = SentenceTransformer(model_name)  
    model.save(save_path) 
    return model  

def load_classifier_model(model_Data_directory):
    """تحميل نموذج RandomForestClassifier المدرب."""
    classifier_path = os.path.join(settings.BASE_DIR, model_Data_directory, 'poetry_classifier.pkl')  # استخدم مسار نسبي
    model = joblib.load(classifier_path)
    return model

def load_classified_data(model_directory):
    """تحميل البيانات المصنفة من ملف CSV."""
    output_path = os.path.join(model_directory, 'classified_data.csv')  # استخدم مسار نسبي
    if os.path.exists(output_path):
        df = pd.read_csv(output_path, encoding='utf-8')
        return list(zip(df['Text'], df['Label']))
    return []

def clean_poetry(text):
    """تنظيف النص من الرموز وعلامات الترقيم."""
    cleaned_text = re.sub(r'[ًٌٍَُِّْ،؛؟!]', '', text)
    return cleaned_text