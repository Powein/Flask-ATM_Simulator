$(function(){
    // 登出
    $('#log-button').click(
        function(event){
            
            window.location.href = '/log'
        }
    )
    
    $('#speed-test').click(
        function(event){
            window.location.href = '/speedtest'
        }
    )

    $('#logout-button').click(
        function(event){
            $.ajax({
                url: '/logout',
                type: 'POST',
                success: function(response) {
                    location.reload()
                }
                }
            )
        }
    )
    // 存款
    $('#deposit').click(
        function(event){
            $.ajax({
                url: '/deposit?amount=' + $('#transaction-amount').val(),
                method: 'POST',
                dataType: 'json',
                success:function(response) {
                    if (response.code == 200){
                        alert(response.message)
                        $('#current-balance').text(response.balance + '元')
                    } else if (response.code == 400){
                        alert(response.message)
                    }
                },
                error:() => {
                    alert('网络错误/未登录')
                }
        })
        }
    )
    // 取款
    $('#withdraw').click(
        function(event){
            $.ajax({
                url: '/withdraw?amount=' + $('#transaction-amount').val(),
                method: 'POST',
                dataType: 'json',
                success:function(response) {
                    if (response.code == 200){
                        alert(response.message)
                        $('#current-balance').text(response.balance + '元')
                    } else if (response.code == 400){
                        alert(response.message)
                    }
                },
                error:() => {
                    alert('网络错误/未登录')
                }
        })
        }
    )
    // 转账
    $('#transfer').click(
        function(event){
            var to_user_id = window.prompt("请输入转账对象ID")
            if (to_user_id){
                $.ajax({
                    url: '/transfer?amount=' + $('#transaction-amount').val() + '&to_user_id=' + to_user_id,
                    method: 'POST',
                    dataType: 'json',
                    success: function(response) {
                        if (response.code == 200){
                            alert(response.message)
                            $('#current-balance').text(response.balance + '元')
                        } else if (response.code == 400){
                            alert(response.message)
                        }
                    },
                    error:() => {
                        alert('网络错误/未登录')
                    }
                    }
                )
            }
        }
    )
    // 日志
})