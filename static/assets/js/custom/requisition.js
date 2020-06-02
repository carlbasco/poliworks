var x = 0;
select_2();
hide();
change_article();
reset();

$('.add-row').click(function(){
    select_2();
    x++
    hide();
    change_article();
    reset();
})

function select_2(){
    $('.art').select2();
}

function hide(){
    $('.add-row').hide();
}

function show(){
    $('.add-row').show();
}

function change_article(){
    $('#id_requisitiondetail-'+x+'-articles').change(function(){
        var article = $(this).val()
        $.ajax({
            method: 'GET',
            url:'http://127.0.0.1:8000/backoffice/api/materials/'+article,
            success:function(data){
                var unit = data[0].unit
                $('#id_requisitiondetail-'+x+'-unit').val(unit);
                show();
            }
        });
    });
}

function reset(){
    $('.delete-row').click(function(){
        x--
        select_2()
        hide()
        change_article()
    })
}