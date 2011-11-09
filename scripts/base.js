// Handler for .ready() called.
$(function(){	
	highlight_current_tab();
	
	/*
	$("input#foods").tokenInput("/foods.json", {
		preventDuplicates : true,
		onAdd : function(){
			setHiddenValues();
		},
		onRemove: function(){
			setHiddenValues();
		}
	});
	*/
	
	$('#find_search_box').bind("keydown", function(e){
		element = this;
		setTimeout(function(){ searchKeyPressed(e,element); }, 1);
	});
	
	var path = window.location.pathname; 
	var path = decodeURIComponent(path);
	var matchData = path.match(/\/find\/(.*)/);
	
	if(matchData != null){
		$("#find_search_box").val(matchData[1]);
		filterReports(matchData[1]);
	} else {
		if(path.match(/^\/find$/)){
			window.history.pushState(null,null,"/find");
		}
	}
});

function searchKeyPressed(element){
	var search_val = $(element).val();
	
	if(search_val != ""){
		document.title = 'FREE NOMS! - Find  "' + search_val + '"';
	} else {
		document.title = 'FREE NOMS! - Find';
	}

	updateSearchURL(search_val);
	filterReports(search_val);
}

function updateSearchURL(val){
	window.history.replaceState(val, val, "/find/" + val );
}

function filterReports(searchVal){
	var searchRegExp = new RegExp(searchVal.toLowerCase());
	var reports = $('ul#reports li');
	
	$.each(reports, function(index, value){
		var val = $(value);
		if(value.textContent.toLowerCase().match(searchRegExp)){
			val.show();
		} else {
			val.hide();
		}
	});
}

function setHiddenValues(){
	var ids = [];
	
	var tokens = $("input#foods").tokenInput("get");
	
	for(var i=0; i<tokens.length ; i++){
		var token = tokens[i];
		
		ids.push(token.id);
	}
	
	$("input#selected_foods").val(ids)
}

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
