import math

# Reactions from report
Pu_req = 30.00      # kips
Vu_req = 55.0      # kips
Mu_req = 5000.0    # kip-ft

max_h = 999.0

theta = 0.0

min_err = None

for i in range(0, 360):
    theta = math.radians(float(i/4.0))
    T = Vu_req / math.cos(theta)
    h = min(Mu_req/(T*math.cos(theta)), max_h)

    Mu = T*math.cos(theta)*h
    Vu = T*math.cos(theta)
    Pu = T*math.sin(theta)

    deltaMu = Mu - Mu_req
    deltaVu = Vu - Vu_req
    deltaPu = math.fabs(Pu - Pu_req)
    err = max(math.fabs(deltaMu/Mu_req),
              math.fabs(deltaVu/Vu_req), math.fabs(deltaPu/Pu_req))

    if min_err is None:
        min_err = err
        min_i = i/4.0
        min_h = h
    elif min_err > err:
        min_err = err
        min_i = i/4.0
        min_h = h


theta = math.radians(min_i/4.0)
T = Vu_req / math.cos(theta)

Mu = T*math.cos(theta)*min_h
Vu = T*math.cos(theta)
Pu = T*math.sin(theta)


print("Preliminary Design")
print("theta = %.2f deg, h = %.2f ft, error = %.2f kips, T = %.2f kips" %
      (min_i, min_h, min_err, T))
print("Pu = %.2f kips, Mu = %.0f kip-ft, Vu = %.2f kips" %
      (Pu, Mu, Vu))
