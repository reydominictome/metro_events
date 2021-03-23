var modal = document.getElementById("request_form");
var btn = document.getElementById("goto_request_section");
var span = document.getElementsByClassName("close_request")[0];

btn.onclick = function() {
	modal.style.left = "540px";
}
		span.onclick = function() {
		   modal.style.left = "2200px";
		}
		window.onclick = function(event) {
		  if (event.target == modal) {
		    modal.style.display = "none";
		    modal.style.opacity = "0";
		  }
		}

		var myVar;

		function myFunction() {
		  myVar = setTimeout(showPage, 1500);
		}

		function showPage() {
		  document.getElementById("loader").style.display = "none";
		  document.getElementById("myDiv").style.display = "block";
		}


var hover = ["goto_request","goto_events_list","goto_admin_org","goto-profile","goto-notif"];


var hover1 = document.getElementById(hover[0]);
var hover2 = document.getElementById(hover[1]);
var hover3 = document.getElementById(hover[2]);
var hover4 = document.getElementById(hover[3]);
var hover5 = document.getElementById(hover[4]);