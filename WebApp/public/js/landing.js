var wel = $("div p"), word="The Blink";
var i=0;
// console.log(wel.text());
wel.text("");
function graphics(){
    if(i<word.length){
        if(i==0){
        wel.text("");
        }
        wel.text(wel.text()+word.charAt(i++));
        // console.log(i);
        setTimeout(graphics,300);
    }
    else{
        i=0;
        // console.log(i);
        // wel.text("        ");
        setTimeout(graphics,1000);
    }
}
graphics();