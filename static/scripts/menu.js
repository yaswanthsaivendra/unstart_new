var menu = document.getElementById('menu')
var panel = document.getElementsByClassName('side-panel-container')[0]
var close = document.getElementById('close')
var body = document.getElementsByClassName("body")[0]
var navi = document.getElementsByClassName("navigation")[0]

menu.addEventListener("click", () => {
    panel.style.display = "block"
    body.style.filter = "blur(10px)"
    navi.style.filter = "blur(10px)"
    document.body.style.overflow = "hidden"
})

close.addEventListener("click", () => {
    panel.style.display = "none"
    body.style.filter = "none"
    navi.style.filter = "none"
    document.body.style.overflow = "scroll"
})