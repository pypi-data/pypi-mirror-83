from typing import Dict, Final, List, Union, Tuple

import numpy as np
from matplotlib.ticker import FuncFormatter, MultipleLocator
from mido import bpm2tempo, second2tick, tempo2bpm, tick2second
from nptyping import Float32, NDArray
from pretty_midi import Instrument, Note, PrettyMIDI, note_number_to_drum_name

from ..audio_file import AudioFile
from .sequencer import Sequencer

# Standard values for note creation
_VELOCITY: Final[int] = 100
_NOTE_DURATION: Final[float] = 0.5


class MidiSequencer(Sequencer):
    """
    See the docs of Sequencer.
    """

    pattern: Final[NDArray[Note]]
    bpm: Final[int]
    beats: Final[int]
    steps: Final[int]

    def __init__(
        self, pattern: NDArray[Note], bpm: int, beats: int, steps: int,
    ):
        self.pattern = pattern
        self.bpm = bpm
        self.beats = beats
        self.steps = steps

    @classmethod
    def from_file(
        cls, mid: PrettyMIDI, bpm: int, beats: int = 8, steps: int = 16,
    ):
        ppqn = int(np.round(steps / 4))
        end_tick = beats * steps

        drum_track = _find_drum_track(mid)
        # Allocate the array
        pattern = np.empty((128, int(end_tick + 1)), dtype=np.object)
        pattern.fill(None)
        # Add up notes
        for note in drum_track.notes:
            note_start_tick = int(
                np.round(second2tick(note.start, ppqn, bpm2tempo(bpm)))
            )
            if note_start_tick <= end_tick:
                pattern[note.pitch, note_start_tick] = note
        return cls(pattern, bpm, beats, steps)

    def create_beat(
        self, samples: Dict[float, NDArray[Float32]] = None, sample_rate: int = 44100,
    ) -> AudioFile:
        """
        Create a beat from the pattern in the sequencer.
        """
        if samples is not None:
            raise ValueError(
                "Samples are not needed to create a beat for an MidiSequencer!"
            )
        mid = PrettyMIDI(initial_tempo=self.bpm)
        drum_track = Instrument(program=0, is_drum=True, name="drums")
        mid.instruments.append(drum_track)
        for row in self.pattern:
            for note in row:
                if note is not None:
                    drum_track.notes.append(note)
        return AudioFile(
            np.array(mid.fluidsynth(fs=sample_rate), dtype=np.float32),
            self.bpm,
            sample_rate,
        )

    @classmethod
    def decode(cls, string_pattern: List[str], bpm: int, beats: int, steps: int):
        """
        Decode the pattern of a string list and create a sequencer from it.
        """
        ppqn = int(np.round(steps / 4))
        end_tick = beats * steps
        # Allocate the array
        pattern = np.empty((128, len(string_pattern)), dtype=np.object)
        pattern.fill(None)
        for start_tick, string in enumerate(string_pattern):
            for pitch in _string_to_pitch(string):
                if start_tick <= end_tick:
                    start_seconds = tick2second(start_tick, ppqn, bpm2tempo(bpm))
                    pattern[pitch, start_tick] = Note(
                        _VELOCITY, pitch, start_seconds, start_seconds + _NOTE_DURATION
                    )

        return cls(pattern, bpm, beats, steps)

    @classmethod
    def decode2(cls, string_pattern: List[str], bpm: int, beats: int, steps: int):
        """
        Decode the pattern of a string list and create a sequencer from it.
        """
        ppqn = int(np.round(steps / 4))
        end_tick = beats * steps
        # Allocate the array
        pattern = np.empty((128, len(string_pattern)), dtype=np.object)
        pattern.fill(None)
        for string in string_pattern:
            for pitch, start_tick in _string_to_tuples(string):
                if start_tick <= end_tick:
                    start_seconds = tick2second(start_tick, ppqn, bpm2tempo(bpm))
                    pattern[pitch, start_tick] = Note(
                        _VELOCITY, pitch, start_seconds, start_seconds + _NOTE_DURATION
                    )

        return cls(pattern, bpm, beats, steps)

    def encode(self) -> List[str]:
        """
        Encode the pattern in a list of strings.
        """
        string_list = ["" for _ in range(self.pattern.shape[-1])]
        for pitch, row in enumerate(self.pattern):
            for start_tick, note in enumerate(row):
                if note is not None:
                    string_list[start_tick] += f"{pitch};"
        return string_list

    def encode2(self) -> List[str]:
        """
        Encode the pattern in a list of strings.
        """
        string_list = ["" for _ in range(self.pattern.shape[-1])]
        for pitch, row in enumerate(self.pattern):
            for start_tick, note in enumerate(row):
                if note is not None:
                    string_list[start_tick] += f"{pitch},{start_tick};"
        return string_list

    def visualize(self, ax_subplot, color: Union[NDArray, str], marker: str = "2"):
        """
        Visualize the pattern.
        """
        x_length = np.arange(0, self.pattern.shape[-1])
        for note_row in self.pattern:
            values = [note.pitch if note is not None else np.nan for note in note_row]
            ax_subplot.scatter(x_length, values, color=color, marker=marker)
        ax_subplot.yaxis.set_major_formatter(
            FuncFormatter(lambda tick, pos: note_number_to_drum_name(tick))
        )
        ax_subplot.xaxis.set_major_locator(MultipleLocator(base=self.steps))
        return ax_subplot


def _find_drum_track(mid: PrettyMIDI) -> Instrument:
    """
    Gets the first occurrence of a drum track in a PrettyMIDI file.
    """
    for instrument in mid.instruments:
        if instrument.is_drum:
            return instrument
    raise ValueError("No drum track found!")


def _string_to_tuples(string: str) -> List[Tuple[int, float]]:
    arguments = string.split(";")
    return [_string_to_tuple(x) for x in arguments if x]


def _string_to_tuple(string: str) -> Tuple[int, float]:
    arguments = string.split(",")
    return int(arguments[0]), int(arguments[1])  # pitch, start_tick


def _string_to_pitch(string: str) -> List[int]:
    arguments = string.split(";")
    return [int(x) for x in arguments if x]
