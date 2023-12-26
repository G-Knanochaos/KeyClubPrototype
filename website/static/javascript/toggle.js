function toggle(id) {
    elm = document.getElementById(id)
    if (elm.style["display"]== "none"){
        console.log("hello!")
        elm.style["display"] = "grid"
    }
    else {
        console.log("bye bye")
        elm.style["display"] = "none"
    }
}