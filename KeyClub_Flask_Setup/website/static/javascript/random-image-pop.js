async function populate(c = "random-image") {
    let elm = document.querySelectorAll("."+c);
    fetch("https://script.google.com/macros/s/AKfycbyg4GQoJQo5-qsfW4-5R8yIFIKkkPKCOwUI9IyZsIGNgJmg5dHGcEhN0MRCPkFyAp4r/exec?n=" + String(elm.length))
  .then((response) => response.json())
  .then((json) => {
    json = json["links"]
    for (var i = 0; i < json.length; i++) {
        elm[i].setAttribute("src",json[i])
    }
});
}