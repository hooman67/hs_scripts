// IMS authentication for foundry-aws-corp.adobe.io HTML gateway
// Sets user_token cookie so the gateway authorizes asset requests.
// Ref: https://docs.ai.corp.adobe.com/v3/services/services/firefly/foundry/apps/html_gateway/README.html

const ADOBE_IMS_KEY = "addedAdobeIMS";

let _adobeIms = null;
let _profile = null;
let _token = null;

function ims_initialize() {
    return new Promise((resolve, reject) => {
        const adobeData = {
            client_id: "colligo_testing",
            scope: "AdobeID,firefly_api,openid",
            locale: "en_US",
            environment: "stg1",
            locale: navigator.language,
            useLocalStorage: false,
            autoValidateToken: true,
            redirect_uri: location.href,
            onAccessToken(tokenInformation) {
                _token = tokenInformation.token;
            },
            onReauthAccessToken: reauthTokenInformation => {},
            onError(error) {
                reject(error);
                console.error("IMS initialization error:", error);
            },
            onAccessTokenHasExpired() {},
            onReady(appState) {
                (async () => {
                    const isSignedIn = _adobeIms.isSignedInUser();
                    if (isSignedIn) {
                        _profile = await _adobeIms.getProfile();
                        resolve(_profile);
                    } else {
                        resolve(undefined);
                    }
                })();
            }
        };

        adobeImsFactory.createIMSLib(adobeData, ADOBE_IMS_KEY);
        _adobeIms = window[ADOBE_IMS_KEY];
        _adobeIms.initialize();
    });
}

function ims_signOut() {
    _adobeIms.signOut();
    _adobeIms = null;
    _profile = null;
    _token = null;
}

function ims_signIn() {
    _adobeIms.signIn();
}

function ims_copyToken() {
    navigator.clipboard.writeText(_token);
}

async function initializeIMS() {
    const imsContainer = document.getElementById("ims");
    let initSuccess = false;
    imsContainer.textContent = "Initializing IMS...";

    let profile;
    try {
        profile = await ims_initialize();
        initSuccess = true;
    } catch (err) {
        imsContainer.innerHTML = "";
        const span = document.createElement("span");
        span.className = "ims-span";
        span.textContent = `IMS auth issue: ${err}`;
        imsContainer.appendChild(span);
    }

    if (initSuccess) {
        imsContainer.innerHTML = "";

        if (!profile) {
            const span = document.createElement("span");
            span.className = "ims-span";
            span.textContent = "Not signed in";
            imsContainer.appendChild(span);

            const btn = document.createElement("button");
            btn.className = "ims-button";
            btn.textContent = "Sign in";
            btn.onclick = ims_signIn;
            imsContainer.appendChild(btn);
        } else {
            const span = document.createElement("span");
            span.className = "ims-span";
            span.textContent = `Signed in as ${profile.displayName} (${profile.account_type})`;
            imsContainer.appendChild(span);

            const outBtn = document.createElement("button");
            outBtn.className = "ims-button";
            outBtn.textContent = "Sign out";
            outBtn.onclick = ims_signOut;
            imsContainer.appendChild(outBtn);

            const copyBtn = document.createElement("button");
            copyBtn.className = "ims-button";
            copyBtn.textContent = "Copy token";
            copyBtn.onclick = ims_copyToken;
            imsContainer.appendChild(copyBtn);
        }
    }

    if (initSuccess || !!_getOverridenToken()) {
        _postInit();
    }

    // Override token button (fallback)
    const overrideBtn = document.createElement("button");
    overrideBtn.className = "ims-button";
    overrideBtn.textContent = _getOverridenToken() ? "Clear overridden token" : "Override token";
    overrideBtn.onclick = () => {
        _overrideToken(_getOverridenToken() ? "" : prompt("Paste token"));
        overrideBtn.textContent = _getOverridenToken() ? "Clear overridden token" : "Override token";
    };
    imsContainer.appendChild(overrideBtn);
}

function _postInit() {
    const token = _token || _getOverridenToken();
    if (token) {
        document.cookie = `user_token=${token}; path=/asset; max-age=86400;`;
    }
    // Show content, hide loading
    document.getElementById("loading").style.display = "none";
    document.getElementById("content").classList.remove("hidden");
    if (typeof onAuthReady === "function") onAuthReady();
}

function _getOverridenToken() {
    return localStorage.getItem("overriden_token");
}

function _overrideToken(token) {
    localStorage.setItem("overriden_token", token || "");
    _postInit();
}
