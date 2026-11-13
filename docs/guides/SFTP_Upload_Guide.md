# Foundry Customer → Adobe Secure Upload Guide (SFTP → S3)

This guide shows how to securely upload files and folders to Adobe’s S3 bucket using AWS Transfer Family (SFTP). No passwords are used; access is granted via your SSH public key.

---

## What You’ll Receive From Adobe
- SFTP endpoint (hostname), for example:
  - `s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com`
- SFTP username (e.g., `test_user`)
- Upload window (start/end time) and any special folder instructions

Do not share these with anyone outside your team.

---

## 1) Generate an SSH Key Pair (one-time)

Only send us the public key. Keep the private key safe and never email it.

### macOS / Linux
```bash
ssh-keygen -t ed25519 -f ~/.ssh/adobe_foundry_customer_sftp -C "Foundry Customer SFTP"
# Press Enter for no passphrase or set a passphrase if your policy requires it

# Show the public key (copy the entire single line)
cat ~/.ssh/adobe_foundry_customer_sftp.pub
```
Email the full contents of `~/.ssh/adobe_foundry_customer_sftp.pub` to your Adobe contact.

### Windows 10/11 (PowerShell, built-in OpenSSH)
```powershell
ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\adobe_foundry_customer_sftp -C "Foundry Customer SFTP"
Get-Content $env:USERPROFILE\.ssh\adobe_foundry_customer_sftp.pub
```
Email the printed `.pub` line only. Keep `adobe_foundry_customer_sftp` (private key) on your machine.

We will provision your SFTP user and reply back with your username and endpoint.

---

## 2) Install an SFTP Client

- macOS and most Linux distributions include `sftp` by default (OpenSSH).
- Windows: The built-in OpenSSH Client includes `sftp`. Alternatively, use GUI clients like WinSCP or FileZilla (Protocol: SFTP).
- Optional (recommended for large folders): `lftp`
  - macOS (Homebrew): `brew install lftp`
  - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y lftp`

---

## 3) Connect to the SFTP Server

Replace `USERNAME` with the one Adobe provided. Use the private key you generated.

### macOS / Linux
```bash
chmod 600 ~/.ssh/adobe_foundry_customer_sftp
sftp -o StrictHostKeyChecking=accept-new \
  -i ~/.ssh/adobe_foundry_customer_sftp \
  USERNAME@s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com
```
- On first connect, `accept-new` records the host key automatically.
- You will land in your upload directory.

### Windows (PowerShell)
```powershell
sftp -o StrictHostKeyChecking=accept-new `
  -i $env:USERPROFILE\.ssh\adobe_foundry_customer_sftp `
  USERNAME@s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com
```

Example (using a sample user):
```bash
sftp -o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 \
  hs_test_user@s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com
```

---

## 4) Upload a Single File (simple smoke test)

Inside the `sftp` prompt:
```text
sftp> put /full/path/to/local/file.ext
sftp> ls
sftp> bye
```
Example you can follow:
```bash
sftp -o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 \
  hs_test_user@s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com

sftp> put outputs/foundry_customer_prompts/images/1.png
sftp> bye
```

---

## 5) Upload an Entire Folder (two recommended methods)

### Option A: sftp (recursive)
Interactive:
```bash
sftp -o StrictHostKeyChecking=accept-new -i ~/.ssh/adobe_foundry_customer_sftp \
  USERNAME@s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com
sftp> lcd /path/to/local_folder
sftp> put -r .
sftp> bye
```

One‑shot (non‑interactive):
```bash
sftp -o StrictHostKeyChecking=accept-new -i ~/.ssh/adobe_foundry_customer_sftp \
  USERNAME@s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com << 'EOF'
lcd /path/to/local_folder
put -r .
bye
EOF
```
Notes:
- `put -r` uploads directories recursively.
- To include dotfiles, use `put -r .` after `lcd` into the folder.
- For better throughput you can increase buffers: `sftp -B 524288 -R 128 ...`

### Option B: lftp (faster, resumable, parallel)
```bash
lftp -u USERNAME,sftp://s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com << 'EOF'
set sftp:connect-program "ssh -a -x -i ~/.ssh/adobe_foundry_customer_sftp"
set net:timeout 30
set net:max-retries 100
set xfer:clobber on
mirror -R --parallel=8 --continue /path/to/local_folder .
bye
EOF
```
Flags:
- `-R` = reverse (upload local → remote)
- `--parallel=8` = upload multiple files concurrently
- `--continue` = resume partial uploads

---

## 6) GUI Clients (optional)

### FileZilla
- File → Site Manager → New Site
- Protocol: SFTP – SSH File Transfer Protocol
- Host: `s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com`
- Port: 22
- Logon Type: Key file
- User: `USERNAME`
- Key file: select your private key (e.g., `~/.ssh/adobe_foundry_customer_sftp`)
- Connect, then drag‑and‑drop folders/files.

### WinSCP
- New Session → File protocol: SFTP
- Host name: `s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com`
- Port: 22
- User name: `USERNAME`
- Advanced → SSH → Authentication → Private key file → select your private key
- Save → Login → drag‑and‑drop to upload.

---

## 7) Troubleshooting
- Permission denied (publickey):
  - Ensure you sent us the `.pub` key and we confirmed user provisioning.
  - Confirm you are using the matching private key and `chmod 600` on it (macOS/Linux).
- Connection issues/timeouts:
  - Corporate firewall may block outbound SSH (port 22); try a different network or request allow‑listing.
- Upload fails:
  - Retry with `lftp` and `--continue`.
  - If issues persist, report approximate time and filename to Adobe for log review.

---

## Security Notes
- Keep your private key private; never email it. Rotate it if you suspect compromise.
- Keys can be time‑boxed: we can disable your SFTP user after the agreed window.

---

## Support
If you need help, email your Adobe contact with:
- Your SFTP username
- Timestamp(s) of the issue (with timezone)
- The command you ran and any error output
- Filenames you were uploading

Thank you!


