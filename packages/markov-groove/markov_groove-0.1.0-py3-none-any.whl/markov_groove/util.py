"""
The util module holds various helper functions, that
are useful, when for instance preprocessing larger datasets
or reading multiple audio files.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Union

import numpy as np
from nptyping import Float32, NDArray
from pretty_midi import PrettyMIDI

from .audio_file import AudioFile
from .onset_detector import OnsetAlgorithm
from .sampler import KeyFunction, Sampler
from .sequencer import AudioSequencer, Sequencer


def create_knowledge_base(
    audios: List[AudioFile],
    onset_algo: OnsetAlgorithm,
    beats: int,
    steps: int,
    verbose: bool = False,
    keyfnc_type: KeyFunction = KeyFunction.CENTROID,
) -> Tuple[List[Sequencer], Dict[float, NDArray[Float32]]]:
    """
    Create the knowledge base from multiple files.
    Prints the File name and its bpm, as well as when a doubled key was found.
    Returns a list of sequences and the samples as dict, which can later be looked up.
    """
    sequences: List[Sequencer] = []
    samples: Dict[float, NDArray[Float32]] = {}
    for i, audio in enumerate(audios):
        if verbose:
            print("File {} has {}bpm".format(i, audio.bpm))
        sampler: Sampler = Sampler.from_audio(
            audio, onset_algorithm=onset_algo, keyfnc_type=keyfnc_type,
        )
        sequencer: AudioSequencer = AudioSequencer.from_sampler(
            sampler, audio.bpm, beats=beats, steps=steps
        )
        if verbose:
            for key in [x == y for x, y in zip(samples, sampler.samples)]:
                if key:
                    print(
                        "Found doubled key: {}! Using key of audio number {}".format(
                            key, i
                        )
                    )
        samples.update(sampler.samples)
        sequences.append(sequencer)
    return sequences, samples


def read_audio_files(path: Union[Path, str], regex: str,) -> List[AudioFile]:
    """
    Reads audio files in given folder and returns a list of AudioFile.
    For all following directories use **/*.*.
    """
    folder = Path(path)
    return [
        AudioFile.from_file(file.resolve(), int(file.parent.stem.rstrip("bpm")))
        for file in folder.glob(regex)
    ]


def read_midi_files(path: Union[Path, str], regex: str,) -> List[PrettyMIDI]:
    """
    Reads mid files in given folder and returns a list of PrettyMIDI.
    For all following directories use **/*.*.
    """
    folder = Path(path)
    return [PrettyMIDI(file.as_posix()) for file in folder.glob(regex)]


def find_closest(array: NDArray, value):
    """
    Find the closest value in an array.
    The value and the values stored in the array
    can only be of numeric nature.
    Furthermore the dtype of array and the value
    have to be the same.
    """
    idx = (np.abs(array - value)).min()
    return array[idx]


def find_closest_samples(
    sequencer: AudioSequencer, samples: Dict[float, NDArray[np.float32]]
):
    """
    Find the closest sample in a given Dictonary of samples
    by using the samples in the seqencer.
    """
    for idx, key in enumerate(sequencer.pattern):
        if not np.isnan(key):
            sequencer.pattern[idx] = find_closest(np.array(samples.keys()), key)
