Faceted.initializeTaxonomySelect2Widget = function(evt){
  jQuery('div.faceted-taxonomy_select2-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.TaxonomySelectWidget(wid);
    var select = jQuery('#' + wid);
    var parameters = {
      containerCssClass: 'faceted-select2-container',
      dropdownCssClass: 'faceted-select2',
    };
    select.select2(parameters);
    jQuery('#s2id_' + wid).width(select.width() * 1.2);
    // Bind events
    jQuery(Faceted.Events).bind(Faceted.Events.QUERY_CHANGED, function(evt){
      select.select2(parameters);
    });
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeTaxonomySelect2Widget);
});
