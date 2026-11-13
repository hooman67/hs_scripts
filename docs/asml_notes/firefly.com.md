## Setup Instructions

### To run locally

1.  Make sure you're on mac
2.  artifcatory
    ```bash
    export ARTFY_USER=hshariati
    export ARTFY_APIKEY=AKCp8pRjLxcs2suDvnKdyogEU76pNmcBuBXJ1zR13WCSyMJ1S8X8wwktpH6JhPFxbhUysWNwN
    ```
3.  Install npm
    ```bash
    curl -o-  [https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh](https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh) | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
    ```
4.  Make sure you use node 20
    ```bash
    nvm install 20
    nvm use 20
    ```
    * make sure:
        ```bash
        node -v
        ```
        Gives above v20 like: v20.13.1
5.  Install pnpm
    ```bash
    npm -g i pnpm
    ./scripts/onetime-setup.sh
    corepack enable pnpm
    corepack use pnpm@8.6.2
    ```
6.  Install mac dependencies
    ```bash
    brew install pkg-config cairo pango libpng jpeg giflib librsvg pixman python-setuptools
    export PKG_CONFIG_PATH="/opt/homebrew/opt/jpeg/lib/pkgconfig"
    echo 'export PATH="/opt/homebrew/opt/jpeg/bin:$PATH"' >> ~/.zshrc
    ```
    ***. I removed canvas from dependencies so that I don't have to install it:
    `/Users/hshariati/spl-web-client/packages/tests/package.json`
7.  Install the project
    ```bash
    pnpm install
    ```
8.  Start the project
    ```bash
    pnpm start
    ```
    **Its better if you do "cd packages/clio-playground" and run the "pnpm start" from there.
9.  You can access It here now
    [https://localhost.adobe.com:8080/](https://localhost.adobe.com:8080/)
10. Sign in with your LDAP
    Then login and select:
    Neal's ETLA Express Firefly
11. You can see the end point that's hit by opening chrome inspector.
12. Then under Network, filter by `ge`
13. `nerate`. And then click on the message.
14. Sd

### Change where ff.com points to:

You just need 1 file change:
[https://git.corp.adobe.com/neuralfiltersplatform/spl-web-client/pull/7125](https://git.corp.adobe.com/neuralfiltersplatform/spl-web-client/pull/7125)

`/files`