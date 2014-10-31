var $ = require('jquery');

var megaExpand = function(ev, $header){

  var $container = $header.parent('.expandable'),
      $button = $header.children('.expandable-button');

  ev.preventDefault();
  ev.stopPropagation();

  $container.toggleClass('open');
  $header.next('.expandable-content').slideToggle();
  $button.toggleClass('open');
  $header.find('.expandable-text').text( $container.hasClass('open') ? 'Collapse' : 'Learn More' );

};


$('.expandable').on( 'click', '.expandable-mainhead', function(ev){
  var $header = $(this).parent('.expandable-header');
  megaExpand(ev, $header);
});

$('.expandable').on( 'click', '.expand-close', function(ev){
  var $header = $(this).parents('.expandable').find('.expandable-header');
  megaExpand(ev, $header);
  var offSet = $header.offset().top;
  $('body').scrollTop(offSet);
});