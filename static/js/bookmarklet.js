
(function(){
    var siteUrl = 'https://127.0.0.1:8000/';
    var styleUrl = siteUrl + 'static/css/bookmarklet.css';
    var minWidth = 250;
    var minHeight = 250;

    // ১. CSS লোড করা
    var head = document.getElementsByTagName('head')[0];
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.type = 'text/css';
    link.href = styleUrl + '?r=' + Math.floor(Math.random() * 9999999999999999);
    head.appendChild(link);

    // ২. HTML ওভারলে কন্টেইনার তৈরি করা
    var body = document.getElementsByTagName('body')[0];
    var boxHtml = `
        <div id="bookmarklet">
            <a href="#" id="close">&times;</a>
            <h1>Select an image to bookmark:</h1>
            <div class="images"></div>
        </div>`;
    body.innerHTML += boxHtml;

    // ৩. মূল ফাংশন (যা ছবি স্ক্যান করবে এবং ইভেন্ট হ্যান্ডেল করবে)
    function bookmarkletLaunch() {
        var bookmarklet = document.getElementById('bookmarklet');
        var imagesFound = bookmarklet.querySelector('.images');
        imagesFound.innerHTML = '';
        bookmarklet.style.display = 'block';

        // ওভারলে বন্ধ করার ইভেন্ট
        bookmarklet.querySelector('#close').addEventListener('click', function(){
            bookmarklet.style.display = 'none';
        });

        // নির্দিষ্ট সাইজের ছবি খুঁজে বের করা
        var images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
        images.forEach(image => {
            if(image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
                var imageFound = document.createElement('img');
                imageFound.src = image.src;
                imagesFound.append(imageFound);
            }
        });

        // ছবির ওপর ক্লিক করলে ব্যাকএন্ডে ডেটা পাঠানোর লজিক
        imagesFound.querySelectorAll('img').forEach(image => {
            image.addEventListener('click', function(event){
                var imageSelected = event.target;
                bookmarklet.style.display = 'none';
                window.open(siteUrl + 'images/create/?url=' 
                    + encodeURIComponent(imageSelected.src) 
                    + '&title=' 
                    + encodeURIComponent(document.title), 
                    '_blank');
            });
        });
    }

    // ৪. ফাংশনটি কল করা
    bookmarkletLaunch();
})();