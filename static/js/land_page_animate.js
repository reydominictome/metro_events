var circle = document.getElementById("move_circle");
var move1 = document.getElementById("Group_53");
var move2 = document.getElementById("Group_56");
var move3 = document.getElementById("Sign-in-form");

var move4 = document.getElementById("Sign-up-form");
var move5 = document.getElementById("Group_68");
var move6 = document.getElementById("Group_69");

var gotosignupbtn = document.getElementById("goto-sign-up");
var gotosigninbtn = document.getElementById("goto-sign-in");

var myVar;

gotosignupbtn.onclick = function() {
 	circle.style.left = "1100px";
 	move1.style.left = "-900px";
 	move2.style.left = "-1200px";
 	move3.style.left = "2200px";

 	move4.style.left = "0px";
 	move5.style.left = "1426px";
 	move6.style.left = "722.147px";
}

gotosigninbtn.onclick = function() {
 	circle.style.left = "-449px";
 	move1.style.left = "466.47px";
 	move2.style.left = "0px";
 	move3.style.left = "1319px";

 	move4.style.left = "-2200px";
 	move5.style.left = "2200px";
 	move6.style.left = "2200px";
}	

function myFunction() {
  myVar = setTimeout(showPage, 1000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDiv").style.display = "block";

}
