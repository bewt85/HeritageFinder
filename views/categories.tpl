          <div id="categoriesList" class="form-group">
            <div class="col-md-3">
            % for category,categoryAlphaOnly,count in category_count[:(len(category_count)+1)/2]:
              <div class="checkbox">
                <span class="badge pull-right">{{ count }}</span>
                <label for="{{categoryAlphaOnly}}">
                  % if categoryAlphaOnly in requested_categories:
                  <input name="cat[]" id="{{categoryAlphaOnly}}" type="checkbox" value="{{categoryAlphaOnly}}" checked/>
                  % else:
                  <input name="cat[]" id="{{categoryAlphaOnly}}" type="checkbox" value="{{categoryAlphaOnly}}"/>
                  % end
                  {{ category }}
                </label>
              </div>
            % end
            </div>
            <div class="col-md-3">
            % for category,categoryAlphaOnly,count in category_count[(len(category_count)+1)/2:]:
              <div class="checkbox">
                <span class="badge pull-right">{{ count }}</span>
                <label for="{{categoryAlphaOnly}}">
                  % if categoryAlphaOnly in requested_categories:
                  <input name="cat[]" id="{{categoryAlphaOnly}}" type="checkbox" value="{{categoryAlphaOnly}}" checked/>
                  % else:
                  <input name="cat[]" id="{{categoryAlphaOnly}}" type="checkbox" value="{{categoryAlphaOnly}}"/>
                  % end
                  {{ category }}
                </label>
              </div>
            % end
            </div>
          </div>
