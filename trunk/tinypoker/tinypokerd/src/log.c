/*
 * Copyright (C) 2005, 2006, 2007, 2008 Thomas Cort <linuxgeek@gmail.com>
 * 
 * This file is part of tinypokerd.
 * 
 * tinypokerd is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option)
 * any later version.
 * 
 * tinypokerd is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 * 
 * You should have received a copy of the GNU General Public License along with
 * tinypokerd.  If not, see <http://www.gnu.org/licenses/>.
 */

#define _XOPEN_SOURCE 500

#include <pthread.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <libxml/xmlwriter.h>

#include "tinypokerd.h"
#include "config.h"
#include "log.h"

/**
 * A lock used to serialize access to writer.
 */
pthread_mutex_t writer_lock;

static xmlTextWriterPtr writer = NULL;

char *protocol_logger_timestamp()
{
	struct tm *tm;
	time_t t;
	size_t len;
	char *s;

	len = sizeof(char) * 32;

	t = time(NULL);
	tm = gmtime(&t);

	s = (char *) malloc(len);
	if (!s) {
		return NULL;
	}
	memset(s, '\0', len);

	strftime(s, 32, ISO8601_FORMAT, tm);
	return s;
}

void protocol_logger_init()
{
	int rc = 0;
	char *timestamp = NULL;

	if (protocol_log_enabled == cfg_false) {
		return;
	}

	if (writer) {
		protocol_logger_exit();
	}

	pthread_mutex_init(&writer_lock, 0);

	writer = xmlNewTextWriterFilename(protocol_log_file, 0);
	if (!writer) {
		return;
	}

	rc = xmlTextWriterSetIndent(writer, 2);
	if (rc < 0) {
		protocol_logger_exit();
		return;
	}

	rc = xmlTextWriterStartDocument(writer, NULL, NULL, NULL);
	if (rc < 0) {
		protocol_logger_exit();
		return;
	}

	rc = xmlTextWriterWriteFormatComment(writer, " Generated by %s %s ", TINYPOKERD_NAME, TINYPOKERD_VERSION);
	if (rc < 0) {
		protocol_logger_exit();
		return;
	}

	rc = xmlTextWriterStartElement(writer, BAD_CAST "Log");
	if (rc < 0) {
		protocol_logger_exit();
		return;
	}

	timestamp = protocol_logger_timestamp();
	if (!timestamp) {
		protocol_logger_exit();
		return;
	}

	rc = xmlTextWriterWriteAttribute(writer, BAD_CAST "timestamp", BAD_CAST timestamp);
	if (rc < 0) {
		free(timestamp);
		timestamp = NULL;
		protocol_logger_exit();
		return;
	}

	free(timestamp);
	timestamp = NULL;
}

/**
 * Logs internet poker protocol messages.
 * @param msg the message to log.
 */
void protocol_logger(char *msg)
{
	int rc;
	char *timestamp;
	static unsigned long long id = 0LL;

	if (protocol_log_enabled == cfg_false) {
		return;
	}

	if (!writer) {
		protocol_logger_init();
		if (!writer) {
			return;
		}
	}

	if (msg && msg[0]) {
		pthread_mutex_lock(&writer_lock);

		rc = xmlTextWriterStartElement(writer, BAD_CAST "Entry");
		if (rc < 0) {
			pthread_mutex_unlock(&writer_lock);
			protocol_logger_exit();
			return;
		}

		rc = xmlTextWriterWriteFormatAttribute(writer, BAD_CAST "id", "%llu", id++);
		if (rc < 0) {
			pthread_mutex_unlock(&writer_lock);
			protocol_logger_exit();
			return;
		}

		timestamp = protocol_logger_timestamp();
		if (!timestamp) {
			pthread_mutex_unlock(&writer_lock);
			protocol_logger_exit();
			return;
		}

		rc = xmlTextWriterWriteAttribute(writer, BAD_CAST "timestamp", BAD_CAST timestamp);
		if (rc < 0) {
			pthread_mutex_unlock(&writer_lock);
			free(timestamp);
			timestamp = NULL;
			protocol_logger_exit();
			return;
		}

		free(timestamp);
		timestamp = NULL;

		rc = xmlTextWriterWriteFormatElement(writer, BAD_CAST "message", "%s", msg);
		if (rc < 0) {
			pthread_mutex_unlock(&writer_lock);
			protocol_logger_exit();
			return;
		}

		rc = xmlTextWriterEndElement(writer);
		if (rc < 0) {
			pthread_mutex_unlock(&writer_lock);
			protocol_logger_exit();
			return;
		}

		pthread_mutex_unlock(&writer_lock);
	}
}

void protocol_logger_exit()
{
	int rc;

	if (protocol_log_enabled == cfg_false) {
		return;
	}

	pthread_mutex_destroy(&writer_lock);

	if (!writer) {
		return;
	}

	rc = xmlTextWriterEndElement(writer);
	if (rc < 0) {
		xmlFreeTextWriter(writer);
		writer = NULL;
		return;
	}

	rc = xmlTextWriterEndDocument(writer);
	if (rc < 0) {
		xmlFreeTextWriter(writer);
		writer = NULL;
		return;
	}

	xmlFreeTextWriter(writer);
	writer = NULL;
	return;

}
