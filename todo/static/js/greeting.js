var today = new Date()
var curHr = today.getHours()


if (curHr < 12) {
    document.getElementById('greeting').innerHTML = 'Good morning!';
  } else if (curHr < 18) {
    document.getElementById('greeting').innerHTML = "Good afternoon, ";
  } else if (curHr < 21) {
    document.getElementById('greeting').innerHTML = "Good afternoon, ";
  } else {
    document.getElementById('greeting').innerHTML = "Good evening, ";
  }