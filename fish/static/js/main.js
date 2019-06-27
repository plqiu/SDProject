$(document).ready(function () {
    //第一次加载
    var data = {water_pump: 0, disinfect: 0, oxygen_supply: 0, heater: 0, temprature: 0, ph: 0};
    jQuery.getJSON('/fishhome/get_data/', function (ws) {data= ws });
    /*监听加载更多*/
    var flag = setInterval('myrefresh()', 1000);//指定30秒刷新一次
    $("#water_pump").click(function () {
        if (data['water_pump'] == 0) {
            data['water_pump'] = 1;
            set_data({"water_pump":1});
            jQuery('#water_pump1').attr('src', '../static/img/red.png');
        }
        else {
            data['water_pump'] = 0;
            set_data({"water_pump":0});
            jQuery('#water_pump1').attr('src', '../static/img/green.png');
        }
    })
    $("#disinfect").click(function () {
        if (data['disinfect'] == 0) {
            data['disinfect'] = 1;
            set_data({"disinfect":1});
            jQuery('#disinfect1').attr('src', '../static/img/red.png');
        }
        else {
            data['disinfect'] = 0;
            set_data({"disinfect":0});
            jQuery('#disinfect1').attr('src', '../static/img/green.png');
        }
    })
    $("#oxygen_supply").click(function () {
        if (data['oxygen_supply'] == 0) {
            data['oxygen_supply'] = 1;
            set_data({"oxygen_supply":1});
            jQuery('#oxygen_supply1').attr('src', '../static/img/red.png');
        }
        else {
            data['oxygen_supply'] = 0;
            set_data({"oxygen_supply":0});
            jQuery('#oxygen_supply1').attr('src', '../static/img/green.png');
        }
    })
    $("#heater").click(function () {
        if (data['heater'] == 0) {
            data['heater'] = 1;
            set_data({"heater":1});
            jQuery('#heater1').attr('src', '../static/img/red.png');
        }
        else {
            data['heater'] = 0;
            set_data({"heater":0});
            jQuery('#heater1').attr('src', '../static/img/green.png');
        }
    })
});

function set_data(datas) {
    alert(datas)
    $.ajax({
        type: "POST",
        url: "/fishhome/set_data/",
        data: datas,
        success: function (data) {
        },
        error: function () {
            alert("false");
        }
    });


}
//water_pump: 0, disinfect: 0, oxygen_supply: 0, heater: 0, temprature: 0, ph: 0
//定时刷新页面
function myrefresh() {
    jQuery.getJSON('/fishhome/get_data/', function (ws) {
        jQuery('#ph').html(ws['ph_value']);
        jQuery('#temprature').html(ws['temperature']);
    });

}
    