<html>
  <head>
    <title>Heritage Search</title>
  </head>
  <body>
    <h1>Heritage Search</h1>
    <p>This is based on data scraped from <a href="http://www.hmrc.gov.uk/heritage/visit.htm">HMRC's tax exempt heritage database</a></p>
    <p>It is not endorsed by HMRC in any form</p>
    <form action="/" method="get">
      <input name="q" type="text" />
      <input value="Search" type="submit" />
    </form>
    <div id="results">{{len(results)}} results found</div>
  </body>
</html>
