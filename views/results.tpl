        <ul class="pagination">
        % for text,url in links:
          <li><a href="{{ url }}">{{ text }}</a></li>
        % end
        </ul>
        <table id="resultsTable" class="table table-condensed">
          <thead>
            <tr><th>#</th><th id="resultsCount">{{ count }} results found</th></tr>
          </thead>
          </tbody>
          % first_result = results_per_page * (page-1)
          % for i,result in enumerate(results):
            <tr class="asset"><td>{{ i+1+first_result }}</td><td class="name"><a href="{{ result['url'] }}">{{ result['name'] }}</a></td></tr>
          % end
          </tbody>
        <table>
