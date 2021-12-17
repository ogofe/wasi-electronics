let nav_open = false;

const carousels = {
    reviews: {
        slides: document.querySelector('#reviews').querySelectorAll('.carousel-item'),
        dots: document.querySelector('#reviews').querySelector('.carousel-indicators').children,
    },
}
let idx;
let current = 0


function toggleNav(){
    if(nav_open){
        document.querySelector('.nav-wrapper').classList.replace('open', 'closed')
        nav_open = !nav_open            
    }else{
        document.querySelector('.nav-wrapper').classList.replace('closed', 'open')
        nav_open = !nav_open        
    }
}


function scrollNav(){
    if (document.body.scrollTop > 200){
        document.querySelector('#navbar').classList.add('scroll')
    }else{
        document.querySelector('#navbar').classList.remove('scroll')
    }
}

function scrollToTop(){
    if (document.body.scrollTop >= 2000){
        document.querySelector('#backtotop').classList.replace('hide', 'show')
    }else{
        document.querySelector('#backtotop').classList.replace('show', 'hide')
    }
}


document.querySelector('#backtotop').addEventListener("click", (ev) => {
    document.body.scrollTo({top: 0, behavior: "smooth"})
})

// let toggles = document.querySelectorAll('.dropdown-toggle');
// toggles.forEach((elem, idx) => {
//     elem.onclick = () => elem.parentElement.classList.toggle('open')
// });


function nextSlide(slide_id, num){
    let slides = carousels[`${slide_id}`].slides;
    let dots =  carousels[`${slide_id}`].dots;
    let max = slides.length-1;
    for (let index = 0; index < slides.length; index++) {
        let activeSlide = slides[index]
        if (activeSlide.classList.contains('active')){
            current = index
        }
        slides[index].classList.replace('active', 'closed')
        dots[index].classList.remove('active')
    }
    idx = current + num
    if (idx > max){
        idx = 0
    }
    if (idx < 0){
        idx = max
    }
    slides[idx].classList.replace('closed', 'active')
    dots[idx].classList.add('active')
}


document.getElementById('services__toggle').addEventListener('click', function(trigger){
    let drop_menu = trigger.target.parentElement;
    if (drop_menu.classList.contains('open')){
        drop_menu.classList.remove('open')
    }else{
        drop_menu.classList.add('open')        
    }
})

document.scrollingElement.onscroll = (event) => {
    scrollNav()
    scrollToTop()
}

this.setInterval(() => nextSlide('reviews', 1), 5000)
this.setInterval(() => nextSlide('projects', 1), 5000)
