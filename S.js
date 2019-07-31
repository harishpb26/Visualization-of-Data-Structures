var ARRAY_START_X = 100;
var ARRAY_START_Y = 100;
var ARRAY_ELEM_WIDTH = 120;
var ARRAY_ELEM_HEIGHT = 50;

var ARRRAY_ELEMS_PER_LINE = 15;
var ARRAY_LINE_SPACING = 130;

var TOP_POS_X = 200;
var TOP_POS_Y = 200;
var TOP_LABEL_X = 80;
var TOP_LABEL_Y =  60;

var VAR_START_X = 100;
var VAR_START_Y = 360;
var LABEL_X = 80;
var LABEL_Y = 320;
var VAR_ELEM_WIDTH = 120;
var VAR_ELEM_HEIGHT = 50;


// initial coordinates
//var TOP_LABEL_X = 80;
//var TOP_LABEL_Y =  60;
//var ARRAY_START_X = 100;
//var ARRAY_START_Y = 100;
//var ARRAY_ELEM_WIDTH = 120;
//var ARRAY_ELEM_HEIGHT = 50;

//var VAR_START_X = 100;
//var VAR_START_Y = 360;
//var LABEL_X = 80;
//var LABEL_Y = 320;
//var VAR_ELEM_WIDTH = 80;
//var VAR_ELEM_HEIGHT = 50;


/*
$.get("/anime", function(data) {
  dict = $.parseJSON(data);
  console.log($.parseJSON(data));
})
*/

var maindict;
var req = new XMLHttpRequest();
req.open('GET','http://127.0.0.1:8080/animek',false);
req.setRequestHeader('Content-type','application/json; charset=utf-8');
req.onload = function(){
  maindict = JSON.parse(req.responseText);
};
req.send();
//console.log(maindict);


function S(am, w, h)
{
    this.init(am, w, h);
}

S.prototype = new Algorithm();
S.prototype.constructor = S;
S.superclass = Algorithm.prototype;

S.prototype.init = function(am, w, h)
{
    // Call the unit function of our "superclass", which adds a couple of
    // listeners, and sets up the undo stack

    S.superclass.init.call(this, am, w, h);

    this.addControls();
    //this.setup();
    // Useful for memory management
    this.nextIndex = 0;
    this.commands = [];
    this.animationManager.resetAll();
    // TODO:  Add any code necessary to set up your own algorithm.  Initialize data
    // structures, etc.

}

S.prototype.addControls =  function()
{
    this.controls = [];
    this.prevButton = addControlToAlgorithmBar("Button", "Prev");
  this.prevButton.onclick = this.prevone.bind(this);
  this.controls.push(this.prevButton);

    this.nextButton = addControlToAlgorithmBar("Button", "Next");
  this.nextButton.onclick = this.nextone.bind(this);
  this.controls.push(this.nextButton);
}

S.prototype.reset = function()
{
    // Reset all of your data structures to *exactly* the state they have immediately after the init
    // function is called.  This method is called whenever an "undo" is performed.  Your data
    // structures are completely cleaned, and then all of the actions *up to but not including* the
    // last action are then redone.  If you implement all of your actions through the "implementAction"
    // method below, then all of this work is done for you in the Animation "superclass"
    //maindict = {};
    // Reset the (very simple) memory manager
    this.nextIndex = 0;
}

/*
function nextone(){
    if(count < maindict.length - 1){
        count++;
        init();
        currentAlg.setup(maindict[count]);
        console.log(count);
    }
    else{
        alert("complete");
    }
}

function prevone(){
    if(count > 0){
        count--;
        init();
        console.log(count);
        currentAlg.setup(maindict[count]);
    }
    else{
        alert("beginning");
    }
}
*/


var count = -1;
console.log(maindict.length)

S.prototype.nextone = function(){
  if(count < maindict.length - 1){
    var R = document.getElementsByClassName('each_line');
    count++;
      if(count)
      {
        R[count-1].style.color = "black";
      }
      R[count].style.color = "red";
      //init();
      //currentAlg.reset();
      this.animationManager.resetAll();
      currentAlg.setup(maindict[count]);
      console.log(count);
  }
  else{
      alert("complete");
  }
}

S.prototype.prevone = function(){
    if(count > 0){
        count--;
        var R = document.getElementsByClassName('each_line');
        R[count].style.color = "red";
        R[count+1].style.color = "black";
        //init();
        //currentAlg.reset();
        this.animationManager.resetAll();
        console.log(count);
        currentAlg.setup(maindict[count]);
    }
    else{
        alert("beginning");
    }
}

S.prototype.setup = function(dict){
    this.commands = [];
    //dict = {"a": ["int", 10, [80, 310], 0], "p": ["struct Node", {"link": ["struct Node*", "?", [80, 110], 2], "data": ["int", "?", [80, 160], 4]}, [80, 60], 6], "b": ["int", 4, [260.0, 310], 7]};
    //dict = {"r": ["struct node*", "NULL", [520, 180.0], 6], "q": ["struct node*", "p", [520, 120.0], 4], "p": ["struct node*", {"data": ["int", 12, [120, 100], 0]}, [520, 60], 2]};
    console.log(dict)
    for(key in dict){
        if(dict[key][0].indexOf("*") >= 0){

            //draw a rect for a pointer
            this.cmd("CreateLabel", dict[key][3], key, dict[key][2][0] ,dict[key][2][1]);

            //if it is null then store null in it
            if(dict[key][1] == "NULL")
              this.cmd("CreateRectangle",dict[key][3]+1, dict[key][1], ARRAY_ELEM_WIDTH, ARRAY_ELEM_HEIGHT,dict[key][2][0],dict[key][2][1]+ARRAY_ELEM_HEIGHT);
            else if(dict[key][1] == "?")
              this.cmd("CreateRectangle",dict[key][3]+1, dict[key][1], ARRAY_ELEM_WIDTH, ARRAY_ELEM_HEIGHT,dict[key][2][0],dict[key][2][1]+ARRAY_ELEM_HEIGHT);
            else 
              this.cmd("CreateRectangle",dict[key][3]+1, "", ARRAY_ELEM_WIDTH, ARRAY_ELEM_HEIGHT,dict[key][2][0],dict[key][2][1]+ARRAY_ELEM_HEIGHT);
          //this.cmd("Connect", dict[key][3]+1,2);

          //draw a structure if the type is a dict
          if(typeof(dict[key][1]) == "object"){
            content = dict[key][1];
                for(key in content){
                    this.cmd("CreateRectangle", content[key][3], key, ARRAY_ELEM_WIDTH, ARRAY_ELEM_HEIGHT,content[key][2][0],content[key][2][1]);
                    if(content[key][0].indexOf("struct") >= 0 && content[key][1] != "NULL" && content[key][1] !="?")
                      this.cmd("CreateRectangle", content[key][3]+1, "", ARRAY_ELEM_WIDTH, ARRAY_ELEM_HEIGHT,content[key][2][0]+ARRAY_ELEM_WIDTH,content[key][2][1]);
                    else
                    this.cmd("CreateRectangle", content[key][3]+1, content[key][1] , ARRAY_ELEM_WIDTH, ARRAY_ELEM_HEIGHT,content[key][2][0]+ARRAY_ELEM_WIDTH,content[key][2][1]);
                }
          }

        }
        else{
            this.cmd("CreateLabel", dict[key][3], key, dict[key][2][0] , dict[key][2][1]);
            this.cmd("CreateRectangle",dict[key][3]+1, dict[key][1], ARRAY_ELEM_WIDTH, ARRAY_ELEM_HEIGHT,dict[key][2][0],dict[key][2][1]+ARRAY_ELEM_HEIGHT);
            //this.cmd("SetText",dict[key][3]+1 , "129");
        }
    }
    //this.cmd("Connect", dict["p"][3]+1, 1);


    //draw the arrow pointers
    for(key in dict){
      if(typeof(dict[key][1]) != "object" && dict[key][1] != "NULL"){
          //console.log(dict[key][3], dict[dict[key][1]][3] )
          if(dict[key][0].indexOf("struct") >= 0 && dict[key][1] != "?"){
            var x = dict[dict[key][1]][1];
            var y;
            for (i in x){
              if(x[0].indexOf("struct") < 0)
              {
                y = i;
                break;
              }
            }
            //console.log(dict[key][3]+1, x[y][3]);
            this.cmd("Connect", dict[key][3]+1, x[y][3] + 1);
          }
      }
      else if(typeof(dict[key][1]) == "object"){
        for (i in dict[key][1]){
          y = i;
          x = dict[key][1][i]; 
          if(x[0].indexOf("struct") >= 0 && x[1] != "NULL" && x[1] !="?")
          {
  
            this.cmd("Connect", x[3]+1, dict[x[1]][3] + 1);
          }

          //break;
        }
        console.log(dict[key][3]+1, dict[key][1][y][3])
        this.cmd("Connect", dict[key][3]+1, dict[key][1][y][3] + 1);
      }
    }


    //this.cmd("SetText",1,"");
    this.animationManager.StartNewAnimation(this.commands);
    this.animationManager.skipForward();
    this.animationManager.clearHistory();
}


// Called by our superclass when we get an animation started event -- need to wait for the
// event to finish before we start doing anything
S.prototype.disableUI = function(event)
{
    for (var i = 0; i < this.controls.length; i++)
    {
        this.controls[i].disabled = true;
    }
}

// Called by our superclass when we get an animation completed event -- we can
/// now interact again.
S.prototype.enableUI = function(event)
{
    for (var i = 0; i < this.controls.length; i++)
    {
        this.controls[i].disabled = false;
    }
}

var currentAlg;

function init()
{
    var animManag = initCanvas();
    currentAlg = new S(animManag, canvas.width, canvas.height);
}