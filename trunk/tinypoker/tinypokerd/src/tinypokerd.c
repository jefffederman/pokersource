/*
 * Copyright (C) 2005, 2006, 2007, 2008 Thomas Cort <tom@tomcort.com>
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

#define _GNU_SOURCE

#include <errno.h>
#include <getopt.h>
#include <libdaemon/dlog.h>
#include <libdaemon/dpid.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <fcntl.h>
#include <pwd.h>
#include <grp.h>

#include <unistd.h>

#include "config.h"
#include "monitor.h"
#include "pokerserv.h"
#include "signal.h"
#include "tinypokerd.h"

/**
 * Determines if gatewayavd should run in the background (daemonized) or
 * not. If daemonize is 1, then gatewayavd should run in the background.
 */
int daemonize;

/**
 * Determines if our process killed a running tinypokerd process successfully.
 */
int killed;

/**
 * Displays some version and copyright information upon request (-v or --version).
 */
void display_version(void)
{
	daemon_log(LOG_INFO, "%s/%s", TINYPOKERD_NAME, TINYPOKERD_VERSION);
	daemon_log(LOG_INFO, "Copyright (C) 2005, 2006, 2007, 2008 Thomas Cort <tom@tomcort.com>");
	daemon_log(LOG_INFO, "This is free software; see the source for copying conditions.  There is NO");
	daemon_log(LOG_INFO, "warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.");
}


/**
 * Displays some usage information, command line parameters and whatnot.
 * @param program the name of the program.
 */
void display_help(char *program)
{
	daemon_log(LOG_INFO, "Usage: %s [options]", program);
	daemon_log(LOG_INFO, "Options:");
	daemon_log(LOG_INFO, "    -h --help          Show this help message");
	daemon_log(LOG_INFO, "    -v --version       Show version information");
	daemon_log(LOG_INFO, "    -k --kill          Kill the running instance");
	daemon_log(LOG_INFO, "    -f --foreground    Run in the foreground");
	daemon_log(LOG_INFO, "    -c --config=file   Use an alternate config");
}

/**
 * A command line parser using getopts.
 * @param argc The number of command line arguments coming in argv.
 * @param argv The command line arguments.
 * @return Returns 0 on success and non-zero when we want the program to terminate.
 */
int parse_args(int argc, char **argv)
{
	int option_index;
	int done;

	static struct option long_options[] = {
		{"help", no_argument, NULL, 'h'},
		{"version", no_argument, NULL, 'v'},
		{"kill", no_argument, NULL, 'k'},
		{"foreground", no_argument, NULL, 'f'},
		{"config", required_argument, NULL, 'c'},
		{0, 0, 0, 0}
	};

	option_index = 0;
	done = 0;

	while (!done) {
		int c;
		int ret;

		c = getopt_long(argc, argv, "hvkfc:", long_options, &option_index);
		if (c < 0) {
			break;
		}
		switch (c) {
		case 'h':
			display_help(argv[0]);
			done = 1;
			break;
		case 'v':
			display_version();
			done = 1;
			break;
		case 'k':
			ret = daemon_pid_file_kill_wait(SIGQUIT, 30);
			if (ret < 0) {
				daemon_log(LOG_ERR, "[MAIN] Daemon not killed: (%s)", strerror(errno));
			} else {
				killed = 1;
			}
			done = 1;
			break;
		case 'f':
			daemonize = 0;
			break;
		case 'c':
			if (configfile) {
				free(configfile);
				configfile = NULL;
			}
			configfile = strdup(optarg);
			if (!configfile) {
				daemon_log(LOG_ERR, "[MAIN] strdup() failed");
				done = 1;
			}
			break;
		default:
			daemon_log(LOG_ERR, "[MAIN] Unsupported option");
			done = 1;
			break;
		}
	}

	return done;
}

const char *get_pid_filename(void)
{
	return "/var/run/tinypokerd/tinypokerd.pid";
}

int main(int argc, char *argv[], char *envp[])
{
	int fd, ret, uid, gid;
	struct passwd *pw;
	struct group *gr;
	struct rlimit rlim;
	pid_t pid;

	/* Default Values for Global Variables */
	daemonize = 1;
	killed = 0;
	setuid_name = NULL;
	setgid_name = NULL;
	x509_ca = NULL;
	x509_crl = NULL;
	x509_cert = NULL;
	x509_key = NULL;
	configfile = NULL;

	/* Sanity Checks */
	if (geteuid() != 0) {
		daemon_log(LOG_ERR, "[MAIN] You need root privileges to run this application.");
		return 1;
	}

	if (argc < 1 || !argv || !argv[0]) {
		daemon_log(LOG_ERR, "[MAIN] Cannot determine program name from argv[0]\n");
		return 1;
	}
	daemon_pid_file_ident = daemon_log_ident = daemon_ident_from_argv0(argv[0]);
	daemon_pid_file_proc = get_pid_filename;

	if (configfile) {
		free(configfile);
		configfile = NULL;
	}
	configfile = strdup(DEFAULT_CONFIGFILE);
	if (!configfile) {
		daemon_log(LOG_ERR, "[MAIN] strdup() failed");
		return 1;
	}

	/* Command Line Arguements */
	ret = parse_args(argc, argv);
	if (ret) {
		if (configfile) {
			free(configfile);
			configfile = NULL;
		}
		return (killed ? 0 : ret);
	}

	/* Configure */
	config_parse();

	if (configfile) {
		free(configfile);
		configfile = NULL;
	}

	/* Daemonize */
	if (daemonize) {
		/* Configure Logging */
		daemon_log_use = DAEMON_LOG_SYSLOG;

		umask(0);

		pid = fork();
		if (pid < 0) {
			return 1;
		} else if (pid > 0) {
			return 0;
		}
		setsid();

		pid = fork();
		if (pid < 0) {
			return 1;
		} else if (pid > 0) {
			return 0;
		}
		ret = chdir("/");
		if (ret < 0) {
			daemon_log(LOG_ERR, "[MAIN] Could not chdir() to '/': %s", strerror(errno));
			return 1;
		}
		/* close open file descriptors */
		for (fd = 0; fd < getdtablesize(); fd++) {
			ret = close(fd);
			if (ret == -1 && errno != EBADF) {
				daemon_log(LOG_ERR, "[MAIN] Could not close fd #%d: %s", fd, strerror(errno));
				return 1;
			}
		}

		/* re-open stdin, stdout, stderr */
		fd = open("/dev/null", O_RDONLY);
		fd = open("/dev/null", O_WRONLY);
		fd = open("/dev/null", O_WRONLY);
	}

	/* disable core dumps so usernames and passwords aren't dumped. */
	rlim.rlim_cur = 0;
	rlim.rlim_max = 0;
	ret = setrlimit(RLIMIT_CORE, &rlim);
	if (ret < 0) {
		daemon_log(LOG_ERR, "[MAIN] setrlimit() failed");
		return 1;
	}

	/* set max file size to 8MB (8388608 bytes) */
	rlim.rlim_cur = 8388608;
	rlim.rlim_max = 8388608;
	ret = setrlimit(RLIMIT_FSIZE, &rlim);
	if (ret < 0) {
		daemon_log(LOG_ERR, "[MAIN] setrlimit() failed");
		return 1;
	}

	/* set max address space to 32MB (33554432 bytes) */
	rlim.rlim_cur = 33554432;
	rlim.rlim_max = 33554432;
	ret = setrlimit(RLIMIT_AS, &rlim);
	if (ret < 0) {
		daemon_log(LOG_ERR, "[MAIN] setrlimit() failed");
		return 1;
	}

	/* set max file descriptor number */
	rlim.rlim_cur = 64;
	rlim.rlim_max = 64;
	ret = setrlimit(RLIMIT_NOFILE, &rlim);
	if (ret < 0) {
		daemon_log(LOG_ERR, "[MAIN] setrlimit() failed");
		return 1;
	}

	/* set max threads to 64 */
	rlim.rlim_cur = 64;
	rlim.rlim_max = 64;
	ret = setrlimit(RLIMIT_NPROC, &rlim);
	if (ret < 0) {
		daemon_log(LOG_ERR, "[MAIN] setrlimit() failed");
		return 1;
	}

	/* don't be a CPU hog */
	if (getpriority(PRIO_PROCESS, getpid()) < 0) {
		ret = setpriority(PRIO_PROCESS, getpid(), 0);
		if (ret == -1) {
			daemon_log(LOG_ERR, "[MAIN] setpriority() failed");
			return 1;
		}
	}

	uid = getuid();
	gid = getgid();

	gr = getgrnam(setgid_name);
	if (gr) {
		gid = gr->gr_gid;
	} else {
		daemon_log(LOG_ERR, "[MAIN] Could not determine groupId for group %s", setgid_name);
		return 1;
	}

	pw = getpwnam(setuid_name);
	if (pw) {
		uid = pw->pw_uid;
	} else {
		daemon_log(LOG_ERR, "[MAIN] Could not determine userId for user %s", setuid_name);
		return 1;
	}

	if (uid == 0 || gid == 0) {
		daemon_log(LOG_ERR, "[MAIN] Refusing to set userId and/or groupId to 0.");
		return 1;
	}

	/* drop privileges */
	ret = setgid(gid);
	if (ret) {
		daemon_log(LOG_ERR, "[MAIN] setgid(%d) failed", gid);
		return 1;
	}

	ret = setuid(uid);
	if (ret) {
		daemon_log(LOG_ERR, "[MAIN] setuid(%d) failed", uid);
		return 1;
	}

	pid = daemon_pid_file_is_running();
	if (pid > 0) {
		daemon_log(LOG_ERR, "[MAIN] %s is already running (PID => %u)", daemon_log_ident, pid);
		daemon_log(LOG_INFO, "[MAIN] Use `%s -k` to kill the running instance", daemon_log_ident);
		return 1;
	}
	ret = daemon_pid_file_create();
	if (ret < 0) {
		daemon_log(LOG_ERR, "[MAIN] Could not create PID file: %s", strerror(errno));
		return 1;
	}

	/*
	   daemon_log(LOG_INFO, "[MAIN] configuration set");
	   daemon_log(LOG_INFO, "[MAIN] setuid => '%s'", setuid_name);
	   daemon_log(LOG_INFO, "[MAIN] setgid => '%s'", setgid_name);
	   daemon_log(LOG_INFO, "[MAIN] x509_ca => '%s'", x509_ca);
	   daemon_log(LOG_INFO, "[MAIN] x509_crl => '%s'", x509_crl);
	   daemon_log(LOG_INFO, "[MAIN] x509_cert => '%s'", x509_cert);
	   daemon_log(LOG_INFO, "[MAIN] x509_key => '%s'", x509_key);
	 */

	/* setup tiny poker */
	ipp_init();

	/* daemon_log(LOG_INFO, "[MAIN] libtinypoker initialized"); */

	/* Install Signal Handlers */
	install_signal_handlers();
	/* daemon_log(LOG_INFO, "[MAIN] signal handlers set"); */

	/* this must run before any threads are created */
	monitor_init();
	/* daemon_log(LOG_INFO, "[MAIN] monitor set"); */

	/* Play some poker until we get a SIGINT, SIGQUIT, or SIGKILL */
	pokerserv();
	/* daemon_log(LOG_INFO, "[MAIN] shutting down"); */

	monitor_wait();		/* thread cleanup */
	/* daemon_log(LOG_INFO, "[MAIN] threads all cleaned up"); */

	ipp_exit();
	/* daemon_log(LOG_INFO, "[MAIN] libtinypoker cleared"); */

	config_free();
	/* daemon_log(LOG_INFO, "[MAIN] config cleared"); */

	daemon_pid_file_remove();
	/* daemon_log(LOG_INFO, "[MAIN] Exiting..."); */

	return 0;
}