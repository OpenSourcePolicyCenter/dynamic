'''
Tests of parameter_plots.py module
'''

import pytest
import os
import numpy as np
import scipy.interpolate as si
from ogusa import utils, parameter_plots, income


# Load in test results and parameters
CUR_PATH = os.path.abspath(os.path.dirname(__file__))
base_params = utils.safe_read_pickle(
    os.path.join(CUR_PATH, 'test_io_data', 'model_params_baseline.pkl'))


def test_plot_imm_rates():
    fig = parameter_plots.plot_imm_rates(base_params)
    assert fig


def test_plot_mort_rates():
    fig = parameter_plots.plot_mort_rates(base_params)
    assert fig


def test_plot_pop_growth():
    fig = parameter_plots.plot_pop_growth(base_params)
    assert fig


def test_plot_ability_profiles():
    fig = parameter_plots.plot_ability_profiles(base_params)
    assert fig


def test_plot_elliptical_u():
    fig = parameter_plots.plot_elliptical_u(base_params)
    assert fig


def test_plot_chi_n():
    fig = parameter_plots.plot_chi_n(base_params)
    assert fig


def test_plot_population():
    fig = parameter_plots.plot_population(base_params)
    assert fig


def test_plot_fert_rates():
    totpers = base_params.S
    min_yr = 20
    max_yr = 100
    fert_data = (np.array([0.0, 0.0, 0.3, 12.3, 47.1, 80.7, 105.5, 98.0,
                           49.3, 10.4, 0.8, 0.0, 0.0]) / 2000)
    age_midp = np.array([9, 10, 12, 16, 18.5, 22, 27, 32, 37, 42, 47,
                         55, 56])
    fert_func = si.interp1d(age_midp, fert_data, kind='cubic')
    fert_rates = np.random.uniform(size=totpers)
    fig = parameter_plots.plot_fert_rates(
        fert_func, age_midp, totpers, min_yr, max_yr, fert_data,
        fert_rates)
    assert fig


def test_plot_mort_rates_data():
    totpers = base_params.S - 1
    min_yr = 21
    max_yr = 100
    age_year_all = np.arange(min_yr, max_yr)
    mort_rates = base_params.rho[1:]
    mort_rates_all = base_params.rho[1:]
    infmort_rate = base_params.rho[0]
    fig = parameter_plots.plot_mort_rates_data(
        totpers, min_yr, max_yr, age_year_all, mort_rates_all,
        infmort_rate, mort_rates, output_dir=None)
    assert fig


def test_plot_omega_fixed():
    E = 0
    S = base_params.S
    age_per_EpS = np.arange(21, S + 21)
    omega_SS_orig = base_params.omega_SS
    omega_SSfx = base_params.omega_SS
    fig = parameter_plots.plot_omega_fixed(
        age_per_EpS, omega_SS_orig, omega_SSfx, E, S)
    assert fig


def test_plot_imm_fixed():
    E = 0
    S = base_params.S
    age_per_EpS = np.arange(21, S + 21)
    imm_rates_orig = base_params.imm_rates[0, :]
    imm_rates_adj = base_params.imm_rates[-1, :]
    fig = parameter_plots.plot_imm_fixed(
        age_per_EpS, imm_rates_orig, imm_rates_adj, E, S)
    assert fig


def test_plot_population_path():
    E = 0
    S = base_params.S
    age_per_EpS = np.arange(21, S + 21)
    pop_2013_pct = base_params.omega[0, :]
    omega_path_lev = base_params.omega.T
    omega_SSfx = base_params.omega_SS
    curr_year = base_params.start_year
    fig = parameter_plots.plot_population_path(
        age_per_EpS, pop_2013_pct, omega_path_lev, omega_SSfx,
        curr_year, E, S)
    assert fig


# TODO:
# gen_3Dscatters_hist
# txfunc_graph
# txfunc_sse_plot


def test_plot_income_data():
    ages = np.linspace(20 + 0.5, 100 - 0.5, 80)
    abil_midp = np.array([0.125, 0.375, 0.6, 0.75, 0.85, 0.945, 0.995])
    abil_pcts = np.array([0.25, 0.25, 0.2, 0.1, 0.1, 0.09, 0.01])
    age_wgts = np.ones(80) * 1 / 80
    emat = income.get_e_orig(age_wgts, abil_pcts)
    fig = parameter_plots.plot_income_data(
        ages, abil_midp, abil_pcts, emat)

    assert fig
