#ifndef __EVX_DEFS__
#define __EVX_DEFS__

#define EvxHandVal_TYPE_SHIFT     (2 * StdDeck_Rank_COUNT)
#define EvxHandVal_SIGCARDS_SHIFT StdDeck_Rank_COUNT
#define EvxHandVal_KICKERS_SHIFT  0

#define EvxHandVal_MAKETYPE(ht) ((ht) << EvxHandVal_TYPE_SHIFT)
#define EvxHandVal_GETTYPE(ehv) ((ehv) >> EvxHandVal_TYPE_SHIFT)

enum {
  EvxHandVal_NOPAIR    = EvxHandVal_MAKETYPE(StdRules_HandType_NOPAIR), 
  EvxHandVal_ONEPAIR   = EvxHandVal_MAKETYPE(StdRules_HandType_ONEPAIR), 
  EvxHandVal_TWOPAIR   = EvxHandVal_MAKETYPE(StdRules_HandType_TWOPAIR), 
  EvxHandVal_TRIPS     = EvxHandVal_MAKETYPE(StdRules_HandType_TRIPS), 
  EvxHandVal_STRAIGHT  = EvxHandVal_MAKETYPE(StdRules_HandType_STRAIGHT), 
  EvxHandVal_FLUSH     = EvxHandVal_MAKETYPE(StdRules_HandType_FLUSH), 
  EvxHandVal_FULLHOUSE = EvxHandVal_MAKETYPE(StdRules_HandType_FULLHOUSE), 
  EvxHandVal_QUADS     = EvxHandVal_MAKETYPE(StdRules_HandType_QUADS), 
  EvxHandVal_STFLUSH   = EvxHandVal_MAKETYPE(StdRules_HandType_STFLUSH),
};

extern uint32 evxPairValueTable[StdDeck_N_RANKMASKS];
extern uint32 evxTripsValueTable[StdDeck_N_RANKMASKS];
extern uint32 evxStrValueTable[StdDeck_N_RANKMASKS];
extern uint32 evxFlushCardsTable[StdDeck_N_RANKMASKS];

#endif
