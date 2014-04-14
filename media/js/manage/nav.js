/**
 * Created by Administrator on 13-12-26.
 * function:To match url for the effect of sidebar in manage page
 * developer:BeginMan
 */

var url_match = [
    {'url':/\/manager/g,'type':0},                            // 管理首页
    {'url':/\/manager\/add_sort/g,'type':1},                   // 标签管理
];

function controlNav(){
    var location_url = window.location.url;
    var type = 0;
    for(var i=0;i<url_match.length;i++){
        var url = url_match[i].url;
        if(url.test(location_url)){
            // 如果匹配成功
            type = url_match[i].type;
            break;
        }

        $('a[type="'+type+'"]').parent('li').addClass('active');
    }

}