function check(elem){
    card = elem.parentNode.parentNode
    dictionary =card.querySelector("#all").getAttribute('value')
    console.log(JSON.stringify({dictionary}))
    if (elem.checked){
        console.log("CHECKED");
        $(function(){
            $.ajax({
                url: '/add_remove_fav',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(dictionary),
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
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(dictionary),
                type: 'DELETE',
                success: function(response){
                    console.log(response);
                    
                },
            });
    });
    }
}