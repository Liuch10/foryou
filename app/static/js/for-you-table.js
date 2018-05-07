$(document).ready(function() {

    $('#startConsult').click(function(){
        $('#comment-history-table').DataTable().destroy();
        var prefix = getLeftNarBarActive();
        var caseIds = getSelectedCase(prefix);
        var case_id=caseIds[0];
        var descriptions = getSelectedCaseDescription(prefix)
        $("#consultation_case_id").text(caseIds[0]);
        $("#consultation_message").text(descriptions[0]);
        var data={
            id: case_id
        }
        $('#add_consultation_comment').unbind('click');
        $('#add_consultation_comment').click(function(){
            var comment={
                msg:     $('#my_comment').val(),
                case_id: case_id
            }
            $.ajax({
                type: 'POST',
                url:  '/addConsultationComment',
                data: comment,
                dataType: 'json',
                success: function(data){
                    if (data.result=='success'){
                        var comment_history_table = $('#comment-history-table').DataTable();
                        comment_history_table.ajax.reload();
                    }else{
                    alert(data.result);
                    }
                },
                error: function(){
                    alert('error');
                }
            });
        });

        //pic display 
        $.ajax({
            type: 'POST',
            url:  '/getImageAddress',
            data: data,
            dataType: 'json',
            success: function(data){
                if (data.result=='success'){
                    ipfs.cat(data.address, function(err, data) {
                        var buf = new buffer.Buffer(data, 'binary');
                        var src=hexToBase64(buf.toString('hex'));
                        $('#consult_img').attr('src','data:image/jpeg;base64,'+src)
                    });
                }else{
                    alert(data.address);
                }
            },
           error: function(){
                alert('error');
            }
        });

        //message display 
        $.ajax({
            type: 'POST',
            url:  '/getConsultationMessage',
            data: data,
            dataType: 'json',
            success: function(data){
                $("#consultation_message").val(data.message);
            },
           error: function(){
                alert('error');
            }
        });
        //table content 
        $('#comment-history-table').DataTable( {
        "scrollY": '350px',
        "scrollCollapse": true,
        "processing": true,
        "serverSide": false,
        "bDeferRender": true,
        "bAutoWidth" : true,
        "ajax": {
            "url": "/comment-history-table-infos?case_id="+case_id.toString(),
            "type": "GET"
        },"columns": [
            { "title": "index",  "data" : "id" },
            { "title": "医生",  "data" : "doctor" },
            { "title": "评论",  "data" : "comment" },
            { "title": "日期",  "data" : "date" }
        ],
        "aoColumnDefs":[
            {
                "bVisible": false,
                "aTargets": [ 0,3]
            },
        ],
        "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            $(nRow).css("background-color", "black");
            $(nRow).css("color", "white");
        },
        initComplete : function() {

        },
        "dom": 't',
        "fnInitComplete":function(){
            $("#pBottom > #case-table_previous").css("color", "white");
            $('.checkbox_select').parent('td').css("background-color","black");
        },
        });
    });

    $('#check_wallet').click(function(){
    $('#wallet_table').DataTable().destroy();
    $('#wallet_table').DataTable( {
        "bPaginate" : true,
        "processing": true,
        "searching": true,
        "serverSide": false,
        "bDeferRender": true,
        "bAutoWidth" : true,
        "bFilter": true,
        "ajax": {
            "url": "/wallet-table-infos",
            "type": "GET"
        },"columns": [
            { "title": "index",  "data" : "id" },
            { "title": "日期",  "data" : "date" },
            { "title": "交易类型",  "data" : "type" },
            { "title": "交易数量",  "data" : "amount" },
            // { "title": "支出",  "data" : "amount1" },
            // { "title": "余币",  "data" : "amount2" },
            { "title": "信息摘要",  "data" : "spec" }
        ],
        "aoColumnDefs":[
            {
                "bVisible": false,
                "aTargets": [ 0 ]
            },
        ],
        "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            $(nRow).css("background-color", "black");
            $(nRow).css("color", "white");
        },
        initComplete : function() {

        },
        "dom": 't<"#pBottom"p>',
        "fnInitComplete":function(){
            $("#pBottom > #case-table_previous").css("color", "white");
            // $('#case-table').css("color","white").css("background-color","black");
            $('.checkbox_select').parent('td').css("background-color","black");
            // $("#case-table_filter").detach().appendTo('#new-search-area');
        },
    });
    });

    $('#case-table').DataTable( {
        "bPaginate" : true,
        "processing": true,
        "searching": true,
        "serverSide": false,
        "bDeferRender": true,
        "bAutoWidth" : true,
        "bFilter": true,
        "ajax": {
            "url": "/case-table-infos",
            "type": "GET"
        },
        "language": {
            "sSearch": "搜索: ",
            "sSearchPlaceholder": "请输入病人ID"
        },
        "columns": [
            { "data" : null },
            { "title": "index",  "data" : "id" },
            { "title": "患者ID",  "data" : "userid" },
            { "title": "姓名",  "data" : "name" },
            { "title": "性别",  "data" : "sex" },
            { "title": "年龄",  "data" : "age" },
            { "title": "影像类型",  "data" : "imgTpye" },
            { "title": "良恶性",  "data" : "type" },
            { "title": "诊断结果",  "data" : "consultResult" },
            { "title": "标注状态",  "data" : "commentType" },
            { "title": "上传日期",  "data" : "uploadDate" },
            { "title": "操作",  "data" : null }
        ],
        "aoColumnDefs":[
            {
                "targets": 0,
                "data": null,
                "bSortable": false,
                render: function(data, type, row) {
                    var html ="<input type ='checkbox' name='check-upload-case' class='checkbox_select' value='" + row.id + "'>";
                    return html;
                }
            },
            {
                "targets": -1,
                "bSortable": false,
                render: function(data, type, row) {
                    var html ='<a data-toggle="modal" data-target="#preview-modal" onclick="previewImage(' + row.id + ')" value="' + row.id + '">查看</a>';

                    return html;
                }
            },
            {
                "bSearchable": true,
                "bVisible": true,
                "bFilter": true,
                "aTargets": [ 2,3,4,5,6,7 ]
            },
            {
                "bVisible": false,
                "aTargets": [ 1, 9 ]
            },
        ],
        "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            $(nRow).css("background-color", "black");
            $(nRow).css("color", "white");
        },
        initComplete : function() {

        },
        "dom": 'rft<"#pBottom"p>',
        "fnInitComplete":function(){
            $("#pBottom > #case-table_previous").css("color", "white");
            // $('#case-table').css("color","white").css("background-color","black");
            $('.checkbox_select').parent('td').css("background-color","black");
            // $("#case-table_filter").detach().appendTo('#new-search-area');
        },
        "fnDrawCallback": function(){
            $("#all_checked").prop("checked",false);
        },
    } );

    $('#comment-page-case-table').DataTable( {
        "bPaginate" : true,
        "processing": true,
        "searching": true,
        "serverSide": false,
        "bDeferRender": true,
        "bAutoWidth" : true,
        "bFilter": true,
        "ajax": {
            "url": "/case-table-infos",
            "type": "GET"
        },
        "language": {
            "sSearch": "搜索: ",
            "sSearchPlaceholder": "请输入病人ID"
        },
        "columns": [
            { "data" : null },
            { "title": "index",  "data" : "id" },
            { "title": "患者ID",  "data" : "userid" },
            { "title": "姓名",  "data" : "name" },
            { "title": "性别",  "data" : "sex" },
            { "title": "年龄",  "data" : "age" },
            { "title": "影像类型",  "data" : "imgTpye" },
            { "title": "良恶性",  "data" : "type" },
            { "title": "诊断结果",  "data" : "consultResult" },
            { "title": "标注状态",  "data" : "commentType" },
            { "title": "上传日期",  "data" : "uploadDate" },
            { "title": "操作",  "data" : null }
        ],
        "aoColumnDefs":[
            {
                "targets": 0,
                "data": null,
                "bSortable": false,
                render: function(data, type, row) {
                    var html ="<input type ='checkbox' name='comment-check-upload-case' class='comment-checkbox-select' value='" + row.id + "'>";
                    return html;
                }
            },
            {
                "targets": -1,
                "bSortable": false,
                render: function(data, type, row) {
                    // var html ='<a href="javascript:alert(' + row.id + ')" value="' + row.id + '">查看</button>';
                    var html ='<a data-toggle="modal" data-target="#preview-modal" onclick="previewImage(' + row.id + ')" value="' + row.id + '">查看</a>';
                    return html;
                }
            },
            {
                "bSearchable": true,
                "bVisible": true,
                "bFilter": true,
                "aTargets": [ 2 ]
            },
            {
                "bVisible": false,
                "aTargets": [ 1 ]
            },
        ],
        "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            $(nRow).css("background-color", "black");
            $(nRow).css("color", "white");
        },
        initComplete : function() {

        },
        "dom": 'rft<"#pBottom"p>',
        "fnInitComplete":function(){
            $("#pBottom > #comment-page-case-table_previous").css("color", "white");
            $('.comment-checkbox-select').parent('td').css("background-color","black");
            // $("#case-table_filter").detach().appendTo('#new-search-area');
        },
        "fnDrawCallback": function(){
            $("#comment-all-checked").prop("checked",false);
        },
    } );

    $('#answer-huizhen-case-table').DataTable( {
        "bPaginate" : true,
        "processing": true,
        "searching": true,
        "serverSide": false,
        "bDeferRender": true,
        "bAutoWidth" : true,
        "bFilter": true,
        "ajax": {
            "url": "/answer-case-table-infos",
            "type": "GET"
        },
        "language": {
            "sSearch": "搜索: ",
            "sSearchPlaceholder": "请输入病人ID"
        },
        "columns": [
            { "data" : null },
            { "title": "index",  "data" : "id" },
            { "title": "会诊说明",  "data" : "description" },
            { "title": "发起人",  "data" : "starter" },
            { "title": "所在医院",  "data" : "hospital" },
            { "title": "所在科室",  "data" : "department" },
            { "title": "发起日期",  "data" : "start-date" },
            { "title": "操作",  "data" : null }
        ],
        "aoColumnDefs":[
            {
                "targets": 0,
                "data": null,
                "bSortable": false,
                render: function(data, type, row) {
                    var html ="<input type ='checkbox' description='"+row.description+"' name='answer-huizhen-check-upload-case' class='answer-huizhen-checkbox-select' value='" + row.id + "'>";
                    return html;
                }
            },
            {
                "targets": -1,
                "bSortable": false,
                render: function(data, type, row) {
                    // var html ='<a href="javascript:alert(' + row.id + ')" value="' + row.id + '">查看</button>';
                    var html ='<a data-toggle="modal" data-target="#preview-modal" onclick="previewImage(' + row.id + ')" value="' + row.id + '">查看</a>';
                    return html;
                }
            },
            {
                "bSearchable": true,
                "bVisible": true,
                "bFilter": true,
                "aTargets": [ 2 ]
            },
            {
                "bVisible": false,
                "aTargets": [ 1 ]
            },
        ],
        "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            $(nRow).css("background-color", "black");
            $(nRow).css("color", "white");
        },
        initComplete : function() {

        },
        "dom": 'rft<"#pBottom"p>',
        "fnInitComplete":function(){
            $("#pBottom > #answer-huizhen-case-table_previous").css("color", "white");
            $('.answer-huizhen-checkbox-select').parent('td').css("background-color","black");
            // $("#case-table_filter").detach().appendTo('#new-search-area');
        },
        "fnDrawCallback": function(){
            $("#answer-huizhen-all-checked").prop("checked",false);
        },
    } );

    $('#ask-huizhen-case-table').DataTable( {
        "bPaginate" : true,
        "processing": true,
        "searching": true,
        "serverSide": false,
        "bDeferRender": true,
        "bAutoWidth" : true,
        "bFilter": true,
        "ajax": {
            "url": "/case-table-infos",
            "type": "GET"
        },
        "language": {
            "sSearch": "搜索: ",
            "sSearchPlaceholder": "请输入病人ID"
        },
        "columns": [
            { "data" : null },
            { "title": "index",  "data" : "id" },
            { "title": "患者ID",  "data" : "userid" },
            { "title": "姓名",  "data" : "name" },
            { "title": "性别",  "data" : "sex" },
            { "title": "年龄",  "data" : "age" },
            { "title": "影像类型",  "data" : "imgTpye" },
            { "title": "良恶性",  "data" : "type" },
            { "title": "诊断结果",  "data" : "consultResult" },
            { "title": "标注状态",  "data" : "commentType" },
            { "title": "上传日期",  "data" : "uploadDate" },
            { "title": "操作",  "data" : null }
        ],
        "aoColumnDefs":[
            {
                "targets": 0,
                "data": null,
                "bSortable": false,
                render: function(data, type, row) {
                    var html ="<input type ='checkbox' name='ask-huizhen-check-upload-case' class='ask-huizhen-checkbox-select' value='" + row.id + "'>";
                    return html;
                }
            },
            {
                "targets": -1,
                "bSortable": false,
                render: function(data, type, row) {
                    // var html ='<a href="javascript:alert(' + row.id + ')" value="' + row.id + '">查看</button>';
                    var html ='<a data-toggle="modal" data-target="#preview-modal" onclick="previewImage(' + row.id + ')" value="' + row.id + '">查看</a>';
                    return html;
                }
            },
            {
                "bSearchable": true,
                "bVisible": true,
                "bFilter": true,
                "aTargets": [ 2 ]
            },
            {
                "bVisible": false,
                "aTargets": [ 1, 9 ]
            },
        ],
        "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            $(nRow).css("background-color", "black");
            $(nRow).css("color", "white");
        },
        initComplete : function() {

        },
        "dom": 'rft<"#pBottom"p>',
        "fnInitComplete":function(){
            $("#pBottom > #ask-huizhen-case-table_previous").css("color", "white");
            $('.ask-huizhen-checkbox-select').parent('td').css("background-color","black");
            // $("#case-table_filter").detach().appendTo('#new-search-area');
        },
        "fnDrawCallback": function(){
            $("#ask-huizhen-all-checked").prop("checked",false);
        },
    } );

    $("#check_source").click(function(){
        $('#source-expert-case-table').DataTable().destroy();
        $('#source-user-case-table').DataTable().destroy();
        $('#source-expert-case-table').DataTable({
        "bPaginate" : true,
        "processing": true,
        "searching": true,
        "serverSide": false,
        "bDeferRender": true,
        "bAutoWidth" : true,
        "bFilter": true,
        "ajax": {
            "url": "/case-table-source-infos?type=expert",
            "type": "GET"
        },
        "language": {
            "sSearch": "搜索: ",
            "sSearchPlaceholder": "请输入病人ID"
        },
        "columns": [
            { "data" : null },
            { "title": "index",  "data" : "id" },
            { "title": "患者ID",  "data" : "userid" },
            { "title": "姓名",  "data" : "name" },
            { "title": "性别",  "data" : "sex" },
            { "title": "年龄",  "data" : "age" },
            { "title": "影像类型",  "data" : "imgTpye" },
            { "title": "良恶性",  "data" : "type" },
            { "title": "诊断结果",  "data" : "consultResult" },
            { "title": "标注状态",  "data" : "commentType" },
            { "title": "上传日期",  "data" : "uploadDate" },
            { "title": "医院",  "data" : "hospital" },
            { "title": "专家",  "data" : "expert" },
            { "title": "操作",  "data" : null }
        ],
        "aoColumnDefs":[
            {
                "targets": 0,
                "data": null,
                "bSortable": false,
                render: function(data, type, row) {
                    var html ="<input type ='checkbox' name='source-expert-check-upload-case' class='source-expert-checkbox-select' value='" + row.id + "'>";
                    return html;
                }
            },
            {
                "targets": -1,
                "bSortable": false,
                render: function(data, type, row) {
                    // var html ='<a href="javascript:alert(' + row.id + ')" value="' + row.id + '">查看</button>';
                    var html ='<a data-toggle="modal" data-target="#preview-modal" onclick="previewImage(' + row.id + ')" value="' + row.id + '">查看</a>';
                    return html;
                }
            },
            {
                "bSearchable": true,
                "bVisible": true,
                "bFilter": true,
                "aTargets": [ 2 ]
            },
            {
                "bVisible": false,
                "aTargets": [ 1 ]
            },
        ],
        "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            $(nRow).css("background-color", "black");
            $(nRow).css("color", "white");
        },
        initComplete : function() {

        },
        "dom": 'rft<"#pBottom"p>',
        "fnInitComplete":function(){
            $("#pBottom > #source-expert-case-table_previous").css("color", "white");
            $('.source-expert-checkbox-select').parent('td').css("background-color","black");
            // $("#case-table_filter").detach().appendTo('#new-search-area');
        },
        "fnDrawCallback": function(){
            $("#source-expert-all-checked").prop("checked",false);
        },
        });

        $('#source-user-case-table').DataTable( {
        "bPaginate" : true,
        "processing": true,
        "searching": true,
        "serverSide": false,
        "bDeferRender": true,
        "bAutoWidth" : true,
        "bFilter": true,
        "ajax": {
            "url": "/case-table-source-infos?type=case",
            "type": "GET"
        },
        "language": {
            "sSearch": "搜索: ",
            "sSearchPlaceholder": "请输入病人ID"
        },
        "columns": [
            { "data" : null },
            { "title": "index",  "data" : "id" },
            { "title": "患者ID",  "data" : "userid" },
            { "title": "姓名",  "data" : "name" },
            { "title": "性别",  "data" : "sex" },
            { "title": "年龄",  "data" : "age" },
            { "title": "影像类型",  "data" : "imgTpye" },
            { "title": "良恶性",  "data" : "type" },
            { "title": "诊断结果",  "data" : "consultResult" },
            { "title": "标注状态",  "data" : "commentType" },
            { "title": "上传日期",  "data" : "uploadDate" },
            { "title": "医院",  "data" : "hospital" },
            { "title": "科室",  "data" : "department" },
            { "title": "操作",  "data" : null }
        ],
        "aoColumnDefs":[
            {
                "targets": 0,
                "data": null,
                "bSortable": false,
                render: function(data, type, row) {
                    var html ="<input type ='checkbox' name='source-user-check-upload-case' class='source-user-checkbox-select' value='" + row.id + "'>";
                    return html;
                }
            },
            {
                "targets": -1,
                "bSortable": false,
                render: function(data, type, row) {
                    // var html ='<a href="javascript:alert(' + row.id + ')" value="' + row.id + '">查看</button>';
                    var html ='<a data-toggle="modal" data-target="#preview-modal" onclick="previewImage(' + row.id + ')" value="' + row.id + '">查看</a>';
                    return html;
                }
            },
            {
                "bSearchable": true,
                "bVisible": true,
                "bFilter": true,
                "aTargets": [ 2 ]
            },
            {
                "bVisible": false,
                "aTargets": [ 1, 12 ]
            },
        ],
        "fnRowCallback": function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            $(nRow).css("background-color", "black");
            $(nRow).css("color", "white");
        },
        initComplete : function() {

        },
        "dom": 'rft<"#pBottom"p>',
        "fnInitComplete":function(){
            $("#pBottom > #source-user-case-table_previous").css("color", "white");
            $('.source-user-checkbox-select').parent('td').css("background-color","black");
            // $("#case-table_filter").detach().appendTo('#new-search-area');
        },
        "fnDrawCallback": function(){
            $("#source-user-all-checked").prop("checked",false);
        },
        });

    });

    $('[name=select_all]').on('click', function () {
        if (this.checked) {
            $('.checkbox_select').each(function () {
                this.checked = true;
            });
        } else {
            $('.checkbox_select').each(function () {
                this.checked = false;
            });
        }
    });

    $('[name=comment-select-all]').on('click', function () {
        if (this.checked) {
            $('.comment-checkbox-select').each(function () {
                this.checked = true;
            });
        } else {
            $('.comment-checkbox-select').each(function () {
                this.checked = false;
            });
        }
    });

    $('[name=ask-huizhen-page-select-all]').on('click', function () {
        if (this.checked) {
            $('.ask-huizhen-checkbox-select').each(function () {
                this.checked = true;
            });
        } else {
            $('.ask-huizhen-checkbox-select').each(function () {
                this.checked = false;
            });
        }
    });

    $('[name=answer-huizhen-page-select-all]').on('click', function () {
        if (this.checked) {
            $('.answer-huizhen-checkbox-select').each(function () {
                this.checked = true;
            });
        } else {
            $('.answer-huizhen-checkbox-select').each(function () {
                this.checked = false;
            });
        }
    });

    $('[name=source-user-select-all]').on('click', function () {
        if (this.checked) {
            $('.source-user-checkbox-select').each(function () {
                this.checked = true;
            });
        } else {
            $('.source-user-checkbox-select').each(function () {
                this.checked = false;
            });
        }
    });

    $('[name=source-expert-select-all]').on('click', function () {
        if (this.checked) {
            $('.source-expert-checkbox-select').each(function () {
                this.checked = true;
            });
        } else {
            $('.source-expert-checkbox-select').each(function () {
                this.checked = false;
            });
        }
    });

    function getSelectedCase(prefix) {
        var a = [];
        $('input[name="' + prefix + 'check-upload-case"]:checked').each(function(){
            a.push($(this).val());
        });
        return a;
    };

    function getSelectedCaseDescription(prefix) {
        var a = [];
        $('input[name="' + prefix + 'check-upload-case"]:checked').each(function(){
            a.push($(this).attr("description"));
        });
        return a;
    };

    function getLeftNarBarActive() {
        var prefix = $(".navbar-nav .nav-link.active").data("tag");
        if (prefix == "huizhen-") {
            prefix = $(".nav.navbar-collapse .nav-link.active.huizhen-nav").data("tag");
        } else if (prefix == "source-") {
            prefix = $(".nav.navbar-collapse .nav-link.active.source-nav").data("tag");
        }
        return prefix;
    }



    $("#startComment").click(function(){
        // TODO 每次标注取第一个选择的case
        var prefix = getLeftNarBarActive();
        var caseIds = getSelectedCase(prefix);
        var targetCaseId = caseIds[0];
        // TODO 跳转到check或者look页面，
        window.location.href='/diagnose?id='+targetCaseId;
        // $.ajax({
        //     type: 'GET',
        //     url:  '/start_comment?id=' + targetCaseId,
        //     success: function(data){
        //         console.log('success');
        //     },
        //     error: function(){
        //         console.log('error');
        //     }
        // });
    });

    $("#updateExpertBtn").click(function(){

        var prefix = getLeftNarBarActive();
        var caseIds = getSelectedCase(prefix);
        var comment = $('#update-expert-comment').val();
        var data={
            'case_id': caseIds[0],
            'comment'           : comment
        }
        $.ajax({
            type: 'POST',
            url:  '/update_expert',
            data: data,
            dataType: 'json',
            success: function(data){
                alert('success');
            },
            error: function(){
                alert('error');
            }
        });
    });

    $("#fqhzModalBtn").click(function(){
        var prefix = getLeftNarBarActive();
        var caseIds = getSelectedCase(prefix);
        var comment = $('#help_text').val();
        alert(comment)
        var data={
            'case_id'          : caseIds[0],
            'comment'           : comment
        }
        $.ajax({
            type: 'POST',
            url:  '/start_consult',
            data: data,
            dataType: 'json',
            success: function(data){
                alert(data.result);
                var answer_huizhen_case_table = $('#answer-huizhen-case-table').DataTable();
                answer_huizhen_case_table.ajax.reload();
            },
           error: function(){
                alert('error');
            }
        });
    });

    $("#show-jshz").click(function () {
        var answer_huizhen_case_table = $('#answer-huizhen-case-table').DataTable();
        answer_huizhen_case_table.ajax.reload();
    })

    $("#loadImageBtn").click(function(){
        var patient_name            = $('#patient_name').val();
        var patient_gender          = $('#patient_gender').val();
        var patient_age             = $('#patient_age').val();
        var patient_photo_type      = $('#patient_photo_type').val();
        var patient_photo_file      = $('#patient_photo_file').val();
        var patient_diagnose_type   = $('#patient_diagnose_type').val();
        var patient_diagnose_result = $('#patient_diagnose_result').val();
        var data={
            'patient_name'           : patient_name,
            'patient_gender'         : patient_gender,
            'patient_age'            : parseInt(patient_age),
            'patient_photo_type'     : patient_photo_type,
            'patient_photo_file'     : patient_photo_file,
            'patient_diagnose_type'  : patient_diagnose_type,
            'patient_diagnose_result': patient_diagnose_result
        }
        $.ajax({
            type: 'POST',
            url:  '/upload_case',
            data: data,
            dataType: 'json',
            success: function(data){
                $('#loadimage').modal('hide')
                if (data.result == "success") {
                    $('#token_amount').html(data.token);
                    $('#jlModal').modal('show');
                    // reload table
                    // var wallet_table = $('#wallet_table').DataTable();
                    var case_table = $('#case-table').DataTable();
                    var comment_page_case_table = $('#comment-page-case-table').DataTable();
                    var answer_huizhen_case_table = $('#answer-huizhen-case-table').DataTable();
                    var ask_huizhen_case_table = $('#ask-huizhen-case-table').DataTable();
                    var source_expert_case_table = $('#source-expert-case-table').DataTable();
                    var source_user_case_table = $('#source-user-case-table').DataTable();

                    // wallet_table.ajax.reload();
                    case_table.ajax.reload();
                    comment_page_case_table.ajax.reload();
                    answer_huizhen_case_table.ajax.reload();
                    ask_huizhen_case_table.ajax.reload();
                    source_expert_case_table.ajax.reload();
                    source_user_case_table.ajax.reload();
                }
                else{
                    alert(data.result)
                }
            },
            error: function(){
                alert('error');
            }
        });
    });


} );
