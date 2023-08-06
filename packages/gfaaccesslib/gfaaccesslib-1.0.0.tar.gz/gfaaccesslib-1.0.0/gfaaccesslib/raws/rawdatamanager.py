import numpy as np

import numpy

from numpy import (amin, amax, ravel, asarray, arange, ones, newaxis,
                   transpose, iscomplexobj, uint8)

try:
    from PIL import Image, ImageFilter
except ImportError:
    import Image
    import ImageFilter

def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value


def bytescale(data, cmin=None, cmax=None, high=255, low=0):
    if data.dtype == uint8:
        return data

    if high > 255:
        raise ValueError("`high` should be less than or equal to 255.")
    if low < 0:
        raise ValueError("`low` should be greater than or equal to 0.")
    if high < low:
        raise ValueError("`high` should be greater than or equal to `low`.")

    if cmin is None:
        cmin = data.min()
    if cmax is None:
        cmax = data.max()

    cscale = cmax - cmin
    if cscale < 0:
        raise ValueError("`cmax` should be larger than `cmin`.")
    elif cscale == 0:
        cscale = 1

    scale = float(high - low) / cscale
    bytedata = (data - cmin) * scale + low
    return (bytedata.clip(low, high) + 0.5).astype(uint8)


_errstr = "Mode is unknown or incompatible with input array shape."


def toimage(arr, high=255, low=0, cmin=None, cmax=None, pal=None,
            mode=None, channel_axis=None):
    """Takes a numpy array and returns a PIL image.

    This function is only available if Python Imaging Library (PIL) is installed.

    The mode of the PIL image depends on the array shape and the `pal` and
    `mode` keywords.

    For 2-D arrays, if `pal` is a valid (N,3) byte-array giving the RGB values
    (from 0 to 255) then ``mode='P'``, otherwise ``mode='L'``, unless mode
    is given as 'F' or 'I' in which case a float and/or integer array is made.

    .. warning::

        This function uses `bytescale` under the hood to rescale images to use
        the full (0, 255) range if ``mode`` is one of ``None, 'L', 'P', 'l'``.
        It will also cast data for 2-D images to ``uint32`` for ``mode=None``
        (which is the default).

    Notes
    -----
    For 3-D arrays, the `channel_axis` argument tells which dimension of the
    array holds the channel data.

    For 3-D arrays if one of the dimensions is 3, the mode is 'RGB'
    by default or 'YCbCr' if selected.

    The numpy array must be either 2 dimensional or 3 dimensional.

    """
    data = asarray(arr)
    if iscomplexobj(data):
        raise ValueError("Cannot convert a complex-valued array.")
    shape = list(data.shape)
    valid = len(shape) == 2 or ((len(shape) == 3) and
                                ((3 in shape) or (4 in shape)))
    if not valid:
        raise ValueError("'arr' does not have a suitable array shape for "
                         "any mode.")
    if len(shape) == 2:
        shape = (shape[1], shape[0])  # columns show up first
        if mode == 'F':
            data32 = data.astype(numpy.float32)
            image = Image.frombytes(mode, shape, data32.tostring())
            return image
        if mode in [None, 'L', 'P']:
            bytedata = bytescale(data, high=high, low=low,
                                 cmin=cmin, cmax=cmax)
            image = Image.frombytes('L', shape, bytedata.tostring())
            if pal is not None:
                image.putpalette(asarray(pal, dtype=uint8).tostring())
                # Becomes a mode='P' automagically.
            elif mode == 'P':  # default gray-scale
                pal = (arange(0, 256, 1, dtype=uint8)[:, newaxis] *
                       ones((3,), dtype=uint8)[newaxis, :])
                image.putpalette(asarray(pal, dtype=uint8).tostring())
            return image
        if mode == '1':  # high input gives threshold for 1
            bytedata = (data > high)
            image = Image.frombytes('1', shape, bytedata.tostring())
            return image
        if cmin is None:
            cmin = amin(ravel(data))
        if cmax is None:
            cmax = amax(ravel(data))
        data = (data * 1.0 - cmin) * (high - low) / (cmax - cmin) + low
        if mode == 'I':
            data32 = data.astype(numpy.uint32)
            image = Image.frombytes(mode, shape, data32.tostring())
        else:
            raise ValueError(_errstr)
        return image

    # if here then 3-d array with a 3 or a 4 in the shape length.
    # Check for 3 in datacube shape --- 'RGB' or 'YCbCr'
    if channel_axis is None:
        if (3 in shape):
            ca = numpy.flatnonzero(asarray(shape) == 3)[0]
        else:
            ca = numpy.flatnonzero(asarray(shape) == 4)
            if len(ca):
                ca = ca[0]
            else:
                raise ValueError("Could not find channel dimension.")
    else:
        ca = channel_axis

    numch = shape[ca]
    if numch not in [3, 4]:
        raise ValueError("Channel axis dimension is not valid.")

    bytedata = bytescale(data, high=high, low=low, cmin=cmin, cmax=cmax)
    if ca == 2:
        strdata = bytedata.tostring()
        shape = (shape[1], shape[0])
    elif ca == 1:
        strdata = transpose(bytedata, (0, 2, 1)).tostring()
        shape = (shape[2], shape[0])
    elif ca == 0:
        strdata = transpose(bytedata, (1, 2, 0)).tostring()
        shape = (shape[2], shape[1])
    if mode is None:
        if numch == 3:
            mode = 'RGB'
        else:
            mode = 'RGBA'

    if mode not in ['RGB', 'RGBA', 'YCbCr', 'CMYK']:
        raise ValueError(_errstr)

    if mode in ['RGB', 'YCbCr']:
        if numch != 3:
            raise ValueError("Invalid array shape for mode.")
    if mode in ['RGBA', 'CMYK']:
        if numch != 4:
            raise ValueError("Invalid array shape for mode.")

    # Here we know data and mode is correct
    image = Image.frombytes(mode, shape, strdata)
    return image


class RawDataManager(object):
    def __init__(self, amplifiers=4):
        self._images = {}
        self._row_callbacks = []
        self.num_amps = amplifiers

    def rem_image(self, image_id):
        return self._images.pop(image_id, None)

    def get_image(self, image_id):
        im = self._images.get(image_id, None)
        if im is None:
            im = RawDataImage(image_id, parent=self)
            self._images[image_id] = im
        return im

    def list_images(self):
        return self._images.keys()

    # def register_row_callback(self, callback, kwargs={}):
    #     """
    #     register a function to be executed as a callback when a new row is ready to be accessed
    #     :param callback: function with at least one argument called amp_rows
    #     :param kwargs: any other argument the function may need
    #     :return:
    #     """
    #     self._row_callbacks.append((callback, kwargs))
    #
    # def exec_row_callbacks(self, amp_rows):
    #     """
    #     execute sequentially all registered callbacks
    #     :param amp_rows: list of RawDataAmpRow
    #     :return:
    #     """
    #     for cb, kwargs in self._row_callbacks:
    #         cb(amp_rows=amp_rows, **kwargs)


class RawDataImage(object):
    def __init__(self, image_id, parent):
        self._image_id = image_id
        self.parent = parent
        self.amplifiers = []
        for ix in range(self.parent.num_amps):
            self.amplifiers.append(RawDataAmplifier(ix, parent=self))
        self._meta = {}
        self._ampdata = None

    @property
    def meta(self):
        return self._meta

    def _get_im_id(self):
        return self._image_id
    image_id = property(_get_im_id)

    def add_meta(self, key, value):
        self._meta[key] = value

    def update_meta(self, meta_dict):
        self._meta.update(meta_dict)

    def get_rows(self, ccd_row_init, ccd_row_end):
        """
        get a set of rows
        :param ccd_row_init:
        :param ccd_row_end:
        :return:
        """
        return [amp.get_rows(ccd_row_init, ccd_row_end) for amp in self.amplifiers]

    def get_ampdata(self, image_id=None):
        """
            Returns 4 numpy arrays one per amplifier with 0,0 being pixel closest to the readout amplifier.
        """
        if self._ampdata is None:
            self._ampdata = []
            for amp in self.amplifiers:
                if not amp.rows:
                    continue
                if amp.check_rows_shape() is False:
                    raise Exception("Not all rows have same size")
                data = np.vstack([el.data for el in amp.rows])
                # data = np.array(amp.rows[0].data)
                # for j in range(1, len(amp.rows)):
                #     data = np.vstack((data, amp.rows[j].data))
                self._ampdata.append(data)
        return self._ampdata

    def get_ampdata_prescan_avg(self, prescan_cols, remove_border=0):
        if remove_border == 0:
            return [np.average(x[:, :prescan_cols]) for x in self.get_ampdata(None)]
        return [np.average(x[remove_border:-remove_border, remove_border:prescan_cols-remove_border]) for x in self.get_ampdata(None)]

    def get_ampdata_prescan_std(self, prescan_cols, remove_border=0):
        if remove_border == 0:
            return [np.std(x[:, :prescan_cols]) for x in self.get_ampdata(None)]
        return [np.std(x[remove_border:-remove_border, remove_border:prescan_cols-remove_border]) for x in self.get_ampdata(None)]

    def get_ampdata_overscan_avg(self, overscan_cols, remove_border=0):
        if remove_border == 0:
            return [np.average(x[:, -overscan_cols:]) for x in self.get_ampdata(None)]
        return [np.average(x[remove_border:-remove_border, remove_border-overscan_cols:-remove_border]) for x in self.get_ampdata(None)]

    def get_ampdata_overscan_std(self, overscan_cols, remove_border=0):
        if remove_border == 0:
            return [np.std(x[:, -overscan_cols:]) for x in self.get_ampdata(None)]
        return [np.std(x[remove_border:-remove_border, remove_border-overscan_cols:-remove_border]) for x in self.get_ampdata(None)]

    def get_ampdata_avg(self, col_start, col_end, row_start, row_end):
        return [np.average(x[col_start:col_end, row_start:row_end]) for x in self.get_ampdata(None)]

    def get_ampdata_std(self, col_start, col_end, row_start, row_end):
        return [np.std(x[col_start:col_end, row_start:row_end]) for x in self.get_ampdata(None)]

    def get_ampdata_shape(self):
        return [x.shape for x in self.get_ampdata()]


    def get_im(self):
        images = []

        for amp in self.amplifiers:
            if not amp.rows:
                continue
            if amp.check_rows_shape() is False:
                raise Exception("Not all rows have same size")
            ndata = np.concatenate(amp.data)
            ndata.shape = len(amp.rows), amp.rows[0].data.size
            images.append(toimage(ndata))

        return images
    
    def show_im(self):
        for im in self.get_im():
            im.show()            

    def _check_fake_2(self):
        # All amplifiers and rows should have same size
        size = self.amplifiers[0].rows[0].data.size

        # not all amplifiers have same data
        for ix, amp in enumerate(self.amplifiers):
            comparer = np.ones(size) * ix * 1000
            for row in amp.rows:
                if np.array_equal(comparer, row.data) is False:
                    # print row.data
                    raise Exception('Error on fake image')
        return True

    def _check_fake_4(self):
        # All amplifiers and rows should have same size
        size = self.amplifiers[0].rows[0].data.size

        # not all amplifiers have same data
        cmp_array = np.empty(size)
        for ix, amp in enumerate(self.amplifiers):
            for row in amp.rows:
                cmp_array.fill(row.meta.get("ccd_row_num", -1))
                comparer = np.array(cmp_array, dtype=int)
                if np.array_equal(comparer, row.data) is False:
                    print(row.meta)
                    print(row.data)
                    print(comparer)
                    raise Exception('Error on fake image')
        return True

    def check_fake_im(self, mode):
        # -----------------------------------------------------------------------------
        # -- datamode
        # --  0: output zeros
        # --  1: output ones
        # --  2: e: 0, f: 1000, g: 2000, h: 3000
        # --  3: e: row + col, f: row + col + 1000, g: row + col + 2000, h: row + col + 3000
        # --  4: pixel value = row
        # --  5: pixel value = column
        # --  6: pixel value = row
        # x
        # col
        # --  7: output is a
        # checker
        # 2
        # x2(TBI)
        # -----------------------------------------------------------------------------

        # All amplifiers and rows should have same size
        size = self.amplifiers[0].rows[0].data.size

        if mode == 0:
            comparer = np.zeros(size)
        elif mode == 1:
            comparer = np.ones(size)
        elif mode == 2:
            return self._check_fake_2()
        elif mode == 3:
            return self._check_fake_3()
        elif mode == 4:
            return self._check_fake_4()
        elif mode == 5:
            comparer = np.array(range(1, size + 1))
            for amp in self.amplifiers:
                for row in amp.rows:
                    inc_1 = [y == (x + 1) for x, y in zip(row.data, row.data[1:])]
                    product = reduce((lambda x, y: x * y), inc_1)
                    if product is False:
                        print("row is not monotonically increasing")
        else:
            raise Exception('Bad mode')
        rowerr = []
        for amp in self.amplifiers:
            for row in amp.rows:
                if np.array_equal(comparer, row.data) is False:
                    print(row.meta, len(row.data), row.data)
                    rowerr = row.data
        if len(rowerr) > 0:
            for x in rowerr:
                print(x)
            raise Exception('Error on fake image')
        return True


class RawDataAmplifier(object):
    def __init__(self, amp_id, parent):
        self.amp_id = amp_id
        self.keywords = {}
        self.rows = []
        self.parent = parent

    def _get_data(self):
        return [row.data for row in self.rows]
    data = property(_get_data)

    def _get_matrix(self):
        return np.matrix(self.data)
    matrix = property(_get_matrix)

    def check_rows_shape(self):
        sizes = [row.data.size for row in self.rows]
        return max(sizes) == min(sizes)

    def get_im_shape(self):
        sizes = [row.data.size for row in self.rows]
        return len(self.rows), min(sizes)

    def add_row(self, data, meta):
        """
        add a new row of raw data
        :param data: list of uints
        :param meta: dictionary of metadata. At least it must contains 'image_id', 'row_num', 'row_width'
        :return: RawDataAmpRow instance
        """
        row = RawDataAmpRow(data, meta)
        self.rows.append(row)
        return row

    def get_rows(self, ccd_row_init, ccd_row_end):
        """
        Return list of rows
        :param row_init: Index of lowest row to return. Index referred to ccd position
        :param row_end: Index of highest row to return. Index referred to ccd position
        :return: list of RawDataRow
        """
        return [el for el in self.rows if (not el.ccd_row > ccd_row_end and not el.ccd_row < ccd_row_init)]


class RawDataAmpRow(object):
    def __init__(self, data, meta={}):
        self.data = np.array(data)
        self.meta = meta

    def _get_ccd_row(self):
        return self.meta.get('ccd_row_num', -1)

    ccd_row = property(_get_ccd_row)

if __name__ == '__main__':


    def callback1(amp_rows):
        print('callback 1')

    def callbackwithargs(caller_id, amp_rows):
        print("callback with arguments: {0} - {1}".format(caller_id, amp_rows))

    man = RawDataManager()
    man.register_row_callback(callback=callback1)
    man.register_row_callback(callback=callbackwithargs, kwargs={'caller_id': 1})

    image = man.get_image(1)
    rows = []
    for amp in image.amplifiers:
        r = amp.add_row(data=range(5), meta={})
        rows.append(r)

    man.exec_row_callbacks(rows)
