"""
The onset_detector module encapsulates the onset detection
of the essentia module. The enums provide easy an replicable
way to use the certain parameters, that are available for the
onset detection.
"""
from enum import Enum

import essentia as es
import essentia.standard as estd
import numpy as np
from nptyping import NDArray, Float32

from .audio_file import AudioFile


class OnsetAlgorithm(Enum):
    """
    This enum provides the names of the different
    algorithms available.
    """

    HFC = "hfc"
    COMPLEX = "complex"
    COMPLEX_PHASE = "complex_phase"
    FLUX = "flux"
    MELFLUX = "melflux"
    RMS = "rms"


class Window(Enum):
    """
    This enum provides the names of the different
    windowing functions available to be used with a the fft.
    """

    HANN = "hann"
    HANNSGCQ = "hannnsgcq"
    HAMMING = "hamming"
    TRIANGULAR = "triangular"
    SQUARE = "square"
    BLACKMANHARRIS62 = "blackmanharris62"
    BLACKMANHARRIS70 = "blackmanharris70"
    BLACKMANHARRIS74 = "blackmanharris74"
    BLACKMANHARRIS92 = "blackmanharris92"


class OnsetDetector:
    """
    This class provides the onset detection.

    Args:
        file (AudioFile): The audio file as AudioFile object.
        algo (OnsetAlgorithm): The algorithm to estimate the onsets.
        frameSize (int): Not recommended to change. Defaults to 1024.
        hopSize (int): Not recommended to change. Default to 512.
        windowfnc (Window): The function to apply to every frame.
        normalize (bool): Normalize each window. Defaults to True.

    Attributes:
        algo (str): String representation of the selected algorithm.
        onsets (NDArray[Float32]): The indcies of every onsets in seconds.

    """

    algo: str
    onsets: NDArray[Float32]
    __length: int

    def __init__(
        self,
        file: AudioFile,
        algo: OnsetAlgorithm,
        frame_size: int = 1024,  # 2 ** 10
        hop_size: int = 512,  # 2 ** 9
        windowfnc: Window = Window.HANN,
        normalize: bool = True,
    ):
        self.algo = algo.value
        self.__length = len(file)
        self.__detect_onsets(file, frame_size, hop_size, windowfnc, normalize)

    def beep(self) -> AudioFile:
        """
        Create a new AudioFile where the onsets are represented as beep.
        """
        tmp = np.zeros(self.__length, dtype="f4")
        return AudioFile(estd.AudioOnsetsMarker(onsets=self.onsets, type="beep")(tmp))

    def __detect_onsets(self, file, frame_size, hop_size, windowfnc, normalize) -> None:
        window = estd.Windowing(
            size=frame_size, type=windowfnc.value, normalized=normalize
        )
        fft = estd.FFT(size=frame_size)
        pool = es.Pool()
        pool_add = pool.add
        cart_to_polar = estd.CartesianToPolar()
        detect_onset = estd.OnsetDetection(method=self.algo)
        for frame in estd.FrameGenerator(
            file.audio, frameSize=frame_size, hopSize=hop_size
        ):
            mag, phase, = cart_to_polar(fft(window(frame)))
            pool_add(
                "features." + self.algo, detect_onset(mag, phase),
            )

        # The onsets algo expects a matrix of features which can be weighted
        self.onsets = estd.Onsets()(es.array([pool["features." + self.algo]]), [1])
