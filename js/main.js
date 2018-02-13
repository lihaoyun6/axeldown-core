String.prototype.fs=function() {
  segments=this.split('%s');
  ret='';
  for (var i in arguments) {
    ret += segments[i] + arguments[i];
  }
  return ret + segments[segments.length-1];
}
String.prototype.trim=function() {
    return this.replace(/^\s+|\s+$/g,"");
}
String.prototype.ltrim=function() {
    return this.replace(/^\s+/,"");
}
String.prototype.rtrim=function() {
    return this.replace(/\s+$/,"");
};
String.prototype.empty=function() {
    return this == '';
};

Number.prototype.human=function() {
    if (this < 1024)
        return parseInt(this) + 'B';
    else if (this < 1024 * 1024)
        return parseInt(this/1024*10)/10 + 'KB';
    else if (this < 1024 * 1024 * 1024)
        return parseInt(this/1024/1024*10)/10 + 'MB';
    else if (this < 1024 * 1024 * 1024 * 1024)
        return parseInt(this/1024/1024/1024*10)/10 + 'GB';
    else
        return parseInt(this/1024/1024/1024/1024*10)/10 + 'TB';
}
Number.prototype.time=function() {
    if (this < 60)
      return parseInt(this) + ' S';
    else if (this < 3600)
      return parseInt(this/60*10)/10 + ' M';
    else if (this < 3600*24)
      return parseInt(this/3600*10)/10 + ' H';
    else
      return parseInt(this/3600/24*10)/10 + ' D';
}


$(function() {
var pdata = {current:'A', states:['A', 'D', 'C', 'W', 'P', 'E']};
$.extend({'alert': function(msg){
  $('#msg').text(msg).show();
},
'unalert': function(){
  $('#msg').hide();
}});
function api(action, data, callback) {
  if (data == undefined)
    data = new Object;
  data['action'] = action;
  $.ajax({
    url:'/api',
    type:'POST',
    data:JSON.stringify(data),
    dataType:'json',
    success:function(ret) {
      callback(ret);
    },
    error:function(ret){
      console.error(ret);
      $.alert("内部错误，请刷新页面, 若无效需重启Axeldown");
    },
    timeout:function(ret){
      console.error("request timeout");
      $.alert("请求超时，请重启Axeldown");
    }
  });
}

function init() {
  $('#toolbar .create').click(open_create_dialog);
  $('#toolbar .cconfig').click(open_cconfig_dialog);
  $('#create button.create').click(function(){
    var urls = $.trim($('#create textarea[name="url"]').val());
    if (!urls) {
      $.alert('请输入下载地址!');
      setTimeout(function(){
        $.unalert();
      }, 5000);
      close_create_dialog();
      return;
    }
    var headers = $('#create textarea[name="headers"]').val();
    var output = $('#create input[name="filename"]').val();
    var thsize = $('#create input[name="thsize"]').val();
    var downloads = $('#create input[name="downloads"]').val();
    var ua = $('#create input[name="ua"]').val();
    var immediately = $('#create input[name="immediately"]').attr('checked') == 'checked';
    urls = urls.split('\n');
    if (urls.length > 1)
      output = "";
    for (var i in urls) {
      var url = urls[i];
      var parts = url.split('\t');
      console.log(parts);
      if (parts.length > 1) {
        url = parts[0];
        output = parts[1];
      }
      var options = {options:{url:url, headers:headers, output:output, downloads:downloads, immediately:immediately, thsize:thsize, ua:ua}};
      api('create', options, function() {
        setTimeout(refresh, 1000);
      });
    }
    close_create_dialog();
    refresh();
  });
  
  $('#cconfig button.save').click(function(){
    var cpath = $('#cconfig input[name="cpath"]').val();
    if (!cpath) {
      $.alert('请输入默认下载位置!');
      setTimeout(function(){
        $.unalert();
      }, 5000);
      close_cconfig_dialog();
      return;
    }
    var cua = $('#cconfig textarea[name="cua"]').val();
    var cmaxspeed = $('#cconfig input[name="cmaxspeed"]').val();
    var cthread = $('#cconfig input[name="cthread"]').val();
    var cqueue = $('#cconfig input[name="cqueue"]').val();
    if (!cqueue) {
      var cqueue = "10";
        }
    var cbuffer = $('#cconfig input[name="cbuffer"]').val();
    if (!cbuffer) {
      var cbuffer = "5120";
    }
    var cforce = $('#cconfig input[name="cforce"]').attr('checked') == 'checked';
    var options = {options:{force_download:cforce, total_maxspeed:cmaxspeed, downloads:cpath, default_thread_size:cthread, buffer_size:cbuffer, task_queue_size:cqueue, user_agent:cua}};
      api('cconfig', options, function() {
        setTimeout(refresh, 1000);
        });
      close_cconfig_dialog();
      refresh();
  });

  $('#toolbar button.pause').click(function(){
    var ids = [];
    $('#list tr:visible input[type="checkbox"]:checked').each(function(i){
      if ($(this).parent().parent().hasClass('D'))
        ids.push($(this).val());
    });
    if (ids.length)
      pause(ids);
  });
  $('#toolbar button.remove').click(function(){
    var ids = [];
    $('#list tr:visible input[type="checkbox"]:checked').each(function(i){
      ids.push($(this).val());
    });
    if (ids.length)
      remove(ids);
  });
  $('#toolbar button.resume').click(function(){
    var ids = [];
    $('#list tr:visible input[type="checkbox"]:checked').each(function(i){
      ids.push($(this).val());
    });
    if (ids.length)
      resume(ids);
  });
  $('#toolbar button.download').click(function(){
    var ids = [];
    $('#list tr:visible input[type="checkbox"]:checked').each(function(i){
      ids.push($(this).val());
    });
    if (ids.length)
      download(ids);
  });
  $('#create button.cancel').click(close_create_dialog);
  $('#cconfig button.cancel').click(close_cconfig_dialog);
  $('#list td.filename').live('click', function(){
    if($(this).parent().next().css('display') != 'none') {
      $(this).parent().next().hide('fast');
    }else{
      $(this).parent().next().show('fast');
    }
  });
  $('#list thead td').click(function(){
    //
  });
  $('#list th.select').click(function(){
    if($(this).find('select').length)
      return;
    var selector  = $('<select>'
                      + '<option value="A">全选</option>'
                      + '<option value="D">下载中</option>'
                      + '<option value="C">已完成</option>'
                      + '<option value="P">暂停中</option>'
                      + '<option value="W">等待中</option>'
                      + '<option value="E">发生错误</option>'
                      + '<option value="N">全不选</option>'
                    + '</select>');
    $('#list td input[type="checkbox"]').attr('checked', 'checked');
    var td = $(this);
    selector.change(function(){
      var selected = $(this).val();
      if (selected == 'A')
        $('#list td input[type="checkbox"]').attr('checked', 'checked');
      else if (selected == 'N')
        $('#list td input[type="checkbox"]').removeAttr('checked');
      else{
        $('#list td input[type="checkbox"]').removeAttr('checked');
        $('#list tr.%s'.fs(selected)).find('td input[type="checkbox"]').attr('checked', 'checked');
      }
      td.html('选中');
    });
    $(this).html('').append(selector);
    return true;
  });
  $('#list td.select').live('click', function() {
    var selector = $(this).find('input');
    if (selector.attr('checked'))
      selector.removeAttr('checked');
    else
      selector.attr('checked', 'checked');
  });
  $('#list td.select input').live('click', function(event) {
    event.stopPropagation()
  });
  $(window).resize(function(){
    reset_progress_length();
  });
  $('#states span').click(function(){
    $('#states span').removeClass('current');
    var cssClass = $(this).attr('class');
    $(this).addClass('current');
    pdata.current = cssClass;
    $('#list tbody tr').each(function(){
      var cc = $(this).attr('class');
      for (var i in pdata.states) {
        var s = pdata.states[i];
        if ($.inArray(s, cc.split(' '))>=0) {
          if (cssClass == 'A' || s == cssClass) {
            $(this).show();
          } else {
            $(this).hide();
          }
          break;
        }
      }
    });
  });

  refresh();
  setInterval(refresh, 1000);
}

function refresh() {
  api('tasks', null, function(return_content){
    states = {1:'W', 2:'D', 3:'P', 4:'C', 5:'E'}
    var tasks = return_content['result'];
    var trs = "";
    $.each(tasks, function(i) {
      var task = tasks[i];
      var errmsg_title = states[task.state] == 'E' ? 'title="%s"'.fs(task.errmsg) : '';
      if (states[task.state] == 'C')
          var tr = '<tr id="task-%s" %s class="%s C completed %s">'.fs(task.id, errmsg_title, i % 2 ? 'odd' : 'even', pdata.current!='C' && pdata.current!='A' ? 'hidden' : '');
      else if (states[task.state] == 'D')
          var tr = '<tr id="task-%s" %s class="%s D downloading %s">'.fs(task.id, errmsg_title, i % 2 ? 'odd' : 'even', pdata.current!='D' && pdata.current!='A' ? 'hidden' : '');
      else if (states[task.state] == 'P')
          var tr = '<tr id="task-%s" %s class="%s P pause %s">'.fs(task.id, errmsg_title, i % 2 ? 'odd' : 'even', pdata.current!='P' && pdata.current!='A' ? 'hidden' : '');
      else if (states[task.state] == 'W')
          var tr = '<tr id="task-%s" %s class="%s W waitting %s">'.fs(task.id, errmsg_title, i % 2 ? 'odd' : 'even', pdata.current!='W' && pdata.current!='A' ? 'hidden' : '');
      else
          var tr = '<tr id="task-%s" %s class="%s E error %s">'.fs(task.id, errmsg_title, i % 2 ? 'odd' : 'even', pdata.current!='E' && pdata.current!='A' ? 'hidden' : '');
      if($('#list input[value="%s"]:checked'.fs(task.id)).length) {
        tr += '<td class="center select"><input type="checkbox" value="%s" checked></td>'.fs(task.id);
      } else {
        tr += '<td class="center select"><input type="checkbox" value="%s"></td>'.fs(task.id);
      }
      //tr += '<td class="center">%s</td>'.fs(task.id);
      tr += '<td class="center state %s">%s</td>'.fs(states[task.state], states[task.state]);
      tr += '<td class="filename">%s%s</td>'.fs(task.downloads ? task.downloads : task.downloads, task.output);
      var total = task.total ? task.total.human() : '';
      if (states[task.state] == 'C')
          var done = total;
      else
          var done = task.done ? task.done.human() : ''
      if (!done && !total)
        tr += '<td class=""></td>';
      else
        tr += '<td class="done"><div percent="%s" class="progress"><span class="filename">%s / %s</span></div></td></td>'.fs(states[task.state] == 'C' ? 1 : task.done/task.total, done, total);
      if (states[task.state] != 'D')
          speed = '';
      else if (task.speed == 0)
          speed = 0;
      else
          speed = task.speed ? task.speed.human() + '/s' : '';
      tr += '<td class="center">%s</td>'.fs(speed);
      if (states[task.state] != 'D')
          left = '';
      else
          left = task.left !== null ? task.left.time() : '';
      tr += '<td class="center">%s</td>'.fs(left);
      tr += '</tr>';

      if ($('#list tr#url-%s'.fs(task.id)).length && $('#list tr#url-%s'.fs(task.id)).css('display') != 'none')
        tr += '<tr style="display:table-row;" id="url-' + task.id + '" class="url"><td colspan="2"></td><td colspan="6">线程数:' + task.thsize + '&nbsp;&nbsp;&nbsp;下载地址:'+ task.url + '</td></tr>';
      else
        tr += '<tr id="url-' + task.id + '" class="url"><td colspan="2"></td><td colspan="6">线程数:' + task.thsize + '&nbsp;&nbsp;&nbsp;下载地址:'+ task.url + '</td></tr>';
      trs += tr;
    });
    $('#wrap table tbody').html(trs);
    reset_progress_length();
  });
}

function reset_progress_length(){
  $('#list .progress').each(function(i){
    var percent = $(this).attr('percent');
    var width = $(this).parent().width();
    $(this).width(width * percent);
    $(this).find('span.filename').width(width);
  });
}

function open_create_dialog() {
  var $d = $(document);
  var ww = $d.width();
  var wh = $d.height();

  var $c = $('#create');
  var cw = $c.width();
  var ch = $c.height()

  var left = (ww - cw) / 2;
  var top = (wh - ch) / 2;
  if (left < 0)
    left = 0;
  if (top < 0)
    top = 0;
  $c.css({left:left,top:top,display:'block'});

  $('#background').css({display:'block',width:ww,height:wh});
  rconfig();
}

function open_cconfig_dialog() {
  var $d = $(document);
  var ww = $d.width();
  var wh = $d.height();

  var $c = $('#cconfig');
  var cw = $c.width();
  var ch = $c.height()

  var left = (ww - cw) / 2;
  var top = (wh - ch) / 2;
  if (left < 0)
    left = 0;
  if (top < 0)
    top = 0;
  $c.css({left:left,top:top,display:'block'});

  $('#background').css({display:'block',width:ww,height:wh});
  rconfig();
}

function close_create_dialog() {
  $('#create').hide();
  $('#background').hide();
}

function close_cconfig_dialog() {
  $('#cconfig').hide();
  $('#background').hide();
}

function pause(ids) {
  api('pause', {ids:ids}, function() {
    $('#list input[type="checkbox"]:checked').removeAttr('checked');
    refresh();
  });
}

function remove(ids) {
  api('remove', {ids:ids}, function() {
    $('#list input[type="checkbox"]:checked').removeAttr('checked');
    refresh();
  });
}

function resume(ids) {
  api('resume', {ids:ids}, function() {
    $('#list input[type="checkbox"]:checked').removeAttr('checked');
    refresh();
  });
}

function download(ids) {
  for (var i in ids) {
    var id = ids[i];
    var filename = $('#task-%s td.filename'.fs(id)).text();
    var url = '/download/%s'.fs(filename);
    document.location.href = url;
  }
}

function rconfig() {
  api('rconfig', null, function(return_content){
    var rconfig = return_content['result'];
    console.error(rconfig);
    $.each(rconfig, function(key, val) {
        $('#' + key).val(val);
        $("input[id="+key+"]").attr("checked",val);
        $('#' + key + "1").val(val);
        $("input[id="+key+"1]").attr("checked",val);
 　　});   
  });
}

function settop() {
}

function setbottom () {
}

init();
});
