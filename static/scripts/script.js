var noti = document.getElementsByClassName('noti-icon')[0]
var noti_list = document.getElementsByClassName('notification-list-container')[0]

var profile = document.getElementsByClassName('image')[0]
var prof_list = document.getElementsByClassName('profile-container')[0]

noti.addEventListener("click", () => {
    if(noti_list.className === "notification-list-container noti-notdisplay")
    {
        noti_list.className = "notification-list-container noti-display"
        // noti.style.content = "url('rsc/icons8-notification.gif')"
        prof_list.className = "profile-container prof-notdisplay"
        // profile.style.border = "none"
    }
    else
    {
        noti_list.className = "notification-list-container noti-notdisplay"
        // noti.style.content = "url('rsc/icons8-notification-48\ \(1\).png')"
    }
})

profile.addEventListener("click", () => {
    if(prof_list.className === "profile-container prof-notdisplay")
    {
        prof_list.className = "profile-container prof-display"
        // profile.style.border = "3px solid #ffc824"
        noti_list.className = "notification-list-container noti-notdisplay"
        // noti.style.content = "url('rsc/icons8-notification-48\ \(1\).png')"
    }
    else
    {
        prof_list.className = "profile-container prof-notdisplay"
        // profile.style.border = "none"
    }
})

body.addEventListener("click", () => {
    if(noti_list.className === "notification-list-container noti-display")
    {
        noti_list.className = "notification-list-container noti-notdisplay"
    }
    if(prof_list.className === "profile-container prof-display")
    {
        prof_list.className = "profile-container prof-notdisplay"
    }
})
