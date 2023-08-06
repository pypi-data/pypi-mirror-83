ANN-SoLo
========

For more information:

* [Official code website](https://github.com/bittremieux/ANN-SoLo)

**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine for fast and accurate open modification searching. ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum. This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match modified spectra to their unmodified counterpart.

The software is available as open-source under the Apache 2.0 license.

Install
-------

See the [wiki](https://github.com/bittremieux/ANN-SoLo/wiki) for detailed instructions on how to install and run ANN-SoLo.

ANN-SoLo requires Python 3.6 or higher. The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms. Please refer to the Faiss installation instructions linked below for more information on OS and GPU support.

### Installation requirements

- **NumPy** needs to be available prior to the installation of ANN-SoLo.
- The **Faiss** installation depends on a specific GPU version. Please refer to the [Faiss installation instructions](https://github.com/facebookresearch/faiss/blob/master/INSTALL.md) for more information.

### Install ANN-SoLo

The recommended way to install ANN-SoLo is using pip:

    pip install ann_solo

ANN-SoLo search
---------------

Run ANN-SoLo to search your spectral data directly using on the command line using `ann_solo` or as a named Python module (if you do not have sufficient rights to install command-line scripts) using `python -m ann_solo.ann_solo`.

ANN-SoLo arguments can be specified as command-line arguments or in a configuration file. Argument preference is command-line args > configuration file > default settings.

For more information on which arguments are available and their default values run `ann_solo -h`.

Most options have sensible default values. Some positional arguments specifying which in- and output files to use are required. Additionally, the precursor and fragment mass tolerances do not have default values as these are data set dependent.

Please note that to run ANN-SoLo in cascade search mode two different precursor mass tolerances need to be specified for both levels of the cascade search (`precursor_tolerance_(mass|mode)` and `precursor_tolerance_(mass|mode)_open`).

```
usage: ann_solo [-h] [-c CONFIG_FILE] [--resolution RESOLUTION]
                [--min_mz MIN_MZ] [--max_mz MAX_MZ] [--remove_precursor]
                [--remove_precursor_tolerance REMOVE_PRECURSOR_TOLERANCE]
                [--min_intensity MIN_INTENSITY] [--min_peaks MIN_PEAKS]
                [--min_mz_range MIN_MZ_RANGE]
                [--max_peaks_used MAX_PEAKS_USED]
                [--max_peaks_used_library MAX_PEAKS_USED_LIBRARY]
                [--scaling {sqrt,rank}] --precursor_tolerance_mass
                PRECURSOR_TOLERANCE_MASS --precursor_tolerance_mode {Da,ppm}
                [--precursor_tolerance_mass_open PRECURSOR_TOLERANCE_MASS_OPEN]
                [--precursor_tolerance_mode_open {Da,ppm}]
                --fragment_mz_tolerance FRAGMENT_MZ_TOLERANCE
                [--allow_peak_shifts] [--fdr FDR]
                [--fdr_tolerance_mass FDR_TOLERANCE_MASS]
                [--fdr_tolerance_mode {Da,ppm}]
                [--fdr_min_group_size FDR_MIN_GROUP_SIZE] [--mode {ann,bf}]
                [--bin_size BIN_SIZE] [--hash_len HASH_LEN]
                [--num_candidates NUM_CANDIDATES] [--batch_size BATCH_SIZE]
                [--num_list NUM_LIST] [--num_probe NUM_PROBE] [--no_gpu]
                spectral_library_filename query_filename out_filename

ANN-SoLo: Approximate nearest neighbor spectral library searching
=================================================================

Bittremieux et al. Fast open modification spectral library searching through
approximate nearest neighbor indexing. Journal of Proteome Research 17,
3464-3474 (2018).

Bittremieux et al. Extremely fast and accurate open modification spectral
library searching of high-resolution mass spectra using feature hashing and
graphics processing units. Journal of Proteome Research 18, 3792-3799 (2019).

Official code website: https://github.com/bittremieux/ANN-SoLo

Args that start with '--' (eg. --resolution) can also be set in a config file
(config.ini or specified via -c). Config file syntax allows: key=value,
flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi).
If an arg is specified in more than one place, then commandline values
override config file values which override defaults.

positional arguments:
  spectral_library_filename
                        spectral library file (supported formats: splib)
  query_filename        query file (supported formats: mgf)
  out_filename          name of the mzTab output file containing the search
                        results

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        config file path
  --resolution RESOLUTION
                        spectral library resolution; masses will be rounded to
                        the given number of decimals (default: no rounding)
  --min_mz MIN_MZ       minimum m/z value (inclusive, default: 11 m/z)
  --max_mz MAX_MZ       maximum m/z value (inclusive, default: 2010 m/z)
  --remove_precursor    remove peaks around the precursor mass (default: no
                        peaks are removed)
  --remove_precursor_tolerance REMOVE_PRECURSOR_TOLERANCE
                        the window (in m/z) around the precursor mass to
                        remove peaks (default: 0 m/z)
  --min_intensity MIN_INTENSITY
                        remove peaks with a lower intensity relative to the
                        maximum intensity (default: 0.01)
  --min_peaks MIN_PEAKS
                        discard spectra with less peaks (default: 10)
  --min_mz_range MIN_MZ_RANGE
                        discard spectra with a smaller mass range (default:
                        250 m/z)
  --max_peaks_used MAX_PEAKS_USED
                        only use the specified most intense peaks for the
                        query spectra (default: 50)
  --max_peaks_used_library MAX_PEAKS_USED_LIBRARY
                        only use the specified most intense peaks for the
                        library spectra (default: 50)
  --scaling {sqrt,rank}
                        to reduce the influence of very intense peaks, scale
                        the peaks by their square root or by their rank
                        (default: rank)
  --precursor_tolerance_mass PRECURSOR_TOLERANCE_MASS
                        precursor mass tolerance (small window for the first
                        level of the cascade search)
  --precursor_tolerance_mode {Da,ppm}
                        precursor mass tolerance unit (options: Da, ppm)
  --precursor_tolerance_mass_open PRECURSOR_TOLERANCE_MASS_OPEN
                        precursor mass tolerance (wide window for the second
                        level of the cascade search)
  --precursor_tolerance_mode_open {Da,ppm}
                        precursor mass tolerance unit (options: Da, ppm)
  --fragment_mz_tolerance FRAGMENT_MZ_TOLERANCE
                        fragment mass tolerance (m/z)
  --allow_peak_shifts   use the shifted dot product instead of the standard
                        dot product
  --fdr FDR             FDR threshold to accept identifications during the
                        cascade search (default: 0.01)
  --fdr_tolerance_mass FDR_TOLERANCE_MASS
                        mass difference bin width for the group FDR
                        calculation during the second cascade level (default:
                        0.1 Da)
  --fdr_tolerance_mode {Da,ppm}
                        mass difference bin unit for the group FDR calculation
                        during the second cascade level (default: Da)
  --fdr_min_group_size FDR_MIN_GROUP_SIZE
                        minimum group size for the group FDR calculation
                        during the second cascade level (default: 20)
  --mode {ann,bf}       search using an approximate nearest neighbors or the
                        traditional (brute-force) mode; 'bf': brute-force,
                        'ann': approximate nearest neighbors (default: ann)
  --bin_size BIN_SIZE   ANN vector bin width (default: 0.04 Da)
  --hash_len HASH_LEN   ANN vector length (default: 800)
  --num_candidates NUM_CANDIDATES
                        number of candidates to retrieve from the ANN index
                        for each query (default: 1024), maximum 1024 when
                        using GPU indexing
  --batch_size BATCH_SIZE
                        number of query spectra to process simultaneously
                        (default: 16384)
  --num_list NUM_LIST   number of partitions in the ANN index (default: 256)
  --num_probe NUM_PROBE
                        number of partitions in the ANN index to inspect
                        during querying (default: 128), maximum 1024 when
                        using GPU indexing
  --no_gpu              don't use the GPU for ANN searching (default: GPU is
                        used if available)
```

Spectrum–spectrum match viewer
------------------------------

Use the ANN-SoLo plotter to visualize spectrum–spectrum matches from your search results. The plotter can be run directly on the command line using `ann_solo_plot` or as a named Python module (if you do not have sufficient rights to install command-line scripts) using `python -m ann_solo.plot_ssm`.

The plotter requires as command-line arguments an mzTab identification file produced by ANN-SoLo and the identifier of the query to visualize.
Please note that the spectral library used to perform the search needs to be present in the exact location as specified in the mzTab file.

The plotter will create a PNG file with a mirror plot to visualize the specified spectrum–spectrum match.

```
usage: ann_solo_plot [-h] mztab_filename query_id

Visualize spectrum–spectrum matches from your ANN-SoLo identification results

positional arguments:
  mztab_filename  Identifications in mzTab format
  query_id        The identifier of the query to visualize

optional arguments:
  -h, --help      show this help message and exit
```

Contact
-------

For more information you can visit the [official code website](https://github.com/bittremieux/ANN-SoLo) or send an email to <wout.bittremieux@uantwerpen.be>.
