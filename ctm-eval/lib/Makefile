LIB=libpoker.a
AR=ar

OBJ=dump_cards.o dump_eval.o dump_rank.o hand_names.o n_bits_table.o \
	top_five_cards_table.o top_card_table.o mask_rank_table.o \
	str_and_flu_table.o straight_table.o rank_fsm_table.o \
	cards_to_counts_table.o string_to_card.o \
	three_of_a_kind_value_table.o top_pair_table.o \
	pair_value_table.o straight_value_table.o flush_cards_table.o \
	newdumpeval.o rank_names.o top_bit_table.o top_five_bits_table.o \
	plural_ranks.o md5c.o 

DERIVED_SRC=n_bits_table.c top_five_cards_table.c top_card_table.c \
	mask_rank_table.c str_and_flu_table.c straight_table.c \
	rank_fsm_table.c cards_to_counts_table.c \
	three_of_a_kind_value_table.c top_pair_table.c \
	pair_value_table.c straight_value_table.c flush_cards_table.c \
	top_bit_table.c top_five_bits_table.c

CFLAGS=-g -O4 -Wall -finline-functions -Winline -DNDEBUG -fomit-frame-pointer -D_REENTRANT
# CC=egcs
# CFLAGS=-g -O6 -Wall -finline-functions -Winline -DNDEBUG -fomit-frame-pointer -mpentiumpro
# CFLAGS=-g -Wall
RANLIB=ranlib

all:	$(LIB) ../include/eval7.h ../include/eval5.h ../include/bit_order.h

$(OBJ):	../include/bit_order.h

$(LIB): $(OBJ)
	$(AR) cr $(LIB) $(OBJ)
	$(RANLIB) $(LIB)

clean:
	rm -f $(OBJ) $(LIB) $(DERIVED_SRC) mktables core makeswitch.o \
			makeswitch ../include/eval7.h endian.o endian \
			../include/bit_order.h makeswitch5.o makeswitch5 \
			../include/eval5.h

$(DERIVED_SRC): mktables
	./mktables $@

mktables:       mktables.c
	$(CC) $(CFLAGS) -I../include -o mktables mktables.c

.c.o:
	$(CC) $(CFLAGS) -I../include -c $<

makeswitch:	makeswitch.o
	$(CC) -o makeswitch makeswitch.o

../include/eval7.h:	makeswitch
	./makeswitch > ../include/eval7.h

../include/bit_order.h:	endian
	./endian > ../include/bit_order.h

makeswitch5.o:	makeswitch.c
	$(CC) $(CFLAGS) -I../include -DCARDS_DEALT=5 -c $< -o makeswitch5.o

makeswitch.o:	makeswitch.c
	$(CC) $(CFLAGS) -I../include -DCARDS_DEALT=7 -c $<

makeswitch5:	makeswitch5.o
	$(CC) -o makeswitch5 makeswitch5.o

../include/eval5.h:	makeswitch5
	./makeswitch5 > ../include/eval5.h
