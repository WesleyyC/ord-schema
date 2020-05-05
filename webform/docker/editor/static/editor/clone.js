console.log("loading...")

var schema = {};
var identifierCount = 0;

var ReactionMessage;
var ReactionIdentifierMessage;
var encodeString;
// Load the protobuf
protobuf.load(proto_url).then(function (root) {
    console.log(root);
    ReactionMessage = root.lookupType("ord.Reaction");
    ReactionUnrepeatedMessage = root.lookupType("ord.ReactionUnrepeated");

    ReactionIdentifierMessage = root.lookupType("ord.ReactionIdentifier");
    console.log("protobuf load");
});
// TODO how to return a success message? Busy-wait using cookies?

// Hook up the Submit button
$('#submit').on('click', function () {
    console.log("submit button clicked");

    // get all elements 
    var identifiers = $("#identifiers-list").children('');
    console.log(identifiers);
    // TODO actually get from elements

    payload = {identifiers: {type: ReactionIdentifierMessage.IdentifierType.RINCHI}}
    var encode = ReactionUnrepeatedMessage.encode(payload).finish()
    console.log(encode)
    // TODO (1) figure out how repeated fields work

    // TODO (2) send to backend, and get backend to actually do interesting things
    // $.post(`/editor/send_protobuf`, {"encode": encode})
    //     .done((data, status) => { console.log(data) })

    // We encode the payload as a string, to use Python's ParseFromString in backend
    // and to allow sending through Ajax/jQuery
    var encodeString = String.fromCharCode.apply(null, encode)
    console.log(encodeString)
    $.post('/editor/send_protobuf', encodeString, function( data ) {
        // $( ".result" ).html( data );
        console.log(data);
      });

});

// Hook up the add buttons
$('.json-editor-btn-add').on('click', function () {
    console.log("add button clicked");

    // create the element
    var newDiv = $('<div>').load("identifier", function () {
        // Hook the element to actually do things
        // Needs to be a callback, in order to properly load
        newDiv.find('.json-editor-btn-delete').on('click', function () {
            console.log("delete button clicked");
        });
    });

    // add it to the site!
    $("#identifiers-list").append(newDiv);

});

// TODO validator