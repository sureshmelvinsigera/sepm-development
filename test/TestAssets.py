import os
import sys
import unittest
import pathlib as pl

TMP_DEL = '×'
PTH_DEL = '/'


def clean_path(pth):
    pth = pth.replace('/', TMP_DEL)
    pth = pth.replace('\\', TMP_DEL)
    return pth


def list_path():
    return sys.path


def get_path(__file__):
    return os.path.abspath(os.path.dirname(__file__))


def get_root_by_name(__file__, dir_name):
    return get_specific_parent_dir(__file__, dir_name)


def get_specific_parent_dir(__file__, dir_name):
    pth = clean_path(get_path(__file__))
    dir_name = clean_path(dir_name)
    candidate = f'{TMP_DEL}{dir_name}{TMP_DEL}'
    if candidate in pth:
        pth = (pth.split(candidate)[0] + TMP_DEL +
               dir_name).replace(TMP_DEL * 2, TMP_DEL)
        return pth.replace(TMP_DEL, PTH_DEL)
    return None


def get_specific_child_dir(__file__, dir_name):
    for x in [x[0] for x in os.walk(get_path(__file__))]:
        dirName = clean_path(dir_name)
        x = clean_path(x)
        if TMP_DEL in x:
            if x.split(TMP_DEL)[-1] == dir_name:
                return x.replace(TMP_DEL, PTH_DEL)
    return None


class TestCaseBase(unittest.TestCase):
    @staticmethod
    def assert_is_file(path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))


class ActualTest(TestCaseBase):
    project_dir = get_root_by_name(__file__, 'sepm-development')

    def test_audio(self):
        audio = ['8-Bit March - Twin Musicom.mp3', "theme.wav"]
        # test for audio assets
        for i in audio:
            p = ActualTest.project_dir + "/assets/audio/" + i
            TestCaseBase.assert_is_file(p)

    def test_cars(self):
        cars = ['black-car.png', 'blue-car.png', 'green-car.png', 'red-car.png']
        # test for car assets
        for i in cars:
            p = ActualTest.project_dir + "/assets/images/cars/" + i
            TestCaseBase.assert_is_file(p)

    def test_backgrounds(self):
        backgrounds = ['dirt.png', 'grass.png', 'stone.png']
        # test for background assets
        for i in backgrounds:
            p = ActualTest.project_dir + "/assets/images/backgrounds/" + i
            TestCaseBase.assert_is_file(p)

    def test_tracks(self):
        track_1 = ['track-1.png', 'track-1-border.png']
        track_2 = ['track-2.png', 'track-2-border.png']
        finish = ['finish.png']
        # test for track-1 assets
        for i in track_1:
            p = ActualTest.project_dir + "/assets/images/tracks/track-1/" + i
            TestCaseBase.assert_is_file(p)
        # test for track-2 assets
        for j in track_2:
            p = ActualTest.project_dir + "/assets/images/tracks/track-2/" + j
            TestCaseBase.assert_is_file(p)
        # test for finish assets
        for k in finish:
            p = ActualTest.project_dir + "/assets/images/tracks/" + k
            TestCaseBase.assert_is_file(p)
