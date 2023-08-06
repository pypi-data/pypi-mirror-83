from abc import ABC, abstractmethod
from typing import Any, List, Union, Final, Dict

from nptyping import NDArray, Float32

from markov_groove.audio_file import AudioFile


class Sequencer(ABC):
    """
    A sequencer can be initalized by a given pattern or
    by using the Class methods from_sampler() or from_file().

    Args:
        pattern (NDArray[Any]): The audio represented in binary form as np.array of float32.
        bpm (int): The bpm of the given sequence. This is used when creating the beat.
        beats (int): The amount of beats of the sequence. If shorter than the given sequence, the 
            created beat is going to be shortend as well.
        steps (int): The resolution of every beat.

    Attributes:
        audio (NDArray[Float32]): The audio in binary form as np.array with dtype float32.
        file_path (Window): The function to apply to every frame.
        sample_rate (int): The sampling rate.
        bpm (int): The bpm. This might not be set on init and can be checked with check_bpm().
    """

    # pattern: NDArray[Any]
    # bpm: int
    # beats: int
    # steps: int

    @abstractmethod
    def create_beat(
        self, samples: Dict[float, NDArray[Float32]] = None, sample_rate: int = 44100,
    ) -> AudioFile:
        """
        Create a beat from the pattern in the sequencer.
        This method requires different parameters for every implementation of Sequencer.
        """

    @abstractmethod
    def visualize(self, ax_subplot, color: Union[NDArray, str], marker: str):
        """
        Visualize the pattern.
        """

    @classmethod
    @abstractmethod
    def decode(cls, string_pattern: List[str], bpm: int, beats: int, steps: int):
        """
        Decode the pattern of a string and create a sequencer from it.
        """

    @abstractmethod
    def encode(self) -> List[str]:
        """
        Encode the pattern in a string.
        """
