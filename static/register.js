
bindCaptchaButton = function() {
        $('#sendCode').click(function(event) {
            var $this = $(this)//获取当前按钮的jquery对象
            event.preventDefault();//防止默认：提交表单
            var email = $('#email').val()
            // alert('验证码已发送至邮箱' + email)
            $.ajax(//这个ajax IO操作可以再被优化, 应该把它丢给另一个进程用,不过这里没必要了.
                {
                    
                    url:'/send_captcha?email=' + email,
                    method:'GET',
                    success:function(data) {
                        $this.off('click')
                        if(data.code == 200){
                            alert('验证码已发送至邮箱' + email)
                        }else{
                            alert(data.message)
                        }
                        var countdown = 10
                        var timer = setInterval(() => {
                            countdown--
                            $this.text('重试(' + countdown + ')')
                            if (countdown <= 0){
                                clearInterval(timer)
                                countdown = 10
                                $this.text('发送验证码')
                                bindCaptchaButton()
                            }
                        }, 1000);

                    },
                    fail:()=>{
                        alert('发送失败')
                    }
                }
            )
        })
    }
$(function() {
    bindCaptchaButton()
})