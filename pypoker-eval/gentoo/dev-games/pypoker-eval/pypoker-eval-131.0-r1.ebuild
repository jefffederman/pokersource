# Copyright 1999-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header$

inherit eutils

DESCRIPTION="python binding for poker-eval"
HOMEPAGE="http://gna.org/projects/pokersource"
MY_P="${PN}_${PV}.orig.tar.gz"
SRC_URI="http://mekensleep.org/gnulinux/gentoo/distfiles/${MY_P}"
SLOT="0"
LICENSE="GPL-2.1"
KEYWORDS="x86"
IUSE=""

DEPEND="poker-eval virtual/python"

src_unpack() {
	unpack ${MY_P}
	if ls ${FILESDIR}/${PVR}*.patch 2>/dev/null
		then
		for i in ${FILESDIR}/${PVR}*.patch
		  do
		  epatch $i
		done
	fi
}


src_install () {
	make install DESTDIR=${D} || die "einstall failed"
}
