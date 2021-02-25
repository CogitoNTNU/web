// slideshow can be customized at the bottom of this js file.
// modifying anything else in this file may or may not create an abomination

// IF SLIDESHOW ISN'T SHOWING UP/LOOKING ALRIGHT:
// don't have multiple slideshows on one page. this code only handles one
// remember to include slideshow.css, can be done with putting <link rel="stylesheet" type="text/css" href="/static/web/css/slideshow.css"> inside of <head>
// Copy-paste this into your html file:
/*

	<div id="slideshow"></div>
	<script src="{% static 'web/js/slideshow.js' %}">
	</script>
	{% for project in projects %}
	{% if project.thumbnail %}
	<script>
		// gets name, img, link, desc from django database
		CreateProject("{{ project.title }}", "/media/{{ project.thumbnail.name }}", "projects/project/{{ project.pk }}", "");
	</script>
	{% endif %}
	{% endfor %}
	<script>
		ResetAll();
	</script>

*/
// The <div id="slideshow"></div> may be moved to mostly anywhere in the document.

// =========== FUNCTIONS ==========

function ResetAll()
{
    ResetSlideshow();
}
function ResetSlideshow()
{
    currentProject = 0;
    SetupSlideshow();
}
function SetupSlideshow()
{  // Updates slideshowEL to find the slideshow div in HTML
    bodyEL = document.body;
    slideshowEL = document.getElementById("slideshow");
    if (slideshowEL == null) console.error("ERROR: couldn't find slideshow element. Did you forget to add a <div id='slideshow'> in the HTML?");
    slideshowEL.innerHTML = "";
    explanationEL = document.createElement("div");
    contentWrapperEL = document.createElement("div");
    textWrapperEL = document.createElement("div");
    imgWrapperEL = document.createElement("div");
    imgEL = document.createElement("img");
    titleEL = document.createElement("div");
    descEL = document.createElement("div");

    lButtonWrapperEL = document.createElement("div");
    lButtonEL = document.createElement("img");
    rButtonWrapperEL = document.createElement("div");
    rButtonEL = document.createElement("img");

    // Setting ids for elements so slideshow.css can modify their style
    //slideshowEL.id = "slideshow";  // already set in html
    explanationEL.id = "slideExplanation";
    lButtonWrapperEL.id = "slideLButtonWrapper";
    rButtonWrapperEL.id = "slideRButtonWrapper";
    lButtonEL.id = "slideLButton";
    rButtonEL.id = "slideRButton";
    contentWrapperEL.id = "slideContentWrapper";
    imgWrapperEL.id = "slideImgWrapper";
    textWrapperEL.id = "slideTextWrapper";
    titleEL.id = "slideTitle";
    descEL.id = "slideDesc";
    imgEL.id = "slideImg";

    lButtonWrapperEL.className = "slideButtonWrapper";
    rButtonWrapperEL.className = "slideButtonWrapper";
    lButtonEL.className = "slideButton";
    rButtonEL.className = "slideButton";

    lButtonEL.src = buttonImage;
    rButtonEL.src = buttonImage;
    explanationEL.innerText = explanation;

    var explanationHeight = explanationSize+explanationPadding*2;
    var slideshowHeight = projectHeight+explanationHeight;

    slideshowEL.style.width = projectWidth+"px";
    slideshowEL.style.height = slideshowHeight+"px";

    explanationEL.style.paddingTop = explanationPadding+"px";
    explanationEL.style.paddingBottom = explanationPadding+"px";
    explanationEL.style.fontSize = explanationSize+"px";
    explanationEL.style.height = explanationHeight+"px";
    
    contentWrapperEL.style.height = projectHeight+"px";
    contentWrapperEL.addEventListener("click", OpenProject);

    var imgWrapperWidth = relImgWidth*projectWidth;
    var textWrapperWidth = (1-relImgWidth)*projectWidth;
    imgWrapperEL.style.width = imgWrapperWidth+"px";

    textWrapperEL.style.width = textWrapperWidth+"px";
    textWrapperEL.style.height = projectHeight+"px";
    textWrapperEL.style.marginLeft = imgWrapperWidth+"px";

    titleEL.style.height = titleHeight+"px";
    titleEL.style.fontSize = titleSize*titleHeight+"px";
    var paddingTitleTop = (1-titleSize)/2*titleHeight;
    var padding = textPadding/2*textWrapperWidth;
    titleEL.style.paddingTop = paddingTitleTop+"px";
    titleEL.style.paddingLeft = padding+"px";

    descEL.style.height = projectHeight-titleHeight+"px";
    descEL.style.padding = padding+"px";

    var buttonWrapperMarginTop = projectHeight/2-buttonSize/2;
    
    lButtonWrapperEL.style.marginLeft = -buttonSize*(1+buttonDistance)+"px";
    lButtonWrapperEL.style.marginTop = buttonWrapperMarginTop+"px";
    lButtonWrapperEL.style.width = buttonSize+"px";
    lButtonWrapperEL.style.height = buttonSize+"px";

    rButtonWrapperEL.style.marginLeft = projectWidth+buttonSize*buttonDistance+"px";
    rButtonWrapperEL.style.marginTop = buttonWrapperMarginTop+"px";
    rButtonWrapperEL.style.width = buttonSize+"px";
    rButtonWrapperEL.style.height = buttonSize+"px";

    lButtonEL.addEventListener("click", ClickLeft);
    rButtonEL.addEventListener("click", ClickRight);

    lButtonWrapperEL.appendChild(lButtonEL);
    rButtonWrapperEL.appendChild(rButtonEL);
    textWrapperEL.appendChild(titleEL);
    textWrapperEL.appendChild(descEL);
    imgWrapperEL.appendChild(imgEL);
    contentWrapperEL.appendChild(textWrapperEL);
    contentWrapperEL.appendChild(imgWrapperEL);
    slideshowEL.appendChild(explanationEL);
    slideshowEL.appendChild(lButtonWrapperEL);  // lButton before contentWrapper
    slideshowEL.appendChild(rButtonWrapperEL);  // rButton before contentWrapper
    slideshowEL.appendChild(contentWrapperEL);

    ShowCurrentProject();
}
function ClickLeft()
{
    ChangeProject(-1);
}
function ClickRight()
{
    ChangeProject(1);
}
function ChangeProject(by)
{
    currentProject += by;
    if (currentProject < 0) currentProject = projects.length-1;
    else if (currentProject >= projects.length) currentProject = 0;
    ShowCurrentProject();
}
function ShowCurrentProject()
{
    var project = projects[currentProject];
    var img = project["img"];
    if (img == "") imgEL.src = defaultImg;
    else imgEL.src = img;
    titleEL.innerText = project["title"];
    descEL.innerText = project["desc"];
    slideshowEL.link = project["link"];
}
function OpenProject()
{
    var p = projects[currentProject];
    var link = p["link"];
    window.location.href = link;
}
function CreateProject(title, img, link, desc)
{
    var newObj = {};
    newObj["title"] = title;
    newObj["img"] = img;
    newObj["link"] = link;
    newObj["desc"] = desc;
    projects.push(newObj);
}

// ========== GLOBAL VARIABLES ==========
var currentProject; // Stores index of the current project in slideshow
var bodyEL;
var slideshowEL;  // contains contentWrapperEL, lButtonWrapperEL, and rButtonWrapperEL
var explanationEL;  // the thing above content
var contentWrapperEL;  // contains textWrapperEL and imgWrapperEL
var textWrapperEL;  // contains titleEL and descEL
var imgWrapperEL;  // contains imgEL
var imgEL;
var titleEL;
var descEL;
var lButtonWrapperEL;  // contains lButtonEL
var lButtonEL;
var rButtonWrapperEL;  // you can probably figure out what this contains
var rButtonEL;



// ========== CONFIG/CUSTOMIZATION ==========
var explanation = "Noen av våre prosjekter";
var defaultImg = "/static/web/img/logo.svg";
var relImgWidth = 0.4;  // Fraction of projectWidth, how much space should the image take? (0-1)
var explanationSize = 50;  // font size in pixels
var explanationPadding = 40;  // pixels
var projectWidth = 800;  // How many pixels width should image and text make up together
var projectHeight = 350;  // Same, but for height
var titleHeight = 50;  // Pixels
var titleSize = 0.7;  // font size, as a fraction of title height (0-1)
var textPadding = 0.1;  // how large fraction of the textarea should be padding? (0-1)
var buttonSize = 100;  // Pixels
var buttonDistance = 0.2;  // distance from slideshow, as a fraction of its size (anything really)
var buttonImage = "https://image.flaticon.com/icons/png/512/61/61791.png";  // TODO: get copyright free image

var projects =  // Some fancy django function to get projects from database?
[
    {"title":"Fake News Generator", "img":"", "link":"https://google.com", "desc":"Vi mekka en sånn derre AI greie som produsere fake tweets av Donald Trump"},
    {"title":"Cogitron", "img":"", "link":"https://google.com", "desc":"Cogitron e en sånn derre robot som utforske omgivelsan og nice greier"},
    {"title":"Testprosjekt som har et veldig langt navn for å teste hvordan den oppfører seg når navnet er veldig langt", "img":"", "link":"https://google.com", "desc":"Det her e egentlig ikke et prosjekt, bare no æ la te for å test slideshow. I tillegg har den en veldig lang description sånn at æ kan få testa koss det ser ut på nettsida, vil den overflowe eller bare kutt teksten? Se neste episode av torbjørns bizarre adventure for å finn ut kordan html tolke det her"},
    {"title":"Testprosjek2", "img":"", "link":"https://google.com", "desc":"Samme med den her egentlig"}
];