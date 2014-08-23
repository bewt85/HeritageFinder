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
