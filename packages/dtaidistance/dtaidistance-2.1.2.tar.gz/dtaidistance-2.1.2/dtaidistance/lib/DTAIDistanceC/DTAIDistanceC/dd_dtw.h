/*!
@header dtw.h
@brief DTAIDistance.dtw : Dynamic Time Warping

@author Wannes Meert
@copyright Copyright © 2020 Wannes Meert. Apache License, Version 2.0, see LICENSE for details.
*/

#ifndef dtw_h
#define dtw_h

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <signal.h>
#include <stdbool.h>
#include <stddef.h>
#include <assert.h>
#include <stdint.h>

#include "dd_globals.h"
#include "dd_ed.h"

/**
 @var keepRunning
 @abstract Indicator to track if an interrupt occured requiring the algorithm to exit.
 */
static volatile int keepRunning = 1;
/**
 @var printPrecision
 @abstract Number of decimals to print when printing (partial) distances.
 */
static int printPrecision = 3;


/**
Settings for DTW operations:
 
@field window : Window size; expressed as distance to a single side, thus
       the total window size will be window*2 + 1.
@field max_dist : Maximal distance, avoid computing cells that have a larger value.
       Return INFINITY if no path is found with a distance lower or equal to max_dist.
@field max_step : Maximal stepsize, replace value with INFINITY if step is
       larger than max_step.
@field max_length_diff : Maximal difference in length between two series.
       If longer, return INFINITY.
@field penalty : Customize the cost for expansion or compression.
@field psi: Psi relaxation allows to ignore this number of entries at the beginning
       and/or end of both sequences.
@field use_pruning : Compute Euclidean distance first to set max_dist (current value in
       max_dist is ignored).
@field only_ub : Only compute the upper bound (Euclidean) and return that value.
 */
struct DTWSettings_s {
    idx_t window;
    seq_t max_dist;
    seq_t max_step;
    idx_t max_length_diff;
    seq_t penalty;
    idx_t psi;
    bool use_pruning;
    bool only_ub;
    
};
typedef struct DTWSettings_s DTWSettings;

/**
 Block to restrict comparisons between series.
 
 @field rb Row begin
 @field re Row end
 @field cb Column begin
 @field ce Column end
 */
struct DTWBlock_s {
    idx_t rb;
    idx_t re;
    idx_t cb;
    idx_t ce;
};
typedef struct DTWBlock_s DTWBlock;


// Settings
DTWSettings dtw_settings_default(void);
void        dtw_settings_print(DTWSettings *settings);

// DTW
typedef seq_t (*DTWFnPtr)(seq_t *s1, idx_t l1, seq_t *s2, idx_t l2, DTWSettings *settings);

seq_t dtw_distance(seq_t *s1, idx_t l1, seq_t *s2, idx_t l2, DTWSettings *settings);
seq_t dtw_distance_ndim(seq_t *s1, idx_t l1, seq_t *s2, idx_t l2, int ndim, DTWSettings *settings);
seq_t dtw_warping_paths(seq_t *wps, seq_t *s1, idx_t l1, seq_t *s2, idx_t l2, bool return_dtw, bool do_sqrt, DTWSettings *settings);

// Bound
seq_t ub_euclidean(seq_t *s1, idx_t l1, seq_t *s2, idx_t l2);
seq_t ub_euclidean_ndim(seq_t *s1, idx_t l1, seq_t *s2, idx_t l2, int ndim);
seq_t lb_keogh(seq_t *s1, idx_t l1, seq_t *s2, idx_t l2, DTWSettings *settings);

// Block
DTWBlock dtw_block_empty(void);
void     dtw_block_print(DTWBlock *block);
bool     dtw_block_is_valid(DTWBlock *block, idx_t nb_series);

// Distance matrix
idx_t dtw_distances_ptrs(seq_t **ptrs, idx_t nb_ptrs, idx_t* lengths, seq_t* output,
                          DTWBlock* block, DTWSettings* settings);
idx_t dtw_distances_ndim_ptrs(seq_t **ptrs, idx_t nb_ptrs, idx_t* lengths, int ndim, seq_t* output,
                               DTWBlock* block, DTWSettings* settings);
idx_t dtw_distances_matrix(seq_t *matrix, idx_t nb_rows, idx_t nb_cols, seq_t* output,
                            DTWBlock* block, DTWSettings* settings);
idx_t dtw_distances_ndim_matrix(seq_t *matrix, idx_t nb_rows, idx_t nb_cols, int ndim, seq_t* output,
                                 DTWBlock* block, DTWSettings* settings);
idx_t dtw_distances_length(DTWBlock *block, idx_t nb_series);

// Auxiliary functions
void dtw_int_handler(int dummy);

void dtw_printprecision_set(int precision);
void dtw_printprecision_reset(void);

void dtw_print_wps(seq_t * wps, idx_t l1, idx_t l2);
void dtw_print_twoline(seq_t * dtw, idx_t r, idx_t c, idx_t length, int i0, int i1, idx_t skip, idx_t skipp, idx_t maxj, idx_t minj);

#endif /* dtw_h */
