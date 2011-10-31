function addNom(pnom) {
    var green = Math.random();

    var newSpan = document.createElement("span");

    if (green > .85) {
        newSpan.className = "greenNom";
        newSpan.appendChild(document.createTextNode("NOM! "));
    } else {
        newSpan.appendChild(document.createTextNode("nom "));
    }

    $(newSpan).bind("mouseover",
    function() {
        $(newSpan).fadeOut()
    });
    pnom.appendChild(newSpan);
}

window.onload = function() {
    var pnom = document.getElementById("noms");

    setInterval(function() { addNom(pnom); }, 50);

	document.body.style.cursor = "url('../images/rageface.cur'), default";
}