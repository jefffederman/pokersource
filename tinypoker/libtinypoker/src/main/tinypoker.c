/*
 * Copyright (C) 2007 Thomas Cort <code@member.fsf.org>
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

#include <ctype.h>
#include <regex.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glib.h>
#include <gnet.h>

#include "tinypoker.h"

/**
 * Convert the string to upper case.
 * Convert multiple spaces to 1 space.
 * Trim leading and trailing white space.
 * Should be called before ipp_validate_msg()
 * @param msg the message, a null terminated string, to transform.
 */
void ipp_normalize_msg(gchar *msg) {
	gint len, i, j;
	len = strlen(msg);
	gchar *pos;

	if (!msg || strlen(msg) < MIN_MSG_SIZE) {
		return;
	}

	while ((pos = strchr(msg, '\n'))) {
		*pos = ' '; /* trim all new lines */
	}

	j = 0; /* Trim leading white space */
	while ((msg[j] == ' ' || msg[j] == '\t') && (j < len)) {
		j++;
	}

	/* Trim whitespace as we go. Convert everything to upper case. */
	for (i = 0; j < len && i < len; i++, j++) {
		msg[i] = toupper(msg[j]);
		if ((msg[i] == ' ' || msg[i] == '\t') && (msg[j+1] == ' ' || msg[j+1] == '\t')) {
			i--;
		}
	}

	/* Trim that last whitespace character not caught by the 'for' loop */
	if (i > 0 && (msg[i-1] == ' ' || msg[i-1] == '\t')) {
		i--;
	}

	msg[i] = '\0';
}


/**
 * Validates IPP Messages
 * @param regex one of the REGEX constants.
 * @param msg a message.
 * @return 1 if msg is valid, 0 if msg is not valid.
 */
gboolean ipp_validate_msg(gchar *regex, gchar *msg) {
	regex_t preg;
	int ret;

	if (!regex || !msg) {
		return FALSE;
	}

	ret = regcomp(&preg, regex, REG_EXTENDED);
	if (ret) { /* compile the pattern */
		return FALSE;
	}

	/* See if the message matches */
	ret = regexec(&preg, msg, 0, 0, 0);
	regfree(&preg); /* Clean up */

	if (!ret) {
		return TRUE;
	} else {
		return FALSE;
	}
}

/**
 * Validates an arbitrary IPP Messages.
 * @param msg a message.
 * @return 1 if msg is valid, 0 if msg is not valid.
 */
gboolean ipp_validate_unknown_msg(gchar *msg) {
	guint i ;
	gboolean is_valid = FALSE;

	char *regex[] = {
		REGEX_MSG_IPP,
		REGEX_MSG_BUYIN,
		REGEX_MSG_WELCOME,
		NULL
	};

	if (!regex || !msg) {
		return FALSE;
	}

	for (i = 0; regex[i]; i++) {
		if (ipp_validate_msg(regex[i], msg)) {
			is_valid = TRUE;
			break;
		}
	}

	return is_valid;
}

/**
 * Initializes gnet. This function *must* be called before performing any network operations!
 */
void ipp_init() {
	gnet_init();
}

/**
 * Connect to a server.
 * @param hostname the hostname of the server to connect to (example: host.domain.tld).
 * @param port the port number (example: 9999).
 * @return a socket or NULL if an error happened.
 */
GTcpSocket* ipp_connect(gchar* hostname, gint port) {
	GInetAddr* addr;
	GTcpSocket* socket;

	if (!hostname || (port < 1 || port > 65535)) {
		return FALSE;
	}

	addr = gnet_inetaddr_new (hostname, port);
	if (!addr) {
		return NULL; /* cannot resolve host name */
	}

	socket = gnet_tcp_socket_new (addr);
	gnet_inetaddr_delete(addr);

	return socket;
}

/**
 * Disconnect from the server.
 */
void ipp_disconnect(GTcpSocket *socket) {
	if (socket) {
		gnet_tcp_socket_delete(socket);
	}
	socket = NULL;
}

/**
 * INTERNAL FUNCTION. DO NOT USE OUTSIDE LIBTINYPOKER!!!
 * @param void_params a __ipp_readln_thread_params structure.
 */
void __ipp_readln_thread(void *void_params) {
	GIOError err;
	__ipp_readln_thread_params *params;
	params = (__ipp_readln_thread_params *) void_params;

	err = gnet_io_channel_readline_strdup(params->chan, params->buffer, params->n);
	if (err != G_IO_ERROR_NONE) {
		pthread_exit(0);
	}

	pthread_exit(0);
}

/**
 * Read a message from the socket.
 * @param socket the socket to read from.
 * @param timeout number of seconds to wait for input.
 * @return a valid normalized message or NULL if message is invalid. All messages need to be deallocate by the user with g_free().
 */
gchar* ipp_read_msg(GTcpSocket *socket, gdouble timeout) {
	gint ret;
	GTimer* clock;
	gchar *buffer;
	GIOChannel *chan;
	gsize n = 0;
	gboolean is_valid;
	pthread_t reader;
	pthread_attr_t reader_attr;
	__ipp_readln_thread_params params;

	chan = gnet_tcp_socket_get_io_channel(socket);
	if (!chan) {
		return NULL;
	}

	params.chan = chan;
	params.buffer = &buffer;
	params.n = &n;

	pthread_attr_init(&reader_attr);
	pthread_attr_setdetachstate(&reader_attr, PTHREAD_CREATE_DETACHED);
	ret = pthread_create(&reader, &reader_attr, (void* (*) (void*)) __ipp_readln_thread, (void*) &params);
	if (ret != 0) {
		pthread_attr_destroy(&reader_attr);
		return NULL;
	}

	clock = g_timer_new();
	do {
		if (g_timer_elapsed(clock, NULL) > timeout) {
			break;
		}
		pthread_yield();
	} while (!n);
	g_timer_stop(clock);
	g_timer_destroy(clock);
	clock = NULL;

	pthread_cancel(reader);
	pthread_attr_destroy(&reader_attr);

	buffer = *(params.buffer);

	if (!n) {
		return NULL;
	}

	ipp_normalize_msg(buffer);

	is_valid = ipp_validate_unknown_msg(buffer);
	if (is_valid) {
		return buffer;
	} else {
		g_free(buffer);
		return NULL;
	}
}

/**
 * Send a message to the socket. It will be normalized and validated by this function before sending.
 * @param socket the socket to read from.
 * @param msg the message to send.
 * @return TRUE if msg was sent OK, else FALSE for error.
 */
gboolean ipp_send_msg(GTcpSocket *socket, gchar *msg) {
	GIOChannel *chan;
	GIOError err;
	gboolean is_valid;
	gsize n;

	ipp_normalize_msg(msg);
	is_valid = ipp_validate_unknown_msg(msg);

	if (is_valid) {
		gchar *final_msg;

		final_msg = g_strndup(msg, strlen(msg) + 1);
		final_msg[strlen(msg)] = '\n';

		chan = gnet_tcp_socket_get_io_channel(socket);
		if (!chan) {
			g_free(final_msg);
			final_msg = NULL;
			return FALSE;
		}

		err = gnet_io_channel_writen(chan, final_msg, strlen(final_msg), &n);
		if (err != G_IO_ERROR_NONE) {
			g_free(final_msg);
			final_msg = NULL;
			return FALSE;
		}
		
		if (n == strlen(final_msg)) {
			g_free(final_msg);
			final_msg = NULL;
			return TRUE;
		} else {
			g_free(final_msg);
			final_msg = NULL;
			return FALSE;
		}
	} else {
		return FALSE;
	}
}
