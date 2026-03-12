# Proxy Server Setup Guide

## Overview
This guide will help you set up a proxy server on your remote server (72.61.171.138) to route browser traffic through it, reducing CAPTCHA challenges.

## What We've Done
1. ✅ Added `PROXY_SERVER` and `PROXY_PORT` to `.env` file
2. ✅ Updated `server.py` to load proxy configuration
3. ✅ Modified Playwright browser to use the proxy server

## Next Steps: Set Up Proxy on Remote Server

### Option 1: Squid Proxy (Recommended)

**On your remote server (72.61.171.138), run:**

```bash
# Install Squid
sudo apt update
sudo apt install squid -y

# Configure Squid
sudo nano /etc/squid/squid.conf
```

**Add these lines to the config:**
```
http_port 8080
http_access allow all
forwarded_for delete
```

**Restart Squid:**
```bash
sudo systemctl restart squid
sudo systemctl enable squid
```

**Open firewall port:**
```bash
sudo ufw allow 8080/tcp
```

### Option 2: TinyProxy (Lightweight)

```bash
# Install TinyProxy
sudo apt update
sudo apt install tinyproxy -y

# Configure
sudo nano /etc/tinyproxy/tinyproxy.conf
```

**Update these settings:**
```
Port 8080
Allow 0.0.0.0/0
DisableViaHeader Yes
```

**Restart:**
```bash
sudo systemctl restart tinyproxy
sudo systemctl enable tinyproxy
```

### Option 3: SSH Tunnel (No proxy server needed)

If you don't want to set up a proxy server, you can use SSH tunneling:

**On your local machine:**
```powershell
# Create SSH tunnel (SOCKS proxy)
ssh -D 8080 -N user@72.61.171.138
```

**Then update `.env`:**
```
PROXY_SERVER=127.0.0.1
PROXY_PORT=8080
```

## Testing the Setup

1. **Start your Flask application:**
   ```bash
   python server.py
   ```

2. **Look for this debug message:**
   ```
   DEBUG: Using proxy server: http://72.61.171.138:8080
   ```

3. **Run a rank check** - The browser should now route through the server IP

## Troubleshooting

### If proxy connection fails:
1. Check if proxy server is running: `sudo systemctl status squid`
2. Verify firewall allows port 8080
3. Test proxy manually: `curl -x http://72.61.171.138:8080 https://google.com`

### If you still get CAPTCHAs:
1. The proxy server might need authentication
2. Consider using residential proxies
3. Add delays between requests (already implemented)

## Security Notes

⚠️ **Important:** The current setup allows open proxy access. For production:

1. **Add authentication to Squid:**
   ```bash
   sudo apt install apache2-utils
   sudo htpasswd -c /etc/squid/passwords yourusername
   ```

2. **Update Squid config:**
   ```
   auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwords
   acl authenticated proxy_auth REQUIRED
   http_access allow authenticated
   ```

3. **Update `.env` with credentials:**
   ```
   PROXY_SERVER=72.61.171.138
   PROXY_PORT=8080
   PROXY_USERNAME=yourusername
   PROXY_PASSWORD=yourpassword
   ```

## Alternative: Use the Server Directly

Instead of using a proxy, you could run the entire Flask app on the remote server. This would be more efficient and eliminate proxy overhead.

Would you like help setting that up instead?
