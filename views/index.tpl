<html>
  <head>
    <title>Heritage Finder</title>
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
  </head>
  <body>
    <div class="container">
      <div class="row page-header">
        <div class="col-md-12">
          <h1>Heritage Search</h1>
          <p class="lead">This is based on data scraped from <a href="http://www.hmrc.gov.uk/heritage/visit.htm">HMRC's tax exempt heritage database</a></p>
          <div class="alert alert-warning" role="alert">
            <strong>Warning</strong> This is not endorsed by HMRC in any respect
          </div>
        </div>
      </div>
      <div class="row">
        <form action="/" method="get">
          <div class="col-md-6">
            <div class="input-group input-group-lg">
              <input class="form-control" placeholder="Search" id="query" name="q" type="text" value="{{query}}"/>
              <span class="input-group-btn">
                <button type="submit" class="btn btn-primary"/>Search</button>
              </span>
            </div>
          </div>
          <div class="col-md-3">
            <div class="form-group">
              <span class="checkbox">
                <label for="artCheckbox">
                  <input class="check_boxes" id="artCheckbox" type="checkbox">
                  Include art
                </label>
                <span class="badge pull-right">100</span>
              </span>
              <span class="checkbox">
                <label for="paintingCheckbox">
                  <input class="check_boxes" id="paintingCheckbox" type="checkbox">
                  Include paintings
                </label>
                <span class="badge pull-right">100</span>
              </span>
            </div>
          </div>
        </form>
      </div>
      <div class="row">
        <div id="results" class="col-md-12">
        % include('results', count=count, results=results, links=links, number_of_pages=number_of_pages)
        </div>
      </div>
    </div>
    <script>
      $(document).ready(function () {
        $("#query").keyup(function() {
          $.ajax({
            url: '/results',
            data: {'q': $("#query").val()},
            success: function(response) {
              $("#results").html(response);
            }
          });
        });
      });
    </script>
  </body>
</html>
