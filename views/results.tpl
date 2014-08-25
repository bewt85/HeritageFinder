        <div id="resultsAndPages">
          <table id="resultsTable" class="table table-condensed">
            <thead>
              <tr>
                <th>#</th>
                <th>Category</th>
                <th>Location</th>
                <th id="resultsCount">{{ count }} results found</th>
              </tr>
            </thead>
            </tbody>
            % first_result = results_per_page * (page-1)
            % for i,result in enumerate(results):
              <tr class="asset">
                <td>{{ i+1+first_result }}</td>
                <td>{{ result['category'].title() }}</td>
                <td>{{ result['region'].title() }}</td>
                <td class="name"><a href="{{ result['url'] }}">{{ result['summary'] }}</a></td>
              </tr>
            % end
            </tbody>
          </table>
          <ul id="pages" class="pagination pull-right">
          % for text,url in links:
            <li><a href="{{ url }}">{{ text }}</a></li>
          % end
          </ul>
        </div>
