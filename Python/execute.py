'''
A 'smoke test' for the ogusa package. Uses a fake data set to run the
baseline
'''

import cPickle as pickle
import os
import numpy as np
import time

import ogusa
ogusa.parameters.DATASET = 'SMALL'


def runner(output_base, input_dir, baseline=False, reform={}, user_params={}, guid='', run_micro=True):


    from ogusa import parameters, wealth, labor, demographics, income
    from ogusa import txfunc

    tick = time.time()

    if run_micro:
        txfunc.get_tax_func_estimate(baseline=baseline, reform=reform, guid=guid)
    print ("in runner, baseline is ", baseline)
    run_params = ogusa.parameters.get_parameters(baseline=baseline, guid=guid)

    # Modify ogusa parameters based on user input
    if 'frisch' in user_params:
        b_ellipse, upsilon = ogusa.elliptical_u_est.estimation(user_params['frisch'],
                                                               run_params['ltilde'])
        run_params.update(user_params)
        run_params['b_ellipse'] = b_ellipse
        run_params['upsilon'] = upsilon

    globals().update(run_params)

    from ogusa import SS, TPI
    #Create output directory structure
    saved_moments_dir = os.path.join(output_base, "Saved_moments")
    ssinit_dir = os.path.join(output_base, "SSinit")
    tpiinit_dir = os.path.join(output_base, "TPIinit")
    #dirs = ["./OUTPUT/Saved_moments", "./OUTPUT/SSinit", "./OUTPUT/TPIinit"]
    dirs = [saved_moments_dir, ssinit_dir, tpiinit_dir]
    for _dir in dirs:
        try:
            os.makedirs(_dir)
        except OSError as oe:
            pass

    # Generate Wealth data moments
    wealth.get_wealth_data(lambdas, J, flag_graphs, output_dir=input_dir)

    # Generate labor data moments
    labor.labor_data_moments(flag_graphs, output_dir=input_dir)

    
    get_baseline = True
    calibrate_model = False
    # List of parameter names that will not be changing (unless we decide to
    # change them for a tax experiment)

    param_names = ['S', 'J', 'T', 'BW', 'lambdas', 'starting_age', 'ending_age',
                'beta', 'sigma', 'alpha', 'nu', 'Z', 'delta', 'E',
                'ltilde', 'g_y', 'maxiter', 'mindist_SS', 'mindist_TPI',
                'b_ellipse', 'k_ellipse', 'upsilon',
                'chi_b_guess', 'chi_n_guess','etr_params','mtrx_params',
                'mtry_params','tau_payroll', 'tau_bq', 'calibrate_model',
                'retire', 'mean_income_data', 'g_n_vector',
                'h_wealth', 'p_wealth', 'm_wealth', 'get_baseline',
                'omega', 'g_n_ss', 'omega_SS', 'surv_rate', 'e', 'rho']


    '''
    ------------------------------------------------------------------------
        Run SS with minimization to fit chi_b and chi_n
    ------------------------------------------------------------------------
    '''

    # This is the simulation before getting the replacement rate values
    sim_params = {}
    glbs = globals()
    lcls = locals()
    for key in param_names:
        if key in glbs:
            sim_params[key] = glbs[key]
        else:
            sim_params[key] = lcls[key]

    sim_params['output_dir'] = input_dir
    sim_params['run_params'] = run_params

    income_tax_params, wealth_tax_params, ellipse_params, ss_parameters, iterative_params = SS.create_steady_state_parameters(**sim_params)

    ss_outputs = SS.run_steady_state(income_tax_params, ss_parameters, iterative_params, get_baseline, calibrate_model, output_dir=input_dir)

    '''
    ------------------------------------------------------------------------
        Run the baseline TPI simulation
    ------------------------------------------------------------------------
    '''

    ss_outputs['get_baseline'] = get_baseline
    sim_params['input_dir'] = input_dir
    income_tax_params, wealth_tax_params, ellipse_params, parameters, N_tilde, omega_stationary, K0, b_sinit, \
    b_splus1init, L0, Y0, w0, r0, BQ0, T_H_0, tax0, c0, initial_b, initial_n = TPI.create_tpi_params(**sim_params)
    ss_outputs['income_tax_params'] = income_tax_params
    ss_outputs['wealth_tax_params'] = wealth_tax_params
    ss_outputs['ellipse_params'] = ellipse_params
    ss_outputs['parameters'] = parameters
    ss_outputs['N_tilde'] = N_tilde
    ss_outputs['omega_stationary'] = omega_stationary
    ss_outputs['K0'] = K0
    ss_outputs['b_sinit'] = b_sinit
    ss_outputs['b_splus1init'] = b_splus1init
    ss_outputs['L0'] = L0
    ss_outputs['Y0'] = Y0
    ss_outputs['r0'] = r0
    ss_outputs['BQ0'] = BQ0
    ss_outputs['T_H_0'] = T_H_0
    ss_outputs['tax0'] = tax0
    ss_outputs['c0'] = c0
    ss_outputs['initial_b'] = initial_b
    ss_outputs['initial_n'] = initial_n
    ss_outputs['tau_bq'] = tau_bq
    ss_outputs['g_n_vector'] = g_n_vector
    ss_outputs['output_dir'] = input_dir


    with open("ss_outputs.pkl", 'wb') as fp:
        pickle.dump(ss_outputs, fp)

    w_path, r_path, T_H_path, BQ_path, Y_path = TPI.run_time_path_iteration(**ss_outputs)


    print "getting to here...."
    TPI.TP_solutions(w_path, r_path, T_H_path, BQ_path, **ss_outputs)
    print "took {0} seconds to get that part done.".format(time.time() - tick)
