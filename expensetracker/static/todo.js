//for adding line-through  
$("tr").on('click','td',function(){
    $(this).parent().toggleClass("listtext");
});


//when span(delete icon) is pressed delete the list
$('ul').on('click','span',function(e){
    $(this).parent().fadeOut(500,function(){
        $(this).remove();
    });
    e.stopPropagation();
});


//for controlling create new todo
$('.fa-plus').on('click', function(){
    $('.floating').toggleClass("inputview");
    $('input').toggleClass("inputview");
    $(this).toggleClass("fa-times");
    $(this).toggleClass("fa-plus");
    
    });

//fadout warning sign
setTimeout(function(){
    $(".fademessage").fadeOut(400,function(){
        $(this).remove();
    });
},3000)


//sign coloring manager
// var data = $("td.text-right").text() //storing all sign to data
// for(var i =0;i<data.length;i++){
//     if(data[i]=='+'){
//         data
//     }
// }

$("td.text-right").each(function (index,element){
    if($(this).text() == '+')
    {
        $(this).text("");
        $(this).addClass("plussign");
    }
    if($(this).text() == '-'){
        $(this).text("");
        $(this).addClass("minussign");
    }
});
