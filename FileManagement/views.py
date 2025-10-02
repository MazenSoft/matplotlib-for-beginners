
from django.shortcuts import render
from django.http import JsonResponse  
from django.views.decorators.csrf import csrf_exempt  
# from FileManagement.DownloadModel import DownloadModelProcess , CheckPath
from FileManagement.ProcessFile import DataAnalysis
from io import BytesIO

from FileManagement.TrainModel import StartTrainModel
from FileManagement.TrainModel2 import StartModel2
from FileManagement.UsingModel import StartModel
from FileManagement.UsingModel2 import StartUsingModel2  


def Homepage(request) :
    return render(request , 'homepage.html')
   

# @csrf_exempt  
# def Download_Model(request):  
#     if request.method == 'POST':  
#         save_path = r'C:\Users\madha\Desktop\model\downloadModel'  
#         # تحقق من صحة المسار  
#         getmessage = CheckPath(save_path)  
#         if getmessage is not None:  
#             return render(request, 'DownloadModel.html', {'messages': [getmessage]})  
        
#         # إرجاع رسالة بدء تحميل النموذج  
#         initial_message = 'جاري تحميل النموذج...'  
#         # عرض الرسالة الأولى  
#         # توجيه المستخدم إلى صفحة جديدة بعد بدء التحميل  
#         # هنا يجب استخدام التحميل في الخلفية (يمكن استخدام خيط جديد أو مكتبة معينة للتعامل مع ذلك)  
#         result_message = DownloadModelProcess(save_path)  

#         return render(request, 'DownloadModel.html', {'messages': [initial_message, result_message]})  
    
#     return render(request, 'DownloadModel.html') 


@csrf_exempt  # استخدم فقط للاختبار في بيئة محلية  
def TrainModel(request):  
    if request.method == 'POST' and request.FILES.get('fileUpload'):   
        file = request.FILES['fileUpload']    
        file_stream = BytesIO(file.read())   
        try:  
            sentences = DataAnalysis(file_stream, file.content_type)  
            
            if sentences is not None:  
                getmess, training_info = StartTrainModel(sentences)   
                print("getmess")   
                print(getmess)   
                print(training_info)   
                return JsonResponse({  
                    'getmess': getmess,  
                    'training_info': training_info
                }, status=200)  
            
        except Exception as e:  
            return JsonResponse({'error': str(e)}, status=400)  
  
    return JsonResponse({'error': 'Invalid request'}, status=400)  

@csrf_exempt  # استخدم فقط للاختبار في بيئة محلية  
def TrainModel2(request):  
    if request.method == 'POST':  
        # استرداد البيانات  
        file = request.FILES.get('custom-file-upload')  # تأكد من استخدام الاسم الصحيح  
        text = request.POST.get('custom-textarea_input', '')  # استرجع قيمة textarea  
        name = request.POST.get('custom-Poet-name')  
        sentences = None  
        if file:  
            try:  
                file_stream = BytesIO(file.read())  
                sentences = DataAnalysis(file_stream, file.content_type)   
                # إذا كان هناك جمل ومحتوى نصي  
                getmess = StartModel2(sentences, text, name)   
                return JsonResponse({'getmess': getmess}, status=200)  
            except Exception as e:  
                return JsonResponse({'error': str(e)}, status=400)  

        if text:  # إذا كان هناك نص ولكن لا يوجد ملف 
            getmess = StartModel2(None, text, name)   
            return JsonResponse({'getmess': getmess}, status=200)  

    return JsonResponse({'error': 'طلب غير صالح.'}, status=400)   


@csrf_exempt  
def UsingModel(request):  
    results = []  # قائمة النتائج  
    getmess = ""  # تهيئة getmess في حالة عدم وجود نتائج  

    if request.method == 'POST':  
        getText = request.POST.get('textarea_input', '')  # استرجع قيمة textarea  
        getcount = request.POST.get('sentences_count')  # استرجع قيمة عدد الجمل  
        print("dsfsf" + getText)  
        print("dsf" + getcount)  

        # التحقق مما إذا كانت قيمة getcount صحيحة  
        if not getcount or not getcount.isdigit():  # تحقق إذا كانت None أو ليست رقمية  
            getmess = "يرجى إدخال عدد صحيح للجمل."  
            return JsonResponse({'getmess': getmess, 'results': []})  # إرجاع رسالة دون نتائج  

        # تحويل getcount إلى عدد صحيح  
        top_n = int(getcount)  # عدد الجمل الأكثر تشابهاً  

        # استدعاء الوظيفة الخاصة بنموذجك  
        results, getmess = StartModel(getText, top_n)  

        # تحويل النتائج إلى نوع بيانات قابل للتهيئة  
        results = [{'sentence': str(r[0]), 'score': float(r[1])} for r in results]  # تأكد من تحويل `score`  

        if not results:  
            getmess = "لا توجد نتائج لعرضها."  

        # إرجاع النتائج بتنسيق JSON  
        return JsonResponse({'getmess': getmess, 'results': results})  

    # إذا كان الطلب GET، عرض الصفحة بشكل عادي  
    return JsonResponse({'error': 'Invalid request'}, status=400)
@csrf_exempt  
def UsingModel2(request):   
    getmess = ""  
    if request.method == 'POST':  
        getText = request.POST.get('user_input_text', '')        
        try:  
            # استدعاء StartUsingModel2 والحصول على النتائج  
            result_dict = StartUsingModel2(getText)  # افترض أن النتائج ترجع كقاموس  
            results = result_dict["results"]  
            getmess = result_dict["getmess"]  

            # تحقق من بنية النتائج  
            if not isinstance(results, list) or not all(  
                isinstance(result, dict) and 'poet_name' in result and 'similarity_score' in result for result in results  
            ):  
                return JsonResponse({'error': 'Invalid results structure'}, status=500)  

            # إعداد النتائج لرد JSON  
            formatted_results = [  
                {"poet_name": result["poet_name"], "similarity_score": float(result["similarity_score"])}  
                for result in results  
            ]  
            
            return JsonResponse({'getmess': getmess, 'results': formatted_results})  
        except Exception as e:  
            return JsonResponse({'error': str(e)}, status=500)  

    return JsonResponse({'error': 'Invalid request'}, status=400)