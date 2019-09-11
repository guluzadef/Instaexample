 // You may required to change this file to fit your need based on your server-side application
$(function() {
  //
  // Skin switcher
  //
  $("head").append('<link id="skin-css" rel="stylesheet">');
  $('.skin-colors li').on('click', function() {
    $('.skins li').removeClass('active');
    $(this).addClass('active');
    $('#skin-css').attr('href', '/static/css/skin-'+ $(this).data('skin') +'.css');
  });
  //
  // Open shot in a modal
  //
  $('.shot-modal-opener, .shot-preview .img, .shot-preview .black-overlay, .shot-preview .title, .shot-preview .text-overlay, .shot-small .shot-info h6 a').on('click', function(e) {

    e.preventDefault();
    // Put a spinner inside the modal and open it
    $('#shot-modal .modal-content').html('<div class="spinner"><span class="dot1"></span><span class="dot2"></span><span class="dot3"></span></div>');
    $('#shot-modal').modal();
    // Load data from server and initialize the gallery.
    // You can add a data-id="XXX" to each .shot
    /*
    var shotId = $(this).parents('.shot').data('id');
    $('#shot-modal .modal-content').load('shot.php?id='+ shotId, function() {
      initGallery();
      initModalLike();
    });
    */
    // ### This code is only for DEMO purpuse ###
    // We use setTimeout to have a delay and demonstrate the spinner
    setTimeout(function(){
      $('#shot-modal .modal-content').load('shot-detail.html', function() {
        initGallery();
        // initModalLike();
      })
    }, 1000);
  });
  //
  // Like buttons
  //
  //
  // Dropzone
  //
  // Visit http://www.dropzonejs.com/ for more options and see how you can handle uploaded files
  Dropzone.autoDiscover = false;
  $(".dropzone").dropzone({
    url: "target.php",
    dictDefaultMessage: '<span class="dropzone-file-icon"></span>Drag and drop a file here or click!'
  });
});
//
// Like button doesn't work in modals because of Ajax content loading
//
// function initModalLike() {
//   $('.modal .like').on('click', function() {
//     // Resolve shot ID and send an ajax request to update number of likes in database
//     $(this).children('.fa').toggleClass('fa-heart-o fa-heart');
//   });
// }
//
// Config gallery and slider in single shot page
//
// Visit http://sachinchoolur.github.io/lightslider/ and http://sachinchoolur.github.io/lightGallery/ for more options
function initGallery() {
  $('.image-gallery').lightSlider({
    gallery:true,
    item:1,
    loop:true,
    thumbItem: 5,
    slideMargin:0,
    enableDrag: true,
    currentPagerPosition:'left',
    onSliderLoad: function(el) {
      el.lightGallery({
        selector: '.image-gallery .lslide'
      });
    }
  });
}
//
// Draw map in page-contact
//
function initMap() {
  var mapDiv = document.getElementById('contact-map');
  var map = new google.maps.Map(mapDiv, {
    center: {lat: 44.540, lng: -78.546},
    zoom: 14
  });
  var marker = new google.maps.Marker({
    position: {lat: 44.540, lng: -78.546},
    icon: "/static/img/app/marker.png",
    map: map
  });
  map.set('styles', [{"featureType":"landscape","stylers":[{"hue":"#FFBB00"},{"saturation":43.400000000000006},{"lightness":37.599999999999994},{"gamma":1}]},{"featureType":"road.highway","stylers":[{"hue":"#FFC200"},{"saturation":-61.8},{"lightness":45.599999999999994},{"gamma":1}]},{"featureType":"road.arterial","stylers":[{"hue":"#FF0300"},{"saturation":-100},{"lightness":51.19999999999999},{"gamma":1}]},{"featureType":"road.local","stylers":[{"hue":"#FF0300"},{"saturation":-100},{"lightness":52},{"gamma":1}]},{"featureType":"water","stylers":[{"hue":"#0078FF"},{"saturation":-13.200000000000003},{"lightness":2.4000000000000057},{"gamma":1}]},{"featureType":"poi","stylers":[{"hue":"#00FF6A"},{"saturation":-1.0989010989011234},{"lightness":11.200000000000017},{"gamma":1}]}]);
}