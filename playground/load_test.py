import math

# Reactions from report
Pu_req = 65.39      # kips
Vu_req = 46.25      # kips
Mu_req = 3046.61    # kip-ft

theta = 0.0

min_err = None

for i in range(0, 360):
    theta = math.radians(float(i/4.0))
    T = Vu_req / math.cos(theta)
    h = Mu_req/(T*math.cos(theta))

    Mu = T*math.cos(theta)*h
    Vu = T*math.cos(theta)
    Pu = T*math.sin(theta)

    deltaMu = Mu - Mu_req
    deltaVu = Vu - Vu_req
    deltaPu = math.fabs(Pu - Pu_req)

    if min_err is None:
        min_err = deltaPu
        min_i = i/4.0
        min_h = h
    elif min_err > deltaPu:
        min_err = deltaPu
        min_i = i/4.0
        min_h = h


T = Vu_req / math.cos(math.radians(min_i/4.0))

print("Preliminary Design")
print("theta = %.2f deg, h = %.2f ft, error = %.2f kips, T = %.2f kips" %
      (min_i, min_h, min_err, T))
