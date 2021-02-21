// Global timer used for doing animation callbacks
//  TODO:  Make this an instance variable of Animation Manager
var timer;
var swapped = false;

function reorderSibling(node1, node2)
{
    node1.parentNode.replaceChild(node1, node2);
    node1.parentNode.insertBefore(node2, node1);
}

function swapControlDiv()
{
    swapped = !swapped;
    if (swapped) {
	reorderSibling(document.getElementById('canvas'), document.getElementById('generalAnimationControlSection'));
        setCookie("VisualizationControlSwapped", "true", 30);

    } else {
	reorderSibling(document.getElementById('generalAnimationControlSection'), document.getElementById('canvas'));
        setCookie("VisualizationControlSwapped", "false", 30);

    }
}

// Utility funciton to read a cookie
function getCookie(cookieName)
{
	var i, x, y;
	var cookies=document.cookie.split(";");
	for (i=0; i < cookies.length; i++)
	{
		x=cookies[i].substr(0,cookies[i].indexOf("="));
		y=cookies[i].substr(cookies[i].indexOf("=")+1);
		x=x.replace(/^\s+|\s+$/g,"");
		if (x==cookieName)
		{
			return unescape(y);
		}
	}
}

// Utility funciton to write a cookie
function setCookie(cookieName,value,expireDays)
{
	var exdate=new Date();
	exdate.setDate(exdate.getDate() + expireDays);
	var cookieValue=escape(value) + ((expireDays==null) ? "" : "; expires="+exdate.toUTCString());
	document.cookie=cookieName + "=" + value;
}

var ANIMATION_SPEED_DEFAULT = 75;

var objectManager;
var animationManager;
var canvas;

var paused = false;
var playPauseBackButton;
var skipBackButton;
var stepBackButton;
var stepForwardButton;
var skipForwardButton;

var widthEntry;
var heightEntry;
var sizeButton;

function returnSubmit(field, funct, maxsize, intOnly)
{

	if (maxsize != undefined)
	{
		field.size = maxsize;
	}
	return function(event)
	{
		var keyASCII = 0;
		if(window.event) // IE
		{
			keyASCII = event.keyCode
		}
		else if (event.which) // Netscape/Firefox/Opera
		{
			keyASCII = event.which
		}

		if (keyASCII == 13)
		{
			funct();
                        return false;
		}
        	else if (keyASCII == 59  || keyASCII == 45 || keyASCII == 46 || keyASCII == 190 || keyASCII == 173)
		{
		       return false;
		}
		else if (maxsize != undefined && field.value.length >= maxsize ||
				 intOnly && (keyASCII < 48 || keyASCII > 57))

		{
			if (!controlKey(keyASCII))
				return false;
		}
	    return true;
	}
}

function animWaiting()
{
	stepForwardButton.disabled = false;
	if (skipBackButton.disabled == false)
	{
		stepBackButton.disabled = false;
	}
	objectManager.statusReport.setText("Animation Paused");
	objectManager.statusReport.setForegroundColor("#FF0000");
}

function animStarted()
{
	skipForwardButton.disabled = false;
	skipBackButton.disabled = false;
	stepForwardButton.disabled = true;
	stepBackButton.disabled = true;
	objectManager.statusReport.setText("Animation Running");
	objectManager.statusReport.setForegroundColor("#009900");
}

function animEnded()
{
	skipForwardButton.disabled = true;
	stepForwardButton.disabled = true;
	if (skipBackButton.disabled == false && paused)
	{
		stepBackButton.disabled = false;
	}
	objectManager.statusReport.setText("Animation Completed");
	objectManager.statusReport.setForegroundColor("#000000");
}

function anumUndoUnavailable()
{
	skipBackButton.disabled = true;
	stepBackButton.disabled = true;
}

function timeout()
{
	// We need to set the timeout *first*, otherwise if we
	// try to clear it later, we get behavior we don't want ...
    timer = setTimeout('timeout()', 30);
	animationManager.update();
	objectManager.draw();
}

function doStep()
{
	animationManager.step();
}

function doSkip()
{
	animationManager.skipForward();
}

function doSkipBack()
{
	animationManager.skipBack();
}

function doStepBack()
{
	animationManager.stepBack();
}

function doPlayPause()
{
	paused = !paused;
	if (paused)
	{
		playPauseBackButton.setAttribute("value", "play");
		if (skipBackButton.disabled == false)
		{
			stepBackButton.disabled = false;
		}
	}
	else
	{
		playPauseBackButton.setAttribute("value", "pause");
	}
	animationManager.SetPaused(paused);
}

function addControlToAnimationBar(type,name,containerType)
{
	if (containerType == undefined)
	{
			containerType = "input";
	}
	var element = document.createElement(containerType);

        element.setAttribute("type", type);
        element.setAttribute("value", name);

	var tableEntry = document.createElement("td");
	tableEntry.appendChild(element);
    var controlBar = document.getElementById("GeneralAnimationControls");

    //Append the element in page (in span).
    controlBar.appendChild(tableEntry);
	return element;
}

function initCanvas()
{
	canvas =  document.getElementById("canvas");
	objectManager = new ObjectManager();
	animationManager = new AnimationManager(objectManager);

	var element = document.createElement("div");
	element.setAttribute("display", "inline-block");
	element.setAttribute("float", "left");
	var tableEntry = document.createElement("td");
    var controlBar = document.getElementById("GeneralAnimationControls");

    //Append the element in page (in span).
    controlBar.appendChild(tableEntry);
    tableEntry.appendChild(element);

	element.setAttribute("style", "width:300px");

	var width=getCookie("VisualizationWidth");
	if (width == null || width == "")
	{
		width = canvas.width;
	}
	else
	{
		width = parseInt(width);
	}
	var height = getCookie("VisualizationHeight");
	if (height == null || height == "")
	{
		height = canvas.height;
	}
	else
	{
		height = parseInt(height);
	}

	var swappedControls=getCookie("VisualizationControlSwapped");
	swapped = swappedControls == "true"
        if (swapped)
        {
	    reorderSibling(document.getElementById('canvas'), document.getElementById('generalAnimationControlSection'));
	}

	canvas.width = width;
	canvas.height = height;

	tableEntry = document.createElement("td");
	txtNode = document.createTextNode("    Width:");
	tableEntry.appendChild(txtNode);
	controlBar.appendChild(tableEntry);

	widthEntry = addControlToAnimationBar("Text", canvas.width);
	widthEntry.size = 4;
	widthEntry.onkeydown = this.returnSubmit(widthEntry, animationManager.changeSize.bind(animationManager), 4, true);

	tableEntry = document.createElement("td");
	txtNode = document.createTextNode("    Height:");
	tableEntry.appendChild(txtNode);
	controlBar.appendChild(tableEntry);

	heightEntry = addControlToAnimationBar("Text", canvas.height);
	heightEntry.onkeydown = this.returnSubmit(heightEntry, animationManager.changeSize.bind(animationManager), 4, true);

	sizeButton = addControlToAnimationBar("Button", "Change Canvas Size");

	sizeButton.onclick = animationManager.changeSize.bind(animationManager) ;

	objectManager.width = canvas.width;
	objectManager.height = canvas.height;
	return animationManager;
}

function AnimationManager(objectManager)
{
	// Holder for all animated objects.
	// All animation is done by manipulating objects in this container
	this.animatedObjects = objectManager;

	// Control variables for stopping / starting animation

	this.animationPaused = false;
	this.awaitingStep = false;
	this.currentlyAnimating = false;

	// Array holding the code for the animation.  This is
	// an array of strings, each of which is an animation command
	// currentAnimation is an index into this array
	this.AnimationSteps = [];
	this.currentAnimation = 0;

	this.previousAnimationSteps = [];

	// Control variables for where we are in the current animation block.
	// currFrame holds the frame number of the current animation block,
	// while animationBlockLength holds the length of the current animation
	// block (in frame numbers).
	this.currFrame = 0;
	this.animationBlockLength = 0;

	//  The animation block that is currently running.  Array of singleAnimations
	this.currentBlock = null;

	/////////////////////////////////////
	// Variables for handling undo.
	////////////////////////////////////
	//  A stack of UndoBlock objects (subclassed, UndoBlock is an abstract base class)
	//  each of which can undo a single animation element
	this.undoStack = [];
	this.doingUndo = false;

	// A stack containing the beginning of each animation block, as an index
	// into the AnimationSteps array
	this.undoAnimationStepIndices = [];
	this.undoAnimationStepIndicesStack = [];

	this.animationBlockLength = 10;

	this.lerp = function(from, to, percent)
	{
		return (to - from) * percent + from;
	}

	// Pause / unpause animation
	this.SetPaused = function(pausedValue)
	{
		this.animationPaused = pausedValue;
		if (!this.animationPaused)
		{
			this.step();
		}
	}

	// Set the speed of the animation, from 0 (slow) to 100 (fast)
	this.SetSpeed = function(newSpeed)
	{
		this.animationBlockLength = Math.floor((100-newSpeed) / 2);
	}

	this.parseBool = function(str)
	{
		var uppercase = str.toUpperCase();
		var returnVal =  !(uppercase == "False" || uppercase == "f" || uppercase == " 0" || uppercase == "0" || uppercase == "");
		return returnVal;

	}

	this.parseColor = function(clr)
	{
			if (clr.charAt(0) == "#")
			{
				return clr;
			}
			else if (clr.substring(0,2) == "0x")
			{
				return "#" + clr.substring(2);
			}
	}

	this.changeSize = function()
	{
		var width = parseInt(widthEntry.value);
		var height = parseInt(heightEntry.value);

		if (width > 100)
		{
			canvas.width = width;
			this.animatedObjects.width = width;
			setCookie("VisualizationWidth", String(width), 30);

		}
		if (height > 100)
		{
			canvas.height = height;
			this.animatedObjects.height = height;
			setCookie("VisualizationHeight", String(height), 30);
		}
		width.value = canvas.width;
		heightEntry.value = canvas.height;

		this.animatedObjects.draw();
		this.fireEvent("CanvasSizeChanged",{width:canvas.width, height:canvas.height});
	}

	this.startNextBlock = function()
	{
		this.awaitingStep = false;
		this.currentBlock = [];
		var undoBlock = []
		if (this.currentAnimation == this.AnimationSteps.length )
		{
			this.currentlyAnimating = false;
			this.awaitingStep = false;
			this.fireEvent("AnimationEnded","NoData");
			clearTimeout(timer);
			this.animatedObjects.update();
			this.animatedObjects.draw();

			return;
		}
		this.undoAnimationStepIndices.push(this.currentAnimation);

		var foundBreak= false;
		var anyAnimations= false;

		while (this.currentAnimation < this.AnimationSteps.length && !foundBreak)
		{
			var nextCommand = this.AnimationSteps[this.currentAnimation].split("<;>");
			if (nextCommand[0].toUpperCase() == "CREATECIRCLE")
			{
				this.animatedObjects.addCircleObject(parseInt(nextCommand[1]), nextCommand[2]);
				if (nextCommand.length > 4)
				{
					this.animatedObjects.setNodePosition(parseInt(nextCommand[1]), parseInt(nextCommand[3]), parseInt(nextCommand[4]));
				}
				undoBlock.push(new UndoCreate(parseInt(nextCommand[1])));

			}
			else if (nextCommand[0].toUpperCase() == "CONNECT")
			{

				if (nextCommand.length > 7)
				{
					this.animatedObjects.connectEdge(parseInt(nextCommand[1]),
                                                                         parseInt(nextCommand[2]),
                                                                         this.parseColor(nextCommand[3]),
                                                                         parseFloat(nextCommand[4]),
                                                                         this.parseBool(nextCommand[5]),
                                                                         nextCommand[6],
                                                                         parseInt(nextCommand[7]));
				}
				else if (nextCommand.length > 6)
				{
					this.animatedObjects.connectEdge(parseInt(nextCommand[1]),
                                                                         parseInt(nextCommand[2]),
                                                                         this.parseColor(nextCommand[3]),
                                                                         parseFloat(nextCommand[4]),
                                                                         this.parseBool(nextCommand[5]),
                                                                         nextCommand[6],
                                                                         0);
				}
				else if (nextCommand.length > 5)
				{
					this.animatedObjects.connectEdge(parseInt(nextCommand[1]),
                                                                         parseInt(nextCommand[2]),
                                                                         this.parseColor(nextCommand[3]),
                                                                         parseFloat(nextCommand[4]),
                                                                         this.parseBool(nextCommand[5]),
                                                                         "",
                                                                         0);
				}
				else if (nextCommand.length > 4)
				{
					this.animatedObjects.connectEdge(parseInt(nextCommand[1]),
                                                                         parseInt(nextCommand[2]),
                                                                         this.parseColor(nextCommand[3]),
                                                                         parseFloat(nextCommand[4]),
                                                                         true,
                                                                         "",
                                                                         0);
				}
				else if (nextCommand.length > 3)
				{
					this.animatedObjects.connectEdge(parseInt(nextCommand[1]),
                                                                         parseInt(nextCommand[2]),
																		 this.parseColor(nextCommand[3]),
                                                                         0.0,
                                                                         true,
                                                                         "",
                                                                         0);
				}
				else
				{
					this.animatedObjects.connectEdge(parseInt(nextCommand[1]),
                                                                         parseInt(nextCommand[2]),
													                    "#000000",
                                                                         0.0,
                                                                         true,
                                                                         "",
                                                                         0);

				}
				undoBlock.push(new UndoConnect(parseInt(nextCommand[1]), parseInt (nextCommand[2]), false));
			}
			else if (nextCommand[0].toUpperCase() == "CREATERECTANGLE")
			{
				if (nextCommand.length == 9)
				{
					this.animatedObjects.addRectangleObject(parseInt(nextCommand[1]), // ID
															nextCommand[2], // Label
															parseInt(nextCommand[3]), // w
															parseInt(nextCommand[4]), // h
															nextCommand[7], // xJustify
															nextCommand[8],// yJustify
															"#ffffff", // background color
					                                        "#000000"); // foreground color
				}
				else
				{
					this.animatedObjects.addRectangleObject(parseInt(nextCommand[1]), // ID
															nextCommand[2], // Label
															parseInt(nextCommand[3]), // w
															parseInt(nextCommand[4]), // h
															"center", // xJustify
															"center",// yJustify
															"#ffffff", // background color
					                                        "#000000"); // foreground color

				}
				if (nextCommand.length > 6)
				{
					this.animatedObjects.setNodePosition(parseInt(nextCommand[1]), parseInt(nextCommand[5]), parseInt(nextCommand[6]));
				}
				undoBlock.push(new UndoCreate(parseInt(nextCommand[1])));
			}

			else if (nextCommand[0].toUpperCase() == "MOVE")
			{
				var objectID = parseInt(nextCommand[1]);
				var nextAnim =  new SingleAnimation(objectID,
													this.animatedObjects.getNodeX(objectID),
													this.animatedObjects.getNodeY(objectID),
													parseInt(nextCommand[2]),
													parseInt(nextCommand[3]));
				this.currentBlock.push(nextAnim);

				undoBlock.push(new UndoMove(nextAnim.objectID, nextAnim.toX, nextAnim.toY, nextAnim.fromX, nextAnim.fromY));

				anyAnimations = true;
			}
			else if (nextCommand[0].toUpperCase() == "DISCONNECT")
			{
				var undoConnect = this.animatedObjects.disconnect(parseInt(nextCommand[1]), parseInt(nextCommand[2]));
				if (undoConnect != null)
				{
					undoBlock.push(undoConnect);
				}
			}
			else if (nextCommand[0].toUpperCase() == "SETTEXT")
			{
				if (nextCommand.length > 3)
				{
					var oldText = this.animatedObjects.getText(parseInt(nextCommand[1]), parseInt(nextCommand[3]));
					this.animatedObjects.setText(parseInt(nextCommand[1]), nextCommand[2], parseInt(nextCommand[3]));
					if (oldText != undefined)
					{
						undoBlock.push(new UndoSetText(parseInt(nextCommand[1]), oldText, parseInt(nextCommand[3]) ));
					}
				}
				else
				{
					oldText = this.animatedObjects.getText(parseInt(nextCommand[1]), 0);
					this.animatedObjects.setText(parseInt(nextCommand[1]), nextCommand[2], 0);
					if (oldText != undefined)
					{
						undoBlock.push(new UndoSetText(parseInt(nextCommand[1]), oldText, 0));
					}
				}
			}
			else if (nextCommand[0].toUpperCase() == "DELETE")
			{
				var objectID  = parseInt(nextCommand[1]);

				var i;
				var removedEdges = this.animatedObjects.deleteIncident(objectID);
				if (removedEdges.length > 0)
				{
					undoBlock = undoBlock.concat(removedEdges);
				}
				var obj = this.animatedObjects.getObject(objectID);
				if (obj != null)
				{
					undoBlock.push(obj.createUndoDelete());
					this.animatedObjects.removeObject(objectID);
				}
			}
			else if (nextCommand[0].toUpperCase() == "CREATELABEL")
			{
				if (nextCommand.length == 6)
				{
					this.animatedObjects.addLabelObject(parseInt(nextCommand[1]), nextCommand[2], this.parseBool(nextCommand[5]));
				}
				else
				{
					this.animatedObjects.addLabelObject(parseInt(nextCommand[1]), nextCommand[2], true);
				}
				if (nextCommand.length >= 5)
				{

					this.animatedObjects.setNodePosition(parseInt(nextCommand[1]), parseFloat(nextCommand[3]), parseFloat(nextCommand[4]));
				}
				undoBlock.push(new UndoCreate(parseInt(nextCommand[1])));
			}
			else
			{
				// throw "Unknown command: " + nextCommand[0];
			}

			this.currentAnimation = this.currentAnimation+1;
		}
		this.currFrame = 0;

		// Hack:  If there are not any animations, and we are currently paused,
		// then set the current frame to the end of the anumation, so that we will
		// advance immediagely upon the next step button.  If we are not paused, then
		// animate as normal.

		if (!anyAnimations && this.animationPaused || (!anyAnimations && this.currentAnimation == this.AnimationSteps.length) )
		{
			this.currFrame = this.animationBlockLength;
		}

		this.undoStack.push(undoBlock);
	}

	//  Start a new animation.  The input parameter commands is an array of strings,
	//  which represents the animation to start
	this.StartNewAnimation =  function(commands)
	{
		clearTimeout(timer);
		if (this.AnimationSteps != null)
		{
			this.previousAnimationSteps.push(this.AnimationSteps);
			this.undoAnimationStepIndicesStack.push(this.undoAnimationStepIndices);
		}
		if (commands == undefined || commands.length == 0)
		{
			this.AnimationSteps = ["Step"];
		}
		else
		{
			this.AnimationSteps = commands;
		}
		this.undoAnimationStepIndices = new Array();
		this.currentAnimation = 0;
		this.startNextBlock();
		this.currentlyAnimating = true;
		this.fireEvent("AnimationStarted","NoData");
		timer = setTimeout('timeout()', 30);
	}

	/// WARNING:  Could be dangerous to call while an animation is running ...
	this.clearHistory = function()
	{
		this.undoStack = [];
		this.undoAnimationStepIndices = null;
		this.previousAnimationSteps = [];
		this.undoAnimationStepIndicesStack = [];
		this.AnimationSteps = null;
		this.fireEvent("AnimationUndoUnavailable","NoData");
		clearTimeout(timer);
		this.animatedObjects.update();
		this.animatedObjects.draw();

	}

	this.resetAll = function()
	{
		this.clearHistory();
		this.animatedObjects.clearAllObjects();
		this.animatedObjects.draw();
		clearTimeout(timer);
	}

	this.skipForward = function()
	{
		if (this.currentlyAnimating)
		{
			this.animatedObjects.runFast = true;
			while (this.AnimationSteps != null && this.currentAnimation < this.AnimationSteps.length)
			{
				var i;
				for (i = 0; this.currentBlock != null && i < this.currentBlock.length; i++)
				{
					var objectID = this.currentBlock[i].objectID;
					this.animatedObjects.setNodePosition(objectID,
													this.currentBlock[i].toX,
													this.currentBlock[i].toY);
				}
				if (this.doingUndo)
				{
					this.finishUndoBlock(this.undoStack.pop())
				}
				this.startNextBlock();
				for (i= 0; i < this.currentBlock.length; i++)
				{
					var objectID = this.currentBlock[i].objectID;
					this.animatedObjects.setNodePosition(objectID,
													this.currentBlock[i].toX,
													this.currentBlock[i].toY);
				}

			}
			this.animatedObjects.update();
			this.currentlyAnimating = false;
			this.awaitingStep = false;
			this.doingUndo = false;

			this.animatedObjects.runFast = false;
			this.fireEvent("AnimationEnded","NoData");
			clearTimeout(timer);
			this.animatedObjects.update();
			this.animatedObjects.draw();
		}
	}
}

AnimationManager.prototype = new EventListener();
AnimationManager.prototype.constructor = AnimationManager;

function SingleAnimation(id, fromX, fromY, toX, toY)
{
	this.objectID = id;
	this.fromX = fromX;
	this.fromY = fromY;
	this.toX = toX;
	this.toY = toY;
}
