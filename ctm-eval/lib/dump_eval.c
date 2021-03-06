char rcsid_dump_eval[] =
	"$Id$";

/*
 *  dump_eval.c: a poker helper routine
 *
 *  Copyright (C) 1993 - 1995  Clifford T. Matthews
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */


#include "poker.h"
#include <stdio.h>

PUBLIC void dump_eval( eval_u eval )
{
    printf("%s: %s", hand_info[eval.eval_t.hand].hand_name,
					     rank_names[eval.eval_t.top_card]);
    if (hand_info[eval.eval_t.hand].n_significant_ranks >= 2)
	printf(", %s", rank_names[eval.eval_t.second_card]);
    if (hand_info[eval.eval_t.hand].n_significant_ranks >= 3)
	printf(", %s", rank_names[eval.eval_t.third_card]);
    if (hand_info[eval.eval_t.hand].n_significant_ranks >= 4)
	printf(", %s", rank_names[eval.eval_t.fourth_card]);
    if (hand_info[eval.eval_t.hand].n_significant_ranks >= 5)
	printf(", %s", rank_names[eval.eval_t.fifth_card]);

    printf("\n");
}
