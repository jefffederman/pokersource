/*
 *
 * Copyright (C) 2004, 2005, 2006 Mekensleep
 *
 *	Mekensleep
 *	24 rue vieille du temple
 *	75004 Paris
 *       licensing@mekensleep.com
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301, USA.
 *
 * Authors:
 * Henry Precheur	<henry at precheur dot org>
 *
 */

#ifndef	_INTERFACE_IO_H_
#define	_INTERFACE_IO_H_

char*	get_string(void);
int	get_int(void);

void	set_string(const char* str);
void	set_int(int i);
void	flush_io_channel(void);

int	init_interface_io(const char* adress);

#endif /* _INTERFACE_IO_H_ */
