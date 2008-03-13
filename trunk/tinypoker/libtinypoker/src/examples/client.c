/*
 * Copyright (C) 2005, 2006, 2007, 2008 Thomas Cort <tom@tomcort.com>
 *
 * This file is part of libtinypoker.
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
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include "../main/tinypoker.h"
#include <string.h>

int main(int argc, char **argv, char **envp)
{
	ipp_socket *sock;
	int rc;
	ipp_message *msg;
	ipp_init();

	sock = ipp_connect("localhost", 9898, "ca.pem");
	if (!sock) {
		printf("! connect failed\n");
		ipp_exit();
		return 1;
	}

	msg = ipp_read_msg(sock, CLIENT_READ_TIMEOUT);
	if (msg && msg->payload && msg->type == MSG_IPP) {
		printf("> %s\n", msg->payload);
		ipp_free_message(msg);
		msg = NULL;
	} else {
		printf("! read error\n");
		ipp_disconnect(sock);
		ipp_free_socket(sock);
		sock = NULL;
		ipp_free_message(msg);
		msg = NULL;
		ipp_exit();
		return 1;
	}

	msg = ipp_new_message();
	if (!msg) {
		printf("! malloc failed\n");
		ipp_disconnect(sock);
		ipp_free_socket(sock);
		sock = NULL;
		return 1;
	}

	msg->type = MSG_BUYIN;
	msg->payload = strdup("BUYIN TOM 500");
	rc = ipp_send_msg(sock, msg, CLIENT_WRITE_TIMEOUT);
	if (rc) {
		printf("< %s\n", msg->payload);
		ipp_free_message(msg);
		msg = NULL;
	} else {
		printf("! send error\n");
		ipp_free_message(msg);
		ipp_disconnect(sock);
		ipp_free_socket(sock);
		sock = NULL;
		ipp_free_message(msg);
		msg = NULL;
		ipp_exit();
		return 1;
	}

	msg = ipp_read_msg(sock, CLIENT_READ_TIMEOUT);
	if (msg && msg->payload && msg->type == MSG_WELCOME) {
		printf("> %s\n", msg->payload);
		ipp_free_message(msg);
		msg = NULL;
	} else {
		printf("! read error\n");
		ipp_disconnect(sock);
		ipp_free_socket(sock);
		sock = NULL;
		ipp_free_message(msg);
		msg = NULL;
		ipp_exit();
		return 1;
	}

	ipp_disconnect(sock);
	ipp_free_socket(sock);
	sock = NULL;
	ipp_exit();

	return 0;
}
