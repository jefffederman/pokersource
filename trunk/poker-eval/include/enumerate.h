#define ENUMERATE_1_CARDS(cards_var, action)    \
{                                               \
  int _i1;                                      \
  CardMask _card;                               \
                                                \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) { \
    _card = Deck_MASK(_i1);                     \
    cards_var = _card;                          \
    do { action } while (0);                    \
  };                                            \
}

#define ENUMERATE_2_CARDS(cards_var, action)    \
{                                               \
  int _i1, _i2;                                 \
  CardMask _card1, _card2,                      \
    _n2;                                        \
                                                \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) { \
    _card1 = Deck_MASK(_i1);                    \
    for (_i2 = _i1-1; _i2 >= 0; _i2--) {        \
      _card2 = Deck_MASK(_i2);                  \
      CardMask_OR(_n2, _card1, _card2);         \
      cards_var = _n2;                          \
      do { action } while (0);                  \
    };                                          \
  };                                            \
}                                               \

#define ENUMERATE_3_CARDS(cards_var, action)    \
{                                               \
  int _i1, _i2, _i3;                            \
  CardMask _card1, _card2, _card3,              \
    _n2, _n3;                                   \
                                                \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) { \
    _card1 = Deck_MASK(_i1);                    \
    for (_i2 = _i1-1; _i2 >= 0; _i2--) {        \
      _card2 = Deck_MASK(_i2);                  \
      CardMask_OR(_n2, _card1, _card2);         \
      for (_i3 = _i2-1; _i3 >= 0; _i3--) {      \
        _card3 = Deck_MASK(_i3);                \
	CardMask_OR(_n3, _n2, _card3);          \
        cards_var = _n3;                        \
        do { action } while (0);                \
      };                                        \
    };                                          \
  };                                            \
}

#define ENUMERATE_4_CARDS(cards_var, action)    \
{                                               \
  int _i1, _i2, _i3, _i4;                       \
  CardMask _card1, _card2, _card3, _card4,      \
    _n2, _n3, _n4;                              \
                                                \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) { \
    _card1 = Deck_MASK(_i1);                    \
    for (_i2 = _i1-1; _i2 >= 0; _i2--) {        \
      _card2 = Deck_MASK(_i2);                  \
      CardMask_OR(_n2, _card1, _card2);         \
      for (_i3 = _i2-1; _i3 >= 0; _i3--) {      \
        _card3 = Deck_MASK(_i3);                \
	CardMask_OR(_n3, _n2, _card3);          \
        for (_i4 = _i3-1; _i4 >= 0; _i4--) {    \
          _card4 = Deck_MASK(_i4);              \
	  CardMask_OR(_n4, _n3, _card4);        \
          cards_var = _n4;                      \
          do { action } while (0);              \
        };                                      \
      };                                        \
    };                                          \
  };                                            \
}

#define ENUMERATE_5_CARDS(cards_var, action)            \
{                                                       \
  int _i1, _i2, _i3, _i4, _i5;                          \
  CardMask _card1, _card2, _card3, _card4, _card5,      \
    _n2, _n3, _n4, _n5;                                 \
                                                        \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) {         \
    _card1 = Deck_MASK(_i1);                            \
    for (_i2 = _i1-1; _i2 >= 0; _i2--) {                \
      _card2 = Deck_MASK(_i2);                          \
      CardMask_OR(_n2, _card1, _card2);                 \
      for (_i3 = _i2-1; _i3 >= 0; _i3--) {              \
        _card3 = Deck_MASK(_i3);                        \
	CardMask_OR(_n3, _n2, _card3);                  \
        for (_i4 = _i3-1; _i4 >= 0; _i4--) {            \
          _card4 = Deck_MASK(_i4);                      \
	  CardMask_OR(_n4, _n3, _card4);                \
          for (_i5 = _i4-1; _i5 >= 0; _i5--) {          \
            _card5 = Deck_MASK(_i5);                    \
            CardMask_OR(_n5, _n4, _card5);              \
            cards_var = _n5;                            \
            do { action } while (0);                    \
          };                                            \
        };                                              \
      };                                                \
    };                                                  \
  };                                                    \
}


#define ENUMERATE_1_CARDS_D(cards_var, dead_cards, action)      \
{                                                               \
  int _i1;                                                      \
  CardMask _card;                                               \
                                                                \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) {                 \
    _card = Deck_MASK(_i1);                                     \
    if (CardMask_ANY_SET(dead_cards, _card))                    \
      continue;                                                 \
    cards_var = _card;                                          \
    do { action } while (0);                                    \
  };                                                            \
}

#define ENUMERATE_2_CARDS_D(cards_var, dead_cards, action)      \
{                                                               \
  int _i1, _i2;                                                 \
  CardMask _card1, _card2,                                      \
    _n2;                                                        \
                                                                \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) {                 \
    _card1 = Deck_MASK(_i1);                                    \
    if (CardMask_ANY_SET(dead_cards, _card1))                   \
      continue;                                                 \
    for (_i2 = _i1-1; _i2 >= 0; _i2--) {                        \
      _card2 = Deck_MASK(_i2);                                  \
      if (CardMask_ANY_SET(dead_cards, _card2))                 \
        continue;                                               \
      CardMask_OR(_n2, _card1, _card2);                         \
      cards_var = _n2;                                          \
      do { action } while (0);                                  \
    };                                                          \
  };                                                            \
}

#define ENUMERATE_3_CARDS_D(cards_var, dead_cards, action)      \
{                                                               \
  int _i1, _i2, _i3;                                            \
  CardMask _card1, _card2, _card3,                              \
    _n2, _n3;                                                   \
                                                                \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) {                 \
    _card1 = Deck_MASK(_i1);                                    \
    if (CardMask_ANY_SET(dead_cards, _card1))                   \
      continue;                                                 \
    for (_i2 = _i1-1; _i2 >= 0; _i2--) {                        \
      _card2 = Deck_MASK(_i2);                                  \
      if (CardMask_ANY_SET(dead_cards, _card2))                 \
        continue;                                               \
      CardMask_OR(_n2, _card1, _card2);                         \
      for (_i3 = _i2-1; _i3 >= 0; _i3--) {                      \
        _card3 = Deck_MASK(_i3);                                \
        if (CardMask_ANY_SET(dead_cards, _card3))               \
          continue;                                             \
	CardMask_OR(_n3, _n2, _card3);                          \
        cards_var = _n3;                                        \
        do { action } while (0);                                \
      };                                                        \
    };                                                          \
  };                                                            \
}

#define ENUMERATE_4_CARDS_D(cards_var, dead_cards, action)      \
{                                                               \
  int _i1, _i2, _i3, _i4;                                       \
  CardMask _card1, _card2, _card3, _card4,                      \
    _n2, _n3, _n4;                                              \
                                                                \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) {                 \
    _card1 = Deck_MASK(_i1);                                    \
    if (CardMask_ANY_SET(dead_cards, _card1))                   \
      continue;                                                 \
    for (_i2 = _i1-1; _i2 >= 0; _i2--) {                        \
      _card2 = Deck_MASK(_i2);                                  \
      if (CardMask_ANY_SET(dead_cards, _card2))                 \
        continue;                                               \
      CardMask_OR(_n2, _card1, _card2);                         \
      for (_i3 = _i2-1; _i3 >= 0; _i3--) {                      \
        _card3 = Deck_MASK(_i3);                                \
        if (CardMask_ANY_SET(dead_cards, _card3))               \
          continue;                                             \
	CardMask_OR(_n3, _n2, _card3);                          \
        for (_i4 = _i3-1; _i4 >= 0; _i4--) {                    \
          _card4 = Deck_MASK(_i4);                              \
          if (CardMask_ANY_SET(dead_cards, _card4))             \
            continue;                                           \
	  CardMask_OR(_n4, _n3, _card4);                        \
          cards_var = _n4;                                      \
          do { action } while (0);                              \
        };                                                      \
      };                                                        \
    };                                                          \
  };                                                            \
}

#define ENUMERATE_5_CARDS_D(cards_var, dead_cards, action)      \
{                                                               \
  int _i1, _i2, _i3, _i4, _i5;                                  \
  CardMask _card1, _card2, _card3, _card4, _card5,              \
    _n2, _n3, _n4, _n5;                                         \
                                                                \
  for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) {                 \
    _card1 = Deck_MASK(_i1);                                    \
    if (CardMask_ANY_SET(dead_cards, _card1))                   \
      continue;                                                 \
    for (_i2 = _i1-1; _i2 >= 0; _i2--) {                        \
      _card2 = Deck_MASK(_i2);                                  \
      if (CardMask_ANY_SET(dead_cards, _card2))                 \
        continue;                                               \
      CardMask_OR(_n2, _card1, _card2);                         \
      for (_i3 = _i2-1; _i3 >= 0; _i3--) {                      \
        _card3 = Deck_MASK(_i3);                                \
        if (CardMask_ANY_SET(dead_cards, _card3))               \
          continue;                                             \
	CardMask_OR(_n3, _n2, _card3);                          \
        for (_i4 = _i3-1; _i4 >= 0; _i4--) {                    \
          _card4 = Deck_MASK(_i4);                              \
          if (CardMask_ANY_SET(dead_cards, _card4))             \
            continue;                                           \
	  CardMask_OR(_n4, _n3, _card4);                        \
          for (_i5 = _i4-1; _i5 >= 0; _i5--) {                  \
            _card5 = Deck_MASK(_i5);                            \
            if (CardMask_ANY_SET(dead_cards, _card5))           \
              continue;                                         \
            CardMask_OR(_n5, _n4, _card5);                      \
            cards_var = _n5;                                    \
            do { action } while (0);                            \
          };                                                    \
        };                                                      \
      };                                                        \
    };                                                          \
  };                                                            \
}




#define ENUMERATE_N_CARDS_D(cards_var, n_cards, dead_cards, action) {      \
  int _i1, _i2, _i3, _i4, _i5, _i6, _i7, _i8, _i9;                         \
  CardMask _card1, _card2, _card3, _card4, _card5,                         \
    _card6, _card7, _card8, _card9,                                        \
    _n1, _n2, _n3, _n4, _n5, _n6, _n7, _n8, _n9;                           \
                                                                           \
  _i1 = _i2 = _i3 = _i4 = _i5 = _i6 = _i7 = _i8 = _i9 = 0;                 \
  CardMask_RESET(_card9);                                                  \
  _card1 = _card2 = _card3 = _card4 = _card5 = _card6                      \
    = _card7 = _card8 = _card9;                                            \
  CardMask_RESET(_n9);                                                     \
  _n1 = _n2 = _n3 = _n4 = _n5 = _n6 = _n7 = _n8 = _n9;                     \
                                                                           \
  switch (n_cards) {                                                       \
  default:                                                                 \
  case 9:                                                                  \
  case 0:                                                                  \
    break;                                                                 \
  case 8:                                                                  \
    _i2 = Deck_N_CARDS-1;                                                  \
    break;                                                                 \
  case 7:                                                                  \
    _i3 = Deck_N_CARDS-1;                                                  \
    break;                                                                 \
  case 6:                                                                  \
    _i4 = Deck_N_CARDS-1;                                                  \
    break;                                                                 \
  case 5:                                                                  \
    _i5 = Deck_N_CARDS-1;                                                  \
    break;                                                                 \
  case 4:                                                                  \
    _i6 = Deck_N_CARDS-1;                                                  \
    break;                                                                 \
  case 3:                                                                  \
    _i7 = Deck_N_CARDS-1;                                                  \
    break;                                                                 \
  case 2:                                                                  \
    _i8 = Deck_N_CARDS-1;                                                  \
    break;                                                                 \
  case 1:                                                                  \
    _i9 = Deck_N_CARDS-1;                                                  \
    break;                                                                 \
  }                                                                        \
  switch (n_cards) {                                                       \
  default:                                                                 \
    fprintf(stderr, "ENUMERATE_N_CARDS: n-cards must be in range 0..9\n"); \
    break;                                                                 \
                                                                           \
  case 9:                                                                  \
    for (_i1 = Deck_N_CARDS-1; _i1 >= 0; _i1--) {                          \
      _card1 = Deck_MASK(_i1);                                             \
      if (CardMask_ANY_SET(dead_cards, _card1))                            \
        continue;                                                          \
      _n1 = _card1;                                                        \
      for (_i2 = _i1-1; _i2 >= 0; _i2--) {                                 \
  case 8:                                                                  \
        _card2 = Deck_MASK(_i2);                                           \
        if (CardMask_ANY_SET(dead_cards, _card2))                          \
          continue;                                                        \
        CardMask_OR(_n2, _n1, _card2);                                     \
        for (_i3 = _i2-1; _i3 >= 0; _i3--) {                               \
  case 7:                                                                  \
          _card3 = Deck_MASK(_i3);                                         \
          if (CardMask_ANY_SET(dead_cards, _card3))                        \
            continue;                                                      \
          CardMask_OR(_n3, _n2, _card3);                                   \
          for (_i4 = _i3-1; _i4 >= 0; _i4--) {                             \
  case 6:                                                                  \
            _card4 = Deck_MASK(_i4);                                       \
            if (CardMask_ANY_SET(dead_cards, _card4))                      \
              continue;                                                    \
            CardMask_OR(_n4, _n3, _card4);                                 \
            for (_i5 = _i4-1; _i5 >= 0; _i5--) {                           \
  case 5:                                                                  \
              _card5 = Deck_MASK(_i5);                                     \
              if (CardMask_ANY_SET(dead_cards, _card5))                    \
                continue;                                                  \
              CardMask_OR(_n5, _n4, _card5);                               \
              for (_i6 = _i5-1; _i6 >= 0; _i6--) {                         \
  case 4:                                                                  \
                _card6 = Deck_MASK(_i6);                                   \
                if (CardMask_ANY_SET(dead_cards, _card6))                  \
                  continue;                                                \
                CardMask_OR(_n6, _n5, _card6);                             \
                for (_i7 = _i6-1; _i7 >= 0; _i7--) {                       \
  case 3:                                                                  \
                  _card7 = Deck_MASK(_i7);                                 \
                  if (CardMask_ANY_SET(dead_cards, _card7))                \
                    continue;                                              \
                  CardMask_OR(_n7, _n6, _card7);                           \
                  for (_i8 = _i7-1; _i8 >= 0; _i8--) {                     \
  case 2:                                                                  \
                    _card8 = Deck_MASK(_i8);                               \
                    if (CardMask_ANY_SET(dead_cards, _card8))              \
                      continue;                                            \
                    CardMask_OR(_n8, _n7, _card8);                         \
                    for (_i9 = _i8-1; _i9 >= 0; _i9--) {                   \
  case 1:                                                                  \
                      _card9 = Deck_MASK(_i9);                             \
                      if (CardMask_ANY_SET(dead_cards, _card9))            \
                        continue;                                          \
                      CardMask_OR(_n9, _n8, _card9);                       \
  case 0:                                                                  \
                        cards_var = _n9;                                   \
                        do { action } while (0);                           \
		    }                                                      \
		  }                                                        \
		}                                                          \
	      }                                                            \
	    }                                                              \
	  }                                                                \
	}                                                                  \
      }                                                                    \
    }                                                                      \
  }                                                                        \
}

