import numpy as np
from scipy import linalg
import sys
import time

def pde_solver(inputs, Nx=40, dt=-1):
  """
  Solver for the Reaction Diffusion Equation
  """
  start_time = time.time()

  #print("Dont forget to compute how much total Enzime there is")

  # Unpacking the values
  Tsim = inputs["SimulationTime"]
  dt_save = inputs["SavingTimeStep"]
  Vc = inputs["CatalystVolume"]
  Vb = inputs["BulkVolume"]
  legend = inputs["Names"]
  IC = inputs["InitialConcentrations"]
  D = inputs["EffectiveDiffusionCoefficients"]
  H_R = inputs["CatalystParticleRadius"]
  H_f = inputs["CatalystParticleRadiusFrequency"]
  Reaction = inputs["ReactionFunction"]
  params = inputs["ReactionParameters"]
  E = inputs["CatalystEnzymeConcentration"]
  if "EnzymeRadialDistribution" in inputs:
    Z = inputs["EnzymeRadialDistribution"]
  else:
    Z = 1.0

  # INDICES IMPORTANTES DE LA SIMULACION
  Nc = len(IC)       # Numero de concentraciones
  Nr = len(H_R) # Numero de radios distintos a considerar
  dt_max = (min(H_R)/Nx)**2 / max(D)
  if dt<0: #if not imposed by user
    dt = min(0.25*dt_max,0.1)

  if Nc:
    N_substance_str = "a single substance"
  else:
    N_substance_str = f"the {Nc} subtances"

  print(f"PDE: Solving the complete reaction-diffusion problem, " + \
       f"considering {N_substance_str} and {Nr} particle radii.")

  ## TOTAL ENZYME CONCENTRATION
  TEC = total_enzyme_concentration(Z, H_R, Nx)
  #print("Total Enzyme Concentration: ", E*TEC)

  ## CONSTRUCCION DE LAS MATRICES (fijas en las iteraciones)
  Mid, Mls, fic = Matrices(H_R, H_f, Vc, Vb, Nx)
  theta = 0.5
  ME, MI, PLU = [], [], []
  for c in range(Nc):
    ME.append( np.matrix(Mid + dt*theta*D[c]*Mls) )
    MI.append( np.matrix(Mid - dt*(1-theta)*D[c]*Mls) )
    PLU.append( linalg.lu_factor( MI[c] ) )

  #print("Must solve {} ecuations of size {}x{}, at least {} times".format(Nc, Mid.shape[0], Mid.shape[1], int(Tsim/dt)))
  # INICIALIZACION DEL ALGORITMO
  ## INICIO DEL TIEMPO
  t = 0.0
  ## CONCENTRACIONES INICIALES
  v = np.zeros(Nr*Nx+1)
  v[-1]= 1
  C_old, C_new = [], []
  for c in range(Nc):
    C_old.append(v*IC[c])
  ## VELOCIDADES INICIALES
  Z_r = eval_Z(Z, H_R, Nx)
  v_C = Reaction(C_old, eval_E(E,t), *params)
  # GUARDAR VALORES INICIALES
  C_save, C_t = [], []
  for c in range(Nc):
    #C_save.append(float(C_old[c][-1]))
    C_save.append(C_old[c])
  C_t.append(C_save)
  T_t = [t,]
  # BUCLE CENTRAL
  if dt_save < 0:
    dt_save = 1.0 # incremental for saving simulation
  print_time(t, Tsim, start_time)
  while t<Tsim:
    for c in range(Nc):
      b = ME[c]*np.matrix(C_old[c]).T + dt*np.matrix(v_C[c]*Z_r*fic).T
      #C_new.append( np.array(linalg.solve(MI[c],b).T)[0] )
      C_new.append( np.array( linalg.lu_solve(PLU[c], b ).T)[0] )
    v_C = Reaction(C_new, eval_E(E,t), *params)
    C_old = C_new
    C_new = []
    t = t+dt
    if (t>T_t[-1]+dt_save):
      C_save = []
      for c in range(Nc):
        C_save.append(C_old[c])
      C_t.append(C_save)
      T_t.append(float(t))
      print_time(t, Tsim, start_time)
  print_time(t, Tsim, start_time, end_char="\n")
  Nt = len(T_t)

  # Adding the new information to the dict  
  pde_solution_dict = {"t":np.array(T_t), 
                       "dt":dt,
                       "E":np.array([eval_E(E,ti) for ti in T_t]), 
                       "C":nested_lists(np.array(C_t), Nx)}
  print(pde_solution_dict)
  return pde_solution_dict

################################################################################
# GENERATES THE MATRICES FOR THE ITERATION
################################################################################
def Matrices(H_R, H_f, Vc, Vb, Nx):
  H_R, H_f = np.array(H_R), np.array(H_f)/sum(H_f)
  nc = len(H_R)
  g = -3*Vc / (Vb*sum(H_f*H_R**3))
  Dr = np.array([-1.5, 2.,-0.5]) # One sided derivative from the right (LBC)
  Dl = np.array([ 0.5,-2., 1.5]) # One sided derivative from the left (RBC)
  dR = H_R/Nx # Delta R used for derivatives
  # Set up of matrices
  Id = np.eye(nc*Nx+1)
  Ls = np.zeros([nc*Nx+1,nc*Nx+1])
  bc = np.ones(nc*Nx+1)
  # auxiliary matrix
  i = range(0,Nx-1)
  vi = np.arange(1,Nx)
  C_aux = np.zeros([Nx-1,Nx+1])
  C_aux[range(0,Nx-1),range(0,Nx-1)] = 1. - 1./vi
  C_aux[range(0,Nx-1),range(1,Nx)] =  -2
  C_aux[range(0,Nx-1),range(2,Nx+1)] =  1. + 1./vi
  #jinv = 1./arange(1,Nx)
  #C_aux = diag(1-jinv,-1) -2*eye(Nx+1,Nx+1) + diag(1+jinv,1)
  # Fill up
  for c in range(nc):
    # LBC : imposed on the rows c*Nx
    Id[c*Nx,c*Nx] = 0
    Ls[c*Nx,c*Nx:(c*Nx+3)] = Dr/dR[c]
    bc[c*Nx] = 0
    # RBC : imposed on the last row
    Ls[-1,((c+1)*Nx-2):(c+1)*Nx] = g*H_f[c]*H_R[c]*Nx*Dl[0:-1]
    # RDE
    Ls[c*Nx+1:(c+1)*Nx,c*Nx:(c+1)*Nx] = C_aux[:,:-1]/dR[c]**2
    Ls[c*Nx+1:(c+1)*Nx,-1] = C_aux[:,-1]/dR[c]**2
  bc[-1] = 0   # LBC: avoid reaction 
  Ls[-1,-1] = g*sum(H_f*H_R)*Nx*Dl[-1] # RBC: gathered terms for Sb
  return Id, Ls, bc

################################################################################
# This converts from the "zipped-format" to the more natural separated format
################################################################################
def nested_lists(C,Nx):
  Nt, Nc, N = C.shape
  Nr = (N-1)//Nx # Debe calzar justo justo
  C_list = []
  for ir in range(Nr):
    C_list.append([])
    for ic in range(Nc):
      C_intra = C[:,ic,ir*Nx:(ir+1)*Nx]
      C_bulk = np.array([C[:,ic,-1]]).T
      C_aux = np.concatenate( (C_intra,C_bulk), axis=1)
      C_list[ir].append( C_aux )
  return C_list


################################################################################
# AUXILIAR EVALUATION OF THE CATALYST ENZYME CONCENTRATION 'CAUSE CAN BE A FUNCTION
################################################################################
def eval_E(E, t):
  """
  Tries to evaluate the possibly function E, otherwise just returns the value E.
  """
  if type(E)==float or type(E)==int:
    return E
  else:
    try:
      return E(t)
    except:
      print("Something went awfully bad in eval_E(E,t)")
      return None
  return

def eval_Z(EnzymeRadialDistribution, H_R, Nx):
  """
  """
  Nc = len(H_R)
  rv = np.ones(Nx*Nc+1)
  if type(EnzymeRadialDistribution) in [float, int]:
    #print("Using a constant Enzyme Radial Distribution")
    return EnzymeRadialDistribution*rv
  else:
    try:
      #print("Using a Enzyme Radial Distribution defined by a function")
      for c, Rc in enumerate(H_R):
        for j in range(Nx):
          rv[c*Nx + j] = EnzymeRadialDistribution(j*Rc/Nx,Rc)
      return rv
    except:
      print("Something went awfully bad in eval_Z(E,t)")
      return None
  return

def total_enzyme_concentration(EnzymeRadialDistribution, H_R, Nx):
  """
  The total enzyme concentration is obtained though the formula:
   MY_FORMULA
  You need to evaluate: 
  * n_i: The number of particles of size R_i
  * EC_i: The enzyme concentration.
  sum n_i EC_i
  """
  Nc = len(H_R)
  enzyme_concentration = 0
  for c, Rc in enumerate(H_R):
    for j in range(Nx):
      R = j*Rc/Nx
      if type(EnzymeRadialDistribution) in [float, int]:
        Z = EnzymeRadialDistribution
      else:
        Z = EnzymeRadialDistribution(R,Rc)
      nc_enzyme_concentration = 4 * np.pi * Z * R**2
    enzyme_concentration = nc_enzyme_concentration 
  return enzyme_concentration

def print_time(t_sim_secs, t_total_secs, start_time, end_char=""):  
  t_sim_secs = int(t_sim_secs)
  t_total_secs = int(t_total_secs)
  elapsed_time_secs = int(time.time() - start_time)
  expected_time_secs = int(np.ceil(elapsed_time_secs * t_total_secs/ (t_sim_secs+0.1) ))
  remaining_time = "?" if (t_sim_secs<60) else int((expected_time_secs - elapsed_time_secs)/60.0) 
  sys.stdout.write("\rSimulated %03d secs out of %03s secs (Remaining time %s mins) %s" %(t_sim_secs, t_total_secs, remaining_time, end_char))
  sys.stdout.flush()
  return