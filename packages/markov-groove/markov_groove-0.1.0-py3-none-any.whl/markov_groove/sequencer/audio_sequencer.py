from typing import Any, Dict, Final, List, Union

import essentia as es
import numpy as np
from matplotlib.ticker import EngFormatter, MultipleLocator
from nptyping import Float32, NDArray

from ..audio_file import AudioFile
from ..onset_detector import OnsetAlgorithm, OnsetDetector
from ..sampler import Sampler
from .sequencer import Sequencer


class AudioSequencer(Sequencer):
    """
    See the docs of Sequencer.
    """

    pattern: Final[NDArray[Float32]]
    bpm: Final[int]
    beats: Final[int]
    steps: Final[int]

    def __init__(
        self, pattern: NDArray[float], bpm: int, beats: int, steps: int,
    ) -> None:
        self.pattern = pattern
        self.bpm = bpm
        self.beats = beats
        self.steps = steps
        self.__update_values()

    @classmethod
    def from_sampler(
        cls, sampler: Sampler, bpm: int, beats: int = 8, steps: int = 16,
    ):
        """
        Create a sequencer with an audio sampler by creating the pattern from it.
        """
        step_width = 60 / bpm / steps
        step_amount = beats * steps
        pattern = _get_pattern_from_sampler(sampler, step_width, step_amount)
        return cls(pattern, bpm, beats, steps)

    def create_beat(
        self, samples: Dict[float, NDArray[Float32]] = None, sample_rate: int = 44100,
    ) -> AudioFile:
        """
        Create a beat from the given samples,
        which have to match the length of occurrences in the pattern.
        """
        if samples is None:
            raise ValueError(
                "Samples are needed to create a beat for an AudioSequencer!"
            )
        if len(samples) != np.sum(np.isfinite(self.pattern)):
            raise ValueError("Number of samples does not match with amount of hits!")

        step_length = int(np.round(self.__step_width * sample_rate))
        loop_length = int(
            np.round(self.__step_amount * self.__step_width * sample_rate)
        )
        zeros = np.zeros(loop_length, dtype=np.float32)
        zeros_step = np.zeros(step_length, dtype=np.float32)
        raw_audio = np.zeros(loop_length, dtype=np.float32)
        sample_index = 0
        for idx, freq in enumerate(self.pattern):
            if not np.isnan(freq):
                tmp = np.tile(zeros_step, int(idx))
                tmp = np.append(tmp, samples[sample_index])
                tmp = np.append(tmp, zeros)
                raw_audio += tmp[:loop_length]
                sample_index += 1

        return AudioFile(raw_audio, bpm=self.bpm)

    @classmethod
    def decode(cls, string_pattern: List[str], bpm: int, beats: int, steps: int):
        """
        Decodes the pattern of a string and create a sequencer from it.
        """
        pattern = np.empty((len(string_pattern)), dtype=np.float32)
        for idx, string in enumerate(string_pattern):
            pattern[idx] = np.float32(string)
        return cls(pattern, bpm, beats, steps)

    def encode(self) -> List[str]:
        """
        Encodes the pattern in a string.
        """
        return [f"{freq}" for freq in self.pattern]

    def visualize(self, ax_subplot, color: Union[NDArray, str], marker: str = "+"):
        """
        Visualize the pattern.
        """
        x_length = np.arange(0, len(self.pattern))
        ax_subplot.set(yscale="log")
        formatter = EngFormatter(unit="Hz")
        ax_subplot.yaxis.set_major_formatter(formatter)
        ax_subplot.yaxis.set_minor_formatter(formatter)
        ax_subplot.grid(b=True, which="both")
        ax_subplot.xaxis.set_major_locator(MultipleLocator(base=self.steps))
        return ax_subplot.scatter(x_length, self.pattern, color=color, marker=marker)

    def __update_values(self) -> None:
        self.__step_width = 60 / self.bpm / self.steps
        self.__step_amount = self.beats * self.steps


def _get_pattern_from_sampler(
    sampler: Sampler, step_width, step_amount,
) -> NDArray[Float32]:
    time_line = np.linspace(0, step_width * step_amount, step_amount + 1)
    onset_indices = _find_indices(sampler.onsets, step_width, time_line)
    pattern = np.full(time_line.shape, np.nan, dtype=np.float32)
    for idx, key_value in zip(onset_indices, sampler.samples):
        pattern[idx] = key_value

    return pattern


def _find_indices(
    onsets: es.array, step_width: float, time_line: List[float]
) -> List[int]:
    onset_indices: List[int] = []
    append = onset_indices.append
    onset_iter = iter(onsets)
    onset = next(onset_iter)
    for time_index, time in enumerate(time_line):
        if time - (step_width / 2) <= onset <= time + (step_width / 2):
            append(time_index)
            try:
                onset = next(onset_iter)
            except StopIteration:
                break
    return onset_indices
