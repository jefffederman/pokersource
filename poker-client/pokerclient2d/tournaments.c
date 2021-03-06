/**
 * Copyright (C) 2005, 2006 Mekensleep <licensing@mekensleep.com>
 *                          24 rue vieille du temple, 75004 Paris
 *
 * This software's license gives you freedom; you can copy, convey,
 * propagate, redistribute and/or modify this program under the terms of
 * the GNU Affero General Public License (AGPL) as published by the Free
 * Software Foundation (FSF), either version 3 of the License, or (at your
 * option) any later version of the AGPL published by the FSF.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
 * General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program in a file in the toplevel directory called
 * "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
 *
 * Authors:
 *  Loic Dachary <loic@dachary.org>
 *  Cedric Pinson <cpinson@freesheep.org>
 */

#include <time.h>
#include <stdio.h>
#include <string.h>
#include <gtk/gtk.h>
#include <glade/glade.h>
#include "gui.h"
#include "interface_io.h"
#include "dispatcher.h"

#include <libintl.h>

extern enum lobby_tab_state g_lobby_tab_state;
static GladeXML* s_tournaments_xml = 0;
static GtkWidget*	s_tournaments_window = 0;
static GtkLabel*	s_players_label = 0;
static GtkLabel*	s_tournaments_label = 0;
static GtkLabel*	s_register_unregister_label = 0;
static GtkButton*	s_register_unregister_button = 0;
static GtkListStore* s_sit_n_go_store = 0;
static GtkTreeSelection* s_sit_n_go_selection = 0;
static GtkListStore* s_regular_store = 0;
static GtkTreeSelection* s_regular_selection = 0;
static GtkNotebook* s_notebook = 0;

static GtkWidget*	s_tournament_info_window = 0;
static GtkListStore* s_players_store = 0;
static int s_disable_buttons = 0;
static GtkWidget*	s_lobby_tabs_window = 0;

static GtkWidget*	s_cashier_button_window = 0;
static GtkButton*	s_cashier_button = 0;

static int		s_tournaments_window_shown = 0;
static GtkLayout* s_screen = 0;

static int can_register = 0;

#define PAGE_REGULAR 0
#define PAGE_SIT_N_GO 1

static void clear_stores(void) {
  gtk_list_store_clear(s_sit_n_go_store);
  gtk_list_store_clear(s_regular_store);
  gtk_list_store_clear(s_players_store);
}

static void	close_tournaments(void)
{
	if (s_screen == NULL)
		return;

  gtk_widget_hide(s_tournaments_window);
  gtk_widget_hide(s_tournament_info_window);
  gtk_widget_hide(s_lobby_tabs_window);
  gtk_widget_hide(s_cashier_button_window);
  clear_stores();
}

static void	on_tournament_register_unregister_clicked(GtkWidget *widget, gpointer user_data)
{
  (void) widget;
  int* selection = (int*)user_data;
  if(*selection > 0) {
      set_string("tournaments");
      set_string(can_register ? "register" : "unregister");
      set_int(*selection);
      flush_io_channel();
  } else
    g_message("no row selected.\n");
}

static void	on_row_activated(GtkTreeView        *treeview,
                             GtkTreePath        *path,
                             GtkTreeViewColumn  *col,
                             gpointer            user_data)
{
  (void) col;
  (void) user_data;

  g_message("row clicked");
  GtkTreeModel*	model;
  GtkTreeIter   iter;

  model = gtk_tree_view_get_model(treeview);

  if (gtk_tree_model_get_iter(model, &iter, path))
    {
      int	id;

      gtk_tree_model_get(model, &iter, 0, &id, -1);
      g_message("Double-clicked row contains %d", id);
#if 0
      set_string("tournaments");
      set_string("select");
      set_int(id);
      flush_io_channel();
      close_tournaments();
#endif
    }
  else
    g_warning("row_activated: unable to find active row");
}

static void	on_tournament_list_treeview_selection_changed(GtkTreeSelection *treeselection,
                                                              gpointer user_data)
{
  int* selection = (int*)user_data;

  GtkTreeModel*	model;
  GtkTreeIter   iter;

  if(gtk_tree_selection_get_selected(treeselection, &model, &iter)) {
      int	id;

      gtk_tree_model_get(model, &iter, 0, &id, -1);
      g_message("clicked row contains %d", id);
      set_string("tournaments");
      set_string("details");
      set_int(id);
      flush_io_channel();

      *selection = id;
    }
  else
    g_warning("treeview_selection: unable to find active row");
}


static void	on_table_toggled(GtkWidget *widget, gpointer user_data)
{
  (void) user_data;

  if(gtk_toggle_button_get_active(GTK_TOGGLE_BUTTON(widget))) {
    set_string("tournaments");
    set_string("quit");
    set_string(gtk_widget_get_name(widget));
    flush_io_channel();
  }
}
//bridge for lobby.c
void tournament_on_table_toggled(GtkWidget *widget, gpointer user_data)
{
  on_table_toggled(widget, user_data);
}


static void	on_tourney_toggled(GtkWidget *widget, gpointer user_data)
{
  (void) user_data;

  if(gtk_toggle_button_get_active(GTK_TOGGLE_BUTTON(widget))) {
    const char* name = gtk_widget_get_name(widget);
    set_string("tournaments");
    set_string("refresh");
    set_string(name);
    flush_io_channel();
    if(!strcmp(name, "sit_n_go")) {
      gtk_notebook_set_current_page(s_notebook, PAGE_SIT_N_GO);
    } else if(!strcmp(name, "regular")) {
      gtk_notebook_set_current_page(s_notebook, PAGE_REGULAR);
    }
  }
}
//bridge for lobby.c
void tournament_on_tourney_toggled(GtkWidget *widget, gpointer user_data)
{
  on_tourney_toggled(widget, user_data);
}

static void	on_all_radio_clicked(GtkWidget* widget, gpointer data)
{
  (void) data;

  if(!s_disable_buttons && gtk_toggle_button_get_active(GTK_TOGGLE_BUTTON(widget))) {
    clear_stores();
    set_string("tournaments");
    set_string("refresh");
    set_string("all");
    flush_io_channel();
  }
}

static void	on_money_one_radio_clicked(GtkWidget* widget, gpointer data)
{
  (void) data;

  if(!s_disable_buttons && gtk_toggle_button_get_active(GTK_TOGGLE_BUTTON(widget))) {
    clear_stores();
    set_string("tournaments");
    set_string("refresh");
    set_string("money_one");
    flush_io_channel();
  }
}

static void	on_money_two_radio_clicked(GtkWidget* widget, gpointer data)
{
  (void) data;

  if(!s_disable_buttons && gtk_toggle_button_get_active(GTK_TOGGLE_BUTTON(widget))) {
    clear_stores();
    set_string("tournaments");
    set_string("refresh");
    set_string("money_two");
    flush_io_channel();
  }
}

static void on_cashier_button_pressed(GtkButton* button, gpointer data)
{
  (void) button;
  (void) data;

  set_string("tournaments");
  set_string("quit");
  set_string("cashier");
  flush_io_channel();
}

int	handle_tournaments(GladeXML* g_tournaments_xml, GladeXML* g_tournament_info_xml, GladeXML* g_lobby_tabs_xml, GladeXML* g_cashier_button_xml, GladeXML* g_clock_xml, GtkLayout* screen, int init)
{
  static int s_selected_tournament = 0;

  if(init) {

    textdomain ("poker2d");    

		s_screen = screen;

    s_tournaments_xml = g_tournaments_xml;
    s_tournaments_window = gui_get_widget(g_tournaments_xml, "tournaments_window");
    g_assert(s_tournaments_window);
    set_nil_draw_focus(s_tournaments_window);
    if(screen) gtk_layout_put(screen, s_tournaments_window, 0, 0);
    s_notebook = GTK_NOTEBOOK(gui_get_widget(g_tournaments_xml, "notebook"));
    g_assert(s_notebook);
    {
      s_sit_n_go_store = gtk_list_store_new(4, G_TYPE_INT, G_TYPE_STRING, G_TYPE_STRING, G_TYPE_STRING);
      GtkTreeView* treeview = GTK_TREE_VIEW(gui_get_widget(g_tournaments_xml, "sit_n_go_treeview"));
      GtkTreeSelection*	selection = gtk_tree_view_get_selection(treeview);
      g_signal_connect(selection, "changed", (GCallback)on_tournament_list_treeview_selection_changed, &s_selected_tournament);
      s_sit_n_go_selection = selection;
      g_signal_connect(treeview, "row-activated", (GCallback)on_row_activated, &s_selected_tournament);
      gtk_tree_view_set_rules_hint(treeview, TRUE);
      gtk_tree_view_set_model(treeview, GTK_TREE_MODEL(s_sit_n_go_store));
      GtkCellRenderer*	text_renderer = gtk_cell_renderer_text_new();

#define SIT_N_GO_ID 0
#define SIT_N_GO_TITLE 1
      {
        GtkTreeViewColumn* column = gtk_tree_view_column_new();
        gtk_tree_view_append_column(treeview, column);
        gtk_tree_view_column_set_title(column, gettext("Title") );
        gtk_tree_view_column_pack_start(column, text_renderer, TRUE);
        gtk_tree_view_column_add_attribute(column, text_renderer, "text", SIT_N_GO_TITLE);
      }
#define SIT_N_GO_STATE 2
      {
        GtkTreeViewColumn* column = gtk_tree_view_column_new();
        gtk_tree_view_append_column(treeview, column);
        gtk_tree_view_column_set_title(column, gettext("State") );
        gtk_tree_view_column_pack_start(column, text_renderer, TRUE);
        gtk_tree_view_column_add_attribute(column, text_renderer, "text", SIT_N_GO_STATE);
      }
#define SIT_N_GO_PLAYERS 3
      {
        GtkTreeViewColumn* column = gtk_tree_view_column_new();
        gtk_tree_view_append_column(treeview, column);
        gtk_tree_view_column_set_title(column, gettext("Players") );
        gtk_tree_view_column_pack_start(column, text_renderer, TRUE);
        gtk_tree_view_column_add_attribute(column, text_renderer, "text", SIT_N_GO_PLAYERS);
      }
    }
    {
      s_regular_store = gtk_list_store_new(5, G_TYPE_INT, G_TYPE_STRING, G_TYPE_STRING, G_TYPE_STRING, G_TYPE_STRING);
      GtkTreeView* treeview = GTK_TREE_VIEW(gui_get_widget(g_tournaments_xml, "regular_treeview"));
      GtkTreeSelection*	selection = gtk_tree_view_get_selection(treeview);
      g_signal_connect(selection, "changed", (GCallback)on_tournament_list_treeview_selection_changed, &s_selected_tournament);
      s_regular_selection = selection;
      g_signal_connect(treeview, "row-activated", (GCallback)on_row_activated, &s_selected_tournament);
      gtk_tree_view_set_rules_hint(treeview, TRUE);
      gtk_tree_view_set_model(treeview, GTK_TREE_MODEL(s_regular_store));
      GtkCellRenderer*	text_renderer = gtk_cell_renderer_text_new();

#define REGULAR_ID 0
#define REGULAR_DATE 1
      {
        GtkTreeViewColumn* column = gtk_tree_view_column_new();
        gtk_tree_view_append_column(treeview, column);
        gtk_tree_view_column_set_title(column, gettext("Date") );
        gtk_tree_view_column_pack_start(column, text_renderer, TRUE);
        gtk_tree_view_column_add_attribute(column, text_renderer, "text", REGULAR_DATE);
      }
#define REGULAR_TITLE 2
      {
        GtkTreeViewColumn* column = gtk_tree_view_column_new();
        gtk_tree_view_append_column(treeview, column);
        gtk_tree_view_column_set_title(column, gettext("Title") );
        gtk_tree_view_column_pack_start(column, text_renderer, TRUE);
        gtk_tree_view_column_add_attribute(column, text_renderer, "text", REGULAR_TITLE);
      }
#define REGULAR_STATE 3
      {
        GtkTreeViewColumn* column = gtk_tree_view_column_new();
        gtk_tree_view_append_column(treeview, column);
        gtk_tree_view_column_set_title(column, gettext("State") );
        gtk_tree_view_column_pack_start(column, text_renderer, TRUE);
        gtk_tree_view_column_add_attribute(column, text_renderer, "text", REGULAR_STATE);
      }
#define REGULAR_PLAYERS 4
      {
        GtkTreeViewColumn* column = gtk_tree_view_column_new();
        gtk_tree_view_append_column(treeview, column);
        gtk_tree_view_column_set_title(column, gettext("Players") );
        gtk_tree_view_column_pack_start(column, text_renderer, TRUE);
        gtk_tree_view_column_add_attribute(column, text_renderer, "text", REGULAR_PLAYERS);
      }
      gtk_tree_view_set_search_column(treeview, REGULAR_TITLE);
    }
    s_players_label = GTK_LABEL(gui_get_widget(g_tournaments_xml, "players_label"));
    s_tournaments_label = GTK_LABEL(gui_get_widget(g_tournaments_xml, "tournaments_label"));
    GUI_BRANCH(g_tournaments_xml, on_all_radio_clicked);
    GUI_BRANCH(g_tournaments_xml, on_money_one_radio_clicked);
    GUI_BRANCH(g_tournaments_xml, on_money_two_radio_clicked);

    s_tournament_info_window = gui_get_widget(g_tournament_info_xml, "tournament_info_window");
    g_assert(s_tournament_info_window);
    if(screen) gtk_layout_put(screen, s_tournament_info_window, 0, 0);
    {
      s_players_store = gtk_list_store_new(1, G_TYPE_STRING);
      GtkTreeView* treeview = GTK_TREE_VIEW(gui_get_widget(g_tournament_info_xml, "players_treeview"));
      gtk_tree_view_set_rules_hint(treeview, TRUE);
      gtk_tree_view_set_model(treeview, GTK_TREE_MODEL(s_players_store));
      GtkCellRenderer*	text_renderer = gtk_cell_renderer_text_new();

      {
        GtkTreeViewColumn* column = gtk_tree_view_column_new();
        gtk_tree_view_append_column(treeview, column);
        gtk_tree_view_column_set_title(column, gettext("Players") );
        gtk_tree_view_column_pack_start(column, text_renderer, TRUE);
        gtk_tree_view_column_add_attribute(column, text_renderer, "text", 0);
      }
    }

    s_register_unregister_label = GTK_LABEL(glade_xml_get_widget(g_tournament_info_xml, "label_register_unregister"));
    s_register_unregister_button = GTK_BUTTON(glade_xml_get_widget(g_tournament_info_xml, "button_register_unregister"));
    g_signal_connect(GTK_OBJECT(s_register_unregister_button), "clicked", (GtkSignalFunc)on_tournament_register_unregister_clicked, &s_selected_tournament);

    s_lobby_tabs_window = gui_get_widget(g_lobby_tabs_xml, "lobby_tabs_window");
    g_assert(s_lobby_tabs_window);
    if(!screen)
      gtk_window_set_title(s_lobby_tabs_window,"tournaments_lobby_tabs_window");
    if(screen) gtk_layout_put(screen, s_lobby_tabs_window, 0, 0);
    gtk_widget_set_size_request(s_lobby_tabs_window, gui_width(screen), -1);

    
    GUI_BRANCH(g_lobby_tabs_xml, on_table_toggled);
    GUI_BRANCH(g_lobby_tabs_xml, on_tourney_toggled);

    s_cashier_button_window = gui_get_widget(g_cashier_button_xml, "cashier_button_window");
    g_assert(s_cashier_button_window);
    if(!screen)
      gtk_window_set_title(s_cashier_button_window,"tournaments_cashier_button_window");
    if(screen) gtk_layout_put(screen, s_cashier_button_window, 0, 0);
    s_cashier_button = GTK_BUTTON(gui_get_widget(g_cashier_button_xml, "cashier_button"));
    g_assert(s_cashier_button);
    GUI_BRANCH(g_cashier_button_xml, on_cashier_button_pressed);

    close_tournaments();
  }

  char* tag = get_string();
  if(!strcmp(tag, "show")) {
    g_lobby_tab_state = tournament;
    /*
     * calculate windows position
     */
    int	screen_width = gui_width(screen);
    int	screen_height = gui_height(screen);

    int	top_left_x = (screen_width - 1000) / 2;
    int	top_left_y = (screen_height - 450) / 2;

    if (screen != NULL || s_tournaments_window_shown == 0)
      {

				{
					static position_t position;
					position.x = screen_width - 610;
					position.y = top_left_y;
					gui_place(s_tournaments_window, &position, screen);
				}

				{
					static position_t position;
					position.x = top_left_x;
					position.y = top_left_y;
					gui_place(s_tournament_info_window, &position, screen);
				}

				{
					static position_t position;
					position.x = 0;
					position.y = 33;
					gui_place(s_lobby_tabs_window, &position, screen);
				}

				{
					static position_t position;
					position.x = top_left_x;
					position.y = top_left_y + 435;
					gui_place(s_cashier_button_window, &position, screen);
				}
				s_tournaments_window_shown = 1;
		
			}
    {
      char* label = get_string();
      gtk_button_set_label(s_cashier_button, label);
      g_free(label);
    }

    s_selected_tournament = 0;

    {
      char* type = get_string();
      if(!strcmp(type, "sit_n_go")) {
        gtk_notebook_set_current_page(s_notebook, PAGE_SIT_N_GO);
      } else {
        gtk_notebook_set_current_page(s_notebook, PAGE_REGULAR);
      }
      GtkToggleButton* button = GTK_TOGGLE_BUTTON(gui_get_widget(g_lobby_tabs_xml, type));
      g_assert(button);
      gtk_toggle_button_set_active(button, TRUE);
      g_free(type);
    }

    {
      char* currency_serial = get_string();
      char* button;
      GtkWidget* radio;
      if(!strcmp(currency_serial, "money_two")) {
        button = "money_two_radio";
      } else if(!strcmp(currency_serial, "money_one")) {
        button = "money_one_radio";
      } else {
        button = "all_radio";
      }

      s_disable_buttons = 1;
      radio = gui_get_widget(s_tournaments_xml, button);
      g_assert(radio);
      gtk_toggle_button_set_active(GTK_TOGGLE_BUTTON(radio), TRUE);
      s_disable_buttons = 0;

      g_free(currency_serial);
    }

    {
      //moneyone
      GtkWidget* sl = gui_get_widget(g_tournaments_xml, "money_one_radio");
      char* label = get_string();
      gtk_button_set_label(GTK_BUTTON(sl), label);
      g_free(label);
    }

    {
      //moneytwo
      GtkWidget* sl = gui_get_widget(g_tournaments_xml, "money_two_radio");
      char* label = get_string();
      gtk_button_set_label(GTK_BUTTON(sl), label);
      g_free(label);
    }

  } else if(!strcmp(tag, "hide")) {
    g_lobby_tab_state = none;
    close_tournaments();

  } else if(!strcmp(tag, "info")) {
    char* players_count = get_string();
    char* tournaments_count = get_string();
    gtk_label_set_text(s_players_label, players_count);
    gtk_label_set_text(s_tournaments_label, tournaments_count);
    g_free(players_count);
    g_free(tournaments_count);

  } else if(!strcmp(tag, "sit_n_go")) {
    int selected = get_int();
    int rows = get_int();
    int i;

    gtk_list_store_clear(s_sit_n_go_store);
    for(i = 0; i < rows; i++) {
      int id = get_int();
      char* title = get_string();
      char* state = get_string();
      char* players = get_string();
      GtkTreeIter	iter;

      gtk_list_store_append(s_sit_n_go_store, &iter);
      gtk_list_store_set(s_sit_n_go_store, &iter, SIT_N_GO_ID, id, SIT_N_GO_TITLE, title, SIT_N_GO_STATE, state, SIT_N_GO_PLAYERS, players, -1);
      if(selected == id)
        gtk_tree_selection_select_iter(s_sit_n_go_selection, &iter);

      g_free(title);
      g_free(state);
      g_free(players);
    }
    s_selected_tournament = selected;
    gtk_list_store_clear(s_players_store);
    gtk_widget_set_sensitive(GTK_WIDGET(s_register_unregister_button), FALSE);

  } else if(!strcmp(tag, "regular")) {
    int selected = get_int();
    int rows = get_int();
    int i;

    gtk_list_store_clear(s_regular_store);
    for(i = 0; i < rows; i++) {
      int id = get_int();
      char* date = get_string();
      char* title = get_string();
      char* state = get_string();
      char* players = get_string();
      GtkTreeIter	iter;

      gtk_list_store_append(s_regular_store, &iter);
      gtk_list_store_set(s_regular_store, &iter, REGULAR_ID, id, REGULAR_DATE, date, REGULAR_TITLE, title, REGULAR_STATE, state, REGULAR_PLAYERS, players, -1);
      if(selected == id)
        gtk_tree_selection_select_iter(s_regular_selection, &iter);

      g_free(date);
      g_free(title);
      g_free(state);
      g_free(players);
    }
    s_selected_tournament = selected;
    gtk_list_store_clear(s_players_store);
    gtk_label_set_text(s_register_unregister_label, "");
    gtk_widget_set_sensitive(GTK_WIDGET(s_register_unregister_button), FALSE);

  } else if(!strcmp(tag, "players")) {
    can_register = get_int();
    char* label = "";
    if(can_register == 1)
      label = gettext("REGISTER");
    else if(can_register == 0)
      label = gettext("UNREGISTER");
    gtk_label_set_text(s_register_unregister_label, label);
    gtk_widget_set_sensitive(GTK_WIDGET(s_register_unregister_button), can_register != 2);
    {
      int players_count = get_int();
      int i;
      gtk_list_store_clear(s_players_store);
      for(i = 0; i < players_count; i++) {
        char* name = get_string();
        GtkTreeIter	iter;
        gtk_list_store_append(s_players_store, &iter);
        gtk_list_store_set(s_players_store, &iter, 0, name, -1);
        g_free(name);
      }
    }
  }

  g_free(tag);
  
  return TRUE;
}
