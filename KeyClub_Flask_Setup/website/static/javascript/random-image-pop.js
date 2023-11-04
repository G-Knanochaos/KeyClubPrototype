function populate(id = "random-image") {
    let elm = document.getElementsByClassName(id)
    let request = new Request("https://script.google.com/macros/s/AKfycbz8DFStA8H6c-VMfsryOgBksfUNSbLD7qr7_vPlq33Zp9QWrgKeXSOFQhUyQwuvnBlk/exec").json()
    request = request["links"]
    for (var i = 0; i < elm.length; i++) {
        elm[i].setAttribute("src",request[i])
    }
}