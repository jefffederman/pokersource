/*
 *
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
 * Henry Precheur	<henry at precheur dot org>
 * Loic Dachary <loic@gnu.org>
 *
 */

#include <glib.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include "interface_io.h"

extern int	g_port_number;
GIOChannel*	g_channel;
GError	g_channel_error;
GError*	gp_channel_error = 0;

char	g_output_buffer[4096]; // FIXME
char*	g_output = g_output_buffer;

void	check_io_status(GIOStatus status)
{
  switch (status)
    {
    case G_IO_STATUS_ERROR:
      g_critical("IO error");
      exit(2);
      break;
    case G_IO_STATUS_EOF:
      g_critical("EOF, connection lost");
      exit(2);
      break;
    case G_IO_STATUS_AGAIN:
      g_critical("Resource temporarily unavailable");
      exit(2);
      break;
    case G_IO_STATUS_NORMAL:
      break;
    default:
      g_assert_not_reached();
    }
}

char*	get_string(void)
{
  char* result = 0;
  check_io_status(g_io_channel_read_line(g_channel,
					 &result,
					 0, 0,
					 &gp_channel_error));
  return result;
}

int	get_int(void)
{
  char*	str = get_string();
  int	i = atoi(str);
  g_free(str);
  return i;
}

void	set_string(const char* str)
{
  g_output += sprintf(g_output, "%s", str) + 1;
}

void	set_int(int i)
{
  g_output += sprintf(g_output, "%d", i) + 1;
}

void	flush_io_channel(void)
{
  gsize	write_size;
  check_io_status(g_io_channel_write_chars(g_channel,
					   g_output_buffer,
					   g_output - g_output_buffer,
					   &write_size,
					   &gp_channel_error));
  check_io_status(g_io_channel_flush(g_channel, &gp_channel_error));
  g_output = g_output_buffer;
}

gboolean	handle_network(GIOChannel *source,
			       GIOCondition condition,
			       gpointer data);

int	init_interface_io(const char* address)
{
  struct sockaddr_in my_addr;
  int	fd = socket(AF_INET, SOCK_STREAM, 0);
  
  my_addr.sin_family = AF_INET;
  my_addr.sin_port = htons(g_port_number);
  my_addr.sin_addr.s_addr = inet_addr(address);
  memset(&(my_addr.sin_zero), 0, 8);

  int on = 1;
  if (setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &on, sizeof(on)) == -1)
    {
      g_critical("unable to setsocketport TCP_NODELAY");
      return FALSE;
    }

  if (connect(fd,
	      (struct sockaddr*)&my_addr,
	      sizeof(struct sockaddr)) == -1)
    {
      g_critical("unable to connect to %s", address);
      return FALSE;
    }

  g_channel = g_io_channel_unix_new(fd);
  g_io_channel_set_encoding(g_channel, 0, 0);
  g_io_channel_set_line_term(g_channel, "\0", 1);
  g_io_add_watch(g_channel, G_IO_IN, handle_network, 0);
  g_io_add_watch(g_channel, G_IO_HUP, handle_network, 0);
  g_io_add_watch(g_channel, G_IO_ERR, handle_network, 0);
  return TRUE;
}
