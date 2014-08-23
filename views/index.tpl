<html>
  <head>
    <title>Heritage Search</title>
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
  </head>
  <body>
    <div class="container">
      <div class="row page-header">
        <h1>Heritage Search</h1>
        <p class="lead">This is based on data scraped from <a href="http://www.hmrc.gov.uk/heritage/visit.htm">HMRC's tax exempt heritage database</a></p>
        <div class="alert alert-warning" role="alert">
          <strong>Warning</strong> This is not endorsed by HMRC in any respect
        </div>
      </div>
      <div class="row">
        <form action="/" method="get" class="form-inline">
          <div class="input-group input-group-lg">
            <input class="form-control" placeholder="Search" id="query" name="q" type="text" value="{{query}}"/>
            <span class="input-group-btn">
              <button type="submit" class="btn btn-primary"/>Search</button>
            </span>
          </div>
        </form>
      </div>
      <div class="row">
        <table id="resultsTable" class="table table-condensed">
          <thead>
            <tr><th>#</th><th id="resultsCount">{{ count }} results found</th></tr>
          </thead>
          </tbody>
          % for i,result in enumerate(results):
            <tr class="asset"><td>{{ i+1 }}</td><td class="name"><a href="{{ result['url'] }}">{{ result['name'] }}</a></td></tr>
          % end
          </tbody>
        <table>
      </div>
    </div>
    <script>
      $(document).ready(function () {
        $("#query").keyup(function() {
          $.ajax({
            url: '/',
            dataType: 'json',
            data: {'q': $("#query").val()},
            beforeSend: setHeader,
            success: function(response) {
              $("#resultsCount").html(response['count'] + " results found");
              $("#resultsTable tbody tr").remove()
              $.each(response['results'], function(i, result) {
                $("<tr class='asset'>").append(
                  "<td>" + (i+1) + "</td><td class='name'><a href='" + result['url'] + "'>" + result['name'] + "</a></td>"
                ).appendTo("#resultsTable");
              })
            }
          });
        });
      });
      function setHeader(hdr) {
        hdr.setRequestHeader('Accept', 'application/json');
      };
    </script>
  </body>
</html>
