/* *
 * Copyright (C) 2004, 2005, 2006 Mekensleep <licensing@mekensleep.com>
 *                                24 rue vieille du temple, 75004 Paris
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
 *  Henry Pr�cheur <henry at precheur dot org>
 *  Loic Dachary <loic@gnu.org>
 *
 */

#include <gtk/gtk.h>
#include <glade/glade.h>
#include "gui.h"
#include "interface_io.h"
#include "dispatcher.h"

static GtkWidget*	g_chooser_window;
static GtkWidget*	g_chooser_label;
static GtkWidget*	g_chooser_vbox;
static GtkWidget*	g_chooser_combobox = 0;
static gboolean	g_chooser_window_shown = 0;
static GtkLayout* g_screen = 0;

void	on_chooser_button_clicked(GtkWidget* widget, gpointer user_data)
{
  (void) widget;
  (void) user_data;

  GtkTreeModel*	model;
  GtkTreeIter	iter;
  char*	str;

  gtk_combo_box_get_active_iter(GTK_COMBO_BOX(g_chooser_combobox), &iter);
  g_object_get(G_OBJECT(g_chooser_combobox), "model", &model, NULL);
  gtk_tree_model_get(model, &iter, 0, &str, -1);
  g_message("%s selected", str);
  set_string("chooser");
  set_string(str);
  flush_io_channel();
	if (g_screen)
		gtk_widget_hide_all(g_chooser_window);
}

int	handle_chooser(GladeXML* g_glade_xml, GtkLayout* screen, int init)
{
  if (init)
    {
      if (!g_glade_xml)
        return FALSE;
      g_chooser_window = glade_xml_get_widget(g_glade_xml,
					      "chooser_window");
      g_assert(g_chooser_window);
      set_nil_draw_focus(g_chooser_window);
      if(screen) gtk_layout_put(screen, g_chooser_window, 0, 0);
      g_chooser_label = glade_xml_get_widget(g_glade_xml,
					     "chooser_label");
      g_assert(g_chooser_label);
      g_chooser_vbox = glade_xml_get_widget(g_glade_xml,
					    "chooser_vbox");
      g_assert(g_chooser_vbox);
      GUI_BRANCH(g_glade_xml, on_chooser_button_clicked);
      /* setup combo box entry */
      g_chooser_combobox = gtk_combo_box_new_text();
      gtk_widget_show(g_chooser_combobox);
      gtk_box_pack_end_defaults(GTK_BOX(g_chooser_vbox), g_chooser_combobox);
    }

  char*	label = get_string();
  gtk_label_set_text(GTK_LABEL(g_chooser_label), label);
  g_free(label);

  /* remove text already in the combobox */
  {
    GtkTreeModel*	tree_model =
      gtk_combo_box_get_model(GTK_COMBO_BOX(g_chooser_combobox));
    GtkListStore*	store;

    g_assert(GTK_IS_LIST_STORE(tree_model));

    store = GTK_LIST_STORE(tree_model);
    gtk_list_store_clear(store);
  }

  int	choices_count = get_int();
  while (choices_count--)
    {
      char*	text = get_string();
      gtk_combo_box_append_text(GTK_COMBO_BOX(g_chooser_combobox), text);
      g_free(text);
    }
  gtk_combo_box_set_active(GTK_COMBO_BOX(g_chooser_combobox), 0);

	if (screen != NULL || !g_chooser_window_shown) 
		{
			gui_center(g_chooser_window, screen);
			g_chooser_window_shown = 1;
		}

  return TRUE;
}
