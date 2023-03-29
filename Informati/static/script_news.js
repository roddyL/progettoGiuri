function check(elem){
    card = elem.parentNode.parentNode
    dictionary =card.querySelector("#all").getAttribute('value')
    // console.log(dictionary);
    console.log(JSON.stringify({dictionary}))
    if (elem.checked){
        console.log("CHECKED");
        $(function(){
            $.ajax({
                url: '/add_remove_fav',
                data: JSON.stringify({dictionary}),
                type: 'POST',
                success: function(response){
                    console.log(response);
                    
                },
                
            });
        
    });
    }
    else{
        console.log("UNCHECKED");
        $(function(){
            $.ajax({
                url: '/add_remove_fav',
                data: JSON.stringify({dictionary}),
                type: 'DELETE',
                success: function(response){
                    console.log(response);
                    
                },
                
            });
        
    });
    }

    
        

}



// function check(elem){
//     card = elem.parentNode.parentNode
//     dictionary =card.querySelector("#all").getAttribute('value')
//     console.log(dictionary);
//     if (elem.checked){
//         console.log("CHECKED");
//         var dml = true
//     }
//     else{
//         console.log("UNCHECKED");
//         var dml = false
//     }

//     $(function(){
//             $.ajax({
//                 url: '/add_remove_fav',
//                 data: {'dic':dictionary,'dml':dml},
//                 type: 'POST',
//                 success: function(response){
//                     console.log(response);
                    
//                 },
                
//             });
        
//     });
        

// }