<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>table</title>
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css">
    <script type="text/javascript" language="javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>
	<script type="text/javascript" charset="utf-8">
		function update_table(){
			$('#datatable').dataTable(
				{
					"pageLength":100,
					"columnDefs": [{
						"render": function ( data, type, row ) {
							return data.slice(0,10)
						},
						"targets": 1
					},
					{ "visible": false,  "targets": [0] }
					]
				}
			);
		}

		$(document).ready(function() {
			$("#date_select").change(function(){
				update_table()
				$("#datatable").load("/table/"+$(this).val())
				//$('#datatable').DataTable().ajax.reload();
			});
		} );
	</script>

</head>
<body>
	<div class="container">
		<select id="date_select">
			%for date in dates:
  			<option value="{{date}}">{{date}}</option>
			%end
		</select>
		<p/>
		<br/>
		<table id="datatable" class="display">
			% include('table.tpl')
		</table>
	</div>
</body>
</html>
