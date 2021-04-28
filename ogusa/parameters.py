import os
import numpy as np
import scipy.interpolate as si
import pkg_resources
import paramtools

# import ogusa
from ogusa import elliptical_u_est
from ogusa.utils import rate_conversion
from ogusa.constants import BASELINE_DIR, TC_LAST_YEAR
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


class Specifications(paramtools.Parameters):
    '''
    Inherits ParamTools Parameters abstract base class.
    '''
    defaults = os.path.join(CURRENT_PATH, "default_parameters.json")
    array_first = True

    def __init__(self,
                 run_micro=False,
                 output_base=BASELINE_DIR, baseline_dir=BASELINE_DIR,
                 test=False, time_path=True, baseline=False, guid='',
                 client=None, num_workers=1):
        super().__init__()

        self.output_base = output_base
        self.baseline_dir = baseline_dir
        self.test = test
        self.time_path = time_path
        self.baseline = baseline
        self.guid = guid
        self.num_workers = num_workers

        # put OG-USA version in parameters to save for reference
        self.ogusa_version = pkg_resources.get_distribution("ogusa").version

        # does cheap calculations to find parameter values
        self.initialize()

        self.parameter_warnings = ''
        self.parameter_errors = ''
        self._ignore_errors = False

    def initialize(self):
        '''
        ParametersBase reads JSON file and sets attributes to self
        Next call self.compute_default_params for further initialization

        Args:
            None

        Returns:
            None

        '''

        if self.test:
            # Make smaller statespace for testing
            self.S = int(40)
            self.lambdas = np.array([0.6, 0.4]).reshape(2, 1)
            self.J = self.lambdas.shape[0]
            self.eta = np.ones((self.S, self.J)) / (self.S * self.J)
            self.maxiter = 35
            self.mindist_SS = 1e-6
            self.mindist_TPI = 1e-3
            self.nu = .4

        self.compute_default_params()

    def compute_default_params(self):
        '''
        Does cheap calculations to return parameter values

        Args:
            None

        Returns:
            None

        '''
        # reshape lambdas
        self.lambdas = self.lambdas.reshape(self.lambdas.shape[0], 1)
        # cast integers as integers
        self.S = int(self.S)
        self.T = int(self.T)
        self.J = len(self.lambdas)

        # get parameters of elliptical utility function
        self.b_ellipse, self.upsilon = elliptical_u_est.estimation(
            self.frisch, self.ltilde)
        # determine length of budget window from start year and last
        # year in TC
        self.BW = int(TC_LAST_YEAR - self.start_year + 1)
        # Find number of economically active periods of life
        self.E = int(
            self.starting_age * (self.S / (self.ending_age -
                                           self.starting_age)))
        # Find rates in model periods from annualized rates
        self.beta = (
            1 / (rate_conversion(1 / self.beta_annual - 1,
                                 self.starting_age, self.ending_age,
                                 self.S) + 1))
        self.delta = (
            -1 * rate_conversion(-1 * self.delta_annual,
                                 self.starting_age, self.ending_age,
                                 self.S))
        self.g_y = rate_conversion(self.g_y_annual, self.starting_age,
                                   self.ending_age, self.S)

        # set fraction of income taxes from payroll to zero initially
        # will be updated when function tax function parameters
        self.frac_tax_payroll = np.zeros(self.T + self.S)

        # Extend parameters that may vary over the time path
        tp_param_list = [
            'alpha_G', 'alpha_T', 'Z', 'world_int_rate_annual',
            'delta_tau_annual', 'cit_rate',
            'adjustment_factor_for_cit_receipts', 'tau_bq',
            'tau_payroll', 'h_wealth', 'm_wealth', 'p_wealth',
            'retirement_age', 'replacement_rate_adjust', 'zeta_D',
            'zeta_K']
        for item in tp_param_list:
            this_attr = getattr(self, item)
            if this_attr.ndim > 1:
                this_attr = np.squeeze(this_attr, axis=1)
            # the next if statement is a quick fix to avoid having to
            # update all these time varying parameters if change T or S
            # ideally, the default json values are read in again and the
            # extension done is here done again with those defaults and
            # the new T and S values...
            if this_attr.size > self.T + self.S:
                this_attr = this_attr[:self.T + self.S]
            this_attr = np.concatenate((
                this_attr, np.ones((self.T + self.S - this_attr.size)) *
                this_attr[-1]))
            setattr(self, item, this_attr)
        # Try to deal with size of tau_c, but don't worry too much at
        # this point, will change when we determine how calibrate and if
        # add multiple consumption goods.
        tau_c_to_set = getattr(self, 'tau_c')
        if tau_c_to_set.size == 1:
            setattr(self, 'tau_c', np.ones((self.T + self.S, self.S,
                                            self.J)) * tau_c_to_set)
        elif tau_c_to_set.ndim == 3:
            if tau_c_to_set.shape[0] > self.T + self.S:
                tau_c_to_set = tau_c_to_set[:self.T + self.S, :, :]
            if tau_c_to_set.shape[1] > self.S:
                tau_c_to_set = tau_c_to_set[:, :self.S, :]
            if tau_c_to_set.shape[2] > self.J:
                tau_c_to_set = tau_c_to_set[:, :, :self.J]
            setattr(self, 'tau_c',  tau_c_to_set)
        else:
            print('please give a tau_c that is a single element or 3-D array')
            assert False

        # Try to deal with size of eta.  It may vary by S, J, T, but
        # want to allow user to enter one that varies by only S, S and J,
        # S and T, or T and S and J.
        eta_to_set = getattr(self, 'eta')
        # this is the case that vary only by S
        if eta_to_set.ndim == 1:
            assert eta_to_set.shape[0] == self.S
            eta_to_set = np.tile(
                (np.tile(eta_to_set.reshape(self.S, 1), (1, self.J)) /
                 self.J).reshape(1, self.S, self.J),
                (self.T + self.S, 1, 1))
        # this could be where vary by S and J or T and S
        elif eta_to_set.ndim == 2:
            # case if S by J input
            if eta_to_set.shape[0] == self.S:
                eta_to_set = np.tile(
                    eta_to_set.reshape(1, self.S, self.J),
                    (self.T + self.S, 1, 1))
                eta_to_set = eta_to_set = np.concatenate(
                    (eta_to_set,
                     np.tile(eta_to_set[-1, :, :].reshape(1, self.S, self.J),
                             (self.S, 1, 1))), axis=0)
            # case if T by S input
            elif eta_to_set.shape[0] == self.T:
                eta_to_set = (np.tile(
                    eta_to_set.reshape(self.T, self.S, 1),
                    (1, 1, self.J)) / self.J)
                eta_to_set = eta_to_set = np.concatenate(
                    (eta_to_set,
                     np.tile(eta_to_set[-1, :, :].reshape(1, self.S, self.J),
                             (self.S, 1, 1))), axis=0)
            else:
                print('please give an eta that is either SxJ or TxS')
                assert False
        # this is the case where vary by S, J, T
        elif eta_to_set.ndim == 3:
            eta_to_set = eta_to_set = np.concatenate(
                (eta_to_set,
                 np.tile(eta_to_set[-1, :, :].reshape(1, self.S, self.J),
                         (self.S, 1, 1))), axis=0)
        setattr(self, 'eta',  eta_to_set)

        # make sure zeta matrix sums to one (e.g., default off due to rounding)
        self.zeta = self.zeta / self.zeta.sum()

        # open economy parameters
        self.world_int_rate = rate_conversion(
            self.world_int_rate_annual, self.starting_age,
            self.ending_age, self.S)

        # set period of retirement
        self.retire = (np.round(((self.retirement_age -
                                  self.starting_age) * self.S) /
                                80.0) - 1).astype(int)

        # Calculations for business income taxes
        # at some point, we will want to make Cost of Capital Calculator
        # a dependency to compute tau_b
        # this adjustment factor has as the numerator CIT receipts/GDP
        # and as the demoninator CIT receipts/GDP from the
        # model with baseline parameterization and no adjustment to the
        # CIT_rate
        self.tau_b = (self.cit_rate * self.c_corp_share_of_assets *
                      self.adjustment_factor_for_cit_receipts)
        self.delta_tau = (
            -1 * rate_conversion(-1 * self.delta_tau_annual,
                                 self.starting_age, self.ending_age,
                                 self.S))

        # for constant demographics
        if self.constant_demographics:
            self.g_n_ss = 0.0
            self.g_n = np.zeros(self.T + self.S)
            surv_rate1 = np.ones((self.S, ))  # prob start at age S
            surv_rate1[1:] = np.cumprod(self.surv_rate[:-1], dtype=float)
            # number of each age alive at any time
            omega_SS = np.ones(self.S) * surv_rate1
            self.omega_SS = omega_SS / omega_SS.sum()
            self.imm_rates = np.zeros((self.T + self.S, self.S))
            self.omega = np.tile(np.reshape(self.omega_SS, (1, self.S)),
                                 (self.T + self.S, 1))
            self.omega_S_preTP = self.omega_SS

        # Interpolate chi_n and create omega_SS_80 if necessary
        if self.S == 80:
            self.chi_n = self.chi_n_80
        elif self.S < 80:
            self.age_midp_80 = np.linspace(20.5, 99.5, 80)
            self.chi_n_interp = si.interp1d(self.age_midp_80,
                                            np.squeeze(self.chi_n_80),
                                            kind='cubic')
            self.newstep = 80.0 / self.S
            self.age_midp_S = np.linspace(20 + 0.5 * self.newstep,
                                          100 - 0.5 * self.newstep,
                                          self.S)
            self.chi_n = self.chi_n_interp(self.age_midp_S)


    def update_specifications(self, revision, raise_errors=True):
        '''
        Updates parameter specification with values in revision
        dictionary.

        Args:
            revision (dict): dictionary or JSON string with one or more
                `PARAM: VALUE` pairs
            raise_errors (boolean):
                    if True (the default), raises ValueError when
                       `parameter_errors` exists;
                    if False, does not raise ValueError when
                       `parameter_errors` exists and leaves error
                       handling to caller of the update_specifications
                       method.

        Returns:
            None

        Raises:
            ValueError: if raise_errors is True AND
              `_validate_parameter_names_types` generates errors OR
              `_validate_parameter_values` generates errors.

        Notes:
            Given a reform dictionary, typical usage of the
            Specifications class is as follows::
                >>> specs = Specifications()
                >>> specs.update_specifications(revision)
            An example of a multi-parameter specification is as follows::
                >>> revision = {
                    frisch: [0.03]
                }

        '''
        if not (isinstance(revision, dict) or isinstance(revision, str)):
            raise ValueError(
                'ERROR: revision is not a dictionary of string')
        self.adjust(revision, raise_errors=raise_errors)
        self.compute_default_params()


def revision_warnings_errors(spec_revision):
    '''
    Generate warnings and errors for OG-USA parameter specifications

    Args:
        spec_revision (dict): dictionary suitable for use with the
            `Specifications.update_specifications method`.

    Returns:
        rtn_dict (dict): with endpoint specific warning and error messages

    '''
    rtn_dict = {'warnings': '', 'errors': ''}
    spec = Specifications()
    spec.update_specifications(spec_revision, raise_errors=False)
    if spec._errors:
        rtn_dict['errors'] = spec._errors
    return rtn_dict
