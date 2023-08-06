import os
import numpy as np
import javabridge as jv
import bioformats as bf
from collections import namedtuple

ShapeTZCYX = namedtuple("Shape", ["T", "Z", "C", "Y", "X"])
"""5D shape object"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class JVM(metaclass=Singleton):
    """Java Virtual Machine pseudo-singleton.

    The Java VM can only be started once. Shutdown JVM only, if not required anymore.
    """

    started = False

    def start(self):
        """Starts the JVM
        """
        if not JVM.started:
            log_config = os.path.join(
                os.path.abspath(os.path.split(__file__)[0]), "res/log4j.properties"
            )
            args = []
            if os.path.exists(log_config):

                args.append(f"-Dlog4j.configuration=file:{log_config}")
            else:
                print("Warning: JVM(): log4j config properties not found...")

            jv.start_vm(class_path=bf.JARS, max_heap_size="8G", args=args)
            JVM.started = True

    def shutdown(self):
        if JVM.started:
            jv.kill_vm()

    def __del__(self):
        self.shutdown()


def get_numpy_pixel_type(pixel_type_int):
    """Returns the correct numpy dtype from bioformats.FormatTools integers

    Args:
        pixel_type_int (int): pixel type integer from bioformats.FormatTools

    Raises:
        RuntimeError: if pixel type not understood

    Returns:
        numpy.dtype: the pixel type
    """

    if pixel_type_int == 0:
        dype = np.int8
    elif pixel_type_int == 1:
        dtype = np.uint8
    elif pixel_type_int == 2:
        dtype = np.int16
    elif pixel_type_int == 3:
        dtype = np.uint16
    elif pixel_type_int == 4:
        dtype = np.int32
    elif pixel_type_int == 5:
        dtype = np.uint32
    elif pixel_type_int == 6:
        dtype = np.float32
    elif pixel_type_int == 7:
        dtype = np.float64
    else:
        raise RuntimeError(
            f"Error: Pixel-type '{pixel_type_int}' not understood. Must be integer in range(8)"
        )
    return dtype


def metadata(file_name):
    """Read the meta data and return the OME metadata object.
    """
    JVM().start()

    meta = bf.get_omexml_metadata(file_name)
    return bf.omexml.OMEXML(meta)


def series_count(file_name):
    """Return number of series in File

    Args:
        file_name (str): path to file

    Returns:
        int: Number of series in File
    """
    JVM().start()
    with bf.ImageReader(file_name) as reader:
        return reader.rdr.getSeriesCount()


def pixel_sizes_xyz(file_name, series=0):
    """Read physical pixel sizes in XYZ

    Args:
        file_name (str): path to file
        series (int, optional): Series. Defaults to 0.

    Returns:
        numpy.array(float): 3x1 array of pixel sizes in XYZ
    """
    meta = metadata(file_name)
    return np.asarray(
        [
            meta.image(series).Pixels.PhysicalSizeX,
            meta.image(series).Pixels.PhysicalSizeY,
            meta.image(series).Pixels.PhysicalSizeZ,
        ]
    )


def pixel_sizes_xyz_units(file_name, series=0):
    """Read physical units of XYZ

    Args:
        file_name (str): path to file
        series (int, optional): Series. Defaults to 0.

    Returns:
        numpy.array(str): 3x1 array of pixel units as string
    """
    meta = metadata(file_name)
    return np.asarray(
        [
            meta.image(series).Pixels.PhysicalSizeXUnit,
            meta.image(series).Pixels.PhysicalSizeYUnit,
            meta.image(series).Pixels.PhysicalSizeZUnit,
        ]
    )


def image_5d_iterator(file_name, rescale=False):
    """Iterate over all series with (name, data)

    Args:
        file_name (str): path to file
        rescale (bool, optional): rescale to min/max. Defaults to False.

    Yields:
        (str, numpy.array): Tuple of series name and pixel content as 5D array
    """
    JVM().start()

    meta_data = metadata(file_name)
    n_series = series_count(file_name)
    for s in range(n_series):
        name = meta_data.image(s).get_Name()
        yield name, image_5d(file_name, series=s, rescale=rescale)


def file_info(file_name):
    """Displays the name and shape of all available series in file_name

    Args:
        file_name (str): path to file
    """
    JVM().start()

    meta_data = metadata(file_name)

    with bf.ImageReader(file_name) as reader:
        n_series = reader.rdr.getSeriesCount()
        for s in range(n_series):
            reader.rdr.setSeries(s)
            shape = _get_TXCYX_shape(reader)
            name = meta_data.image(s).get_Name()

            print(f"Series {s}: {name}, {shape}")


def _get_TXCYX_shape(reader):
    z_size = reader.rdr.getSizeZ()
    y_size = reader.rdr.getSizeY()
    x_size = reader.rdr.getSizeX()
    c_size = reader.rdr.getSizeC()
    t_size = reader.rdr.getSizeT()

    return ShapeTZCYX(t_size, z_size, c_size, y_size, x_size)


def image_5d(
    file_name, series=0, rescale=False, frames=None, zslices=None, channels=None
):
    """Read a single series as 5d numpy array

    Args:
        file_name (str): path to file
        series (int, optional): series to open. Defaults to 0.
        rescale (bool, optional): rescale each plane to min/max. Defaults to False.
        frames (list[int], optional): list of frame indices to read. Defaults to None.
        zslices (list[int], optional): list of zslice indices to read. Defaults to None.
        channels (list[int], optional): list of channel indices to read. Defaults to None.

    Returns:
        numpy.array: 5d numpy array (TZCYX)
    """

    JVM().start()

    with bf.ImageReader(file_name) as reader:
        reader.rdr.setSeries(series)

        dtype = get_numpy_pixel_type(reader.rdr.getPixelType())
        t_size, z_size, c_size, y_size, x_size = _get_TXCYX_shape(reader)

        t_list = range(t_size)
        if frames is not None:
            t_list = sorted(list(set(frames) & set(t_list)))
        assert len(t_list) > 0, "Please choose at least one valid frame"

        z_list = range(z_size)
        if zslices is not None:
            z_list = sorted(list(set(zslices) & set(z_list)))
        assert len(z_list) > 0, "Please choose at least one valid z-slice"

        c_list = range(c_size)
        if channels is not None:
            c_list = sorted(list(set(channels) & set(c_list)))
        assert len(c_list) > 0, "Please choose at least one valid channel"

        img_5d = np.zeros(
            (len(t_list), len(z_list), len(c_list), y_size, x_size), dtype=dtype
        )

        for ti, t in enumerate(t_list):
            for zi, z in enumerate(z_list):
                for ci, c in enumerate(c_list):
                    img_5d[ti, zi, ci, :, :] = reader.read(
                        series=series, z=z, t=t, c=c, rescale=rescale
                    )
    return img_5d

