/* Template: Evolo - StartUp HTML Landing Page Template
   Author: Inovatik
   Created: June 2019
   Description: Custom JS file
*/

$('.selectLoc').on('submit', function(event) {

    $.get("/endParkingReve", function(data){
        console.log(data.mySlot)
      });


    $.get("/myParkingSpace", function(data){
        console.log(data.mySlot)
        $('#urSlot').empty();
            num=`
            <h3>Your Parking Slot is </h3>
            <h3>Slot `+data.mySlot+`</h3>
            <button onclick="cancelReservation(`+data.mySlot+`)"  class="btn btn-danger btn-loc">Cancel Reservation</button>

            `;
            $('#urSlot').append(num)

      });
      
    var numberSlots=0;
    $.ajax({
        data : {
            area : $('#area').val(),
        },
        type : 'POST',
        url : '/getParkingSpaces',
        success:function(data) {
   
            $('#parkingslot').empty()
           
            html=` <div style="margin-top:100px" class="row">
            `;
          
            for(var i =1 ; i <= 10 ;i++){

                if(data['slots'].includes(i)){
                    html +=  `

                    <div class="col-lg-3 col-md-6 col-sm-6 col-12 mt-2 sidenav">
                    <div class="slot1">
                
                      <h6>Slot `+i+`</h6>
                      <img class="img-fluid" style="width: 80px;height: 80px;" src="static/img/nop.jpg" alt="alternative">
                    </div>
                    </div>
                  `
                }

                else{
                    html +=  `
                    <div class="col-lg-3 col-md-6 col-sm-6 col-12 mt-2 sidenav">
                    <div class="slot1">
                
                    <h6>Slot `+i+`</h6>
                
                    <button style="background-color:white;border:0" type="button" id="place" value=`+i+` onclick="getvalue(this.value)"  data-toggle="modal" data-target="#myModal"><img class="img-fluid" style="width: 80px;height: 80px;" src="static/img/p.png" alt="alternative"></button>

                    </div>
                    </div>
                `
                }

                if(i%4==0){

                    html +=  `
                    <div class="col-lg-12 col-md-12 col-sm-12 col-12">
                    <hr style=" height: 1px;
                    background-image: linear-gradient(90deg, #000, #000 75%, transparent 75%, transparent 100%);
                    background-size: 20px 1px;
                    border: none;" class="border02">

                    </div>
`
                }

            }

         html+=`
         </div>


         </div>
         <br>
         <br>
         `

$('#parkingslot').append(html)
       
            
            
         },
    })
    .done(function(data) {

        if (data.error) {
         console.log("asdas")
        }
        else {
        }

    });

    event.preventDefault();
});




function cancelReservation(){

    $.ajax({
        data : {
            area : $('#area').val(),
        },
        type : 'POST',
        url : '/Cancel_Reservation',
        success:function(data) {
        console.log("deleted")
         $('#urSlot').empty();
         
        }
    })
}

function getvalue(val){

    document.getElementById("registerSpace").value=val;
}


$(document).on('click', '.number-spinner button', function () {    
	var btn = $(this),
		oldValue = btn.closest('.number-spinner').find('input').val().trim(),
		newVal = 0;
	
	if (btn.attr('data-dir') == 'up') {
        if(oldValue>=20)
        {
            newVal=20;
        }
        else{
            newVal = parseInt(oldValue) + 1;
        }
	} else {
		if (oldValue > 1) {
			newVal = parseInt(oldValue) - 1;
		} else {
			newVal = 1;
		}
	}
	btn.closest('.number-spinner').find('input').val(newVal);
});
// let map;

// function initMap() {
//   map = new google.maps.Map(document.getElementById("map"), {
//     center: { lat: -34.397, lng: 150.644 },
//     zoom: 8,
//   });
// }



$("#registerSpace").click(function(){
    console.log(    document.getElementById("hours").value
    )
    $.ajax({
        data : {
            space : document.getElementById("registerSpace").value,
            hours : document.getElementById("hours").value,
        },
        type : 'POST',
        url : '/RegisterParkingSpaces',
        success:function(data) {
          console.log("added")   
        }
    })
    .done(function(data) {

        if (data.error) {
         console.log("asdas")
        }
        else {
            console.log(data)
        }

    });
    
  });
////////////////////////////Stripe//////////////////////////////////

let stripe = Stripe(

    'pk_test_51J6DmPGbd5hvE4QivXGtK7Ugbvs0dxhSS4uFd2yk5NjYz0VTOsc2v036NRqI9TCIVlHvALcx3owTOxW8221voZm000h0os29Zk'
    )

$('#checkOut').on('click', function(event) {

    $.ajax({
        data : {
            area : "aa"
        },
        type : 'POST',
        url : '/getSessionIDMonth',
        success:function(data) {
            console.log(data.sessionID.sessionId);
                      // Call Stripe.js method to redirect to the new Checkout page
                      stripe
                        .redirectToCheckout({
                          sessionId: data.sessionID.sessionId
                        })
                        .then(handleResult);
         },
    })
    .done(function(data) {

        if (data.error) {
         console.log("error")
        }
        else {
        }

    });

    event.preventDefault();
});

  ////////////////////////////////////////////////////
(function($) {
    "use strict"; 
	
	/* Preloader */
	$(window).on('load', function() {
		var preloaderFadeOutTime = 500;
		function hidePreloader() {
			var preloader = $('.spinner-wrapper');
			setTimeout(function() {
				preloader.fadeOut(preloaderFadeOutTime);
			}, 500);
		}
		hidePreloader();
	});

	
	/* Navbar Scripts */
	// jQuery to collapse the navbar on scroll
    $(window).on('scroll load', function() {
		if ($(".navbar").offset().top > 60) {
			$(".fixed-top").addClass("top-nav-collapse");
		} else {
			$(".fixed-top").removeClass("top-nav-collapse");
		}
    });

	// jQuery for page scrolling feature - requires jQuery Easing plugin
	$(function() {
		$(document).on('click', 'a.page-scroll', function(event) {
			var $anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: $($anchor.attr('href')).offset().top
			}, 600, 'easeInOutExpo');
			event.preventDefault();
		});
	});

    // closes the responsive menu on menu item click
    $(".navbar-nav li a").on("click", function(event) {
    if (!$(this).parent().hasClass('dropdown'))
        $(".navbar-collapse").collapse('hide');
    });


    /* Image Slider - Swiper */
    var imageSlider = new Swiper('.image-slider', {
        autoplay: {
            delay: 2000,
            disableOnInteraction: false
		},
        loop: true,
        spaceBetween: 30,
        slidesPerView: 5,
		breakpoints: {
            // when window is <= 580px
            580: {
                slidesPerView: 1,
                spaceBetween: 10
            },
            // when window is <= 768px
            768: {
                slidesPerView: 2,
                spaceBetween: 20
            },
            // when window is <= 992px
            992: {
                slidesPerView: 3,
                spaceBetween: 20
            },
            // when window is <= 1200px
            1200: {
                slidesPerView: 4,
                spaceBetween: 20
            },

        }
    });


    /* Card Slider - Swiper */
	var cardSlider = new Swiper('.card-slider', {
		autoplay: {
            delay: 4000,
            disableOnInteraction: false
		},
        loop: true,
        navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev'
		}
    });
    

    /* Video Lightbox - Magnific Popup */
    $('.popup-youtube, .popup-vimeo').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false,
        iframe: {
            patterns: {
                youtube: {
                    index: 'youtube.com/', 
                    id: function(url) {        
                        var m = url.match(/[\\?\\&]v=([^\\?\\&]+)/);
                        if ( !m || !m[1] ) return null;
                        return m[1];
                    },
                    src: 'https://www.youtube.com/embed/%id%?autoplay=1'
                },
                vimeo: {
                    index: 'vimeo.com/', 
                    id: function(url) {        
                        var m = url.match(/(https?:\/\/)?(www.)?(player.)?vimeo.com\/([a-z]*\/)*([0-9]{6,11})[?]?.*/);
                        if ( !m || !m[5] ) return null;
                        return m[5];
                    },
                    src: 'https://player.vimeo.com/video/%id%?autoplay=1'
                }
            }
        }
    });


    /* Lightbox - Magnific Popup */
	$('.popup-with-move-anim').magnificPopup({
		type: 'inline',
		fixedContentPos: false, /* keep it false to avoid html tag shift with margin-right: 17px */
		fixedBgPos: true,
		overflowY: 'auto',
		closeBtnInside: true,
		preloader: false,
		midClick: true,
		removalDelay: 300,
		mainClass: 'my-mfp-slide-bottom'
	});
    
    
    /* Move Form Fields Label When User Types */
    // for input and textarea fields
    $("input, textarea").keyup(function(){
		if ($(this).val() != '') {
			$(this).addClass('notEmpty');
		} else {
			$(this).removeClass('notEmpty');
		}
    });


    /* Request Form */
    $("#requestForm").validator().on("submit", function(event) {
    	if (event.isDefaultPrevented()) {
            // handle the invalid form...
            rformError();
            rsubmitMSG(false, "Please fill all fields!");
        } else {
            // everything looks good!
            event.preventDefault();
            rsubmitForm();
        }
    });

    function rsubmitForm() {
        // initiate variables with form content
		var name = $("#rname").val();
		var email = $("#remail").val();
		var phone = $("#rphone").val();
        var select = $("#rselect").val();
        var terms = $("#rterms").val();
        
        $.ajax({
            type: "POST",
            url: "php/requestform-process.php",
            data: "name=" + name + "&email=" + email + "&phone=" + phone + "&select=" + select + "&terms=" + terms, 
            success: function(text) {
                if (text == "success") {
                    rformSuccess();
                } else {
                    rformError();
                    rsubmitMSG(false, text);
                }
            }
        });
	}

    function rformSuccess() {
        $("#requestForm")[0].reset();
        rsubmitMSG(true, "Request Submitted!");
        $("input").removeClass('notEmpty'); // resets the field label after submission
    }

    function rformError() {
        $("#requestForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
	}

    function rsubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#rmsgSubmit").removeClass().addClass(msgClasses).text(msg);
    }
    

    /* Contact Form */
    $("#contactForm").validator().on("submit", function(event) {
    	if (event.isDefaultPrevented()) {
            // handle the invalid form...
            cformError();
            csubmitMSG(false, "Please fill all fields!");
        } else {
            // everything looks good!
            event.preventDefault();
            csubmitForm();
        }
    });

    function csubmitForm() {
        // initiate variables with form content
		var name = $("#cname").val();
		var email = $("#cemail").val();
        var message = $("#cmessage").val();
        var terms = $("#cterms").val();
        $.ajax({
            type: "POST",
            url: "php/contactform-process.php",
            data: "name=" + name + "&email=" + email + "&message=" + message + "&terms=" + terms, 
            success: function(text) {
                if (text == "success") {
                    cformSuccess();
                } else {
                    cformError();
                    csubmitMSG(false, text);
                }
            }
        });
	}

    function cformSuccess() {
        $("#contactForm")[0].reset();
        csubmitMSG(true, "Message Submitted!");
        $("input").removeClass('notEmpty'); // resets the field label after submission
        $("textarea").removeClass('notEmpty'); // resets the field label after submission
    }

    function cformError() {
        $("#contactForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
	}

    function csubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#cmsgSubmit").removeClass().addClass(msgClasses).text(msg);
    }


    /* Privacy Form */
    $("#privacyForm").validator().on("submit", function(event) {
    	if (event.isDefaultPrevented()) {
            // handle the invalid form...
            pformError();
            psubmitMSG(false, "Please fill all fields!");
        } else {
            // everything looks good!
            event.preventDefault();
            psubmitForm();
        }
    });

    function psubmitForm() {
        // initiate variables with form content
		var name = $("#pname").val();
		var email = $("#pemail").val();
        var select = $("#pselect").val();
        var terms = $("#pterms").val();
        
        $.ajax({
            type: "POST",
            url: "php/privacyform-process.php",
            data: "name=" + name + "&email=" + email + "&select=" + select + "&terms=" + terms, 
            success: function(text) {
                if (text == "success") {
                    pformSuccess();
                } else {
                    pformError();
                    psubmitMSG(false, text);
                }
            }
        });
	}

    function pformSuccess() {
        $("#privacyForm")[0].reset();
        psubmitMSG(true, "Request Submitted!");
        $("input").removeClass('notEmpty'); // resets the field label after submission
    }

    function pformError() {
        $("#privacyForm").removeClass().addClass('shake animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass();
        });
	}

    function psubmitMSG(valid, msg) {
        if (valid) {
            var msgClasses = "h3 text-center tada animated";
        } else {
            var msgClasses = "h3 text-center";
        }
        $("#pmsgSubmit").removeClass().addClass(msgClasses).text(msg);
    }
    

    /* Back To Top Button */
    // create the back to top button
    $('body').prepend('<a href="body" class="back-to-top page-scroll">Back to Top</a>');
    var amountScrolled = 700;
    $(window).scroll(function() {
        if ($(window).scrollTop() > amountScrolled) {
            $('a.back-to-top').fadeIn('500');
        } else {
            $('a.back-to-top').fadeOut('500');
        }
    });


	/* Removes Long Focus On Buttons */
	$(".button, a, button").mouseup(function() {
		$(this).blur();
	});

})(jQuery);