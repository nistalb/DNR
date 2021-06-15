$("#add_pdf").on("click", function(e) {
    console.log("clicked add pdf")
    $("#add_pdf_div").css("visibility", "visible");
    $("#pdf_span_holder").css("visibility", "hidden");
})

$("#submit_pdf").on("click", function() {
    $("#wait_message").css("visibility", "visible")
})
