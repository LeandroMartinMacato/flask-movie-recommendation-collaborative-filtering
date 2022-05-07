function show_movies() {
	$.ajax({
		url: "/get_recommend",
		type: "POST",
		dataType: "json",
		success: function (data) {
			console.log("Ajax Success");
			console.log(data);
			$(dynamic_movies).replaceWith(data);
		},
	});
}

$(function () {
	$("a#test").on("click", function (e) {
		e.preventDefault();
		$.getJSON("/clear_movies", function (data) {
			console.log(data);
		});
	});
});
