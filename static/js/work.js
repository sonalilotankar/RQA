
    $(function(){
      $('.demo-contenteditable').pastableContenteditable();
      $('.demo').on('pasteImage', function(ev, data){
        var blobUrl = URL.createObjectURL(data.blob);
        var name = data.name != null ? ', name: ' + data.name : '';
        // console.log(data);
        var res = 'zero';
        var url = window.location.href + '/upload';
        $.ajax({
            url: url,
            type: 'POST',
            data:
                {
                    'data': data.dataURL
                },
            success: function (response) {
                // console.log(response);
                res = response.message;
                $('#message').text( "Picture uploaded successfully, conversion result:");
                $('#result').text(res);
                $('#btn').attr("data-clipboard-text",res);
            },
            error: function(responsestr){
                // console.log("error");
                // console.log(responsestr);
                $('#message').text( "Upload failed, please try again!");
            }
        });
        $('#message').text( 'Picture is uploading, size：' + data.width + ' x ' + data.height);
      })
    });
