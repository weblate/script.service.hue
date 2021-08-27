import datetime

import requests
import xbmc
import xbmcgui

from resources.lib import CACHE, reporting, hue
from resources.lib.settings import convert_time
from resources.lib.qhue import QhueException
from . import ADDON
 
from .language import get_string as _

STATE_STOPPED = 0
STATE_PLAYING = 1
STATE_PAUSED = 2

VIDEO = 1
AUDIO = 2
ALL_MEDIA = 3


class LightGroup(xbmc.Player):
    def __init__(self, light_group_id, bridge, media_type, flash=False, initial_state=STATE_STOPPED):
        self.light_group_id = light_group_id
        self.bridge = bridge
        self.enabled = ADDON.getSettingBool(f"group{self.light_group_id}_enabled")

        self.start_behavior = ADDON.getSettingBool(f"group{self.light_group_id}_startBehavior")
        self.start_scene = ADDON.getSettingString(f"group{self.light_group_id}_startSceneID")

        self.pause_behavior = ADDON.getSettingBool(f"group{self.light_group_id}_pauseBehavior")
        self.pause_scene = ADDON.getSettingString(f"group{self.light_group_id}_pauseSceneID")

        self.stop_behavior = ADDON.getSettingBool(f"group{self.light_group_id}_stopBehavior")
        self.stop_scene = ADDON.getSettingString(f"group{self.light_group_id}_stopSceneID")

        self.state = initial_state

        self.media_type = media_type
        self.lights = self.bridge.lights
        self.group0 = self.bridge.groups[0]

        if flash:
            self.flash()

        super().__init__()

    def __repr__(self):
        return f"light_group_id: {self.light_group_id}, enabled: {self.enabled}, state: {self.state}"

    def flash(self):
        # xbmc.log("[script.service.hue] in KodiGroup Flash")
        try:
            self.group0.action(alert="select")
        except QhueException as exc:
            xbmc.log(f"[script.service.hue] Hue call fail: {exc.type_id}: {exc.message}")
            reporting.process_exception(exc)
        except requests.RequestException as exc:
            xbmc.log(f"[script.service.hue] RequestException: {exc}")

    def onAVStarted(self):
        if self.enabled:
            xbmc.log(
                "In KodiGroup[{}], onPlaybackStarted. Group enabled: {},startBehavior: {} , isPlayingVideo: {}, isPlayingAudio: {}, self.mediaType: {},self.playbackType(): {}".format(
                    self.light_group_id, self.enabled, self.start_behavior, self.isPlayingVideo(), self.isPlayingAudio(),
                    self.media_type, self.playback_type()))
            self.state = STATE_PLAYING
            self.last_media_type = self.playback_type()

            if self.isPlayingVideo() and self.media_type == VIDEO:  # If video group, check video activation. Otherwise it's audio so ignore this and check other conditions.
                try:
                    self.video_info_tag = self.getVideoInfoTag()
                except Exception as exc:
                    xbmc.log(f"[script.service.hue] Get InfoTag Exception: {exc}")
                    reporting.process_exception(exc)
                    return
                # xbmc.log("[script.service.hue] InfoTag: {}".format(self.videoInfoTag))
                if not self.check_video_activation(self.video_info_tag):
                    return
            else:
                self.video_info_tag = None

            if (self.check_active_time() or self.check_already_active(self.start_scene)) and self.check_keep_lights_off_rule(self.start_scene) and self.start_behavior and self.media_type == self.playback_type():
                self.run_play()

    def onPlayBackStopped(self):
        if self.enabled:
            xbmc.log(f"[script.service.hue] In KodiGroup[{self.light_group_id}], onPlaybackStopped() , mediaType: {self.media_type}, lastMediaType: {self.last_media_type} ")
            self.state = STATE_STOPPED

            try:
                if self.media_type == VIDEO and not self.check_video_activation(
                        self.video_info_tag):  # If video group, check video activation. Otherwise it's audio so ignore this and check other conditions.
                    return
            except AttributeError:
                xbmc.log("[script.service.hue] No videoInfoTag")

            if (self.check_active_time() or self.check_already_active(self.stop_scene)) and self.check_keep_lights_off_rule(self.stop_scene) and self.stop_behavior and self.media_type == self.last_media_type:
                self.run_stop()

    def onPlayBackPaused(self):
        if self.enabled:
            xbmc.log(f"[script.service.hue] In KodiGroup[{self.light_group_id}], onPlaybackPaused() , isPlayingVideo: {self.isPlayingVideo()}, isPlayingAudio: {self.isPlayingAudio()}")
            self.state = STATE_PAUSED

            if self.media_type == VIDEO and not self.check_video_activation(
                    self.video_info_tag):  # If video group, check video activation. Otherwise it's audio so we ignore this and continue
                return

            if (self.check_active_time() or self.check_already_active(self.pause_scene)) and self.check_keep_lights_off_rule(self.pause_scene) and self.pause_behavior and self.media_type == self.playback_type():
                self.last_media_type = self.playback_type()
                self.run_pause()

    def onPlayBackResumed(self):
        # xbmc.log("[script.service.hue] In KodiGroup[{}], onPlaybackResumed()".format(self.light_group_id))
        self.onAVStarted()

    def onPlayBackError(self):
        # xbmc.log("[script.service.hue] In KodiGroup[{}], onPlaybackError()".format(self.light_group_id))
        self.onPlayBackStopped()

    def onPlayBackEnded(self):
        # xbmc.log("[script.service.hue] In KodiGroup[{}], onPlaybackEnded()".format(self.light_group_id))
        self.onPlayBackStopped()

    def run_play(self):
        try:
            self.group0.action(scene=self.start_scene)
        except QhueException as exc:
            xbmc.log(f"[script.service.hue] onAVStarted: Hue call fail: {exc.type_id}: {exc.message}")
            if exc.type_id == 7:
                xbmc.log("[script.service.hue] Scene not found")
                hue.notification(_("Hue Service"), _("ERROR: Scene not found"), icon=xbmcgui.NOTIFICATION_ERROR)
            else:
                reporting.process_exception(exc)

    def run_pause(self):
        try:
            xbmc.sleep(500)  # sleep for any left over ambilight calls to complete first.
            self.group0.action(scene=self.pause_scene)
            # xbmc.log("[script.service.hue] In KodiGroup[{}], onPlaybackPaused() Pause scene activated")
        except QhueException as exc:
            xbmc.log(f"[script.service.hue] run_pause Hue call fail: {exc.type_id}: {exc.message}")
            if exc.type_id == 7:
                xbmc.log("[script.service.hue] Scene not found")
                hue.notification(_("Hue Service"), _("ERROR: Scene not found"), icon=xbmcgui.NOTIFICATION_ERROR)
            else:
                reporting.process_exception(exc)

    def run_stop(self):
        try:
            xbmc.sleep(100)  # sleep for any left over ambilight calls to complete first.
            self.group0.action(scene=self.stop_scene)
            xbmc.log("[script.service.hue] In KodiGroup[{}], onPlaybackStop() Stop scene activated")
        except QhueException as exc:
            xbmc.log(f"[script.service.hue] onPlaybackStopped: Hue call fail: {exc.type_id}: {exc.message}")
            if exc.type_id == 7:
                xbmc.log("[script.service.hue] Scene not found")
                hue.notification(_("Hue Service"), _("ERROR: Scene not found"), icon=xbmcgui.NOTIFICATION_ERROR)
            else:
                reporting.process_exception(exc)

    def activate(self):
        xbmc.log(f"[script.service.hue] Activate group [{self.light_group_id}]. State: {self.state}")
        xbmc.sleep(200)
        if self.state == STATE_PAUSED:
            self.onPlayBackPaused()
        elif self.state == STATE_PLAYING:
            self.onAVStarted()
        else:
            # if not playing and activate is called, probably should do nothing.
            xbmc.log(f"[script.service.hue] Activate group [{self.light_group_id}]. playback stopped, doing nothing. ")

    def playback_type(self):
        if self.isPlayingVideo():
            media_type = VIDEO
        elif self.isPlayingAudio():
            media_type = AUDIO
        else:
            media_type = None
        return media_type

    @staticmethod
    def check_active_time():
        service_enabled = CACHE.get("script.service.hue.service_enabled")
        daylight = CACHE.get("script.service.hue.daylight")
        # xbmc.log("[script.service.hue] Schedule: {}, daylightDisable: {}, daylight: {}, startTime: {}, endTime: {}".format(ADDON.getSettingBool("enableSchedule"), ADDON.getSettingBool("daylightDisable"), daylight, ADDON.getSettingBool("startTime"),
        #         ADDON.getSettingBool("endTime")))

        if ADDON.getSettingBool("daylightDisable") and daylight:
            xbmc.log("[script.service.hue] Disabled by daylight")
            return False

        if service_enabled:
            if ADDON.getSettingBool("enableSchedule"):
                start = convert_time(ADDON.getSettingBool("startTime"))
                end = convert_time(ADDON.getSettingBool("endTime"))
                now = datetime.datetime.now().time()
                if (now > start) and (now < end):
                    # xbmc.log("[script.service.hue] Enabled by schedule")
                    return True
                # xbmc.log("[script.service.hue] Disabled by schedule")
                return False
            # xbmc.log("[script.service.hue] Schedule not enabled")
            return True

        # xbmc.log("[script.service.hue] Service disabled")
        return False

    def check_video_activation(self, info_tag):
        try:
            duration = info_tag.getDuration() / 60  # returns seconds, convert to minutes
            media_type = info_tag.getMediaType()
            file_name = info_tag.getFile()
            if not file_name and self.isPlayingVideo():
                file_name = self.getPlayingFile()
            #
            # if not fileName and previousFileName:
            #     fileName = previousFileName
            # elif fileName:
            #     previousFileName = fileName

            # xbmc.log("[script.service.hue] InfoTag contents: duration: {}, mediaType: {}, file: {}".format(duration, mediaType, fileName))
        except AttributeError:
            xbmc.log("[script.service.hue] Can't read infoTag")
            return False
        # xbmc.log("Video Activation settings({}): minDuration: {}, Movie: {}, Episode: {}, MusicVideo: {}, PVR : {}, Other: {}".format(self.light_group_id, settings_storage['videoMinimumDuration'], settings_storage['video_enableMovie'],
        #                settings_storage['video_enableEpisode'], settings_storage['video_enableMusicVideo'], settings_storage['video_enablePVR'], settings_storage['video_enableOther']))
        # xbmc.log("[script.service.hue] Video Activation ({}): Duration: {}, mediaType: {}, ispvr: {}".format(self.light_group_id, duration, mediaType, fileName[0:3] == "pvr"))
        if ((duration >= ADDON.getSettingInt("video_MinimumDuration") or file_name[0:3] == "pvr") and
                ((ADDON.getSettingBool("video_Movie") and media_type == "movie") or
                 (ADDON.getSettingBool("video_Episode") and media_type == "episode") or
                 (ADDON.getSettingBool("video_MusicVideo") and media_type == "MusicVideo") or
                 (ADDON.getSettingBool("video_PVR") and file_name[0:3] == "pvr") or
                 (ADDON.getSettingBool("video_Other") and media_type != "movie" and media_type != "episode" and media_type != "MusicVideo" and file_name[0:3] != "pvr"))):
            xbmc.log("[script.service.hue] Video activation: True")
            return True
        xbmc.log("[script.service.hue] Video activation: False")
        return False

    def check_already_active(self, scene):
        if not scene:
            return False

        xbmc.log(f"[script.service.hue] Check if scene light already active, settings: enable {ADDON.getSettingBool('enable_if_already_active')}")
        if ADDON.getSettingBool("enable_if_already_active"):
            try:
                scene_data = self.bridge.scenes[scene]()
                for light in scene_data["lights"]:
                    l = self.bridge.lights[light]()
                    if l["state"]["on"]:  # one light is on, the scene can be applied
                        # xbmc.log("[script.service.hue] Check if scene light already active: True")
                        return True
                # xbmc.log("[script.service.hue] Check if scene light already active: False")
            except QhueException as exc:
                xbmc.log(f"[script.service.hue] checkAlreadyActive: Hue call fail: {exc.type_id}: {exc.message}")

        return False

    def check_keep_lights_off_rule(self, scene):
        if not scene:
            return True

        xbmc.log(f"[script.service.hue] Check if lights should stay off, settings: enable {ADDON.getSettingBool('keep_lights_off')}")
        if ADDON.getSettingBool("keep_lights_off"):
            try:
                scene_data = self.bridge.scenes[scene]()
                for light in scene_data["lights"]:
                    l = self.bridge.lights[light]()
                    if l["state"]["on"] is False:  # one light is off, the scene should not be applied
                        xbmc.log("[script.service.hue] Check if lights should stay off: True")
                        return False
                xbmc.log("[script.service.hue] Check if lights should stay off: False")
            except QhueException as exc:
                xbmc.log(f"[script.service.hue] checkKeepLightsOffRule: Hue call fail: {exc.type_id}: {exc.message}")

        return True