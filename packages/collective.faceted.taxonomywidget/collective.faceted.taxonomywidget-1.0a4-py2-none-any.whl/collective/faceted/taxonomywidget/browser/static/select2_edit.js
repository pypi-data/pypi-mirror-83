FacetedEdit.initializeTaxonomySelect2Widget = function(){
  jQuery('div.faceted-taxonomy_select2-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    FacetedEdit.Widgets[wid] = new FacetedEdit.SelectWidget(wid);
    var select = jQuery('#' + wid);
    select.select2({
      containerCssClass: 'faceted-select2-container',
      dropdownCssClass: 'faceted-select2',
    });
    jQuery('#s2id_' + wid).width(select.width() * 1.2);
  });
};

jQuery(document).ready(function(){
  jQuery(FacetedEdit.Events).bind(
    FacetedEdit.Events.INITIALIZE_WIDGETS,
    FacetedEdit.initializeTaxonomySelect2Widget);
});
