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
    }, {
      loading: {
        show: function(){ window.jQuery$('#spinner').show(); },
        hide: function(){ window.jQuery$('#spinner').hide(); },
      }
    });
  };
}

require([
  'jquery',
  'pat-registry',
  'mockup-utils',
  'mockup-patterns-modal'
], function($, Registry, utils, Modal) {
  'use strict';

  var loadModals = function(){
    $('.recordsEditLink').each(function(){
      var $el = $(this);
      var options = {
        actionOptions: {
          onSuccess: function(modal){
            modal.hide();
            $('#searchrow form#registry-filter').trigger('submit');
          }
        }
      };
      $el.addClass('pat-plone-modal');
      new Modal($el, options);
    });
  }

  $().ready(function() {
    loadModals();

    /* ajax retrieval of paging */
    $('#recordsContainer').on('click', 'nav.pagination a, div.listingBar a', function(){
      var self = $(this);
      utils.loading.show();
      $('#recordsContainer').load(self.attr('href') + ' #recordsTable', function(){
        /* scan registry */
        loadModals();
        utils.loading.hide();
      });
      return false;
    });

    /* ajax form submission */
    $('#recordsContainer').on('submit', '#searchrow form', function(e){
      var self = $(this);
      utils.loading.show();
      $('#recordsContainer').load(
        $('body').attr('data-base-url') + '?' + self.serialize() + ' #recordsTable',
        function(){
          $('#spinner').hide();
          $('#searchrow input[name="q"]').trigger('keypress');
          loadModals();
          utils.loading.hide();
        }
      );
      e.preventDefault();
      return false;
    });

    /* force submit on select change */
    $('#recordsContainer').on('change', '#searchrow select', function(){
      $('#searchrow form#registry-filter').trigger('submit');
    });

    /* some init */
    $('#searchrow input[name="q"]').trigger('keypress');
  });

});
