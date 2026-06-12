/*
 *  abs_synapse.cpp
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

#include "abs_synapse.h"

// Includes from nestkernel:
#include "common_synapse_properties.h"
#include "connector_model.h"
#include "connector_model_impl.h"
#include "model_manager_impl.h"
#include "nest_impl.h"


namespace felixmodule
{

  void register_abs_synapse()
  {
    nest::register_connection_model< abs_synapse >( "abs_synapse" );
  }
  
//
// Implementation of class ABSCommonProperties.
//

ABSCommonProperties::ABSCommonProperties()
  : CommonSynapseProperties()
  , theta_pre (0.05)   // theta_pre( 0.05 )
  , theta_plus(0.15) // theta_plus( 0.15 )
  , theta_minus(0.11) //theta_minus( 0.10 )
  , Delta(0.0006) //Delta( 0.0008 )
{
}

void
ABSCommonProperties::get_status( Dictionary& d ) const
{
  CommonSynapseProperties::get_status( d );

  d[ "theta_pre" ] = theta_pre;
  d[ "theta_plus" ] = theta_plus;
  d[ "theta_minus" ] = theta_minus;
  d[ "Delta" ] = Delta;
}

void
ABSCommonProperties::set_status( const Dictionary& d, nest::ConnectorModel& cm )
{
  CommonSynapseProperties::set_status( d, cm );

  d.update_value( "theta_pre", theta_pre );
  d.update_value( "theta_plus", theta_plus );
  d.update_value( "theta_minus", theta_minus );
  d.update_value( "Delta", Delta );
}

} // of namespace nest
