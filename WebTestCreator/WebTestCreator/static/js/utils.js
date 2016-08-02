/*!
 * Utils v1.0 
 * Copyright (c) 2016 Kronegger GmbH.
 * Created by Marc Bayon using jQuery & Ajax
 */

var $xmlCommands;
var numrows = 1;

$(window).load(function () {
    $('#myModal').modal('show');
});

$(document).ready(function () {
    numrows = 1;
    $('input[name=numrows]').val(numrows);
    $('select[name=row1_command]').val("Reset");
    $('input[name=row1_order]').val(1);
        
});

$.ajax({
    type: "GET",
    url: "/static/js/command_tree.xml",
    dataType: "xml",
    error: function () {
        alert('Error loading XML document, Please report this to the WebMaster (marc.bayon@kronegger.com)');
    },
    success: function (xml) {
        $xmlCommands = $(xml);
        selectChanged(document.getElementById('row1_command'));

    }
});



function addLine() {
    var $lastdiv = $('div[id^="row"]:last');
    var num = parseInt($lastdiv.prop("id").match(/\d+/g), 10) + 1;
    var clonedDiv = $('#row0').clone();
    var $clon = clonedDiv.clone().prop("id", 'row' + num);
    $('input[name=numrows]').val(num);
    //Update the names of column 1 & 2
    $clon.children().each(function () {
        var divId = $(this).attr('id');
        if (divId == "col1") {
            $(this).find("input").prop("name", 'row' + num + '_order');
            $(this).find("input").prop("value", num );
        }
        else {
            $(this).find("select").prop("name", 'row' + num + '_command');
            $(this).find("select").prop("id", 'row' + num + '_command');
        }
    });
    $('#cloneHere').before($clon);
    selectChanged(document.getElementById('row'+num+'_command'));
    $clon.fadeIn();    

}

function removeLine(item) {
    $(item).parent().parent().fadeOut("normal", function () {
        $(this).remove();
    });


}


function selectChanged(item) {
    
    var $workingRow = $(item).parent().parent();
    var $payload = $workingRow.find("#payload");
    var $response = $workingRow.find("#response");
    var $errorcode = $workingRow.find("#errorcode");
    var rowDivId = $workingRow.attr('id');
    var $commands = $xmlCommands.find("command");

    $commands.each(function () {
        var commandID = $(this).attr('id');
        if (commandID.toLowerCase() == item.value.toLowerCase()) {

            //clean divs
            $payload.empty();
            $response.empty();
            $errorcode.empty();
            var errorList = "";
            var order_payload = 1;
            var order_response = 1;
            $(this).children().each(function () {
                //Payloads
                var $foundPayload = $(this).find("payload").each(function () {
                    
                    var compare = $(this).find('type').text();
                    //Inputs
                    if (compare == "Input") {
                        var name = $(this).find('name').text();
                        $payload.append('<input type="text" name="' + rowDivId + '_' + commandID + '_' + name + '_payload_'+order_payload+'" class="form-control" placeholder="' + name + '">');
                        order_payload = order_payload + 1;
                    }
                });
                //Responses
                var $foundResponse = $(this).find("response").each(function () {
                    var compare = $(this).find('type').text();
                    //Inputs
                    if (compare == "Input") {
                        var name = $(this).find('name').text();
                        $response.append('<input type="text" name="' + rowDivId + '_' + commandID + '_' + name + '_response_'+order_response+'" class="form-control" placeholder="' + name + '">');
                        order_response = order_response + 1;
                    }
                });
                //Error Codes

                var $foundErrorCode = $(this).find("error").each(function () {
                    var error = $(this).text();
                    //ErrorList
                    errorList = errorList + ('<option>' + error + '</option>');
                });

            });
            $errorcode.append('<select class="form-control" name="' + rowDivId + '_' + commandID + '_error"  onchange="blockErrorSelect(this);" >' + errorList + '</select>');

            return false;//break
        }
        else {
            $payload.text(item.value);
            $response.text(item.value);
            $errorcode.text(item.value);
        }
    });

}

function getName(item) {

    $("#current_users").clone(false).find("*[id]").andSelf().each(function () { $(this).attr("id", $(this).attr("id") + "_cloned"); });
    var numiId = $(item).parent().parent().attr('id');
    alert(numId);
}

function blockErrorSelect(item) {
    var $workingRow = $(item).parent().parent().parent();
    if (item.value != "") {
        $workingRow.find("#response input").each(function (index)
        {
            
            $(this).val('');
            $(this).prop("disabled", 'disabled');
        });
    }
    else {
        $workingRow.find("#response input").each(function (index)
        {
            $(this).val('');
            $(this).prop("disabled", '');
        });
    }
}
