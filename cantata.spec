
Name:    cantata
Summary: Music Player Daemon (MPD) graphical client
Version: 2.5.2
Release: 1.1%{?dist}

# Most files in this project are GPL-2.0-or-later.  Exceptions:
# (GPL-2.0-only OR GPL-3.0-only):
# - support/shortcutsmodel.{cpp,h}
# - support/shortcutssettingswidget.{cpp,h}
# GPL-3.0-or-later:
# - context/lyricsettings.{cpp,h}
# - context/ultimatelyrics.{cpp,h}
# - context/ultimatelyricsprovider.{cpp,h}
# - mpd-interface/cuefile.{cpp,h}
# - widgets/stretchheaderview.{cpp,h}
# LGPL-2.0-or-later:
# - devices/musicbrainz.{cpp,h}
# - support/acceleratormanager.{cpp,h}
# - support/acceleratormanager_private.h
# LGPL-2.1-or-later:
# - support/kmessagewidget.{cpp,h}
# - 3rdparty/solid-lite/xdgbasedirs.cpp
# - 3rdparty/solid-lite/xdgbasedirs_p.h
# LGPL-2.1-only:
# - support/fancytabwidget.{cpp,h}
# LGPL-3.0-only:
# - icons/yaru/render-bitmaps.py
# (LGPL-2.1-only OR LGPL-3.0-only):
# - 3rdparty/solid-lite (except as noted above)
# MIT:
# - support/windowmanager.{cpp,h}
#
# The following are not built into the binary RPM so their licenses are ignored:
# - 3rdparty/ebur128
# - 3rdparty/kcategorizedview
# - 3rdparty/qtiocompressor
# - 3rdparty/qtsingleapplication
# - 3rdparty/qxt
License: GPL-2.0-or-later AND (GPL-2.0-only OR GPL-3.0-only) AND GPL-3.0-or-later AND LGPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.1-only AND LGPL-3.0-only AND (LGPL-2.1-only OR LGPL-3.0-only) AND MIT
URL:     https://github.com/CDrummond/cantata
Source0: https://github.com/CDrummond/cantata/releases/download/v%{version}/cantata-%{version}.tar.bz2
Source1: com.github.cdrummond.cantata.metainfo.xml
# Unbundle the FontAwesome font file and adapt to FontAwesome 6.x
Patch0:  %{name}-unbundle-fontawesome.patch
# Unbundle qtiocompressor
Patch1:  %{name}-unbundle-qtiocompressor.patch

BuildRequires: appstream
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: ffmpeg-free-devel
BuildRequires: gcc-c++
BuildRequires: gettext
BuildRequires: pkgconfig(phonon4qt5)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Multimedia)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(Qt5Xml)
BuildRequires: qtiocompressor-devel
# translations
BuildRequires: qt5-linguist
BuildRequires: media-player-info
BuildRequires: pkgconfig(avahi-client)
BuildRequires: pkgconfig(cdparanoia-3)
BuildRequires: pkgconfig(libcddb)
BuildRequires: pkgconfig(libcdio_paranoia)
BuildRequires: pkgconfig(libebur128)
BuildRequires: pkgconfig(libmpg123)
BuildRequires: pkgconfig(libmtp)
BuildRequires: pkgconfig(libmusicbrainz5)
BuildRequires: pkgconfig(taglib)
BuildRequires: pkgconfig(taglib-extras)
BuildRequires: systemd-devel

Requires: font(fontawesome6brands)
Requires: font(fontawesome6free)
Requires: media-player-info

%description
Cantata is a graphical client for the music player daemon (MPD).

Features:
* Multiple MPD collections.
* Highly customisable layout.
* Songs grouped by album in play queue.
* Context view to show artist, album, and song information of current track.
* Simple tag editor.
* File organizer - use tags to organize files and folders.
* Ability to calculate ReplyGain tags.
* Dynamic playlists.
* Online services; Jamendo, Magnatune, SoundCloud, and Podcasts.
* Radio stream support - with the ability to search for streams via TuneIn
and ShoutCast.
* USB-Mass-Storage and MTP device support.
* Audio CD ripping and playback.
* Playback of non-MPD songs, via simple in-built HTTP server.
* MPRISv2 DBUS interface.
* Support for KDE global shortcuts (KDE builds), GNOME media keys, and generic
media keys (via Qxt support)
* Ubuntu/ambiance theme integration.


%prep
%autosetup -p1

rm -fv translations/blank.ts

# Make sure the bundled FontAwesome font file is not used
rm -fv support/Cantata-FontAwesome* support/support.qrc

# Make sure the bundled qtiocompressor is not used
rm -rf 3rdparty/qtiocompressor

# Inject the version number for qtiocompressor
iocversion=$(ls -1 %{_libdir}/libQt5Solutions_IOCompressor-*.so | sed 's/.*-\([.[:digit:]]*\)\.so/\1/')
sed -i "s/@IOCVERSION@/$iocversion/" CMakeLists.txt

%build
PATH="%{_qt5_bindir}:$PATH" ; export PATH ;

%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_KDE:BOOL=%{?kde:ON}%{!?kde:OFF} \
  -DENABLE_QT5:BOOL=%{?qt5:ON}%{!?qt5:OFF} \
  -DENABLE_FFMPEG=ON -DENABLE_CATEGORIZED_VIEW=ON

%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}%{_metainfodir}
install -pm 644 %{SOURCE1} %{buildroot}%{_metainfodir}

%find_lang %{name} --with-qt --all-name

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/cantata.desktop 
appstreamcli validate --no-net \
  %{buildroot}%{_metainfodir}/com.github.cdrummond.cantata.metainfo.xml

%files -f %{name}.lang
%doc AUTHORS ChangeLog README TODO
%license LICENSE
%{_bindir}/cantata
# libexecdir type stuff
%{_prefix}/lib/cantata/
%{_metainfodir}/com.github.cdrummond.cantata.metainfo.xml
%{_datadir}/applications/cantata.desktop
%{_datadir}/icons/hicolor/*/*/*
%dir %{_datadir}/cantata/
%{_datadir}/cantata/icons/
%{_datadir}/cantata/scripts/
%dir %{_datadir}/cantata/translations/

%changelog
* Wed Jul 31 2024 11:54:03 +0530 Manvendra Bhangui <cantata@indimail.org> 2.5.2-1.1
- mac/macnotify.mm: Fixed crash on macos when output device is changed
- mpd-interface/mpdconnections.h: fixed "Unsupported URI scheme" error
  message in mpd log (incorrect lsinfo command)
- mpd-interface/mpdconnections.cpp: Increased constConnTimer value to 10000,
  constSocketCommsTimeout to 4000, constConnTimer to 10000
- mpd-interface/mpdconnections.cpp: added constSocketDataTimeout=2000
- mpd-interface/mpdconnections.cpp: Changed [Radio Streams] to Radio-Streams
- mpd-interface/mpdconnections.cpp: Create MPD_HOST, MUSIC_DIR files in
  $HOME/.config/cantata
- mpd-interface/mpdconnections.cpp: fixed multiple reconnects from power
  management code
- mpd-interface/mpdconnections.cpp: removed dead code
- scrobbling/scrobblinglove.cpp: replaced mpc_o with cantata-mpc

* Mon Apr 15 2024 12:17:29 +0530 Manvendra Bhangui <cantata@indimail.org> - 2.5.1-1
- Scrobbling button fixes

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 30 2023 Jerry James <loganjerry@gmail.com> - 2.5.0-1
- Version 2.5.0 (bz 2060187)
- Convert the License tag to SPDX and clarify the license
- Add an AppData file (bz 2099339)
- Unbundle the FontAwesome font, libebur128, and qtiocompressor
- Be compatible with FontAwesome 6.x
- Enable avahi, ffmpeg, and mpg123 support

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 04 2022 Rex Dieter <rdieter@fedoraproject.org> - 2.4.2-5
- drop qt4 build dep (phonon)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 26 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 2.4.2-1
- build(update): 2.4.2 | Fix: rh#1855892

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 30 2020 Adrian Reber <adrian@lisas.de> - 2.3.1-6
- Rebuilt for libcdio-2.1.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.3.1-1
- cantata-2.3.1
- include upstream commit that removes samba share mounting code

* Fri Apr 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.3.0-1
- cantata-2.3.0

* Thu Mar 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.2.0-1
- cantata-2.2.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.1-5
- Remove obsolete scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 06 2016 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-1
- 2.0.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-1
- 2.0.0, Qt 5 build (#1147393)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Thu Nov 27 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 1.4.1-2
- Rebuilt against newer libmusicbrainz5

* Wed Aug 27 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.4.1-1
- cantata-1.4.1 (#1082278)
- missing dependency oxygen theme (#1134333)
- re-enable kde build

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 09 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.4-2
- make libsolidlite convenience lib explicitly static

* Sat Jun 07 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.3.4-1
- cantata-1.3.4
- disable kde integration (for now, FTBFS)
- revert whitespace changes
- restore cmake types for build options
- use system libqxt
- ready Qt5-enabled build (not used yet)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.2.2-2
- Use system qtiocompressor instead of bundled one

* Mon Jan 06 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-1
- cantata-1.2.2 (#1048750)

* Thu Dec 26 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-1
- cantata-1.2.1 (#1034054)

* Tue Dec 17 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-1
- cantata-1.2.0

* Tue Dec 17 2013 Rex Dieter <rdieter@fedoraproject.org> 1.1.3-1
- cantata-1.1.3 

* Wed Aug 14 2013 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-1
- cantata-1.1.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.9.2-2
- Perl 5.18 rebuild

* Mon Jan 28 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2

* Sat Jan 05 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-1
- cantata-0.9.1

* Wed Nov 28 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.3.1-2
- patch s|^#!/usr/bin/env perl|#!/usr/bin/perl|

* Tue Sep 25 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.3.1-1
- cantata-0.8.3.1
- run desktop-file-validate
- add icon scriptlets
- drop Requires: mpd
- %%doc LICENSE AUTHORS ChangeLog README TODO
- omit and explicitly disable ffmpeg, mpg123 support

* Thu Aug 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-1
- first try

