$(function() {
  /*
  $(document).tooltip({
    items:    "#book-now",
    content:  "<div class='ui-tooltip'>Click here to find out more!</div>",
    hide:     false,
    position: {my: "center center", at: "right center"},
    show:     100
  });
  */
  $("#book-dialog").dialog({
    autoOpen: false,
    draggable: false,
    height: "auto",
    hide: "fadeOut",
    modal: true,
    position: {my: "top", at: "top+10%", of: window},
    resizable: false,
    show: "slideDown",
    width: 400,
    open: function(e, ui) {
      $("body").addClass("isModal");
      $("body").on("click", potential_close);
    },
    close: function(e, ui) {
      $("body").removeClass("isModal");
      $("body").off("click", potential_close);
    }
  });
  $("#navtab-booking a:first").on("click", function(e) {
    e.preventDefault();
    $("#book-dialog").dialog("open");
  });
  $("#navbar").css("visibility", "visible");
});


var potential_close = function(e) {
  /* make sure that anything other than a click on something inside of the modal
   * closes it.
   */
  E = e;
  if(e.type == "click") {
    if(!_.contains($(e.target).parents(), $(".ui-dialog:first")[0]) && e.target != $("#navtab-booking a:first")[0])
      $("#book-dialog").dialog("close");
  }
}
