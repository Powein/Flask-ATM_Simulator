var total_time = 0.0
var tried_times = 0
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));// 在外面等待他完成就可以了
}

speed_test = function() {
    var start =performance.now()
    $.ajax(
        {
            url: 'speedtest',
            type: 'POST',
            success:function(response){
                if(response.code == 200){
                    var end = performance.now()
                    var time_consumed = end - start
                    total_time += time_consumed
                    tried_times += 1
                    // console.log(total_time)
                    // console.log(start)
                    // console.log(end)
                    $('#speed-test-result').text("当前延迟:"+(total_time / tried_times).toFixed(1) +'毫秒')
                }
            }
        }
        
    )
// $('#speed-test-result').text(total_time +'ms')
}

async function test_n_speed(n) {
    for (var i = 0; i < n; i++) {
        speed_test()
        await sleep(100)
    }
}
// $(function(){
//     $('#start-speed-test').click(
//         () => {
//             for (var i = 0; i < 1; i++){
//                 speed_test()
//                 await sleep(1000)
//             }
//         }
//     )
// })
