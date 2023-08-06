# -*- coding: utf-8 -*-
"""Workchain to relax a structure using Abinit"""
from aiida import orm
from aiida.common import AttributeDict, exceptions
from aiida.engine import WorkChain, ToContext, if_, while_, append_
from aiida.plugins import CalculationFactory, WorkflowFactory

AbinitBaseWorkChain = WorkflowFactory('abinit.base')

class AbinitRelaxWorkChain(WorkChain):
    """Workchain to relax a structure using Abinit"""

    @classmethod
    def define(cls, spec):
        """Define the process specification."""
        # yapf: disable
        super().define(spec)
        spec.expose_inputs(AbinitBaseWorkChain, namespace='base',
            exclude=('abinit.structure', 'abinit.parent_folder'),
            namespace_options={'help': 'Inputs for the `AbinitBaseWorkChain`.'})
        spec.input('structure', valid_type=orm.StructureData, help='The inputs structure.')
        spec.input('optcell', valid_type=orm.Int, default=lambda: orm.Int(2),
            help='The relaxation scheme to use.')          
        spec.input('ionmov', valid_type=orm.Int, default=lambda: orm.Int(2),
            help='The relaxation scheme to use.')          
        spec.outline(
            cls.setup,
            cls.run_relax,
            cls.inspect_relax,
            cls.results,
        )

    def setup(self):
        """Input validation and context setup."""
        self.ctx.current_number_of_bands = None
        self.ctx.current_structure = self.inputs.structure
        self.ctx.current_cell_volume = None
        self.ctx.is_converged = False
        self.ctx.iteration = 0



