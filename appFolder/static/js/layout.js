function switchOnNightMode() {
	$('.container').css('color', '#F28F38');
	$('.button').css({
		'background-color': '#131926',
		'color': '#F28F38'
	});
	$('.messageError').css('color', '#F28F38');
	$('footer').css('color', '#F28F38');
	$('input').css({
		'background-color': 'black',
		'color': '#F28F38'
	});
	$('select').css({
		'background-color': 'black',
		'color': '#F28F38'
	});
	$('.tab button').css('background-color', 'black');
	// $('.tab button:hover').css('background-color', '#ddd'); 
	$('.tab button.active').css('background-color', '#131926');
}

function switchOffNightMode() {
	$('.container').css('color', '#F28F38');
	$('.button').css({
		'background-color': '#354B8C',
		'color': '#F28F38'
	});
	$('.messageError').css('color', 'white');
	$('footer').css('color', '#F28F38');
	$('input').css({
		'background-color': 'black',
		'color': '#F28F38'
	});
	$('select').css({
		'background-color': 'black',
		'color': '#F28F38'
	});
	$('.tab button').css('background-color', '#354B8C');
	$('.tab button.active').css('background-color', '#2C3D73');

}

$(document).ready(function () {
	// set the mode day/night permanent - pages transition
	if (localStorage.getItem('mode') === 'night') {
		switchOnNightMode();
		$('#night_mode').click();
	} else {
		switchOffNightMode();
	}
	// ############ Night Mode ############
	$('#night_mode').change(function () {
		if (this.checked) {
			switchOnNightMode();
			localStorage.setItem('mode', 'night');
		}
		else {
			switchOffNightMode();
			localStorage.setItem('mode', 'day');
		}
	});

	$("#bilou").click(function(e){
		e.preventDefault();
		$("#player")[0].play();
	});
});