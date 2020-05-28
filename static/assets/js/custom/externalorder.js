var x=0
var unitprice
var qty
var totalprice

unitprice_change()
quantity_change()
click_delete()
calculate_total()


$('.add-row').click(function(){
    x++
    unitprice_change()
    quantity_change()
    click_delete()
})

function click_delete(){
    $('.delete-row').click(function(){
        x--
        unitprice_change()
        quantity_change()
        calculate_total()
    })
}

function unitprice_change(){
    $('#id_externalorderdetails-'+x+'-unitprice').keyup(function(){
        unitprice = $(this).val()
        qty = $('#id_externalorderdetails-'+x+'-quantity').val()
        if(qty == ""){
            $('#id_externalorderdetails-'+x+'-quantity').val(1)
            unitprice_change();
        }
        else{
            multiply();
        }
    })
}

function quantity_change(){
    $('#id_externalorderdetails-'+x+'-quantity').keyup(function(){
        qty = $(this).val()
        unitprice = $('#id_externalorderdetails-'+x+'-unitprice').val()
        if(unitprice != ""){
            multiply()
        }
    })
}

function multiply(){
    totalprice = qty*unitprice
    $('#id_externalorderdetails-'+x+'-totalprice').val(totalprice)
    calculate_total()
}

function calculate_total(){
    var sum = 0;
    $('.total_price').each(function() {
        var value = $(this).val();
        if(!isNaN(value) && value.length != 0 && value != 0) {
            sum += parseFloat(value);
        }
        $('#total_amount').val(sum)
    })
}

