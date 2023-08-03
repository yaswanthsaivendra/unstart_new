const coursebtn=document.querySelectorAll(".btn-course");
const coursepopup=document.querySelector(".course-popup");
const close=document.querySelector(".btn-close");
const coursecards=document.querySelectorAll(".course-card");

close.addEventListener("click",()=>{
    coursepopup.style.display="none"; 
})




coursebtn[0].addEventListener("click",()=>{
    if(coursepopup.style.display=="none" || coursepopup.style.display=="" || coursepopup.style.display==" "){
        coursepopup.style.display="flex";
    }
    else{
        coursepopup.style.display="none";        
    }
})

coursebtn[1].addEventListener("click",()=>{
    if(coursepopup.style.display=="none" || coursepopup.style.display=="" || coursepopup.style.display==" "){
        coursepopup.style.display="flex";
    }
    else{
        coursepopup.style.display="none";        
    }
})


coursecards.forEach((element)=>{
    const viewbtn=element.querySelector(".collapse");
    const list =element.querySelector(".list");
    viewbtn.addEventListener("click",()=>{
        if(list.style.display=="none" || list.style.display=="" || list.style.display==" "){
            list.style.display="block"
            viewbtn.textContent="Close Chapter Details"
        }
        else{
            list.style.display="none";
            viewbtn.textContent="View Chapter Details"
        }
    })
})