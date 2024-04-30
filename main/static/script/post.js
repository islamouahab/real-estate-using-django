const myCarouselElement = document.querySelector('#myCarousel')

const carousel = new bootstrap.Carousel(myCarouselElement, {
  interval: 2000,
  touch: false
})
function show_number(phone_num){
    let phone_num_label = document.querySelector('#phone_num_label');
    let num_btn = document.querySelector('.phone_num');
    phone_num_label.innerHTML=phone_num;
    num_btn.textContent="Hide phone number";
    num_btn.addEventListener('click',hide_num);
    
}
function hide_num(){
       let phone_num_label = document.querySelector('#phone_num_label');
       let num_btn = document.querySelector('.phone_num');
       phone_num_label.innerHTML="";
        num_btn.textContent="show phone number";
        num_btn.removeEventListener('click',hide_num);
}