document.addEventListener('DOMContentLoaded',()=>{
    let profile_pic = document.querySelector('#profile-pic');
    let close_btn = document.querySelector('.close-button');
    let input = document.querySelector('.input-container');
    profile_pic.addEventListener('click',()=>{
        input.style.display='block';
    })
    close_btn.addEventListener('click',()=>{
        input.style.display='none';
    })
})