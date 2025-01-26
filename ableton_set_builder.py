import xmltodict
import json
import os
import gzip
from typing import List, Dict, Any

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
