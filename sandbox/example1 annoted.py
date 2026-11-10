#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 11:15:18 2019

@author: haduong
"""

import pypsa
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 500)

# Instantiate the system container
network = pypsa.Network()

"""
                Bus2
               /    \
              /      \
             /        \
Generator--Bus0 ----> Bus1--Load
"""

# Add three buses
"""
A Bus is a node, for Kirchhoff's laws

The buses in a power system are associated with four quantities. These quantities are
  the magnitude of the voltage,
  the phase angle of the voltage,
  active or true power, and
  the reactive power.
  
Any Load, Generator, StorageUnit, Store and ShuntImpedance is connected to a bus

Input v_nom is nominal voltage in kV
"""
network.add("Bus", "My bus 0", v_nom=20.)
network.add("Bus", "My bus 1", v_nom=20.)
network.add("Bus", "My bus 2", v_nom=20.)

print(network.buses)

#add three lines in a ring
"""
A Line connects two bus0 and bus1

x is the series reactance in Ohm
r is the series resistance in Ohm
The series impedance of the line is z = r + j x

We neglect shunt capacitance effect, making the short-length line (<80km) assumption
"""
network.add("Line", "My line 0", bus0="My bus 0", bus1="My bus 1", x=0.1, r=0.01)
network.add("Line", "My line 1", bus0="My bus 1", bus1="My bus 2", x=0.1, r=0.01)
network.add("Line", "My line 2", bus0="My bus 2", bus1="My bus 0", x=0.1, r=0.01)

print(network.lines)

#add a generator at bus 0
"""
p_set is the active power power set point (for PF), in MW
control is the P, Q, V control strategy (for PF), must be "PQ", "QV" or "Slack". Defaults to "PQ".
"""
network.add("Generator","My gen",
            bus="My bus 0",
            p_set=100,
            control="PQ")

print(network.generators)

print(network.generators.p_set)

#add a load at bus 1
"""
p_set is the active power consumption, in MW
"""
network.add("Load","My load",
            bus="My bus 1",
            p_set=100)

print(network.loads)

print(network.loads.p_set)

"""
q_set is the reative power consumption, in MVar, positive for inductive load
"""
network.loads.q_set = 100.

#Do a Newton-Raphson power flow
"""
The goal of a power-flow study is to obtain complete voltages angle and magnitude information
for each bus in a power system for specified load and generator real power and voltage conditions.
Once this information is known, real and reactive power flow on each branch as well as
generator reactive power output can be analytically determined.

The problem is non-linear
Newton-Raphson solves using a sequence of linearized problems.
More advanced algorithms would be Fast Decoupled Load-Flow (FDLF) method or
Holomorphic Embedding Load-flow Method (HELM), I don t know if it is implemented
"""
network.pf()

#Active power at bus0 for each line in MW
"""
There are two routes.
Since lines are identical, but the second route involves two lines,
so it has twice the resistance of the first route.
Hence roughly 2/3 of the power go via direct line 0->1 , and 1/3 via route 1->2->0 (backward).
"""
print(network.lines_t.p0)

# Output v_ang      is a time series of Voltage angle, in radians
print(network.buses_t.v_ang*180/np.pi)

# Output v_mag_pu   is a time series of Voltage magnitude, per unit of v_nom
"""
 The loss is even between the segments 1->2 and 2->0, since the two lines are identical.
"""
print(network.buses_t.v_mag_pu)
