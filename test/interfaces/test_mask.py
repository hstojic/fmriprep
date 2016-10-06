# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
''' Testing module for fmriprep.interfaces.mask '''
import os
import unittest
import mock
import nibabel as nb
import numpy as np

from fmriprep.interfaces.mask import BinarizeSegmentation

class TestMask(unittest.TestCase):
    ''' Testing class for fmriprep.interfaces.mask '''

    segmentation_nii = nb.Nifti1Image(np.array([[[0, 1], [2, 3]],
                                                [[3, 2], [1, 0]]]), np.eye(4))

    @mock.patch.object(nb, 'load', return_value=segmentation_nii)
    @mock.patch.object(nb.nifti1, 'save')
    @mock.patch.object(os.path, 'isfile', return_value=True)
    @mock.patch.object(nb.nifti1.Nifti1Image, '__eq__', autospec=True,
                       side_effect=lambda me: me.get_data().sum() == 4)
    def test_binarize_segmentation(self, nii_eq, mock_file_exists, mock_save, mock_load):
        '''
        mocked an equality function for niftis.
        it will probably catch errors but not guaranteed '''
        # set up
        segmentation = 'thisfiletotallyexists'
        out_file = 'thisonedoesnot.yet'

        # run
        bi = BinarizeSegmentation(in_segments=segmentation, false_values=[0, 1], out_mask=out_file)
        bi.run()

        # assert
        dummy_mask = nb.Nifti1Image(np.array([]), np.eye(4))

        mock_load.assert_called_once_with(segmentation)

        out_file_abs = os.path.abspath(out_file)
        mock_save.assert_called_once_with(dummy_mask, out_file_abs)
        self.assertEqual(bi.aggregate_outputs().get()['out_mask'], out_file_abs)
