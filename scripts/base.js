// Handler for .ready() called.
$(function(){	
	highlight_current_tab();
	
	if($('.find').length > 0) {
		var descriptions = $('#reports .description');
		descriptions.each(function(index, description){
			description = $(description);
			var description_words = description.text().split(" ");

			for(var i=0 ; i < description_words.length; i++){
				var hash_word = description_words[i];
				var match_data = hash_word.match(/#([\w\d]*)/);
				if(match_data){
					var word = match_data[1];
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

		$('#num_hours').text(2);

		$('#slider').slider({
			value: 2,
			min: 1,
			max: 5,
			step: 1,
			slide: function(event, ui){
				$('#num_hours').text(ui.value);
				filterReports($('#find_search_box').val());
			}
		});		
		
		setSearchText();
		filterReports($('#find_search_box').val())
	}

	if($('.report').length > 0) {
		setvalidation();
	}
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
}

function filterReports(searchVal){	
	var searchRegExp = new RegExp(searchVal.toLowerCase());
	var hours = parseInt($('#num_hours').text());
	var deltaHours_ms = hours * 60 * 60 * 1000;
	
	$('ul#reports li').each(function(index, value){
		var report = $(value);		
		var date = Date.parse($(".full_date", report).text());
		var diff = Date.now() - date;
		
		var pass_search = true;
		if(searchVal != ""){
			pass_search = report.text().toLowerCase().match(searchRegExp);
		}
		var pass_date = diff <= deltaHours_ms;
		
		if(pass_search && pass_date){
			report.removeClass("hidden");
			report.addClass("visible")
		} else {
			report.addClass("hidden");
			report.removeClass("visible")
		}
	});
	
	displayNoticeIfNone();
}

function updateSearchURL(val){
	window.history.replaceState(val, val, "/find/" + val );
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

/***************************/
//@Author: Adrian "yEnS" Mato Gondelle & Ivan Guardado Castro
//@website: www.yensdesign.com
//@email: yensamg@gmail.com
//@license: Feel free to use it, but keep this credits please!
// Modified by Christian Reyes					
/***************************/

function setvalidation(){
	var form = $(".report_form");
    var description = $("#description");
    var descriptionInfo = $("#descriptionInfo");
    var location = $("#location");
    var locationInfo = $("#locationInfo");

    //On blur
    description.blur(validateDescription);
    location.blur(validateLocation);
	
	//On keydown
	description.keyup(validateDescription);
    location.keyup(validateLocation);
	
    //On Submitting
    form.submit(function () {
        if (validateDescription() &
            validateLocation())
            return true
        else
            return false;
    });

    //validation functions
    function validateDescription() {
        //if it's NOT valid
        if (description.val().length < 1) {
            description.addClass("error");
            descriptionInfo.text("Required");
            descriptionInfo.addClass("error");
            return false;
        }
        //if it's valid
        else {
            description.removeClass("error");
            descriptionInfo.text("");
            descriptionInfo.removeClass("error");
            return true;
        }
    }

    function validateLocation() {
        //if it's NOT valid
        if (location.val().length < 1) {
            location.addClass("error");
            locationInfo.text("Required");
            locationInfo.addClass("error");
            return false;
        }
        //if it's valid
        else {
            location.removeClass("error");
            locationInfo.text("");
            locationInfo.removeClass("error");
            return true;
        }
    }
}