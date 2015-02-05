/* global require */

if(require === undefined){
  require = function(reqs, torun){
    'use strict';
    return torun(window.jQuery, {
      scan: function(){
        /* I don't know if this is necessary.... 
           but, this is a way to maintain plone 4 compatibility */
        window.jQuery('a.recordsEditLink').prepOverlay({
          subtype: 'ajax',
          filter: '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info',
          formselector: 'form:has(div[id^="formfield-form-widgets-value"])',
          closeselector: '[name="form.buttons.cancel"]',
          noform: function(el) {
            var o = window.jQuery(el);
            var emsg = o.find('dl.portalMessage.error');
            if (emsg.length) {
                o.children().replaceWith(emsg);
                return false;
            } else {
                return 'reload';
            }
          }
        });
      }
    });
  };
}

require([
  'jquery',
  'pat-registry'
], function($, Registry) {
  'use strict';

  $().ready(function() {

    /* expand the size of search as needed */
    $('#recordsContainer').delegate('#searchrow input[name="q"]', 'keypress', function(){
      var self = $(this);
      var count = self.val().length + 5;
      if(count > parseInt(self.attr('size'))){
        self.attr('size', count);
      }
    });

    /* ajax retrieval of paging */
    $('#recordsContainer').delegate('div.listingBar a', 'click', function(){
      var self = $(this);
      $('#spinner').show();
      $('#recordsContainer').load(self.attr('href') + ' #recordsTable', function(){
        /* scan registry */
        Registry.scan($('#recordsTable'));
      });
      return false;
    });

    /* ajax form submission */
    $('#recordsContainer').delegate('#searchrow form', 'submit', function(e){
      var self = $(this);
      $('#spinner').show();
      $('#recordsContainer').load(
        $('body').attr('data-base-url') + '?' + self.serialize() + ' #recordsTable',
        function(){
          $('#spinner').hide();
          $('#searchrow input[name="q"]').trigger('keypress');
          Registry.scan($('#recordsTable'));
        }
      );
      e.preventDefault();
      return false;
    });

    /* force submit on select change */
    $('#recordsContainer').delegate('#searchrow select', 'change', function(){
        $('#searchrow form#registry-filter').trigger('submit');
    });

    /* some init */
    $('#searchrow input[name="q"]').trigger('keypress');
  });

});