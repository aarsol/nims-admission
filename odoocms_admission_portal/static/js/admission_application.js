// before submitting check and change color of required fields
function check_form_validation(params) {
    // this function is used for checking all the requied fields are valid and filled properly
    form = $(params).parent().find('form')
    var valid_form = true
    form_inputs = $(form).find('.form-control')
    $(form_inputs).each(function (index, element) {
        if ($(element).prop('required')) {

            if ($(element).is(":hidden")) {
                $(element).removeAttr('required')
            }

            if (!(element.checkValidity()) && $(element).is(":visible")) {
                $(element).css("border-bottom", "2px solid red")
                $(element).focus()
                valid_form = false
                return false
            }
            if ($(element).get(0).tagName == 'SELECT' && $(element).is(":visible")) {
                if ($(element).find(':selected').val() == '0' || $(element).find(':selected').val() == '') {
                    $(element).css("border-bottom", "2px solid red")
                    $(element).focus()
                    valid_form = false
                    return false;
                }
            }
        }
    });
    if (valid_form == true) {
        $(form).find(':submit').click()
    }

}
function prepare_final_confirmation() {
    $('#final_confirmation_profile_pic').empty()
    $('#review_final').empty()
    $('#preference_testing').empty()
    $('#undertaking_div').empty()
    var element_no = 1
    $('.collapse_div').each(function (index, element) {
        index += 1
        element = $(element).find('.col-8').first().clone()
        if (index < $('.collapse_div').length - 1) {
            $('#final_confirmation_div').find('#review_final').append(element.html())
        }
    })
    // $('#final_confirmation_div').find('#sortable_program_list').removeAttr('id')
    // $('#final_confirmation_div').find('#preference_testing').append($('.collapse_div').find('#sortable_program_list').parent().clone())
    $('#final_confirmation_div').find('#disciplicne_collapse').parent().remove()
    $('#final_confirmation_div').find('#preference_testing').append($('.collapse_div').find('#test_center_id').parent().clone())
    $('#final_confirmation_div').find('#test_center_id').parent().find('label').removeAttr('style')
    $('#final_confirmation_profile_pic').append($('.circle_image').find('img').clone())
    $('#final_confirmation_profile_pic').find('img').css({ 'width': '250px', 'height': '250px', 'border-radius': '50%', 'border': ' 1px solid gray', })
    $('#final_confirmation_div').find('button').remove();
    $('#final_confirmation_div').find('button').remove();
    if (!($('#final_confirmation_dropdpown').parents('div').hasClass('diable_header_tab'))) {
        if (($('#apply_final_application').length)) { } else {
            $('#agreement_terms').parent().show()

            apply_application_button = `<button  id='apply_final_application' onclick="apply_application()" style='border:None' class="btn btn-primary ml-1  mt-2 mb-5 px-5">Submit Application</button>`
            $('#apply_application_button_div').append(apply_application_button)
        }
    }
    $('#final_confirmation_div').find('a').remove();
    $('#final_confirmation_div').find('#required_document').show();
    $('#final_confirmation_div').find("input[type='file']").remove();
    $('#final_confirmation_div').find('#fee_voucher_form').remove();
    $('#final_confirmation_div').find('#fee_voucher_form_suffa').remove();
    $('#final_confirmation_div').find('#is_same_address').parent().remove();
    $('#final_confirmation_div').find('#document_upload_form').siblings('div').remove();
    $('#final_confirmation_div').find('#document_upload_form').find('img').parent().addClass('col-2');
    $('#final_confirmation_div').find('#document_upload_form').find('img').parent().removeClass('col-6');
    $('#final_confirmation_div').find('#education_table thead tr th').last().remove();
    $('#final_confirmation_div').css({ 'pointer-events': 'none', })

}
// progress and header tab enable
function prepare_next_step(data) {

    $('#application_step').val(data['step_no'])
    $('#application_state').val(data['application_state'])
    $('.header_tab').each(function (index, element) {
        index += 1
        application_step = $('#application_step').val()
        application_state = $('#application_state').val()


        if (index <= application_step) {
            if (index < application_step) {
                if ($(element).hasClass('diable_header_tab')) {
                    $(element).removeClass('diable_header_tab')
                }
                if ($(element).children('a').last().children('i').hasClass('fa-angle-up')) {
                    $(element).click()
                }
            }
            if (index == application_step) {
                if ($(element).hasClass('diable_header_tab')) {
                    $(element).removeClass('diable_header_tab')
                }
                if ($(element).children('a').last().children('i').hasClass('fa-angle-down')) {
                    $(element).click()

                    // $(element).focus()
                }
                var offset = $(element).offset()
                // offset.left -= 20;
                offset.top = 400;
                // offset.top = 1-00;
                $('html, body').animate({
                    scrollTop: offset.top,
                }, 1000);
                // scrollLeft: offset.left
                return false
            }
        }
    })
    for (i = 0; i < data['step_no']; i++) {
        $('#progressbar li').eq(i).addClass("active");
    }
    $('#message_popup_text').text(data['msg'])
    $('#toast_body_alert').text(data['msg'])
    $('#toast_body_alert').css({ 'color': 'green' })
    $('#alert_show_button').click()
    $('#application_step').val(data['step_no'])
    $('#application_state').val(data['application_state'])

    // for final step
    if (!$('#final_confirmation_dropdpown').parents('div').hasClass('diable_header_tab')) {
        if ($('#application_state').val() == 'draft') {

            window.location.replace(window.location.href)

            return false
        }
        // prepare_final_confirmation()
        // apply_application_button = `<button id='apply_final_application' onclick="apply_application()" style='border:None' class="btn btn-primary ml-1  mt-2 mb-5 px-5">Submit Application</button>`
        // $('#apply_application_button_div').append(apply_application_button)
    }

    $('#page_loader').hide()
}
// delete education from table and from database
function delete_education(param) {
    edu_id = $(param).attr('value')
    data = {
        'edu_id': edu_id,
    }
    let confirmAction = confirm("Are you sure to delete?");
    if (confirmAction) {
        $.post("/delete/education/", data,
            function (data, textStatus,) {
                $(param).parents('tr').remove()

            },
        );
    }
}
// change preference from backend
function delete_preference(param) {
    $(param).parents('li').remove()
    count = 1
    $('.program_count').each(function (index, element) {
        $(element).find('.count_preference').text(count);
        if ($('#sortable_program_list').find('li').length > 0) {
            if (count = 1) {
                let preferenceTestId = $(element).attr('pretest_id')
                let preTestName = `${$(element).attr('pretest_name')}`
                if (preTestName != 'no_pretest') {
                    $('#pretest_div').show();
                    option = `<option selected='1' value='${preferenceTestId}'>${preTestName}</option>`
                    $('#pretest_div').find('select').empty()
                    $('#pretest_div').find('select').append(option)
                } else {
                    $('#pretest_div').hide();
                }
            }
        }
        count += 1
    })

    if ($('#sortable_program_list').find('li').length >= $('#preference_allowed').val()) {
        $('#view_offered_program_button').click()
        $('#view_offered_program_button').css({ 'pointer-events': 'none' })
        $('#view_offered_program_button').attr('disabled', '1');
    }
    if ($('#sortable_program_list').find('li').length < $('#preference_allowed').val()) {
        document.getElementById('view_offered_program_button').style.removeProperty('pointer-events')
        $('#view_offered_program_button').css({ 'pointer-events': '' })
        $('#view_offered_program_button').removeAttr('disabled');
    }

    if ($('#sortable_program_list').find('li').length < 1) {
        $('#pretest_div').hide();

    }

}
// change profile image from backend as well as frontend
function profileImageUpdate(input) {
    // this function is used for updating profile image 
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#profile_image_preview').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
        formData = new FormData();
        var profile_image = document.getElementById('profile_image')
        image_file = profile_image.files[0];
        formData.append('image_file', image_file)
        $.ajax({
            url: '/profile/image/update/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)
                if (data['status'] == 'noerror') {
                    $('#profile_image_checked').attr('checked', true);
                }
                $('#message_popup_text').text(data['msg'])
                $('#toast_body_alert').text(data['msg'])
                $('#toast_body_alert').css({ 'color': 'green' })
                $('#alert_show_button').click();
                // $('#message_popup').show()
            },
            error: function (response) {}
        });
    }
}
// this function is used to show document preview
function image_preview_func(input) {
    // this function is used for displaying fee voucher
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $(input).siblings('img').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}
function on_change_test_center(id) {
    var formData = new FormData();
    formData.append('id',id)
    $.ajax({
        url: "/admissiononline/testcenter/change",
        type: "POST",
        dataType: "json",
        data: formData,
        contentType: false,
        processData:false,
        success: function(data)
        {
            if (data.test_type == 'pbt' && data.schedule.length > 0)
            {
                $("#test_schedule_div").show();
                $("#pbt").empty();
                $("#cbt").empty();
                //$("#pbt").append("<b>Test Type:</b>"+" "+"Paper Based Test"+"<br/><br/><br/>"+"<b>Test Date:</b>"+ " " + data.schedule[0].date + "<br/>" + "<b>Test Time:</b>" + " " + data.schedule[0].time );
                $("#pbt").append("<b>Test Type:</b>"+" "+"Paper Based Test"+"<br/><br/>"+"Please choose: <br/><br/>")
                for(i=0; i < data.schedule.length;i++){
                    $("#pbt").append(
                        "<input type='radio' required='true'  value='"+data.schedule[i].id+"'  name='test_timing' id='time"+i+"'>" + " " + "<b>Test Date:</b>"+ " " + data.schedule[i].date + "<b>Test Time:</b>" + " " + data.schedule[i].time + "<br/><br/>"
                    );
                }
           }
           else if(data.test_type == 'cbt' && data.schedule.length > 0)
           {``
                $("#test_schedule_div").show();
                $("#cbt").empty();
                $("#pbt").empty();
                $("#cbt").append("<b>Test Type:</b>"+" "+"Computer Based Test"+"<br/><br/>"+"Please choose: <br/><br/>")
                for(i=0; i < data.schedule.length;i++){
                    $("#cbt").append(
                      "<input type='radio' required='true'  value='"+data.schedule[i].id+"' name='test_timing' id='time"+i+"'>" + " " + "<b>Test Date:</b>"+ " " + data.schedule[i].date + "<b>Test Time:</b>" + " " + data.schedule[i].time + "<br/><br/>"
                );
           }
           } else {
                $("#cbt").empty();
                $("#pbt").empty();
                $("#test_schedule_div").hide();
           }
        },
        error: function() {
            console.log('error');
        }
    });
}

function on_change_test_time(selected_disciplines){

  var formData = new FormData();
  var center = $("#test_center option:selected").val();

  formData.append('center_id',center);
 for(i=0; i < selected_disciplines.length; i++){
 debugger;
 //var time = $("input[type='radio'][name='test_timing_"+selected_disciplines[i]+"']:checked").val();
 var time = $("input[type='radio'][name='test_timing']:checked").val();
 formData.append("time_id_"+selected_disciplines[i],time)
 }


  console.log('sending');

  $.ajax({
      url: "/admissiononline/testcenter/save",
      type: "POST",
      dataType: "json",
      data: formData,
      contentType: false,
      processData:false,
      success: function(data)
      {
           $("#test_center_lock").show();
           confirm_test_center();
      },
	  error: function()
	  {
    	console.log('error');
    	}
    });
  //console.log(rate_value);
}
function confirm_test_center(){


    var formData = new FormData();
    $.ajax({
        url: "/confirm/test/center",
		type: "POST",
		dataType: "json",
		data: formData,
		beforeSend: function(){
		    $("#body-overlay-voucher").show();
		},
		contentType: false,
    	   processData:false,
		success: function(data){
		if(data.status_is != 'error'){
			$("#test_center").prop('disabled', 'disabled');
			$('input[name=test_timing]').attr("disabled",true);
			$('#test_center_lock').attr("disabled",true);
			$('#admit_card_down').show();
			}
			else{
			alert('Not Confirmed');
			}
		},
		error: function(){}
	});
}
function on_change_is_any_disability() {
    if ($('#disabled_person').find(":selected").val() == 'yes')
        {
         $("#disability_div").css("display", "block");
         $("#disabled_person_detail").attr("required", "1");

        }
    else{
        $("#disability_div").css("display", "none");
        $("#disabled_person_detail").attr("required", "0");
    }

}
function on_change_is_forces_quota() {
    if ($('#forces_quota').find(":selected").val() == 'yes')
        {
         $("#forces_quota_div").css("display", "block");
         $("#forces_quota_details").attr("required", "1");

        }
    else{
        $("#forces_quota_div").css("display", "none");
        $("#forces_quota_details").attr("required", "0");
    }

}
function on_change_is_rural_quota() {
    if ($('#rural_quota').find(":selected").val() == 'yes')
        {
         $("#rural_quota_div").css("display", "block");
         $("#rural_quota_details").attr("required", "1");

        }
    else{
        $("#rural_quota_div").css("display", "none");
        $("#rural_quota_details").attr("required", "0");
    }

}
function on_change_first_in_family() {
    if ($('#first_in_family').find(":selected").val() == 'no')
        {
         $("#first_in_family_detail_div").css("display", "block");
         $("#first_in_family_detail").attr("required", "1");

        }
    else{
        $("#first_in_family_detail_div").css("display", "none");
        $("#first_in_family_detail").attr("required", "0");
    }

}
function on_change_disease() {
    if ($('#disease_ddl').find(":selected").val() == 'yes')
        {
         $("#disease_details_div").css("display", "block");
         $("#disease_details").attr("required", "1");

        }
    else{
        $("#disease_details_div").css("display", "none");
        $("#disease_details").attr("required", "0");
    }

}
function apply_application() {

    let confirmAction = confirm("You Can Not Change Any Thing After Submit Application.");
    if (confirmAction) {
        $.get("/apply/application/",
            function (data, textStatus) {
                data = JSON.parse(data);
                if (data['status'] == 'noerror') {
                    $('#message_popup_text').text(data['msg'])
                    $('#toast_body_alert').text(data['msg'])
                    $('#toast_body_alert').css({ 'color': 'green' })
                    $('#alert_show_button').click()
                    // $('#message_popup').show()
                    $('#application_step').val(data['step_no'])
                    $('#application_state').val(data['application_state'])
                    window.location.replace(window.location.href)
                    prepare_next_step(data)
                }
            },
        );
    }

}

function prepare_program() {
    // elem = $('#program_div').find("[code='" + $(param).attr('code') + "']");
    $('#program_div').show();
    // $(elem).show();
}

function add_preference(param) {

    count = $('.program_count').length + 1

    let preferenceTestId = $(param).attr('pretest_id')
    let preTestName = `${$(param).attr('pretest_name')}`

    item = `<li id = '${$(param).attr('id')}' pretest_id=${$(param).attr('id')} pretest_name=${preTestName} class='list-group-item d-flex justify-content-between align-items-start border program_count' ><div><i class="fas fa-expand-arrows-alt mr-1"></i>${$(param).text()}</div><div ><span class='badge badge-primary badge-pill count_preference'>${count}</span> <span onclick='delete_preference(this)' class='delete_preference'>  <i class="fas fa-trash-alt ml-1"></i></span></div></ > `

    var item_id = $(param).attr('id')
    $("#sortable_program_list li").each(function (index, element) {
        if ($(element).attr('id') == item_id) {
            item_id = false;
        }
    })
    if (item_id != false) {
        $('#sortable_program_list').append(item)
        $('#view_offered_program_button').click()
        if ($('#sortable_program_list').find('li').length >= $('#preference_allowed').val()) {
            $('#view_offered_program_button').css({ 'pointer-events': 'none' })
            $('#view_offered_program_button').attr('disabled', '1');
        }
    }




    if (preTestName != 'no_pretest' && $('#sortable_program_list').find('li').length < 2) {
        $('#pretest_div').show();
        option = `<option selected='1' value='${preferenceTestId}'>${preTestName}</option>`
        $('#pretest_div').find('select').empty()
        $('#pretest_div').find('select').append(option)
    }

    if (preTestName == 'no_pretest' && $('#sortable_program_list').find('li').length < 2) {
        $('#pretest_div').hide();

    }



    // elem = $('#sortable_program_list').find('li').first()
    // let new_id = $(elem).attr('pretest_id')
    // let new_name = `${$(elem).attr('pretest_name')}`
    // if (preTestName != 'no_pretest') {
    //     $('#pretest_div').show();
    //     option = `<option selected='1' value='${new_id}'>${new_name}</option>`
    //     $('#pretest_div').find('select').empty()
    //     $('#pretest_div').find('select').append(option)
    // } else {
    //     $('#pretest_div').hide();
    // }





}
// this function is used when we add subject in education
function prepare_subject(param) {

    let selected = $(param).find('option:selected').val()
    if (selected != '') {
        $(param).parents('.subject_main_div').siblings('.subject_main_div').find('select').find(`option[value=${selected}]`).attr('disabled', '1')
    }
    var all_selected_option = []
    selected_option = $('.subject_main_div').find('select').find('option:selected')
    $(selected_option).each(function (index, element) {
        if ($(element).val() != '') {
            all_selected_option.push(parseInt($(element).val()))
        }
    })
    all_option = $('.subject_main_div').find('select option')
    $(all_option).each(function (index, element) {
        element_value = parseInt($(element).val())
        if (element_value != '') {
            if (all_selected_option.includes(element_value)) {
            } else {
                $('.subject_main_div').find('select').find(`option[value=${element_value}]`).each(function (index, el) {
                    $(el).removeAttr('disabled')
                })
            }
        }
    })

    // console.log(all_selected_option);
    // console.log($('.subject_main_div').find('select').find('option:selected').length);
    // $(param).parents('.subject_main_div').siblings('.subject_main_div').find('select').find('option:selected')
    //  all_option = $('#subject_div').find('select').find('option')
    //  console.log(all_option);
    //  all_option.each(function(index,element){
    //     option_value = $(element).val()
    //     check_option =$('#subject_div').find(`option:selected[value='${option_value}']`)
    //     if(check_option.length < 1){
    //         console.log(check_option.length);
    //     $(param).parents('.subject_main_div').siblings('.subject_main_div').find('select').find(`option[value=${selected_option}]`).removeAttr('disabled')

    //         // $('#subject_div').find(`option:selected[value='${option_value}']`).removeAttr('disabled')
    //         // $(param).parents('.subject_main_div').siblings('.subject_main_div').find('select').find(`option:selected[value='${option_value}']`).attr('disabled','0')
    //     }



    //  })
    //  selec = $.map(allSelected,function(value,elem){
    //     return [value]
    //  })
    //  console.log(selec);

    // $.map(all_selected_option,function(index,element){
    //     console.log(element);
    // })

    //     if (selected_option == ''){
    //         let allSelectedOption = []
    // // console.log(allSelectedOption);
    //         // $(param).parents('.subject_main_div').siblings('.subject_main_div').find('select option:selected').each(function(index,element){
    //         //     allSelectedOption.push($(element).val())
    //         // })

    //         // console.log($(param).parents('.subject_main_div').siblings('.subject_main_div').find('select option:selected').val());
    //     }else{
    //         $(param).parents('.subject_main_div').siblings('.subject_main_div').find('select').find(`option[value=${selected_option}]`).attr('disabled','1')
    //     }

    // $('#subject_main_div')
    value = $(param).val()
    $(param).parents('subject_main_div').attr('id', value)
}

function check_subject_marks(param) {
    const obtained_marks = $(param).parents('.subject_main_div').find("input[name='subj_marks']").val()
    const total_marks = $(param).val()

    if (obtained_marks != '' && total_marks != '') {
        if (parseInt(total_marks) < parseInt(obtained_marks)) {
            console.log('calling');
            $(param).parents('.subject_main_div').find("input[name='subj_marks']").val('')
        }
    }
}
$(":input").inputmask();

$(document).ready(function () {


    var final_step_inital_state = $('#final_confirmation_div').clone()
    if ($('#application_step').val() == $('.header_tab').length) {
        $('.header_tab').last().click()
    }
    $('#agreement_terms').parent().hide()
    $('#agreement_terms').on('change', function () {
        agreement = $('#agreement_terms').prop('checked')
        if (agreement == true) {
            $('#apply_application_button_div').show();
        } else {
            $('#apply_application_button_div').hide();

        }
    })

    $('#close_popup_message').on('click', function () {
        $('#message_popup').hide();
    })

    $('.header_tab').each(function (index, element) {
        index += 1
        application_step = $('#application_step').val()
        if (index < application_step) {
            $(element).removeClass('diable_header_tab')
        }
        if (index == application_step) {
            $(element).removeClass('diable_header_tab')
            // $(element).click()
        }
        // if(index==1){
        //     $(element).click()
        // }
        if (index > application_step) {
            return false;
        }
    })
    $('.header_tab').eq($('#application_step').val() - 1).click()

    $(function () {

        $("#date_of_birth").datepicker({
            changeMonth: true,
            changeYear: true,
            yearRange: '1970:2050',
            maxDate: new Date($('#dob_min').val()),
            minDate: new Date($('#dob_max').val()),
            // dateFormat: 'yyyy-mm-dd',    
            onSelect: function (date) {
                $("#date_of_birth").attr('value', date)
            },
        })
    });

    // validate input that only enter keypress is character
    $('.validate_char').on('keypress', function (event) {
        return (event.charCode > 64 && event.charCode < 91) || (event.charCode > 96 && event.charCode < 123) || (event.charCode == 32)
    })

    $('.validate_number').on('keypress', function (event) {
        return (event.charCode >= 48 && event.charCode <= 57) || (event.charCode == 13)
    })

    // Personal detail Form js
    $('#province2_div').hide();
    if ($('#domicile_id :selected').val() == '0') {
        $('#domicile_id').empty()
        $("#domicile_id").append(" <option value='0'+ >Select Domicile </option>");
    }
    $('#nationality').on('change', function () {
        if ($('#nationality  :selected').val() == '0') {
            $('#province_div').hide();
            $('#passport_div').hide();
            $('#cnic_div').hide();
            $('#province2_div').hide();
            $('#domicile_div').hide();

        }
        if ($('#nationality  :selected').val() == '177') {
            $('#province2_div').hide();
            $('#province_div').show();
            $('#domicile_div').show();
            $('#cnic_div').show();
            $('#passport_div').hide();

        } else {

            $('#cnic_div').hide();
            $('#passport_div').show();
            $('#domicile_div').hide();
            $('#province_div').hide();
            $('#province2_div').show();
        }
    });
    if ($('#nationality :selected').val() == '177') {
        $('#province2_div').hide();
        $('#province_div').show();
        $('#cnic_div').show();
        $('#domicile_div').show();
        $('#passport_div').hide();

    } else {
        $('#cnic_div').hide();
        $('#passport_div').show();
        $('#domicile_div').hide();
        $('#province_div').hide();
        $('#province2_div').show();
    }
    if ($('#nationality :selected').val() == '0') {
        $('#province_div').hide();
        $('#passport_div').hide();
        $('#cnic_div').hide();
        $('#province2_div').hide();
        $('#domicile_div').hide();

    }
    $('#province_id').on('change', function () {
        province_id = $("#province_id").val()
        var formData = new FormData();
        formData.append('province_id', province_id)
        $.ajax({
            url: "/province/domicile/",
            type: "POST",
            dataType: "json",
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                $("#domicile_id").empty();
                $("#domicile_id").append(" <option selected='1' value='0'+  >Select Domicile </option>");
                for (j = 0; j < data.domiciles.length; j++) {
                    $("#domicile_id").append(" <option value=" + data.domiciles[j].id + " > " + data.domiciles[j].name + "</option>");
                }
            }
        });
    })
    $('#personal_detail_form').on('submit', function (e) {
        e.preventDefault();
        if (!$('#profile_image_checked').prop('checked')) {
            $('#message_popup_text').text('Please Update Profile Image!')
            $('#toast_body_alert').text('Please Update Profile Image!')
            $('#toast_body_alert').css({ 'color': 'red' })
            $('#alert_show_button').click()
            return false;
        }
        if ($('#personal_detail_form').find('#date_of_birth').val().length < 4) {
            $('#date_of_birth').css("border-bottom", "2px solid red")
            $('#date_of_birth').focus()
            return false
        }
        date_of_birth = $('#personal_detail_form').find('#date_of_birth').val()
        var formData = new FormData();
        var form_data = $('#personal_detail_form').serializeArray();
        $.each(form_data, function (key, input) {

            formData.append(input.name, input.value);
        });
        $('#page_loader').show()
        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
        });
    })
    // end personal detail form

    // *******************************************************************************

    // Contact Detail Form 
    $("#per_domicile").empty()
    $('#per_province').on('change', function () {
        province_id = $("#per_province").val()
        var formData = new FormData();
        formData.append('province_id', province_id)
        $.ajax({
            url: "/province/domicile/",
            type: "POST",
            dataType: "json",
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                $("#per_domicile").empty();
                for (j = 0; j < data.domiciles.length; j++) {
                    $("#per_domicile").append(" <option value=" + data.domiciles[j].id + " > " + data.domiciles[j].name + "</option>");
                }
            }
        });
    })
    $('#is_same_address').on('change', function () {
        if ($('#is_same_address').prop('checked') == true) {
            $('#per_country_id').val($('#country_id').val());
            $('#per_city').val($('#city :selected').val());
            $('#per_street').val($('#street').val());
            $('#per_street2').val($('#street2').val());
            $('#per_zip').val($('#zip').val());
        } else {
            $('#per_country').val('');
            $('#per_city').val('');
            $('#per_street').val('');
            $('#per_street2').val('');
            $('#per_zip').val('');
        }
    })
    $('#contact_detail_form').on('submit', function (e) {
        e.preventDefault();
        // $('#ring1').show()
        var formData = new FormData();
        var form_data = $('#contact_detail_form').serializeArray();
        $.each(form_data, function (key, input) {
            formData.append(input.name, input.value);
        });
        $('#page_loader').show()
        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
                data = JSON.parse(response)
                alert(data['msg'])
            }
        });
    })
    $('#program_transfer_request_form').on('submit', function (e) {
        e.preventDefault();
        // $('#ring1').show()

        var formData = new FormData();
        var form_data = $('#program_transfer_request_form').serializeArray();
        $.each(form_data, function (key, input) {
            formData.append(input.name, input.value);
        });
        formData.append('current_program', $('#current_selected_program').attr('program'))
        $('#page_loader').show()
        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)

                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
                data = JSON.parse(response)
                alert(data['msg'])
            }
        });
    })
    // scholarship
    $('#scholarship_form').on('submit', function (e) {
        e.preventDefault();
        // $('#ring1').show()

        var formData = new FormData();
        var form_data = $('#scholarship_form').serializeArray();
        $.each(form_data, function (key, input) {
            formData.append(input.name, input.value);
        });
        $('#page_loader').show()

        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
                data = JSON.parse(response)
                alert(data['msg'])
            }
        });
    })
    $('#quota_form').on('submit', function (e) {
        e.preventDefault();
        // $('#ring1').show()

        var formData = new FormData();
        var form_data = $('#quota_form').serializeArray();
        $.each(form_data, function (key, input) {
            formData.append(input.name, input.value);
        });
        $('#page_loader').show()

        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
                data = JSON.parse(response)
                alert(data['msg'])
            }
        });
    })

    // ***********************************************************************************

    // Guardina Detail Form
    $('#guardian_relation').on('change', function () {
        console.log($(this).val());
        if ($(this).val() == 'mother') {
            $('#guardian_name').val($('#mother_name').val())
            $('#guardian_cnic').val($('#mother_cnic').val())
            $('#guardian_cell').val($('#mother_cell').val())
            $('#guardian_profession').val($('#mother_profession option:selected').val())
            console.log($('#mother_education option:selected').val())
            $('#guardian_education').val($('#mother_education option:selected').val())

        }
        else if ($(this).val() == 'father') {

            $('#guardian_name').val($('#father_name').val())
            $('#guardian_cnic').val($('#father_cnic').val())
            $('#guardian_cell').val($('#father_cell').val())
            $('#guardian_profession').val($('#father_profession option:selected').val())
            $('#guardian_education').val($('#father_education option:selected').val())
        }

        else {

            // $('#guardian_detail_form').trigger("reset");
            $('#guardian_name').val('')
            $('#guardian_cnic').val('')
            $('#guardian_cell').val('')
            $('#guardian_profession').val('')
            $('#guardian_education').val('')
        }

    })
    $('#guardian_detail_form').on('submit', function (e) {
        e.preventDefault();
        // $('#ring1').show()

        var formData = new FormData();
        var form_data = $('#guardian_detail_form').serializeArray();
        $.each(form_data, function (key, input) {
            formData.append(input.name, input.value);
        });
        $('#page_loader').show()

        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
                data = JSON.parse(response)
                alert(data['msg'])
            }
        });

    })


    $('#mother_status').on('change', function () {
        if ($('#mother_status').val() == 'alive') {
            $('#mother_status_div').show();
            $('#mother_status_div').find("div").show();
        } else {
            $('#mother_status_div').hide();
        }
    })
    $('#father_status').on('change', function () {
        if ($('#father_status').val() == 'alive') {
            $('#father_status_div').show();
            $('#father_status_div').find("div").show();

        } else {
            $('#father_status_div').hide();

        }
    })

    // *******************************************************************************************
    // Fee Voucher js
    function prepare_admission_fee_voucher() {
        $.get("/prepare/admission/invoice/",
            function (data, textStatus) {
                data = JSON.parse(data);
                if (data['error'] == 'unavailable') {
                    $('#message_popup_text').text('Preference Programs Seat Not Available!')
                    $('#toast_body_alert').text(data['msg'])
                    $('#toast_body_alert').css({ 'color': 'red' })
                    $('#alert_show_button').click()
                    $('#fee_voucher_form').parent().hide();
                    $('#fee_voucher_challan').hide();
                    $('#fee_button').show()

                } else {

                    $('#fee_voucher_state').val(data['fee_voucher_state'])
                    $('#father_name_voucher').text(data['father_name']);
                    $('#student_name_voucher').text(data['student_name']);
                    $('#voucher_cnic').text(data['cnic']);

                    account_payable = data['account_payable'] + ' or ' + data['account_payable2']
                    $('#account_payable').text(account_payable);
                    acount_title = data['account_title'] + ' or ' + data['account_title']
                    $('#account_title').text(acount_title);
                    account_no = data['account_no'] + ' or ' + data['account_no2']
                    $('#account_no').text(account_no);
                    if (data['is_dual_nationality']) {
                        application_fee_international_row = `<tr><th>Application Processing Fee</th><td> ${data['registration_fee_international']}<span>$</span></td></tr><tr><th>Total</th><td>${data['total_fee']}<span> $</span></td></tr>`
                        amount_in_word = data['total_fee_word_international'] + ' $'
                        $('#invoice-report').prepend(application_fee_international_row)
                        $('#amount_in_words').text(amount_in_word)
                    } else {
                        application_fee_row = `<tr><th>Application Processing Fee</th><td>${data['registration_fee']}<span>PKR</span></td></tr><tr><th>Total</th><td>${data['total_fee']}<span> PKR</span></td></tr>`
                        amount_in_word = data['total_fee_word'] + ' PKR'
                        $('#invoice-report').prepend(application_fee_row)
                        $('#amount_in_words').text(amount_in_word)
                    }
                }

            },
        );
    }
    if ($('#fee_voucher_state').val() != 'no') {
        prepare_admission_fee_voucher()
        $('#fee_button').hide()
    }
    if ($('#fee_voucher_state').val() == 'no') {
        $('#fee_voucher_form').parent().hide();
        $('#fee_voucher_challan').hide();
        $('#fee_button').show()
    }

    // nutech
    if ($('#fee_voucher_state').val() != 'no') {
        $('#fee_button').hide()
    }
    if ($('#fee_voucher_state').val() == 'no') {
        $('#fee_voucher_form').parent().hide();
        $('#fee_button').show()
    }
    $('#fee_button').on('click', function (e) {
        prepare_admission_fee_voucher()
        $('#fee_voucher_form').parent().show();
        $('#fee_voucher_challan').show();
        $('#fee_button').hide()
    });
    $('#fee_voucher_form').on('submit', function (e) {
        e.preventDefault();
        // $('#ring1').show()

        var formData = new FormData();
        formData.append('voucher_number', $('#voucher_number').val());
        formData.append('voucher_date', $('#deposit_date').val());
        formData.append('step_name', 'fee_voucher');
        formData.append('step_no', $('#step_no_voucher').val());
        var image = document.getElementById('fee_voucher_image')
        voucher_image = image.files[0];
        formData.append('voucher_image', voucher_image)
        $('#page_loader').show()
        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
            }
        });

    });
    $('#fee_voucher_form_suffa').on('submit', function (e) {
        e.preventDefault();
        // $('#ring1').show()

        var formData = new FormData();
        formData.append('voucher_number', $('#voucher_number').val());
        formData.append('voucher_date', $('#deposit_date').val());
        formData.append('step_name', 'fee_voucher');
        formData.append('step_no', $('#step_no_voucher').val());
        var image = document.getElementById('fee_voucher_image')
        voucher_image = image.files[0];
        formData.append('voucher_image', voucher_image)
        $('#page_loader').show()
        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
            }
        });

    });
    $('#fee_voucher_skip').on('click', function (e) {

        e.preventDefault();
        // $('#ring1').show()

        var formData = new FormData();
        formData.append('step_skip', 'yes');
        formData.append('step_name', 'fee_voucher');
        formData.append('step_no', $(this).siblings('input').val());
        $('#page_loader').show()

        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {
                data = JSON.parse(response)
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
            }
        });
    });

    // merit
    $.get("/get/merit/",
        function (data, status) {

            data = JSON.parse(data)
            if (data['status'] == 'noerror') {
                merit_no = data['merit_no']
                score = data['score']
                aggregate = data['aggregate']
                $('#merit_no').val(merit_no)
                $('#merit_score').val(score)
                $('#merit_aggregate').val(aggregate)
            }

        },

    );
    // testing center JS
    if ($('#test_center_skip').val() == 'yes') {
        $('#testing_center_update').text('Skip')
    }
    if ($('#test_center_skip').val() == 'no') {
        $('#testing_center_update').text('Update')

    }
    $('#test_center_id').on('change', function () {
        test_center_id = $("#test_center_id").val()
        var formData = new FormData();
        formData.append('test_center_id', test_center_id)
        $.ajax({
            url: "/test/slot/",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                data = JSON.parse(data)
                if (data['status'] == 'noerror') {
                    $("#test_center_slot").parent().show();

                    $("#test_center_slot").empty();
                    $("#test_center_slot").append(" <option selected='1' value='0'  >Select Test Center Slot </option>");
                    for (j = 0; j < data.slots_data.length; j++) {
                        $("#test_center_slot").append(" <option value=" + data.slots_data[j].id + " > " + data.slots_data[j].name + "</option>");
                    }
                    if (data.slots_data.length < 1) {

                        $("#test_center_slot").parent().hide();
                    }
                } else {
                    $("#test_center_slot").empty();
                    $("#test_center_slot").parents('div').hide();
                    $("#test_center_slot").append(" <option selected='1' disabled='1' value='0'+  >Select Test Center Slot </option>");
                }
            }
        });
    })
    $('#center_selection_form').on('submit', function (e) {
        e.preventDefault();
        // $('#ring1').show()

        // $('#ring1').show()

        var formData = new FormData();
        var form_data = $('#center_selection_form').serializeArray();
        $.each(form_data, function (key, input) {
            formData.append(input.name, input.value);
        });
        $('#page_loader').show()

        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (response) {

                data = JSON.parse(response)
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
            }
        });
    })
    // ****************************************************************8

    // document uploaed js
    $('#document_upload_form').on('submit', function (e) {
        e.preventDefault();
        // $('#ring1').show()

        var formData = new FormData();

        // formData.append('matric_file', document.getElementById('matric_file').files[0])
        // formData.append('intermediate_file', document.getElementById('intermediate_level_file').files[0])
        if (document.getElementById('cnic_front') != null) {
            formData.append('cnic_file', document.getElementById('cnic_front').files[0])
        }
        if (document.getElementById('cnic_back') != null) {
            formData.append('cnic_back_file', document.getElementById('cnic_back').files[0])
        }
        if (document.getElementById('domicile_file') != null) {
            formData.append('domicile_file', document.getElementById('domicile_file').files[0])
        }
        if (document.getElementById('pass_port') != null) {
            formData.append('passport', document.getElementById('pass_port').files[0])
        }

        formData.append('step_name', 'document')
        formData.append('step_no', $('#step_no_document').val())
        $('#page_loader').show()

        $.ajax({
            url: '/admission/application/save/',
            type: 'POST',
            contentType: false,
            processData: false,
            data: formData,
            success: function (data) {
                data = JSON.parse(data);
                prepare_next_step(data)
                // $('#page_loader').hide()

            },
            error: function (response) {
            }
        });

    })

    // **************************************************************************************************
    // preference js
    // ********************************************************************


    $('#pretest_check').on('change', function () {
        if ($('#pretest_check').prop('checked')) {
            $('#pre_test_marks').attr('requied', '1')
        } else {
            $('#pre_test_marks').removeAttr('required')
            $('#pre_test_marks').val('')

        }
    })

    if($('#pretest_div').is(":visible") && $('#pretest_check').prop('checked') ){
        pretest_name =$('#sortable_program_list').find('li').first().attr('pretest_name')
        option = `<option selected='1'>${pretest_name}</option>`
        $('#pretest').append(option)

    }

    $('#view_offered_program_button').on('click', function () {
        $('#program_div').empty()
        $('#discipline_list').empty()
        $.get("/prepare/preference/",
            function (data, status) {
                data = JSON.parse(data)
                // console.log(data);
                var preferencePreTest = data['pretest']
                if (data['status'] == 'noerror') {
                    program_offered = data['program_offered']
                    program_offered_items = ``
                    for (const program in program_offered) {
                        pretest_program = preferencePreTest[program]

                        pretest_program_id = false
                        pretest_program_name = false

                        if (typeof pretest_program == 'object') {
                            pretest_program_id = Object.keys(pretest_program)[0]
                            pretest_program_name = pretest_program[pretest_program_id]
                            program_offered_items = program_offered_items + `<li id='${program}' pretest_id='${pretest_program_id}' pretest_name='${pretest_program_name}'  onclick='add_preference(this)' class="list-group-item ">${program_offered[program]}</li>`
                        } else {
                            program_offered_items = program_offered_items + `<li id='${program}' pretest_id='${program}' pretest_name='no_pretest'  onclick='add_preference(this)' class="list-group-item ">${program_offered[program]}</li>`
                        }
                    }
                    program_offered_div = `<div  class="col-8 ml-0 mt-3">
                    <ul class="list-group">
                      <li style='color:whitesmoke;background-color:#875A7B;pointer-events:none' class="list-group-item">Add Program </li>
                      ${program_offered_items}
                    </ul>
                  </div>`
                    $('#program_div').append(program_offered_div)
                    prepare_program()


                    // for (const rec in program_offered) {
                    //     var descipline_list = `<li code='${rec}' onclick='prepare_program(this)' class="list-group-item descipline_preference">${rec}</li>`

                    //     $('#discipline_list').append(descipline_list)

                    //     descipline_progaram = program_offered[rec]
                    //     program_offered_items = ``
                    //     for (const program in descipline_progaram) {
                    //         program_offered_items = program_offered_items + `<li id='${program}' onclick='add_preference(this)' class="list-group-item ">${descipline_progaram[program]}</li>`
                    //     }

                    //     program_offered_div = `<div code='${rec}' style='display: none;' class="col-4 ml-0 mt-3">
                    //     <ul class="list-group">
                    //       <li style='color:whitesmoke;background-color:#875A7B;pointer-events:none' class="list-group-item">Add Program </li>
                    //       ${program_offered_items}
                    //     </ul>
                    //   </div>`
                    //     $('#program_div').append(program_offered_div)

                    // }
                }

            },
        );
    })
    $('#request_prog_trans_header_tab').on('click', function () {
        $('#new_selected_program').empty()
        $('#new_selected_program').append(`<option selected='1' disabled='1' value=''>Select New Program</option>`)
        $('#sortable_program_list li').each(function (index, element) {
            value = $(element).attr('id')
            text = $(element).text()
            $('#new_selected_program').append(`<option value='${value}'>${text}</option>`)
        })

    })
    if ($('#sortable_program_list').find('li').length >= $('#preference_allowed').val()) {

        $('#view_offered_program_button').css({ 'pointer-events': 'none' })
        $('#view_offered_program_button').attr('disabled', '1');
    }
    $('#discipline_list').find('li').on('click', function (e) {

        elem = $('#program_div').find("[code='" + $(this).attr('code') + "']");
        $('#program_div div').hide()
        $(elem).show();
    })
    $('#preference_update').on('click', function (e) {



        if ($('#sortable_program_list li').length < 1) {
            $('#message_popup_text').text('Please Select At Least One Preference!')
            $('#toast_body_alert').text('Select Preference!')
            $('#toast_body_alert').css({ 'color': 'red' })
            $('#alert_show_button').click()
            return false
        }

        if ($('#pretest_check').prop('checked') && $('#pre_test_marks').val() ==''){
            $('#message_popup_text').text('Please Enter Pre Test Marks!')
            $('#toast_body_alert').text('Select Marks!')
            $('#toast_body_alert').css({ 'color': 'red' })
            $('#alert_show_button').click()
            return false
        }
  


        var formData = new FormData();
        step_preference_no = $('#step_preference_no').val()
        step_preference_name = $('#step_preference_name').val()
        if($('#pretest_check').prop('checked')){
            pre_test_marks = $('#pre_test_marks').val()

        }else{
            pre_test_marks = ''
        }

        formData.append('pre_test_marks', pre_test_marks)
        formData.append('step_name', step_preference_name)
        formData.append('step_no', step_preference_no)
        $('#sortable_program_list li').each(function (index, element) {
            preference = index + 1
            program_id = $(element).attr('id');
            formData.append(preference, program_id)
        });
        $('#page_loader').show()

        $.ajax({
            url: "/admission/application/save/",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                data = JSON.parse(data);
                prepare_next_step(data)
                // $('#page_loader').hide()
            }
        })

    })

    $(function () {
        $("#sortable_program_list").sortable({
            update: function () {
                var count = 1
                $('.program_count').each(function (index, element) {
                    $(element).find('.count_preference').text(count);
                    if (count == 1) {
                        elem = $('#sortable_program_list').find('li').first()
                        let preferenceTestId = $(elem).attr('pretest_id')
                        let preTestName = `${$(elem).attr('pretest_name')}`
                        if (preTestName != 'no_pretest') {
                            $('#pretest_div').show();
                            option = `<option selected='1' value='${preferenceTestId}'>${preTestName}</option>`
                            $('#pretest_div').find('select').empty()
                            $('#pretest_div').find('select').append(option)
                        } else {
                            $('#pretest_div').hide();
                        }
                    }
                    count += 1

                })
            }

        });
    });

    // ****************************************************************************************
    // education details js
    // ******************************************************************

    function result_status_change() {
        $('#roll_number_last').parent('div').hide()
        $('#total_marks').siblings('span').text('Total Marks')
        $('#obtained_marks').siblings('span').text('Obtained Marks')
        if ($('#degree_id option:selected').text().trim() == 'Intermediate' || $('#degree_id option:selected').text().trim() == 'intermediate') {
            if ($('#result_status').val() == 'waiting') {
                $('#roll_number_last').parent('div').show()
                $('#roll_number_last').siblings('span').text('Second Year Roll No.')
                $('#total_marks').siblings('span').text('First Year Total Marks')
                $('#obtained_marks').siblings('span').text('First Year Obtained Marks')
            } else {
                $('#roll_number_last').parent('div').hide()

                $('#total_marks').siblings('span').text('Total Marks')
                $('#obtained_marks').siblings('span').text('Obtained Marks')
            }
        }
        if ($('#degree_id option:selected').text().trim() == 'DAE' || $('#degree_id option:selected').text().trim() == 'dae') {
            if ($('#result_status').val() == 'waiting') {
                $('#roll_number_last').parent('div').show()

                $('#roll_number_last').siblings('span').text('DAE Last Year Roll No.')
                $('#total_marks').siblings('span').text('Second Year Total Marks')
                $('#obtained_marks').siblings('span').text('Second Year Obtained Marks')
            } else {
                $('#roll_number_last').parent().hide()
                $('#total_marks').siblings('span').text('Total Marks')
                $('#obtained_marks').siblings('span').text('Obtained Marks')
            }
        }
    }
    $('#degree_level').on('change', function (e) {
        $("#subject_div").empty();
        $("#specialization_id").empty();
        $("#specialization_id").append("<option selected='1' value=''>Select Specializations </option>");

        if ($("#degree_level").val() == '') {
            return false
        }
        degree_level_id = $("#degree_level").val()
        var formData = new FormData();
        formData.append('degree_id', degree_level_id)
        $.ajax({
            url: "/degree/level/degree/",
            type: "POST",
            dataType: "json",
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.status == 'noerror') {
                    $("#degree_id").empty();
                    $("#degree_id").append(" <option selected='1' value='0'+  >Select Degree </option>");
                    for (j = 0; j < data.degrees.length; j++) {
                        $("#degree_id").append(" <option value=" + data.degrees[j].id + " > " + data.degrees[j].name + "</option>");
                    }
                }
            }
        });

    })
    $('#olevel_calculator_btn').hide()
    $('#alevel_calculator_btn').hide()

    $('#degree_id').on('change', function (e) {
        degree_id = $("#degree_id").val()
        degree_name = $('#degree_id option:selected').text().trim()

        if (degree_name == 'O-Level' || degree_name == 'olevel' || degree_name == 'o-level') {

            $('#specialization_id').parent().parent().hide()
            $('#result_status').parent().hide()
            $('#board').parent().parent().hide()
            $('#roll_no').parent().parent().hide()
            $('#olevel_calculator_btn').show()
            $('#alevel_calculator_btn').hide()

            $('#obtained_marks').attr('readonly', '1')
            $('#total_marks').attr('readonly', '1')

            return false
        } else if (degree_name == 'A-Level' || degree_name == 'alevel' || degree_name == 'a-level') {
            $('#specialization_id').parent().parent().hide()
            $('#result_status').parent().hide()
            $('#board').parent().parent().hide()
            $('#roll_no').parent().parent().hide()
            $('#olevel_calculator_btn').hide()
            $('#alevel_calculator_btn').show()
            $('#obtained_marks').attr('readonly', '1')
            $('#total_marks').attr('readonly', '1')
            return false
        } else {
            $('#specialization_id').parent().parent().show()
            $('#result_status').parent().show()
            $('#board').parent().parent().show()
            $('#roll_no').parent().parent().show()
            $('#olevel_calculator_btn').hide()
            $('#alevel_calculator_btn').hide()
            $('#obtained_marks').removeAttr('readonly')
            $('#total_marks').removeAttr('readonly')
        }

        var formData = new FormData();
        formData.append('degree_id', degree_id)
        $.ajax({
            url: "/degree/specializations/",
            type: "POST",
            dataType: "json",
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                result_status_change();
                if (data.status == 'noerror') {
                    $("#specialization_id").empty();
                    $("#specialization_id").append("<option selected='1' value=''>Select Specializations </option>");
                    for (j = 0; j < data.specializations.length; j++) {
                        $("#specialization_id").append("<option value=" + data.specializations[j].id + ">" + data.specializations[j].name + "</option>");
                    }
                }
            }
        });

    })
    $('#specialization_id').on('change', function (e) {
        specialization_id = $("#specialization_id option:selected   ").val()
        console.log(specialization_id);
        if (specialization_id == '') {
            $('#subject_div').hide()
            $('.subject_div').empty()
            return false
        }
        var formData = new FormData();
        formData.append('specialization_id', specialization_id)
        $.ajax({
            url: "/degree/specializations/subjects",
            type: "POST",
            dataType: "json",
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                console.log(data);
                if (data.status == 'noerror') {
                    console.log(data.specializations_subject.length > 0);
                    if (data.specializations_subject.length > 0) {
                        selection_subjects = "'<option selected='1'  value=''>Select Subject</option>'"
                        for (j = 0; j < data.specializations_subject.length; j++) {
                            if (data.specializations_subject[j].name) {
                                selection_subjects = selection_subjects + `<option value='${data.specializations_subject[j].id}'>${data.specializations_subject[j].name}</option>`
                            }
                        }
                        selection_div = `<select required='1' id='selected_subject'>${selection_subjects}</select>`
                        for (j = 0; j < 3; j++) {
                            if (j == 0) {
                                $("#subject_div").empty();
                                $("#subject_div").append('<h3>Subjects Details</h3>');
                                $("#subject_div").append('<hr/>');

                            }
                            if (data.specializations_subject[j].name) {

                                str = `<div div class='subject_main_div row' id = '${data.specializations_subject[j].id}' >
                            <div id='select_marks_div' class="col-md-2 mt-2 px-0">
                            <select onchange='prepare_subject(this)' required='1' class='form-control' name='selected_subject' id='selected_subject'>${selection_subjects}</select>
                            </div>
                            <div class="col-lg-4 mt-1">
                            <input class="form-control " onkeypress="return (event.charCode >= 48 && event.charCode <= 57) || (event.charCode == 13)" placeholder='Obtained Marks' required='1' type="text" name="subj_marks" id="${data.specializations_subject[j].name}_marks" />
                            </div>
                            <div class="col-lg-5 mt-1">
                            <input class="form-control subject_total_marks" onchange='check_subject_marks(this)' onkeypress="return (event.charCode >= 48 && event.charCode <= 57) || (event.charCode == 13)" placeholder='Total  Marks' required='1' type="text" name="subj_total_marks" id="${data.specializations_subject[j].name}_total_marks" />
                            </div>
                            </div>
                            `
                                $("#subject_div").append(str);
                                // $("#select_marks_div").append(selection_div);
                                // <input class="form-control " required='1' type="text" name="subj_total_marks" id="${data.specializations_subject[j].name}_total_marks" />
                            }
                        }
                        $("#subject_div").append("<br/><hr class='mt-2' />");
                        $('#subject_div').show()
                    }
                    else {
                        $('#subject_div').hide()
                        $('#subject_div').empty()
                        return false
                    }
                }
            }
        });

    })
    if ($('#education_table').find('tbody tr').length < 1) {
        $('#education_table').hide()
    }
    $('#roll_number_last').parent().hide()
    $('#result_status').on('change', function () {
        result_status_change();

    })
    $('#obtained_marks,#total_marks').on('change', function () {

        if ($('#obtained_marks').val() > 0) {
            if (parseInt($('#obtained_marks').val()) > parseInt($('#total_marks').val())) {
                $('#obtained_marks').val('')
                $('#percentage').val('')
            }
            else {
                var percentage = (parseInt($('#obtained_marks').val()) / parseInt($('#total_marks').val())) * 100
                $('#percentage').val(Math.round(percentage).toFixed(2))
            }
        }
    })
    $('#add_education_form').submit(function (e) {
        // e.stopPropagation();
        e.preventDefault();
        // $('#ring1').show()
        var marks_data = $('#subject_div').find('.subject_main_div');
        data = {}
        if ($('#subject_div').find('.subject_main_div').length > 1) {
            marks_data.each(function (index, element) {
                var subject_id = $(element).attr('id')
                marks = $(element).find('input')
                subject_data = {}
                $(marks).each(function (index, element) {
                    subject_data[$(element).attr('name')] = $(element).val()
                })
                data[subject_id] = JSON.stringify(subject_data)
            })
        }
        var formData = new FormData();
        //var degree_document = document.getElementById('degree_document')
        //degree_file = degree_document.files[0];
        //var filesize = ((degree_document.files[0].size / 1024) / 1024).toFixed(4);
        //console.log(filesize);

        //formData.append('degree_file', degree_file)
        formData.append('step_no', $('#step_no_edu').val())
        formData.append('step_name', $('#step_name_edu').val())
        formData.append('roll_number_last', $('#roll_number_last').val())
        formData.append('degree_level', $('#degree_level').val())
        formData.append('degree', $('#degree_id').val())
        formData.append('specialization', $('#specialization_id').val())
        formData.append('passing_year', $('#year').val())
        formData.append('total_marks', $('#total_marks').val())
        formData.append('obtained_marks', $('#obtained_marks').val())
        formData.append('percentage', $('#percentage').val())
        formData.append('roll_no', $('#roll_no').val())
        formData.append('institute', $('#institute').val())
        formData.append('board', $('#board').val())
        formData.append('result_status', $('#result_status option:selected').val())
        if ($('#subject_div').find('.subject_main_div').length > 1) {
            formData.append('subject_marks', JSON.stringify(data))
        }
        $('#page_loader').show()

        $.ajax({
            url: "/admission/application/save/",
            type: "POST",
            dataType: "json",
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                document.getElementById("add_education_form").reset();
                var education_criteria = data['education_criteria']
                $('#page_loader').hide()
                if (data['status'] == 'noerror') {
                    $('#education_table_body').empty()
                    $('#education_table').show()
                    for (j = 0; j < data.academic_data.length; j++) {
                        if ((data.academic_data[j].specialization).length < 1) {
                            data.academic_data[j].specialization = '--'
                        }
                        var row = `<tr id='${data.academic_data[j].id}'>
                        <td class='col-auto'><input type='text' value="${data.academic_data[j].degree_name}" readonly='1' id='degree_val' class='form-control-plaintext col-auto'/></td>
                        <td class='col-auto'><input type='text' value="${(data.academic_data[j].specialization)}" readonly='1' class='form-control-plaintext col-auto'/></td>
                        <td class='col-auto'><input type='text' value="${data.academic_data[j].institue}" readonly='1' class='form-control-plaintext col-auto'/></td>
                        <td class='col-auto'><input type='text' value="${data.academic_data[j].percentage}" readonly='1' class='form-control-plaintext col-auto'/>
                        <td class='col-auto'><input type='text' value="${data.academic_data[j].state}" readonly='1' class='form-control-plaintext col-auto'/></td>
                        <td class='col-auto'><a href='/file/download/${data.academic_data[j].id}/applicant.academic.detail'><i class='fas fa-download'></i></a></td>
                        <td class='col-auto'><button id='education_delete' value="${data.academic_data[j].id}" type='button' class='btn btn-outline-primary' onclick='delete_education(this)'><i style='color: #875A7B;border:None' class='fa-solid fa-trash'></i></button></td>
                        </tr>`
                        $('#education_table_body').append(row)
                    }

                    $('#addeducation').modal('toggle')


                    if ($('#education_table_body').find('tr').length > 1) {
                        if (education_criteria == 'yes') {
                            prepare_next_step(data)
                        }
                    }
                    // $('#message_popup').show()
                    // data= JSON.parse(data)
                    // alert(data['msg'])
                } else {
                    $('#addeducation').modal('toggle')
                    if ($('#education_table_body').find('tr').length > 1) {
                        if (education_criteria == 'yes') {
                            prepare_next_step(data)
                        }
                    }
                    $('#message_popup_text').css({ 'color': 'red' })
                    $('#message_popup_text').text(data['msg'])
                    $('#toast_body_alert').text(data['msg'])
                    $('#toast_body_alert').css({ 'color': 'red' })
                    $('#alert_show_button').click()
                    // $('#message_popup').show()
                }
            }
        })
    });
    $('.subject_total_marks').on('keyup', function () {
        console.log('calling.....');
    })
    $('#calculate_olevel').on('submit', function (e) {
        e.preventDefault()
        var subject_marks = 0
        $('#calculate_olevel').find('select option:selected').each(function (index, element) {
            subject_marks += parseInt($(element).val())
        })
        total_marks = $('#calculate_olevel').find('select').length * 100
        obtained_marks = subject_marks
        percentage = ((obtained_marks / total_marks) * 100).toFixed(1)
        $('#addeducation').find('#total_marks').val(total_marks)
        $('#addeducation').find('#obtained_marks').val(obtained_marks)
        $('#addeducation').find('#percentage').val(percentage)
        $('#addeducation').find('#result_status').val('complete')
        $('#olevel_calculator').modal('toggle')
        document.getElementById("calculate_olevel").reset();
        return false

    })
    $('#calculate_alevel').on('submit', function (e) {
        e.preventDefault()
        var subject_marks = 0

        $('#calculate_alevel').find('select option:selected').each(function (index, element) {
            subject_marks += parseInt($(element).val())
        })
        total_marks = $('#calculate_alevel').find('select').length * 100
        obtained_marks = subject_marks
        percentage = ((obtained_marks / total_marks) * 100).toFixed(1)
        $('#addeducation').find('#total_marks').val(total_marks)
        $('#addeducation').find('#obtained_marks').val(obtained_marks)
        $('#addeducation').find('#percentage').val(percentage)
        $('#addeducation').find('#result_status').val('complete')
        $('#alevel_calculator').modal('toggle')
        document.getElementById("calculate_alevel").reset();
        return false
    })





    prepare_final_confirmation();
    $('.form-control').on('change', function () {
        $(this).css("border-bottom", "2px solid #875A7B")
    })
    $('.collapse_div').each(function (index, element) {
        $(element).slideToggle('fast');
    });
    listItems = $('#progressbar li')
    // change the floating label of no required fields as those fields are not changed by default css
    $('#date_of_birth').on('change', function (e) {
        $('#date_of_birth').siblings().css({
            'top': '48px',
            'bottom': '-10px',
            'left': '18px',
            'font-size': '11px',
            'opacity': '0.7'
        })
    })
    $('#date_of_birth').siblings().css({
        'top': '48px',
        'bottom': '-10px',
        'left': '18px',
        'font-size': '11px',
        'opacity': '0.7'
    })
    $('select').siblings('label').css({
        'top': '48px',
        'bottom': '-10px',
        'left': '18px',
        'font-size': '11px',
        'opacity': '0.7'
    })
    // floating label change css that is not required as its not handled by css
    $('.floating-label-norequired').siblings().each(function (index, el) {
        if ($(el).val().length > 0) {
            $(el).siblings('.floating-label-norequired').css({
                'top': '48px',
                'bottom': '-10px',
                'left': '18px',
                'font-size': '11px',
                'opacity': '0.7'
            })
        }
    })

    $('.floating-label-norequired').siblings('input').on('change', function () {
        var value = $(this).val();
        if (value.length > 0) {
            $(this).siblings('.floating-label-norequired').css({
                'top': '48px',
                'bottom': '-10px',
                'left': '18px',
                'font-size': '11px',
                'opacity': '0.7'
            })
        }
        if (value.length < 1) {
            $(this).siblings('.floating-label-norequired').css({
                'position': 'absolute',
                'left': '25px',
                'top': '15px',
                'font-family': 'Verdana, Arial, Helvetica, sans-serif',
                'opacity': '0.2',
                'font-size': '13px',
                'transition': '0.2s ease all',
                'font-weight': '400',
                'pointer-events': 'none',
            })
        }
    });

    $('.form-control').each(function (index) {
        if ($(this).prop('required')) {
            $(this).css('border-bottom ,2px solid #875A7B')
        }
    })
    $('#page_loader').hide()

});
