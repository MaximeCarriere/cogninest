/*
 *  felixmodule.h
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

#ifndef FELIXMODULE_H
#define FELIXMODULE_H

// Includes from NEST:
#include "nest_extension_interface.h"

// Put your stuff into your own namespace.
namespace felixmodule
{

/**
 * Class defining your model.
 */
class Felixmodule : public nest::NESTExtensionInterface
{
public:
  Felixmodule() {}
  ~Felixmodule() override {}

  /**
   * Initialize module: register all node models and synapses.
   */
  void initialize() override;

};
} // namespace felixmodule

#endif
