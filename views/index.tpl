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
    <div id="resultsCount">{{len(results)}} results found</div>
    <table id="resultsTable">
      <tr><th>Description</th></tr>
    % for result in results[:20]:
      <tr class="asset"><td class="name"><a href="{{ result['url'] }}">{{ result['name'] }}</a></td></tr>
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
            success: function(result) {
              $("#resultsCount").html(result['count'] + " results found");
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
