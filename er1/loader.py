import glob
import calibrithm as clb

def get_expt(expt=None, day=None, idx=None, track=None):
    """
    Translate experiment id, day of observation, or track id to experiment id

    Args:
        expt:  experiment id      (3597--3601)
        day:   day of observation (1--5)
        idx:   index of the day   (0--4)
        track: track id           ('A'--'E')

    Return:
        experiment id as an integer
    """
    track_dict = {'A':3600,
                  'B':3598,
                  'C':3599,
                  'D':3597,
                  'E':3601}

    input_count = 0
    if expt  is not None:
        input_count += 1
    if idx   is not None:
        input_count += 1
        expt = min(track_dict.values()) + idx
    if day   is not None:
        input_count += 1
        expt = min(track_dict.values()) + day - 1
    if track is not None:
        input_count += 1
        expt = track_dict[track.upper()]

    if input_count == 0:
        return min(track_dict.values()) # default value
    elif input_count == 1:
        if expt in track_dict.values():
            return expt
        else:
            raise ValueError('Experiment {} is not part of the EHT '
                             '2017 observation'.format(expt))
    else:
        raise ValueError('Only one of the keywords "expt", "day", and "track" '
                         'should be specified')

def load(repos, src="sgra", band="lo",
         expt=None, day=None, idx=None, track=None,
         pipeline="hops", stage=7,
         quiet=False):

    expt = get_expt(expt=expt, day=day, idx=idx, track=track)

    if pipeline == 'hops':
        if stage < 6:
            pattern = "{}/{}-{}/{}.*/data/alist.v6".\
                format(repos, pipeline, band, stage)
        elif stage == 6:
            pattern = "{}/{}-{}/{}.*/hops_{}_{}_{}*.uvfits".\
                format(repos, pipeline, band, stage, expt, src, band)
        else:
            pattern = "{}/{}-{}/{}.*/data/hops_{}_{}_{}*.uvfits".\
                format(repos, pipeline, band, stage, expt, src, band)
    else:
        pattern = "{}/{}-v{}/e17{}*-1-{}.apcal.{}.uvfits".\
            format(repos, pipeline, stage, track, band, src)

    files = glob.glob(pattern)
    if len(files) == 1:
        file = files[0]
        if not quiet:
            print(file)
        if file.endswith(".uvfits"):
            return clb.open_uvfits(file)
        else:
            return clb.open_alist(file, expt=expt, src=src)
    else:
        raise ValueError('The pattern "{}" has multiple matches'.
                         format(pattern))

    return None
