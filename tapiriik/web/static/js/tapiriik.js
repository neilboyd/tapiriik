// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

tapiriik = {};

tapiriik.Init = function(){
	// ...
	$("#syncButton").click(tapiriik.ImmediateSyncRequested);
	$(".service a.authDialog").click(tapiriik.AuthDialogLinkClicked);
	$(".service a.deauthDialog").click(tapiriik.DeauthDialogLinkClicked);
	$.address.change(tapiriik.AddressChanged);
	tapiriik.AddressChanged();
	if (tapiriik.User !== undefined){
		if (tapiriik.User.ConnectedServicesCount > 1){
			tapiriik.UpdateCountdownTimer = setInterval(tapiriik.UpdateSyncCountdown, 60000);
			tapiriik.RefreshCountdownTimer = setInterval(tapiriik.RefreshSyncCountdown, 1000);
			tapiriik.UpdateSyncCountdown();
		}
	}
	$(".logo").click(function(e){
		if (e.shiftKey){
			tapiriik.ShowDebugInfo();
			return false;
		}
	});

	$(".paymentForm").hide();
	$(".paymentButton").show();
	$(".paymentButton").click(function(){
		$(".paymentButton").slideUp();
		$(".paymentForm").slideDown();
		return false;
	});
	$(".reclaimButton").click(tapiriik.PaymentReclaimDialogLinkClicked);
};

tapiriik.AddressChanged=function(){
	var components = $.address.pathNames();
	if (components[0]=="auth") {
		tapiriik.OpenAuthDialog(components[1]);
		return;
	} else if (components[0]=="disconnect") {
		tapiriik.OpenDeauthDialog(components[1]);
		return;
	} else if (components[0]=="payments" && components[1]=="claim"){
		tapiriik.OpenPaymentReclaimDialog();
		return;
	}
	tapiriik.DismissServiceDialog();
};

tapiriik.PaymentReclaimDialogLinkClicked = function(){
	$.address.value("payments/claim");
	return false;
};

tapiriik.AuthDialogLinkClicked = function(e){
	$.address.value("auth/"+$(this).attr("service"));
	return false;
};

tapiriik.DeauthDialogLinkClicked = function(e){
	$.address.value("disconnect/"+$(this).attr("service"));
	return false;
};

tapiriik.IFrameOAuthReturn=function(success){
	if (success){
		$.address.value("/");
		window.location.reload();
	} else {
		$.address.value("/");
	}
};


tapiriik.OpenAuthDialog = function(svcId){
	var mode = tapiriik.ServiceInfo[svcId].AuthenticationType;
	var contents;
	if (mode == "oauth"){
		contents = $("<iframe>").attr("src",tapiriik.ServiceInfo[svcId].AuthorizationURL).attr("id",svcId);
	} else if (mode == "direct") {
		contents = tapiriik.CreateDirectLoginForm(svcId);
	}
	tapiriik.CreateServiceDialog(svcId, contents);
};

tapiriik.OpenDeauthDialog = function(svcId){
	var form = $("<form><center><button id=\"disconnect\">Disconnect</button><button id=\"cancel\" class=\"cancel\">Never mind</button></center></form><h2>(nothing will be deleted)</h2>");
	form.bind("submit", function() {return false;});
	$("#disconnect", form).click(function(){
		if (tapiriik.DeauthPending !== undefined) return false;
		tapiriik.DeauthPending = true;
		$("#disconnect", form).addClass("disabled");
		$.ajax({url:"/auth/disconnect-ajax/"+svcId,
				type:"POST",
				success: function(){
					$.address.value("/");
					window.location.reload();
				},
				error: function(data){
					alert("Error in disconnection: " + $.parseJSON(data.responseText).error+"\n Please contact me ASAP");
					tapiriik.DeauthPending = undefined;
					$("#disconnect", form).removeClass("disabled");
				}});
		return false;
	});
	
	$("#cancel", form).click(function(){
		$.address.value("/");
	});

	tapiriik.CreateServiceDialog(svcId, form);
};

tapiriik.CreateDirectLoginForm = function(svcId){
	var form = $("<form><div class=\"error\">There was a problem logging you in</div><label for=\"email\">Email</label><input autofocus type=\"email\" id=\"email\"/><label for=\"password\">Password</label><input type=\"password\" id=\"password\"><br/><center><button type=\"submit\" >Log in</button></center></form>");
	var loginPending = false;
	form.bind("submit", function(){
		if (loginPending) return false;
		loginPending=true;
		$("button",form).addClass("disabled");
		$.post("/auth/login-ajax/"+svcId,{username:$("#email",form).val(),password:$("#password",form).val()}, function(data){
			if (data.success) {
				$.address.value("/");
				window.location.reload();
			} else {
				$(".error",form).show();
				$("button",form).removeClass("disabled");
				loginPending = false;
			}
		}, "json");
		return false;
	});
	return form;
};

tapiriik.OpenPaymentReclaimDialog = function(){
	var form = $("<form><center><div class=\"error\">Unknown Transaction ID</div><label for=\"txn\" style=\"margin-bottom:7px\">PayPal Transaction ID</label><input type=\"text\" style=\"width:220px;text-align:center;\" placeholder=\"VADE0B248932\" id=\"txn\"><br/><button type=\"submit\" id=\"claim\">Claim</button><p>Your payment will be reassociated with the accounts you a currently connected to</p></center></form>");
	var pending = false;
	form.bind("submit", function(){
		if (pending) return false;
		pending = true;
		$("button",form).addClass("disabled");
		$.ajax({url:"/payments/claim-ajax",
				type:"POST",
				data:{txn: $("#txn",form).val()},
				success: function(){
					$.address.value("/");
					window.location.reload();
				},
				error: function(data){
					$(".error",form).show();
				$("button",form).removeClass("disabled");
				pending = false;
				}});
		return false;
	});
	tapiriik.CreateServiceDialog("tapiriik",form);
};

tapiriik.CreateServiceDialog = function(serviceID, contents) {
	$(".dialogWrap").remove();
	var icon;
	if (serviceID != "tapiriik"){
		var origIcon = $(".service#"+serviceID+" .icon img");
		icon = origIcon.clone().attr("src", origIcon.attr("lgsrc")).hide();
	} else {
		icon = $("<div>").hide().addClass("logo inline").text("tapiriik");
	}
	popover = $("<div>").addClass("dialogPopoverWrap").append(tapiriik.CreatePopover(contents).css({"position":"relative"}));
	popover.css({"position":"relative","display":"none", "width":"100%"});
	var dialogWrap = $("<div>").addClass("dialogWrap").append(icon).append(popover);
	$(".contentWrap").append(dialogWrap);
	$(".mainBlock").fadeOut(250, function(){
		popover.fadeIn(250);
		icon.fadeIn(250);
	});
};
tapiriik.DismissServiceDialog = function(){
	$(".dialogWrap").fadeOut(250, function(){
		$(".dialogWrap").remove();
		$(".mainBlock").fadeIn(250);
	});
};
// I started writing a popover function, then decided it sucked, so I did what you see above
tapiriik.CreatePopover = function(contents){
	var popoverStruct = $("<div class=\"popover\"><div class=\"popoverOuterBorder\"><div class=\"popoverArrow\"><div class=\"popoverArrowInner\"></div></div><div class=\"popoverInner\"></div></div></div>");
	$(".popoverInner", popoverStruct).append(contents);
	return popoverStruct;
};

tapiriik.ImmediateSyncRequested = function(){
	if (!$("#syncButton").hasClass("active")) return false;

	$.get("/sync/schedule/now");
	tapiriik.NextSync = new Date();
	tapiriik.LastSync = new Date();

	tapiriik.RefreshSyncCountdown();
	return false;
};

tapiriik.UpdateSyncCountdown = function(){
	$.ajax({"url":"/sync/status", success:function(data){
		tapiriik.NextSync = data.NextSync !== null ? new Date(data.NextSync) : null;
		tapiriik.LastSync = data.LastSync !== null ? new Date(data.LastSync) : null;
		if (tapiriik.SyncErrorsCt != data.Errors && tapiriik.SyncErrorsCt !== undefined){
			window.location.reload(); // show them the errors
		}
		tapiriik.SyncErrorsCt = data.Errors;
		tapiriik.Synchronizing = data.Synchronizing;
		tapiriik.RefreshSyncCountdown();
	}});
};
tapiriik.FormatTimespan = function(spanMillis){
	if (Math.abs(spanMillis/1000)>60){
		return Math.round(spanMillis/1000/60)+" minute"+(Math.ceil(spanMillis/1000/60)!=1?"s":"");
	} else {
		return Math.ceil(spanMillis/1000)+" second"+(Math.ceil(spanMillis/1000)!=1?"s":"");
	}
};
tapiriik.RefreshSyncCountdown = function(){
	if (tapiriik.SyncErrorsCt !== undefined){

		var delta = tapiriik.NextSync - (new Date());
		if (delta>0 || tapiriik.NextSync == undefined){
			$("#syncButton").show();
			var inCooldown = ((new Date()) - tapiriik.LastSync) <= tapiriik.MinimumSyncInterval*1000;
			if (tapiriik.NextSync !== null){
				if (!inCooldown) {
					$("#syncButton").addClass("active");
				} else {
					$("#syncButton").removeClass("active");
				}
				$("#syncStatusPreamble").text("Next synchronization in ");
				$("#syncButton").text(tapiriik.FormatTimespan(delta));
			} else {
				if (!inCooldown){
					$("#syncButton").addClass("active");
					$("#syncStatusPreamble").text("");
					$("#syncButton").text("Synchronize now");
				} else {
					$("#syncButton").removeClass("active");
					$("#syncStatusPreamble").text("Synchronized");
					$("#syncButton").text("");
				}
			}
			if (tapiriik.FastUpdateCountdownTimer !== undefined){
				clearInterval(tapiriik.FastUpdateCountdownTimer);
				tapiriik.FastUpdateCountdownTimer = undefined;
			}
		} else {
			$("#syncButton").hide();

			if (!tapiriik.Synchronizing){
				$("#syncStatusPreamble").text("Queuing to synchronize");
			} else {
				$("#syncStatusPreamble").text("Synchronizing now");
			}
			
			if (tapiriik.FastUpdateCountdownTimer === undefined){
				tapiriik.FastUpdateCountdownTimer = setInterval(tapiriik.UpdateSyncCountdown, 1000);
			}
		}
		$(".syncStatus").show();
	}
};

tapiriik.ShowDebugInfo = function(){
	if ($(".debugInfo").length>0 || window.location.pathname != "/") return;
	var infoPane = $("<div class=\"debugInfo\"><h3>Diagnostics</h3></div>");
	if (tapiriik.User !== undefined) infoPane.append($("<div><b>User ID:</b> <tt>" + tapiriik.User.ID + "</tt></div>"));
	infoPane.append($("<div><b>System:</b> <tt>" + tapiriik.SiteVer + "</tt></div>"));
	infoPane.hide();
	$(".content").append(infoPane);
	infoPane.slideDown();
};

$(window).load(tapiriik.Init);