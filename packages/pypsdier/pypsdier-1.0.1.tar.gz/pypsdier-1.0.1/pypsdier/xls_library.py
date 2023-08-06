# -*- coding: utf-8 -*-
from xlwt import Workbook, easyxf
import numpy as np
import os

##########################################################################
# Fonts
##########################################################################
title = easyxf('font: bold on;')
subtitle = easyxf('font: italic on;')

##########################################################################
# Export the data-dictionary as a spreadsheet
##########################################################################
def save_as_spreadsheet(inputs, outputs, filename):
  """
  export_to_xls allows to export the solution
  of the simulation in format xls 
  """
  wb = Workbook()
  filepath = os.path.abspath(filename)
  write_parameters_sheet(wb, inputs)
  if "ode" in outputs and "pde" in outputs:
    write_ode_and_pde_sheet(wb, inputs, outputs)
  wb.save(filepath)
  print(f"Saving simulation as xls file at {filepath}")
  return


##########################################################################
# Saving the parameters into the xls
##########################################################################
def write_parameters_sheet(wb, p):
  """Writes the excel sheet with the provided parameters information.

  :param wb: [description]
  :type wb: [type]
  :param p: [description]
  :type p: [type]
  """
  # Shorthand notation
  Nc = len(p["Names"])
  Nr = len(p["CatalystParticleRadius"])
  Np = len(p["ReactionParameters"])

  # Writing the parameters
  ws1 = wb.add_sheet('Parameters')

  # Catalyst
  n = 0
  write_to_xls(ws1, 2, n, "Catalyst", title)
  write_to_xls(ws1, 3, n, "Catalyst Volume")
  write_to_xls(ws1, 4, n, "Vc [ml]")
  write_to_xls(ws1, 4, n+1, p["CatalystVolume"])
  write_to_xls(ws1, 5, n, "Catalyst Enzyme Concentration")
  write_to_xls(ws1, 6, n, "E0 [mM]")
  if type(p["CatalystEnzymeConcentration"]) in [float, int]: 
    write_to_xls(ws1, 6, n+1, p["CatalystEnzymeConcentration"])
  else:
    write_to_xls(ws1, 6, n+1, "Given as function of time, see original file")
  write_to_xls(ws1, 7, n, "Thiele Modulus")
  write_to_xls(ws1, 8, n, "Phi")
  write_to_xls(ws1, 8, n+1, 0)  # FIX HERE
  write_to_xls(ws1, 9, n, "Radiuses values and frequencies")  # FIX HERE
  for i in range(Nr):
    R = p["CatalystParticleRadius"][i] / 1.E-6
    f = p["CatalystParticleRadiusFrequency"][i]
    write_to_xls(ws1, 10+i, n, "R [um]")
    write_to_xls(ws1, 10+i, n+1, R)
    write_to_xls(ws1, 10+i, n+2, " with probability ")
    write_to_xls(ws1, 10+i, n+3, f)

  # Reaction Conditions
  n = 5
  write_to_xls(ws1, 2, n, "Reaction Conditions", title)
  write_to_xls(ws1, 3, n, "Bulk Volume")
  write_to_xls(ws1, 4, n, "Vb [ml]")
  write_to_xls(ws1, 4, n+1, p["BulkVolume"])
  write_to_xls(ws1, 5, n, "Initial Concentrations")  
  for i in range(Nc):
    write_to_xls(ws1, 6+i, n, p["Names"][i] + " [mM]")
    write_to_xls(ws1, 6+i, n+1, p["InitialConcentrations"][i])

  # Reaction-Diffusion Parameters
  n = 8
  write_to_xls(ws1, 2, n, "Reaction-Diffusion Parameters", title)
  write_to_xls(ws1, 3, n, "Effective Diffusion Coefficient") 
  for i in range(Nc):
    write_to_xls(ws1, 4+i, n, p["Names"][i] + " [m2/s]")
    write_to_xls(ws1, 4+i, n+1, p["EffectiveDiffusionCoefficients"][i])
  write_to_xls(ws1, 4+Nc, n, "Reaction Function")
  """
  write_to_xls(ws1, 5+Nc, n, "Name")
  write_to_xls(ws1, 5+Nc, n+1, p["ReactionFunction"]["Name"])
  write_to_xls(ws1, 6+Nc, n, "Reaction Parameters")
  for i in range(Np):
    # Ask for them with reverse notation to skip over first unnecessary values
    write_to_xls(ws1, 7+Nc+i, n, p["ReactionFunction"]["Arguments"][2+i])
    write_to_xls(ws1, 7+Nc+i, n+1, p["ReactionParameters"][i])
  """

  # Simulation Parameters
  n = 11
  write_to_xls(ws1, 2, n, "Simulation Parameters", title)
  write_to_xls(ws1, 3, n, "Simulation Time")
  write_to_xls(ws1, 4, n, "Tsim [s]")
  write_to_xls(ws1, 4, n+1, p["SimulationTime"])
  write_to_xls(ws1, 5, n, "Saving Time Step dt [s]")
  write_to_xls(ws1, 6, n, "dt [s]")
  write_to_xls(ws1, 6, n+1, p["SavingTimeStep"])
  return

##########################################################################
# Writing the ode and pde times and concentrations on bulk module
##########################################################################
def write_ode_and_pde_sheet(wb, inputs, p):
  Nc = len(inputs["Names"])
  Nr = len(inputs["CatalystParticleRadius"])
  Np = len(inputs["ReactionParameters"])

  # Writing the parameters
  ws = wb.add_sheet("bulk ode-pde")

  # Writing the ode
  n = 0
  write_to_xls(ws, 0, n, "ode", title)
  t = p["ode"]["t"]
  write_to_xls(ws, 1, n, "Time [s]", subtitle)
  write_to_xls(ws, 2, n, t.reshape(len(t),1))
  for i in range(Nc):
    c = p["ode"]["C"][:,i]
    write_to_xls(ws, 1, n+1+i, inputs["Names"][i] + " [mM]", subtitle)
    write_to_xls(ws, 2, n+1+i, c.reshape(len(c),1))
   
  # Writing the pde
  n = Nc+2
  write_to_xls(ws, 0, n, "pde", title)
  t = p["pde"]["t"]
  write_to_xls(ws, 1, n, "Time [s]", subtitle)
  write_to_xls(ws, 2, n, t.reshape(len(t),1))
  for i in range(Nc):
    c = p["pde"]["C"][0][i][:,-1] # All radius have the same bulk concentration
    write_to_xls(ws, 1, n+1+i, inputs["Names"][i] + " [mM]", subtitle)
    write_to_xls(ws, 2, n+1+i, c.reshape(len(c),1))

  return
    
##########################################################################
# Wrappers and helpers
##########################################################################
def write_to_xls(ws, i_ws, j_ws, A, font=''):
  """
  Wrapper to write a matrix into a workbook into a specific position
  """
  #print("A=",A)
  if type(A)==str:
    if font:
      ws.write(i_ws, j_ws, A, font)
    else:
      ws.write(i_ws, j_ws, A)
  else:
    A = np.matrix(A)
    n, m = A.shape
    for i in range(n):
      for j in range(m):
        if font:
          ws.write(i_ws+i,j_ws+j,str(A[i,j]),font)
        else:
          ws.write(i_ws+i,j_ws+j,str(A[i,j]))
  return