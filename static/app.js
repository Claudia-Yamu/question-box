let questions = [];

let database = [];

const container =
document.getElementById("container");


const SHOW_COUNT = 18;


let usedQuestions = [];

let activePositions = [];

let positionIndex = 0;




// =====================
// 加载问题
// =====================

fetch("/static/questions.json")

.then(response => response.json())

.then(data => {

    questions = data;

    createBackgroundQuestions();

});





// =====================
// 加载答案
// =====================

fetch("/static/answers.json")

.then(response => response.json())

.then(data => {

    database = data;

});






// =====================
// 创建背景问题
// =====================


function createBackgroundQuestions(){


for(let i=0;i<SHOW_COUNT;i++){


    setTimeout(()=>{


        createOneQuestion();


    },i*1200);


}


}







function createOneQuestion(){



let q =
getRandomQuestion();



let div =
document.createElement("div");



div.className="question";


div.innerText=q;



let position =
getBalancedPosition();




div.style.left =
position.x+"%";


div.style.top =
position.y+"%";



adjustStyle(div);



setRandomMovement(div);



container.appendChild(div);



setTimeout(()=>{


div.classList.add("show");


},300);





let stayTime =
24000 + Math.random()*6000;




setTimeout(()=>{


removeQuestion(
div,
position.index
);


},stayTime);



}








function removeQuestion(element,index){



element.classList.remove("show");

element.classList.add("hide");



setTimeout(()=>{


element.remove();



activePositions =
activePositions.filter(
item=>item!==index
);



createOneQuestion();



},2000);



}








// =====================
// 随机问题
// =====================


function getRandomQuestion(){



let q;



do{


q =
questions[
Math.floor(
Math.random()*questions.length
)
];



}

while(
usedQuestions.includes(q)
);



usedQuestions.push(q);



if(
usedQuestions.length>100
){

usedQuestions.shift();

}



return q;


}








// =====================
// 空间区域
// =====================


function getBalancedPosition(){



let positions=[



// 左上区域

{x:[5,25],y:[8,22]},


// 上左

{x:[28,42],y:[5,18]},


// 上中

{x:[45,58],y:[8,20]},


// 上右

{x:[65,80],y:[5,18]},


// 右上

{x:[82,95],y:[10,25]},


// 左侧上

{x:[5,22],y:[28,45]},


// 左侧中

{x:[8,25],y:[48,65]},


// 左侧下

{x:[5,25],y:[70,88]},


// 下左

{x:[28,42],y:[80,95]},


// 下中左

{x:[45,58],y:[75,90]},


// 下中右

{x:[60,72],y:[82,95]},


// 右下

{x:[78,95],y:[70,90]},


// 右侧下

{x:[82,95],y:[48,65]},


// 右侧中

{x:[78,95],y:[30,45]},


// 中左

{x:[25,35],y:[35,50]},


// 中右

{x:[65,75],y:[35,50]},


// 中上

{x:[40,55],y:[22,35]},


// 中下

{x:[40,55],y:[65,78]},


// 左中偏内

{x:[22,32],y:[55,70]},


// 右中偏内

{x:[68,78],y:[55,70]}



];





let index;



let attempts=0;



do{


index =
positionIndex %
positions.length;


positionIndex++;


attempts++;



}

while(

activePositions.includes(index)

&&

attempts<30

);





activePositions.push(index);



let zone =
positions[index];




return{


x:

zone.x[0]
+
Math.random()*
(zone.x[1]-zone.x[0]),



y:

zone.y[0]
+
Math.random()*
(zone.y[1]-zone.y[0]),



index:index


};



}








// =====================
// 字体
// =====================


function adjustStyle(element){



let size =
20+Math.random()*6;



element.style.fontSize =
size+"px";



element.style.setProperty(
"--opacity",
0.38+Math.random()*0.22
);



}








// =====================
// 漂浮
// =====================


function setRandomMovement(element){



let range =
100+Math.random()*100;



element.style.setProperty(

"--x1",

Math.random()*range-range/2+"px"

);



element.style.setProperty(

"--y1",

Math.random()*range-range/2+"px"

);



element.style.setProperty(

"--x2",

Math.random()*range-range/2+"px"

);



element.style.setProperty(

"--y2",

Math.random()*range-range/2+"px"

);



element.style.animationDuration =

25+Math.random()*25+"s";



}







// =====================
// 查询答案
// =====================


function searchAnswer(){


let id =

document
.getElementById("qid")
.value
.trim()
.toUpperCase();



let conversation =
database[id];



let result =
document.getElementById("result");



if(!conversation){


result.innerHTML="没有找到这个问题";

return;

}



let html="";



conversation.forEach(turn=>{


if(turn.type==="question"){


html+=`

<div class="question-text">

Q: ${turn.text}

</div>

`;

}



if(turn.type==="answer"){


html+=`

<div class="answer-text">

A: ${turn.text}

</div>

`;

}



});



result.innerHTML=html;



document
.getElementById("qid")
.value="";



}