#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 08:33:47 2018

@author: prmiles
"""

from pymcmcstat.MCMC import print_rejection_statistics, MCMC
from pymcmcstat.structures.ParameterSet import ParameterSet
import test.general_functions as gf
import unittest
from mock import patch
import io
import sys
import os
import shutil
import numpy as np


def setup_pseudo_results(initialize=True):
    mcstat = gf.setup_mcmc_case_cp(initialize=initialize)
    rejectedin = {'total': 10, 'in_adaptation_interval': 4, 'outside_bounds': 1}
    mcstat._MCMC__rejected = rejectedin.copy()
    mcstat._MCMC__simulation_time = 0.1
    return mcstat


# --------------------------
class MCMCInitialization(unittest.TestCase):

    def test_initialization(self):
        MC = MCMC()
        check_these = ['data', 'model_settings', 'simulation_options', 'parameters',
                       '_error_variance', '_covariance', '_sampling_methods', '_mcmc_status']
        for ct in check_these:
            self.assertTrue(hasattr(MC, ct), msg=str('Object missing attribute: {}'.format(ct)))
        self.assertFalse(MC._mcmc_status, msg='Status is False')

    def test_numpy_error_set(self):
        MCMC(seterr={})
        a = np.geterr()
        self.assertEqual(a['over'], 'ignore', msg='Expect default ignore')
        self.assertEqual(a['under'], 'ignore', msg='Expect default ignore')
        MCMC(seterr=dict(over='warn', under='ignore'))
        a = np.geterr()
        self.assertEqual(a['over'], 'warn', msg='Expect overwrite to warn')
        self.assertEqual(a['under'], 'ignore', msg='Expect default ignore')

    def test_set_seed(self):
        MCMC(rngseed=1)
        a = np.random.rand(1)
        self.assertAlmostEqual(a[0], 0.417022,
                               msg=str('Expect seed to cause consistent random draw: {} neq {}'.format(
                                       a, np.array([0.417022]))))


# --------------------------
class DisplayCurrentMCMCSettings(unittest.TestCase):

    def test_standard_print(self):
        mcstat = gf.setup_mcmc_case_cp()
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        mcstat.display_current_mcmc_settings()
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertTrue(isinstance(capturedOutput.getvalue(), str), msg='Caputured string')


# --------------------------
class PrintRejectionStatistics(unittest.TestCase):
    def test_print_stats(self):
        rejected = {'total': 10, 'in_adaptation_interval': 4, 'outside_bounds': 1}
        isimu = 100
        iiadapt = 10
        verbosity = 3
        capturedOutput = io.StringIO()  # Create StringIO object
        sys.stdout = capturedOutput  # and redirect stdout.
        print_rejection_statistics(rejected=rejected, isimu=isimu, iiadapt=iiadapt, verbosity=verbosity)
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), str('i:{} ({},{},{})\n\n'.format(
                isimu, rejected['total']*isimu**(-1)*100, rejected['in_adaptation_interval']*iiadapt**(-1)*100,
                rejected['outside_bounds']*isimu**(-1)*100)), msg='Strings should match')


# --------------------------
class UpdateChain(unittest.TestCase):
    def test_chain_accepted(self):
        accept = 1
        outsidebounds = 0
        CL = {'theta': np.array([1.0, 2.0]), 'ss': 1.0, 'prior': 0.0, 'sigma2': 0.0}
        parset = ParameterSet(theta=CL['theta'], ss=CL['ss'], prior=CL['prior'], sigma2=CL['sigma2'])
        mcstat = gf.setup_initialize_chains(CL)
        mcstat._MCMC__update_chain(accept=accept, new_set=parset, outsidebounds=outsidebounds)
        self.assertTrue(
                np.array_equal(mcstat._MCMC__chain[-1, :], parset.theta),
                msg=str('theta added to end of chain - {}'.format(mcstat._MCMC__chain[-1, :])))
        self.assertEqual(mcstat._MCMC__old_set, parset, msg='old_set updated to new set')

    def test_chain_not_accepted_within_bounds(self):
        accept = 0
        outsidebounds = 0
        CL = {'theta': np.array([1.0, 2.0]), 'ss': 1.0, 'prior': 0.0, 'sigma2': 0.0}
        parset = ParameterSet(theta=CL['theta'], ss=CL['ss'], prior=CL['prior'], sigma2=CL['sigma2'])
        mcstat = gf.setup_initialize_chains(CL)
        mcstat._MCMC__rejected = {'total': 10, 'in_adaptation_interval': 4, 'outside_bounds': 1}
        mcstat._MCMC__update_chain(accept=accept, new_set=parset, outsidebounds=outsidebounds)
        self.assertTrue(
                np.array_equal(mcstat._MCMC__chain[-1, :], mcstat._MCMC__old_set.theta),
                msg=str('theta added to end of chain - {}'.format(mcstat._MCMC__chain[-1, :])))


# --------------------------
class UpdateRejected(unittest.TestCase):
    @classmethod
    def common_setup(cls):
        mcstat = gf.setup_mcmc_case_cp()
        rejectedin = {'total': 10, 'in_adaptation_interval': 4, 'outside_bounds': 1}
        mcstat._MCMC__rejected = rejectedin.copy()
        return mcstat, rejectedin

    def common_checks(self, mcstat, rejectedin, expect=0):
        self.assertEqual(mcstat._MCMC__rejected['total'],
                         rejectedin['total']+1,
                         msg='Adds one to counter')
        self.assertEqual(mcstat._MCMC__rejected['in_adaptation_interval'],
                         rejectedin['in_adaptation_interval']+1,
                         msg='Adds one to counter')
        self.assertEqual(mcstat._MCMC__rejected['outside_bounds'],
                         rejectedin['outside_bounds'] + expect,
                         msg='This counter stays the same.')

    def test_update_rejection_stats_not_outsidebounds(self):
        mcstat, rejectedin = self.common_setup()
        mcstat._MCMC__update_rejected(outsidebounds=0)
        self.common_checks(mcstat, rejectedin)

    def test_update_rejection_stats_outsidebounds(self):
        mcstat, rejectedin = self.common_setup()
        mcstat._MCMC__update_rejected(outsidebounds=1)
        self.common_checks(mcstat=mcstat, rejectedin=rejectedin, expect=1)


# --------------------------
class InitializeChain(unittest.TestCase):

    @classmethod
    def setup_CL(cls):
        return {'theta': np.array([1.0, 2.0]), 'ss': 1.0, 'prior': 0.0, 'sigma2': 0.0}

    def test_initialize_chain_updatesigma_1(self):
        CL = self.setup_CL()
        mcstat = gf.setup_initialize_chains(CL)
        self.assertEqual(mcstat._MCMC__chain.shape,
                         (mcstat.simulation_options.nsimu, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__chain.shape)))
        self.assertEqual(mcstat._MCMC__sschain.shape,
                         (mcstat.simulation_options.nsimu, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__sschain.shape)))
        self.assertEqual(mcstat._MCMC__s2chain.shape,
                         (mcstat.simulation_options.nsimu, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__s2chain.shape)))

    def test_initialize_chain_updatesigma_0(self):
        CL = self.setup_CL()
        mcstat = gf.setup_initialize_chains(CL, updatesigma=False)
        self.assertEqual(mcstat._MCMC__chain.shape,
                         (mcstat.simulation_options.nsimu, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__chain.shape)))
        self.assertEqual(mcstat._MCMC__sschain.shape,
                         (mcstat.simulation_options.nsimu, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__sschain.shape)))
        self.assertEqual(mcstat._MCMC__s2chain, None,
                         msg=str('s2chain should be None -> {}'.format(mcstat._MCMC__s2chain)))

    def test_initialize_chain_updatesigma_1_nsos_2(self):
        CL = self.setup_CL()
        mcstat = gf.setup_initialize_chains(CL, nsos=2)
        self.assertEqual(mcstat._MCMC__chain.shape,
                         (mcstat.simulation_options.nsimu, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__chain.shape)))
        self.assertEqual(mcstat._MCMC__sschain.shape,
                         (mcstat.simulation_options.nsimu, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__sschain.shape)))
        self.assertEqual(mcstat._MCMC__s2chain.shape,
                         (mcstat.simulation_options.nsimu, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__s2chain.shape)))


# --------------------------
class ExpandChain(unittest.TestCase):

    @classmethod
    def setup_CL(cls):
        return {'theta': np.array([1.0, 2.0]), 'ss': 1.0, 'prior': 0.0, 'sigma2': 0.0}

    def test_expand_chain_updatesigma_1(self):
        CL = self.setup_CL()
        mcstat = gf.setup_initialize_chains(CL)
        mcstat._MCMC__expand_chains(nsimu=mcstat.simulation_options.nsimu,
                                    npar=mcstat.parameters.npar,
                                    nsos=mcstat.model_settings.nsos,
                                    updatesigma=mcstat.simulation_options.updatesigma)
        self.assertEqual(mcstat._MCMC__chain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__chain.shape)))
        self.assertEqual(mcstat._MCMC__sschain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__sschain.shape)))
        self.assertEqual(mcstat._MCMC__s2chain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__s2chain.shape)))

    def test_expand_chain_updatesigma_0(self):
        CL = self.setup_CL()
        mcstat = gf.setup_initialize_chains(CL, updatesigma=False)
        mcstat._MCMC__expand_chains(nsimu=mcstat.simulation_options.nsimu,
                                    npar=mcstat.parameters.npar,
                                    nsos=mcstat.model_settings.nsos,
                                    updatesigma=mcstat.simulation_options.updatesigma)
        self.assertEqual(mcstat._MCMC__chain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__chain.shape)))
        self.assertEqual(mcstat._MCMC__sschain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__sschain.shape)))
        self.assertEqual(mcstat._MCMC__s2chain, None,
                         msg=str('s2chain should be None -> {}'.format(mcstat._MCMC__s2chain)))

    def test_expand_chain_updatesigma_1_nsos_2(self):
        CL = self.setup_CL()
        mcstat = gf.setup_initialize_chains(CL, nsos=2)
        mcstat._MCMC__expand_chains(nsimu=mcstat.simulation_options.nsimu,
                                    npar=mcstat.parameters.npar,
                                    nsos=mcstat.model_settings.nsos,
                                    updatesigma=mcstat.simulation_options.updatesigma)
        self.assertEqual(mcstat._MCMC__chain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__chain.shape)))
        self.assertEqual(mcstat._MCMC__sschain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__sschain.shape)))
        self.assertEqual(mcstat._MCMC__s2chain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__s2chain.shape)))


# --------------------------
class SetupSimulator(unittest.TestCase):
    def test_setup_simu_use_prev_false(self):
        mcstat = gf.setup_mcmc_case_cp(initialize=False)
        mcstat._MCMC__setup_simulator(use_previous_results=False)
        self.assertEqual(mcstat._MCMC__chain_index, 0, msg='Chain index should be 0')
        self.assertEqual(mcstat._MCMC__chain.shape, (mcstat.simulation_options.nsimu, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__chain.shape)))
        self.assertEqual(mcstat._MCMC__sschain.shape, (mcstat.simulation_options.nsimu, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__sschain.shape)))
        self.assertEqual(mcstat._MCMC__s2chain.shape, (mcstat.simulation_options.nsimu, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__s2chain.shape)))

    @patch('pymcmcstat.structures.ResultsStructure.ResultsStructure.load_json_object',
           return_value={'parind': np.array([0, 1, 2], dtype=int),
                         'names': ['m', 'b', 'b2'], 'local': np.zeros([3]),
                         'theta': np.array([0.2, 0.5, 0.7]),
                         'qcov': np.array([[0.2, 0.1, 0.05], [0.1, 0.4, 0.02], [0.05, 0.02, 0.6]])})
    def test_setup_simu_use_json_file(self, mock_json_object):
        mcstat = gf.setup_mcmc_case_cp(initialize=False)
        mcstat.simulation_options.json_restart_file = 1
        mcstat._MCMC__setup_simulator(use_previous_results=False)
        self.assertTrue(
                np.array_equal(mcstat.simulation_options.qcov,
                               np.array([[0.2, 0.1, 0.05], [0.1, 0.4, 0.02], [0.05, 0.02, 0.6]])),
                msg='Expect arrays to match')
        self.assertEqual(mcstat.parameters.parameters[0]['theta0'],
                         0.2, msg='Expect theta0 = 0.2')
        self.assertEqual(mcstat.parameters.parameters[1]['theta0'],
                         -5.0, msg='Expect theta0 = -5.0 because sample = 0')
        self.assertEqual(mcstat.parameters.parameters[2]['theta0'],
                         0.7, msg='Expect theta0 = 0.7')
        self.assertEqual(mcstat._MCMC__chain_index, 0, msg='Chain index should be 0')
        self.assertEqual(mcstat._MCMC__chain.shape,
                         (mcstat.simulation_options.nsimu, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__chain.shape)))
        self.assertEqual(mcstat._MCMC__sschain.shape,
                         (mcstat.simulation_options.nsimu, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__sschain.shape)))
        self.assertEqual(mcstat._MCMC__s2chain.shape,
                         (mcstat.simulation_options.nsimu, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__s2chain.shape)))

    def test_setup_simu_use_prev_true_causes_error(self):
        mcstat = gf.setup_mcmc_case_cp(initialize=False)
        with self.assertRaises(SystemExit, msg='No previous results exist'):
            mcstat._MCMC__setup_simulator(use_previous_results=True)

    def test_setup_simu_use_prev_true(self):
        mcstat = setup_pseudo_results(initialize=False)
        mcstat._MCMC__setup_simulator(use_previous_results=False)
        mcstat._MCMC__generate_simulation_results()
        mcstat._mcmc_status = True
        mcstat._MCMC__setup_simulator(use_previous_results=True)
        self.assertEqual(mcstat._MCMC__chain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 2),
                         msg=str('Shape should be (nsimu,2) -> {}'.format(mcstat._MCMC__chain.shape)))
        self.assertEqual(mcstat._MCMC__sschain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__sschain.shape)))
        self.assertEqual(mcstat._MCMC__s2chain.shape,
                         (mcstat.simulation_options.nsimu*2 - 1, 1),
                         msg=str('Shape should be (nsimu,1) -> {}'.format(mcstat._MCMC__s2chain.shape)))


# --------------------------
class GenerateSimulationResults(unittest.TestCase):
    def test_results_generation_ntry_gt_1(self):
        mcstat = setup_pseudo_results(initialize=False)
        mcstat._MCMC__setup_simulator(use_previous_results=False)
        mcstat._MCMC__generate_simulation_results()
        results = mcstat.simulation_results.results
        self.assertTrue(mcstat.simulation_results.basic, msg='Basic successfully added if true')
        self.assertTrue(np.array_equal(results['R'], mcstat._covariance._R), msg='Arrays should match')
        self.assertTrue(np.array_equal(results['cov'], mcstat._covariance._covchain), msg='Arrays should match')
        check_for_these = ['simulation_options', 'model_settings',
                           'chain', 's2chain', 'sschain', 'drscale', 'iacce', 'RDR']
        for cft in check_for_these:
            self.assertTrue(cft in results, msg=str('{} assigned successfully'.format(cft)))


# ------------------------------------------------
class SaveToLogFile(unittest.TestCase):
    def test_no_save_to_log_file(self):
        mcstat = gf.basic_mcmc()
        mcstat.simulation_options.save_to_bin = False
        mcstat.simulation_options.save_to_txt = False
        tmpfolder = gf.generate_temp_folder()
        mcstat.simulation_options.savedir = tmpfolder
        chains = []
        chains.append(dict(file='chain', mtx=np.random.random_sample((1000, 3))))
        savecount, lastbin = mcstat._MCMC__save_to_log_file(chains=chains, start=0, end=100)
        self.assertEqual(savecount, 0, msg='Expect 0')
        self.assertEqual(lastbin, 100, msg='Expect lastbin = end = 100')
        self.assertFalse(os.path.isdir(tmpfolder), msg=str('Folder exists: {}'.format(tmpfolder)))

    def test_save_to_log_file_bin(self):
        mcstat = gf.basic_mcmc()
        mcstat.simulation_options.save_to_bin = True
        mcstat.simulation_options.save_to_txt = False
        tmpfolder = gf.generate_temp_folder()
        mcstat.simulation_options.savedir = tmpfolder
        chains = []
        chains.append(dict(file='chain', mtx=np.random.random_sample((1000, 3))))
        savecount, lastbin = mcstat._MCMC__save_to_log_file(chains=chains, start=0, end=100)
        self.assertEqual(savecount, 0, msg='Expect 0')
        self.assertEqual(lastbin, 100, msg='Expect lastbin = end = 100')
        shutil.rmtree(tmpfolder)

    def test_save_to_log_file_txt(self):
        mcstat = gf.basic_mcmc()
        mcstat.simulation_options.save_to_bin = False
        mcstat.simulation_options.save_to_txt = True
        tmpfolder = gf.generate_temp_folder()
        mcstat.simulation_options.savedir = tmpfolder
        chains = []
        chains.append(dict(file='chain', mtx=np.random.random_sample((1000, 3))))
        savecount, lastbin = mcstat._MCMC__save_to_log_file(chains=chains, start=0, end=100)
        self.assertEqual(savecount, 0, msg='Expect 0')
        self.assertEqual(lastbin, 100, msg='Expect lastbin = end = 100')
        shutil.rmtree(tmpfolder)

    def test_save_to_log_file_bin_no_append(self):
        mcstat = gf.basic_mcmc()
        mcstat.simulation_options.save_to_bin = True
        mcstat.simulation_options.save_to_txt = False

        tmpfolder = gf.generate_temp_folder()
        mcstat.simulation_options.savedir = tmpfolder
        tmpfile = tmpfolder + os.sep + 'binlogfile.txt'
        chains = []
        chains.append(dict(file='chain', mtx=np.random.random_sample((1000, 3))))
        savecount, lastbin = mcstat._MCMC__save_to_log_file(chains=chains, start=0, end=100, append_to_log=False)
        self.assertFalse(os.path.isfile(tmpfile), msg=str('File exists: {}'.format(tmpfile)))
        shutil.rmtree(tmpfolder)

    def test_save_to_log_file_txt_no_append(self):
        mcstat = gf.basic_mcmc()
        mcstat.simulation_options.save_to_bin = False
        mcstat.simulation_options.save_to_txt = True

        tmpfolder = gf.generate_temp_folder()
        mcstat.simulation_options.savedir = tmpfolder
        tmpfile = tmpfolder + os.sep + 'txtlogfile.txt'
        chains = []
        chains.append(dict(file='chain', mtx=np.random.random_sample((1000, 3))))
        savecount, lastbin = mcstat._MCMC__save_to_log_file(chains=chains, start=0, end=100, append_to_log=False)
        self.assertFalse(os.path.isfile(tmpfile), msg=str('File exists: {}'.format(tmpfile)))
        shutil.rmtree(tmpfolder)

    def test_covmtx_save_to_log_file(self):
        mcstat = gf.setup_case()
        mcstat.simulation_options.save_to_bin = False
        mcstat.simulation_options.save_to_txt = True
        tmpfolder = gf.generate_temp_folder()
        mcstat.simulation_options.savedir = tmpfolder
        tmpfile = tmpfolder + os.sep + 'txtlogfile.txt'
        tmptxtfile = tmpfolder + os.sep + 'covchainfile.txt'
        savecount, lastbin = mcstat._MCMC__save_to_log_file(
                chains=[dict(mtx=np.dot(mcstat._covariance._R.transpose(), mcstat._covariance._R))],
                start=0, end=100, covmtx=True)
        self.assertEqual(savecount, 0, msg='Expect 0')
        self.assertEqual(lastbin, 100, msg='Expect lastbin = end = 100')
        self.assertTrue(os.path.isfile(tmpfile), msg=str('File exists: {}'.format(tmpfile)))
        self.assertTrue(os.path.isfile(tmptxtfile), msg=str('File exists: {}'.format(tmptxtfile)))
        mcstat.simulation_options.save_to_bin = True
        mcstat.simulation_options.save_to_txt = False
        tmpfile = tmpfolder + os.sep + 'binlogfile.txt'
        tmpbinfile = tmpfolder + os.sep + 'covchainfile.h5'
        savecount, lastbin = mcstat._MCMC__save_to_log_file(
                chains=[dict(mtx=np.dot(mcstat._covariance._R.transpose(), mcstat._covariance._R))],
                start=0, end=100, covmtx=True)
        self.assertEqual(savecount, 0, msg='Expect 0')
        self.assertEqual(lastbin, 100, msg='Expect lastbin = end = 100')
        self.assertTrue(os.path.isfile(tmpfile), msg=str('File exists: {}'.format(tmpfile)))
        self.assertTrue(os.path.isfile(tmpbinfile), msg=str('File exists: {}'.format(tmpbinfile)))
        shutil.rmtree(tmpfolder)


# --------------------------------------------------------
class RunSimulation(unittest.TestCase):
    def test_run_simulation(self):
        mcstat = gf.basic_mcmc()
        mcstat.simulation_options.nsimu = 100
        mcstat.simulation_options.save_to_bin = False
        mcstat.simulation_options.save_to_txt = False
        tmpfolder = gf.generate_temp_folder()
        mcstat.simulation_options.savedir = tmpfolder
        mcstat.run_simulation()
        self.assertTrue(mcstat._mcmc_status, msg='Expect True if successfully run')
        check_these = ['mcmcplot', 'PI', 'chainstats']
        for ci in check_these:
            self.assertTrue(hasattr(mcstat, ci), msg=str('object has attribute: {}'.format(ci)))

    def test_run_simulation_with_json(self):
        mcstat = gf.basic_mcmc()
        mcstat.simulation_options.nsimu = 100
        mcstat.simulation_options.save_to_bin = False
        mcstat.simulation_options.save_to_txt = False
        tmpfile = gf.generate_temp_file(extension='json')
        tmpfolder = gf.generate_temp_folder()
        os.mkdir(tmpfolder)
        mcstat.simulation_options.savedir = tmpfolder
        mcstat.simulation_options.results_filename = tmpfile
        mcstat.simulation_options.save_to_json = True
        mcstat.run_simulation()
        self.assertTrue(mcstat._mcmc_status, msg='Expect True if successfully run')
        check_these = ['mcmcplot', 'PI', 'chainstats']
        for ci in check_these:
            self.assertTrue(hasattr(mcstat, ci), msg=str('object has attribute: {}'.format(ci)))
        shutil.rmtree(tmpfolder)

    def test_run_simulation_verbose(self):
        mcstat = gf.basic_mcmc()
        mcstat.simulation_options.nsimu = 200
        mcstat.simulation_options.save_to_bin = False
        mcstat.simulation_options.save_to_txt = False
        tmpfolder = gf.generate_temp_folder()
        mcstat.simulation_options.savedir = tmpfolder
        mcstat.simulation_options.verbosity = 20
        mcstat.run_simulation()
        self.assertTrue(mcstat._mcmc_status, msg='Expect True if successfully run')
        check_these = ['mcmcplot', 'PI', 'chainstats']
        for ci in check_these:
            self.assertTrue(hasattr(mcstat, ci), msg=str('object has attribute: {}'.format(ci)))


# --------------------------------------------------------
class CustomRun(unittest.TestCase):

    def test_run_simulation(self):
        mcstat = gf.basic_mcmc()
        mcstat.simulation_options.nsimu = 100
        mcstat.simulation_options.save_to_bin = False
        mcstat.simulation_options.save_to_txt = False
        mcstat.custom_samplers.append(gf.CustomSampler(nsimu=100))
        tmpfolder = gf.generate_temp_folder()
        mcstat.simulation_options.savedir = tmpfolder
        mcstat.run_simulation()
        self.assertTrue(mcstat._mcmc_status, msg='Expect True if successfully run')
