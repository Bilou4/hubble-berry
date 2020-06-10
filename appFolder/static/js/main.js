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
}


$(document).ready(function(){
	document.getElementById("default_open").click(); // default tab 'photo' is opened	
	$("#stop_video").hide();

	$("#take_a_photo").click(function(e){
		e.preventDefault();
		$.ajax({
			url:'/take_a_photo',
			type:'POST',
			dataType:"json",
			data:'path='+$("#path").val()+'&exposure_photo='+$('#exposure_photo').val(),
			
			success : function(codeJson){
				if(codeJson.length!=0){
					$("#message").text(codeJson.text + " " +codeJson.name);	
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
					$("#message").text(codeJson.text + " " +codeJson.name);	
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

	$("#start_video").click(function(e){
		e.preventDefault();
		$.ajax({
			url:'/start_video',
			type:'POST',
			dataType:"json",
			data:'path='+$("#path").val(),
			
			success : function(codeJson){
				if(codeJson.length!=0){
					$("#message").text(codeJson.text + " " +codeJson.name);
					$("#start_video").hide();
					$("#stop_video").show();	
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
			data:'video_name='+$("#message").text(),
			
			success : function(codeJson){
				if(codeJson.length!=0){
					$("#message").text(codeJson.text + " " +codeJson.name);
					$("#start_video").show();
					$("#stop_video").hide();
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

	$("#exposure_photo_timelapse, #number_photos, #time_between_photos").change(function() {
		var time = (parseFloat($('#exposure_photo_timelapse').val())
					+ parseFloat($('#time_between_photos').val()) ) 
					* parseFloat($('#number_photos').val());
		$("#calculated_time").text("Temps total (calculé) => " + time + " secondes");
	});
});
