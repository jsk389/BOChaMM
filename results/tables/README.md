# Tables of Results

Tables 1 and 2 from the paper are presented in this directory.


**Table 1**

| Column Header        | Description                                                                                                                                                              |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `KIC`                | Kepler Input Catalog identifier                                                                                                                                          |
| `mh`                 | Stellar bulk metallicity [M/H] from APOGEE DR17. Units are in dex/cgs                                                                                                    |
| `mh_err`             | Uncertainty in [M/H]. Units are in dex/cgs                                                                                                                               |
| `mass`               | Stellar mass estimated using asteroseimic scaling relations calibrated using `asfgrid`, in units of $M_{\odot}$                                                          |
| `mass_err`           | Uncertainty in stellar mass in units of $M_{\odot}$                                                                                                                      |
| `numax`              | Frequency at oscillation maximum power, $\nu_{\mathrm{max}}$, in $\mu\,$Hz                                                                                               |
| `numax_std`          | Uncertainty in $\nu_{\mathrm{max}}$ in $\mu\,$Hz                                                                                                                         |
| `Deltanu`            | Large frequency separation, $\Delta\nu$, in $\mu\,$Hz                                                                                                                    |
| `Deltanu_std`        | Uncertainty in $\Delta\nu$ in $\mu\,$Hz                                                                                                                                  |
| `DPi`                | Dipole mode period spacing, $\Delta\Pi$, in seconds                                                                                                                      |
| `DPi_e`, `DPi_E`     | Lower and upper errorbars for $\Delta\Pi$ in seconds, respectively                                                                                                       |
| `q`                  | Mixed-mode coupling factor, $q$                                                                                                                                          |
| `q_e`, `q_E`         | Lower and upper errorbars for $q$, respectively                                                                                                                          |
| `eps_g`              | g-mode phase offset, $\epsilon_g$                                                                                                                                        |
| `eps_g_e`, `eps_g_E` | Lower and upper errorbars for $\epsilon_g$, respectively                                                                                                                 |
| `drot`               | Mixed-mode rotational splitting, $\delta\nu_{\mathrm{rot}}$, in units of $\mu\,$Hz. Set to 0 if no rotationally-split components are detected in dipole the mixed-modes. |
| `drot_e`, `drot_E`   | Lower and upper errorbars for $\delta\nu_{\mathrm{rot}}$ in $\mu\,$Hz, respectively                                                                                      |
