$(document).ready(function () {
 // $("#clgResultTable").hide();
 $("#midTermResultTable").css("display", "none");
 $("#termResultTable").css("display", "none");
 $("#preTestResultTable").css("display", "none");
 $("#testResultTable").css("display", "none");
});




var hiddenDiv;

function replaceResult(hide, show) {
 document.getElementById(hide).style.display = "none";
 document.getElementById(show).style.display = "block";

}
function replaceResult1(hide, hide1, hide2, hide3, show) {
 document.getElementById(hide).style.display = "none";
 document.getElementById(hide1).style.display = "none";
 document.getElementById(hide2).style.display = "none";
 document.getElementById(hide3).style.display = "none";
 document.getElementById(show).style.display = "block";
}



