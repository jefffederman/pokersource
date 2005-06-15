/* *
 * Copyright (C) 2004, 2005 Mekensleep
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
 *  Henry Pr�cheur <henry at precheur dot org>
 *  Loic Dachary <loic@gnu.org>
 *
 */
#include <string.h>
#include <gtk/gtk.h>
#include <glade/glade.h>
#include "gui.h"
#ifndef	GLADE_FILE
#	define	GLADE_FILE "bad glade file"
#endif // GLADE_FILE

static char* s_glade_file = 0;

void gui_set_glade_file(char* glade_file) {
  if(s_glade_file) g_free(s_glade_file);
  s_glade_file = NULL;
  if(glade_file) s_glade_file = g_strdup(glade_file);
}

GladeXML*	gui_load_widget(const char* widget_name)
{
  char*	filename = GLADE_FILE;

  if (s_glade_file && g_file_test(s_glade_file, G_FILE_TEST_EXISTS))
    filename = s_glade_file;
  else if (g_file_test("interface.glade", G_FILE_TEST_EXISTS))
    filename = "interface.glade";
  else if (g_file_test("../../poker3d-interface/interface.glade", G_FILE_TEST_EXISTS))
    filename = "../../poker3d-interface/interface.glade";
  g_message("reading glade file %s", filename);
  GladeXML*	xml = glade_xml_new(filename, widget_name, NULL);
  if (!xml)
    {
      g_critical("unable to load glade file %s", filename);
      return NULL;
    }
  return xml;
}

GtkWidget*	gui_get_widget(GladeXML* self, const char* widget_name)
{
  GtkWidget*	widget = glade_xml_get_widget(self,
					      widget_name);
  if (!widget)
    g_error("unable to load %s from glade xml", widget_name);
  return widget;
}

static void gui_get_screen_size(GtkLayout* screen, gint* width, gint* height) {
  if(screen == NULL) {
    *width = gdk_screen_width();
    *height = gdk_screen_height();
  } else {
    gtk_layout_get_size(screen, width, height);
  }
}

static void gui_get_widget_size(GtkWidget* window, gint* width, gint* height) {
  if(GTK_IS_WINDOW(window)) {
    gtk_window_get_size(GTK_WINDOW(window), width, height);
  } else {
    GtkRequisition requisition;
    gtk_widget_size_request(window, &requisition);
    *width = requisition.width;
    *height = requisition.height;
  }
}

static void gui_move(GtkWidget* window, GtkLayout* screen, gint x, gint y) {
  if(GTK_IS_WINDOW(window)) {
    gtk_window_move(GTK_WINDOW(window), x, y);
  } else {
    if(gtk_widget_get_parent(window) != GTK_WIDGET(screen)) 
      //gtk_layout_put(screen, window, x, y);
      g_assert(0 && "gui_move not a child");
    else {
      GValue value_x;
      GValue value_y;
      memset(&value_x, 0, sizeof(GValue));
      memset(&value_y, 0, sizeof(GValue));
      g_value_init(&value_x, G_TYPE_INT);
      g_value_init(&value_y, G_TYPE_INT);
      gtk_container_child_get_property(GTK_CONTAINER(screen), window, "x", &value_x);
      gtk_container_child_get_property(GTK_CONTAINER(screen), window, "y", &value_y);
      if(x != g_value_get_int (&value_x) || y != g_value_get_int(&value_y))
        gtk_layout_move(screen, window, x, y);
    }
  }
}

// g_message("gui_"#NAME"_move %dx%d window to x=%d y=%d (screen %dx%d)", window_width, window_height, x, y, screen_width, screen_height);

#define GUI_FUNCTION_MOVE(NAME, X, Y) \
static void	gui_##NAME##_move(GtkWidget* window, GtkLayout* screen, int window_width, int window_height) \
{ \
  gint screen_width; \
  gint screen_height; \
  gui_get_screen_size(screen, &screen_width, &screen_height); \
 \
  if(window_width < 0 || window_height < 0) \
    gui_get_widget_size(window, &window_width, &window_height); \
 \
  gint x = (X); \
  gint y = (Y); \
\
  gui_move(window, screen, x, y); \
} \
 \
static void	gui_##NAME##_show_callback(GtkWidget*	widget, \
                                     gpointer	user_data) \
{ \
  gui_##NAME##_move(widget, GTK_LAYOUT(user_data), -1, -1); \
} \
 \
static void	gui_##NAME##_size_callback(GtkWidget*	widget, \
                                     GtkAllocation*	allocation, \
                                     gpointer	user_data) \
{ \
  gui_##NAME##_move(widget, GTK_LAYOUT(user_data), allocation->width, allocation->height); \
} \
\
void	gui_##NAME(GtkWidget* window, GtkLayout* screen) \
{ \
  g_signal_connect(G_OBJECT(window), "show", \
                   G_CALLBACK(gui_##NAME##_show_callback), screen); \
  g_signal_connect(G_OBJECT(window), "size-allocate", \
                   G_CALLBACK(gui_##NAME##_size_callback), \
                   screen); \
  gtk_widget_show_all(window); \
  gui_##NAME##_move(window, screen, -1, -1); \
}

GUI_FUNCTION_MOVE(center, ((screen_width - window_width) / 2), ((screen_height - window_height) / 2));
GUI_FUNCTION_MOVE(top_right, (screen_width - window_width), 0);
GUI_FUNCTION_MOVE(top_left, 0, 0);
GUI_FUNCTION_MOVE(bottom_left, 0, (screen_height - window_height));
GUI_FUNCTION_MOVE(bottom_right, (screen_width - window_width), (screen_height - window_height));

static void	gui_place_show_callback(GtkWidget*	widget,
                                     gpointer	user_data)
{
  position_t* position = (position_t*)user_data;
  gui_move(widget, position->screen, position->x, position->y);
}

static void	gui_place_size_callback(GtkWidget*	widget,
                                     GtkAllocation*	allocation,
                                     gpointer	user_data)
{
  (void)allocation;
  position_t* position = (position_t*)user_data;
  gui_move(widget, position->screen, position->x, position->y);
}

void	gui_place(GtkWidget* window, position_t* position, GtkLayout* screen)
{
  g_signal_connect(G_OBJECT(window), "show",
                   G_CALLBACK(gui_place_show_callback), position);
  g_signal_connect(G_OBJECT(window), "size-allocate",
                   G_CALLBACK(gui_place_size_callback),
                   position);
  position->screen = screen;
  gtk_widget_show_all(window);
  gui_move(window, screen, position->x, position->y);
}

static void nil_draw_focus(GtkStyle        *style,
                           GdkWindow       *window,
                           GtkStateType    state_type,
                           GdkRectangle    *area,
                           GtkWidget       *widget,
                           const gchar     *detail,
                           gint            x,
                           gint            y,
                           gint            width,
                           gint            height)
{}

void set_nil_draw_focus(GtkWidget* widget) {
  GtkStyle* style = gtk_widget_get_style(widget);
  g_assert(style);
  GTK_STYLE_GET_CLASS(style)->draw_focus = nil_draw_focus;
}

int gui_width(GtkLayout* screen) {
  if(screen) {
    gint width;
    gint height;
    gtk_layout_get_size(screen, &width, &height);
    return width;
  } else {
    return gdk_screen_width();
  }
}

int gui_height(GtkLayout* screen) {
  if(screen) {
    gint width;
    gint height;
    gtk_layout_get_size(screen, &width, &height);
    return height;
  } else {
    return gdk_screen_height();
  }
}
