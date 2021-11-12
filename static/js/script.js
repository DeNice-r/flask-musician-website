let a = document.querySelectorAll('.nav-a')

let page_name = window.location.href

if(page_name.endsWith('/')){
    a[0].classList.remove('btn-dark')
    a[0].classList.add('btn-secondary')
}

if(page_name.endsWith('about')){
    a[1].classList.remove('btn-dark')
    a[1].classList.add('btn-secondary')
}

if(page_name.endsWith('history')){
    a[2].classList.remove('btn-dark')
    a[2].classList.add('btn-secondary')
}

if(page_name.endsWith('albums')){
    a[3].classList.remove('btn-dark')
    a[3].classList.add('btn-secondary')
}
if(page_name.endsWith('login')){
    a[4].classList.remove('btn-dark')
    a[4].classList.add('btn-secondary')
}

