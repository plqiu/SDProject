$(document).ready(function() {

	$("#modify").click(function(){
        var host = $('#host').val();
        var port = $('#port').val();
        var active = $('#active').val();
        var ftphost = $('#ftphost').val();
        var port = $('#port').val();
        var user = $('#user').val();
        var password = $('#password').val();
        var remote = $('#remote').val();
        var samactive = $('#samactive').val();
        var path = $('#path').val();
        
        var WindFramName = $('#WindFramName').val();
        var template = $('#template').val();
        var expire = $('#expire').val();

        var datas = {};

        var datas1 = {};
        var datas2 = {};
        var datas3 = {};
        var datas4 = {};

        var csrf = $('input[name="csrfmiddlewaretoken"]').val();

        datas1['host'] = host;
        datas1['port'] = port;
        
        datas2['active'] = active;
        datas2['host'] = ftphost;
        datas2['port'] = port;
        datas2['user'] = user;
        datas2['password'] = password;
        datas2['remote_save_dir'] = remote;

        datas3['active'] = samactive;
        datas3['path'] = path;
        
        datas4['WindFramName'] = WindFramName;
        datas4['template'] = template;
        
        datas['udp_server'] = datas1;
        datas['ftp'] = datas2;
        datas['samba'] = datas3;
        datas['WindFramInformation'] = datas4;
        datas['expire'] = expire;
        datas['csrfmiddlewaretoken'] = csrf;

        console.log(datas);
        
        $.ajax({ 
            type:"POST",  
            url:"/modify/",
            
            data:JSON.stringify(datas),

            success:function(data){
            	 alert(data);

            },
            error:function(){
                alert("false");
            }
        });
        


    });
});