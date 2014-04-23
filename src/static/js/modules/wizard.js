// rate-checker wizard walk through

var hideOnDisplay = $('#wizard-all, #wizard-next, .wizard-description'),
    showOnDisplay = $('.wizard, .wizard.visuallyhidden, #wizard-back'),
    wizard = $('.wizard');

var displayFullWizard = function(){
  showOnDisplay.removeClass('visuallyhidden');
  $('.wizard.current').removeClass('current');
  hideOnDisplay.addClass('visuallyhidden');
};

var backWizard = function(){
  wizard.addClass('visuallyhidden');
  hideOnDisplay.removeClass('visuallyhidden');
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

// start the wizard over
$('#wizard-back').click(function(e) {
  e.preventDefault();
  $(this).addClass('visuallyhidden');
  backWizard();
});