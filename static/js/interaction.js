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
    width: 900
    });
  $("#book-now a:first").on("click", function() {
    $("#book-dialog").dialog("open");
  });
});


