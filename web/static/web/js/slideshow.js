// =========== FUNCTIONS ==========

function ResetAll()
{
    GetProjects();
    ResetSlideshow();
    SetProjectPoses(0);
}
function GetProjects()
{
    /* PSEUDOCODE
    projects = [];
    for (var i = 0; i < { % PROJECT_COUNT % }; i++)
    {
        var newProj = {};
        newProj["title"] = { % PROJECT_TITLE % }
        newProj["desc"] = { % PROJECT_DESC % }
        newProj["img"] = { % PROJECT_IMG % }
        newProj["link"] = { % PROJECT_LINK % }
        projects.push(newProj);
    }
    */
}
function ResetSlideshow()
{
    GetSlideshow();
    slideshowEL.innerHTML = "";
    currentProject = Math.floor(projects.length/2);
    AddProjects();
    SetProjectPoses();
}
function AddProjects()
{
    for (var i = 0; i < projects.length; i++)
    {
        AddProject(i);
    }
}
function AddProject(i)
{  // i is index of the project in projects variable
    var projectEL = document.createElement("div");
    projectEL.index = i;
    projectEL.className = "project";
    projectEL.style.backgroundColor = "rgb("+(40*i)+","+(255-40*i)+","+128+")";
    projectEL.style.width = projectWidth+"px";
    projectEL.style.height = projectHeight+"px";

    var pixelPos = GetTargetPixelPosition(projectEL);
    projectEL.style.left = pixelPos+"px";
    projectEL.pixelPos = pixelPos;

    AddElementsToProject(projectEL, i);

    slideshowEL.appendChild(projectEL);
}
function AddElementsToProject(pEL, i)
{
    var project = projects[i];

    var titleEL = document.createElement("div");
    titleEL.innerText = project["title"];

    var imgEL = document.createElement("img");
    imgEL.src = project["img"];

    var descEL = document.createElement("div");
    descEL.innerText = project["desc"];

    pEL.appendChild(titleEL);
    pEL.appendChild(descEL);
    pEL.appendChild(imgEL);
}
function GetSlideshow()
{  // Updates slideshowEL to find the slideshow div in HTML
    bodyEL = document.body;
    slideshowEL = document.getElementById("slideshow");
    if (slideshowEL == null) console.error("ERROR: couldn't find slideshow element. Did you forget to add a <div id='slideshow'> in the HTML?");
    projectELs = slideshowEL.children;
}
function SwitchToProject(e)
{
    var newProjectEL = e.target;
    if (newProjectEL.className != "project")
    newProjectEL = newProjectEL.parentNode;
    currentProject = newProjectEL.index; // The index of the project that will be centered
    SetProjectPoses();
}
function SetProjectPoses()
{
    for (var i = 0; i < projectELs.length; i++)
    {
        SetProjectPos(projectELs[i]);
    }   
    //InterpolateAnimation();
}
function SetProjectPos(projectEL)
{
    var pixelPos = GetTargetPixelPosition(projectEL);
    projectEL.style.left = pixelPos+"px";
}
function GetTargetPixelPosition(projectEL)
{
    var midPos = Math.floor(bodyEL.clientWidth/2);
    var adjustToCenter = Math.floor(projectWidth/2);
    var index = projectEL.index;
    var absPos = index-currentProject;

    if (IsOverflowing(absPos))
    {
        // Overflowing. Checks if it doesn't overflow if wrapped around.
        var tempPos = absPos + projects.length;
        if (!IsOverflowing(tempPos)) absPos = tempPos;
        else
        {
            tempPos = absPos - projects.length;
            if (!IsOverflowing(tempPos)) absPos = tempPos;
        }
    }
    var overflow = IsOverflowing(absPos);

    if (absPos == 0)
    {
        projectEL.removeEventListener("click", SwitchToProject);
        projectEL.addEventListener("click", OpenProject);
    }
    else
    {
        projectEL.removeEventListener("click", OpenProject)
        projectEL.addEventListener("click", SwitchToProject);
    }

    projectEL.overflow = overflow;
    if (overflow) projectEL.style.display = "none";
    else projectEL.style.display = "inline-block";
    var finalPos = midPos-adjustToCenter+absPos*(projectWidth*1.1);
    return finalPos;
}
function IsOverflowing(pos)
{
    return (pos < -visibleSideProjects || pos > visibleSideProjects);
}
function OpenProject(e)
{
    var projectEL = e.target;
    var index = projectEL.index;
    var link = projects[index]["link"];
    window.location.href = link;
}
function InterpolateAnimation()
{

    var continueRecursion = false;
    for (var i = 0; i < projectELs.length; i++)
    {
        var projectEL = projectELs[i];
        var posInSlideshow = projectEL.posInSlideshow;
        var finalPos = GetTargetPixelPosition(projectEL);

        var previousPos = parseInt(projectEL.style.left);
        var nextPos =(previousPos*(1-interpolationSpeed)+finalPos*interpolationSpeed);
        var pixelPos;
        if (Math.abs(finalPos-nextPos) < 2)
        {
            pixelPos = finalPos;
        } else
        {
            pixelPos = nextPos;
            continueRecursion = true;
        }
        projectEL.style.left = pixelPos+"px";
        projectEL.pixelPos = pixelPos;

        var opacity = 1-Math.abs(posInSlideshow/4);
        projectEL.style.opacity = opacity;
        if (opacity <= 0) projectEL.style.display = "none";
        else projectEL.style.display = "inline-block";

    }
    if (continueRecursion)
    {
                setTimeout(function() { InterpolateAnimation(); }, animationInterval);
    }
}
function CreateProject(title, img, link, desc)
{
    var newObj = {};
    newObj["title"] = title;
    newObj["img"] = img;
    newObj["link"] = link;
    newObj["desc"] = desc;
    projects.push(newObj);
    ResetAll();
}

// ========== GLOBAL VARIABLES ==========
var currentProject; // Stores index of the current project in slideshow
var bodyEL;
var slideshowEL;
var projectELs;  // Stores elements
var interpolationSpeed = 0.05;
var animationInterval = 16;  // in ms, how long to wait between position set
var projectWidth = 600;
var projectHeight = 400;
var visibleSideProjects = 1;  // How many extra projects should display on each side of the current project preview
var projects =  // Some fancy django function to get projects from database?
[
    {"title":"Fake News Generator", "img":"", "link":"https://google.com", "desc":"Vi mekka en sånn derre AI greie som produsere fake tweets av Donald Trump"},
    {"title":"Cogitron", "img":"", "link":"https://google.com", "desc":"Cogitron e en sånn derre robot som utforske omgivelsan og nice greier"},
    {"title":"Testprosjekt", "img":"", "link":"https://google.com", "desc":"Det her e egentlig ikke et prosjekt, bare no æ la te for å test slideshow"},
    {"title":"Testprosjek2", "img":"", "link":"https://google.com", "desc":"Samme med den her egentlig"}
];

// ========== INITIALIZATION ==========
document.addEventListener("scroll", SetProjectPoses);
window.addEventListener("resize", SetProjectPoses);
ResetAll();