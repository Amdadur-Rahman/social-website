const siteUrl = '//127.0.0.1.8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const mainWidth = 250;
const mainHeight = 250;

// add css
let head = document.getElementsByTagName('head')[0];
let link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random() *9999999999999999);
head.appendChild(link);

// load html
let body = document.getElementsByTagName('body')[0];
boxHtml = `
<div id="bookmarklet">
    <a href="#" id="close">@times;</a>
    <h1>select an image to bookmark:</h1>
    <div class="images"></div>
</div>`;
body.innerHTML += boxHtml;


function bookmarkletLaunch() {
    bookmarklet = document.getElementById('bookmarklet');
    let imagesFound = bookmarklet.querySelector('.images');
    imagesFound.innerHTML = '';
    bookmarklet.style.display = 'block';

    bookmarklet.querySelector('#close')
    .addEventListener('click',function(){
        bookmarklet.style.display = 'none'
    })
}

images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"] ');
images.forEach(image => {
    if (image.naturalWidth >= mainWidth && image.naturalHeight >= mainHeight){
        let imageFound = document.createElement('img');
        imageFound.src = image.src;
        imagesFound.append(imageFound);
    }
})

bookmarkletLaunch()