# This source code file is a part of SigProfilerTopography
# SigProfilerTopography is a tool included as part of the SigProfiler
# computational framework for comprehensive analysis of mutational
# signatures from next-generation sequencing of cancer genomes.
# SigProfilerTopography provides the downstream data analysis of
# mutations and extracted mutational signatures w.r.t.
# nucleosome occupancy, replication time, strand bias and processivity.
# Copyright (C) 2018-2020 Burcak Otlu

# #############################################################
# import sys
# import os
# current_abs_path = os.path.dirname(os.path.realpath(__file__))
# commonsPath = os.path.join(current_abs_path,'commons')
# sys.path.append(commonsPath)
# #############################################################

import math
import time
import numpy as np
import pandas as pd
import scipy
import statsmodels
import matplotlib as plt

import shutil
import platform
import multiprocessing

import SigProfilerMatrixGenerator as matrix_generator
MATRIX_GENERATOR_PATH=matrix_generator.__path__[0]

from SigProfilerTopography import version as topography_version
from SigProfilerMatrixGenerator import version as matrix_generator_version
from SigProfilerSimulator import version as simulator_version

from SigProfilerMatrixGenerator.scripts import SigProfilerMatrixGeneratorFunc as matGen
from SigProfilerSimulator import SigProfilerSimulator as simulator

from SigProfilerTopography.source.commons.TopographyCommons import readProbabilities
from SigProfilerTopography.source.commons.TopographyCommons import readChrBasedMutationsMergeWithProbabilitiesAndWrite

from SigProfilerTopography.source.commons.TopographyCommons import DATA
from SigProfilerTopography.source.commons.TopographyCommons import FIGURE
from SigProfilerTopography.source.commons.TopographyCommons import SAMPLE

from SigProfilerTopography.source.commons.TopographyCommons import K562
from SigProfilerTopography.source.commons.TopographyCommons import MCF7

from SigProfilerTopography.source.commons.TopographyCommons import SIGPROFILERTOPOGRAPHY_DEFAULT_FILES

from SigProfilerTopography.source.commons.TopographyCommons import getNucleosomeFile
from SigProfilerTopography.source.commons.TopographyCommons import getReplicationTimeFiles

from SigProfilerTopography.source.commons.TopographyCommons import available_nucleosome_biosamples
from SigProfilerTopography.source.commons.TopographyCommons import available_replication_time_biosamples

from SigProfilerTopography.source.commons.TopographyCommons import EPIGENOMICSOCCUPANCY
from SigProfilerTopography.source.commons.TopographyCommons import NUCLEOSOMEOCCUPANCY
from SigProfilerTopography.source.commons.TopographyCommons import REPLICATIONTIME
from SigProfilerTopography.source.commons.TopographyCommons import REPLICATIONSTRANDBIAS
from SigProfilerTopography.source.commons.TopographyCommons import TRANSCRIPTIONSTRANDBIAS
from SigProfilerTopography.source.commons.TopographyCommons import PROCESSIVITY

from SigProfilerTopography.source.commons.TopographyCommons import EPIGENOMICS
from SigProfilerTopography.source.commons.TopographyCommons import STRANDBIAS

from SigProfilerTopography.source.commons.TopographyCommons import DEFAULT_H3K27ME3_OCCUPANCY_FILE
from SigProfilerTopography.source.commons.TopographyCommons import DEFAULT_H3K36ME3_OCCUPANCY_FILE
from SigProfilerTopography.source.commons.TopographyCommons import DEFAULT_H3K9ME3_OCCUPANCY_FILE
from SigProfilerTopography.source.commons.TopographyCommons import DEFAULT_H3K27AC_OCCUPANCY_FILE
from SigProfilerTopography.source.commons.TopographyCommons import DEFAULT_H3K4ME1_OCCUPANCY_FILE
from SigProfilerTopography.source.commons.TopographyCommons import DEFAULT_H3K4ME3_OCCUPANCY_FILE
from SigProfilerTopography.source.commons.TopographyCommons import DEFAULT_CTCF_OCCUPANCY_FILE
from SigProfilerTopography.source.commons.TopographyCommons import DEFAULT_ATAC_SEQ_OCCUPANCY_FILE

from SigProfilerTopography.source.commons.TopographyCommons import UNDECLARED

from SigProfilerTopography.source.commons.TopographyCommons import USING_APPLY_ASYNC
from SigProfilerTopography.source.commons.TopographyCommons import STRINGENT
from SigProfilerTopography.source.commons.TopographyCommons import USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM
from SigProfilerTopography.source.commons.TopographyCommons import USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM_SPLIT

from SigProfilerTopography.source.commons.TopographyCommons import CONSIDER_COUNT
from SigProfilerTopography.source.commons.TopographyCommons import CONSIDER_DISTANCE
from SigProfilerTopography.source.commons.TopographyCommons import CONSIDER_DISTANCE_ALL_SAMPLES_TOGETHER

from SigProfilerTopography.source.commons.TopographyCommons import MISSING_SIGNAL
from SigProfilerTopography.source.commons.TopographyCommons import NO_SIGNAL

from SigProfilerTopography.source.commons.TopographyCommons import SBS96
from SigProfilerTopography.source.commons.TopographyCommons import ID
from SigProfilerTopography.source.commons.TopographyCommons import DBS

from SigProfilerTopography.source.commons.TopographyCommons import SUBS
from SigProfilerTopography.source.commons.TopographyCommons import INDELS
from SigProfilerTopography.source.commons.TopographyCommons import DINUCS

from SigProfilerTopography.source.commons.TopographyCommons import SBS_CONTEXTS
from SigProfilerTopography.source.commons.TopographyCommons import SNV

from SigProfilerTopography.source.commons.TopographyCommons import CHRBASED

from SigProfilerTopography.source.commons.TopographyCommons import GRCh37
from SigProfilerTopography.source.commons.TopographyCommons import GRCh38
from SigProfilerTopography.source.commons.TopographyCommons import MM9
from SigProfilerTopography.source.commons.TopographyCommons import MM10

from SigProfilerTopography.source.commons.TopographyCommons import ONE_DIRECTORY_UP
from SigProfilerTopography.source.commons.TopographyCommons import LIB
from SigProfilerTopography.source.commons.TopographyCommons import UCSCGENOME

from SigProfilerTopography.source.commons.TopographyCommons import WIG
from SigProfilerTopography.source.commons.TopographyCommons import BED

from SigProfilerTopography.source.commons.TopographyCommons import current_abs_path

from SigProfilerTopography.source.commons.TopographyCommons import getChromSizesDict
from SigProfilerTopography.source.commons.TopographyCommons import getShortNames
from SigProfilerTopography.source.commons.TopographyCommons import copyMafFiles
from SigProfilerTopography.source.commons.TopographyCommons import fillCutoff2Signature2PropertiesListDictionary
from SigProfilerTopography.source.commons.TopographyCommons import fill_mutations_dictionaries_write
from SigProfilerTopography.source.commons.TopographyCommons import get_mutation_type_context_for_probabilities_file

from SigProfilerTopography.source.commons.TopographyCommons import Table_MutationType_NumberofMutations_NumberofSamples_SamplesList_Filename
from SigProfilerTopography.source.commons.TopographyCommons import Table_ChrLong_NumberofMutations_Filename

from SigProfilerTopography.source.commons.TopographyCommons import Table_SubsSignature_Cutoff_NumberofMutations_AverageProbability_Filename
from SigProfilerTopography.source.commons.TopographyCommons import Table_IndelsSignature_Cutoff_NumberofMutations_AverageProbability_Filename
from SigProfilerTopography.source.commons.TopographyCommons import Table_DinucsSignature_Cutoff_NumberofMutations_AverageProbability_Filename

from SigProfilerTopography.source.commons.TopographyCommons import NUMBER_OF_MUTATIONS_IN_EACH_SPLIT

from SigProfilerTopography.source.nucleosomeoccupancy.NucleosomeOccupancyAnalysis import occupancyAnalysis
from SigProfilerTopography.source.replicationtime.ReplicationTimeAnalysis import replicationTimeAnalysis
from SigProfilerTopography.source.replicationstrandbias.ReplicationStrandBiasAnalysis import replicationStrandBiasAnalysis

from SigProfilerTopography.source.transcriptionstrandbias.TranscriptionStrandBiasAnalysis import transcriptionStrandBiasAnalysis
from SigProfilerTopography.source.processivity.ProcessivityAnalysis import processivityAnalysis

from SigProfilerTopography.source.plotting.OccupancyAverageSignalFigures import occupancyAverageSignalFigures
from SigProfilerTopography.source.plotting.OccupancyAverageSignalFigures import compute_fold_change_with_p_values_plot_heatmaps

from SigProfilerTopography.source.plotting.ReplicationTimeNormalizedMutationDensityFigures import replicationTimeNormalizedMutationDensityFigures
from SigProfilerTopography.source.plotting.TranscriptionReplicationStrandBiasFigures import transcriptionReplicationStrandBiasFiguresUsingDataframes

from SigProfilerTopography.source.plotting.ProcessivityFigures import processivityFigures

from SigProfilerTopography.source.commons.TopographyCommons import TRANSCRIBED_VERSUS_UNTRANSCRIBED
from SigProfilerTopography.source.commons.TopographyCommons import GENIC_VERSUS_INTERGENIC
from SigProfilerTopography.source.commons.TopographyCommons import LAGGING_VERSUS_LEADING

from SigProfilerTopography.source.commons.TopographyCommons import PLOTTING_FOR_SIGPROFILERTOPOGRAPHY_TOOL

from SigProfilerTopography.source.commons.TopographyCommons import COMBINE_P_VALUES_METHOD_FISHER
from SigProfilerTopography.source.commons.TopographyCommons import WEIGHTED_AVERAGE_METHOD
from SigProfilerTopography.source.commons.TopographyCommons import COLORBAR_SEISMIC


############################################################
#Can be move to DataPreparationCommons under /source/commons
#read chr based dinucs (provided by SigProfilerMatrixGenerator) and merge with probabilities (provided by SigProfilerTopography)
def prepareMutationsDataAfterMatrixGenerationAndExtractorForTopography(chromShortNamesList,inputDir,outputDir,jobname,mutation_type_context,mutations_probabilities_file_path,mutation_type_context_for_probabilities,startSimNum, endSimNum,partialDirname,PCAWG,verbose):

    ###########################################################################################
    #original matrix generator chrbased data will be under inputDir/output/vcf_files/SNV
    #original matrix generator chrbased data will be under inputDir/output/vcf_files/DBS
    #original matrix generator chrbased data will be under inputDir/output/vcf_files/ID

    #sim1 matrix generator chrbased data will be under inputDir/output/simulations/sim1/96/output/vcf_files/SNV
    #sim1 matrix generator chrbased data will be under inputDir/output/simulations/sim1/ID/output/vcf_files/ID
    #sim1 matrix generator chrbased data will be under inputDir/output/simulations/sim1/DBS/output/vcf_files/DBS

    df_columns_contain_ordered_signatures=None

    os.makedirs(os.path.join(outputDir,jobname,DATA,CHRBASED),exist_ok=True)
    for simNum in range(1,endSimNum+1):
        simName = 'sim%d' % (simNum)
        os.makedirs(os.path.join(outputDir,jobname,DATA,CHRBASED,simName), exist_ok=True)
    ###########################################################################################

    ###########################################################################################
    if ((mutations_probabilities_file_path is not None) and (os.path.exists(mutations_probabilities_file_path))):

        ##########################################################################################
        mutations_probabilities_df = readProbabilities(mutations_probabilities_file_path,verbose)
        df_columns_contain_ordered_signatures = mutations_probabilities_df.columns.values
        ##########################################################################################

        if verbose:
            print('\tVerbose mutations_probabilities_df.head()')
            print('\tVerbose %s' %(mutations_probabilities_df.head()))
            print('\tVerbose mutations_probabilities_df.columns.values')
            print('\tVerbose %s' %(mutations_probabilities_df.columns.values))

        ##########################################################################################
        #Step1 SigProfilerTopography Python Package
        #For Release we will use SAMPLE as it is, no change in SAMPLE column is needed.

        # For PCAWG_Matlab
        # This statement below is customized for  PCAWG_Matlab
        # To get rid of inconsistent cancer type names in sample column of chrbased mutation files and probabilities files
        # Breast-LobularCA_SP124191
        if PCAWG:
            mutations_probabilities_df[SAMPLE] = mutations_probabilities_df[SAMPLE].str.split('_',expand=True)[1]
        ##########################################################################################

        ############################################################################################
        ##############################  pool.apply_async starts ####################################
        ############################################################################################

        ################################
        numofProcesses = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=numofProcesses)
        ################################

        ################################
        jobs = []
        ################################

        sim_nums = range(startSimNum,endSimNum+1)
        sim_num_chr_tuples = ((sim_num, chrShort) for sim_num in sim_nums for chrShort in chromShortNamesList)

        for simNum, chrShort in sim_num_chr_tuples:
            simName = 'sim%d' % (simNum)
            chr_based_mutation_filename = '%s_seqinfo.txt' % (chrShort)
            if (simNum == 0):
                matrix_generator_output_dir_path = os.path.join(inputDir, 'output', 'vcf_files', partialDirname)
            else:
                matrix_generator_output_dir_path = os.path.join(inputDir, 'output', 'simulations', simName,mutation_type_context, 'output', 'vcf_files',partialDirname)
            if (os.path.exists(matrix_generator_output_dir_path)):
                chr_based_mutation_filepath = os.path.join(matrix_generator_output_dir_path,chr_based_mutation_filename)
                inputList = []
                inputList.append(chrShort)
                inputList.append(outputDir)
                inputList.append(jobname)
                inputList.append(chr_based_mutation_filepath)
                inputList.append(mutations_probabilities_df)
                inputList.append(mutation_type_context_for_probabilities)
                inputList.append(mutation_type_context)
                inputList.append(simNum)
                inputList.append(PCAWG)
                jobs.append(pool.apply_async(readChrBasedMutationsMergeWithProbabilitiesAndWrite,args=(inputList,)))
        ################################################################################

        ##############################################################################
        # wait for all jobs to finish
        for job in jobs:
            if verbose: print('\tVerbose Transcription Strand Bias Worker pid %s job.get():%s ' % (str(os.getpid()), job.get()))
        ##############################################################################

        ################################
        pool.close()
        pool.join()
        ################################

        ############################################################################################
        ##############################  pool.apply_async ends ######################################
        ############################################################################################

    ###########################################################################################

    ###########################################################################################
    elif (mutations_probabilities_file_path is None):
        #For Information
        print('There is a situation/problem: mutations_probabilities_file_path:%s does not exist.' %(mutations_probabilities_file_path))

        ############################################################################################
        ##############################  pool.apply_async starts ####################################
        ############################################################################################

        ################################
        numofProcesses = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=numofProcesses)
        ################################

        ################################
        jobs = []
        ################################

        sim_nums = range(startSimNum,endSimNum+1)
        sim_num_chr_tuples = ((sim_num, chrShort) for sim_num in sim_nums for chrShort in chromShortNamesList)

        for simNum, chrShort in sim_num_chr_tuples:
            simName = 'sim%d' % (simNum)
            chr_based_mutation_filename = '%s_seqinfo.txt' % (chrShort)
            if (simNum == 0):
                matrix_generator_output_dir_path = os.path.join(inputDir, 'output', 'vcf_files', partialDirname)
            else:
                matrix_generator_output_dir_path = os.path.join(inputDir, 'output', 'simulations', simName,mutation_type_context, 'output', 'vcf_files',partialDirname)
            if (os.path.exists(matrix_generator_output_dir_path)):
                chr_based_mutation_filepath = os.path.join(matrix_generator_output_dir_path,chr_based_mutation_filename)
                inputList = []
                inputList.append(chrShort)
                inputList.append(outputDir)
                inputList.append(jobname)
                inputList.append(chr_based_mutation_filepath)
                inputList.append(None)
                inputList.append(mutation_type_context_for_probabilities)
                inputList.append(mutation_type_context)
                inputList.append(simNum)
                inputList.append(PCAWG)
                jobs.append(pool.apply_async(readChrBasedMutationsMergeWithProbabilitiesAndWrite,args=(inputList,)))
        ################################################################################

        ##############################################################################
        # wait for all jobs to finish
        for job in jobs:
            if verbose: print('\tVerbose Transcription Strand Bias Worker pid %s job.get():%s ' % (str(os.getpid()), job.get()))
        ##############################################################################

        ################################
        pool.close()
        pool.join()
        ################################

        ############################################################################################
        ##############################  pool.apply_async ends ######################################
        ############################################################################################

    return df_columns_contain_ordered_signatures
    ###########################################################################################

############################################################


#######################################################
#JAN 9, 2020
def check_download_replication_time_files(replication_time_signal_file,replication_time_valley_file,replication_time_peak_file):
    current_abs_path = os.path.dirname(os.path.abspath(__file__))
    # print(current_abs_path)

    #These are currently full path, therefore convert them to filename
    replication_time_signal_file=os.path.basename(replication_time_signal_file)
    replication_time_valley_file=os.path.basename(replication_time_valley_file)
    replication_time_peak_file=os.path.basename(replication_time_peak_file)

    os.makedirs(os.path.join(current_abs_path,'lib','replication'),exist_ok=True)
    lib_replication_path = os.path.join(current_abs_path,'lib','replication')

    if os.path.isabs(lib_replication_path):
        # print('%s an absolute path.' %(lib_replication_path))
        os.chdir(lib_replication_path)

        replication_time_signal_file_path= os.path.join(lib_replication_path,replication_time_signal_file)
        replication_time_valley_file_path= os.path.join(lib_replication_path,replication_time_valley_file)
        replication_time_peak_file_path= os.path.join(lib_replication_path,replication_time_peak_file)

        if not os.path.exists(replication_time_signal_file_path):
            print('Does not exists: %s' %(replication_time_signal_file_path))
            try:
                # print('Downloading %s_signal_wgEncodeSydhNsome_%sSig.npy under %s' %(chrLong,cell_line,chrbased_npy_array_path))
                print('Downloading %s under %s' % (replication_time_signal_file, lib_replication_path))

                #wget -c Continue getting a partially-downloaded file
                #wget -nc  If a file is downloaded more than once in the same directory, the local file will be clobbered, or overwritten
                # cmd="bash -c '" + 'wget -r -l1 -c -nc --no-parent -nd -P ' + chrombased_npy_path + ' ftp://alexandrovlab-ftp.ucsd.edu/pub/tools/SigProfilerTopography/lib/nucleosome/chrbased/' + filename + "'"
                cmd="bash -c '" + 'wget -r -l1 -c -nc --no-parent -nd ftp://alexandrovlab-ftp.ucsd.edu/pub/tools/SigProfilerTopography/lib/replication/' + replication_time_signal_file + "'"
                # print(cmd)
                os.system(cmd)
            except:
                # print("The UCSD ftp site is not responding...pulling from sanger ftp now.")
                print("The ftp://alexandrovlab-ftp.ucsd.edu site is not responding...")

        if not os.path.exists(replication_time_valley_file_path):
            print('Does not exists: %s' %(replication_time_valley_file_path))
            try:
                # print('Downloading %s_signal_wgEncodeSydhNsome_%sSig.npy under %s' %(chrLong,cell_line,chrbased_npy_array_path))
                print('Downloading %s under %s' % (replication_time_valley_file, lib_replication_path))

                #wget -c Continue getting a partially-downloaded file
                #wget -nc  If a file is downloaded more than once in the same directory, the local file will be clobbered, or overwritten
                # cmd="bash -c '" + 'wget -r -l1 -c -nc --no-parent -nd -P ' + chrombased_npy_path + ' ftp://alexandrovlab-ftp.ucsd.edu/pub/tools/SigProfilerTopography/lib/nucleosome/chrbased/' + filename + "'"
                cmd="bash -c '" + 'wget -r -l1 -c -nc --no-parent -nd ftp://alexandrovlab-ftp.ucsd.edu/pub/tools/SigProfilerTopography/lib/replication/' + replication_time_valley_file + "'"
                # print(cmd)
                os.system(cmd)
            except:
                # print("The UCSD ftp site is not responding...pulling from sanger ftp now.")
                print("The ftp://alexandrovlab-ftp.ucsd.edu site is not responding...")

        if not os.path.exists(replication_time_peak_file_path):
            print('Does not exists: %s' %(replication_time_peak_file_path))
            try:
                # print('Downloading %s_signal_wgEncodeSydhNsome_%sSig.npy under %s' %(chrLong,cell_line,chrbased_npy_array_path))
                print('Downloading %s under %s' % (replication_time_peak_file, lib_replication_path))

                #wget -c Continue getting a partially-downloaded file
                #wget -nc  If a file is downloaded more than once in the same directory, the local file will be clobbered, or overwritten
                # cmd="bash -c '" + 'wget -r -l1 -c -nc --no-parent -nd -P ' + chrombased_npy_path + ' ftp://alexandrovlab-ftp.ucsd.edu/pub/tools/SigProfilerTopography/lib/nucleosome/chrbased/' + filename + "'"
                cmd="bash -c '" + 'wget -r -l1 -c -nc --no-parent -nd ftp://alexandrovlab-ftp.ucsd.edu/pub/tools/SigProfilerTopography/lib/replication/' + replication_time_peak_file + "'"
                # print(cmd)
                os.system(cmd)
            except:
                # print("The UCSD ftp site is not responding...pulling from sanger ftp now.")
                print("The ftp://alexandrovlab-ftp.ucsd.edu site is not responding...")

    else:
        #It has to be an absolute path
        print('%s is not an absolute path.' %(lib_replication_path))

    #go back
    os.chdir(current_abs_path)

#######################################################



#######################################################
#Nov25, 2019
# Download nucleosome occupancy chr based npy files from ftp alexandrovlab if they do not exists
# We are using this function if user is using our available nucleosome data for GM12878 adnd K562 cell lines
def check_download_chrbased_npy_nuclesome_files(nucleosome_file,chromNamesList):

    current_abs_path = os.path.dirname(os.path.abspath(__file__))
    # print(current_abs_path)

    os.makedirs(os.path.join(current_abs_path,'lib','nucleosome','chrbased'),exist_ok=True)
    chrombased_npy_path = os.path.join(current_abs_path,'lib','nucleosome','chrbased')
    # print(chrombased_npy_path)

    if os.path.isabs(chrombased_npy_path):
        # print('%s an absolute path.' %(chrombased_npy_path))
        os.chdir(chrombased_npy_path)

        nucleosome_filename_wo_extension = os.path.splitext(os.path.basename(nucleosome_file))[0]

        for chrLong in chromNamesList:
            # GM12878 and K562 comes from woman samples therefore there is no chrY
            if chrLong != 'chrY':
                # filename = '%s_signal_wgEncodeSydhNsome%sSig.npy' %(chrLong,cell_line)
                filename = '%s_signal_%s.npy' % (chrLong, nucleosome_filename_wo_extension)

                chrbased_npy_array_path = os.path.join(chrombased_npy_path, filename)
                if not os.path.exists(chrbased_npy_array_path):
                    print('Does not exists: %s' % (chrbased_npy_array_path))
                    try:
                        # print('Downloading %s_signal_wgEncodeSydhNsome_%sSig.npy under %s' %(chrLong,cell_line,chrbased_npy_array_path))
                        print('Downloading %s_signal_%s.npy under %s' % (
                        chrLong, nucleosome_filename_wo_extension, chrbased_npy_array_path))

                        # wget -c Continue getting a partially-downloaded file
                        # wget -nc  If a file is downloaded more than once in the same directory, the local file will be clobbered, or overwritten
                        # cmd="bash -c '" + 'wget -r -l1 -c -nc --no-parent -nd -P ' + chrombased_npy_path + ' ftp://alexandrovlab-ftp.ucsd.edu/pub/tools/SigProfilerTopography/lib/nucleosome/chrbased/' + filename + "'"
                        cmd = "bash -c '" + 'wget -r -l1 -c -nc --no-parent -nd ftp://alexandrovlab-ftp.ucsd.edu/pub/tools/SigProfilerTopography/lib/nucleosome/chrbased/' + filename + "'"
                        # print(cmd)
                        os.system(cmd)
                    except:
                        # print("The UCSD ftp site is not responding...pulling from sanger ftp now.")
                        print("The UCSD ftp site is not responding...")

    else:
        #It has to be an absolute path
        print('%s is not an absolute path.' %(chrombased_npy_path))


    #go back
    os.chdir(current_abs_path)
#######################################################


#######################################################

#######################################################
#For Skin-Melanoma USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM_SPLIT is better
#For others USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM is better
def runOccupancyAnalyses(genome,
                         outputDir,
                         jobname,
                         numofSimulations,
                         job_tuples,
                         sample_based,
                         library_file_with_path,
                         library_file_memo,
                         chromSizesDict,
                         chromNamesList,
                         ordered_sbs_signatures,
                         ordered_dbs_signatures,
                         ordered_id_signatures,
                         ordered_sbs_signatures_cutoffs,
                         ordered_dbs_signatures_cutoffs,
                         ordered_id_signatures_cutoffs,
                         computation_type,
                         occupancy_type,
                         occupancy_calculation_type,
                         plusorMinus,
                         remove_outliers,
                         quantileValue,
                         verbose):

    #######################################################################
    if (os.path.basename(library_file_with_path) not in SIGPROFILERTOPOGRAPHY_DEFAULT_FILES) and (not os.path.exists(library_file_with_path)):
        print('There is no such file under %s' %(library_file_with_path))
    #######################################################################

    # computation_type = USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM
    # computation_type =USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM_SPLIT
    occupancyAnalysis(genome,
                      computation_type,
                      occupancy_type,
                      occupancy_calculation_type,
                      sample_based,
                      plusorMinus,
                      chromSizesDict,
                      chromNamesList,
                      outputDir,
                      jobname,
                      numofSimulations,
                      job_tuples,
                      library_file_with_path,
                      library_file_memo,
                      ordered_sbs_signatures,
                      ordered_dbs_signatures,
                      ordered_id_signatures,
                      ordered_sbs_signatures_cutoffs,
                      ordered_dbs_signatures_cutoffs,
                      ordered_id_signatures_cutoffs,
                      remove_outliers,
                      quantileValue,
                      verbose)
#######################################################

#######################################################
def runReplicationTimeAnalysis(genome,
                               outputDir,
                               jobname,
                               numofSimulations,
                               job_tuples,
                               sample_based,
                               replicationTimeFilename,
                               chromSizesDict,
                               chromNamesList,
                               computation_type,
                               ordered_sbs_signatures,
                               ordered_dbs_signatures,
                               ordered_id_signatures,
                               ordered_sbs_signatures_cutoffs,
                               ordered_dbs_signatures_cutoffs,
                               ordered_id_signatures_cutoffs,
                               verbose,
                               matrix_generator_path):

    #Fill np array during runtime managed by replication_time_np_arrays_fill_runtime=True
    # Supported computation types
    # computation_type= USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM
    # computation_type =USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM_SPLIT
    replicationTimeAnalysis(computation_type,
                            sample_based,
                            genome,
                            chromSizesDict,
                            chromNamesList,
                            outputDir,
                            jobname,
                            numofSimulations,
                            job_tuples,
                            replicationTimeFilename,
                            ordered_sbs_signatures,
                            ordered_dbs_signatures,
                            ordered_id_signatures,
                            ordered_sbs_signatures_cutoffs,
                            ordered_dbs_signatures_cutoffs,
                            ordered_id_signatures_cutoffs,
                            verbose,
                            matrix_generator_path)
    ###############################################

#######################################################


#######################################################
def runReplicationStrandBiasAnalysis(outputDir,
                                     jobname,
                                     numofSimulations,
                                     job_tuples,
                                     sample_based,
                                     replicationTimeFilename,
                                     replicationTimeValleyFilename,
                                     replicationTimePeakFilename,
                                     chromSizesDict,
                                     chromNamesList,
                                     computation_type,
                                     ordered_sbs_signatures,
                                     ordered_dbs_signatures,
                                     ordered_id_signatures,
                                     ordered_sbs_signatures_cutoffs,
                                     ordered_dbs_signatures_cutoffs,
                                     ordered_id_signatures_cutoffs,
                                     verbose):

    os.makedirs(os.path.join(outputDir,jobname,DATA,REPLICATIONSTRANDBIAS),exist_ok=True)

    smoothedWaveletRepliseqDataFilename = replicationTimeFilename
    valleysBEDFilename = replicationTimeValleyFilename
    peaksBEDFilename = replicationTimePeakFilename

    # Supported computation types
    # computation_type= USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM
    # computation_type =USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM_SPLIT
    replicationStrandBiasAnalysis(computation_type,
                                  sample_based,
                                  chromSizesDict,
                                  chromNamesList,
                                  outputDir,
                                  jobname,
                                  numofSimulations,
                                  job_tuples,
                                  smoothedWaveletRepliseqDataFilename,
                                  valleysBEDFilename,
                                  peaksBEDFilename,
                                  ordered_sbs_signatures,
                                  ordered_dbs_signatures,
                                  ordered_id_signatures,
                                  ordered_sbs_signatures_cutoffs,
                                  ordered_dbs_signatures_cutoffs,
                                  ordered_id_signatures_cutoffs,
                                  verbose)
    ###############################################

#######################################################

#######################################################
def runTranscriptionStradBiasAnalysis(outputDir,
                                      jobname,
                                      numofSimulations,
                                      job_tuples,
                                      sample_based,
                                      chromNamesList,
                                      computation_type,
                                      ordered_sbs_signatures,
                                      ordered_dbs_signatures,
                                      ordered_id_signatures,
                                      ordered_sbs_signatures_cutoffs,
                                      ordered_dbs_signatures_cutoffs,
                                      ordered_id_signatures_cutoffs,
                                      verbose):

    os.makedirs(os.path.join(outputDir,jobname,DATA,TRANSCRIPTIONSTRANDBIAS),exist_ok=True)

    # Supported computation types
    # computation_type= USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM
    # computation_type =USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM_SPLIT
    transcriptionStrandBiasAnalysis(computation_type,
                                    sample_based,
                                    chromNamesList,
                                    outputDir,
                                    jobname,
                                    numofSimulations,
                                    job_tuples,
                                    ordered_sbs_signatures,
                                    ordered_dbs_signatures,
                                    ordered_id_signatures,
                                    ordered_sbs_signatures_cutoffs,
                                    ordered_dbs_signatures_cutoffs,
                                    ordered_id_signatures_cutoffs,
                                    verbose)
    ###############################################
#######################################################


#######################################################
def runProcessivityAnalysis(mutation_types_contexts,
                            outputDir,
                            jobname,
                            numofSimulations,
                            chromNamesList,
                            processivity_calculation_type,
                            subsSignature_cutoff_numberofmutations_averageprobability_df,
                            verbose):

    os.makedirs(os.path.join(outputDir,jobname,DATA,PROCESSIVITY),exist_ok=True)

    #Internally Set
    considerProbabilityInProcessivityAnalysis = True
    # considerProbabilityInProcessivityAnalysis = False
    computation_type=USING_APPLY_ASYNC
    print('processivity_calculation_type:%s' %processivity_calculation_type)

    processivityAnalysis(mutation_types_contexts,
                         chromNamesList,
                         computation_type,
                         processivity_calculation_type,
                         outputDir,
                         jobname,
                         numofSimulations,
                         considerProbabilityInProcessivityAnalysis,
                         subsSignature_cutoff_numberofmutations_averageprobability_df,
                         verbose)
    ###############################################
#######################################################


#######################################################
def deleteOldData(outputDir,jobname,occupancy_type):
    #############################################
    # Delete the output/jobname/DATA/occupancy_type if exists
    jobnamePath = os.path.join(outputDir,jobname,DATA,occupancy_type)

    ################################################
    if (os.path.exists(jobnamePath)):
        try:
            shutil.rmtree(jobnamePath)
        except OSError as e:
            print('Error: %s - %s.' % (e.filename, e.strerror))
    ################################################
#######################################################

#######################################################
def deleteOldFigures(outputDir, jobname, occupancy_type):

    jobnamePath = os.path.join(outputDir, jobname, FIGURE, occupancy_type)
    print('Topography.py jobnamePath:%s ' %jobnamePath)

    ############################################################
    if (os.path.exists(jobnamePath)):
        try:
            shutil.rmtree(jobnamePath)
        except OSError as e:
            print('Error: %s - %s.' % (e.filename, e.strerror))
    ############################################################
#######################################################


#######################################################
# Depreceated.
# We assume that simulated data will have the same number_of_splits as the real data
def get_job_tuples(chrlong_numberofmutations_df,numofSimulations):

    job_tuples = []
    sim_nums = range(0, numofSimulations + 1)

    for chrLong in chrlong_numberofmutations_df['chrLong'].unique():
        number_of_mutations=int(chrlong_numberofmutations_df[chrlong_numberofmutations_df['chrLong']==chrLong]['number_of_mutations'].values[0])
        number_of_splits = math.ceil(number_of_mutations / NUMBER_OF_MUTATIONS_IN_EACH_SPLIT)
        split_indexes = range(0, number_of_splits)

        ###############################################################
        for sim_num in sim_nums:
            for split_index in split_indexes:
                job_tuples.append((chrLong, sim_num, split_index))
        ###############################################################

    return job_tuples
#######################################################


#######################################################
# inputDir ='/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/input_for_matgen/BreastCancer560_subs_indels_dinucs'
# outputDir = '/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/output_test/'
# jobname = 'BreastCancer560'

#Run SigProfilerTopography Analyses
#Former full path now only the filename with extension
# nucleosomeOccupancy = '/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/lib/nucleosome/wgEncodeSydhNsomeGm12878Sig.wig'
# replicationSignal = '/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/lib/replication/GSM923442_hg19_wgEncodeUwRepliSeqMcf7WaveSignalRep1.wig'
# replicationValley = '/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/lib/replication/GSM923442_hg19_wgEncodeUwRepliSeqMcf7ValleysRep1.bed'
# replicationPeak = '/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/lib/replication/GSM923442_hg19_wgEncodeUwRepliSeqMcf7PkRep1.bed'
# subs_probabilities_file_path = '/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/output/560_BRCA_WGS_DINUCS/SBS96/Suggested_Solution/Decomposed_Solution/Mutation_Probabilities.txt'
# indels_probabilities_file_path = '/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/output/560_BRCA_WGS_DINUCS/ID83/Suggested_Solution/Decomposed_Solution/Mutation_Probabilities.txt'
# dinucs_probabilities_file_path = '/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/output/560_BRCA_WGS_DINUCS/DBS78/Suggested_Solution/Decomposed_Solution/Mutation_Probabilities.txt'
def runAnalyses(genome,
                inputDir,
                outputDir,
                jobname,
                numofSimulations,
                sbs_probabilities=None,
                id_probabilities= None,
                dbs_probabilities=None,
                mutation_types_contexts=None,
                mutation_types_contexts_for_signature_probabilities=None,
                epigenomics_files=[DEFAULT_H3K27ME3_OCCUPANCY_FILE,DEFAULT_H3K36ME3_OCCUPANCY_FILE,DEFAULT_H3K9ME3_OCCUPANCY_FILE,DEFAULT_H3K27AC_OCCUPANCY_FILE,DEFAULT_H3K4ME1_OCCUPANCY_FILE,DEFAULT_H3K4ME3_OCCUPANCY_FILE,DEFAULT_CTCF_OCCUPANCY_FILE,DEFAULT_ATAC_SEQ_OCCUPANCY_FILE],
                epigenomics_files_memos=None,
                epigenomics_biosamples=None,
                epigenomics_dna_elements=None,
                epigenomics_dir_name=None,
                nucleosome_biosample=None,
                nucleosome_file=None,
                replication_time_biosample=None,
                replication_time_signal_file=None,
                replication_time_valley_file=None,
                replication_time_peak_file=None,
                computation_type=USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM,
                epigenomics=False,
                nucleosome=False,
                replication_time=False,
                strand_bias=False,
                replication_strand_bias=False,
                transcription_strand_bias=False,
                processivity=False,
                sample_based=False,
                plot_figures=True,
                full_mode=True,
                step1_sim_data=True,
                step2_matgen_data=True,
                step3_prob_merged_data=True,
                step4_tables=True,
                cutoff_type=STRINGENT,
                average_probability=0.9,
                num_of_sbs_required=5000,
                num_of_id_required=1000,
                num_of_dbs_required=200,
                plusorMinus_epigenomics=1000,
                plusorMinus_nucleosome=1000,
                verbose=False,
                matrix_generator_path=MATRIX_GENERATOR_PATH,
                PCAWG=False,
                data_ready_plot_epigenomics=False,
                data_ready_plot_nucleosome=False,
                data_ready_plot_replication_time=False,
                data_ready_plot_replication_strand_bias=False,
                data_ready_plot_transcription_strand_bias=False,
                data_ready_plot_processivity=False,
                remove_outliers=False,
                quantileValue=0.97,
                delete_old=False,
                plot_mode=PLOTTING_FOR_SIGPROFILERTOPOGRAPHY_TOOL,
                occupancy_calculation_type=MISSING_SIGNAL,
                processivity_calculation_type=CONSIDER_DISTANCE,
                combine_p_values_method=COMBINE_P_VALUES_METHOD_FISHER,
                fold_change_window_size=100):

    current_abs_path = os.path.dirname(os.path.realpath(__file__))

    chromSizesDict = getChromSizesDict(genome)
    chromNamesList = list(chromSizesDict.keys())
    chromShortNamesList=getShortNames(chromNamesList)

    #Filled in Step3
    ordered_sbs_signatures_wrt_probabilities_file = None
    ordered_dbs_signatures_wrt_probabilities_file = None
    ordered_id_signatures_wrt_probabilities_file = None

    ###################################################
    # if mutation_types_contexts is None:
    #     mutation_types_contexts=[]
    #     if (sbs_probabilities is not None) and (os.path.exists(sbs_probabilities)):
    #         mutation_types_contexts.append(SBS96)
    #     if (id_probabilities is not None) and (os.path.exists(id_probabilities)):
    #         mutation_types_contexts.append(ID)
    #     if (dbs_probabilities is not None) and (os.path.exists(dbs_probabilities)):
    #         mutation_types_contexts.append(DBS)

    if mutation_types_contexts is None:
        mutation_types_contexts=[]
        if (sbs_probabilities is not None):
            mutation_types_contexts.append(SBS96)
        if (id_probabilities is not None):
            mutation_types_contexts.append(ID)
        if (dbs_probabilities is not None):
            mutation_types_contexts.append(DBS)

    if mutation_types_contexts_for_signature_probabilities is None:
        mutation_types_contexts_for_signature_probabilities=mutation_types_contexts
    ###################################################


    #################################################################################
    ################################## Setting starts ###############################
    ################## Set full path library files starts ###########################
    #################################################################################
    if genome is None:
        print('Parameter genome:%s must be set for SigProfilerTopography Analysis.' %(genome))

    ###############################################
    if strand_bias:
        replication_strand_bias=True
        transcription_strand_bias=True
    ###############################################

    ###############################################
    # We need full path of the library files
    default_epigenomics_files = [DEFAULT_H3K27ME3_OCCUPANCY_FILE,
                                 DEFAULT_H3K36ME3_OCCUPANCY_FILE,
                                 DEFAULT_H3K9ME3_OCCUPANCY_FILE,
                                 DEFAULT_H3K27AC_OCCUPANCY_FILE,
                                 DEFAULT_H3K4ME1_OCCUPANCY_FILE,
                                 DEFAULT_H3K4ME3_OCCUPANCY_FILE,
                                 DEFAULT_CTCF_OCCUPANCY_FILE,
                                 DEFAULT_ATAC_SEQ_OCCUPANCY_FILE]

    if (set(epigenomics_files) == set(default_epigenomics_files)):
        # Set default
        # Order in default_epigenomics_files and epigenomics_files_memos must match
        epigenomics_files = default_epigenomics_files
        epigenomics_files_memos = [os.path.splitext(os.path.basename(DEFAULT_H3K27ME3_OCCUPANCY_FILE))[0],
                                   os.path.splitext(os.path.basename(DEFAULT_H3K36ME3_OCCUPANCY_FILE))[0],
                                   os.path.splitext(os.path.basename(DEFAULT_H3K9ME3_OCCUPANCY_FILE))[0],
                                   os.path.splitext(os.path.basename(DEFAULT_H3K27AC_OCCUPANCY_FILE))[0],
                                   os.path.splitext(os.path.basename(DEFAULT_H3K4ME1_OCCUPANCY_FILE))[0],
                                   os.path.splitext(os.path.basename(DEFAULT_H3K4ME3_OCCUPANCY_FILE))[0],
                                   os.path.splitext(os.path.basename(DEFAULT_CTCF_OCCUPANCY_FILE))[0],
                                   os.path.splitext(os.path.basename(DEFAULT_ATAC_SEQ_OCCUPANCY_FILE))[0]]

        # Defines columns in the heatmap
        # These strings must be within filenames (without file extension)
        # Order is not important
        epigenomics_dna_elements=['H3K27me3', 'H3K36me3', 'H3K9me3', 'H3K27ac', 'H3K4me1', 'H3K4me3', 'CTCF', 'ATAC']

        # Defines rows in the detailed heatmap
        # These strings must be within filenames (without file extension)
        # Order is not important
        epigenomics_biosamples = ['breast_epithelium']

        for file_index, filename in enumerate(epigenomics_files):
            epigenomics_files[file_index] = os.path.join(current_abs_path, LIB, EPIGENOMICS, filename)
    ###############################################

    ###############################################
    # We need to set nucleosome_file
    # By default nucleosome_biosample=K562 and nucleosome_file is None
    # Here we set filename with extension not full path
    #There can be 2 cases:
    #Case 1 : nucleosome_biosample is an available nucleosome biosample and nucleosome_file is set as filename without fullpath
    #Case 2 : nucleosome_biosample is NOT an available nucleosome biosample and nucleosome_file is already set as filename with fullpath by the user

    #Case1: File is not set, Biosample is not set
    if (nucleosome_file is None) and (nucleosome_biosample is None):
        nucleosome_biosample = K562
        nucleosome_file = getNucleosomeFile(nucleosome_biosample)
        if nucleosome:
            check_download_chrbased_npy_nuclesome_files(nucleosome_file, chromNamesList)

    #Case2: File is not set, Biosample is set
    elif (nucleosome_file is None) and (nucleosome_biosample is not None):
        if (nucleosome_biosample in available_nucleosome_biosamples):
            #Sets the filename without the full path
            nucleosome_file = getNucleosomeFile(nucleosome_biosample)
            if (nucleosome):
                check_download_chrbased_npy_nuclesome_files(nucleosome_file, chromNamesList)
    #Case3: nucleosome_file is a filename with fullpath (User provided) , biosample is not set
    elif ((nucleosome_file is not None) and (nucleosome_biosample is None)):
        # We expect that user has provided nucleosome file with full path
        nucleosome_biosample = UNDECLARED
    #Case4: nucleosome_file is a filename with fullpath (User provided), biosample is set
    #Do nothing use as it is
    ###############################################

    ###############################################
    #We need full path of the library files
    #By default replication_time_biosample=MCF7 and signal, valley, peak files are None
    #Case1: Files are not set, Biosample is not set
    if (replication_time_signal_file is None) and (replication_time_valley_file is None) and (replication_time_peak_file is None) and (replication_time_biosample is None):
        replication_time_biosample=MCF7
        replication_time_signal_file, replication_time_valley_file,replication_time_peak_file=getReplicationTimeFiles(replication_time_biosample)
        if (replication_time or replication_strand_bias):
            # For using SigProfilerTopography Provided Replication Time Files
            check_download_replication_time_files(replication_time_signal_file, replication_time_valley_file,replication_time_peak_file)

    #Case2: Files are not set, Biosample is set
    elif (replication_time_signal_file is None) and (replication_time_valley_file is None) and (replication_time_peak_file is None) and (replication_time_biosample is not None):
        if (replication_time_biosample in available_replication_time_biosamples):
            replication_time_signal_file, replication_time_valley_file, replication_time_peak_file = getReplicationTimeFiles(replication_time_biosample)
            if (replication_time or replication_strand_bias):
                # For using SigProfilerTopography Provided Replication Time Files
                check_download_replication_time_files(replication_time_signal_file, replication_time_valley_file,replication_time_peak_file)

    #Case3: nucleosome_file is a filename with fullpath (User provided) , biosample is not set
    elif ((replication_time_signal_file is not None) or (replication_time_valley_file is not None) or (replication_time_peak_file is not None)) and (replication_time_biosample is None):
        replication_time_biosample = UNDECLARED
    #Case4: Files are set. Biosample is set. Use as it is. Do nothing.
    ###############################################

    ###############################################
    # data files are named using user provided epigenomics_files_memos or using epigenomics_file_memos_created
    epigenomics_file_memos_created = []

    # Run for each epigenomics file
    if (epigenomics_files_memos is None) or (len(epigenomics_files_memos) != len(epigenomics_files)):
        for idx, epigenomics_file in enumerate(epigenomics_files):
            epigenomics_file_memo = os.path.splitext(os.path.basename(epigenomics_file))[0]
            epigenomics_file_memos_created.append(epigenomics_file_memo)

    # Used for plotting
    if (epigenomics_files_memos is None) or (len(epigenomics_files_memos) != len(epigenomics_files)):
        epigenomics_files_memos = epigenomics_file_memos_created

    if (epigenomics_biosamples is None) or (len(epigenomics_biosamples) == 0):
        epigenomics_biosamples = [UNDECLARED]
    ###############################################

    #################################################################################
    ################## Set full path library files ends #############################
    ################################## Setting ends #################################
    #################################################################################


    print('#################################################################################')
    # print('--- %s' %platform.platform())
    # print('--- %s' %platform.system())
    #print("--- Operating System: %s" %(platform.uname()[0]))
    print("--- SigProfilerTopography starts")
    print('#################################################################################')

    print('#################################################################################')
    print("--- Operating System: %s" %(platform.platform()))
    print("--- Release: %s" %platform.uname()[2])
    print("--- Version: %s" %platform.uname()[3])
    print("--- Nodename: %s" %platform.uname()[1])
    print('#################################################################################')

    print('#################################################################################')
    print("--- Python and Package Versions")
    print("--- Python Version: %s" %(str(platform.sys.version_info.major) + "." + str(platform.sys.version_info.minor) + "." + str(platform.sys.version_info.micro)))
    print('--- SigProfilerTopography Version:%s' % topography_version.version)
    print("--- SigProfilerMatrixGenerator Version: %s" %matrix_generator_version.version)
    print("--- SigProfilerSimulator version: %s" %simulator_version.version)
    print("--- pandas version: %s" %pd.__version__)
    print("--- numpy version: %s" %np.__version__)
    print("--- statsmodels version: %s" %statsmodels.__version__)
    print("--- scipy version: %s" %scipy.__version__)
    print("--- matplotlib version: %s" %plt.__version__)
    print('#################################################################################\n')

    print('#################################################################################')
    print('--- SigProfilerTopography parameters')
    print('--- Genome: %s' %(genome))
    print('--- inputDir:%s' %inputDir)
    print('--- outputDir:%s' %outputDir)
    print('--- jobname:%s' %jobname)
    if (sbs_probabilities is not None):
        print('--- sbs_probabilities:%s' %sbs_probabilities)
    if (dbs_probabilities is not None):
        print('--- dbs_probabilities:%s' %dbs_probabilities)
    if (id_probabilities is not None):
        print('--- id_probabilities:%s' %id_probabilities)

    print('--- numofSimulations:%d' %numofSimulations)
    print('\n--- epigenomics_files:%s' %epigenomics_files)
    print('--- epigenomics_files_memos:%s' %epigenomics_files_memos)
    print('--- epigenomics_biosamples:%s' %epigenomics_biosamples)
    print('--- epigenomics_dna_elements:%s' %epigenomics_dna_elements)
    print('--- number of epigenomics_files:%d' %len(epigenomics_files))

    print('\n--- nucleosome_biosample:%s' %nucleosome_biosample)
    print('--- nucleosome_file:%s' % nucleosome_file)

    print('\n--- replication_time_biosample:%s' % replication_time_biosample)
    print('--- replication_time_signal_file:%s' % replication_time_signal_file)
    print('--- replication_time_valley_file:%s' % replication_time_valley_file)
    print('--- replication_time_peak_file:%s' % replication_time_peak_file)

    print('\n--- mutation_types_contexts:%s' %mutation_types_contexts)
    print('--- mutation_types_contexts_for_signature_probabilities:%s' %mutation_types_contexts_for_signature_probabilities)
    print('--- computation_type:%s\n' %computation_type)
    if sample_based:
        print('--- Sample Based Analysis.')

    if epigenomics:
        print('--- Epigenomics Analysis.')
    if nucleosome:
        print('--- Nucleosome Analysis.')
    if replication_time:
        print('--- Replication Time Analysis.')
    if (strand_bias or replication_strand_bias):
        print('--- Replication Strand Bias Analysis.')
    if (strand_bias or transcription_strand_bias):
        print('--- Transcription Strand Bias Analysis.')
    if processivity:
        print('--- Processivity Analysis.')

    print('--- plot_figures:%s' %plot_figures)
    print('--- average mutation probability required %0.2f' %average_probability)
    print('--- minimum number of sbs mutations required: %d' %num_of_sbs_required)
    print('--- minimum number of id mutations required: %d' %num_of_id_required)
    print('--- minimum number of dbs mutations required: %d' %num_of_dbs_required)
    if epigenomics:
        print('--- number of bases considered before and after mutation start for epigenomics analysis: %d' %plusorMinus_epigenomics)
    if nucleosome:
        print('--- number of bases considered before and after mutation start for nucleosome occupancy analysis: %d' %plusorMinus_nucleosome)
    print('#################################################################################\n')

    print('#################################################################################')
    numofProcesses = multiprocessing.cpu_count()
    print('--- numofProcesses for multiprocessing: %d' %numofProcesses)
    print('#################################################################################\n')

    #################################################################################
    print('#################################################################################')
    print('--- For Genome: %s' %(genome))
    print('--- Chromosome names: %s' %(chromNamesList))
    print('--- Chromosome short names: %s' % (chromShortNamesList))
    print('--- current_abs_path: %s ' % current_abs_path)
    print('#################################################################################\n')
    #################################################################################



    ###################################################################################################################
    ################################################# Full Mode starts ################################################
    ###################################################################################################################

    ###################################################################################################
    ######################### SigProfilerMatrixGenerator for original data starts #####################
    ###################################################################################################
    if (step2_matgen_data):

        # Run MatrixGenerator for original data: this call prepares chrBased input files for original data with mutation contexts
        print('#################################################################################')
        print('--- SigProfilerMatrixGenerator for original data')
        start_time = time.time()

        print('For original data inputDir:%s' % (inputDir))
        matrices = matGen.SigProfilerMatrixGeneratorFunc(jobname, genome, inputDir, plot=False, seqInfo=True)
        # print('matrices')
        # print(matrices)

        # original matrix generator chrbased data will be under inputDir/output/vcf_files/SNV
        # original matrix generator chrbased data will be under inputDir/output/vcf_files/DBS
        # original matrix generator chrbased data will be under inputDir/output/vcf_files/ID

        print("--- SigProfilerMatrixGenerator for original data: %s seconds ---" % (time.time() - start_time))
        print("--- SigProfilerMatrixGenerator for original data: %f minutess ---" % float((time.time() - start_time) / 60))
        print('#################################################################################\n')
    ###################################################################################################
    ######################### SigProfilerMatrixGenerator for original data ends #######################
    ###################################################################################################


    ###################################################################################################################
    ################################## First Step Simulations if any starts ###########################################
    ###################################################################################################################
    if ((numofSimulations > 0) and (step1_sim_data)):

        ###################################################################################################
        ############################  SigProfilerSimulator for n simulations starts #######################
        ###################################################################################################
        print('#################################################################################')
        print('--- SigProfilerSimulator for %d simulations starts' %(numofSimulations))
        start_time = time.time()
        #Call SigProfilerSimulator separately for each mutation type context otherwise it counts DBS mutations also in SBS mutations
        # Topography uses same mutation types with Simulator
        # Acceptable contexts for Simulator include {'96', '384', '1536', '6144', 'DBS', 'ID', 'ID415'}.
        # '96' or '384' for single base substitutions (Simulator 1536, or 3072)
        # 'DBS' for double base substitutions
        # 'ID' for indels
        for mutation_type_context in mutation_types_contexts:
            mutation_type_context_for_simulator = []
            mutation_type_context_for_simulator.append(mutation_type_context)
            # Please notice that Simulator reverse the given input mutationTypes_for_simulator
            print('--- SigProfilerSimulator is running for %s' %(mutation_type_context))
            simulator.SigProfilerSimulator(jobname, inputDir, genome, mutation_type_context_for_simulator,simulations=numofSimulations,chrom_based=True, gender='male')

        print("--- SigProfilerSimulator for %d simulations: %s seconds" %(numofSimulations,(time.time() -  start_time)))
        print("--- SigProfilerSimulator for %d simulations: %f minutes" %(numofSimulations,float((time.time()-start_time)/60)))
        print('--- SigProfilerSimulator for %d simulations ends' %(numofSimulations))
        print('#################################################################################\n')
        ###################################################################################################
        ############################  SigProfilerSimulator for n simulations ends #########################
        ###################################################################################################

    ###################################################################################################################
    ################################## First Step Simulations if any ends #############################################
    ###################################################################################################################


    ###################################################################################################################
    ################################## Second Step Matrix Generator for n simulations starts ##########################
    ###################################################################################################################
    if (step2_matgen_data):

        if (numofSimulations > 0):
            ###################################################################################################
            ########################### Create simN directories for MatrixGenerator starts ####################
            ###################################################################################################

            print('#################################################################################')
            print('--- Create directories for %d simulations under %s/output/simulations/' %(numofSimulations,inputDir))
            start_time = time.time()
            #Create directories sim1 to SimN under inputDir/output/simulations/
            access_rights = 0o755
            for simNum in range(1,numofSimulations+1):
                try:
                    simName = 'sim%d' %(simNum)
                    simDir = os.path.join(inputDir,'output','simulations',simName)
                    if (not os.path.exists(simDir)):
                        os.mkdir(simDir, access_rights)
                    for mutation_type_context in mutation_types_contexts:
                        simDir = os.path.join(inputDir,'output','simulations',simName,mutation_type_context)
                        if (not os.path.exists(simDir)):
                            os.mkdir(simDir, access_rights)
                except OSError:
                    print("Creation of the directory %s failed" %simDir)
                # else:
                #     print("Successfully created the directory %s" %simDir)

            for mutation_type_context in mutation_types_contexts:
                # Simulator creates one maf file for each simulation for each mutation context
                # Simulator creates maf files under inputDir/output/simulations/jobname_simulations_GRCh37_96
                # Simulator creates maf files under inputDir/output/simulations/jobname_simulations_GRCh37_ID
                # Simulator creates maf files under inputDir/output/simulations/jobname_simulations_GRCh37_DBS
                dirName = '%s_simulations_%s_%s' %(jobname, genome,mutation_type_context)
                copyFromDir = os.path.join(inputDir,'output','simulations',dirName)
                copyToMainDir= os.path.join(inputDir,'output','simulations')

                # Topography copies these maf files to inputDir/output/simulations/simX/mutation_type_context/X.maf
                # So that, in the next step MatrixGenerator can create chrom based seqinfo text files for each X.maf file
                copyMafFiles(copyFromDir,copyToMainDir,mutation_type_context,numofSimulations)
            print("--- Create directories and copy files: %s seconds ---" %(time.time()-start_time))
            print("--- Create directories and copy files: %f minutes ---" %(float((time.time()-start_time)/60)))
            print('#################################################################################\n')

            ###################################################################################################
            ########################### Create simN directories for MatrixGenerator ends ######################
            ###################################################################################################

            ###################################################################################################
            #Important note: Separate directory creation is necessary for Matrix Generator
            #inputDir/output/simulations/simX/96/X.maf
            #inputDir/output/simulations/simX/ID/X.maf
            #inputDir/output/simulations/simX/DBS/X.maf

            #enables MatrixGenerator to create chr based simulated data files under
            #sim1 matrix generator chrbased data will be under inputDir/output/simulations/simX/96/output/vcf_files/SNV
            #sim1 matrix generator chrbased data will be under inputDir/output/simulations/simX/ID/output/vcf_files/ID
            #sim1 matrix generator chrbased data will be under inputDir/output/simulations/simX/DBS/output/vcf_files/DBS

            #otherwise all simulations maf files will be under
            #inputDir/output/simulations/Skin-Melanoma_simulations_GRCh37_96
            #inputDir/output/simulations/Skin-Melanoma_simulations_GRCh37_DBS
            #inputDir/output/simulations/Skin-Melanoma_simulations_GRCh37_ID

            #Then running MatrixGenerator for each simulation will not be possible.
            ###################################################################################################

            ###################################################################################################
            ####################### Run MatrixGenerator for each simulation starts ############################
            ###################################################################################################
            print('#################################################################################')
            print('--- Run SigProfilerMatrixGenerator for each simulation starts')
            start_time = time.time()
            for simNum in range(1,numofSimulations+1):
                simName = 'sim%d' %(simNum)
                #For each simulation we are calling matrix generator separately for each mutation type context

                print('--- SigProfilerMatrixGenerator is run for %s starts' %(simName))
                for mutation_type_context in mutation_types_contexts:
                    simInputDir=  os.path.join(inputDir,'output','simulations',simName,mutation_type_context)
                    print('For %s: %s simInputDir:%s' %(mutation_type_context,simName,simInputDir))
                    matrices = matGen.SigProfilerMatrixGeneratorFunc(jobname,genome,simInputDir,plot=False, seqInfo=True)
                    # print('matrices')
                    # print(matrices)
                    print('#####################################')
                print('--- SigProfilerMatrixGenerator is run for %s ends\n' % (simName))
            #sim1 matrix generator chrbased data will be under inputDir/output/simulations/sim1/96/output/vcf_files/SNV
            #sim1 matrix generator chrbased data will be under inputDir/output/simulations/sim1/ID/output/vcf_files/ID
            #sim1 matrix generator chrbased data will be under inputDir/output/simulations/sim1/DBS/output/vcf_files/DBS

            #simN matrix generator chrbased data will be under inputDir/output/simulations/simN/96/output/vcf_files/SNV
            #simN matrix generator chrbased data will be under inputDir/output/simulations/simN/ID/output/vcf_files/ID
            #simN matrix generator chrbased data will be under inputDir/output/simulations/simN/DBS/output/vcf_files/DBS
            print("--- Run MatrixGenerator for each simulation: %s seconds" %(time.time()-start_time))
            print("--- Run MatrixGenerator for each simulation: %f minutes" %(float((time.time()-start_time)/60)))
            print('--- Run SigProfilerMatrixGenerator for each simulation ends')
            print('#################################################################################\n')
            ###################################################################################################
            ####################### Run MatrixGenerator for each simulation ends ##############################
            ###################################################################################################

    ###################################################################################################################
    ################################## Second Step Matrix Generator for n simulations ends ############################
    ###################################################################################################################


    ###################################################################################################################
    ########### Third Step Merge chrom based matrix generator generated files with probabilities starts ###############
    ###################################################################################################################
    if (step3_prob_merged_data):
        ####################################################################################################################
        ##################  Merge original chr based files with Mutation Probabilities starts ##############################
        ####################################################################################################################
        print('#################################################################################')
        print('--- Merge original chr based files with Mutation Probabilities starts')
        print('#################################################################################')
        startSimNum = 0
        endSimNum = 0
        start_time = time.time()
        # SBS
        for mutation_type_context in mutation_types_contexts:
            # if (mutation_type_context in SBS_CONTEXTS) and (sbs_probabilities is not None):
            if (mutation_type_context in SBS_CONTEXTS):
                mutation_type_context_for_probabilities = get_mutation_type_context_for_probabilities_file(mutation_types_contexts_for_signature_probabilities,SUBS)
                print('--- Merge %s context mutations with probabilities for %s' % (mutation_type_context, sbs_probabilities))
                ordered_sbs_signatures_wrt_probabilities_file = prepareMutationsDataAfterMatrixGenerationAndExtractorForTopography(chromShortNamesList,
                                                                                   inputDir,
                                                                                   outputDir,
                                                                                   jobname,
                                                                                   mutation_type_context,
                                                                                   sbs_probabilities,
                                                                                   mutation_type_context_for_probabilities,
                                                                                   startSimNum,
                                                                                   endSimNum,
                                                                                   SNV,
                                                                                   PCAWG,
                                                                                   verbose)

        # ID
        # if ((ID in mutation_types_contexts) and (id_probabilities is not None)):
        if (ID in mutation_types_contexts):
            mutation_type_context_for_probabilities = get_mutation_type_context_for_probabilities_file(mutation_types_contexts_for_signature_probabilities, INDELS)
            print('--- Merge %s mutations with probabilities for %s' % (ID, id_probabilities))
            ordered_id_signatures_wrt_probabilities_file = prepareMutationsDataAfterMatrixGenerationAndExtractorForTopography(chromShortNamesList,
                                                                               inputDir,
                                                                               outputDir,
                                                                               jobname,
                                                                               ID,
                                                                               id_probabilities,
                                                                               mutation_type_context_for_probabilities,
                                                                               startSimNum, endSimNum, ID,PCAWG,verbose)

        # DBS
        # if ((DBS in mutation_types_contexts) and (dbs_probabilities is not None)):
        if (DBS in mutation_types_contexts):
            mutation_type_context_for_probabilities = get_mutation_type_context_for_probabilities_file(mutation_types_contexts_for_signature_probabilities, DINUCS)
            print('--- Merge %s mutations with probabilities for %s' % (DBS, dbs_probabilities))
            ordered_dbs_signatures_wrt_probabilities_file = prepareMutationsDataAfterMatrixGenerationAndExtractorForTopography(chromShortNamesList, inputDir, outputDir,
                                                                               jobname, DBS,
                                                                               dbs_probabilities,
                                                                               mutation_type_context_for_probabilities,
                                                                               startSimNum, endSimNum, DBS,PCAWG,verbose)


        print("--- Merge original chr based files with Mutation Probabilities: %s seconds" % (time.time() - start_time))
        print("--- Merge original chr based files with Mutation Probabilities: %f minutes" % (float((time.time() - start_time) / 60)))
        print('--- Merge original chr based files with Mutation Probabilities ends')
        print('#################################################################################\n')
        ####################################################################################################################
        ##################  Merge original chr based files with Mutation Probabilities ends ################################
        ####################################################################################################################

        ####################################################################################################################
        ##################  Merge simulations chr based files with Mutation Probabilities starts ###########################
        ####################################################################################################################
        if (numofSimulations > 0):
            print('#################################################################################')
            print('--- Merge simulations chr based files with Mutation Probabilities starts')
            print('#################################################################################')
            startSimNum=1
            endSimNum=numofSimulations
            start_time = time.time()
            #SBS
            for mutation_type_context in mutation_types_contexts:
                # if (mutation_type_context in SBS_CONTEXTS) and (sbs_probabilities is not None):
                if (mutation_type_context in SBS_CONTEXTS):
                    mutation_type_context_for_probabilities = get_mutation_type_context_for_probabilities_file(mutation_types_contexts_for_signature_probabilities, SUBS)
                    print('--- Merge %s mutations with probabilities for %s' %(mutation_type_context,sbs_probabilities))
                    prepareMutationsDataAfterMatrixGenerationAndExtractorForTopography(chromShortNamesList,inputDir,outputDir,jobname,mutation_type_context,sbs_probabilities,mutation_type_context_for_probabilities,startSimNum,endSimNum,'SNV',PCAWG,verbose)

            #ID
            # if ((ID in mutation_types_contexts) and (id_probabilities is not None)):
            if (ID in mutation_types_contexts):
                mutation_type_context_for_probabilities = get_mutation_type_context_for_probabilities_file(mutation_types_contexts_for_signature_probabilities, ID)
                print('--- Merge %s mutations with probabilities for %s' % (ID, id_probabilities))
                prepareMutationsDataAfterMatrixGenerationAndExtractorForTopography(chromShortNamesList,inputDir,outputDir,jobname,'ID',id_probabilities,mutation_type_context_for_probabilities,startSimNum,endSimNum,'ID',PCAWG,verbose)

            #DBS
            # if ((DBS in mutation_types_contexts) and (dbs_probabilities is not None)):
            if (DBS in mutation_types_contexts):
                mutation_type_context_for_probabilities = get_mutation_type_context_for_probabilities_file(mutation_types_contexts_for_signature_probabilities, DBS)
                print('--- Merge %s mutations with probabilities for %s' % (DBS,dbs_probabilities))
                prepareMutationsDataAfterMatrixGenerationAndExtractorForTopography(chromShortNamesList,inputDir,outputDir,jobname,'DBS',dbs_probabilities,mutation_type_context_for_probabilities,startSimNum,endSimNum,'DBS',PCAWG,verbose)

            print("--- Merge simulations chr based files with Mutation Probabilities: %s seconds" %(time.time()-start_time))
            print("--- Merge simulations chr based files with Mutation Probabilities: %f minutes" %(float((time.time()-start_time)/60)))
            print('--- Merge simulations chr based files with Mutation Probabilities ends')
            print('#################################################################################\n')
        ####################################################################################################################
        ##################  Merge simulations chr based files with Mutation Probabilities ends #############################
        ####################################################################################################################

    else:
        for mutation_type_context in mutation_types_contexts:
            if (mutation_type_context in SBS_CONTEXTS):
                if ((sbs_probabilities is not None) and (os.path.exists(sbs_probabilities))):
                    ordered_sbs_signatures_wrt_probabilities_file = pd.read_csv(sbs_probabilities,sep='\t', index_col=0, nrows=0).columns.values
        if (DBS in mutation_types_contexts):
            if ((dbs_probabilities is not None) and (os.path.exists(dbs_probabilities))):
                ordered_dbs_signatures_wrt_probabilities_file = pd.read_csv(dbs_probabilities,sep='\t', index_col=0, nrows=0).columns.values
        if (ID in mutation_types_contexts):
            if ((id_probabilities is not None) and (os.path.exists(id_probabilities))):
                ordered_id_signatures_wrt_probabilities_file = pd.read_csv(id_probabilities,sep='\t', index_col=0, nrows=0).columns.values
    ###################################################################################################################
    ########### Third Step Merge chrom based matrix generator generated files with probabilities ends #################
    ###################################################################################################################


    #######################################################################################################
    ################################### Fourth Step Fill Table Starts #####################################
    #######################################################################################################
    if (step4_tables):
        #################################################################################
        print('#################################################################################')
        print('--- Fill tables/dictionaries using original data starts')
        start_time = time.time()
        ##################################################################################
        # For each signature we will find a cutoff value for mutations with average probability >=0.9
        # Our aim is to have at most 10% false positive rate in mutations
        # number of mutations >= 5K for subs signatures
        # number of mutations >= 1K for indels signatures
        # number of mutations >= 200 for dinuc signatures
        # If we can not satisfy this condition we will discard the signature

        cutoffs = []
        for cufoff in np.arange(0.5, 0.91, 0.01):
            cutoffs.append("%.2f" % (cufoff))

        # Initialize
        # mutationType2PropertiesListDict: PropertiesList consists of [NumberofMutations NumberofSamples SamplesList]
        mutationType2PropertiesDict = {}
        chrLong2NumberofMutationsDict={}

        # We are reading original data to fill the signature2PropertiesListDict
        subsSignature_cutoff_numberofmutations_averageprobability_df = fillCutoff2Signature2PropertiesListDictionary(outputDir,
                                                                                        jobname,
                                                                                        chromNamesList,
                                                                                        SUBS,
                                                                                        cutoffs,
                                                                                        average_probability,
                                                                                        num_of_sbs_required,
                                                                                        num_of_id_required,
                                                                                        num_of_dbs_required,
                                                                                        mutationType2PropertiesDict,
                                                                                        chrLong2NumberofMutationsDict,
                                                                                        cutoff_type)
        indelsSignature_cutoff_numberofmutations_averageprobability_df = fillCutoff2Signature2PropertiesListDictionary(outputDir,
                                                                                        jobname,
                                                                                        chromNamesList,
                                                                                        INDELS,
                                                                                        cutoffs,
                                                                                        average_probability,
                                                                                        num_of_sbs_required,
                                                                                        num_of_id_required,
                                                                                        num_of_dbs_required,
                                                                                        mutationType2PropertiesDict,
                                                                                        chrLong2NumberofMutationsDict,
                                                                                        cutoff_type)

        dinucsSignature_cutoff_numberofmutations_averageprobability_df = fillCutoff2Signature2PropertiesListDictionary(outputDir,
                                                                                        jobname,
                                                                                        chromNamesList,
                                                                                        DINUCS,
                                                                                        cutoffs,
                                                                                        average_probability,
                                                                                        num_of_sbs_required,
                                                                                        num_of_id_required,
                                                                                        num_of_dbs_required,
                                                                                        mutationType2PropertiesDict,
                                                                                        chrLong2NumberofMutationsDict,
                                                                                        cutoff_type)

        ####################################################################
        #Add the last row
        numberofMutations = 0
        all_samples = set()

        for mutation_type in mutationType2PropertiesDict:
            numberofMutations += mutationType2PropertiesDict[mutation_type]['number_of_mutations']
            samples_list = mutationType2PropertiesDict[mutation_type]['samples_list']
            all_samples = all_samples.union(samples_list)

        mutationType2PropertiesDict['All']={}
        mutationType2PropertiesDict['All']['number_of_mutations'] = numberofMutations
        mutationType2PropertiesDict['All']['number_of_samples'] = len(all_samples)
        mutationType2PropertiesDict['All']['samples_list'] = list(all_samples)

        # Write mutationType2PropertiesListDict dictionary as a dataframe starts
        filePath = os.path.join(outputDir, jobname, DATA, Table_MutationType_NumberofMutations_NumberofSamples_SamplesList_Filename)

        L = sorted([(mutation_type, a['number_of_mutations'], a['number_of_samples'], a['samples_list'])
                    for mutation_type, a  in mutationType2PropertiesDict.items()])
        mutationtype_numberofmutations_numberofsamples_sampleslist_df = pd.DataFrame(L, columns=['mutation_type', 'number_of_mutations', 'number_of_samples', 'samples_list'])

        # write this dataframe
        mutationtype_numberofmutations_numberofsamples_sampleslist_df.to_csv(filePath, sep='\t', header=True, index=False)
        # Write dictionary as a dataframe ends
        ####################################################################

        ####################################################################
        # Write chrLong2NumberofMutationsDict dictionary as a dataframe starts
        filePath = os.path.join(outputDir, jobname, DATA, Table_ChrLong_NumberofMutations_Filename)

        L = sorted([(chrLong, number_of_mutations)
                    for chrLong, number_of_mutations in chrLong2NumberofMutationsDict.items()])
        chrlong_numberofmutations_df = pd.DataFrame(L, columns=['chrLong', 'number_of_mutations'])

        # write this dataframe
        chrlong_numberofmutations_df.to_csv(filePath, sep='\t', header=True, index=False)
        # Write dictionary as a dataframe ends
        ####################################################################


        ##################################################################################

        ##################################################################################
        # We are reading original data again to fill the mutationType based, sample based and signature based dictionaries
        if sample_based:
            # Create files
            # createFiles(outputDir, jobname, MutationType2NumberofMutatiosDictFilename)

            # Using original data
            fill_mutations_dictionaries_write(outputDir, jobname, chromNamesList, SUBS,
                                              subsSignature_cutoff_numberofmutations_averageprobability_df, num_of_sbs_required, num_of_id_required,
                                              num_of_dbs_required)
            fill_mutations_dictionaries_write(outputDir, jobname, chromNamesList, INDELS,
                                              indelsSignature_cutoff_numberofmutations_averageprobability_df, num_of_sbs_required,
                                              num_of_id_required,
                                              num_of_dbs_required)
            fill_mutations_dictionaries_write(outputDir, jobname, chromNamesList, DINUCS,
                                              dinucsSignature_cutoff_numberofmutations_averageprobability_df, num_of_sbs_required,
                                              num_of_id_required,
                                              num_of_dbs_required)

        ##################################################################################
        print("--- Fill tables/dictionaries using original data: %s seconds" % (time.time() - start_time))
        print("--- Fill tables/dictionaries using original data: %f minutes" % (float((time.time() - start_time) / 60)))
        print('--- Fill tables/dictionaries using original data ends')
        print('#################################################################################\n')
        #################################################################################

    else:
        mutationtype_numberofmutations_numberofsamples_sampleslist_df=pd.read_csv(os.path.join(outputDir,jobname,DATA,Table_MutationType_NumberofMutations_NumberofSamples_SamplesList_Filename),sep='\t', header=0, dtype={'mutation_type':str, 'number_of_mutations':np.int32})
        chrlong_numberofmutations_df = pd.read_csv(os.path.join(outputDir, jobname, DATA, Table_ChrLong_NumberofMutations_Filename), sep='\t',header=0, dtype={'chrLong': str, 'number_of_mutations': np.int32})
        subsSignature_cutoff_numberofmutations_averageprobability_df=pd.read_csv(os.path.join(outputDir,jobname,DATA,Table_SubsSignature_Cutoff_NumberofMutations_AverageProbability_Filename),sep='\t', header=0, dtype={'cutoff':np.float32,'signature':str, 'number_of_mutations':np.int32,'average_probability':np.float32})
        indelsSignature_cutoff_numberofmutations_averageprobability_df= pd.read_csv(os.path.join(outputDir,jobname,DATA,Table_IndelsSignature_Cutoff_NumberofMutations_AverageProbability_Filename),sep='\t', header=0, dtype={'cutoff':np.float32,'signature':str, 'number_of_mutations':np.int32,'average_probability':np.float32})
        dinucsSignature_cutoff_numberofmutations_averageprobability_df=pd.read_csv(os.path.join(outputDir,jobname,DATA,Table_DinucsSignature_Cutoff_NumberofMutations_AverageProbability_Filename),sep='\t',header=0, dtype={'cutoff':np.float32,'signature':str, 'number_of_mutations':np.int32,'average_probability':np.float32})
    #######################################################################################################
    ################################### Fourth Step Fill Table ends #######################################
    #######################################################################################################


    ###################################################################################################################
    ################################################# Full Mode ends ##################################################
    ###################################################################################################################


    ####################################################################################################################
    #Fill ordered_signatures and ordered_signatures_cutoffs arrays
    # cutoffs_df are filled in (Step4=True or False but full_mode=True) or full_mode=False
    # ordered_signatures_wrt_probabilities are filled in (Step3=True or False but full_mode=True) or full_mode=False
    subs_signatures = subsSignature_cutoff_numberofmutations_averageprobability_df['signature'].values
    dinucs_signatures = dinucsSignature_cutoff_numberofmutations_averageprobability_df['signature'].values
    indels_signatures = indelsSignature_cutoff_numberofmutations_averageprobability_df['signature'].values

    #Fill numpy arrays with the signatures in cutoff files
    ordered_sbs_signatures=np.array([])
    ordered_dbs_signatures=np.array([])
    ordered_id_signatures=np.array([])

    ordered_sbs_signatures_cutoffs=[]
    ordered_dbs_signatures_cutoffs=[]
    ordered_id_signatures_cutoffs=[]

    if ordered_sbs_signatures_wrt_probabilities_file is not None:
        df_columns_subs_signatures_mask_array = np.isin(ordered_sbs_signatures_wrt_probabilities_file, subs_signatures)
        ordered_sbs_signatures = ordered_sbs_signatures_wrt_probabilities_file[df_columns_subs_signatures_mask_array]
        for signature in ordered_sbs_signatures:
            cutoff = subsSignature_cutoff_numberofmutations_averageprobability_df[subsSignature_cutoff_numberofmutations_averageprobability_df['signature'] == signature]['cutoff'].values[0]
            ordered_sbs_signatures_cutoffs.append(cutoff)

    if ordered_dbs_signatures_wrt_probabilities_file is not None:
        df_columns_dbs_signatures_mask_array = np.isin(ordered_dbs_signatures_wrt_probabilities_file, dinucs_signatures)
        ordered_dbs_signatures = ordered_dbs_signatures_wrt_probabilities_file[df_columns_dbs_signatures_mask_array]
        for signature in ordered_dbs_signatures:
            cutoff = dinucsSignature_cutoff_numberofmutations_averageprobability_df[dinucsSignature_cutoff_numberofmutations_averageprobability_df['signature'] == signature]['cutoff'].values[0]
            ordered_dbs_signatures_cutoffs.append(cutoff)

    if ordered_id_signatures_wrt_probabilities_file is not None:
        df_columns_id_signatures_mask_array = np.isin(ordered_id_signatures_wrt_probabilities_file, indels_signatures)
        ordered_id_signatures = ordered_id_signatures_wrt_probabilities_file[df_columns_id_signatures_mask_array]
        for signature in ordered_id_signatures:
            cutoff = indelsSignature_cutoff_numberofmutations_averageprobability_df[indelsSignature_cutoff_numberofmutations_averageprobability_df['signature'] == signature]['cutoff'].values[0]
            ordered_id_signatures_cutoffs.append(cutoff)

    ordered_sbs_signatures_cutoffs = np.array(ordered_sbs_signatures_cutoffs)
    ordered_dbs_signatures_cutoffs = np.array(ordered_dbs_signatures_cutoffs)
    ordered_id_signatures_cutoffs = np.array(ordered_id_signatures_cutoffs)
    ####################################################################################################################


    ####################################################################################################################
    ################################### Run SigProfilerTopography Analysis starts ######################################
    ####################################################################################################################
    print('#################################################################################')
    print('--- Run SigProfilerTopography Analysis starts')

    if (computation_type==USING_APPLY_ASYNC_FOR_EACH_CHROM_AND_SIM_SPLIT):
        job_tuples=get_job_tuples(chrlong_numberofmutations_df,numofSimulations)
    else:
        job_tuples=[]

    if (nucleosome):
        #Nucleosome Occupancy
        occupancy_type = NUCLEOSOMEOCCUPANCY

        if delete_old:
            deleteOldData(outputDir,jobname,occupancy_type)

        start_time = time.time()

        runOccupancyAnalyses(genome,
                             outputDir,
                             jobname,
                             numofSimulations,
                             job_tuples,
                             sample_based,
                             nucleosome_file,
                             None,
                             chromSizesDict,
                             chromNamesList,
                             ordered_sbs_signatures,
                             ordered_dbs_signatures,
                             ordered_id_signatures,
                             ordered_sbs_signatures_cutoffs,
                             ordered_dbs_signatures_cutoffs,
                             ordered_id_signatures_cutoffs,
                             computation_type,
                             occupancy_type,
                             occupancy_calculation_type,
                             plusorMinus_nucleosome,
                             remove_outliers,
                             quantileValue,
                             verbose)
        print('#################################################################################')
        print("--- Run Nucleosome Occupancy Analyses: %s seconds --- %s" %((time.time()-start_time),nucleosome_file))
        print("--- Run Nucleosome Occupancy Analyses: %f minutes --- %s" %(float((time.time()-start_time)/60),nucleosome_file))
        print('#################################################################################\n')

    if (replication_time):
        # Replication Time
        # Required genome is already downloaded by matrix generator
        if delete_old:
            deleteOldData(outputDir,jobname,REPLICATIONTIME)

        start_time = time.time()

        runReplicationTimeAnalysis(genome,
                                   outputDir,
                                   jobname,
                                   numofSimulations,
                                   job_tuples,
                                   sample_based,
                                   replication_time_signal_file,
                                   chromSizesDict,
                                   chromNamesList,
                                   computation_type,
                                   ordered_sbs_signatures,
                                   ordered_dbs_signatures,
                                   ordered_id_signatures,
                                   ordered_sbs_signatures_cutoffs,
                                   ordered_dbs_signatures_cutoffs,
                                   ordered_id_signatures_cutoffs,
                                   verbose,
                                   matrix_generator_path)
        print('#################################################################################')
        print("--- Run Replication Time Analyses: %s seconds --- %s" %((time.time()-start_time),computation_type))
        print("--- Run Replication Time Analyses: %f minutes --- %s" %(float((time.time()-start_time)/60),computation_type))
        print('#################################################################################\n')

    if replication_strand_bias:
        # Replication Strand Bias
        if delete_old:
            deleteOldData(outputDir,jobname,REPLICATIONSTRANDBIAS)

        start_time = time.time()

        runReplicationStrandBiasAnalysis(outputDir,
                                         jobname,
                                         numofSimulations,
                                         job_tuples,
                                         sample_based,
                                         replication_time_signal_file,
                                         replication_time_valley_file,
                                         replication_time_peak_file,
                                         chromSizesDict,
                                         chromNamesList,
                                         computation_type,
                                         ordered_sbs_signatures,
                                         ordered_dbs_signatures,
                                         ordered_id_signatures,
                                         ordered_sbs_signatures_cutoffs,
                                         ordered_dbs_signatures_cutoffs,
                                         ordered_id_signatures_cutoffs,
                                         verbose)
        print('#################################################################################')
        print("--- Run Replication Strand Bias Analyses: %s seconds --- %s" %((time.time()-start_time),computation_type))
        print("--- Run Replication Strand Bias Analyses: %f minutes --- %s" %(float((time.time()-start_time)/60),computation_type))
        print('#################################################################################\n')

    if transcription_strand_bias:
        # Transcription Strand Bias
        if delete_old:
            deleteOldData(outputDir,jobname,TRANSCRIPTIONSTRANDBIAS)

        start_time = time.time()
        runTranscriptionStradBiasAnalysis(outputDir,
                                          jobname,
                                          numofSimulations,
                                          job_tuples,
                                          sample_based,
                                          chromNamesList,
                                          computation_type,
                                          ordered_sbs_signatures,
                                          ordered_dbs_signatures,
                                          ordered_id_signatures,
                                          ordered_sbs_signatures_cutoffs,
                                          ordered_dbs_signatures_cutoffs,
                                          ordered_id_signatures_cutoffs,
                                          verbose)
        print('#################################################################################')
        print("--- Run Transcription Strand Bias Analyses: %s seconds --- %s" %((time.time()-start_time),computation_type))
        print("--- Run Transcription Strand Bias Analyses: %f minutes --- %s" %(float((time.time()-start_time)/60),computation_type))
        print('#################################################################################\n')

    if (processivity):
        # Processivity
        if delete_old:
            deleteOldData(outputDir,jobname,PROCESSIVITY)

        start_time = time.time()

        runProcessivityAnalysis(mutation_types_contexts,
                                outputDir,
                                jobname,
                                numofSimulations,
                                chromNamesList,
                                processivity_calculation_type,
                                subsSignature_cutoff_numberofmutations_averageprobability_df,
                                verbose)
        print('#################################################################################')
        print("--- Run Processivity Analyses: %s seconds ---" %(time.time()-start_time))
        print("--- Run Processivity Analyses: %f minutes ---" %(float((time.time()-start_time)/60)))
        print('#################################################################################\n')

    if (epigenomics):
        #Epigenomics
        #If there is  a user provided name use it as occupancy_type
        if (epigenomics_dir_name is not None):
            occupancy_type=epigenomics_dir_name
        else:
            occupancy_type=EPIGENOMICSOCCUPANCY

        if delete_old:
            deleteOldData(outputDir,jobname,occupancy_type)

        #Run for each epigenomics file
        for idx, epigenomics_file in enumerate(epigenomics_files):
            start_time = time.time()
            if (epigenomics_files_memos is not None) and (len(epigenomics_files_memos)==len(epigenomics_files)):
                epigenomics_file_memo= epigenomics_files_memos[idx]
            else:
                epigenomics_file_memo = os.path.splitext(os.path.basename(epigenomics_file))[0]

            runOccupancyAnalyses(genome,
                                 outputDir,
                                 jobname,
                                 numofSimulations,
                                 job_tuples,
                                 sample_based,
                                 epigenomics_file,
                                 epigenomics_file_memo,
                                 chromSizesDict,
                                 chromNamesList,
                                 ordered_sbs_signatures,
                                 ordered_dbs_signatures,
                                 ordered_id_signatures,
                                 ordered_sbs_signatures_cutoffs,
                                 ordered_dbs_signatures_cutoffs,
                                 ordered_id_signatures_cutoffs,
                                 computation_type,
                                 occupancy_type,
                                 occupancy_calculation_type,
                                 plusorMinus_epigenomics,
                                 remove_outliers,
                                 quantileValue,
                                 verbose)
            print('#################################################################################')
            print("--- Run Epigenomics Analyses: %s seconds --- %s" %((time.time()-start_time),epigenomics_file))
            print("--- Run Epigenomics Analyses: %f minutes --- %s" %(float((time.time()-start_time)/60),epigenomics_file))
            print('#################################################################################\n')

    print('--- Run SigProfilerTopography Analysis ends')
    print('#################################################################################\n')
    ####################################################################################################################
    ################################### Run SigProfilerTopography Analysis ends ########################################
    ####################################################################################################################

    ####################################################################################################################
    ############################################ Plot figures starts ###################################################
    ####################################################################################################################
    if (plot_figures):
        print('#################################################################################')
        print('--- Plot figures starts')
        start_time = time.time()
        plotFigures(outputDir,
                    jobname,
                    numofSimulations,
                    sample_based,
                    mutation_types_contexts,
                    epigenomics_files,
                    epigenomics_files_memos,
                    epigenomics_biosamples,
                    epigenomics_dna_elements,
                    epigenomics_dir_name,
                    nucleosome_file,
                    nucleosome_biosample,
                    epigenomics,
                    nucleosome,
                    replication_time,
                    replication_strand_bias,
                    transcription_strand_bias,
                    processivity,
                    plusorMinus_epigenomics,
                    plusorMinus_nucleosome,
                    verbose,
                    data_ready_plot_epigenomics,
                    data_ready_plot_nucleosome,
                    data_ready_plot_replication_time,
                    data_ready_plot_replication_strand_bias,
                    data_ready_plot_transcription_strand_bias,
                    data_ready_plot_processivity,
                    delete_old,
                    plot_mode,
                    combine_p_values_method,
                    fold_change_window_size)
        print('#################################################################################')
        print("--- Plot Figures: %s seconds ---" %(time.time()-start_time))
        print("--- Plot Figures: %f minutes ---" %(float((time.time()-start_time)/60)))
        print('--- Plot figures ends')
        print('#################################################################################\n')
    ####################################################################################################################
    ############################################ Plot figures ends #####################################################
    ####################################################################################################################

    print('#################################################################################')
    print("--- SigProfilerTopography ended successfully")
    print("--- Thanks for using SigProfilerTopography")
    print('#################################################################################\n')


#######################################################


##############################################################
#Plot Figures for the attainded data after SigProfilerTopography Analyses
def plotFigures(outputDir,
                jobname,
                numberofSimulations,
                sample_based,
                mutationTypes,
                epigenomics_files,
                epigenomics_files_memos,
                epigenomics_biosamples,
                epigenomics_dna_elements,
                epigenomics_dir_name,
                nucleosome_file,
                nucleosome_biosample,
                epigenomics,
                nucleosome,
                replication_time,
                replication_strand_bias,
                transcription_strand_bias,
                processivity,
                plusOrMinus_epigenomics,
                plusOrMinus_nucleosome,
                verbose,
                data_ready_plot_epigenomics,
                data_ready_plot_nucleosome,
                data_ready_plot_replication_time,
                data_ready_plot_replication_strand_bias,
                data_ready_plot_transcription_strand_bias,
                data_ready_plot_processivity,
                delete_old,
                plot_mode,
                combine_p_values_method,
                fold_change_window_size):


    ############################################################
    if (nucleosome or data_ready_plot_nucleosome):
        occupancy_type=NUCLEOSOMEOCCUPANCY
        if delete_old:
            deleteOldFigures(outputDir, jobname, occupancy_type)
        nucleosome_file_basename = os.path.basename(nucleosome_file)
        occupancyAverageSignalFigures(outputDir,jobname,numberofSimulations,sample_based,mutationTypes,nucleosome_file_basename,None,occupancy_type,plusOrMinus_nucleosome,verbose,plot_mode)
    ############################################################

    ############################################################
    if (replication_time or data_ready_plot_replication_time):
        if delete_old:
            deleteOldFigures(outputDir, jobname, REPLICATIONTIME)
        replicationTimeNormalizedMutationDensityFigures(outputDir,jobname,numberofSimulations,sample_based,mutationTypes,plot_mode)
    ############################################################

    ############################################################
    if ((replication_strand_bias and transcription_strand_bias) or (data_ready_plot_replication_strand_bias and data_ready_plot_transcription_strand_bias)):
        if delete_old:
            deleteOldFigures(outputDir, jobname, STRANDBIAS)
        # old way
        # transcriptionReplicationStrandBiasFigures(outputDir,jobname,figureAugmentation,numberofSimulations,sample_based)
        strand_bias_list=[TRANSCRIBED_VERSUS_UNTRANSCRIBED,GENIC_VERSUS_INTERGENIC,LAGGING_VERSUS_LEADING]
        transcriptionReplicationStrandBiasFiguresUsingDataframes(outputDir,jobname,numberofSimulations,strand_bias_list,sample_based,plot_mode)
    elif (replication_strand_bias or data_ready_plot_replication_strand_bias):
        strand_bias_list=[LAGGING_VERSUS_LEADING]
        transcriptionReplicationStrandBiasFiguresUsingDataframes(outputDir,jobname,numberofSimulations,strand_bias_list,sample_based,plot_mode)
    elif (transcription_strand_bias or data_ready_plot_transcription_strand_bias):
        strand_bias_list=[TRANSCRIBED_VERSUS_UNTRANSCRIBED,GENIC_VERSUS_INTERGENIC]
        transcriptionReplicationStrandBiasFiguresUsingDataframes(outputDir,jobname,numberofSimulations,strand_bias_list,sample_based,plot_mode)
    ############################################################

    ############################################################
    if (processivity or data_ready_plot_processivity):
        if delete_old:
            deleteOldFigures(outputDir, jobname, PROCESSIVITY)
        processivityFigures(outputDir,jobname,numberofSimulations,verbose)
    ############################################################

    ############################################################
    if (epigenomics or data_ready_plot_epigenomics):
        if epigenomics_dir_name is not None:
            occupancy_type=epigenomics_dir_name
        else:
            occupancy_type=EPIGENOMICSOCCUPANCY

        if delete_old:
            deleteOldFigures(outputDir, jobname, occupancy_type)

        #Initiate the pool
        numofProcesses = multiprocessing.cpu_count()

        #################################################################
        pool = multiprocessing.Pool(numofProcesses)
        jobs=[]

        #Please note that epigenomics_file_memo is not None
        #If None then it is created from filename.
        for idx, epigenomics_file in enumerate(epigenomics_files):
            epigenomics_file_basename = os.path.basename(epigenomics_file)
            epigenomics_file_memo= epigenomics_files_memos[idx]
            jobs.append(pool.apply_async(occupancyAverageSignalFigures,
                                         args=(outputDir,jobname,numberofSimulations,sample_based,mutationTypes,epigenomics_file_basename,epigenomics_file_memo,occupancy_type,plusOrMinus_epigenomics,verbose,plot_mode,)))

        if verbose: print('\tVerbose %s Plotting figures len(jobs):%d ' %(occupancy_type,len(jobs)))

        # wait for all jobs to finish
        for job in jobs:
            if verbose: print('\n\tVerbose %s Worker pid %s Plotting figures  job.get():%s ' %(occupancy_type,str(os.getpid()),job.get()))

        pool.close()
        pool.join()
        #################################################################

        # original old call
        # sequential
        # occupancyAverageSignalFigures(outputDir, jobname, figureAugmentation, numberofSimulations,sample_based, mutationTypes,epigenomics_file_basename,epigenomics_file_memo,occupancy_type,plusOrMinus_epigenomics,verbose)

        compute_fold_change_with_p_values_plot_heatmaps(combine_p_values_method,
                                              fold_change_window_size,
                                              outputDir,
                                              jobname,
                                              numberofSimulations,
                                              nucleosome_file,
                                              nucleosome_biosample,
                                              epigenomics_files_memos,
                                              epigenomics_biosamples,
                                              epigenomics_dna_elements,
                                              plusOrMinus_epigenomics,
                                              plusOrMinus_nucleosome,
                                              verbose)
    ############################################################

##############################################################



##############################################################
#To run on laptob
import os

if __name__== "__main__":

    genome = 'GRCh37'
    jobname = 'Test-Skin-Melanoma'
    numberofSimulations = 2

    inputDir = '/oasis/tscc/scratch/burcak/developer/python/SigProfilerTopography/SigProfilerTopography/input/PCAWG_Matlab_Clean/Skin-Melanoma/filtered/'
    outputDir = os.path.join('C:\\','Users','burcak','Developer','Python','SigProfilerTopography','SigProfilerTopography','output_test')

    sbs_probabilities_file_path = os.path.join('C:\\','Users','burcak','Developer','Python','SigProfilerTopography','SigProfilerTopography','output_for_extractor','PCAWG_Matlab','Skin-Melanoma_sbs96_mutation_probabilities.txt')
    id_probabilities_file_path = os.path.join('C:\\','Users','burcak','Developer','Python','SigProfilerTopography','SigProfilerTopography','output_for_extractor','PCAWG_Matlab','Skin-Melanoma_id83_mutation_probabilities.txt')
    dbs_probabilities_file_path = os.path.join('C:\\','Users','burcak','Developer','Python','SigProfilerTopography','SigProfilerTopography','output_for_extractor','PCAWG_Matlab','Skin-Melanoma_dbs_mutation_probabilities.txt')

    # user_provided_replication_time_file_path = os.path.join('C:\\','Users','burcak','Developer','Python','SigProfilerTopography','SigProfilerTopography','lib','replication','wgEncodeUwRepliSeqNhekWaveSignalRep1.wig')
    # user_provided_replication_time_valley_file_path = os.path.join('C:\\','Users','burcak','Developer','Python','SigProfilerTopography','SigProfilerTopography','lib','replication','wgEncodeUwRepliSeqNhekValleysRep1.bed')
    # user_provided_replication_time_peak_file_path = os.path.join('C:\\','Users','burcak','Developer','Python','SigProfilerTopography','SigProfilerTopography','lib','replication','wgEncodeUwRepliSeqNhekPkRep1.bed')

    # user_provided_nucleosome_file_path= os.path.join('C:\\','Users','burcak','Developer','Python','SigProfilerTopography','SigProfilerTopography','lib','nucleosome','wgEncodeSydhNsomeK562Sig.wig')
    user_provided_nucleosome_file_path = os.path.join('C:\\', 'Users', 'burcak', 'Developer', 'Python','SigProfilerTopography', 'SigProfilerTopography', 'lib','nucleosome', 'wgEncodeSydhNsomeGm12878Sig.wig')
    # user_provided_nucleosome_file_path= os.path.join('C:\\','Users','burcak','Developer','Python','SigProfilerTopography','SigProfilerTopography','lib','nucleosome','wgEncodeSydhNsomeGm12878Sig.bigWig')

    runAnalyses(genome, inputDir, outputDir, jobname, numberofSimulations,
                           sbs_probabilities=sbs_probabilities_file_path,
                           id_probabilities=id_probabilities_file_path,
                           dbs_probabilities=dbs_probabilities_file_path,
                            # nucleosome_biosample='K562',
                            # replication_time_biosample='NHEK',
                           # nucleosome_file=user_provided_nucleosome_file_path,
                           # replication_time_signal_file=user_provided_replication_time_file_path,
                           # replication_time_valley_file=user_provided_replication_time_valley_file_path,
                           # replication_time_peak_file=user_provided_replication_time_peak_file_path,
                           epigenomics=True, nucleosome=False, replication_time=False, strand_bias=False, processivity=False,
                           sample_based=False, new_simulations_enforced=False, full_mode=False, verbose=False,necessary_dictionaries_already_exists=True)
##############################################################