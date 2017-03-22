%global _with_restricted 1

Name:           idjc
Version:        0.8.16
Release:        3%{?dist}
Summary:        DJ application for streaming audio

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://idjc.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/idjc/idjc/0.8/%{name}-%{version}.tar.gz

BuildRequires:  pygtk2-devel
BuildRequires:  python-devel
BuildRequires:	python-setuptools
BuildRequires:  python-mutagen
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libsndfile-devel
BuildRequires:  speex-devel
BuildRequires:  flac-devel
BuildRequires:  desktop-file-utils
BuildRequires:  glib2-devel
BuildRequires:  libshout-idjc-devel >= 2.4.1

%if 0%{?_with_restricted}
BuildRequires:	libmad-devel
BuildRequires:	twolame-devel
BuildRequires:	lame-devel
BuildRequires:	mpg123-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	opus-devel
%endif

Requires:       python-mutagen
Requires:       pulseaudio-module-jack
Requires:	alsa-plugins-jack 
Requires:	qjackctl 

%if 0%{?_with_restricted}
Requires:	ffmpeg
Requires:	lame 
Requires:	lame-libs
Requires:	twolame
Requires:	libmad
Requires:	mpg123-libs
Requires:	opus
%endif

Requires:	flac
Requires:	MySQL-python
Requires:	libshout-idjc


%description
Internet DJ Console is a client for streaming live radio shows over the
Internet using Icecast or Shoutcast servers. It has a two panel playlist mode,
with automatic cross-fading. It uses jack as a back-end and it supports all
major free audio codecs.


%prep
%setup -q -n %{name}-%{version}


%build
./configure  \
    --prefix=/usr  \
    --libdir=%{_libdir} \
%if 0%{?_with_restricted}
    --enable-libav \
    --enable-lame \
    --enable-mpg123 \
    --enable-twolame \
    --enable-opus  \
%endif
    --enable-speex  \
    --enable-flac  
make 


%install

make install DESTDIR=%{buildroot}
sed -i 's|#! /usr/bin/python22.7|#! /usr/bin/python2|' %{buildroot}/usr/bin/idjc

%find_lang %{name}

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

%changelog

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.8.16-3
- Rebuilt for libbluray

* Thu Jun 30 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.8.16-1
- Updated to 0.8.16

* Wed Sep 09 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.8.15-1
- Updated to 0.8.15

* Mon Oct 27 2014 David Vasquez <davidjeremias82 at gmail dot com> - 0.8.14-1
- Initial build
