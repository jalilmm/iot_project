<!DOCTYPE html>
<html>
<head>
	<title>Room Temperature</title>
  <link rel="stylesheet" href="styles.css">
	<script>
		function updateTemperature() {
			var xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
				if (this.readyState == 4 && this.status == 200) {
					var data = JSON.parse(this.responseText);
					document.getElementById("current-temp").innerHTML = data.current_temperature + " &deg;C";
					document.getElementById("min-temp").innerHTML = data.min_temperature + " &deg;C";
					document.getElementById("max-temp").innerHTML = data.max_temperature + " &deg;C";
				}
			};
			xhttp.open("GET", "temperature.php", true);
			xhttp.send();
		}
		setInterval(updateTemperature, 5000); // Update temperature every 5 seconds
	</script>
</head>
<body>
	<h1>Current Room Temperature in room 405 in DORM 8 </h1>
	<p>Current temperature: <span id="current-temp"></span></p>
	<p>Minimum temperature today: <span id="min-temp"></span></p>
	<p>Maximum temperature today: <span id="max-temp"></span></p>
</body>
</html>
