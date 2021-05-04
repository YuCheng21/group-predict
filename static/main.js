// 設定 nav-bar 隱藏的時機
$(window).scroll(function(e) {
    // add/remove class to navbar when scrolling to hide/show
    var scroll = $(window).scrollTop();
    if (scroll >= 150) {
        $('.navbar').addClass("navbar-hide");
    } else {
        $('.navbar').removeClass("navbar-hide");
    }
});

// 設定輸入數字上下限
function inputNum(id) {
    var val = document.getElementById(id).value;
    if (parseFloat(val) > 100.0) {
        document.getElementById(id).value = "100";
    } else if (parseFloat(val) < 0.0) {
        document.getElementById(id).value = "0";
    }
}

// 關閉 modal 時自動暫停影片
$('#infoModal').on('hide.bs.modal', function () {
    $('video').each(function(){
        this.pause();
        this.currentTime = 0;
    });
})