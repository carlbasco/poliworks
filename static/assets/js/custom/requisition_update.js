jQuery(function ($) {        
    $('form').bind('submit', function () {
        $(this).find('.art').prop('disabled', false);
        enable_fields();
    });
    
    disable_fields();
    var x = 0;
    select_2();
    get_data();
    reset();
});

$('.add-row').click(function(){
    disable_field_article();
    select_2();
    x++;
    $('#id_requisitiondetail-'+x+'-articles').val('').trigger('change');
    hide_add_btn();
    change_article();
    reset();
})

function select_2(){
    $('.art').select2();
}

function hide_add_btn(){
    $('.add-row').hide();
}

function show_add_btn(){
    $('.add-row').show();
}

function disable_fields(){
    $('#id_projectsite').prop('disabled', 'disabled');
    $('#id_date').prop('disabled', 'disabled');
    $('#id_admin').prop('disabled', 'disabled');
    $('#id_whm').prop('disabled', 'disabled');
}

function enable_fields(){
    $('#id_projectsite').prop('disabled', false);
    $('#id_date').prop('disabled', false);
    $('#id_admin').prop('disabled', false);
    $('#id_whm').prop('disabled', false);
}

function disable_field_article(){
    $('#id_requisitiondetail-'+x+'-articles').prop('disabled', 'disabled');
}

function enable_field_article(){
    $('#id_requisitiondetail-'+x+'-articles').prop('disabled', false);
}

function get_data(){
    count();
    for(var i=0; i<x; i++){
        populate(i)
    };
    x--;
    $(".art").prop('disabled', 'disabled');
}

function count(){
    x=0;
    $('.unit').each(function(){
        x++;
    });
}

function populate(i){
    var article =  $('#id_requisitiondetail-'+i+'-articles').val()
    $.ajax({
        method: 'GET',
        url:'http://127.0.0.1:8000/backoffice/api/materials/'+article,
        success:function(data){
            var unit = data[0].unit
            $('#id_requisitiondetail-'+i+'-unit').val(unit);
        }
    });
}

function change_article(){
    $('#id_requisitiondetail-'+x+'-articles').change(function(){
        var article = $(this).val()
        if(article != ""){
            $.ajax({
                method: 'GET',
                url:'http://127.0.0.1:8000/backoffice/api/materials/'+article,
                success:function(data){
                    var unit = data[0].unit
                    $('#id_requisitiondetail-'+x+'-unit').val(unit);
                    show_add_btn();
                }
            });
        }
        else{
            hide_add_btn();
        }
    });
}

function reset(){
    $('.delete-row').click(function(){
        x--
        select_2();
        show_add_btn();
        enable_field_article();
        change_article();
    });
}