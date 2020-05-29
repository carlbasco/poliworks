$('#id_province').select2();
$('#id_city').select2();

$('#id_province').change(function(){
var select = $('#id_city');
var province = $(this).val()
    if(province =="" || province=="---------"){
        select.empty();
        $('#div_id_city').hide();
    }
    else{
        $.ajax({
        method: 'GET',
        url:'http://127.0.0.1:8000/api/city/'+province,
            success:function(data){
                $('#div_id_city').show();
                select.empty();
                select.append("<option value=''>---Select City---</option>");
                for (var j = 0; j < data.length; j++){
                        console.log(data[j].name + "--" + data[j].id);
                        $("#id_city").append("<option value='" +data[j].id+ "'>" +data[j].name+ "     </option>");
                }
                $('#id_city').select2();
            }
        })
    }
});