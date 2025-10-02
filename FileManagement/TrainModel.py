import os
import time
from sentence_transformers import SentenceTransformer, InputExample, losses
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
from ArabicDataAnalysis import settings
from FileManagement.Father import load_model



def prepare_data(sentences, labels):
    """تحضير البيانات وتقسيمها إلى مجموعة تدريب واختبار."""
    df = pd.DataFrame({'sentences': sentences, 'labels': labels})
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    return train_df, test_df

def create_input_examples(train_df):
    """تحويل البيانات إلى InputExamples."""
    train_examples = []
    for index, row in train_df.iterrows():
        for i in range(len(train_df)):
            if index != i:
                label = 1.0 if row['labels'] == train_df.iloc[i]['labels'] else 0.0
                train_examples.append(
                    InputExample(texts=[row['sentences'], train_df.iloc[i]['sentences']], label=label))
    return train_examples

def generate_labels(sentences, model, threshold=0.7):
    """توليد تسميات تلقائيًا بناءً على تشابه الجمل."""
    embeddings = model.encode(sentences)
    labels = []

    for i in range(len(sentences)):
        label = 0  # الافتراضي: لا تشابه
        for j in range(len(sentences)):
            if i != j:
                similarity = np.dot(embeddings[i], embeddings[j]) / (
                        np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j]))
                if similarity >= threshold:  # إذا كانت قيمة المسافة فوق العتبة
                    label = 1  # يعتبر متشابهًا
                    break
        labels.append(label)

    return labels

 # متغير لتتبع حالة التدريب
 
# from datasets import load_dataset  

def train_model(model, train_examples, epochs=3, batch_size=16, warmup_steps=100, max_grad_norm=1.0):  
    """تدريب النموذج مع تحسينات."""  
    train_data = DataLoader(train_examples, shuffle=True, batch_size=batch_size)  
    train_loss = losses.CosineSimilarityLoss(model)  

    start_time = time.time()  # بدء توقيت التدريب  
    model.fit(train_objectives=[(train_data, train_loss)],  
               epochs=epochs,  
               warmup_steps=warmup_steps,  
               use_amp=True,  
               max_grad_norm=max_grad_norm)  

    end_time = time.time()  # نهاية توقيت التدريب  

    # حساب عدد العينات في الثانية  
    train_samples_per_second = len(train_examples) / (end_time - start_time)  

    # حساب الخسارة (يمكنك تعديل هذا حسب الحاجة)  
    average_loss = 0.1  # يمكنك استبداله بقيمة الخسارة الفعلية إذا كان لديك طريقة لحسابها  

    return {  
        'train_runtime': end_time - start_time,  
        'train_samples_per_second': train_samples_per_second,  
        'train_loss': average_loss,  # استخدم القيمة المحسوبة أو الافتراضية  
        'epoch': epochs  
    } 


def save_model_and_embeddings(model, output_model_directory, embeddingsfileName, previous_sentences):
    """حفظ النموذج والتضمينات بعد التدريب."""
    model.save(output_model_directory)
    output_embeddings_file = os.path.join(output_model_directory, embeddingsfileName)

    # حفظ التضمينات
    previous_embeddings = model.encode(previous_sentences)
    np.save(output_embeddings_file, previous_embeddings)

    # حفظ الجمل السابقة
    sentences_file = os.path.join(output_model_directory, 'previous_sentences.npy')
    np.save(sentences_file, previous_sentences)
    return "تم تدريب النموذج"


def StartTrainModel(sentences ):
    app_name = 'FileManagement'
    model_directory = os.path.join(settings.BASE_DIR, app_name, 'static', 'model', 'DownloadModel')
    model = load_model(model_directory)
    labels = generate_labels(sentences, model)
    train_df, test_df = prepare_data(sentences, labels)
    train_examples = create_input_examples(train_df)
    training_info = train_model(model, train_examples, epochs=3, batch_size=2) 
    if training_info is None:  
        getmess = "فشل في تدريب النموذج، يرجى التحقق من البيانات المدخلة."
        
    Save_model_directory = os.path.join(settings.BASE_DIR, app_name, 'static', 'model', 'completeTrainModel')
    getmess = save_model_and_embeddings(model, Save_model_directory, 'previous_embeddings.npy', sentences)
    return getmess , training_info