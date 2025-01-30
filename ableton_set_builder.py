import xmltodict
import json
import os
import gzip
from enum import Enum
from typing import List, Dict, Any

class ColorsDir(Enum):
    salmon = {id: 0, hex: "#fe9aaa"}
    frank_orange = {id: 1, hex: "#fea741"}
    dirty_gold = {id: 2, hex: "#d19d3a"}
    lemonade = {id: 3, hex: "#f7f58c"}
    lime = {id: 4, hex: "#c1fc40"}
    highlighter_green = {id: 5, hex: "#2dfe50"}
    bianchi = {id: 6, hex: "#34feaf"}
    turquiose = {id: 7, hex: "#65ffea"}
    sky_blue = {id: 8, hex: "#90c7fc"}
    sapphire = {id: 9, hex: "#5c86e1"}
    periwinkle = {id: 10, hex: "#97abfb"}
    orchid = {id: 11, hex: "#d975e2"}
    magenta = {id: 12, hex: "#e55ca2"}
    white = {id: 13, hex: "#ffffff"}
    fire_hydrant_red = {id: 14, hex: "#fe3e40"}
    tangerine = {id: 15, hex: "#f76f23"}
    sand = {id: 16, hex: "#9f7752"}
    sunshine_yellow = {id: 17, hex: "#fff054"}
    terminal_green = {id: 18, hex: "#8dff79"}
    forest = {id: 19, hex: "#42c52e"}
    tiffany_blue = {id: 20, hex: "#11c2b2"}
    cyan = {id: 21, hex: "#28e9fd"}
    cerulean = {id: 22, hex: "#1aa6eb"}
    united_nations_blue = {id: 23, hex: "#5c86e1"}
    amethyst = {id: 24, hex: "#8e74e2"}
    iris = {id: 25, hex: "#ba81c7"}
    flamingo = {id: 26, hex: "#fe41d1"}
    aluminium = {id: 27, hex: "#d9d9d9"}
    terracotta = {id: 28, hex: "#e26f64"}
    light_salmon = {id: 29, hex: "#fea67e"}
    whiskey = {id: 30, hex: "#d6b27f"}
    canary = {id: 31, hex: "#eeffb7"}
    primrose = {id: 32, hex: "#d6e6a6"}
    wild_willow = {id: 33, hex: "#bfd383"}
    dark_sea_green = {id: 34, hex: "#a4c99a"}
    honeydew = {id: 35, hex: "#d9fde5"}
    pale_turquiose = {id: 36, hex: "#d2f3f9"}
    light_periwinkle = {id: 37, hex: "#c2c9e6"}
    fog = {id: 38, hex: "#d3c4e5"}
    dull_lavender = {id: 39, hex: "#b5a1e4"}
    whisper = {id: 40, hex: "#eae3e7"}
    silver_chalice = {id: 41, hex: "#b3b3b3"}
    dusty_pink = {id: 42, hex: "#cb9b96"}
    barley_corn = {id: 43, hex: "#bb8862"}
    pale_oyster = {id: 44, hex: "#9f8a75"}
    dark_khaki = {id: 45, hex: "#c3be78"}
    pistachio = {id: 46, hex: "#a9c12f"}
    dollar_bill = {id: 47, hex: "#84b45d"}
    neptune = {id: 48, hex: "#93c7c0"}
    nepal = {id: 49, hex: "#a5bbc9"}
    polo_blue = {id: 50, hex: "#8facc5"}
    vista_blue = {id: 51, hex: "#8d9ccd"}
    amethyst_smoke = {id: 52, hex: "#ae9fbb"}
    lilac = {id: 53, hex: "#c6a9c4"}
    turkish_rose = {id: 54, hex: "#bf7a9c"}
    steel = {id: 55, hex: "#838383"}
    medium_carmine = {id: 56, hex: "#b53637"}
    red_orche = {id: 57, hex: "#ae5437"}
    coffee = {id: 58, hex: "#775345"}
    durian_yellow = {id: 59, hex: "#dec633"}
    pomelo_green = {id: 60, hex: "#899b31"}
    apple = {id: 61, hex: "#57a53f"}
    aquamarine = {id: 62, hex: "#139f91"}
    sea_blue = {id: 63, hex: "#256686"}
    cosmic_cobalt = {id: 64, hex: "#1a3096"}
    dark_sapphire = {id: 65, hex: "#3155a4"}
    plump_purple = {id: 66, hex: "#6751ae"}
    purpureus = {id: 67, hex: "#a752af"}
    fuchsia_rose = {id: 68, hex: "#ce3571"}
    eclipse = {id: 69, hex: "#3f3f3f"}

class AbletonSetBuilder:
    def __init__(self, template_path: str):
        self.load_template(template_path)
        self.tracks = self.doc["Ableton"]["LiveSet"]["Tracks"]
        self.audio_tracks: List[Dict[str, Any]] = []
        self.midi_tracks: List[Dict[str, Any]] = []
        self.audio_tracks_first_clips: List[Dict[str, Any]] = []
        self.midi_tracks_first_clips: List[Dict[str, Any]] = []
        self.master_track = self.doc["Ableton"]["LiveSet"]["MasterTrack"]
        
        self.initialize_tracks()

    def load_template(self, template_path: str):
        if os.path.splitext(template_path)[1] == '.als':
            with gzip.open(template_path, 'rb') as f:
                self.doc = xmltodict.parse(f.read())
        elif os.path.splitext(template_path)[1] == '.xml':
            with open(template_path) as fd:
                self.doc = xmltodict.parse(fd.read())
        else:
            raise ValueError("Invalid file format. Please provide an .als or .xml file.")

    def initialize_tracks(self):
        # Handle audio tracks
        if isinstance(self.tracks["AudioTrack"], list):
            self.audio_tracks = self.tracks["AudioTrack"]
        else:
            self.audio_tracks = [self.tracks["AudioTrack"]]
        
        # Handle MIDI tracks
        if isinstance(self.tracks["MidiTrack"], list):
            self.midi_tracks = self.tracks["MidiTrack"]
        else:
            self.midi_tracks = [self.tracks["MidiTrack"]]
        
        # Get first clips for audio and MIDI tracks
        for audio_track in self.audio_tracks:
            audio_track_first_clip = audio_track["DeviceChain"]["MainSequencer"]["ClipSlotList"]["ClipSlot"]
            self.audio_tracks_first_clips.append(audio_track_first_clip)
        
        for midi_track in self.midi_tracks:
            midi_track_first_clip = midi_track["DeviceChain"]["MainSequencer"]["ClipSlotList"]["ClipSlot"]
            self.midi_tracks_first_clips.append(midi_track_first_clip)

    def create_clip_slot(self, id: int, lom_id: int, has_stop: str, need_refreeze: str) -> Dict[str, Any]:
        return {
            "@Id": str(id),
            "LomId": {
                "@Value": str(lom_id)
            },
            "ClipSlot": {
                "Value": None
            },
            "HasStop": {
                "@Value": has_stop
            },
            "NeedRefreeze": {
                "@Value": need_refreeze
            }
        }

    def create_scene(self, id: int, name: str, annotation: str, color: int, tempo: int, time_signature_id: int) -> Dict[str, Any]:
        scene = {
            "@Id": str(id),
            "FollowAction": {
                "FollowTime": {"@Value": "4"},
                "IsLinked": {"@Value": "true"},
                "LoopIterations": {"@Value": "1"},
                "FollowActionA": {"@Value": "4"},
                "FollowActionB": {"@Value": "0"},
                "FollowChanceA": {"@Value": "100"},
                "FollowChanceB": {"@Value": "0"},
                "JumpIndexA": {"@Value": "1"},
                "JumpIndexB": {"@Value": "1"},
                "FollowActionEnabled": {"@Value": "false"}
            },
            "Name": {"@Value": name},
            "Annotation": {"@Value": annotation},
            "Color": {"@Value": str(color)},
            "Tempo": {"@Value": str(tempo)},
            "IsTempoEnabled": {"@Value": "true"},
            "TimeSignatureId": {"@Value": str(time_signature_id)},
            "IsTimeSignatureEnabled": {"@Value": "true"},
            "LomId": {"@Value": "0"},
            "ClipSlotsListWrapper": {"@LomId": "0"}
        }
        return scene

    def clear_track(self, track: Dict[str, Any]):
        track["DeviceChain"]["MainSequencer"]["ClipSlotList"]["ClipSlot"] = []
        track["DeviceChain"]["FreezeSequencer"]["ClipSlotList"]["ClipSlot"] = []

    def add_clip_to_track(self, track: Dict[str, Any], clip: Dict[str, Any]):
        # check if clip is not a list:
        if not isinstance(track["DeviceChain"]["MainSequencer"]["ClipSlotList"]["ClipSlot"], list):
            track["DeviceChain"]["MainSequencer"]["ClipSlotList"]["ClipSlot"] = [track["DeviceChain"]["MainSequencer"]["ClipSlotList"]["ClipSlot"]]
        
        if not isinstance(track["DeviceChain"]["FreezeSequencer"]["ClipSlotList"]["ClipSlot"], list):
            track["DeviceChain"]["FreezeSequencer"]["ClipSlotList"]["ClipSlot"] = [track["DeviceChain"]["FreezeSequencer"]["ClipSlotList"]["ClipSlot"]]
        track["DeviceChain"]["MainSequencer"]["ClipSlotList"]["ClipSlot"].append(clip)
        track["DeviceChain"]["FreezeSequencer"]["ClipSlotList"]["ClipSlot"].append(clip)

    def add_scene(self, id: int, name: str, annotation: str = "", color: int = -1, tempo: int = 120, time_signature_id: int = 201):
        new_scene = self.create_scene(id, name, annotation, color, tempo, time_signature_id)
        self.doc["Ableton"]["LiveSet"]["Scenes"]["Scene"].append(new_scene)
        
        # Add clip slots to tracks for this scene
        for track in self.audio_tracks + self.midi_tracks:
            self.add_clip_to_track(track, self.create_clip_slot(id, 0, "true", "true"))

    def add_template_scene(self, scene_id: int, scene_name: str, color: int = -1, tempo: int = 120):
        # Create a new scene
        new_scene = self.create_scene(scene_id, scene_name, "", color, tempo, 201)
        
        # Add the scene to the scenes list
        if "Scene" not in self.doc["Ableton"]["LiveSet"]["Scenes"]:
            self.doc["Ableton"]["LiveSet"]["Scenes"]["Scene"] = []
        # check if scene is not a list:
        if not isinstance(self.doc["Ableton"]["LiveSet"]["Scenes"]["Scene"], list):
            self.doc["Ableton"]["LiveSet"]["Scenes"]["Scene"] = [self.doc["Ableton"]["LiveSet"]["Scenes"]["Scene"]]
        
        self.doc["Ableton"]["LiveSet"]["Scenes"]["Scene"].append(new_scene)
        
        # Add the first clips of the audio and midi tracks to the scene
        for i, audio_track_first_clip in enumerate(self.audio_tracks_first_clips):
            new_clip = audio_track_first_clip.copy()
            new_clip["@Id"] = str(scene_id)
            self.add_clip_to_track(self.audio_tracks[i], new_clip)
        
        for i, midi_track_first_clip in enumerate(self.midi_tracks_first_clips):
            new_clip = midi_track_first_clip.copy()
            new_clip["@Id"] = str(scene_id)
            self.add_clip_to_track(self.midi_tracks[i], new_clip)
    
    def clearScenes(self):
        self.doc["Ableton"]["LiveSet"]["Scenes"]["Scene"] = []
        # self.clear_track(self.master_track)
        
        for audio_track in self.audio_tracks:
            self.clear_track(audio_track)
        for midi_track in self.midi_tracks:
            self.clear_track(midi_track)

    def build_als(self, output_path: str):
        xml_path = os.path.splitext(output_path)[0] + '.xml'
        with open(xml_path, 'w') as f:
            xmltodict.unparse(self.doc, output=f, pretty=True)
        os.rename(xml_path, output_path)

# Example usage
if __name__ == "__main__":
    builder = AbletonSetBuilder('test.xml')
    builder.add_scene(1, "Scene 1", color=5, tempo=125)
    builder.add_template_scene(1, "Template Scene", color=9, tempo=130)
    builder.build_als('./output/new-live-set-v2.als')
