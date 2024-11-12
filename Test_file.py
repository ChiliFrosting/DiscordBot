#Test code blocks for twitch api outside of Bot framework 

#This approach is robust in its simplicity although not the inteneded way to check status 
#Pros: simple, no fuss

#Cons: simple, will have to check manually if channel is live
#      overhead, potential resource hog
#      impractical, if set to check on a schedule it will have to be adjusted manually for changes 
import requests

channel = "noxious_tgs"

contents = requests.get("https://www.twitch.tv/"+channel).content.decode("utf-8")

if "isLiveBroadcast" in contents:
    print(f"{channel} is live!")
else:
    print(f"{channel} is offline!")