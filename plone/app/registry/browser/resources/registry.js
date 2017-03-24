/* global require */
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
        Registry.scan($('#recordsTable'));
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
          Registry.scan($('#recordsTable'));
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
