# .............................................................................
#                              Electrical Machines
#                                   PY_RBF.py     
#                          (c) Oellerich, Jan (2026)
#                               weg//weiser GmbH
# .............................................................................

import os
import subprocess
from pathlib import Path
import numpy as np

# ... clear terminal
subprocess.run("cls" if os.name == "nt" else "clear", shell = True)

# ... functions
def NormalizeInput(InputArg1):
    # ... INPUT
    #       InputArg1   input values

    InputValues = InputArg1

    InputMinimum = InputValues.min(axis = 0)
    InputRange = InputValues.max(axis = 0) - InputMinimum

    if np.any(InputRange == 0):
        raise ValueError("Warning: At least one input dimension has no variation.")

    NormalizedInputValues = (InputValues - InputMinimum) / InputRange 

    # ... OUTPUT
    #       OuputArg    normalized input values
    OutputArg = NormalizedInputValues

    return OutputArg
#
#
#

def RBFWeights(InputArg1, InputArg2, InputArg3, InputArg4, KernelType):
    # ... INPUT
    #       InputArg1   normalized input data
    #       InputArg2   response data
    #       InputArg3   c
    #       InputArg4   lam
    #       KernelType
    #           "gaussian"
    #           "inversemultiquadric"
    #           "multiquadric"

    InputDataNormalized = np.asarray(InputArg1, dtype = float)
    ResponseData = np.asarray(InputArg2, dtype = float)
    c = InputArg3
    lam = InputArg4

    N = len(InputDataNormalized)


    # ... calculate differences
    Differences = (InputDataNormalized[:, np.newaxis, :] - InputDataNormalized[np.newaxis, :, :])

    
    # ... kernel matrix
    if KernelType.lower() == "gaussian":
        DistanceMatrix = np.sum(Differences**2, axis = 2)
        KernelMatrix = np.exp(-c * DistanceMatrix)

    elif KernelType.lower() == "inversequadratic":
        DistanceMatrix = np.sum(Differences**2, axis = 2)
        KernelMatrix = 1. / (1. + c * DistanceMatrix)
    
    elif KernelType.lower() == "inversemultiquadric":
        DistanceMatrix = np.sum(Differences**2, axis = 2)
        KernelMatrix = 1. / np.sqrt(1.0 + c * DistanceMatrix)
    
    elif KernelType.lower() == "multiquadric":
        DistanceMatrix = np.sum(Differences**2, axis = 2)
        KernelMatrix = np.sqrt(1.0 + c * DistanceMatrix)

    else:
        raise ValueError(f"Warning: Kernel '{KernelType}' not known.")

    
    # ... calculate weights
    #KernelMatrixRegularized = KernelMatrix + lam * np.eye(N)
    #Weights = np.linalg.solve(KernelMatrixRegularized, ResponseData)

    KernelMatrixRegularized = KernelMatrix.T @ KernelMatrix + lam * np.eye(N)
    B = KernelMatrix.T @ ResponseData
    Weights = np.linalg.solve(KernelMatrixRegularized, B)

    return Weights
#
#
#

def RBFFunction(InputArg1, InputArg2, InputArg3, InputArg4, KernelType):
    # ... INPUT
    #       InputArg1   normalized evaluation data
    #       InputArg2   normalized input data
    #       InputArg3   RBF weights
    #       InputArg4   c
    #       KernelType
    #           "gaussian"
    #           "inversemultiquadric"
    #           "multiquadric"
    
    EvaluationDataNormalized = np.asarray(InputArg1, dtype = float)
    InputDataNormalized = np.asarray(InputArg2, dtype = float)
    Weights = InputArg3
    c = InputArg4

    # ... quadratische Distanz zwischen Evaluations- und Trainingsdaten
    Differences = EvaluationDataNormalized[:, np.newaxis, :] - InputDataNormalized[np.newaxis, :, :]
    

    # ... kernel matrix
    if KernelType.lower() == "gaussian":
        DistanceSquared = np.sum(Differences**2, axis = 2)
        KernelMatrix = np.exp(-c * DistanceSquared)

    elif KernelType.lower() == "inversequadratic":
        DistanceMatrix = np.sum(Differences**2, axis = 2)
        KernelMatrix = 1. / (1. + c * DistanceMatrix)
    
    elif KernelType.lower() == "inversemultiquadric":
        DistanceSquared = np.sum(Differences**2, axis = 2)
        KernelMatrix = 1.0 / np.sqrt(1.0 + c * DistanceSquared)
    
    elif KernelType.lower() == "multiquadric":
        DistanceSquared = np.sum(Differences**2, axis = 2)
        KernelMatrix = np.sqrt(1.0 + c * DistanceSquared)
        
    else:
        raise ValueError(f"Warning: Kernel '{KernelType}' not known.")


    # ... calculate response
    ResponsePrediction = (KernelMatrix @ Weights)


    # ... OUTPUT
    return ResponsePrediction
#
#
#

def RBFGradient(InputArg1, InputArg2, InputArg3, InputArg4, InputArg5, KernelType):
    # ... INPUT
    #       InputArg1   input data (original data)
    #       InputArg2   normalized evaluation data (M, d)
    #       InputArg3   normalized input data (N, d)
    #       InputArg4   RBF weights (N,)
    #       InputArg5   c
    #       KernelType  
    #           "gaussian" 
    #           "inverseMultiquadric" 
    #           "multiquadric"
    
    InputData = InputArg1
    EvaluationDataNormalized = InputArg2
    InputDataNormalized = InputArg3
    Weights = InputArg4
    c = InputArg5

    # ... normalize data
    InputMinimum = InputData.min(axis = 0)
    InputRange = InputData.max(axis = 0) - InputMinimum

    # Differences: (M, N, d) 
    Differences = EvaluationDataNormalized[:, np.newaxis, :] - InputDataNormalized[np.newaxis, :, :]
    
    # DistanceSquared: (M, N)
    DistanceSquared = np.sum(Differences**2, axis = 2)
    
    # ... kernel matrix 
    if KernelType.lower() == "gaussian":
        EvaluationKernel = np.exp(-c * DistanceSquared)
        GradientKernel = -2.0 * c * Differences * EvaluationKernel[:, :, np.newaxis]

    elif KernelType.lower() == "inversequadratic":
        EvaluationKernel = (1.0 / (1.0 + c * DistanceSquared))**2
        GradientKernel = -2.0 * c * Differences * EvaluationKernel[:, :, np.newaxis]
    
    elif KernelType.lower() == "inversemultiquadric":
        EvaluationKernelCube = (1.0 / np.sqrt(1.0 + c * DistanceSquared))**3
        GradientKernel = -c * Differences * EvaluationKernelCube[:, :, np.newaxis]
        
    elif KernelType.lower() == "multiquadric":
        EvaluationKernelInverse = 1.0 / np.sqrt(1.0 + c * DistanceSquared)
        GradientKernel = c * Differences * EvaluationKernelInverse[:, :, np.newaxis]
        
    else:
        raise ValueError(f"Warning: Kernel '{KernelType}' not known for gradient calculation.")

    # ... calculate gradient
    # Weights Form: (1, N, 1), GradientKernel Form: (M, N, d) 
    GradientNormalized = np.sum(Weights[np.newaxis, :, np.newaxis] * GradientKernel, axis = 1) # Form: (M, d)
    
    # ... OUTPUT
    Gradient = GradientNormalized / InputRange 

    return Gradient
#
#
#
#
#





# ... section 1: RBF fit on input values ......................................
Data = np.loadtxt(Path(__file__).resolve().parents[2] / "datasets/historical_exports/Dataset_Raw_vs_Fitted_Flux.dat", skiprows = 1)
#Data = np.loadtxt("DAT/Dataset_Himmelblau_Lowess_Gradient.dat", skiprows = 1)
#Data = np.loadtxt("DAT/Dataset_Rosenbrock_Lowess_Gradient.dat", skiprows = 1)

# ... prepare fitting data
InputData = Data[:, 0:2]
ResponseData = Data[:, 2] 
InputDataNormalized = NormalizeInput(InputData)


# ... perform RBF fitting
#KernelType = "gaussian"
#KernelType = "inversequadratic"
#KernelType = "multiquadric"
KernelType = "inversemultiquadric"

c = 10
lam = 1E-03


Weights = RBFWeights(InputDataNormalized, ResponseData, c, lam, KernelType)
SmoothFunction = RBFFunction(InputDataNormalized, InputDataNormalized, Weights, c, KernelType) 
SmoothGradient = RBFGradient(InputData, InputDataNormalized, InputDataNormalized, Weights, c, KernelType)
GradientX = SmoothGradient[:, 0]
GradientY = SmoothGradient[:, 1]


# ... calculate residuals
ResidualFunction = SmoothFunction - ResponseData
ResidualFunctionMaximum = np.max(np.abs(ResidualFunction))
ResidualFunctionMean = np.mean(np.abs(ResidualFunction))

SSresFunction = np.sum((ResponseData - SmoothFunction)**2)
SStotFunction = np.sum((ResponseData - np.mean(ResponseData))**2)

RsquaredFunction = 1 - SSresFunction / SStotFunction

print(f"ResidualFunctionMaximum     {ResidualFunctionMaximum:6f}")
print(f"ResidualFunctionMean        {ResidualFunctionMean:6f}")
print(f"ResidualFunctionSquared     {RsquaredFunction:6f}")
