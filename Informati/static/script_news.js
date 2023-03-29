
function check(elem){
    card = elem.parentNode.parentNode
    dictionary =card.querySelector("#all").getAttribute('value')
    if (elem.checked){
        console.log("CHECKED");
        var dml = true
    }
    else{
        console.log("UNCHECKED");
        var dml = false
    }

    $(function(){
            $.ajax({
                url: '/add_remove_fav',
                data: {'dic':dictionary,'dml':dml},
                type: 'POST',
                success: function(response){
                    console.log(response);
                },
                
            });
        
    });
        

}