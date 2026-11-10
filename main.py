#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reproduce the paper
2018 4th International Conference on Green Technology and Sustainable Development (GTSD)
A Cost-Optimal Pathway to Integrate Renewable Energy into the
Future Vietnamese Power System
Dinh Thanh Viet, Vo Van Phuong, Minh Quan Duong, Ma Phuoc Khanh, Alexander Kies, and Bruno Schyska

using the data received from Alexander

Created on Thu Aug  8 11:15:18 2019

@author: haduong
"""

import pypsa

# Dataset: extract upstream/vietnam3.tar.xz into data/ (kept out of git)
import os
here = os.path.dirname(os.path.abspath(__file__))
network = pypsa.Network(import_name=os.path.join(here, "data"))

# The full dataset covers 2015-2016 hourly; run one day (use [:168] for a week)
network.set_snapshots(network.snapshots[:24])

#set to your favourite solver
solver_name = "glpk"

network.lopf(snapshots=network.snapshots,solver_name=solver_name)


print(network.generators.p_nom_opt)

print(network.generators_t.p)

print(network.storage_units.p_nom_opt)

print(network.storage_units_t.p)

print(network.lines.s_nom_opt)

print(network.lines_t.p0)