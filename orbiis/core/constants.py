import math

# physical constants
c = 299792458.0                 # [m/s] speed of light
mu = 3.986005e14                # [m^3/s^2] gravitational constant * mass of Earth (GPS)
F = -4.442807633e-10            # [] relativistic correction factor
omega_e = 7.2921151467e-5       # [rad/s] Earth's angular velocity (WGS84)
deg2rad = math.pi / 180.0       # [rad/deg] degrees to radians conversion

# earth constants
EARTH_GM = 3.986005e14          # m^3/s^2 (gravitational constant * mass of Earth)
EARTH_RADIUS = 6.378137e6       # m (WGS84 Earth's equatorial radius)
EARTH_FLATTENING = 1.0 / 298.257223563  # Earth's flattening factor (WGS84)
EARTH_ROTATION_RATE = 7.2921151467e-5   # rad/s (Earth's angular velocity)

# astronomical constants
AU = 149597870691.0            # m (astronomical unit, average distance from Earth to Sun)
SECS_IN_MIN = 60
SECS_IN_HR = 60 * SECS_IN_MIN
SECS_IN_DAY = 24 * SECS_IN_HR
SECS_IN_WEEK = 7 * SECS_IN_DAY
SECS_IN_YEAR = 365 * SECS_IN_DAY
SECS_IN_CENTURY = SECS_IN_DAY * 36525.0  # seconds in a Julian century

# gravitational parameters
GMS = 1.327124e20              # m^3/s^2 (gravitational constant * mass of the Sun)
GMM = 4.902801e12              # m^3/s^2 (gravitational constant * mass of the Moon)
MU_GAL = 3.986004418e14        # m^3/s^2 (gravitational constant * mass of Earth for Galileo)

# radian conversions
D2R = deg2rad                  # degrees to radians
AS2R = D2R / 3600.0            # arcseconds to radians

# satellite frequencies
FREQ_G1 = 1.57542e9            # [Hz] GPS L1
FREQ_G2 = 1.22760e9            # [Hz] GPS L2
FREQ_G5 = 1.17645e9            # [Hz] GPS L5

FREQ_E1 = 1.57542e9            # [Hz] GAL E1
FREQ_E5a = 1.17645e9           # [Hz] GAL E5a
FREQ_E5b = 1.207140e9          # [Hz] GAL E5b
FREQ_E5 = 1.191795e9           # [Hz] GAL E5
FREQ_E6 = 1.278750e9           # [Hz] GAL E6

# constants
PI = 3.1415926535898
HALFPI = 1.5707963267949

COS_5 = 0.9961946980917456
SIN_5 = -0.0871557427476582

P2_5 = 0.03125
P2_6 = 0.015625
P2_8 = 0.00390625
P2_9 = 0.001953125
P2_10 = 9.765625000000000E-04
P2_11 = 4.882812500000000E-04
P2_12 = 2.441406250000000E-04
P2_13 = 1.220703125000000E-04
P2_14 = 6.103515625000000E-05
P2_15 = 3.051757812500000E-05
P2_16 = 1.525878906250000E-05
P2_17 = 7.629394531250000E-06
P2_19 = 1.907348632812500E-06
P2_20 = 9.536743164062500E-07
P2_21 = 4.768371582031250E-07
P2_24 = 5.960464477539063e-08
P2_27 = 7.450580596923828e-09
P2_28 = 3.725290298461914E-09
P2_29 = 1.862645149230957E-09
P2_30 = 9.313225746154785E-10
P2_31 = 4.656612873077393E-10
P2_32 = 2.328306436538696E-10
P2_33 = 1.164153218269348E-10
P2_34 = 5.820766091346740E-11
P2_35 = 2.910383045673370E-11
P2_37 = 7.275957614183426E-12
P2_38 = 3.637978807091713E-12
P2_39 = 1.818989403545856E-12
P2_40 = 9.094947017729280E-13
P2_41 = 4.547473508864641E-13
P2_43 = 1.136868377216160E-13
P2_44 = 5.684341886080802E-14
P2_46 = 1.421085471520200E-14
P2_48 = 3.552713678800501E-15
P2_49 = 1.776356839400251E-15
P2_50 = 8.881784197001252E-16
P2_51 = 4.440892098500626E-16
P2_55 = 2.775557561562891E-17
P2_57 = 6.938893903907228E-18
P2_59 = 1.734723475976810E-18
P2_60 = 8.673617379884035E-19
P2_66 = 1.355252715606880E-20
P2_68 = 3.388131789017201E-21
SC2RAD = 3.1415926535898