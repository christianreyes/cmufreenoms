// Handler for .ready() called.
$(function(){	
	highlight_current_tab();
		
	var descriptions = $('#reports .description');
	descriptions.each(function(index, description){
		description = $(description);
		var description_words = description.text().split(" ");
	
		for(var i=0 ; i < description_words.length; i++){
			var hash_word = description_words[i];
		
			if(hash_word.match(/#.*/)){
				var word = hash_word.substring(1,hash_word.length);
				var tag_link = $('<a class="tagged_food"></a>');
				tag_link.attr("href", "/find/" + word); 
				tag_link.text(hash_word);
				description_words[i] = tag_link[0].outerHTML;
				
			}
		}
		description.html(description_words.join(" "));
		$('#reports .description .tagged_food').click(function(e){
			searchKeyPressed(e, $(this).attr('href').match(/find\/(.*)/)[1]);
			setSearchText();
			return false;
		});
	});
	
	$('#reports .location').click(function(e){
		searchKeyPressed(e, $(this).attr('href').match(/find\/(.*)/)[1]);
		setSearchText();
		return false;
	});
	
	$('#find_search_box').bind("keydown", function(e){
		element = this;
		setTimeout(function(){ searchKeyPressed(e,$(element).val()); }, 1);
	});
	
	setSearchText();
	displayNoticeIfNone();
});

function displayNoticeIfNone(){
	var visible = $('#reports li.visible');
	var no_results = $('#no_results');
	if(visible.length == 0){
		no_results.removeClass("hidden");
	} else {
		no_results.addClass("hidden");
	}
}

function setSearchText(){
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
}

function searchKeyPressed(e, search_val){
	if(search_val != ""){
		document.title = 'FREE NOMS! - Find  "' + search_val + '"';
	} else {
		document.title = 'FREE NOMS! - Find';
	}

	updateSearchURL(search_val);
	filterReports(search_val);
	displayNoticeIfNone();
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
			val.removeClass("hidden");
			val.addClass("visible")
		} else {
			val.addClass("hidden");
			val.removeClass("visible")
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
