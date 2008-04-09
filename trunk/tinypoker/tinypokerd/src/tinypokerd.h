/*
 * Copyright (C) 2005, 2006, 2007, 2008 Thomas Cort <tom@tomcort.com>
 * 
 * This file is part of tinypokerd.
 * 
 * tinypokerd is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option)
 * any later version.
 * 
 * tinypokerd is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 * 
 * You should have received a copy of the GNU General Public License along with
 * tinypokerd.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef __TINYPOKERD_H
#define __TINYPOKERD_H


#define TINYPOKERD_NAME "tinypokerd"
#define TINYPOKERD_VERSION "0.0.0"

#include <tinypoker.h>

#if (LIBTINYPOKER_MAJOR_VERSION == 0 && LIBTINYPOKER_MINOR_VERSION < 1)
#error "libtinypoker version too old. Minimum version is 0.1.0"
#endif

#endif
