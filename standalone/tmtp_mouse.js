//global variables
var tooltip;

function init(evt) {
    //get reference to child (content) of the city text-Element
    tooltip = document.getElementById("tooltip");
}

function ShowTooltip(evt) {
    // Put tooltip in the right position, change the text and make it visible
    tooltip.setAttributeNS(null,"x",evt.clientX+10);
    tooltip.setAttributeNS(null,"y",evt.clientY+30);
    tooltip.firstChild.data = evt.target.getAttributeNS(null,"id");
    //tooltip.firstChild.data = evt.target.getAttributeNS(null,"mouseovertext");
    tooltip.setAttributeNS(null,"visibility","visible");
}

function HideTooltip(evt) {
    tooltip.setAttributeNS(null,"visibility","hidden");
}
