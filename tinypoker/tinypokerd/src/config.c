/*
 * Copyright (C) 2005, 2006, 2007, 2008 Thomas Cort <tom@tomcort.com>
 *
 * This file is part of tinypokerd.
 *
 * tinypokerd is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * tinypokerd is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with tinypokerd.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <confuse.h>
#include <libdaemon/dlog.h>
#include <tinypoker.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <strings.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#include "config.h"

/**
 * Checks if the configuration file exists as a regular file.
 * @return Returns 1 if the file exists and is regular, else 0.
 */
static int config_file_exists()
{
	struct stat s;

	/* No config file defined - NULL Pointer Check */
	if (!DEFAULT_CONFIGFILE) {
		return 0;
	}

	/* File exists? */
	if (stat(DEFAULT_CONFIGFILE, &s) < 0) {
		return 0;
	}

	/* File is a regular file? */
	if (!S_ISREG(s.st_mode)) {
		return 0;
	}

	return 1;
}

/**
 * Release any resources that hold configuration information.
 * This function effectively resets all configurable values.
 * It should be called at the end of the program.
 */
void config_free()
{
	port = 0;

	if (database) {
		free(database);
		database = NULL;
	}
}

/**
 * Examines each value of the current configuration.
 * If a value was not set, it is set to the default.
 */
static void config_with_defaults()
{
	if (port == 0) {
		port = IPP_SERVER_PORT_TLS;
	}

	if (database == NULL) {
		database = strdup(DEFAULT_DATABASE);
	}
}

/**
 * Parses an tinypokerd.conf configuration file.
 */
void config_parse()
{
	int rc;

	config_free();

	cfg_t *cfg;
	cfg_opt_t opts[] = {
		CFG_SIMPLE_INT("port", &port),
		CFG_SIMPLE_INT("database", &database),
		CFG_END()
	};

	cfg = NULL;

	if (!config_file_exists()) {
		daemon_log(LOG_INFO, "[CONF] Configuration file '%s' not found. Loading defaults...", DEFAULT_CONFIGFILE);
		config_with_defaults();
		return;
	}

	cfg = cfg_init(opts, 0);
	if (!cfg) {
		daemon_log(LOG_ERR, "[CONF] cfg_init failed! Loading defaults...");
		config_with_defaults();
		return;
	}

	rc = cfg_parse(cfg, DEFAULT_CONFIGFILE);
	if (rc == CFG_PARSE_ERROR) {
		daemon_log(LOG_ERR, "[CONF] parser error '%s'", DEFAULT_CONFIGFILE);
	}

	if (cfg) {
		cfg_free(cfg);
		cfg = NULL;
	}

	config_with_defaults();
}
