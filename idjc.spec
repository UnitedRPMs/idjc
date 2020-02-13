#
# spec file for package idjc
#
# Copyright (c) 2020 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

%global _with_restricted 1

Name:           idjc
Version:        0.8.17
Release:        7%{?dist}
Summary:        DJ application for streaming audio

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://idjc.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/idjc/%{name}-%{version}.tar.gz

BuildRequires:  pygtk2-devel
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libsndfile-devel
BuildRequires:  speex-devel
BuildRequires:  flac-devel
BuildRequires:  desktop-file-utils
BuildRequires:  glib2-devel
BuildRequires:  libshout-idjc-devel >= 2.4.3
BuildRequires:  libmad-devel
BuildRequires:  twolame-devel
BuildRequires:  lame-devel
BuildRequires:  mpg123-devel
BuildRequires:  opus-devel
BuildRequires:	gcc-c++
BuildRequires:	python2-rpm-macros
%if 0%{?fedora} >= 32
BuildRequires:	python2-pip
BuildRequires:	git
%endif

%if 0%{?_with_restricted}
BuildRequires:  ffmpeg-devel >= 4.1
%endif

Requires:       pygtk2
Requires:       dbus-python
%if 0%{?fedora} <= 31
Requires:       python2-mutagen
%endif
Requires:       pulseaudio-module-jack
Requires:       alsa-plugins-jack
Requires:       qjackctl
Requires:       lame
Requires:       lame-libs
Requires:       twolame
Requires:       libmad
Requires:       mpg123-libs
Requires:       opus
Requires:       flac
Requires:       MySQL-python
Requires:       libshout-idjc

%if 0%{?_with_restricted}
Requires:       ffmpeg
%endif


%description
Internet DJ Console is a client for streaming live radio shows over the
Internet using Icecast or Shoutcast servers. It has a two panel playlist mode,
with automatic cross-fading. It uses jack as a back-end and it supports all
major free audio codecs.


%prep
%setup -n %{name}-%{version}

sed -i 's|PYTHON=python|PYTHON=python2|g' py-compile

%build

find -depth -type f -writable -name "*.py" -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python2}=' {} +

export PYTHON=/usr/bin/python2
./configure \
    --prefix=/usr \
    --libdir=%{_libdir} \
    --enable-lame \
    --enable-mpg123 \
    --enable-twolame \
    --enable-opus \
    --enable-speex \
    --enable-flac \
%if 0%{?_with_restricted}
    --enable-libav
%endif
make


%install

make install DESTDIR=%{buildroot}

%find_lang %{name}


%if 0%{?fedora} >= 32
python2 -m pip install --user 'mutagen==1.43.0' 
pushd $HOME
cp -rf .local/lib/python2.7/site-packages/* %{buildroot}/%{python2_sitelib}/
popd
%endif

%post

if [ ! -f %{_libdir}/libmp3lame.so ]; then
ln -s %{_libdir}/libmp3lame.so.0.0.0 %{_libdir}/libmp3lame.so
fi

if [ ! -f %{_libdir}/libmad.so ]; then
ln -s %{_libdir}/libmad.so.0.2.1 %{_libdir}/libmad.so
fi


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%{_bindir}/idjc
%{python2_sitelib}/idjcmonitor.py
%{python2_sitelib}/idjcmonitor.pyc
%{python2_sitelib}/idjcmonitor.pyo
%{_libdir}/idjc/
%{_datadir}/applications/idjc.desktop
%{_docdir}/%{name}-%{version}/
%{_datadir}/idjc/
%{_mandir}/man1/idjc-auto.1.gz
%{_mandir}/man1/idjc-ls.1.gz
%{_mandir}/man1/idjc-new.1.gz
%{_mandir}/man1/idjc-noauto.1.gz
%{_mandir}/man1/idjc-rm.1.gz
%{_mandir}/man1/idjc-run.1.gz
%{_mandir}/man1/idjc.1.gz
%{_datadir}/pixmaps/idjc.png
%{_datadir}/appdata/idjc.appdata.xml

%if 0%{?fedora} >= 32
%{python2_sitelib}/mutagen-1.43.0.dist-info/
%{python2_sitelib}/mutagen/
%endif

%changelog

* Tue Feb 11 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.8.17-7 
- Rebuilt for ffmpeg
- pypi mutagen for deprecation of python2

* Thu Dec 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.8.17-6  
- Rebuilt for ffmpeg

* Sat Sep 15 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.8.17-5  
- Automatic Mass Rebuild

* Thu Sep 13 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.8.17-4  
- Rebuilt for libshout-idjc

* Thu Apr 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.8.17-2  
- Automatic Mass Rebuild

* Mon Dec 11 2017 Francisco de la Peña <fran AT fran DOT cr> 0.8.17-1
- Updated to 0.8.17

* Wed Oct 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.8.16-7  
- Automatic Mass Rebuild

* Mon Jul 24 2017 Francisco de la Peña <fran AT fran DOT cr> 0.8.16-6
- Add pygtk2 dependency
- Remove MP3 dependencies from restricted
- Remove obsolete sed call

* Sun May 07 2017 Francisco de la Peña <fran AT fran DOT cr> 0.8.16-5
- Add dbus-python dependency

* Tue Apr 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.8.16-4
- Automatic Mass Rebuild

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.8.16-3
- Rebuilt for libbluray

* Thu Jun 30 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.8.16-1
- Updated to 0.8.16

* Wed Sep 09 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.8.15-1
- Updated to 0.8.15

* Mon Oct 27 2014 David Vasquez <davidjeremias82 at gmail dot com> - 0.8.14-1
- Initial build
