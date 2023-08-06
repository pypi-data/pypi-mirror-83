Faceted.TaxonomySelectWidget = Faceted.SelectWidget
Faceted.TaxonomySelectWidget.prototype = Object.create(Faceted.SelectWidget.prototype)

Faceted.TaxonomySelectWidget.prototype.count_update = function(data, sortcountable){
    var context = this;
    var select = jQuery('select', context.widget);
    var options = jQuery('option', context.widget);
    var groups = jQuery('optgroup', context.widget);
    var current_val = select.val();
    jQuery(options).each(function(){
      var option = jQuery(this);
      option.removeClass('faceted-select-item-disabled');
      option.attr('disabled', false);
      var key = option.val();

      var value = data[key];
      value = value ? value : 0;
      var option_txt = option.attr('title');
      option_txt += ' (' + value + ')';

      option.html(option_txt);
      if(sortcountable){
        option.data('count', value);
      }
      if(!value){
        option.attr('disabled', 'disabled');
        option.addClass('faceted-select-item-disabled');
      }
    });
    jQuery(groups).each(function(){
      var group = jQuery(this);
      group.removeClass('faceted-select-group-disabled');
      if (group.find('option:enabled').length == 0) {
        group.addClass('faceted-select-group-disabled');
      }
    });
    if(sortcountable){
      options.detach().sort(function(x, y) {
        var a = jQuery(x).data('count');
        var b = jQuery(y).data('count');
        return b - a;
      });
      select.append(options);
      select.val(current_val);
    }
  }

Faceted.initializeTaxonomySelectWidget = function(evt){
  jQuery('div.faceted-taxonomy_select-widget').each(function(){
    var wid = jQuery(this).attr('id');
    wid = wid.split('_')[0];
    Faceted.Widgets[wid] = new Faceted.TaxonomySelectWidget(wid);
  });
};

jQuery(document).ready(function(){
  jQuery(Faceted.Events).bind(
    Faceted.Events.INITIALIZE,
    Faceted.initializeTaxonomySelectWidget);
});
