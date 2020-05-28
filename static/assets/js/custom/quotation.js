var x=0
load_function()
select_2()

$('.add-row').click(function(){
    select_2()
    x++
    load_function()
})

function select_2(){
    $('.sow').select2()
}

function hide(){
    $('.add-row').hide()
}

function show(){
    $('.add-row').show()
}

function disable(){
    $('#id_quotationdetails_set-'+x+'-quantity').attr('readonly', true);
}

function enable(){
    $('#id_quotationdetails_set-'+x+'-quantity').attr('readonly', false);  
}

function change_scope(){
    $('#id_quotationdetails_set-'+x+'-scope_of_work').change(function(){
        var scope = $(this).val()
        if(scope==""|| scope=="---------"){
            disable()
        }
        else{
            $.ajax({
                method: 'GET',
                url:'http://127.0.0.1:8000/backoffice/project/quotation/api/'+scope,
                success:function(data){
                    var cost = data[0].materialcost+data[0].laborcost+data[0].subbid
                    $('#id_quotationdetails_set-'+x+'-cost').val(cost)
                }
            })
            enable()
        }
    })
}

function calculate(){
    var sum = 0;
    $('.tcost').each(function() {
        var value = $(this).val();
        if(!isNaN(value) && value.length != 0 && value != 0) {
            sum += parseFloat(value);
        }
        $('#total_amount').val(sum)
    })
}

function get_tcost(){
    $('#id_quotationdetails_set-'+x+'-quantity').change(function(){ 
        var scope =$('#id_quotationdetails_set-'+x+'-scope_of_work').val();
        var qty=$(this).val();
        $.ajax({
            method: 'GET',
            url:'http://127.0.0.1:8000/backoffice/project/quotation/api/'+scope,
            success:function(data){
                var cost = data[0].materialcost+data[0].laborcost+data[0].subbid
                var unit_cost = parseFloat(cost * qty)
                $('#id_quotationdetails_set-'+x+'-tcost').val(unit_cost)
                calculate()
                show()
            }
        })
    })
}

function reset(){
    $('.delete-row').click(function(){
        x--
        calculate()
        show()
    })
}

function load_function(){
    get_tcost()
    hide()
    disable()
    change_scope()
    reset()
    calculate()
}

