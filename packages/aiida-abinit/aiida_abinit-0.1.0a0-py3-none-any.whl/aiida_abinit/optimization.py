import os

import pymatgen as mg

from aiida import load_profile
from aiida.engine import run, calcfunction
from aiida.orm import (Code, Float, Str, Dict, StructureData)
from aiida_abinit.calculations import AbinitCalculation

from aiida_optimize import OptimizationWorkChain
from aiida_optimize.engines import Convergence
from aiida_optimize.wrappers import AddInputsWorkChain, CreateEvaluateWorkChain

load_profile()

CODE = 'abinit_9.2.1'

code = Code.get_from_string(CODE)
thisdir = os.path.dirname(os.path.realpath(__file__))

structure = StructureData(pymatgen=mg.Structure.from_file(
    os.path.join(thisdir, "../", 'Si_mp-149_primitive.cif')))

parameters_dict = {
    'code': code,
    'structure': structure,
    'parameters': Dict(dict={
        'ecut': 8.0,
        'kptopt': 1,
        'ngkpt': '4 4 4',
        'nshiftk': 1,
        'shiftk': '0 0 0',
        'nstep': 50,
        'toldfe': 1.0e-8,
        'diemac': 12.0,
        'pp_dirpath': '\"$ABI_PSPDIR\"',
        'pseudos': '\"PseudosTM_pwteter/14si.pspnc\"',
    }),
    'metadata': {
        'options': {
            'withmpi': True,
            'max_wallclock_seconds': 10 * 60,
            'resources': {
                'num_machines': 1,
                'num_mpiprocs_per_machine': 4,
            }
        }
    }
}

run(AbinitCalculation, **parameters_dict)

# run(
#     OptimizationWorkChain,
#     engine=Convergence,
#     engine_kwargs=Dict(dict=dict(
#         input_values=[10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
#         tol=5.0,
#         input_key='added_input_values',
#         result_key='output_parameters.energy',
#         convergence_window=2
#     )),
#     evaluate_process=AddInputsWorkChain,
#     evaluate={
#         'inputs': parameters_dict,
#         'added_input_keys': Str('parameters:ecut'),
#         'sub_process': Str(":".join([AbinitCalculation.__module__, AbinitCalculation.__name__]))
#     }
# )

# run(
#     CreateEvaluateWorkChain,
#     **{
#         'create': {
#             'added_input_keys': Str('parameters:ecut'),
#             'added_input_values': Float(8.0),
#             'inputs': parameters_dict,
#             'sub_process': Str(":".join([AbinitCalculation.__module__, AbinitCalculation.__name__]))
#         },
#         'create_process': Str(":".join([AddInputsWorkChain.__module__, AddInputsWorkChain.__name__])),
#         'evaluate': {},
#         'evaluate_process': Str(),
#         'output_input_mapping': Dict(dict={'output_parameters': 'output_parameters'})
#     }
# )
