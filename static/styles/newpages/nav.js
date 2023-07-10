const ham=document.getElementById('ham');
const nav=document.getElementById("navbar")
const close=document.getElementById("close")

close.addEventListener("click",()=>{
    nav.style.left="-100%"
})

ham.addEventListener("click",()=>{
    if(nav.style.left==""||nav.style.left=="-100%"){
        nav.style.left="0px";
    }
    else{
        nav.style.left="-100%"
    }

})