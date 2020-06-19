function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "inline-block";
	evt.currentTarget.className += " active";
	
	$("#message").text(""); // deleting text in message paragraph to hide previous text
	$("#filename").text("");
}

function disable_tables(){
	$(".tablinks").prop('disabled', true);
	$("#validate_path").hide();
}

function enable_tables(){
	$(".tablinks").prop('disabled', false);
	$("#validate_path").show();
}

function stop_photo(cancel_was_clicked){
	$.ajax({
		url:'/stop_photo',
		type:'POST',
		dataType:"json",
		data:'photo_name='+$("#filename").text()+'&cancel='+cancel_was_clicked,
		
		success : function(codeJson){
			if(codeJson.length!=0){
				$("#message").text(codeJson.text);
				$("#filename").text(codeJson.name);
				$("#take_a_photo").show();
				$("#cancel_photo").hide();
				enable_tables();
				if(the_timeout_handler!=null){
					clearTimeout(the_timeout_handler);
					the_timeout_handler = null;
				}
			}
			else{
				console.log("else");
			}
		},
		error : function(result, status, error){
			console.log(result, status, error);
		},	
	});
}
var the_timeout_handler = null;

$(document).ready(function(){
	document.getElementById("default_open").click(); // default tab 'photo' is opened	
	$("#stop_video").hide();
	$("#stop_timelapse").hide();
	$("#cancel_photo").hide();
	
	// ############ Photo ############

	$("#take_a_photo").click(function(e){
		e.preventDefault();
		$.ajax({
			url:'/take_a_photo',
			type:'POST',
			dataType:"json",
			data:'path='+$("#path").val()+'&exposure_photo='+$('#exposure_photo').val(),
			
			success : function(codeJson){
				if(codeJson.length!=0){
					$("#message").text(codeJson.text);
					$("#filename").text(codeJson.name);
					disable_tables();
					$("#take_a_photo").hide();
					$("#cancel_photo").show();
					the_timeout_handler = setTimeout( () => {
						enable_tables();
						stop_photo(false);
						the_timeout_handler = null;
					}, parseFloat($('#exposure_photo').val())*1000);				
				}
				else{
					console.log("else");
				}
			},
			error : function(result, status, error){
				console.log(result,status,error);
			},
		});
	});

	$("#cancel_photo").click( (e) =>{
		e.preventDefault();
		stop_photo(true);
	});

	// ############ Timelapse ############

	$("#take_timelapse").click(function(e){
		e.preventDefault();
		$.ajax({
			url:'/take_timelapse',
			type:'POST',
			dataType:"json",
			data:'path='+$("#path").val()+'&exposure_photo='+$('#exposure_photo_timelapse').val()
					+'&time_between_photos=' + $('#time_between_photos').val()
					+'&number_photos=' + $('#number_photos').val(),
			
			success : function(codeJson){
				if(codeJson.length!=0){
					$("#message").text(codeJson.text);
					$("#filename").text(codeJson.name);
					disable_tables();
					$("#take_timelapse").hide();
					$("#stop_timelapse").show();
					the_timeout_handler = setTimeout( () => {
						enable_tables();
						$("#stop_timelapse").click();
						the_timeout_handler = null;
					}, parseFloat($("#calculated_time").text())*1000);
				}
				else{
					console.log("else");
				}
			},
			error : function(result, status, error){
				console.log(result,status,error);
			},
		});
	});

	$("#stop_timelapse").click(function(e){
		e.preventDefault();
		$.ajax({
			url:'/stop_timelapse',
			type:'POST',
			dataType:"json",
			data:'timelapse_name='+$("#filename").text(),
			
			success : function(codeJson){
				if(codeJson.length!=0){
					$("#message").text(codeJson.text);
					$("#filename").text(codeJson.name);
					$("#take_timelapse").show();
					$("#stop_timelapse").hide();
					enable_tables();
					if(the_timeout_handler!=null){
						clearTimeout(the_timeout_handler);
						the_timeout_handler = null;
					}
				}
				else{
					console.log("else");
				}
			},
			error : function(result, status, error){
				console.log(result, status, error);
			},
		});
	});

	// ############ Video ############

	$("#start_video").click(function(e){
		e.preventDefault();
		$.ajax({
			url:'/start_video',
			type:'POST',
			dataType:"json",
			data:'path='+$("#path").val(),
			
			success : function(codeJson){
				if(codeJson.length!=0){
					$("#message").text(codeJson.text);
					$("#filename").text(codeJson.name);
					$("#start_video").hide();
					$("#stop_video").show();
					disable_tables();
				}
				else{
					console.log("else");
				}
			},
			error : function(result, status, error){
				console.log(result,status,error);
			},
		});
	});

	$("#stop_video").click(function(e){
		e.preventDefault();
		$.ajax({
			url:'/stop_video',
			type:'POST',
			dataType:"json",
			data:'video_name='+$("#filename").text(),
			
			success : function(codeJson){
				if(codeJson.length!=0){
					$("#message").text(codeJson.text);
					$("#filename").text(codeJson.name);
					$("#start_video").show();
					$("#stop_video").hide();
					enable_tables();
				}
				else{
					console.log("else");
				}
			},
			error : function(result, status, error){
				console.log(result,status,error);
			},
		});
	});


 	// ############ Calculated time ############

	$("#exposure_photo_timelapse, #number_photos, #time_between_photos").change(function() {
		var time = (parseFloat($('#exposure_photo_timelapse').val())
					+ parseFloat($('#time_between_photos').val()) ) 
					* parseFloat($('#number_photos').val());
		$("#calculated_time").text(time);
	});

	
	// ############ Save in USB ############

	$("#save_in_usb").click( (e) => {
		e.preventDefault();
		$.ajax({
			url:'/save_usb',
			type:'POST',
			dataType:"json",
			data:'',
			
			success : function(codeJson){
				if(codeJson.length!=0){
					$("#usb_status").text(codeJson.text);
				}
				else{
					console.log("else");
				}
			},
			error : function(result, status, error){
				console.log(result,status,error);
			},
		});
	});
});
