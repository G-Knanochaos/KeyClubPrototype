

var ID = "home-count-down"
function setId(id) {
    ID = id
}
// Update the count down every 1 second
function countDown(date) {

var countDownDate = new Date(Date.parse(date)).getTime();

// Get today's date and time
var now = new Date().getTime();

// Find the distance between now and the count down date
var distance = countDownDate - now;

// Time calculations for days, hours, minutes and seconds
var time = {
    days : Math.floor(distance / (1000 * 60 * 60 * 24)),
    hours : Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
    minutes : Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
    seconds : Math.floor((distance % (1000 * 60)) / 1000)
}

// Display the result in the element with id="demo"
document.getElementById(ID).childNodes.forEach(element => {
    element.innerHTML = time[element.id] + " " + element.id 
});

// If the count down is finished, write some text
if (distance < 0) {
    clearInterval(x);
    document.getElementById(ID).innerHTML = "NOW!!!";
}
}