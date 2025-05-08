let g_SteamAccountDetails = null;

let g_RequestInFlight = false;
let g_IsAutoConfirming = false;
let g_IsAutoCanceling = false;
let g_UsedTimestamps = [];
let g_CheckInitAttempts = 0;

checkInit();
async function checkInit() {
  loading("Loading");

  if (!window.UserScriptInjected) {
    if (++g_CheckInitAttempts < 20) {
      // Give the userscript some time to inject and run
      setTimeout(checkInit, 100);
      return;
    }

    // Userscript is not present
    $(".view").hide();
    $("#fatal-error-view").show();

    return;
  }

  await UserScriptInjected.setServerUrl("http://127.0.0.1:5000/sda2/");

  // Userscript is present
  let accountDetails = await UserScriptInjected.getLoggedInAccountDetails();
  if (!accountDetails) {
    fatalError(
      "Sign in to steamcommunity.com before attempting to access this page."
    );
    return;
  }

  g_SteamAccountDetails = accountDetails;
  $("#account-name").val(accountDetails.accountName);

  loadConfirmations();
}

$("#refresh-btn").click(loadConfirmations);

async function loadConfirmations() {
  try {
    loading("Loading your confirmations");

    let confsList = await UserScriptInjected.getConfirmationList();
    if (!confsList.success) {
      throw new Error(
        confsList.message ||
          confsList.detail ||
          "Failed to load confirmations list"
      );
    }

    let $mainAppView = $("#main-app-view");

    $("#loader-view").hide();
    $mainAppView.show();

    let $confsContainer = $("#confs-container");

    let confs = confsList.conf || [];
    $mainAppView[confs.length == 0 ? "removeClass" : "addClass"](
      "has-confirmations"
    );
    if (confs.length == 0) {
      return;
    }

    $confsContainer.html("");

    confs.forEach((conf) => {
      let {
        id,
        nonce,
        headline,
        icon,
        summary,
        type_name: typeName,
        accept,
        cancel,
      } = conf;

      let $conf = $('<div class="confirmation" />');

      let removeConf = () => {
        $conf.remove();
        if ($confsContainer.find(".confirmation").length == 0) {
          $("#main-app-view").removeClass("has-confirmations");
        } else if (g_IsAutoConfirming) {
          // start confirming the next one
          $("#accept-all-btn").click();
        } else if (g_IsAutoCanceling) {
          // start canceling the next one
          $("#cancel-all-btn").click();
        }
      };

      let $typeDesc = $('<span class="type-desc" />');
      $typeDesc.text(typeName);

      let $headline = $('<span class="headline" />');
      $headline.text(headline);

      let $summary = $('<span class="summary" />');
      $summary.html(summary.join("<br />"));

      let $icon = $('<img class="icon" />');
      $icon.attr("src", icon);

      let $btnAccept = $('<button class="cs-btn action accept" />');
      $btnAccept.attr("title", accept);
      $btnAccept.html("Accept");
      $btnAccept.click(async () => {
        if (g_RequestInFlight) {
          return;
        }

        try {
          g_RequestInFlight = true;
          $conf.addClass("loading");

          let overrideTimestamp = null;
          if (g_IsAutoConfirming || g_IsAutoCanceling) {
            overrideTimestamp = Math.floor(Date.now() / 1000);

            while (g_UsedTimestamps.includes(overrideTimestamp)) {
              overrideTimestamp++;
            }

            g_UsedTimestamps.push(overrideTimestamp);
          }

          let result = await UserScriptInjected.respondToConfirmation(
            id,
            nonce,
            true,
            overrideTimestamp
          );
          if (!result.success) {
            throw new Error(
              result.message || result.detail || "Could not act on confirmation"
            );
          }

          g_RequestInFlight = false;
          removeConf();
        } catch (ex) {
          alert(ex.message || ex);
          $conf.removeClass("loading");
          g_RequestInFlight = false;
        }
      });

      let $btnCancel = $('<button class="cs-btn action cancel" />');
      $btnCancel.attr("title", cancel);
      $btnCancel.html("Cancel");
      $btnCancel.click(async () => {
        if (g_RequestInFlight) {
          return;
        }

        try {
          g_RequestInFlight = true;
          $conf.addClass("loading");
          let result = await UserScriptInjected.respondToConfirmation(
            id,
            nonce,
            false
          );
          if (!result.success) {
            throw new Error(
              result.message || result.detail || "Could not act on confirmation"
            );
          }

          g_RequestInFlight = false;
          removeConf();
        } catch (ex) {
          alert(ex.message || ex);
          $conf.removeClass("loading");
          g_RequestInFlight = false;
        }
      });

      $conf.append($typeDesc);
      $conf.append($headline);
      $conf.append($summary);
      $conf.append($icon);
      $conf.append($btnAccept);
      $conf.append($btnCancel);

      $confsContainer.append($conf);
    });
  } catch (ex) {
    fatalError("Error: " + (ex.message || ex));
  }
}

$("#accept-all-btn").click(() => {
  if (g_RequestInFlight) {
    return;
  }

  let $confsContainer = $("#confs-container");

  if ($confsContainer.find(".confirmation").length == 0) {
    // nothing to do here
    g_IsAutoConfirming = false;
    return;
  }

  g_IsAutoConfirming = true;
  g_AutoConfirmTimestampOffset = -20;
  $confsContainer.find(":first-child").find(".accept").click();
});

$("#cancel-all-btn").click(() => {
  if (g_RequestInFlight) {
    return;
  }

  let $confsContainer = $("#confs-container");

  if ($confsContainer.find(".confirmation").length == 0) {
    // nothing to do here
    g_IsAutoCanceling = false;
    return;
  }

  g_IsAutoCanceling = true;
  g_AutoConfirmTimestampOffset = -20;
  $confsContainer.find(":first-child").find(".cancel").click();
});

function loading(message) {
  $(".view").hide();

  let $loaderView = $("#loader-view");
  $loaderView.find("h1").text(message);
  $loaderView.show();
}

function fatalError(message) {
  $(".view").hide();

  let $fatalView = $("#fatal-error-view");
  $fatalView.find("#fatal-error-msg").text(message);
  $fatalView.show();
}

async function copyCode() {
  try {
    const accountName = g_SteamAccountDetails.accountName;

    const response = await fetch(
      `http://127.0.0.1:5000/sda2/code/${accountName}`
    );

    if (!response.ok) {
      throw new Error("Failed to fetch the code");
    }

    const code = await response.text();
    await navigator.clipboard.writeText(code);
  } catch (error) {
    console.error("Error fetching or copying the code:", error);
    alert("Failed to fetch or copy the code.");
  }
}
