
$(document).ready(function () {

    // for toggling page and active nav
    $('.validate_number').on('keypress', function (event) {
        return (event.charCode >= 48 && event.charCode <= 57) || (event.charCode == 13)
    })

    
    $('#country_id_signup').parent().hide()
    $('#country_id_signup').on('change',function(){
        const selected_country = $('#country_id_signup option:selected').val()
        if (parseInt(selected_country) == 177)
        {
            $('#international_student').val('national')
            $('#country_id_signup').parent().hide()
        }


    })
    $('#international_student').on('change',function(){

        const check_student = $('#international_student option:selected').val()
        if (check_student != ''){
            if (check_student =='national'){
                $('#cnic').attr('required','1')
                $('#cnic').show()
                $('#country_id_signup').parent().hide()
                $('#country_id_signup').parent().hide()
                $('#country_id_signup').removeAttr('required');
            }else{
                $('#cnic').removeAttr('required')
                $('#cnic').hide()
                $('#country_id_signup').parent().show()
                $('#country_id_signup').attr('required','1')
                $('#country_id_signup').val('')            }
        }
    })



    $('#myTab').on('click', function () {
        if ($('#signup').is(":visible")) {
            $('#signup').hide()
            $('#signin').show()
        } else {
            $('#signup').show()
            $('#signin').hide()
        }
        $('#myTab li').each(function (index, element) {
            $(element).find('a').toggleClass('active', '');

        })
    })
});

