char rcsid_caro2[] =
	"$Id$";

/*
 *  caro2.c: a program to explore some of the search space of Mike Caro's
 *	r.g.p. challenge #2.
 *              
 *  Copyright (C) 1993 - 1997 Clifford T. Matthews
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

#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>

#include "poker.h"
#include "eval7.h"

/* speed doesn't matter for lcd_of_first_n_positive_integers */

PRIVATE int
lcd_of_first_n_positive_integers (int n)
{
  int retval, i;
  boolean_t done;

  retval = n;
  done = false;

  while (!done)
    {
      done = true;
      for (i = 2; done && i <= n; ++i)
	if (retval % i)
	  {
	    done = false;
	    ++retval;
	  }
    }
  return retval;
}

#define MACRO_INSTEAD_OF_INLINE
#if !defined (MACRO_INSTEAD_OF_INLINE)

PRIVATE inline void
extr_suits (uint64 cards, rank_set_t *heartsp, rank_set_t *diamondsp,
	                  rank_set_t *clubsp,  rank_set_t *spadesp)
{
  *heartsp   =  cards        & 0x1FFF;
  *diamondsp = (cards >> 13) & 0x1FFF;
  *clubsp    = (cards >> 26) & 0x1FFF;
  *spadesp   = (cards >> 39) & 0x1FFF;
}

#else

#define extr_suits(cards, heartsp, diamondsp, clubsp, spadesp)	\
do								\
{								\
  *(heartsp)   =  (cards)        & 0x1FFF;			\
  *(diamondsp) = ((cards) >> 13) & 0x1FFF;			\
  *(clubsp)    = ((cards) >> 26) & 0x1FFF;			\
  *(spadesp)   = ((cards) >> 39) & 0x1FFF;			\
}								\
while (false)

#endif

PUBLIC int
main (int argc, char *argv[])
{
  uint64 hands[9];
  uint32 val, high_val;
  int to_reward[9], *rewardp;
  rank_set_t card_diffs[8 * 4], *card_diffp;
  int reward;
  int reward_table[10]; /* NOTE: 1-based array, not 0-based */
  uint32 score[9];
  int lcd;
  int i;
  uint8 n_cards;
  uint64 temp_card, dead_cards, pegged_common;
  uint64 card1, card2, card3, card4, card5;
  uint64 n1, n2, n3, n4, n5;
  boolean_t seen_cards_already;
  int hole_card_no;

  lcd = lcd_of_first_n_positive_integers (9);

  hole_card_no = 0;
  memset (hands, 0, sizeof hands);
  memset (score, 0, sizeof score);
  for (i = 1; i <= 9; ++i)
    reward_table[i] = lcd / i;

  n_cards = 5;
  dead_cards = 0;
  pegged_common = 0;
  seen_cards_already = false;
  for (i = 1; i < argc; ++i)
    {
      if (argv[i][0] == '-')
	{
	  if (seen_cards_already)
	    {
	      fprintf(stderr, "Cards must come before options\n");
	      exit(1);
	    }
	  if (strcmp (argv[i], "-d") == 0 ||
	      strcmp (argv[i], "-c") == 0)
	    {
	      if (i == argc)
		{
		  fprintf(stderr, "Missing card portion of -d\n");
		  exit(1);
		}
	      temp_card = string_to_card(argv[i]);
	      if (!temp_card)
		{
		  fprintf(stderr, "Malformed card \"%s\"\n", argv[i]);
		  exit(1);
		}
	      else
		{
		  if (argv[i][1] == 'c')
		    pegged_common |= temp_card;
		  dead_cards |= temp_card;
		  --n_cards;
		  ++i;
		}
	    }
	  else
	    {
	      fprintf(stderr, "Unknown switch \"%s\"\n", argv[i]);
	      exit(1);
	    }
	}
      else
	{
	  temp_card = string_to_card(argv[i]);
	  if (!temp_card)
	    {
	      fprintf(stderr, "Malformed card \"%s\"\n", argv[i]);
	      exit(1);
	    }
	  else
	    {
	      hands[hole_card_no++/2] |= temp_card;
	      dead_cards |= temp_card;
	    }
	}
    }

  if (hole_card_no != 18)
    {
      fprintf (stderr, "Wrong number of hole cards\n");
      exit (1);
    }

  card_diffp = card_diffs;
  for (i = 0; i < 8; ++i)
    {
      rank_set_t h0, h1, c0, c1, d0, d1, s0, s1;
      extr_suits (hands[i]  , &h0, &d0, &c0, &s0);
      extr_suits (hands[i+1], &h1, &d1, &c1, &s1);
      *card_diffp++ = h0 ^ h1;
      *card_diffp++ = d0 ^ d1;
      *card_diffp++ = c0 ^ c1;
      *card_diffp++ = s0 ^ s1;
    }

     n1 =    n2 =    n3 =    n4 =    n5 = 0;
  card1 = card2 = card3 = card4 = card5 = 0;

  switch (n_cards)
    {
    default:
      fprintf(stderr, "Number of cards to iterate must be "
	      "between 0 and 5 inclusive\n");
      exit(1);
    case 5:
      /* will set up normally below */
      break;
    case 4:
      card2 = (uint64) 1 << 51;
      n1    = hands[0] | pegged_common;
      break;
    case 3:
      card3 = (uint64) 1 << 51;
      n2    = hands[0] | pegged_common;
      break;
    case 2:
      card4 = (uint64) 1 << 51;
      n3    = hands[0] | pegged_common;
      break;
    case 1:
      card5 = (uint64) 1 << 51;
      n4    = hands[0] | pegged_common;
      break;
    case 0:
      n5    = hands[0] | pegged_common;
      break;
    }
  switch (n_cards)
    {
    case 5:
      for (card1 = (uint64) 1 << 51; card1 ; card1 >>= 1)
	{
	  if (card1 & dead_cards)
/*-->*/	    continue;
	  n1 = hands[0] | card1;
	  for (card2 = card1 >> 1; card2 ; card2 >>= 1)
	    {
    case 4:
	      if (card2 & dead_cards)
/*-->*/		continue;
	      n2 = n1 | card2;
	      for (card3 = card2 >> 1; card3 ; card3 >>= 1)
		{
    case 3:
		  if (card3 & dead_cards)
/*-->*/		    continue;
		  n3 = n2 | card3;
		  for (card4 = card3 >> 1; card4 ; card4 >>= 1)
		    {
    case 2:
		      if (card4 & dead_cards)
/*-->*/			continue;
		      n4 = n3 | card4;
		      for (card5 = card4 >> 1; card5 ; card5 >>= 1)
			{
			  rank_set_t hearts, clubs, diamonds, spades;

    case 1:
			  if (card5 & dead_cards)
/*-->*/			    continue;
			  n5 = n4 | card5;
    case 0:
                          extr_suits (n5, &hearts, &diamonds, &clubs, &spades);
			  high_val = 0;
			  rewardp = to_reward;
			  card_diffp = card_diffs;
			  i = 0;
			  {
loop:
			    val = eval_exactly_7_cards(hearts, diamonds,
						       clubs,  spades);
			    if (val >= high_val)
			      {
				if (val > high_val)
				  {
				    high_val = val;
				    rewardp = to_reward;
				  }
				*rewardp++ = i;
			      }
			    if (++i <= 8)
			      {
				hearts   ^= *card_diffp++;
				diamonds ^= *card_diffp++;
				clubs    ^= *card_diffp++;
				spades   ^= *card_diffp++;
				goto loop;
			      }
			  }
			  reward = reward_table[rewardp - to_reward];
			  do
			    score[*--rewardp] += reward;
			  while (rewardp > to_reward);
			}
		    }
		}
	    }
	}
    }

  {
    uint32 low, high;

    low = 0x7fffffff;
    high = 0;
  
    for (i = 0; i < 9; ++i)
      {
	printf ("        %9d\n", score[i]);
	if (score[i] < low)
	  low = score[i];
	if (score[i] > high)
	  high = score[i];
      }
    printf (" high = %9d\n  low = %9d\nratio = %f\n", high, low,
	    (float) high / low);
  }

  return 0;
}
