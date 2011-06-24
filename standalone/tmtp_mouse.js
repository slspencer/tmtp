//global variables
var tooltip;

function init(evt) {
    //get reference to child (content) of the city text-Element
    tooltip = document.getElementById("tooltip");
}

function ShowTooltip(evt) {
    // Put tooltip in the right position, change the text and make it visible
    //tooltip.setAttributeNS(null,"x",evt.clientX+10);
    //tooltip.setAttributeNS(null,"y",evt.clientY+30);
 
    //alert(evt.currentTarget.cx.baseVal.value);

    // works on non-transformed objects
    //tooltip.setAttributeNS(null,"x",evt.currentTarget.cx.baseVal.value);
    //tooltip.setAttributeNS(null,"y",evt.currentTarget.cy.baseVal.value);

    var svg = document.getElementsByTagName('svg')[0];
    var pt  = svg.createSVGPoint();
    var matrix  = evt.currentTarget.getCTM();
    pt.x = evt.currentTarget.cx.baseVal.value;
    pt.y = evt.currentTarget.cy.baseVal.value;
    rpt = pt.matrixTransform(matrix);
    tooltip.setAttributeNS(null,"x",rpt.x);
    tooltip.setAttributeNS(null,"y",rpt.y - 20);

    var ttl = evt.target.getAttributeNS(null,"id").split(".");
    ttl.shift();
    tooltip.firstChild.data = ttl.join(".");
    tooltip.setAttributeNS(null,"visibility","visible");
}

function HideTooltip(evt) {
    tooltip.setAttributeNS(null,"visibility","hidden");
}
