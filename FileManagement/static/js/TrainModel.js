

function ekUpload(){  
    function Init() {  
        var fileSelect = document.getElementById('file-upload'),  
            fileDrag = document.getElementById('file-drag');  
            // submitButton = document.getElementById('submit-button');  

        fileSelect.addEventListener('change', fileSelectHandler, false);  

        // Is XHR2 available?  
        var xhr = new XMLHttpRequest();  
        if (xhr.upload) {  
            // File Drop  
            fileDrag.addEventListener('dragover', fileDragHover, false);  
            fileDrag.addEventListener('dragleave', fileDragHover, false);  
            fileDrag.addEventListener('drop', fileSelectHandler, false);  
        }  
        
    }  

    function fileDragHover(e) {  
        var fileDrag = document.getElementById('file-drag');  
        e.stopPropagation();  
        e.preventDefault();  
        fileDrag.className = (e.type === 'dragover' ? 'hover' : 'modal-body file-upload');  
    }  

    function fileSelectHandler(e) {  
        var files = e.target.files || e.dataTransfer.files;  
        fileDragHover(e);  

        for (var i = 0, f; f = files[i]; i++) {  
            parseFile(f);  
            uploadFile(f);  
        }  
    }  

    function output(msg) {  
        var m = document.getElementById('messages');  
        m.innerHTML = msg;  
    }  

    function parseFile(file) {  
        console.log(file.name);  
        output('<strong>' + encodeURI(file.name) + '</strong>');  

        var fileName = file.name;  
        var isAllowed = fileName.endsWith('.doc') || fileName.endsWith('.docx') || fileName.endsWith('.pdf');  

        if (isAllowed) {  
            document.getElementById('start').classList.add("hidden");  
            document.getElementById('response').classList.remove("hidden");  
            document.getElementById('notimage').classList.add("hidden");   
        } else {   
            document.getElementById('notimage').classList.remove("hidden");  
            document.getElementById('start').classList.remove("hidden");  
            document.getElementById('response').classList.add("hidden");  
            output('يرجى اختيار ملف من نوع Word أو PDF فقط.');  
            document.getElementById("file-upload-form").reset();  
        }  
    }  

    function setProgressMaxValue(e) {  
        var pBar = document.getElementById('file-progress');  
        if (e.lengthComputable) {  
            pBar.max = e.total;  
        }  
    }  

    function updateFileProgress(e) {  
        var pBar = document.getElementById('file-progress');  
        if (e.lengthComputable) {  
            pBar.value = e.loaded;  
        }  
    }  

    function uploadFile(file) {  
        var xhr = new XMLHttpRequest(),  
            pBar = document.getElementById('file-progress'),  
            fileSizeLimit = 1024; // In MB  
        if (xhr.upload) {  
            // Check if file is less than x MB  
            if (file.size <= fileSizeLimit * 1024 * 1024) {  
                pBar.style.display = 'inline';  
                xhr.upload.addEventListener('loadstart', setProgressMaxValue, false);  
                xhr.upload.addEventListener('progress', updateFileProgress, false);  

            } else {  
                output('يرجى تحميل ملف أصغر من ' + fileSizeLimit + ' MB.');  
            }  
        }  
    }  

    if (window.File && window.FileList && window.FileReader) {  
        Init();  
    } else {  
        document.getElementById('file-drag').style.display = 'none';  
    }  
}  
ekUpload();


  
function showTable() {  
    document.getElementById('result-table').style.display = 'table';  // تغيير الحالة إلى 'table'  
}  


// $(document).ready(function() {  
// $('#submit-button').click(function(event) {  
//     // تأكد من منع الإرسال الافتراضي  
//     event.preventDefault();  
//     var fileInput = $('#file-upload')[0];  
//     var file = fileInput.files[0];  
//     var savePath = $('#getfolderModelSavePath').val();  

//     // تحقق من وجود ملف  
//     if (!file) {  
//         swal("خطأ!", "يرجى تحميل ملف ليتم تدريبه.", "error");  
//         return;  
//     }  

//     // تحقق من نوع الملف  
//     var validFileTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];  
//     if (!validFileTypes.includes(file.type)) {  
//         swal("خطأ!", "يرجى تحميل ملف بصيغة PDF أو Word.", "error");  
//         return;  
//     }  

//     var reader = new FileReader();  
//     reader.onload = function(event) {  
//         var content = event.target.result;  
//         // تحقق من محتوى الملف  
//         if (!content.trim()) {  
//             swal("خطأ!", "الملف الذي تم تحميله فارغ. يرجى تحميل ملف يحتوي على بيانات نصية.", "error");  
//             return;  
//         }  

//         // إذا كانت جميع الشروط صحيحة، قم بإرسال النموذج يدويًا  
//         $('#training-status').show();  
//         startLoadingDots(); 
//         $('#file-upload-form').submit();  // قم باستدعاء عملية إرسال النموذج  
//     };  
    
//     reader.onerror = function() {  
//         swal("خطأ!", "حدثت مشكلة أثناء قراءة الملف. يرجى التحقق من الملف.", "error");  
//     };  

//     reader.readAsText(file); // قراءة محتوى الملف  
// });  
// });  

// function startLoadingDots() {  
// let dots = $('.dots');  
// let dotCount = 0;  

// dots.show(); // إظهار العناصر  
// dots.html(''); // مسح النقاط السابقة  

// // وظيفة لإضافة النقاط  
// let interval = setInterval(function() {  
//     dotCount = (dotCount + 1) % 4; // عدد النقاط 3 (..)  
//     dots.html('.'.repeat(dotCount)); // تكرار النقاط  
// }, 500);  

// return interval; // إرجاع معرف الفترة  
// } 
