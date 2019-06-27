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
   var flag = setInterval('myrefresh()',19000);//指定30秒刷新一次
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

	//控制台显示信息
       function starttime()
			{
			console.log($('#start_time').val());
			}
		function stoptime()
			{
			console.log($('#stop_time').val());
			}
		function interval1(){
			console.log($('#interval option:selected').val());
		}
		function wind_turbine_name1(){
			console.log($('#wind_turbine_name option:selected').val());
		}
		/*将需要采集的数据列表转换成数组*/
		function collect(){
			var collect=$('#collect_var_name li');
			var arr=new Array();
			for (var i = 0; i < collect.length; i++) {
			arr.push($(collect[i]).text());
			}
			console.log($('#start_time').val());
			console.log($('#stop_time').val());
			console.log(arr);
			console.log($('#interval option:selected').val());
			console.log($('#wind_turbine_name option:selected').val());

		}
		/*开始采集，向服务器发送请求*/
		function start()
				{
				var xmlhttp;
				if (window.XMLHttpRequest)
				  {// code for IE7+, Firefox, Chrome, Opera, Safari
				  xmlhttp=new XMLHttpRequest();
				  }
				else
				  {// code for IE6, IE5
				  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
				  }
				xmlhttp.onreadystatechange=function()
				  {
				  if (xmlhttp.readyState==4 && xmlhttp.status==200)
				    {
				    document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
				    }
				  }
				xmlhttp.open("GET","192.168.0.104:8080?start_time=$('#start_time').val()&stop_time=$('#stop_time').val()&collect_var_name=arr&interval=$('#interval option:selected').val()&wind_turbine_name=$('#wind_turbine_name option:selected').val()",true);
				xmlhttp.send();
				}

		$(function get_var(){
			//读取本地xml文件cfads1_02.xml，将name放置在ul中。要求在浏览器路径后添加 --allow-file-access-from-files，不然由于跨域问题不能读取
			if (window.XMLHttpRequest)
				{// code for IE7+, Firefox, Chrome, Opera, Safari
				xmlhttp=new XMLHttpRequest();
				}
				else
				{// code for IE6, IE5
				xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
				}
				xmlhttp.open("GET","cfads1_02.xml",false);
				xmlhttp.send();
				xmlDoc=xmlhttp.responseXML;

				var x=xmlDoc.getElementsByTagName('data');
				for (i=1;i<x.length;i++)
				{
				$('#var_name').append('<label><input type="checkbox"><li>'+x[i].getAttribute('name')+'</li></label>');
				}

				//添加模拟量变量名
		    	$('#add').click(function(){
		    		var a=document.getElementById('var_name');
		    		var add=document.getElementById('add');
		    		var b=a.getElementsByTagName('label');
		    		var c=a.getElementsByTagName('input');
			    		for (var i = 0; i < b.length; i++){
			    			c[i].index=i;
			    			var f=b[i].textContent;
			    			/*console.log(b[i]);*/
		    				if (c[i].checked==true){
		    					$('#collect_var_name').append('<label><input type="checkbox"><li>'+f+'</option></li>');
		    					c[i].checked=false;
			    			};
			    		};
		    		})

		    	//读取本地xml文件cfads1_04.xml，将name放置在ul中。要求在浏览器路径后添加 --allow-file-access-from-files，不然由于跨域问题不能读取
				xmlhttp.open("GET","cfads1_04.xml",false);
				xmlhttp.send();
				xmlDoc=xmlhttp.responseXML;

				var x=xmlDoc.getElementsByTagName('data');
				for (i=1;i<x.length;i++)
				{
				$('#var_name1').append('<label><input type="checkbox"><li>'+x[i].getAttribute('name')+'</li></label>');
				}

				//添加数字量变量名
		    	$('#add1').click(function(){
		    		var a=document.getElementById('var_name1');
		    		var b=a.getElementsByTagName('label');
		    		var c=a.getElementsByTagName('input');
			    		for (var i = 0; i < b.length; i++){
			    			c[i].index=i;
			    			var f=b[i].textContent;

		    				if (c[i].checked==true){
		    						$('#collect_var_name').append('<label><input type="checkbox"><li>'+f+'</li></label>');
		    						c[i].checked=false;
		    	/*$('#add1').click(function(){
		    		var a=$('#var_name1');
		    		var b=$('label');
		    		var c=$('input');
			    		for (var i = 0; i < b.length; i++){
		    				if (c[i].checked==true){
		    				$('#collect_var_name').append(b[i]);*/
			    			};
			    		};
		    		})
    			})
		/*删除已经选择的元素*/
		function remove_varname(){
			var q=$('#collect_var_name label');
			var w=$('#collect_var_name input');
			for (var i = 0; i < w.length; i++) {
				if(w[i].checked==true){
					q[i].remove();
				}
			}
		}

		function test(){
			console.log($('#collect_var_name ul'));
		}
