$(() => {
  $('.menu').click(function() {
    $(this).toggleClass('menu-clicked');
    $('.sidebar').toggleClass('show-sidebar hide-sidebar');
  });
});
