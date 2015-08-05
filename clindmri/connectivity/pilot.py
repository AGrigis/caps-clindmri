#! /usr/bin/env python
##########################################################################
# NSAP - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Import
import nibabel
import os
import numpy
import matplotlib.pyplot as plt
import clindmri.plot.pvtk as pvtk
from clindmri.segmentation.freesurfer import cortex
from clindmri.tractography.pydipy import deterministic
from clindmri.tractography import Tractogram
from clindmri.extensions.freesurfer import read_cortex_surface_segmentation
from clindmri.connectivity.anatomical import diffusion_connectivity_matrix
from clindmri.connectivity.anatomical import anatomical_connectivity_matrix
from clindmri.extensions.fsl import flirt2aff


fsdir = "/volatile/imagen/dmritest/000000022453/fs"
t1file = (
    "/volatile/imagen/dmritest/000000022453/ADNI_MPRAGE/000000022453s012a1001.nii.gz")
dfile = (
    "/volatile/imagen/dmritest/000000022453/DTI/000000022453s011a1001.nii.gz")
bvecfile = "/volatile/imagen/dmritest/000000022453/DTI/000000022453s011a1001.bvec"
bvalfile = "/volatile/imagen/dmritest/000000022453/DTI/000000022453s011a1001.bval"
outdir = "/volatile/imagen/dmritest/000000022453/processed"
labelsfile = os.path.join(outdir, "labels.nii.gz")
trffile = os.path.join(outdir, "diff_to_anat.trf")
t2file = os.path.join(outdir, "diff_to_anat.nii.gz")
maskfile = os.path.join(outdir, "mask.nii.gz")

if 0:
    physical_to_index = numpy.linalg.inv(nibabel.load(t1file).get_affine())
    seg = read_cortex_surface_segmentation(fsdir, physical_to_index, None)   
    ren = pvtk.ren()
    for hemi in ["lh", "rh"]:
        surf = seg[hemi]
        ctab = [item["color"] for _, item in surf.metadata.items()]
        actor = pvtk.surface(surf.vertices, surf.triangles, surf.labels, ctab)
        pvtk.add(ren, actor)
        pvtk.show(ren)
        pvtk.clear(ren)
        actor = pvtk.surface(surf.inflated_vertices, surf.triangles,
                             surf.labels, ctab)
        pvtk.add(ren, actor)
        pvtk.show(ren)
        pvtk.clear(ren)
if 0:
    mask, label = cortex(t1file, fsdir, outdir, dfile)

if 0:
    outdir = "/volatile/imagen/dmritest/000000022453/processed/2"
    mask, label = cortex(t1file, fsdir, outdir)

if 0:
    mask = os.path.join(outdir, "cortex000000022453s011a1001-mask.nii.gz")
    tracks = deterministic(dfile, bvecfile, bvalfile, outdir, mask_file=mask,
                           order=4, nb_seeds_per_voxel=1, step=0.5, fmt="%.4f")

if 0:
    trffile = os.path.join(outdir, "dest_to_t1_000000022453s011a1001.trf")
    destfile = os.path.join(outdir, "e000000022453s011a1001-0.nii.gz")
    affine = flirt2aff(trffile, destfile, t1file)
    tracks = os.path.join(outdir, "000000022453s011a1001.trk")
    tractogram = Tractogram(tracks)
    density = tractogram.density(shape=nibabel.load(destfile).get_shape())
    density_file = os.path.join(outdir, "density-diffusion.nii.gz")
    density_image = nibabel.Nifti1Image(density, nibabel.load(destfile).get_affine())
    nibabel.save(density_image, density_file)
    tractogram.apply_affine(affine)
    density = tractogram.density(shape=nibabel.load(t1file).get_shape())
    density_file = os.path.join(outdir, "density-anatomic.nii.gz")
    density_image = nibabel.Nifti1Image(density, nibabel.load(t1file).get_affine())
    nibabel.save(density_image, density_file)
    print tractogram.apply_affine_on_endpoints(affine).shape
    ren = pvtk.ren()
    actor = pvtk.line(tractogram.tracks, 0)
    pvtk.add(ren, actor)
    pvtk.show(ren)

if 1:
    label = os.path.join(outdir, "cortex000000022453s011a1001-labels.nii.gz")
    tracks = os.path.join(outdir, "000000022453s011a1001.trk")
    connectivity = diffusion_connectivity_matrix(tracks, label, symmetric=True)
    plt.imshow(numpy.log1p(connectivity), interpolation="nearest")
    plt.show()

if 1:
    label = os.path.join(outdir, "2", "cortex000000022453s012a1001-labels.nii.gz")
    tracks = os.path.join(outdir, "000000022453s011a1001.trk")
    trffile = os.path.join(outdir, "dest_to_t1_000000022453s011a1001.trf")
    dt2file = os.path.join(outdir, "e000000022453s011a1001-0.nii.gz")
    connectivity = anatomical_connectivity_matrix(tracks, label, t1file,
                                                  dt2file, trffile,  symmetric=True)
    plt.imshow(numpy.log1p(connectivity), interpolation="nearest")
    plt.show()
