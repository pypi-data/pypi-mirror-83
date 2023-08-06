# distutils: language=c++
# distutils: sources=SpectrumMatch.cpp

import numpy as np
cimport numpy as np
from libcpp cimport bool as bool_t
from libcpp.utility cimport pair
from libcpp.vector cimport vector


cdef extern from 'SpectrumMatch.h' namespace 'ann_solo' nogil:
    cdef cppclass Spectrum:
        Spectrum(double, unsigned int, unsigned int,
                 np.float32_t*, np.float32_t*, np.uint8_t*) except +

    cdef cppclass SpectrumSpectrumMatch:
        SpectrumSpectrumMatch(unsigned int) nogil except +
        unsigned int getCandidateIndex() nogil
        double getScore() nogil
        vector[pair[uint, uint]]* getPeakMatches() nogil

    cdef cppclass SpectrumMatcher:
        SpectrumMatcher() nogil except +
        SpectrumSpectrumMatch* dot(
                Spectrum*, vector[Spectrum*], double, bool_t) nogil


def get_best_match(query, candidates, fragment_mz_tolerance, allow_shift):
    """
    Find the best matching candidate spectrum compared to the given query
    spectrum.

    Spectrum similarity is evaluated based on the dot product. Either a
    standard element-wise dot product (while taking the fragment mass tolerance
    into account), or an element-wise dot product with allowed peak shifts
    based on the precursor mass difference between the spectra is calculated.
    This shifted dot product can result in a more appropriate score when PTM(s)
    cause some peaks in the spectrum to be shifted to another mass value. When
    peak shifts are allowed, annotated peaks from the candidate spectra (i.e.
    known library spectra) will be taken into account, whereas no annotations
    are taken into account for the peaks from the query spectrum.

    Args:
        query: The query spectrum for which the most similar candidate spectrum
            is determined.
        candidates: All candidate spectra that are compared to the query
            spectrum.
        fragment_mz_tolerance: Mass tolerance indicating the window around the
            mass peaks used for matching two peaks.
        allow_shift: Allow peaks to be shifted according to the precursor mass
            difference or not.

    Returns:
        The candidate with the highest similarity compared to the query
        spectrum, their similarity score, and a list of tuples `(query_peak_id,
        candidate_peak_id)` of the matching peaks between the query spectrum
        and the optimal candidate spectrum.
    """
    cdef double fragment_mz_tolerance_c
    cdef bool_t allow_shift_c
    fragment_mz_tolerance_c = fragment_mz_tolerance
    allow_shift_c = allow_shift

    cdef vector[Spectrum*] candidates_vec
    cdef np.float32_t[:] mz, intensity
    cdef np.uint8_t[:] charge
    cdef unsigned int candidate_index
    cdef double score
    cdef vector[pair[uint, uint]] peak_matches

    try:
        # Convert the candidates.
        for candidate in candidates:
            if not hasattr(candidate, 'charge'):
                candidate.charge = np.zeros_like(
                    candidate.annotation, dtype=np.uint8)
                for index, annotation in enumerate(candidate.annotation):
                    if annotation is not None:
                        candidate.charge[index] = annotation.charge
            mz = candidate.mz
            intensity = candidate.intensity
            charge = candidate.charge
            candidates_vec.push_back(new Spectrum(
                candidate.precursor_mz, candidate.precursor_charge,
                len(candidate.mz), &mz[0], &intensity[0], &charge[0]))

        mz = query.mz
        intensity = query.intensity
        query.charge = np.zeros_like(query.mz, dtype=np.uint8)
        charge = query.charge
        query_spec = new Spectrum(
            query.precursor_mz, query.precursor_charge, len(query.mz),
            &mz[0], &intensity[0], &charge[0])

        with nogil:
            query_matcher = new SpectrumMatcher()
            result = query_matcher.dot(query_spec, candidates_vec,
                                       fragment_mz_tolerance_c, allow_shift_c)
            candidate_index = result.getCandidateIndex()
            score = result.getScore()
            peak_matches = result.getPeakMatches()[0]

        return (candidates[candidate_index], score,
                [peak_matches[i] for i in range(peak_matches.size())])
    finally:
        for i in range(candidates_vec.size()):
            del candidates_vec[i]
        candidates_vec.clear()
        del query_spec
        del query_matcher
        del result
