(function($){
    'use strict';
    //menu options
    var fixed_top = $(".main-menu");
    var fixed_top_two = $(".menu-two");
    var fixed_top_four = $(".menu-four");
    var fixed_top_five = $(".menu-five");
    var fixed_top_six = $(".menu-six");
    var fixed_top_seven = $(".menu-seven");

    $(window).on('scroll', function(){
        if( $(this).scrollTop() > 100 ){  
            fixed_top.addClass("animated fadeInDown");
        }
        else{
            fixed_top.removeClass("animated fadeInDown");
        }
	  
        if( $(this).scrollTop() > 100 ){  
            fixed_top_two.addClass("menu-two-bg");
        }
        else{
            fixed_top_two.removeClass("menu-two-bg");
        }
	  
        if( $(this).scrollTop() > 100 ){  
            fixed_top_four.addClass("menu-four-bg");
        }
        else{
            fixed_top_four.removeClass("menu-four-bg");
        }
    
        if( $(this).scrollTop() > 100 ){  
            fixed_top_five.addClass("menu-five-bg");
        }
        else{
            fixed_top_five.removeClass("menu-five-bg");
        }
    
        if( $(this).scrollTop() > 100 ){  
            fixed_top_six.addClass("menu-six-bg");
        }
        else{
            fixed_top_six.removeClass("menu-six-bg");
        }
        if( $(this).scrollTop() > 100 ){  
            fixed_top_seven.addClass("menu-seven-bg");
        }
        else{
            fixed_top_seven.removeClass("menu-seven-bg");
        }
    });

    //js code for mobile menu 
    $('.navbar-toggle').on('click', function(e) {
        $('body').toggleClass('open-mobile-menu')
    });
    $('.close').on('click', function(e) {
        $('body').removeClass('open-mobile-menu')
    });

    $('.mobile-menu>ul>li>a,.mobile-menu ul.mobile-submenu>li>a').on('click', function(e) {
        var element = $(this).parent('li');
        if (element.hasClass('open')) {
            element.removeClass('open');
            element.find('li').removeClass('open');
            element.find('ul').slideUp(1500,"swing");
        }
        else {
            element.addClass('open');
            element.children('ul').slideDown(1500,"swing");
            element.siblings('li').children('ul').slideUp(1500,"swing");
            element.siblings('li').removeClass('open');
            element.siblings('li').find('li').removeClass('open');
            element.siblings('li').find('ul').slideUp(1500,"swing");
        }
    }); 

    //jQuery for page scrolling feature - requires jQuery Easing plugin
    $('a.page-scroll').on('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });


      
    $('#countdown').countdown({
        date: '10/22/2020 17:00:00',
        offset: +2,
        day: 'Day',
        days: 'Days'
    }, 
    function () {
        // alert('Done!');
    });


	//counter up
    $('.counter').each(function() {
        var $this = $(this),
        countTo = $this.attr('data-count');
        $({ countNum: $this.text()}).animate({
            countNum: countTo
        },
        {
            duration: 2000,
            easing:'linear',
            step: function() {
                $this.text(Math.floor(this.countNum));
            },
            complete: function() {
               $this.text(this.countNum);
               //alert('finished');
            }
        });  
    });


	//Product list grid view
	var list = $("#list");
	var grid = $("#grid");
	list.on('click', function(){    
	    $('.product-item-grid').animate({opacity:0},function(){
		    $('.grid').removeClass('grid-active');
		    $('.list').addClass('list-active');
		    $('.product-item-grid').attr('class', 'product-item-list shadow');
		    $('.product-item-list').stop().animate({opacity:1});
	    });
	});

	grid.on('click', function(){  
	    $('.product-item-list').animate({opacity:0},function(){
		    $('.list').removeClass('list-active');
		    $('.grid').addClass('grid-active');
		    $('.product-item-list').attr('class', 'product-item-grid shadow');
		    $('.product-item-grid').stop().animate({opacity:1});
	    });
	});



    //lightcase
    $('a[data-rel^=lightcase]').lightcase();

    //directional-hover
    $(window).load(function() {
        $('.dh-container').directionalHover();
    });


    //masonery
    jQuery(window).load(function() {	
       $('.grid').masonry({
	       // set itemSelector so .grid-sizer is not used in layout
	       itemSelector: '.grid-item',
	       // use element for option
	       columnWidth: '.grid-sizer',
	       percentPosition: true
        })
    });


    //Sponsor one
    var swiper = new Swiper('.sponsor-slider-one', {
        slidesPerView: 3,
        spaceBetween: 30,
        autoplay: 2000,
        loop: true,
        breakpoints: {
            // when window width is <= 320px
            540: {
              slidesPerView: 1
            },
            // when window width is <= 480px
            640: {
              slidesPerView: 2
            }
        }
    });

    //Sponsor two
    var swiper = new Swiper('.sponsor-slider-two', {
        slidesPerView: 4,
        spaceBetween: 15,
        autoplay: 1500,
        loop: true,
        breakpoints: {
            // when window width is <= 320px
            540: {
              slidesPerView: 1
            },
            // when window width is <= 480px
            640: {
              slidesPerView: 2
            },
            // when window width is <= 767px
            767: {
              slidesPerView: 3
            }
        }
    });

    //Sponsor Three
    var swiper = new Swiper('.sponsor-slider-three', {
        slidesPerView: 5,
        spaceBetween: 15,
        autoplay: 1000,
        loop: true,
        breakpoints: {
            // when window width is <= 320px
            540: {
              slidesPerView: 1
            },
            // when window width is <= 480px
            640: {
              slidesPerView: 2
            },
            // when window width is <= 767px
            767: {
              slidesPerView: 4
            }
        }
    });

    //Sponsor Three
    var swiper = new Swiper('.testimonial-container', {
        slidesPerView: 1,
        spaceBetween: 30,
        autoplay: 3000,
        loop: true,
    });



    // fashion homepage
    var swiper = new Swiper('.fashion-hp-container', {
        direction: 'vertical',
        slidesPerView: 1,
        spaceBetween: 0,
        mousewheel: true,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
    });



    $('.fb-plus').on('click', function(e) {
        $('.fashion-bottom-content').toggleClass('open')
    });


    // event schedule section start here
    $('.schedule-time').on('click',function (e){
        if($(this).next('.schedule-dropdown-element').css('display') != 'block'){
            $('.active1').slideUp(500).removeClass('active1');
            $('.schedule-time').removeClass('in');
            $(this).next('.schedule-dropdown-element').addClass('active1').slideDown(500);
            $(this).addClass('in');
        }else{
            $('.active1').slideUp(500).removeClass('active1');
            $(this).removeClass('in');
        }
    });


	$('.parallax-one').parallax({imageSrc: 'images/11-04-19/paralax2.png'});
    $('.parallax-two').parallax({imageSrc: 'images/11-04-19/paralax.png'});
   
   // sticky-widget
   $(document).ready(function() {
      $('section .container .sticky-widget').theiaStickySidebar();
   });

    // 1-12-2019
    // testimonial section start here
    var swiper = new Swiper('.testimonial-slider',{
        slidesPerView: 3,
        spaceBetween: 30,
        speed: 1200,
        autoplay: 3500,
        loop: true,
        breakpoints: {
            991: {
                slidesPerView: 3,
            },
            768: {
                slidesPerView: 2,
            },
            576: {
                slidesPerView: 1,
            }
        },
    });

})(jQuery);	  