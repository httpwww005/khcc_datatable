<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>KHCC visitcount</title>

    <style>
        li { list-style: none; }
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>
        $(document).ready(function() {
			$("#message").load("/view")

			$("#refresh").click(function(){
				$("#message").text("Loading...")
				$("#message").load("/refresh")
			})
        });
    </script>
</head>
<body>
	<button id="refresh">Refresh</button>
    <div id="message">this is message</div>
</body>
</html>
