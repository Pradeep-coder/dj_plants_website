$(document).ready(function () {

    $('.payWithRazorpay').click(function (e) {
        e.preventDefault();

        var firstname = $("[name='firstname']").val();
        var lastname = $("[name='lastname']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if(firstname == "" || lastname == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || country == "" || pincode == ""){
            // alert("All fields are mandatory");
            // OR use alert or swal
            swal("Alert!", "All fields are mandatory", "warning");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    var options = {
                        "key": "rzp_test_CbclSwBIrE51Hm", // Enter the Key ID generated from the Dashboard
                        "amount": 1*100, //response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Recent Gardener",
                        "description": "Thank you for spreading GREEN!",
                        "image": "./static/images/favicon.png",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);
                            data = {
                                "firstname": firstname,
                                "lastname": lastname,
                                "email": email,
                                "phone": phone,
                                "address": address,
                                "city": city,
                                "state": state,
                                "country": country,
                                "pincode": pincode,
                                "payment_mode": "Paid with Razorpay",
                                "payment_id": responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                            }
                            $.ajax({
                                method: "POST",
                                url: "/placeorder",
                                data: data,
                                success: function (responsec){
                                    // alert("Congratulations!",responsec.status);
                                    swal("Congratulations!", responsec.status, "success").then((value) => {
                                        window.location.href = '/my-orders'
                                      });

                                }
                            });
                        },
                        "prefill": {
                            "name": firstname+" "+lastname,
                            "email": email,
                            "contact": phone
                        },

                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });




        }

        


    });
});