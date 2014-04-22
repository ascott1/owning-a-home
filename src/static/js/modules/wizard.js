  // rate-checker wizard walk through

var displayFullWizard = function(){
  $('.wizard.visuallyhidden, #wizard-back').removeClass('visuallyhidden');
  $('#wizard-all, #wizard-next, .wizard-description').addClass('visuallyhidden');
};

var backWizard = function(){
  $('.wizard').addClass('visuallyhidden');
  $('#wizard-all, #wizard-next, .wizard-description').removeClass('visuallyhidden');
  $('.wizard:first').removeClass('visuallyhidden').addClass('current');
};

$('#wizard-next').click(function(e) {
  e.preventDefault();
  var current = $('.wizard.current'),
      next = current.next('.wizard');
  if (next.length) {
    current.toggleClass('visuallyhidden').removeClass('current');
    next.removeClass('visuallyhidden').addClass('current');
  } else {
    displayFullWizard();
  }
});

// show all wizard elements
$('#wizard-all').click(function(e) {
  e.preventDefault();
  displayFullWizard();
});

$('#wizard-back').click(function(e) {
  e.preventDefault();
  $(this).addClass('visuallyhidden');
  backWizard();
});