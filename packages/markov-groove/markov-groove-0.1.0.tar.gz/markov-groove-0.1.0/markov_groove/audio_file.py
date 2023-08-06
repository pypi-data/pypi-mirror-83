"""
This module consist solely of the AudioFile class.
"""
from pathlib import Path

import essentia as es
import essentia.standard as estd
import numpy as np
from IPython.display import Audio
from nptyping import Float32, NDArray


class AudioFile:
    """
    This class loads up audio files, regardless of their filetype and sampling rate.
    Downmixes stereo audio files to mono files resamples them to the given rate.
    When initiating with an array, make sure the sampling rate is correct.

    Args:
        audio (NDArray[Float32]): The audio represented in binary form as np.array of float32.
        bpm (int): Optional, provides additional information for future analysis. Defaults to 0.
        sample_rate (int): The desired sampling rate of the audio file.
                            Needs to match the sampling rate when reading from binary form.
                            Defaults to 44.1 khz

    Attributes:
        audio (NDArray[Float32]): The audio in binary form as np.array with dtype float32.
        file_path (Window): The function to apply to every frame.
        sample_rate (int): The sampling rate.
        bpm (int): The bpm. This might not be set on init and can be checked with check_bpm().
    """

    # The margin is used in check_bpm.
    # It lengthens short files, in order to improve the estimation.
    # The factor is a constant factor, which shows the best results.
    __MARGIN_FACTOR = 15

    audio: NDArray[Float32]
    file_path: Path
    sample_rate: int
    __bpm: float
    __margin: int

    def __init__(
        self, audio: NDArray[Float32], bpm: int = 0, sample_rate: int = 44100
    ) -> None:
        self.__bpm = float(bpm)
        self.sample_rate = sample_rate
        self.__margin = self.__MARGIN_FACTOR * sample_rate
        self.audio = audio

    @classmethod
    def from_file(cls, file_path: Path, bpm: int = 0, sample_rate: int = 44100):
        """
        Create a new AudioFile object from a file.
        """
        file = cls(None, bpm, sample_rate)
        file.file_path = file_path
        file.audio = estd.MonoLoader(
            filename=file_path.as_posix(), sampleRate=sample_rate
        )()
        return file

    def __abs__(self) -> float:
        """
        Returns the length of the audio in seconds.
        """
        return len(self.audio) / self.sample_rate

    def __len__(self) -> int:
        """
        Returns the length of the audio in samples.
        """
        return len(self.audio)

    @property
    def bpm(self) -> int:
        """
        Returns the bpm as integer value.
        """
        return int(self.__bpm)

    def check_bpm(self) -> float:
        """
        This method runs an analyzer to determine the BPM.
        If the audio is shorter then the setted time margin,
        it is append multiple times with itself
        to make up for the missing data and increase accuracy.
        """
        temp = self.audio
        if len(temp) < self.__margin:
            factor = int(np.round(self.__margin / len(temp)))
            temp = np.tile(temp, factor)
        rhythm_extractor = estd.RhythmExtractor2013()
        self.__bpm = rhythm_extractor(temp)[0]
        return self.__bpm

    def display(self, autoplay: bool = False):
        """
        Display a given audio through IPython. Useful when using in notebooks.
        """
        return Audio(data=self.audio, rate=self.sample_rate, autoplay=autoplay)

    def mix(self, snd, right: bool = True) -> None:
        """
        Mix the given audio to the right(default) channel.
        """
        if right:
            self.audio = estd.StereoMuxer()(self.audio, snd.audio)
        else:
            self.audio = estd.StereoMuxer()(snd.audio, self.audio)

    def normalize(self) -> None:
        """
        Normalize the audio, by scaling the raw audio
        between one and minus one.
        """
        self.audio = self.audio - np.mean(self.audio)
        self.audio = self.audio / np.max(self.audio) - np.min(self.audio)

    def save(self, file_path: Path = Path.cwd() / ".temp" / "audio.wav") -> None:
        """
        Export the AudioFile at the newly given path.
        """
        try:
            file_path.parent.mkdir()
        except FileExistsError:
            pass
        if len(self.audio.shape) != 2:
            estd.MonoWriter(
                filename=file_path.as_posix(),
                format=file_path.suffix[1:],
                sampleRate=self.sample_rate,
            )(self.audio)
        else:
            estd.AudioWriter(
                filename=file_path.as_posix(),
                format=file_path.suffix[1:],
                sampleRate=self.sample_rate,
            )(self.audio)
