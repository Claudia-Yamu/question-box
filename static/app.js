let questions = [];

let database = [];

const container =
document.getElementById("container");


const SHOW_COUNT = 12;


let usedQuestions = [];

let scrollAnimation = null;


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
// 背景问题
// =====================


function createBackgroundQuestions(){


for(let i=0;i<SHOW_COUNT;i++){


    setTimeout(()=>{


        createOneQuestion();


    },i*2500);


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
getSafePosition();



div.style.left =
position.x+"%";

div.style.top =
position.y+"%";



adjustStyle(div);

setRandomMovement(div);



container.appendChild(div);



setTimeout(()=>{

div.classList.add("show");

},500);





let stayTime =
30000 + Math.random()*10000;



setTimeout(()=>{

removeQuestion(div);

},stayTime);



}



function removeQuestion(element){


element.classList.remove("show");

element.classList.add("hide");



setTimeout(()=>{


element.remove();


createOneQuestion();


},5000);


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
usedQuestions.length>60
){

usedQuestions.shift();

}



return q;


}





// =====================
// 位置
// =====================


function getSafePosition(){


let zones=[

{x:[5,25],y:[8,25]},

{x:[38,62],y:[5,20]},

{x:[72,92],y:[10,30]},

{x:[5,25],y:[35,55]},

{x:[75,95],y:[38,60]},

{x:[5,28],y:[70,88]},

{x:[38,62],y:[75,92]},

{x:[72,95],y:[70,90]}

];



let zone =
zones[
Math.floor(
Math.random()*zones.length
)
];



return {


x:
zone.x[0]+
Math.random()*
(zone.x[1]-zone.x[0]),



y:
zone.y[0]+
Math.random()*
(zone.y[1]-zone.y[0])


};


}





// =====================
// 字体透明度
// =====================


function adjustStyle(element){


let size =
20+Math.random()*6;


element.style.fontSize =
size+"px";



element.style.setProperty(

"--opacity",

0.25+Math.random()*0.2

);


}




// =====================
// 漂浮
// =====================


function setRandomMovement(element){


let range =
40+Math.random()*40;



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

45+Math.random()*35+"s";


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


html +=
`

<div class="question-text">

Q: ${turn.text}

</div>

`;


}



if(turn.type==="answer"){


html +=
`

<div class="answer-text">

A: ${turn.text}

</div>

`;


}



});





result.innerHTML=

`

<div class="scroll-wrapper">


<div class="scroll-content">

${html}

</div>



<div class="scroll-content clone">

${html}

</div>


</div>

`;



startAnswerScroll();



document
.getElementById("qid")
.value="";


}






// =====================
// 循环滚动
// =====================


function startAnswerScroll(){


let result =
document.getElementById("result");


let wrapper =
result.querySelector(
".scroll-wrapper"
);



if(!wrapper){

return;

}





if(scrollAnimation){

clearInterval(scrollAnimation);

scrollAnimation=null;

}





let position=0;



setTimeout(()=>{


scrollAnimation=setInterval(()=>{


position+=0.15;



wrapper.style.transform=

`translateY(-${position}px)`;





let content =
wrapper.querySelector(
".scroll-content"
);



if(
position>=content.offsetHeight
){


position=0;


wrapper.style.transform=
"translateY(0)";


}



},30);



},2000);



}
