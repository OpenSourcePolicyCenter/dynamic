'''
------------------------------------------------------------------------
Last updated: 5/21/2015

Calculates steady state of OLG model with S age cohorts.

This py-file calls the following other file(s):
            income.py
            demographics.py
            tax_funcs.py
            OUTPUT/given_params.pkl
            OUTPUT/Saved_moments/wealth_data_moments_fit_{}.pkl
                name depends on which percentile
            OUTPUT/Saved_moments/labor_data_moments.pkl
            OUTPUT/income_demo_vars.pkl
            OUTPUT/Saved_moments/{}.pkl
                name depends on what iteration just ran
            OUTPUT/SS/d_inc_guess.pkl
                if calibrating the income tax to match the wealth tax

This py-file creates the following other file(s):
    (make sure that an OUTPUT folder exists)
            OUTPUT/income_demo_vars.pkl
            OUTPUT/Saved_moments/{}.pkl
                name depends on what iteration is being run
            OUTPUT/Saved_moments/payroll_inputs.pkl
            OUTPUT/SSinit/ss_init.pkl
------------------------------------------------------------------------
'''

# Packages
import numpy as np
import time
import os
import scipy.optimize as opt
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats

import income
import demographics
import hh_focs
import tax_funcs as tax
reload(hh_focs)


'''
------------------------------------------------------------------------
Imported user given values
------------------------------------------------------------------------
S            = number of periods an individual lives
J            = number of different ability groups
T            = number of time periods until steady state is reached
lambdas_init  = percent of each age cohort in each ability group
starting_age = age of first members of cohort
ending age   = age of the last members of cohort
E            = number of cohorts before S=1
beta         = discount factor for each age cohort
sigma        = coefficient of relative risk aversion
alpha        = capital share of income
nu_init      = contraction parameter in steady state iteration process
               representing the weight on the new distribution gamma_new
Z            = total factor productivity parameter in firms' production
               function
delta        = depreciation rate of capital for each cohort
ltilde       = measure of time each individual is endowed with each
               period
eta          = Frisch elasticity of labor supply
g_y          = growth rate of technology for one cohort
TPImaxiter   = Maximum number of iterations that TPI will undergo
TPImindist   = Cut-off distance between iterations for TPI
b_ellipse    = value of b for elliptical fit of utility function
k_ellipse    = value of k for elliptical fit of utility function
slow_work    = time at which chi_n starts increasing from 1
mean_income_data  = mean income from IRS data file used to calibrate income tax
               (scalar)
a_tax_income = used to calibrate income tax (scalar)
b_tax_income = used to calibrate income tax (scalar)
c_tax_income = used to calibrate income tax (scalar)
d_tax_income = used to calibrate income tax (scalar)
tau_bq       = bequest tax (scalar)
tau_payroll  = payroll tax (scalar)
theta    = payback value for payroll tax (scalar)
retire       = age in which individuals retire(scalar)
h_wealth     = wealth tax parameter h
p_wealth     = wealth tax parameter p
m_wealth     = wealth tax parameter m
scal         = value to scale the initial guesses by in order to get the
               fsolve to converge
------------------------------------------------------------------------
'''

variables = pickle.load(open("OUTPUT/Saved_moments/wealth_data_moments_fit_25.pkl", "r"))
for key in variables:
    globals()[key] = variables[key]
top25 = highest_wealth_data_new
top25[2:26] = 500.0

variables = pickle.load(open("OUTPUT/Saved_moments/wealth_data_moments_fit_50.pkl", "r"))
for key in variables:
    globals()[key] = variables[key]
top50 = highest_wealth_data_new

variables = pickle.load(open("OUTPUT/Saved_moments/wealth_data_moments_fit_70.pkl", "r"))
for key in variables:
    globals()[key] = variables[key]
top70 = highest_wealth_data_new

variables = pickle.load(open("OUTPUT/Saved_moments/wealth_data_moments_fit_80.pkl", "r"))
for key in variables:
    globals()[key] = variables[key]
top80 = highest_wealth_data_new

variables = pickle.load(open("OUTPUT/Saved_moments/wealth_data_moments_fit_90.pkl", "r"))
for key in variables:
    globals()[key] = variables[key]
top90 = highest_wealth_data_new

variables = pickle.load(open("OUTPUT/Saved_moments/wealth_data_moments_fit_99.pkl", "r"))
for key in variables:
    globals()[key] = variables[key]
top99 = highest_wealth_data_new

variables = pickle.load(open("OUTPUT/Saved_moments/wealth_data_moments_fit_100.pkl", "r"))
for key in variables:
    globals()[key] = variables[key]
top100 = highest_wealth_data_new



variables = pickle.load(open("OUTPUT/Saved_moments/labor_data_moments.pkl", "r"))
for key in variables:
    globals()[key] = variables[key]

variables = pickle.load(open("OUTPUT/given_params.pkl", "r"))
for key in variables:
    globals()[key] = variables[key]


'''
------------------------------------------------------------------------
Generate income and demographic parameters
------------------------------------------------------------------------
e            = S x J matrix of age dependent possible working abilities
               e_s
omega        = T x S x J array of demographics
g_n          = steady state population growth rate
omega_SS     = steady state population distribution
surv_rate    = S x 1 array of survival rates
rho    = S x 1 array of mortality rates
------------------------------------------------------------------------
'''

if SS_stage == 'first_run_for_guesses':
    # These values never change, so only run it once
    omega, g_n, omega_SS, surv_rate = demographics.get_omega(
        S, J, T, lambdas, starting_age, ending_age, E)
    e = income.get_e(S, J, starting_age, ending_age, lambdas, omega_SS)
    rho = 1-surv_rate
    var_names = ['omega', 'g_n', 'omega_SS', 'surv_rate', 'e', 'rho']
    dictionary = {}
    for key in var_names:
        dictionary[key] = globals()[key]
    pickle.dump(dictionary, open("OUTPUT/income_demo_vars.pkl", "w"))
else:
    variables = pickle.load(open("OUTPUT/income_demo_vars.pkl", "r"))
    for key in variables:
        globals()[key] = variables[key]


chi_n_guess = np.array([47.12000874 , 22.22762421 , 14.34842241 , 10.67954008 ,  8.41097278
 ,  7.15059004 ,  6.46771332 ,  5.85495452 ,  5.46242013 ,  5.00364263
 ,  4.57322063 ,  4.53371545 ,  4.29828515 ,  4.10144524 ,  3.8617942  ,  3.57282
 ,  3.47473172 ,  3.31111347 ,  3.04137299 ,  2.92616951 ,  2.58517969
 ,  2.48761429 ,  2.21744847 ,  1.9577682  ,  1.66931057 ,  1.6878927
 ,  1.63107201 ,  1.63390543 ,  1.5901486  ,  1.58143606 ,  1.58005578
 ,  1.59073213 ,  1.60190899 ,  1.60001831 ,  1.67763741 ,  1.70451784
 ,  1.85430468 ,  1.97291208 ,  1.97017228 ,  2.25518398 ,  2.43969757
 ,  3.21870602 ,  4.18334822 ,  4.97772026 ,  6.37663164 ,  8.65075992
 ,  9.46944758 , 10.51634777 , 12.13353793 , 11.89186997 , 12.07083882
 , 13.2992811  , 14.07987878 , 14.19951571 , 14.97943562 , 16.05601334
 , 16.42979341 , 16.91576867 , 17.62775142 , 18.4885405  , 19.10609921
 , 20.03988031 , 20.86564363 , 21.73645892 , 22.6208256  , 23.37786072
 , 24.38166073 , 25.22395387 , 26.21419653 , 27.05246704 , 27.86896121
 , 28.90029708 , 29.83586775 , 30.87563699 , 31.91207845 , 33.07449767
 , 34.27919965 , 35.57195873 , 36.95045988 , 38.62308152])


rho[-1] = 1


def HH_solve(guesses, r, w, bq, T_H, params):
    '''
    Parameters: Steady state interest rate, wage rate, distribution of bequests
                government transfers  

    Returns:    1) Array of 2*S*J Euler equation errors
                2) Values for asset holdings, labor supply, and consumption from
                   FOCS
    '''
    chi_b = np.tile(np.array(params[:J]).reshape(1, J), (S, 1))
    chi_n = np.array(params[J:])
    chi_b = np.tile(np.array(params[:J]).reshape(1, J), (S, 1))
    chi_n = np.array(params[J:])
       
    BQ = (bq * omega_SS).sum(0)
  
    b_guess = guesses[0: S * J].reshape((S, J))
    n_guess = guesses[S * J:-1].reshape((S, J))  
    
    error1 = hh_focs.Euler1(w, r, e, n_guess, BQ, T_H, chi_b, rho)
    error2 = hh_focs.Euler2(w, r, e, n_guess, BQ, T_H, chi_n)
    error3 = hh_focs.Euler3(w, r, e, n_guess, b_guess, BQ, chi_b, T_H)
    return list(error1.flatten()) + list(
        error2.flatten()) + list(error3.flatten())     


def Steady_State(guesses, params):
    '''
    Parameters: Steady state interest rate, wage rate, distribution of bequests
                government transfers  

    Returns:    Array of 2*S*J Euler equation errors
    '''
    
    
    b_guess_init = np.ones((S, J)) * .01 # should be better way to update these after run for first time...
    n_guess_init = np.ones((S, J)) * .99 * ltilde
    
    r = guesses[0]
    w = guesses[1]
    bq =guesses[2: 1 * J].reshape((1, J))
    T_H = guesses[-1]
    
    guesses =  list(b_guess_init.flatten()) + list(n_guess_init.flatten())  
    
    HH_solve_X2 = lambda x: HH_solve(x, r, w, bq, T_H, final_chi_b_params)
    b, n , c = opt.fsolve(HH_solve_X2, guesses, xtol=1e-13)
    
    Steady_State_X2 = lambda x: Steady_State(x, final_chi_b_params)
    
    solutions = opt.fsolve(Steady_State_X2, guesses, xtol=1e-13)
    
    chi_b = np.tile(np.array(params[:J]).reshape(1, J), (S, 1))
    chi_n = np.array(params[J:])
    r_guess = guesses[0]
    w_guess = guesses[1]
    bq_guess =guesses[2: 1 * J].reshape((1, J))
    T_H_guess = guesses[-1]
    
    b_guess = guesses[0: S * J].reshape((S, J))
    B = (b_guess * omega_SS * rho.reshape(S, 1)).sum(0)
    K = (omega_SS * b_guess).sum()
    n_guess = guesses[S * J:-1].reshape((S, J))
    L = hh_focs.get_L(e, n_guess, omega_SS)
    Y = hh_focs.get_Y(K, L)
    w = hh_focs.get_w(Y, L)
    r = hh_focs.get_r(Y, K)
    BQ = (1 + r) * B
    b1 = np.array(list(np.zeros(J).reshape(1, J)) + list(b_guess[:-2, :]))
    b2 = b_guess[:-1, :]
    b3 = b_guess[1:, :]
    b1_2 = np.array(list(np.zeros(J).reshape(1, J)) + list(b_guess[:-1, :]))
    b2_2 = b_guess
    factor = guesses[-1]
    T_H = tax.tax_lump(r, b1_2, w, e, n_guess, BQ, lambdas, factor, omega_SS)
    error1 = hh_focs.Euler1(w, r, e, n_guess, b1, b2, b3, BQ, factor, T_H, chi_b, rho)
    error2 = hh_focs.Euler2(w, r, e, n_guess, b1_2, b2_2, BQ, factor, T_H, chi_n)
    error3 = hh_focs.Euler3(w, r, e, n_guess, b_guess, BQ, factor, chi_b, T_H)
    average_income_model = ((r * b1_2 + w * e * n_guess) * omega_SS).sum()
    error4 = [mean_income_data - factor * average_income_model]
    # Check and punish constraint violations
    mask1 = n_guess < 0
    error2[mask1] += 1e9
    mask2 = n_guess > ltilde
    error2[mask2] += 1e9
    if b_guess.sum() <= 0:
        error1 += 1e9
    tax1 = tax.total_taxes_SS(r, b1_2, w, e, n_guess, BQ, lambdas, factor, T_H)
    cons = hh_focs.get_cons(r, b1_2, w, e, n_guess, BQ.reshape(1, J), lambdas, b2_2, g_y, tax1)
    mask3 = cons < 0
    error2[mask3] += 1e9
    mask4 = b_guess[:-1] <= 0
    error1[mask4] += 1e9
    # print np.abs(np.array(list(error1.flatten()) + list(
    #     error2.flatten()) + list(error3.flatten()) + error4)).max()
    return list(error1.flatten()) + list(
        error2.flatten()) + list(error3.flatten()) + error4


def constraint_checker(bssmat, nssmat, cssmat):
    '''
    Parameters:
        bssmat = steady state distribution of capital ((S-1)xJ array)
        nssmat = steady state distribution of labor (SxJ array)
        wss    = steady state wage rate (scalar)
        rss    = steady state rental rate (scalar)
        e      = distribution of abilities (SxJ array)
        cssmat = steady state distribution of consumption (SxJ array)
        BQ     = bequests

    Created Variables:
        flag1 = False if all borrowing constraints are met, true
               otherwise.
        flag2 = False if all labor constraints are met, true otherwise

    Returns:
        # Prints warnings for violations of capital, labor, and
            consumption constraints.
    '''
    # print 'Checking constraints on capital, labor, and consumption.'
    flag1 = False
    if bssmat.sum() <= 0:
        print '\tWARNING: Aggregate capital is less than or equal to zero.'
        flag1 = True
    if flag1 is False:
        print '\tThere were no violations of the borrowing constraints.'
    flag2 = False
    if (nssmat < 0).any():
        print '\tWARNING: Labor supply violates nonnegativity constraints.'
        flag2 = True
    if (nssmat > ltilde).any():
        print '\tWARNING: Labor suppy violates the ltilde constraint.'
    if flag2 is False:
        print '\tThere were no violations of the constraints on labor supply.'
    if (cssmat < 0).any():
        print '\tWARNING: Consumption volates nonnegativity constraints.'
    else:
        print '\tThere were no violations of the constraints on consumption.'



'''
------------------------------------------------------------------------
    Run SS in various ways, depending on the stage of the simulation
------------------------------------------------------------------------
'''

bnds = tuple([(1e-6, None)] * (S + J))

if SS_stage == 'first_run_for_guesses':
    #b_guess_init = np.ones((S, J)) * .01
    #n_guess_init = np.ones((S, J)) * .99 * ltilde
    r_guess_init = 0.04 
    w_guess_init = 0.1
    bq_guess_init = np.ones((1, J)) * 0.001
    T_H_guess_init = 0.05
    #avIguess = ((rguess * b_guess_init + wguess * e * n_guess_init) * omega_SS).sum()
    #factor_guess = [mean_income_data / avIguess]
    guesses = r_guess_init + w_guess_init + list(bq_guess_init.flatten()) + 
              T_H_guess_init 
    chi_b_guesses = np.ones(S+J)
    chi_b_guesses[0:J] = np.array([5, 10, 90, 250, 250, 250, 250]) + chi_b_scal
    print 'Chi_b:', chi_b_guesses[0:J]
    chi_b_guesses[J:] = chi_n_guess
    chi_b_guesses = list(chi_b_guesses)
    final_chi_b_params = chi_b_guesses
    Steady_State_X2 = lambda x: Steady_State(x, final_chi_b_params)
    solutions = opt.fsolve(Steady_State_X2, guesses, xtol=1e-13)
    print np.array(Steady_State_X2(solutions)).max()
elif SS_stage == 'loop_calibration':
    variables = pickle.load(open("OUTPUT/Saved_moments/loop_calibration_solutions.pkl", "r"))
    for key in variables:
        globals()[key] = variables[key]
    guesses = list((solutions[:S*J].reshape(S, J) * scal.reshape(1, J)).flatten()) + list(
        solutions[S*J:-1].reshape(S, J).flatten()) + [solutions[-1]]
    chi_b_guesses = np.ones(S+J)
    chi_b_guesses[0:J] = np.array([5, 10, 90, 250, 250, 250, 250]) + chi_b_scal
    print 'Chi_b:', chi_b_guesses[0:J]
    chi_b_guesses[J:] = chi_n_guess
    chi_b_guesses = list(chi_b_guesses)
    final_chi_b_params = chi_b_guesses
    Steady_State_X2 = lambda x: Steady_State(x, final_chi_b_params)
    solutions = opt.fsolve(Steady_State_X2, guesses, xtol=1e-13)
    print np.array(Steady_State_X2(solutions)).max()
elif SS_stage == 'SS_init':
    variables = pickle.load(open("OUTPUT/Saved_moments/minimization_solutions.pkl", "r"))
    for key in variables:
        globals()[key] = variables[key]
    guesses = list((solutions[:S*J].reshape(S, J) * scal.reshape(1, J)).flatten()) + list(
        solutions[S*J:-1].reshape(S, J).flatten()) + [solutions[-1]]
    chi_b_guesses = final_chi_b_params
    Steady_State_X2 = lambda x: Steady_State(x, final_chi_b_params)
    solutions = opt.fsolve(Steady_State_X2, guesses, xtol=1e-13)
    print np.array(Steady_State_X2(solutions)).max()
elif SS_stage == 'SS_tax':
    variables = pickle.load(open("OUTPUT/Saved_moments/SS_init_solutions.pkl", "r"))
    for key in variables:
        globals()[key] = variables[key]
    guesses = list((solutions[:S*J].reshape(S, J) * scal.reshape(1, J)).flatten()) + list(
        solutions[S*J:-1].reshape(S, J).flatten()) + [solutions[-1]]
    chi_b_guesses = final_chi_b_params
    Steady_State_X2 = lambda x: Steady_State(x, final_chi_b_params)
    solutions = opt.fsolve(Steady_State_X2, guesses, xtol=1e-13)
    print np.array(Steady_State_X2(solutions)).max()


'''
------------------------------------------------------------------------
    Save the initial values in various ways, depending on the stage of
        the simulation
------------------------------------------------------------------------
'''

if SS_stage == 'first_run_for_guesses':
    var_names = ['solutions', 'final_chi_b_params']
    dictionary = {}
    for key in var_names:
        dictionary[key] = globals()[key]
    pickle.dump(dictionary, open("OUTPUT/Saved_moments/first_run_solutions.pkl", "w"))
    pickle.dump(dictionary, open("OUTPUT/Saved_moments/loop_calibration_solutions.pkl", "w"))
elif SS_stage == 'loop_calibration':
    var_names = ['solutions', 'final_chi_b_params']
    dictionary = {}
    for key in var_names:
        dictionary[key] = globals()[key]
    pickle.dump(dictionary, open("OUTPUT/Saved_moments/loop_calibration_solutions.pkl", "w"))
elif SS_stage == 'SS_init':
    var_names = ['solutions', 'final_chi_b_params']
    dictionary = {}
    for key in var_names:
        dictionary[key] = globals()[key]
    pickle.dump(dictionary, open("OUTPUT/Saved_moments/SS_init_solutions.pkl", "w"))
elif SS_stage == 'SS_tax':
    var_names = ['solutions', 'final_chi_b_params']
    dictionary = {}
    for key in var_names:
        dictionary[key] = globals()[key]
    pickle.dump(dictionary, open("OUTPUT/Saved_moments/SS_tax_solutions.pkl", "w"))


if SS_stage != 'first_run_for_guesses' and SS_stage != 'loop_calibration':
    bssmat = solutions[0:(S-1) * J].reshape(S-1, J)
    BQ = solutions[(S-1)*J:S*J]
    Bss = (np.array(list(bssmat) + list(BQ.reshape(1, J))).reshape(
        S, J) * omega_SS * rho.reshape(S, 1)).sum(0)
    bssmat2 = np.array(list(np.zeros(J).reshape(1, J)) + list(bssmat))
    bssmat3 = np.array(list(bssmat) + list(BQ.reshape(1, J)))
    Kss = (omega_SS[:-1, :] * bssmat).sum() + (omega_SS[-1, :]*BQ).sum()
    nssmat = solutions[S * J:-1].reshape(S, J)
    Lss = hh_focs.get_L(e, nssmat, omega_SS)
    Yss = hh_focs.get_Y(Kss, Lss)
    wss = hh_focs.get_w(Yss, Lss)
    rss = hh_focs.get_r(Yss, Kss)
    b1_2 = np.array(list(np.zeros(J).reshape((1, J))) + list(bssmat))
    factor_ss = solutions[-1]
    BQ = Bss * (1+rss)
    T_Hss = tax.tax_lump(rss, bssmat2, wss, e, nssmat, BQ, lambdas, factor_ss, omega_SS)
    taxss = tax.total_taxes_SS(rss, bssmat2, wss, e, nssmat, BQ, lambdas, factor_ss, T_Hss)
    cssmat = hh_focs.get_cons(rss, bssmat2, wss, e, nssmat, BQ.reshape(1, J), lambdas.reshape(1, J), bssmat3, g_y, taxss)

    constraint_checker(bssmat, nssmat, cssmat)

    '''
    ------------------------------------------------------------------------
    Generate variables for graphs
    ------------------------------------------------------------------------
    b1          = (S-1)xJ array of bssmat in period t-1
    b2          = copy of bssmat
    b3          = (S-1)xJ array of bssmat in period t+1
    b1_2        = SxJ array of bssmat in period t
    b2_2        = SxJ array of bssmat in period t+1
    euler1      = euler errors from first euler equation
    euler2      = euler errors from second euler equation
    euler3      = euler errors from third euler equation
    ------------------------------------------------------------------------
    '''
    b1 = np.array(list(np.zeros(J).reshape((1, J))) + list(bssmat[:-1, :]))
    b2 = bssmat
    b3 = np.array(list(bssmat[1:, :]) + list(BQ.reshape(1, J)))
    b1_2 = np.array(list(np.zeros(J).reshape((1, J))) + list(bssmat))
    b2_2 = np.array(list(bssmat) + list(BQ.reshape(1, J)))

    chi_b = np.tile(final_chi_b_params[:J].reshape(1, J), (S, 1))
    chi_n = np.array(final_chi_b_params[J:])
    euler1 = hh_focs.Euler1(wss, rss, e, nssmat, b1, b2, b3, BQ, factor_ss, T_Hss, chi_b, rho)
    euler2 = hh_focs.Euler2(wss, rss, e, nssmat, b1_2, b2_2, BQ, factor_ss, T_Hss, chi_n)
    euler3 = hh_focs.Euler3(wss, rss, e, nssmat, bssmat3, BQ, factor_ss, chi_b, T_Hss)

'''
------------------------------------------------------------------------
    Save the values in various ways, depending on the stage of
        the simulation, to be used in TPI or graphing functions
------------------------------------------------------------------------
'''
if SS_stage == 'constrained_minimization':
    bssmat_init = np.array(list(bssmat) + list(BQ.reshape(1, J)))
    nssmat_init = nssmat
    var_names = ['retire', 'nssmat_init', 'wss', 'factor_ss', 'e',
                 'J', 'omega_SS']
    dictionary = {}
    for key in var_names:
        dictionary[key] = globals()[key]
    pickle.dump(dictionary, open("OUTPUT/Saved_moments/payroll_inputs.pkl", "w"))
elif SS_stage == 'SS_init':
    bssmat_init = np.array(list(bssmat) + list(BQ.reshape(1, J)))
    nssmat_init = nssmat

    var_names = ['bssmat_init', 'nssmat_init']
    dictionary = {}
    for key in var_names:
        dictionary[key] = globals()[key]
    pickle.dump(dictionary, open("OUTPUT/SSinit/ss_init_tpi.pkl", "w"))

    var_names = ['S', 'beta', 'sigma', 'alpha', 'nu', 'Z', 'delta', 'e', 'E',
                 'J', 'Kss', 'bssmat', 'Lss', 'nssmat',
                 'Yss', 'wss', 'rss', 'omega', 'chi_n', 'chi_b', 'ltilde', 'T',
                 'g_n', 'g_y', 'omega_SS', 'TPImaxiter', 'TPImindist', 'BQ',
                 'rho', 'Bss', 'lambdas',
                 'b_ellipse', 'k_ellipse', 'upsilon',
                 'factor_ss',  'a_tax_income', 'b_tax_income',
                 'c_tax_income', 'd_tax_income', 'tau_payroll',
                 'tau_bq', 'theta', 'retire',
                 'mean_income_data', 'bssmat2', 'cssmat',
                 'starting_age', 'bssmat3',
                 'ending_age', 'T_Hss', 'euler1', 'euler2', 'euler3',
                 'h_wealth', 'p_wealth', 'm_wealth']
    dictionary = {}
    for key in var_names:
        dictionary[key] = globals()[key]
    pickle.dump(dictionary, open("OUTPUT/SSinit/ss_init.pkl", "w"))
elif SS_stage == 'SS_tax':
    var_names = ['S', 'beta', 'sigma', 'alpha', 'nu', 'Z', 'delta', 'e', 'E',
                 'J', 'Kss', 'bssmat', 'Lss', 'nssmat',
                 'Yss', 'wss', 'rss', 'omega',
                 'chi_n', 'chi_b', 'ltilde', 'T',
                 'g_n', 'g_y', 'omega_SS', 'TPImaxiter', 'TPImindist', 'BQ',
                 'rho', 'Bss', 'lambdas',
                 'b_ellipse', 'k_ellipse', 'upsilon',
                 'factor_ss',  'a_tax_income', 'b_tax_income',
                 'c_tax_income', 'd_tax_income', 'tau_payroll',
                 'tau_bq', 'theta', 'retire',
                 'mean_income_data', 'bssmat2', 'cssmat',
                 'starting_age', 'bssmat3',
                 'ending_age', 'euler1', 'euler2', 'euler3', 'T_Hss',
                 'h_wealth', 'p_wealth', 'm_wealth']
    dictionary = {}
    for key in var_names:
        dictionary[key] = globals()[key]
    pickle.dump(dictionary, open("OUTPUT/SS/ss_vars.pkl", "w"))

print('SS capital stock and interest rate')
print(Kss)
print(rss)