// Get current date
var today = new Date();
var day = today.getDate();
/*if (day < 10) {
  day = '0' + day
}*/
var out = document.getElementById("date-num");
out.innerHTML = day;

// Time
$(document).ready(function() {
	setInterval(function(){
		getTime();
	}, 50);
	function getTime() {
		var d = new Date();
		var s = d.getSeconds() + (d.getMilliseconds()/1000);
		var m = d.getMinutes();
		var h = hour12();	
		$(".hand-sec").css("transform", "rotateZ(" + s*6 + "deg)");
		$(".hand-min").css("transform", "rotateZ(" + m*6 + "deg)");
		$(".hand-hour").css("transform", "rotateZ(" + (h*30 + m*0.5) + "deg)");
		function hour12() {
			var hour = d.getHours();
			if(hour >= 12) {
				hour = hour-12;
			}
			if(hour == 0) {
				h = 12;
			}
			return hour;
		}
	}
});