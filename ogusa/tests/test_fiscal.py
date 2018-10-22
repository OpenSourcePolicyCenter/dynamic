import numpy as np
import pytest
from ogusa import fiscal


def test_D_G_path():
    T = 320
    S = 80
    debt_ratio_ss = 1.2
    tG1 = 20
    tG2 = int(T * 0.8)
    ALPHA_T = np.ones(T) * 0.09
    ALPHA_G = np.ones(T) * 0.05
    rho_G = 0.1
    r_gov = np.ones(T + S) * 0.03
    g_n_vector = np.ones(T + S) * 0.02
    g_y = 0.03
    D0 = 0.59
    G0 = 0.05
    Y = np.append(np.array([1., 1.033, 1.067089, 1.10230294, 1.13867893,
                    1.17625534, 1.21507176, 1.25516913, 1.29658971,
                    1.33937718, 1.38357662, 1.42923465, 1.47639939,
                    1.52512057, 1.57544955, 1.62743939, 1.68114489,
                    1.73662267, 1.79393122, 1.85313095, 1.91428427,
                    1.97745565, 2., 2., 2., 2., 2., 2., 2., 2., 2., 2.,
                    2., 2., 2., 2., 2., 2., 2., 2., 2., 2., 2., 2., 2.,
                       2., 2., 2., 2., 2.  ,
                       2., 2., 2., 2., 2.  ,
                       2., 2., 2., 2., 2.  ,
                       2., 2., 2., 2., 2.  ,
                       2., 2., 2., 2., 2.  ,
                       2., 2., 2., 2., 2.  ,
                       2., 2., 2., 2., 2.  ,
                       2., 2., 2., 2., 2.  ,
                       2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.,
                     2., 2., 2., 2., 2.]), np.ones(S) * 2.)
    T_H = np.append(np.array([0.09, 0.09297, 0.09603801, 0.09920726, 0.1024811,
                     0.10586298, 0.10935646, 0.11296522, 0.11669307, 0.12054395,
                     0.1245219, 0.12863112, 0.13287595, 0.13726085, 0.14179046,
                     0.14646954, 0.15130304, 0.15629604, 0.16145381, 0.16678179,
                     0.17228558, 0.17797101, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18,
                     0.18, 0.18, 0.18, 0.18, 0.18]), np.ones(S) * 0.18)
    REVENUE = np.append(np.array([0.1, 0.1033, 0.1067089, 0.11023029, 0.11386789,
                         0.11762553, 0.12150718, 0.12551691, 0.12965897, 0.13393772,
                         0.13835766, 0.14292347, 0.14763994, 0.15251206, 0.15754496,
                         0.16274394, 0.16811449, 0.17366227, 0.17939312, 0.18531309,
                         0.19142843, 0.19774556, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2,
                         0.2, 0.2, 0.2, 0.2, 0.2]), np.ones(S) * 0.2)

    D_expected = np.append(np.array([0.59, 0.61623291, 0.64319598, 0.67091602, 0.69942066,
       0.72873841, 0.75889866, 0.78993172, 0.82186883, 0.85474225,
       0.88858522, 0.92343206, 0.95931814, 0.99627999, 1.03435529,
       1.07358289, 1.11400293, 1.15565679, 1.19858719, 1.24283823,
       1.28845541, 1.38932398, 1.48768626, 1.57891764, 1.66102587,
       1.73492329, 1.80143096, 1.86128786, 1.91515908, 1.96364317,
       2.00727885, 2.04655097, 2.08189587, 2.11370628, 2.14233565,
       2.16810209, 2.19129188, 2.21216269, 2.23094642, 2.24785178,
       2.2630666, 2.27675994, 2.28908395, 2.30017555, 2.310158,
       2.3191422, 2.32722798, 2.33450518, 2.34105466, 2.3469492,
       2.35225428, 2.35702885, 2.36132596, 2.36519337, 2.36867403,
       2.37180663, 2.37462596, 2.37716337, 2.37944703, 2.38150233,
       2.3833521, 2.38501689, 2.3865152, 2.38786368, 2.38907731,
       2.39016958, 2.39115262, 2.39203736, 2.39283362, 2.39355026,
       2.39419523, 2.39477571, 2.39529814, 2.39576833, 2.39619149,
       2.39657234, 2.39691511, 2.3972236, 2.39750124, 2.39775111,
       2.397976, 2.3981784, 2.39836056, 2.39852451, 2.39867206,
       2.39880485, 2.39892437, 2.39903193, 2.39912874, 2.39921586,
       2.39929428, 2.39936485, 2.39942836, 2.39948553, 2.39953697,
       2.39958328, 2.39962495, 2.39966245, 2.39969621, 2.39972659,
       2.39975393, 2.39977854, 2.39980068, 2.39982061, 2.39983855,
       2.3998547, 2.39986923, 2.39988231, 2.39989407, 2.39990467,
       2.3999142, 2.39992278, 2.3999305, 2.39993745, 2.39994371,
       2.39994934, 2.3999544, 2.39995896, 2.39996307, 2.39996676,
       2.39997008, 2.39997308, 2.39997577, 2.39997819, 2.39998037,
       2.39998233, 2.3999841, 2.39998569, 2.39998712, 2.39998841,
       2.39998957, 2.39999061, 2.39999155, 2.3999924, 2.39999316,
       2.39999384, 2.39999446, 2.39999501, 2.39999551, 2.39999596,
       2.39999636, 2.39999673, 2.39999705, 2.39999735, 2.39999761,
       2.39999785, 2.39999807, 2.39999826, 2.39999843, 2.39999859,
       2.39999873, 2.39999886, 2.39999897, 2.39999908, 2.39999917,
       2.39999925, 2.39999933, 2.39999939, 2.39999945, 2.39999951,
       2.39999956, 2.3999996, 2.39999964, 2.39999968, 2.39999971,
       2.39999974, 2.39999977, 2.39999979, 2.39999981, 2.39999983,
       2.39999985, 2.39999986, 2.39999988, 2.39999989, 2.3999999,
       2.39999991, 2.39999992, 2.39999993, 2.39999993, 2.39999994,
       2.39999995, 2.39999995, 2.39999996, 2.39999996, 2.39999996,
       2.39999997, 2.39999997, 2.39999997, 2.39999998, 2.39999998,
       2.39999998, 2.39999998, 2.39999998, 2.39999999, 2.39999999,
       2.39999999, 2.39999999, 2.39999999, 2.39999999, 2.39999999,
       2.39999999, 2.39999999, 2.39999999, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4,
       2.4, 2.4, 2.4, 2.4, 2.4]), np.ones(1) * 2.4)

    G_expected = np.array([0.05, 0.05165, 0.05335445, 0.05511515, 0.05693395,
       0.05881277, 0.06075359, 0.06275846, 0.06482949, 0.06696886,
       0.06917883, 0.07146173, 0.07381997, 0.07625603, 0.07877248,
       0.08137197, 0.08405724, 0.08683113, 0.08969656, 0.09265655,
       0.15230167, 0.15242377, 0.14722604, 0.13955871, 0.13265811,
       0.12644757, 0.12085808, 0.11582754, 0.11130006, 0.10722532,
       0.10355806, 0.10025752, 0.09728704, 0.09461361, 0.09220752,
       0.09004203, 0.0880931, 0.08633906, 0.08476042, 0.08333965,
       0.08206096, 0.08091013, 0.07987439, 0.07894222, 0.07810327,
       0.07734821, 0.07666866, 0.07605706, 0.07550663, 0.07501123,
       0.07456538, 0.07416411, 0.07380297, 0.07347794, 0.07318542,
       0.07292215, 0.0726852, 0.07247195, 0.07228003, 0.07210729,
       0.07195183, 0.07181192, 0.071686, 0.07157267, 0.07147067,
       0.07137887, 0.07129626, 0.0712219, 0.07115498, 0.07109475,
       0.07104055, 0.07099176, 0.07094786, 0.07090834, 0.07087278,
       0.07084077, 0.07081196, 0.07078604, 0.0707627, 0.0707417,
       0.0707228, 0.07070579, 0.07069048, 0.0706767, 0.0706643,
       0.07065314, 0.0706431, 0.07063406, 0.07062592, 0.0706186,
       0.07061201, 0.07060608, 0.07060074, 0.07059594, 0.07059161,
       0.07058772, 0.07058422, 0.07058107, 0.07057823, 0.07057568,
       0.07057338, 0.07057131, 0.07056945, 0.07056778, 0.07056627,
       0.07056491, 0.07056369, 0.07056259, 0.0705616, 0.07056071,
       0.07055991, 0.07055919, 0.07055854, 0.07055796, 0.07055743,
       0.07055696, 0.07055653, 0.07055615, 0.0705558, 0.07055549,
       0.07055521, 0.07055496, 0.07055474, 0.07055453, 0.07055435,
       0.07055418, 0.07055404, 0.0705539, 0.07055378, 0.07055367,
       0.07055358, 0.07055349, 0.07055341, 0.07055334, 0.07055327,
       0.07055322, 0.07055317, 0.07055312, 0.07055308, 0.07055304,
       0.070553, 0.07055297, 0.07055295, 0.07055292, 0.0705529,
       0.07055288, 0.07055286, 0.07055285, 0.07055283, 0.07055282,
       0.07055281, 0.0705528, 0.07055279, 0.07055278, 0.07055277,
       0.07055276, 0.07055276, 0.07055275, 0.07055274, 0.07055274,
       0.07055274, 0.07055273, 0.07055273, 0.07055273, 0.07055272,
       0.07055272, 0.07055272, 0.07055272, 0.07055272, 0.07055271,
       0.07055271, 0.07055271, 0.07055271, 0.07055271, 0.07055271,
       0.07055271, 0.07055271, 0.07055271, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527,
       0.0705527, 0.0705527, 0.0705527, 0.0705527, 0.0705527])

    budget_balance = False
    baseline_spending = False
    other_dg_params = (T, r_gov, g_n_vector, g_y)
    dg_fixed_values = (Y, REVENUE, T_H, D0, G0)
    fiscal_params = (budget_balance, ALPHA_T, ALPHA_G, tG1, tG2, rho_G,
                     debt_ratio_ss)
    test_D, test_G = fiscal.D_G_path(dg_fixed_values, fiscal_params,
                                     other_dg_params, baseline_spending)
    assert np.allclose(test_D, D_expected, rtol=1e-05, atol=1e-06)
    assert np.allclose(test_G, G_expected, rtol=1e-05, atol=1e-06)
