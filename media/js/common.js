//将所有bootstrap 自带的label块变成inline，使之平铺
function setLabel(){
    $('label').each(function(){
        $(this).css('display','inline');
    })
}

// 删除图片
function del_pic(id){
    if(confirm('是否删除该图')){
        var url = '/manager/blog/del_pic/';
        $.post(url,{'pic_id':id},function(data){
            if(data == 'ok'){
                alert('删除成功');
                return true;
            }else{
                alert('删除失败');
                return false;
            }
        })
    }
}
//插入标签
function getTags(){
    var url = '/manager/blog/get_tags/';
    $.post(url,function(data){
        var dialog = art.dialog({
        title:'插入标签',
        content:data
        })
    })
};

// 选择标签插入标签框中
function getIt(elem,id){
    var text = $(elem).text();
    var html = '' +
    '<li class="tagit-choice ui-widget-content ui-state-default ui-corner-all tagit-choice-editable">' +
    '<span class="tagit-label">'+text+'</span><a class="tagit-close">' +
    '<span class="text-icon" onclick="delt('+text+')">×</span>' +
    '<span class="ui-icon ui-icon-close"></span>' +
    '</a>' +
    '</li>'
    $('.tagit-new').before(html);
    addText();
}
function delt(text){
    $("#id_for_tags").tagit("removeTagByLabel", text)
}

// 页面所有超链接添加随机数
function addRandom(){
     rand = Math.random();
    //超链接
     $("a").each(function () {
        href = $(this).attr("href");
        if (href.length == 0 || href.indexOf("javascript") > -1) return;
        else if (href.indexOf("?") > -1) {
            $(this).attr("href", href + "&" + rand);
        }
        else {
            $(this).attr("href", href + "?" + rand);
        }
     });
    // 表单action
    $('form').each(function(){
        action = $(this).attr('action');
        if (action.length == 0 || action.indexOf("javascript") > -1) return;
        else if (action.indexOf("?") > -1) {
            $(this).attr("action", action + "&" + rand);
        }
        else {
            $(this).attr("action", action + "?" + rand);
        }

    })
}

// POST数据
function comPost(url, jsonData,msg){
    try{
        $.post(url,jsonData,function(data){
            if(data == 'ok'){
                alert(msg+'成功');
                return true;
            }else{
                alert(msg+'失败');
                return false;
            }
        })
    }catch (err){
        alert('错误名称：'+err.name);
        alert('错误信息：'+err.message)
    }

}


// 公共浏览次数、赞、踩、分享到等方法，异步获取和提交
function sharp_and_opera(jsonData, showHtml){
    /*
    jsonData:{'id':1, 'app_label':'blog', 'model':'blog','type':xx}  具体见视图函数
    showHtml:表示要显示在某个id为shwoHtml的区域里
     */
    var url = '/commons/sharp_and_opera/';
    $.post(url, jsonData, function(data){
        $('#'+showHtml).html(data);
    })
}

// 清空表单
function cleanForm(){
    $(':input','form')
     .not(':button, :submit, :reset, :hidden')
     .val('')
     .removeAttr('checked')
     .removeAttr('selected');

    //$('#'+form)[0].reset();
}

//设置禁用或启用按钮
function is_disabled(id, is_disable) {
	/*
	id:对象id
	is_disable:true启用;false:禁用
	is_disable参数如果不传默认为true
	author:xw
	date:2009-4-13
	*/

	var img_display = '';
	if (arguments.length == 1) {
		is_disable = true;
	}
	if(typeof($("#"+id+"_img").attr("id")) == "undefined") {
		$("#"+id).after("&nbsp;<img id='"+id+"_img' src='/site_media/images/loading.gif' />");
	}
	if (!is_disable){
		img_display = 'none';
	}
	$('#'+id).attr('disabled', is_disable);
	$('#'+id+'_img').css('display', img_display);
}

function isCheckEmail(email) {
	/*
	 *验证邮箱格式是否正确, 正确：true， 错误：false
	**/
	//var e = /^([a-zA-Z0-9_-])+[@]{1}(\S)+[.]{1}(\w)+/;
	var e =  /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/;
	if (e.test(email)) {
		return true;
	}
	return false;
}

//返回加载等待html
function GetLodingHtml(margin) {
	/*
	margin:上下距离， 默认：50px
	*/
	var margin_num = 50;
	if (typeof(margin) !== 'undefined') {
		margin_num = parseInt(margin);
	}
	var html = '<div style="margin:'+margin_num+'px 0;">';
    html += '<div class="loading-img">正在加载数据，请稍后...</div>';
    html += '</div>';
	return html;
}

//删除字符串两边空格
function del_blank(s)
{
	return s.replace(/^\s*/,"").replace(/\s*$/,"");
}

// 是否为中文
function isChn(str) {
  var reg = /^[\u4E00-\u9FA5]+$/;
  if (!reg.test(str)) {
	return false;
  }
  return true;
}

//全选事件
function CheckAll(name) {
	$("[name="+name+"]").attr('checked', true);
}

//反选事件
function CheckInverse(name) {
	$.each($("[name="+name+"]"),function(n){
		this.checked = !this.checked;
	});
}

//关闭页面所有对话框
function allClose(){
    var list = art.dialog.list;
    for (var i in list) {
        list[i].close();
    };
}

//删除两边空格，包括中文圆角空格
(function($){
	$.trim = function (text) {
		return (text||"").replace(/^\s+|\s+$/g,"").replace(/^[　]+|[　]+$/g, "");
	}
})(jQuery);

// 显示图片
function showPic(id){
    var url = '/commons/showPic/';
    $.post(url,{"id":id}, function(data){
        art.dialog({title:"图片浏览", content:'<img src="/upload_media/'+data+'" >' , lock:true,padding: 0});
    })
}