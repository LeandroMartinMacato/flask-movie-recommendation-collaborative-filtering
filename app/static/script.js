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
	$("#clear-butt").click(function (e) {
		e.preventDefault();
		$.getJSON("/clear_movies", function (data) {
			console.log(data);
		});

		$(".reset-alert").append(
			`
			<div class="alert alert-info alert-dismissible fade show" role="alert"
			style="margin-top: 10px;">
				<strong> Successfully Reset Movie Reviews </strong>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
			</div>
			`
		);
	});
});
