$(document).ready(function() {
    //第一次加载
    var counter = 0; /*计数器*/
    var pageStart = 0; /*offset*/
    var pageSize = 10; /*size*/

    var counterAll = 0;
    var pageStartAll = 0;
    var pageSizeAll = 10;

    var counterError = 0;
    var pageStartError = 0;
    var pageSizeError = 10;

    /*首次加载*/
    getData(pageStart,pageSize);
    
   
    
    /*监听加载更多*/
    $('.load-more').click(function(){
       
        counter ++;
        pageStart = counter * pageSize;

        getData(pageStart,pageSize);
    });
    
    /*var alarm_alert = $('.alarm').val();

    if(alarm_alert == true){
        alert("有新错误啦！");
        $('.alarm').attr("value","false");
    }*/
   var flag = setInterval('myrefresh()',9000);//指定30秒刷新一次
//时间控件

    $( "#datepicker_start" ).datetimepicker({
        dateFormat: "yy-mm-dd",
        showSecond: true,        
        timeFormat: 'HH:mm:ss',
        
    });
    $( "#datepicker_end" ).datetimepicker({
        dateFormat: "yy-mm-dd",
        showSecond: true,
        timeFormat: 'HH:mm:ss',
    });
    error();
    //时间查询
    $("#search").click(function(){
        
        var input_dict = {};
        var start_date = $(".start").val();
        var end_date = $(".end").val();
        var start_name = $(".start").attr('name');
        var end_name = $(".end").attr('name');
        var select = $("#select option:selected").text();
        var select_name = $('.choice').attr('name');
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();

       

        $('#datepicker_start').val(start_date);
        $('#datepicker_end').val(end_date);
        
        if(start_date == "" && end_date != ""){
            alert("请输入开始时间！");
            return;
        } 
        if(start_date != "" && end_date == ""){
            alert("请输入结束时间");
            return;
        }
        if(start_date == "" && end_date == ""){
            
            start_date = "2000-1-1 00:00:00";
            var date = new Date();
            var seperator1 = "-";
            var seperator2 = ":";
            var month = date.getMonth() + 1;
            var strDate = date.getDate();
            if(month >= 1 && month <= 9){
                month = "0" + month;
            }
            if (strDate >= 0 && strDate <= 9){
                strDate = "0" + strDate;
            }
            end_date = date.getFullYear() + seperator1 + month + seperator1 +strDate + " " + date.getHours() + seperator2 + date.getMinutes() + seperator2 + date.getSeconds();

        }
        /*if(select == "ALL"){
            window.location.reload();
        }*/

        input_dict[start_name] = start_date;
        input_dict[end_name] = end_date;
        input_dict[select_name] = select;
        input_dict['csrfmiddlewaretoken'] = csrf;
        if (select == "ALL"){
            input_dict['pageStart'] = pageStartAll;
            input_dict['pageSize'] = pageSize;
        }
        if (select == "ERROR"){
            input_dict['pageStart'] = pageStartError;
            input_dict['pageSize'] = pageSize;
        }
        

        getSearchData(input_dict);
        
        
        
    });

  

   //$(".load").on('click','div',function(){});
   //关闭自动刷新
  
  $("#open").click(function(){
      var flag = setInterval('myrefresh()',10000);

  });
  $("#close").click(function(){
       clearInterval(flag);

  });
   
    $(document).on("click", "#searchAll", function() {
        
        counterAll ++;
        pageStart = counterAll * pageSize;    
        input_dict = getDic(pageStart,pageSize);
       
        getMoreSearchData(input_dict);
    });

    $(document).on("click", "#searchError", function() {
        
        counterError ++;
        pageStart = counterError * pageSize;
        input_dict = getDic(pageStart,pageSize); 

        getMoreSearchData(input_dict);
    });


  });
function getDic(pageStart,pageSize){

        var input_dict = {};
        var start_date = $(".start").val();
        var end_date = $(".end").val();
        var start_name = $(".start").attr('name');
        var end_name = $(".end").attr('name');
        var select = $("#select option:selected").text();
        var select_name = $('.choice').attr('name');
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();

       

        $('#datepicker_start').val(start_date);
        $('#datepicker_end').val(end_date);
        
        if(start_date == "" && end_date != ""){
            alert("请输入开始时间！");
            return;
        } 
        if(start_date != "" && end_date == ""){
            alert("请输入结束时间");
            return;
        }
        if(start_date == "" && end_date == ""){
            
            start_date = "2000-1-1 00:00:00";
            var date = new Date();
            var seperator1 = "-";
            var seperator2 = ":";
            var month = date.getMonth() + 1;
            var strDate = date.getDate();
            if(month >= 1 && month <= 9){
                month = "0" + month;
            }
            if (strDate >= 0 && strDate <= 9){
                strDate = "0" + strDate;
            }
            end_date = date.getFullYear() + seperator1 + month + seperator1 +strDate + " " + date.getHours() + seperator2 + date.getMinutes() + seperator2 + date.getSeconds();

        }
        /*if(select == "ALL"){
            window.location.reload();
        }*/

        input_dict[start_name] = start_date;
        input_dict[end_name] = end_date;
        input_dict[select_name] = select;
        input_dict['csrfmiddlewaretoken'] = csrf;
        input_dict['pageStart'] = pageStart;
        input_dict['pageSize'] = pageSize;

        return input_dict;
}

 
    

function getData(offset,size){
        
        var getData = {};
        getData['offset'] = offset;
        getData['size'] = size;
        var lastNum;
      
        $.ajax({
            type: 'GET',
            url:"/load/",
            data:getData,

            success:function(data){

                var sum = data['number'];
               
                var dataList = data['data'];
                var result = '';
                var remain = sum - offset -1;
                var alarm;
                if (sum == 0){
                    alert("此时间段没有数据!");
                }
                console.log(sum);
                console.log(dataList);
                if (remain >= size ){
                    for(var i = 0; i <10; i++){
                        result = "<tr>" + "<td>" + dataList[i].date + "</td>" +"<td>" + dataList[i].location + "</td>"+"<td>" + dataList[i].type + "</td>"+"<td>" + dataList[i].content + "</td>" + "</tr>";        
                        $('.all_info').append(result); 
                    }
                } else {
                    for(var i = 0; i <=remain; i++){
                        result = "<tr>" + "<td>" + dataList[i].date + "</td>" +"<td>" + dataList[i].location + "</td>"+"<td>" + dataList[i].type + "</td>"+"<td>" + dataList[i].content + "</td>" + "</tr>";        
                        $('.all_info').append(result); 
                    }
                }  
                
                error();
               
                alarm = data["alarm"];
                
                if ( (offset + size) >= sum){
                    
                    $(".load-more").html("加载完毕");
                }
                if(alarm == true)
                {
                  
                    alert("有新错误了！");
                    var music = document.getElementById('music');
                    music.play();
                }
                //$('.alarm').attr("value",alarm);
      
            },
            error:function(){
                alert("false");
            }

        });
        
        
    }

//getSearch  data
function getSearchData(datas){
    var type = datas['choice'];
    var offset = datas['pageStart'];
    var size = datas['pageSize'];

    $.ajax({
            type:"POST",  
            url:"/search/", 
            data:datas,
            
            success:function(data){ 
                        
                var sum = data['number'];
               
                var dataList = data['data'];
                var remain = sum - offset -1;
                var result = '';

                console.log(sum);
                console.log(dataList);
                console.log(remain);

                if (sum == 0){
                    alert("此时间段没有数据!");
                }
                
                $('.all_info ').html("");
                var item_header = "<tr>" + "<td>" + "时间" + "</td>" +"<td>" + "位置" + "</td>"+"<td>" + "类型" + "</td>"+"<td>" + "内容" + "</td>" +"</tr>";
                $('.all_info ').prepend(item_header);
                /*for(var i = 0 ;i < datas.length; i++){ 

                    result = "<tr>" + "<td>" + datas[i].date + "</td>" +"<td>" + datas[i].type + "</td>"+"<td>" + datas[i].content + "</td>" + "</tr>";        
                    $('.all_info').prepend(result);     
                }
                $('.all_info ').prepend(item_header);
                error();
                
                $('.load').html("");*/
                if (remain >= size ){
                    for(var i = 0; i <10; i++){
                        result = "<tr>" + "<td>" + dataList[i].date + "</td>" +"<td>" + dataList[i].location + "</td>"+"<td>" + dataList[i].type + "</td>"+"<td>" + dataList[i].content + "</td>" + "</tr>";        
                        $('.all_info').append(result); 
                    }
                } else {
                    for(var i = 0; i <=remain; i++){
                        result = "<tr>" + "<td>" + dataList[i].date + "</td>" +"<td>" + dataList[i].location + "</td>"+"<td>"+"<td>" + dataList[i].type + "</td>"+"<td>" + dataList[i].content + "</td>" + "</tr>";        
                        $('.all_info').append(result); 
                    }
                }  
               
                error();
                
                if (type == "ALL"){
                    $('.load').children('div').remove();
                    var newbutton = "<div id = 'searchAll'>"+"加载更多"+"</div>";
                    $('.load').append(newbutton);
                }
                if (type == "ERROR"){
                    $('.load').children('div').remove();
                    var newbutton = "<div id = 'searchError'>"+"加载更多"+"</div>";
                    $('.load').append(newbutton);
                }
                
                
              
            },
            error:function(){
                alert("false");
            }
            
        });


}
//getmore
function getMoreSearchData(datas){
    var type = datas['choice'];
    var offset = datas['pageStart'];
    var size = datas['pageSize'];

    $.ajax({
            type:"POST",  
            url:"/search/", 
            data:datas,
            
            success:function(data){ 
                
                
                
                var sum = data['number'];
               
                var dataList = data['data'];
                var remain = sum - offset -1;

                var result = '';
                console.log(sum);
                console.log(dataList);
                console.log(remain);

                if (sum == 0){
                    alert("此时间段没有数据!");
                }  
               // $('.all_info ').html("");
               // var item_header = "<tr>" + "<td>" + "日期" + "</td>" +"<td>" + "类型" + "</td>"+"<td>" + "内容" + "</td>" +"</tr>";
                //$('.all_info ').prepend(item_header);
                /*for(var i = 0 ;i < datas.length; i++){ 

                    result = "<tr>" + "<td>" + datas[i].date + "</td>" +"<td>" + datas[i].type + "</td>"+"<td>" + datas[i].content + "</td>" + "</tr>";        
                    $('.all_info').prepend(result);     
                }
                $('.all_info ').prepend(item_header);
                error();
                
                $('.load').html("");*/
                if (remain >= size ){
                    for(var i = 0; i <10; i++){
                        result = "<tr>" + "<td>" + dataList[i].date + "</td>" +"<td>" + dataList[i].location + "</td>"+"<td>" + dataList[i].type + "</td>"+"<td>" + dataList[i].content + "</td>" + "</tr>";        
                        $('.all_info').append(result); 
                    }
                } else {
                    for(var i = 0; i <=remain; i++){
                        result = "<tr>" + "<td>" + dataList[i].date + "</td>" +"<td>" + dataList[i].location + "</td>"+"<td>" + dataList[i].type + "</td>"+"<td>" + dataList[i].content + "</td>" + "</tr>";        
                        $('.all_info').append(result); 
                    }
                }  
               
                error();

                if ( (offset + size) >= sum){
                    if (type == "ALL"){
                        $("#searchAll").html("加载完毕");
                    }
                    if (type == "ERROR"){
                        $("#searchError").html("加载完毕");
                    }
                    
                }
                  
            },
            error:function(){
                alert("false");
            }
            
        });


}



function error(){

    var tr_list = $('.all_info tr');
    var str = new RegExp("ERROR");
    $('.all_info tr').each(function(i){
        $(this).children('td').each(function(j){
            var exist_error = str.test($(this).text());
            if(exist_error){
                $(this).parent('tr').addClass("error");      
            }
        });
    });
          
}

//定时刷新页面
function myrefresh (){
    
    window.location.reload();

}
    