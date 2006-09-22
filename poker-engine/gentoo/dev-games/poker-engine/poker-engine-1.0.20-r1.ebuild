# Copyright 1999-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header$

inherit eutils

DESCRIPTION="poker-engine is a python library that implements poker rules according to variants and betting structures specified in configuration files"
HOMEPAGE="http://gna.org/projects/pokersource"
MY_P="${PN}-${PV}.tar.gz"
SRC_URI="http://download.gna.org/underware/sources/${MY_P}"
SLOT="0"
LICENSE="GPL-2.1"
KEYWORDS="x86"
IUSE=""

DEPEND=">=sys-devel/automake-1.9.0 dev-util/pkgconfig >=dev-lang/python-2.4.0 dev-games/pypoker-eval dev-libs/libxml2 dev-libs/libxslt dev-python/pyxml net-misc/rsync"

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
