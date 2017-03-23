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
				$("#message").load("/refresh")
			})
			setInterval(function(){
				$("#message").load("/view")
			},3000)
        });
    </script>
</head>
<body>
	<button id="refresh">Refresh</button>
    <div id="message">{{get("message","csv_file not available")}}</div>
</body>
</html>
