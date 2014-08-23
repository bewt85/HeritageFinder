<html>
  <head>
    <title>Heritage Search</title>
  </head>
  <body>
    <h1>Heritage Search</h1>
    <p>This is based on data scraped from <a href="http://www.hmrc.gov.uk/heritage/visit.htm">HMRC's tax exempt heritage database</a></p>
    <p>It is not endorsed by HMRC in any form</p>
    <form action="/" method="get">
      <input id="query" name="q" type="text" value="{{query}}"/>
      <input value="Search" type="submit" />
    </form>
    <div id="resultsCount">{{ count }} results found</div>
    <table id="resultsTable">
      <tr><th><th><th>Description</th></tr>
    % for i,result in enumerate(results):
      <tr class="asset"><td>{{ i+1 }}</td><td class="name"><a href="{{ result['url'] }}">{{ result['name'] }}</a></td></tr>
    % end
    <table>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
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
              $("#resultsTable tr:not(:first)").remove()
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
