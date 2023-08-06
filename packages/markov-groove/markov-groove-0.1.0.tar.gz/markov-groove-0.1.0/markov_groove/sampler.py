"""
The sampler module consist mainly of the
Sampler class. The Sampler class is used for
creating samples from an audio file with their onsets.
The length of each sample varies, and is limited by the next
onset index.
The KeyFunction enum is used to define the keyfunctions,
that are used to describe the samples in a numerical
way.
"""
from enum import Enum
from typing import Any, Dict, List

import essentia as es
import essentia.standard as estd
import numpy as np
from more_itertools import pairwise
from nptyping import Float32, NDArray

from .audio_file import AudioFile
from .onset_detector import OnsetAlgorithm, OnsetDetector, Window


class KeyFunction(Enum):
    """
    This enum provides the names of the different
    keyfunctions available.
    """

    CENTROID = "centroid"
    MAX = "max"
    MFCC = "mfcc"
    MELBANDS = "melbands"
    MELBANDS_LOG = "melbands_log"
    RMS = "rms"


class Sampler:
    """
    This class holds samples with their matching onset frames.
    They can be determined automatically be using the from_audio constructor.

    Args:
        onsets (List[float]): The onsets of each sample. The length of this has to match
                                the amount of the given samples.
        samples (Dict[Any, NDArray[Float32]]): The samples or audio snippets that have
                                been detetceted, when determining the onsets. The length has
                                too much the amount of the given onsets.
        sample_rate (int): The sampling rate of the samples.

    Attributes:
        onsets (List[float]): The onsets of each sample.
        samples (Dict[Any, NDArray[Float32]]): The samples.
        sample_rate (int): The sampling rate of the samples.


    """

    onsets: List[float]
    samples: Dict[Any, NDArray[Float32]]
    sample_rate: int

    def __init__(
        self, onsets: es.array, samples: Dict[float, es.array], sample_rate: int,
    ):
        self.onsets = onsets
        self.samples = samples
        self.sample_rate = sample_rate

    @classmethod
    def from_audio(
        cls,
        audio: AudioFile,
        windowfnc: Window = Window.HANN,
        onsets: es.array = None,
        onset_algorithm: OnsetAlgorithm = OnsetAlgorithm.COMPLEX,
        keyfnc_type: KeyFunction = KeyFunction.CENTROID,
    ):
        """
        Creates a sampler from a given AudioFile.
        Detects the onsets via OnsetDetector, when no onsets are given.

        Args:
        audio (AudioFile): The audio represented as AudioFile object.
        windowfnc (Window): The windowing function both used in the onset detection and
                                to estimate the key features.
        onsets (List[float]): Optional, provides additonal information for future analysis. Defaults to 0.
        samples (int): The desired sampling rate of the audio file.
                          Needs to match the sampling rate when reading from binary form.
                          Defaults to 44.1 khz
        """
        if onsets is None:
            onsets = OnsetDetector(audio, onset_algorithm).onsets

        onset_indices = (int(i) for i in onsets * audio.sample_rate)
        keys = lambda sample: _key_fnc(
            sample, int(audio.sample_rate / 2), windowfnc, keyfnc_type
        )

        frames = (
            np.append(
                audio.audio[index:next_index],
                np.zeros(len(audio.audio[index:next_index]), dtype=np.float32),
            )
            for index, next_index in pairwise(onset_indices)
        )
        samples = {keys(sample): sample for sample in frames}

        return Sampler(onsets, samples, audio.sample_rate)


def _key_fnc(
    sample: NDArray[Float32],
    frequency_rate: int,
    windowfnc: Window,
    key_type: KeyFunction,
):
    """
    This function computes the key function,
    which in return calculates the keys for the [this.samples] map.
    To calculate the spectral centroid,
    the frequency_rate should be equal to the half of the samplerate.
    """

    if key_type == KeyFunction.CENTROID:
        return _get_centroid(
            sample,
            estd.Centroid(range=frequency_rate),
            estd.Spectrum(),
            estd.Windowing(type=windowfnc.value),
        )
    if key_type == KeyFunction.MAX:
        return _get_max(sample, estd.Spectrum(), estd.Windowing(type=windowfnc.value),)
    if key_type == KeyFunction.MFCC:
        return _get_mfcc(
            sample, estd.MFCC(), estd.Spectrum(), estd.Windowing(type=windowfnc.value),
        )
    if key_type == KeyFunction.MELBANDS:
        return _get_melbands(
            sample, estd.MFCC(), estd.Spectrum(), estd.Windowing(type=windowfnc.value),
        )
    if key_type == KeyFunction.MELBANDS_LOG:
        return estd.UnaryOperator(type="log")(
            _get_melbands(
                sample,
                estd.MFCC(),
                estd.Spectrum(),
                estd.Windowing(type=windowfnc.value),
            )
        )
    raise ValueError("Keyfunction is not defined!")


def _get_centroid(sample: NDArray[Float32], centroid, spectrum, window) -> float:
    """
    Return the centroid of a sample.
    It can be used to compute the spectral or the temporal centroid.
    For more information view: https://essentia.upf.edu/reference/std_Centroid.html.
    """
    return centroid(spectrum(window(sample)))


def _get_max(sample: NDArray[Float32], spectrum, window) -> float:
    """
    This function could be used as another key, for the get_key closure.
    """
    raise NotImplementedError()


def _get_mfcc(sample: NDArray[Float32], mfcc, spectrum, window) -> float:
    """
    Return the mfcc of a sample.
    """
    return mfcc(spectrum(window(sample)))


def _get_melbands(sample: NDArray[Float32], mfcc, spectrum, window) -> float:
    """
    Return the mfcc of a sample.
    """
    raise NotImplementedError()
