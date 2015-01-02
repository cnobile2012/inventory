/*
 * The code below was gleaned from:
 *     SuckerTree Vertical Menu 1.1 (Nov 8th, 06)
 *     Dynamic Drive: http://www.dynamicdrive.com/style/
 * with changes for use with jQuery.
 */

//Enter id(s) of SuckerTree UL menus, separated by commas
var menuids = ["suckertree1"];

function buildSubmenus()
    {
    for(var i = 0; i < menuids.length; i++)
        {
        var ultags = $("ul#" + menuids[i] + " ul");

        for(var t = 0; t < ultags.length; t++)
            {
            //var tmp = ultags[t];
            ultags[t].parentNode.getElementsByTagName("a")[0].className="subfolderstyle";
            /*
             * If this is a first level submenu
             *
             * Dynamically position first level submenus to be width of
             * main menu item
             */
            if (ultags[t].parentNode.parentNode.id == menuids[i])
                {
                ultags[t].style.left = ultags[t].parentNode.offsetWidth + "px";
                }
            else // else if this is a sub level submenu (ul)
                // position menu to the right of menu item that activated it
                ultags[t].style.left = ultags[t-1].getElementsByTagName("a")[0].offsetWidth+"px";

            ultags[t].parentNode.onmouseover = function()
                {
                this.getElementsByTagName("ul")[0].style.display = "block";
                }

            ultags[t].parentNode.onmouseout = function()
                {
                this.getElementsByTagName("ul")[0].style.display = "none";
                }
            }

        /*
         * Loop through all sub menus again, and use "display:none" to
         * hide menus (to prevent possible page scrollbars
         */
        for(var t = ultags.length-1; t > -1; t--)
            {
            ultags[t].style.visibility = "visible";
            ultags[t].style.display = "none";
            }
        }
    }

$(document).ready(function() {
    buildSubmenus();
});
