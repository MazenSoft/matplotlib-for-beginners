function ekUpload(){  
    function Init() {  
        var fileSelect = document.getElementById('custom-file-upload'),  // تغيير هنا  
            fileDrag = document.getElementById('custom-file-drag');  // تغيير هنا  

        fileSelect.addEventListener('change', fileSelectHandler, false);  
 
        var xhr = new XMLHttpRequest();  
        if (xhr.upload) {  
            fileDrag.addEventListener('dragover', fileDragHover, false);  
            fileDrag.addEventListener('dragleave', fileDragHover, false);  
            fileDrag.addEventListener('drop', fileSelectHandler, false);  
        }  
    }  

    function fileDragHover(e) {  
        var fileDrag = document.getElementById('custom-file-drag');  // تغيير هنا  
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
        var m = document.getElementById('custom-messages');  // تغيير هنا  
        m.innerHTML = msg;  
    }  

    function parseFile(file) {  
        console.log(file.name);  
        output('<strong>' + encodeURI(file.name) + '</strong>');  

        var fileName = file.name;  
        var isAllowed = fileName.endsWith('.doc') || fileName.endsWith('.docx') || fileName.endsWith('.pdf');  

        if (isAllowed) {  
            document.getElementById('custom-start').classList.add("hidden");  // تغيير هنا  
            document.getElementById('custom-response').classList.remove("hidden");  // تغيير هنا  
            document.getElementById('custom-notimage').classList.add("hidden");   // تغيير هنا  
        } else {   
            document.getElementById('custom-notimage').classList.remove("hidden");  // تغيير هنا  
            document.getElementById('custom-start').classList.remove("hidden");  // تغيير هنا  
            document.getElementById('custom-response').classList.add("hidden");  // تغيير هنا  
            output('يرجى اختيار ملف من نوع Word أو PDF فقط.');  
            document.getElementById("custom-file-upload-form").reset();  // تغيير هنا  
        }  
    }  

    function setProgressMaxValue(e) {  
        var pBar = document.getElementById('custom-file-progress');  // تغيير هنا  
        if (e.lengthComputable) {  
            pBar.max = e.total;  
        }  
    }  

    function updateFileProgress(e) {  
        var pBar = document.getElementById('custom-file-progress');  // تغيير هنا  
        if (e.lengthComputable) {  
            pBar.value = e.loaded;  
        }  
    }  

    function uploadFile(file) {  
        var xhr = new XMLHttpRequest(),  
            pBar = document.getElementById('custom-file-progress'),  // تغيير هنا  
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
        document.getElementById('custom-file-drag').style.display = 'none';  // تغيير هنا  
    }  
}  
ekUpload();