import logging
import datetime
import pickle
import os
import os.path
from collections import Iterable

import numpy as np
from astropy.io import fits

log = logging.getLogger(__name__)


class RawImageMetadata (object):
    def __init__(self, columns, storage, active, overscan, prescan, exptime, gfa_id, ccd_serial):
        self.columns = columns
        self.num_rows = storage + active
        self.storage_rows = storage
        self.active_rows = active
        self.overscan = overscan
        self.prescan = prescan
        self.exptime = exptime
        self.gfa_id = gfa_id
        self.ccd_id = ccd_serial


class RawRepresentation:

    def __init__(self, raw_image):
        self._im = raw_image

    def get_matrix(self):
        e = np.flipud(self._im.amplifiers[0].matrix)
        f = np.flipud(np.fliplr(self._im.amplifiers[1].matrix))
        g = np.fliplr(self._im.amplifiers[2].matrix)
        h = self._im.amplifiers[3].matrix
        log.debug('E,F,G,H shapes: {0}, {1}, {2}, {3}'.format(e.shape, f.shape, g.shape, h.shape))
        try:
            if len(f) == 1 and len(g) == 1:
                top = h
                bottom = e
            elif len(h) == 1 and len(e) == 1:
                top = g
                bottom = f
            else:
                top = np.concatenate((h, g), axis=1)
                bottom = np.concatenate((e, f), axis=1)
        except Exception as ex:
            log.exception('Exception when concatenating matrices')
            now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
            unique_fn = '/tmp/gfaaccesslib_im_dump_{0}.pickle'.format(now)
            with open(unique_fn, 'wb') as f:
                try:
                    pickle.dump(self._im, f)
                    log.info("Saved image object to {0}".format(unique_fn))
                except pickle.PickleError:
                    log.exception("Exception when dumping image to pickle")
                    pass
            raise ex

        return np.concatenate((top, bottom), axis=0)

    def get_avg(self):
        matrix = self.get_matrix()

        light_avg = np.array(matrix).astype(np.uint16)
        bias_avg = np.right_shift(matrix, 16).astype(np.uint16)

        return light_avg, bias_avg

    def get_light(self):
        matrix = self.get_matrix()

        light_samples = np.right_shift(matrix, 24).astype(np.uint8)
        light_sum = np.bitwise_and(matrix, 0x00ffffff)

        return light_samples, light_sum

    def get_bias(self):
        matrix = self.get_matrix()

        bias_samples = np.right_shift(matrix, 24).astype(np.uint8)
        bias_sum = np.bitwise_and(matrix, 0x00ffffff)

        return bias_samples, bias_sum


class RawPixel(object):
    # -- 15:0 => adc_data
    # -- 18:16 => acq lines
    # -- 19 => start pixel
    # -- 20 =>  clk_phase_info(0) <= i_clk_rg;
    # -- 21 => clk_phase_info(1) <= i_clk_r01;
    # -- 22 => clk_phase_info(2) <= i_clk_r02;
    # -- 23 => clk_phase_info(3) <= i_clk_r03;
    # -- 24 => clk_phase_info(4) <= '1' when sm_current = state_hor_rg else '0'; -- reset phase
    # -- 25 => clk_phase_info(5) <= '1' when sm_current = state_hor_settle_reference
    # --                               or sm_current = state_hor_acq_reference else '0'; -- reference phase
    # -- 26 => clk_phase_info(6) <= '1' when sm_current = state_hor_settle_signal
    # --                               or sm_current = state_hor_acq_signal else '0'; -- signal phase
    # -- 27 => clk_phase_info(7) <= in_roi_range when cmd_read_roi = '1' else -- capture data in raw mode
    # --                            in_roi_range or in_overscan_range when cmd_roi_plus_overscan = '1' else
    # --                            i_acq_debug_current_pixel when i_debug_cmd = '1' else
    # --                            serial_register_shift;
    def __init__(self, pix_value):
        self.pix = pix_value

    @property
    def adc_counts(self):
        return self.pix & 0xffff

    @property
    def acq_signal(self):
        return (self.pix & 1 << 16) >> 16

    @property
    def acq_reference(self):
        return (self.pix & 1 << 17) >> 17

    @property
    def acq_debug(self):
        return (self.pix & 1 << 18) >> 18

    @property
    def start_pixel(self):
        return (self.pix & 1 << 19) >> 19

    @property
    def clk_rg(self):
        return (self.pix & 1 << 20) >> 20

    @property
    def clk_r01(self):
        return (self.pix & 1 << 21) >> 21

    @property
    def clk_r02(self):
        return (self.pix & 1 << 22) >> 22

    @property
    def clk_r03(self):
        return (self.pix & 1 << 23) >> 23

    @property
    def phase_reset(self):
        return (self.pix & 1 << 24) >> 24

    @property
    def phase_reference(self):
        return (self.pix & 1 << 25) >> 25

    @property
    def phase_signal(self):
        return (self.pix & 1 << 26) >> 26

    @property
    def raw_acquire(self):
        return (self.pix & 1 << 27) >> 27


class RawImageFile:

    def __init__(self, raw_image, metadata: RawImageMetadata=None):
        self._im = raw_image
        self._metadata = metadata

    @staticmethod
    def _check_directory(path):
        os.makedirs(path, exist_ok=True)

    def _rename_keys(self, key):
        name_rel = {
            "VERT_TOI": "VTOI", "VERT_TDTR": "VTDTR",
            "VERT_TDRT": "VTDRT", "VERT_TDRG": "VTDRG",
            "VERT_TDGR": "VTDGR", "HOR_DEBUG_PHASE": "DEBUGPH",
            "HOR_RG_SKIP": "RGSKP", "HOR_RG": "RGWIDTH",
            "HOR_PRERG_SKIP": "PRERGSKP", "HOR_PRERG": "PRERG",
            "HOR_POSTRG_SKIP": "POSRGSKP", "HOR_POSTRG": "POSTRG",
            "HOR_OVERLAP_SKIP": "OVERSKP", "HOR_OVERLAP": "OVERLAP",
            "HOR_DEL_SKIP": "DELSKP", "HOR_DEL": "DELAY",
            "HOR_ACQ_SKIP": "ACQSKP", "HOR_ACQ": "ACQTIME",
            "OG": "DETVOG", "OD_FG": "DETVODFG",
            "OD_EH": "DETVODEH", "DD": "DETVDD",
            "VSS": "DETVSS", "RD": "DETVRD",
            "DG_LOW": "DETDGL", "DG_HI": "DETDGH",
            "RG_LOW": "DETRGL", "RG_HI": "DETRGH",
            "R03_LOW": "DETH3L", "R03_HI": "DETH3H",
            "R02_LOW": "DETH2L", "R02_HI": "DETH2H",
            "R01_LOW": "DETH1L", "R01_HI": "DETH1H",
            "I04_ST_LOW": "DETV4STL", "I04_ST_HI": "DETV4STH",
            "I04_IM_LOW": "DETV4IML", "I04_IM_HI": "DETV4IMH",
            "I03_ST_LOW": "DETV3STL", "I03_ST_HI": "DETV3STH",
            "I03_IM_LOW": "DETV3IML", "I03_IM_HI": "DETV3IMH",
            "I02_ST_LOW": "DETV2STL", "I02_ST_HI": "DETV2STH",
            "I02_IM_LOW": "DETV2IML", "I02_IM_HI": "DETV2IMH",
            "I01_ST_LOW": "DETV1STL", "I01_ST_HI": "DETV1STH",
            "I01_IM_LOW": "DETV1IML", "I01_IM_HI": "DETV1IMH",
        }

        key = key.upper()

        if key.endswith("_VALUE"):
            s = "_"
            key = s.join(key.split("_")[:-1])

        if key in name_rel:
            return name_rel[key]
        else:
            return key

    def _fill_header(self, header):
        header['IMAGE_ID'] = self._im.image_id

        if self._metadata is not None:
            for key, value in vars(self._metadata).items():
                header[key] = value
        if self._im.meta:
            def add_metadata_dict(d, previous_key=""):
                for k, value in d.items():
                    key = self._rename_keys(k)

                    if previous_key:
                        key = "{}_{}".format(previous_key, key)
                    if isinstance(value, dict):
                        add_metadata_dict(value, key)
                    elif isinstance(value, Iterable):
                        counter = 0
                        for i in value:
                            n_key = "{}{}".format(key, counter)
                            header[n_key] = i
                            counter += 1
                    else:
                        header[key] = value
            add_metadata_dict(self._im.meta)

    def save_fits(self, base_path, base_name, overwrite=False):
        self._check_directory(base_path)

        hdul = fits.HDUList()
        main_hdu = fits.PrimaryHDU()
        header = main_hdu.header
        self._fill_header(header)
        hdul.append(main_hdu)

        for amp in self._im.amplifiers:
            amp_hdu = fits.ImageHDU(amp.matrix)
            amp_header = amp_hdu.header
            amp_header['AMPSEC'] = '[1:1024,1:1024]'
            amp_header['CCDSEC'] = '[1:1024,1:1024]'
            amp_header['CCDSIZE'] = '[1:1024,1:1024]'
            amp_header['DETSEC'] = '[1:1024,1:1024]'
            amp_header['DETSIZE'] = '[1:1024,1:1024]'
            amp_header['PRESCAN'] = '[1:50,1:1024]'
            amp_header['BIASSEC'] = '[1075:1107,1:1024]'
            amp_header['DATASEC'] = '[51:1074,1:1024]'
            amp_header['TRIMSEC'] = '[51:1074,1:1024]'
            hdul.append(amp_hdu)

        name = '{0}.fits'.format(base_name)
        path = os.path.join(base_path, name)
        if not overwrite:
            counter = 0
            while os.path.isfile(path):
                counter += 1
                name = '{}_{}.fits'.format(base_name, counter)
                path = os.path.join(base_path, name)

        hdul.writeto(path, overwrite=overwrite)

    def save_waveform_table(self, path, base_name, use_date=True):
        self._check_directory(path)

        file_name = base_name
        if use_date:
            now = datetime.datetime.now()
            file_name = '{}_{}'.format(now.strftime('%Y%m%d_%H%M%S'), base_name)

        for amp in self._im.amplifiers:
            if not amp.rows:
                continue

            file = os.path.join(path, '{0}_amp{1}.csv'.format(file_name, amp.amp_id))
            with open(file, 'w') as f:
                f.write('# UTC: {0}\n'.format(datetime.datetime.utcnow()))
                for k, v in amp.rows[0].meta.items():
                    f.write('# {0}: {1}\n'.format(k, v))
                f.write('# row, adc_counts, signal Sample, reference Sample, debug sample, '
                        'start pixel, clk_rg, clk_r01, clk_r02, clk_r03, reset phase, reference phase'
                        'signal phase, raw acquire\n'.format(''))
                for row in amp.rows:
                    for pix in row.data:
                        p = RawPixel(pix)
                        f.write('{}\n'.format(', '.join([str(x) for x in [row.meta['ccd_row_num'], p.adc_counts, p.acq_signal,
                                                         p.acq_reference, p.acq_debug, p.start_pixel, p.clk_rg,
                                                         p.clk_r01, p.clk_r02, p.clk_r03, p.phase_reset,
                                                         p.phase_reference, p.phase_signal, p.raw_acquire]])))

    def save_to_files(self, path, base_name, use_date=True):
        self._check_directory(path)

        file_name = base_name
        if use_date:
            now = datetime.datetime.now()
            file_name = '{}_{}'.format(now.strftime('%Y%m%d_%H%M%S'), base_name)

        for amp in self._im.amplifiers:
            if not amp.rows:
                continue

            file = os.path.join(path, '{0}_amp{1}.csv'.format(file_name, amp.amp_id))
            with open(file, 'w') as f:
                for r in amp.rows:
                    f.write('{0}\n'.format(', '.join(['{0}'.format(i) for i in r.data])))
