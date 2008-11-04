/*
*
* Copyright (C) 2006 Mekensleep
*
*	Mekensleep
*	24 rue vieille du temple
*	75004 Paris
* licensing@mekensleep.com
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
*  Jerome Jeannin <griim.work@gmail.com>
*
*/

#include "UnitTest++.h"
#include <iostream>
#include <gtk/gtk.h>
#include <glade/glade-build.h>

extern "C"
{
  void gui_set_glade_file(char* glade_file);  
  GladeXML* gui_load_widget(char* const);
}

TEST( Gui_loadWidget )
{
  gtk_init(NULL, NULL);

  static GladeXML* test_gladeXml = 0;
  char* glade_file = getenv("GLADE_FILE");
  gui_set_glade_file(glade_file);
  test_gladeXml = gui_load_widget("login_window");
  CHECK( 0 != test_gladeXml);
}
