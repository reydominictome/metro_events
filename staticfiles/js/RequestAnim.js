   $(document).ready( function () {
            let initialTableSettings = {
              searching: true
              //dom: 'lrtBi<"posR"p>'
            }

            let table = $('#movieTable').DataTable(initialTableSettings);

            $("input[type=date][name$=min]").val(new Date(0).toISOString().slice(0,10));
            $("input[type=date][name$=max]").val(new Date().toISOString().slice(0,10));
            //Logic that used in order to filter the table
            let dateRangeFunc = function (settings, data, dataIndex) {
                    let min = new Date($('#min').val()).getTime();
                    let max = new Date($('#max').val()).getTime();
                    let date = new Date(data[0]).getTime(); // use data for the column to range filter
                    if ( min <= date && date <= max ) {
                        return true;
                    }
                    return false;
                }
            
            //Here we will put the custom date range filter to the table
            $.fn.dataTable.ext.search.push(dateRangeFunc);

            //NOW, we need to refresh the table each time so that we could see the filtered data!
            $('#min, #max').change( function() {
                table.draw();//Artist maning javascript diay
            });

            //Reset the table
            $('#resetDateRange').click(function () {
                $("input[type=date][name$=min]").val(new Date(0).toISOString().slice(0,10));
                $("input[type=date][name$=max]").val(new Date().toISOString().slice(0,10));
                table.draw();
            });
        } );

var modal = document.getElementById("filter-section");
var btn = document.getElementById("filter");
var span = document.getElementsByClassName("cancel-filter")[0];
var modal2 = document.getElementsByClassName("Rectangle_121")[0];

var desc = document.getElementById("see_description");
var minimize = document.getElementById("minimize-desc");
var accept = document.getElementById("request-accepted");
var denied = document.getElementById("Denied");

var cont = document.getElementById("contact");
var minimize2 = document.getElementsByClassName("minimize-cont");


function minimCont() {
    cont.style.top="-1500px";
}

function gotoContact() {
   cont.style.top="141px";
}


document.getElementById("view_desc").onclick = function() {viewDesc()};

function viewDesc(){
	desc.style.top="204px"
}

minimize.onclick = function() {
	desc.style.top="1500px"
}
accept.onclick = function() {
	desc.style.top="1500px"
}
denied.onclick = function() {
	desc.style.top="1500px"
}



btn.onclick = function() {
	if(modal2.style.transitionDelay=="0.5s"){
		modal2.style.transitionDelay="0s";
	}
	modal.style.transitionDelay = "0.5s";
	modal.style.height = "290px";
	modal2.style.width = "900px";
}
span.onclick = function() {
	if(modal.style.transitionDelay=="0.5s"){
		modal.style.transitionDelay="0s";
	}
	modal.style.height = "0px";
	modal2.style.transitionDelay = "0.5s";
	modal2.style.width = "46px";
}

function applyFilter() {
	modal.style.height = "0px";
  document.getElementById("myFilter").submit();
  
}



function uncheckElements()
{
 var uncheck=document.getElementsByTagName('input');
 for(var i=0;i<uncheck.length;i++)
 {
  if(uncheck[i].type=='checkbox')
  {
   uncheck[i].checked=false;
  }
  if(uncheck[i].type=='date')
  {
   uncheck[i].value="";
  }
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