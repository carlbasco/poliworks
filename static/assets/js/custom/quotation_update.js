jQuery(function ($) {        
    $('form').bind('submit', function () {
        $(this).find('.sow').prop('disabled', false);
        $(this).find('.qty').prop('disabled', false);
    });
});

var x=0;
load_quotation();

function load_quotation(){
    $('.sow').select2()
    count();
    get_quotation_cost();
    set_cost();
    remove_btn_click();
}

function count(){
    x=0;
    $('.tcost').each(function(){
        x++;
    });
}

function get_quotation_cost(){
    for(var i=0; i<x; i++){
        populate(i)
    };
    x--;
    console.log(x)
    $(".sow").prop('disabled', 'disabled');
    $('.qty').prop('disabled', 'disabled');
    forms_disable_false();
}

function populate(i){
    var scope = $("#id_quotationdetails_set-"+i+"-scope_of_work").val();
    var quantity = $('#id_quotationdetails_set-'+i+'-quantity').val();
    $.ajax({
        method: 'GET',
        url:'http://127.0.0.1:8000/backoffice/api/scope/'+scope,
        success:function(data){
            var cost = parseFloat(data[0].materialcost+data[0].laborcost+data[0].subbid);
            var unit_cost = parseFloat(cost * quantity);
            $('#id_quotationdetails_set-'+i+'-tcost').val(unit_cost);
            calculate();
        }
    });
}

function load_function(){
    $("#id_quotationdetails_set-"+x+"-scope_of_work").select2();
    $("#id_quotationdetails_set-"+x+"-scope_of_work").val('').trigger('change')
    quantity_reanable();
    $('.add-row').hide();
    quantity_disable();
    set_cost();
    calculate();
    remove_btn_click();
}

function remove_btn_click(){
    $('.delete-row').click(function(){
        count();
        x--;
        forms_disable_false();
        calculate();
        add_btn_show();
        $('.sow').select2()
        console.log(x)
    });
}

function count(){
    x=0;
    $('.tcost').each(function(){
        x++;
    });
}

$('.add-row').click(function(){
    $("#id_quotationdetails_set-"+x+"-scope_of_work").prop('disabled', 'disabled');
    $('#id_quotationdetails_set-'+x+'-quantity').prop('disabled', 'disabled');
    x++;
    load_function();
    console.log(x)
});

function quantity_reanable(){
    var scope = $("#id_quotationdetails_set-"+x+"-scope_of_work")
    var quantity = $('#id_quotationdetails_set-'+x+'-quantity')
    scope.change(function(){
        if(scope.val() == ""){
            quantity_disable()
            reset_form_values()
            calculate()
        }
        else{
            if(quantity.val()==""){
                quantity_disable_false();
            }
            else{
                quantity_disable_false();
            }
        }
    });
}

function set_cost(){
    $('#id_quotationdetails_set-'+x+'-quantity').change(function(){
        var scope = $("#id_quotationdetails_set-"+x+"-scope_of_work").val()
        var quantity = $('#id_quotationdetails_set-'+x+'-quantity').val()
        $.ajax({
            method: 'GET',
            url:'http://127.0.0.1:8000/backoffice/api/scope/'+scope,
            success:function(data){
                var cost = parseFloat(data[0].materialcost+data[0].laborcost+data[0].subbid)
                var unit_cost = parseFloat(cost * quantity)
                $('#id_quotationdetails_set-'+x+'-tcost').val(unit_cost)
                calculate();
                add_btn_show();
            }
        });
    });
}

function forms_disable_false(){
    $("#id_quotationdetails_set-"+x+"-scope_of_work").prop('disabled', false);
    $('#id_quotationdetails_set-'+x+'-quantity').prop('disabled', false);
}

function reset_form_values(){
    $('#total_amount').val("");
    $('#id_quotationdetails_set-'+x+'-quantity').val("");
    $('#id_quotationdetails_set-'+x+'-tcost').val("");
}

function add_btn_show(){
    $('.add-row').show();
}

function quantity_disable(){
    $('#id_quotationdetails_set-'+x+'-quantity').prop('disabled', 'disabled');
}

function quantity_disable_false(){
    $('#id_quotationdetails_set-'+x+'-quantity').prop('disabled', false);
}

function calculate(){
    var sum = 0;
    $('.tcost').each(function() {
        var value = $(this).val();
        if(!isNaN(value) && value.length != 0 && value != 0) {
            sum += parseFloat(value);
        }
        $('#total_amount').val(sum)
    });
}