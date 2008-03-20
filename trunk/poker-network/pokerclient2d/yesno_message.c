/* *
 * Copyright (C) 2004, 2005, 2006 Mekensleep
 *
 *	Mekensleep
 *	24 rue vieille du temple
 *	75004 Paris
 *       licensing@mekensleep.com
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
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
 *  Henry Pr�cheur <henry@precheur.org>
 *
 */

#include <gtk/gtk.h>
#include <glade/glade.h>
#include "gui.h"
#include "interface_io.h"
#include "dispatcher.h"

static GtkWidget*	g_yesno_window;
static GtkWidget*	g_yesno_message;
static gboolean	g_yesno_window_shown = 0;
static GtkLayout*	g_screen = 0;

void	on_yesno_no_button_clicked(GtkWidget *widget, gpointer user_data)
{
  (void) widget;
  (void) user_data;

  g_message("no");
  set_string("yesno");
  set_string("no");
  flush_io_channel();
	if (g_screen)
		gtk_widget_hide_all(g_yesno_window);
}

void	on_yesno_yes_button_clicked(GtkWidget *widget, gpointer user_data)
{
  (void) widget;
  (void) user_data;

  g_message("yes");
  set_string("yesno");
  set_string("yes");
  flush_io_channel();
	if (g_screen)
		gtk_widget_hide_all(g_yesno_window);
}

int	handle_yesno(GladeXML* g_glade_xml, GtkLayout* screen, int init)
{
  if (init)
    {
			g_screen = screen;
      g_yesno_window = glade_xml_get_widget(g_glade_xml,
					    "yesno_window");
      g_assert(g_yesno_window);
      set_nil_draw_focus(g_yesno_window);
      if(screen) gtk_layout_put(screen, g_yesno_window, 0, 0);
      g_yesno_message = glade_xml_get_widget(g_glade_xml,
					     "yesno_message");
      g_assert(g_yesno_message);
      GUI_BRANCH(g_glade_xml, on_yesno_no_button_clicked);
      GUI_BRANCH(g_glade_xml, on_yesno_yes_button_clicked);
    }

  char*	message = get_string();
  gtk_label_set_text(GTK_LABEL(g_yesno_message), message);
  g_free(message);

	if (screen != NULL || !g_yesno_window_shown)
		{
			gui_center(g_yesno_window, screen);
			g_yesno_window_shown = 1;
		}
  return TRUE;
}
