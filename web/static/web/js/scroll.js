var scrollClass = "scroll";
var defaultScrollScalar = 1;  // relative, typically [-1, 1]
var defaultScrollOffset = 0;  // in px

function init() {
    forAllScrollELsDo(logInitialY);
    addPageEvents();
    scrollPage();
}
function addPageEvents() {
    document.addEventListener("scroll", scrollPage);
    window.addEventListener("resize", scrollPage);
}
function scrollPage() {
    forAllScrollELsDo(scroll);
}
function forAllScrollELsDo(f) {
    var scrollELs = getScrollELs();
    for (var i = 0; i < scrollELs.length; i++) {
        var el = scrollELs[i];
        f(el);
    }
}
function scroll(el) {
    var pageY = getPageY();
    var iY = el.iY;
    var d = el.dataset;
    var scrollScalar = d.scrollscalar || defaultScrollScalar;
    var scrollOffset = d.scrolloffset|| defaultScrollOffset;
    var scrollAnchorBottom = d.scrollanchorbottom || false;


    var newY = scrollScalar*pageY + iY - scrollOffset;

    
    // for some reason, this must be done on mobile
    if (isMobile() && scrollAnchorBottom && el.offsetTop < 0) {
        newY -= el.offsetTop;
    }

    // really atrocious code
    el.parentNode.style.position = "relative";
    el.parentNode.style.overflow = "hidden";

    el.style.position = "absolute";
    el.style.top = newY+"px";
    console.log(el.style.top);

}
function logInitialY(el) {
    var y = el.getBoundingClientRect().top;
    var docY = document.documentElement.scrollTop;
    var iY = y + docY;
    el.iY = iY;
}
function getPageY() {
    return window.pageYOffset || document.documentElement.scrollTop;
}
function getScrollELs() {
    return document.getElementsByClassName(scrollClass);
}
function getOffsetBottom(el) {
    var top = el.offsetTop;
    var height = el.offsetHeight;
    console.log(top + ", " + height);
    return top + height;
}
function isMobile(el) {
    return /Android|webOS|iPhone|iPad|Mac|Macintosh|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

init();