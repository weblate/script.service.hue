#      Copyright (C) 2019 Kodi Hue Service (script.service.hue)
#      This file is part of script.service.hue
#      SPDX-License-Identifier: MIT
#      See LICENSE.TXT for more information.

# Based upon: https://raw.githubusercontent.com/Quihico/handy.stuff/master/language.py
# https://forum.kodi.tv/showthread.php?tid=268081&highlight=generate+.po+python+gettext
# generated by language_gen.py


from . import STRDEBUG, ADDON, xbmc

_strings = {}


def get_string(t):
    string_id = _strings.get(t.lower())
    if not string_id:
        xbmc.log(f"[script.service.hue] LANGUAGE: missing translation for '{t.lower()}'")
        return t

    if STRDEBUG:
        return f"STR:{string_id} {ADDON.getLocalizedString(string_id)}"

    return ADDON.getLocalizedString(string_id)


# GENERATED
_strings['video scenes'] = 32100
_strings['audio scenes'] = 32102
_strings['start/resume'] = 32201
_strings['pause'] = 32202
_strings['stop'] = 32203
_strings['scene:'] = 30036
_strings['scene id'] = 32511
_strings['select...'] = 32512
_strings['bridge'] = 30500
_strings['discover hue bridge / enter ip'] = 30501
_strings['bridge ip'] = 30502
_strings['bridge user'] = 30503
_strings['enable schedule (24h format)'] = 30505
_strings['start time:'] = 30506
_strings['end time:'] = 30507
_strings['disable during daytime'] = 30508
_strings['activate during playback at sunset'] = 30509
_strings['general'] = 30510
_strings['schedule'] = 30511
_strings['scenes'] = 30512
_strings['play scene enabled'] = 30513
_strings['pause scene enabled'] = 30514
_strings['stop scene enabled'] = 30515
_strings['disable time check if any light already on'] = 30516
_strings['don\'t enable scene if any light is off'] = 30517
_strings['[b][i]warning: not supported on all hardware[/b][/i]'] = 30521
_strings['cpu & hue performance'] = 30522
_strings['ambilight'] = 30523
_strings['advanced'] = 32101
_strings['video activation rules'] = 32106
_strings['select lights'] = 6101
_strings['enabled'] = 30520
_strings['press connect button on hue bridge'] = 9001
_strings['hue service'] = 30000
_strings['check your bridge and network'] = 30004
_strings['hue connected'] = 30006
_strings['bridge not found'] = 30008
_strings['user not found'] = 30010
_strings['complete!'] = 30011
_strings['cancelled'] = 30013
_strings['select hue lights...'] = 30015
_strings['found bridge: '] = 30017
_strings['discover bridge...'] = 30018
_strings['bridge connection failed'] = 30021
_strings['discovery started'] = 30022
_strings['bridge not configured'] = 30023
_strings['check hue bridge configuration'] = 30024
_strings['cancel'] = 30034
_strings['lights:'] = 30035
_strings['save'] = 30037
_strings['fade time (seconds)'] = 30042
_strings['error'] = 30043
_strings['connection lost. check settings. shutting down'] = 30047
_strings['n-upnp discovery...'] = 30050
_strings['upnp discovery...'] = 30051
_strings['searching for bridge...'] = 30005
_strings['invalid start or end time, schedule disabled'] = 30052
_strings['set brightness on start'] = 30056
_strings['light names:'] = 30058
_strings['update interval (ms)'] = 30065
_strings['hue transition time (ms)'] = 30066
_strings['frame capture size'] = 30067
_strings['show hue bridge capacity errors'] = 30068
_strings['minimum duration (minutes)'] = 30800
_strings['enable for movies'] = 30801
_strings['enable for tv episodes'] = 30802
_strings['enable for music videos'] = 30803
_strings['enable for other videos (discs)'] = 30804
_strings['enable for live tv'] = 30805
_strings['saturation'] = 30809
_strings['minimum brightness'] = 30810
_strings['maximum brightness'] = 30811
_strings['average image processing time:'] = 30813
_strings['on playback stop'] = 30814
_strings['resume light state'] = 30815
_strings['resume transition time (secs.)'] = 30816
_strings['only colour lights are supported'] = 30071
_strings['unsupported hue bridge'] = 30072
_strings['disabled'] = 30055
_strings['play'] = 30060
_strings['hue status: '] = 30061
_strings['settings'] = 30062
_strings['disabled by daytime'] = 30063
_strings['error: scene not found, it may have been deleted'] = 30064
_strings['the following error occurred:'] = 30080
_strings['automatically report this error?'] = 30081
_strings['no lights selected for ambilight.'] = 30069
_strings['ok'] = 30070
_strings['hue bridge over capacity'] = 30075
_strings['network not ready'] = 30076
_strings['the hue bridge is over capacity. increase refresh rate or reduce the number of ambilights.'] = 30077
_strings['bridge not found[cr]check your bridge and network.'] = 30078
_strings['press link button on bridge. waiting for 90 seconds...'] = 30082
_strings['unknown'] = 30083
_strings['user found![cr]saving settings...'] = 30084
_strings['user not found[cr]check your bridge and network.'] = 30086
_strings['do not show again'] = 30073
_strings['hue bridge v1 (round) is unsupported. hue bridge v2 (square) is required.'] = 30001
_strings['unknown colour gamut for light:'] = 30012
_strings['report errors'] = 30016
_strings['never report errors'] = 30020
_strings['hue service error'] = 30032
_strings['connection error'] = 30029
_strings['error: lights incompatible with ambilight'] = 30014
_strings['bridge not found automatically. please make sure your bridge is up to date and has access to the internet. [cr]would you like to enter your bridge ip manually?'] = 30007
_strings['connecting...'] = 30009
_strings['bridge outdated. please update your bridge.'] = 30019
_strings['reconnected'] = 30033
_strings['morning disable time:'] = 31334
_strings['transition time (seconds):'] = 31335
_strings['bridge overloaded, stopping ambilight'] = 30002
_strings['bridge unauthorized, please reconfigure.'] = 30025
_strings['connection failed, retrying...'] = 30026
_strings['not selected'] = 30003
_strings['error: light not found, it may have been deleted'] = 30027
