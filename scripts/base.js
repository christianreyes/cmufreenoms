// Handler for .ready() called.
$(function(){	
	highlight_current_tab();
	
	$("input#foods").tokenInput("/foods.json");
});

function highlight_current_tab(){
	var homeElement = $('img#report');
	var reportElement = $('div.report');
	var findElement = $('div.find');
	
	var atHome = homeElement.length > 0;
	var atReport = reportElement.length > 0;
	var atFind = findElement.length > 0;
	
	if(atHome){
		$('#menu li:nth-child(1)').css("background-color", "#eee");
		$('#menu li:nth-child(1)').css("border-bottom", "3px solid #bbb");
	} else if (atReport){
		$('#menu li:nth-child(2)').css("background-color", "#eee");
		$('#menu li:nth-child(2)').css("border-bottom", "3px solid #bbb");
	} else if (atFind){
		$('#menu li:nth-child(3)').css("background-color", "#eee");
		$('#menu li:nth-child(3)').css("border-bottom", "3px solid #bbb");
	}
}