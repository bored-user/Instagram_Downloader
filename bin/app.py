#!/usr/bin/python3

import sys
import requests
import json
import urllib.request
import os

def handleProfile(page):
    page = json.loads(page.content)["graphql"]
    name = str(page["user"]["username"])
    is_private = str(page["user"]["is_private"])

    print("Bio: " + str(page["user"]["biography"]))
    print("Seguidores: " + str(page["user"]["edge_followed_by"]["count"]))
    print("Seguindo: " + str(page["user"]["edge_follow"]["count"]))
    print("Nome completo: " + str(page["user"]["full_name"]))
    print("ID: " + str(page["user"]["id"]))
    print("Conta business: " + str(page["user"]["is_business_account"]))
    print("Conta privada: " + is_private)
    print("URL da foto de perfil: " + str(page["user"]["profile_pic_url_hd"]))
    print("Username: " + name)
    print("Facebook conectado: " + str(page["user"]["connected_fb_page"]) + "\n")
    if is_private:
        if input("Baixar as todas as fotos/ videos (Y/N)? ").upper() == "Y":
            if not os.path.isdir(name):
                os.makedirs(name)
            for i in range(len(page["user"]["edge_felix_video_timeline"]["edges"]) - 1):
                media = page["user"]["edge_felix_video_timeline"]["edges"][i]["node"]
                extension = "." + str(media["display_url"]).split("?")[0].split(".")[len(str(media["display_url"]).split("?")[0].split(".")) - 1]
                urllib.request.urlretrieve(str(media["display_url"]), name + "/EFVT_photo_" + str(i) + extension)

            for i in range(len(page["user"]["edge_owner_to_timeline_media"]["edges"]) - 1):
                media = page["user"]["edge_owner_to_timeline_media"]["edges"][i]["node"]
                extension = "." + str(media["display_url"]).split("?")[0].split(".")[len(str(media["display_url"]).split("?")[0].split(".")) - 1]
                urllib.request.urlretrieve(str(media["display_url"]), name + "/EOTM_photo_" + str(i) + extension)

            for i in range(len(page["user"]["edge_saved_media"]["edges"]) - 1):
                media = page["user"]["edge_saved_media"]["edges"][i]["node"]
                extension = "." + str(media["display_url"]).split("?")[0].split(".")[len(str(media["display_url"]).split("?")[0].split(".")) - 1]
                urllib.request.urlretrieve(str(media["display_url"]), name + "/ESM_photo_" + str(i) + extension)

            for i in range(len(page["user"]["edge_media_collections"]["edges"]) - 1):
                media = page["user"]["edge_media_collections"]["edges"][i]["node"]
                extension = "." + str(media["display_url"]).split("?")[0].split(".")[len(str(media["display_url"]).split("?")[0].split(".")) - 1]
                urllib.request.urlretrieve(str(media["display_url"]), name + "/EMC_photo_" + str(i) + extension)


def getProfile(profile):
    if "https://www.instagram.com/" in profile and not "?__a=1" in profile:
        if "/" in profile:
            page = requests.get(profile + "?__a=1")
        else:
            page = requests.get(profile + "/?__a=1")
    elif not "https://www.instagram.com/" in profile and "?__a=1" in profile:
        page = requests.get("https://www.instagram.com/" + profile)
    elif "https://www.instagram.com/" in profile and "?__a=1" in profile:
        page = requests.get(profile)
    else:
        page = requests.get("https://www.instagram.com/" + profile + "?__a=1")
    handleProfile(page)

def main():
    if len(sys.argv) > 1:
        sys.argv.pop(0)
        if len(sys.argv) > 1:
            for profile in sys.argv:
                getProfile(profile)
        else:
            getProfile(sys.argv[0])
    else:
        par = input("Profile(s): ").split(",")
        if isinstance(par, list):
            for profile in par:
                getProfile(profile)
        else:
            getProfile(par)

if __name__ == "__main__":
    main()