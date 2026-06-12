/*
 *  felixmodule.cpp
 *
 *  This file is part of NEST.
 *
 *  Copyright (C) 2004 The NEST Initiative
 *
 *  NEST is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  NEST is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with NEST.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#include "felixmodule.h"

// include headers with your own stuff
#include "abs_synapse.h"
#include "felix_exc.h"
#include "felix_inh.h"
#include "felix_spike_recorder.h"

// Define module instance outside of namespace to avoid name-mangling problems.
// NEST 3.8+ uses the symbol <modulename>_LTX_module (not _LTX_mod).
felixmodule::Felixmodule felixmodule_LTX_module;

void
felixmodule::Felixmodule::initialize()
{
  nest::kernel().model_manager.register_node_model< felixmodule::felix_exc >( "felix_exc" );
  nest::kernel().model_manager.register_node_model< felixmodule::felix_inh >( "felix_inh" );
  nest::kernel().model_manager.register_node_model< felixmodule::felix_spike_recorder >( "felix_spike_recorder" );

  register_abs_synapse();
}
