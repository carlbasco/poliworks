(function ($) {
'use strict';
    $(function () {
        $("#signupForm").validate({
            rules: {
                password: {
                    required: true,
                    minlength: 8
                },
                cpassword: {
                    required: true,
                    minlength: 8,
                    equalTo: "#id_password"
                },
                email: {
                    required: true,
                    email: true
                },
            },
            messages: {
                password: {
                    required: "Please provide a password",
                    minlength: "Your password must be at least 8 characters long"
                },
                cpassword: {
                    required: "Please provide a password",
                    minlength: "Your password must be at least 8 characters long",
                    equalTo: "Please enter the same password as above"
                },
                email: "Please enter a valid email address",
            },
            errorPlacement: function (label, element) {
                label.addClass('mt-2 text-danger');
                label.insertAfter(element);
            },
            highlight: function (element, errorClass) {
                $(element).parent().addClass('has-danger')
                $(element).addClass('form-control-danger')
            }
        });
    });
})(jQuery);