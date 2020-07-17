function switchOnNightMode() {
	$('.container').css('color', '#e57373');
	$('.button').css({
		'background-color': '#d32f2f',
		'color': '#e57373'
	});
	$('.messageError').css('color', '#e57373');
	$('footer').css('color', '#e57373');
	$('input').css({
		'background-color': 'black',
		'color': '#e57373'
	});
	$('select').css({
		'background-color': 'black',
		'color': '#e57373'
	});
	$('.tab button').css('background-color', '#e57373');
	// $('.tab button:hover').css('background-color', '#ddd'); 
	$('.tab button.active').css('background-color', '#d32f2f');
}

function switchOffNightMode() {
	$('.container').css('color', 'white');
	$('.button').css({
		'background-color': 'blueviolet',
		'color': 'white'
	});
	$('.messageError').css('color', 'white');
	$('footer').css('color', 'white');
	$('input').css({
		'background-color': 'black',
		'color': 'white'
	});
	$('select').css({
		'background-color': 'black',
		'color': 'white'
	});
	$('.tab button').css('background-color', '#f1f1f1');
	$('.tab button.active').css('background-color', '#ccc');

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