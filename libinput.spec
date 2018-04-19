%global udevdir %(pkg-config --variable=udevdir udev)

#global gitdate 20141211
%global gitversion 58abea394

Name:           libinput
Version:        1.10.4
Release:        2%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
Summary:        Input device library

License:        MIT
URL:            http://www.freedesktop.org/wiki/Software/libinput/
%if 0%{?gitdate}
Source0:        %{name}-%{gitdate}.tar.xz
Source1:        make-git-snapshot.sh
Source2:        commitid
%else
Source0:        http://www.freedesktop.org/software/libinput/libinput-%{version}.tar.xz
%endif

Patch01:        0001-evdev-disable-ABS_MT_TOOL_PALM-on-the-Lenovo-X1-Carb.patch

BuildRequires:  git-core
BuildRequires:  gcc gcc-c++
BuildRequires:  meson
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(mtdev) >= 1.1.0
BuildRequires:  pkgconfig(libevdev) >= 0.4
BuildRequires:  pkgconfig(libwacom) >= 0.20

%description
libinput is a library that handles input devices for display servers and other
applications that need to directly deal with input devices.

It provides device detection, device handling, input device event processing
and abstraction so minimize the amount of custom input code the user of
libinput need to provide the common set of functionality that users expect.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        utils
Summary:        Utilities and tools for debugging %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-evdev python3-pyudev

%description    utils
The %{name}-utils package contains tools to debug hardware and analyze
%{name}.

%prep
%autosetup -S git

%build
%meson -Ddebug-gui=false \
       -Ddocumentation=false \
       -Dtests=false \
       -Dudev-dir=%{udevdir}
%meson_build

%install
%meson_install

%post
/sbin/ldconfig
/usr/bin/udevadm hwdb --update  >/dev/null 2>&1 || :

%postun -p /sbin/ldconfig


%files
%doc COPYING
%{_libdir}/libinput.so.*
%{udevdir}/libinput-device-group
%{udevdir}/libinput-model-quirks
%{udevdir}/rules.d/80-libinput-device-groups.rules
%{udevdir}/rules.d/90-libinput-model-quirks.rules
%{udevdir}/hwdb.d/90-libinput-model-quirks.hwdb
%{_bindir}/libinput
%dir %{_libexecdir}/libinput/
%{_libexecdir}/libinput/libinput-debug-events
%{_libexecdir}/libinput/libinput-list-devices
%{_mandir}/man1/libinput.1*

%{_mandir}/man1/libinput-list-devices.1*
%{_mandir}/man1/libinput-debug-events.1*
%{_bindir}/libinput-list-devices
%{_bindir}/libinput-debug-events

%files devel
%{_includedir}/libinput.h
%{_libdir}/libinput.so
%{_libdir}/pkgconfig/libinput.pc

%files utils
%{_libexecdir}/libinput/libinput-measure
%{_libexecdir}/libinput/libinput-measure-touchpad-tap
%{_libexecdir}/libinput/libinput-measure-touchpad-pressure
%{_libexecdir}/libinput/libinput-measure-touch-size
%{_libexecdir}/libinput/libinput-measure-trackpoint-range
%{_mandir}/man1/libinput-measure.1*
%{_mandir}/man1/libinput-measure-touchpad-tap.1*
%{_mandir}/man1/libinput-measure-touch-size.1*
%{_mandir}/man1/libinput-measure-touchpad-pressure.1*
%{_mandir}/man1/libinput-measure-trackpoint-range.1*

%changelog
* Thu Apr 19 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.4-2
- Disable ABS_MT_TOOL_PALM on the Lenovo Carbon X1 6th (#1565692)

* Mon Apr 09 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.4-1
- libinput 1.10.4

* Wed Mar 14 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.3-1
- libinput 1.10.3

* Mon Mar 12 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.2-4
- Fix occasional crashes on gestures when libinput loses track of hovering
  fake fingers

* Thu Mar 08 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.2-3
- Add BuildRequires gcc-c++, needed for a test build

* Wed Mar 07 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.2-2
- libinput 1.10.2

* Fri Mar 02 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.1-2
- Fix touchpad jitter by changing from "disable if no jitter" to "enable if
  jitter" (#1548550)

* Wed Feb 28 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.1-1
- libinput 1.10.1

* Tue Feb 13 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.0-2
- Fix crasher due to missing devnode after resume (#1536633)

* Tue Feb 13 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.10.0-1
- libinput 1.10

* Tue Feb 06 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.9.902-1
- libinput 1.10rc2

* Mon Feb 05 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.9.901-3
- Fix crasher on first event from tablets not supported by libwacom
  (#1535755)

* Fri Feb 02 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.9.901-2
- Use autosetup instead of the manual git magic

* Mon Jan 22 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.9.901-1
- libinput 1.10rc1

* Thu Dec 14 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.4-1
- libinput 1.9.4

* Fri Dec 08 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.3-2
- Immediately post key events, don't wait for EV_SYN

* Tue Nov 28 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.3-1
- libinput 1.9.3

* Wed Nov 15 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.2-1
- libinput 1.9.2

* Wed Nov 15 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-4
- Mark the Lenovo Compact Keyboard as external (#1510814)

* Tue Nov 14 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-3
- Handle printing of tablet mode switches (#1510814)

* Thu Nov 09 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-2
- Split some of the tools into a libinput-utils package so we can require
  the various bits easier (#1509298)

* Mon Oct 30 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-1
- libinput 1.9.1

* Thu Oct 26 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-2
- Drop explicit .gz from the man pages

* Thu Oct 19 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-1
- libinput 1.9.0

* Tue Oct 10 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.8.902-1
- libinput 1.9rc2

* Thu Sep 28 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.8.901-1
- libinput 1.9rc1

* Thu Sep 07 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.8.2-1
- libinput 1.8.2

* Tue Sep 05 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.8.1-4
- Don't try pinching when the finger number exceeds available slots
- Don't resume a disabled touchpad after a lid switch open (#1448962)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.8.1-1
- libinput 1.8.1

* Thu Jul 13 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.0-2
- Add missing BuildRequires: gcc
- Fixup other BuildRequires
- Rebuild for pkg-config fix from meson

* Mon Jul 03 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-1
- libinput 1.8

* Tue Jun 27 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.902-2
- Switch to meson as build system

* Mon Jun 26 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.902-1
- libinput 1.8rc2

* Mon Jun 19 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.901-2
- libinput 1.8rc1 with source files this time

* Mon Jun 19 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.901-1
- libinput 1.8rc1

* Mon Jun 12 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.3-1
- libinput 1.7.3

* Tue May 09 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.2-2
- Ignore taps in the palm detection area even in software buttons (#1415796)

* Tue May 09 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.2-1
- libinput 1.7.2

* Thu May 04 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.1-4
- Fix a crash when shutting down a touchpad lid listener (#1440927)

* Thu May 04 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.1-3
- Fix crash when we have multiple keyboard event listeners for the lid
  switch (#1440927)

* Tue May 02 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.1-2
- Add patches to fix elantech pressure detection

* Tue Apr 25 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.1-1
- libinput 1.7.1

* Thu Mar 23 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.7.0-1
- libinput 1.7

* Fri Mar 10 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.902-1
- libinput 1.7rc2

* Thu Feb 23 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.901-1
- libinput 1.7rc1

* Wed Feb 22 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.2-2
- Fix middle button emulation for Logitech Marble Mouse (#1421439)

* Tue Feb 21 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.2-1
- libinput 1.6.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.1-1
- libinput 1.6.1

* Wed Feb 01 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-2
- revert the tap timeout reduction (#1414935)

* Fri Jan 20 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-1
- libinput 1.6

* Mon Jan 16 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.5.902-1
- libinput 1.6rc2

* Tue Jan 10 2017 Peter Hutterer <peter.hutterer@redhat.com> 1.5.901-1
- libinput 1.6rc1

* Wed Dec 07 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.3-1
- libinput 1.5.3

* Fri Nov 25 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.2-2
- Swap to the correct tarball so we match the checksums from upstream (had a
  local mixup of tarballs)

* Fri Nov 25 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.2-1
- libinput 1.5.2

* Tue Nov 22 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.1-2
- Improve responsiveness of touchpads by reducing the motion history.

* Fri Nov 11 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.1-1
- libinput 1.5.1

* Wed Sep 14 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.0-2
- Drop the synaptics 3-slot workaround

* Wed Sep 14 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.5.0-1
- libinput 1.5.0

* Thu Sep 08 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.4.901-2
- Avoid spurious trackpoint events halting the touchpad (related #1364850)

* Wed Sep 07 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.4.901-1
- libinput 1.5rc1

* Wed Aug 31 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.4.2-2
- Add quirk for the HP 8510w touchpad (#1351285)

* Tue Aug 30 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.4.2-1
- libinput 1.4.2

* Fri Aug 05 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.4.1-1
- libinput 1.4.1

* Mon Jul 18 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-1
- libinput 1.4

* Tue Jul 12 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.3.901-1
- libinput 1.4rc1

* Fri Jun 24 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.3.3-2
- Drop the now unnecessary patch

* Fri Jun 24 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.3.3-1
- libinput 1.3.3

* Thu Jun 16 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.3.2-1
- libinput 1.3.2

* Mon May 30 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.3.1-1
- libinput 1.3.1

* Fri May 20 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-3
- Stop pointer jitter on the Dell E5420, E530 and Lenovo Yoga 2

* Thu May 19 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-2
- Disable negative pressure transition on non-synaptics pads to avoid
  jerky movement (#1335249)

* Tue May 10 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-1
- libinput 1.3.0

* Wed May 04 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.903-1
- libinput 1.3rc3

* Thu Apr 21 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.902-1
- libinput 1.3rc2

* Tue Apr 19 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.4-1
- libinput 1.2.4

* Tue Apr 12 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.3-1
- libinput 1.2.3

* Tue Mar 15 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-1
- libinput 1.2.2

* Fri Mar 11 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-4
- Fix jerky pointer motion on the Lenovo T450/T460/X1 3rd hardware

* Mon Mar 07 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-3
- Fix segfault on mislabeled tablets (#1314955)

* Wed Mar 02 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-2
- Bump to maintain upgrade path with F23

* Mon Feb 29 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-1
- libinput 1.2.1

* Tue Feb 23 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.2.0-1
- libinput 1.2.0

* Mon Feb 15 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.1.902-2
- Add libwacom-devel to BuildRequires

* Mon Feb 15 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.1.902-1
- libinput 1.2rc2

* Wed Feb 10 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.1.7-1
- libinput 1.1.7

* Fri Feb 05 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.1.6-1
- libinput 1.1.6

* Thu Feb 04 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.1.5-4
- Fix patches from -3, they got corrupted somehow

* Thu Feb 04 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.1.5-3
- Disable the mode button on the Cyborg RAT 5
- Drop touchpad motion hysteresis by default

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.1.5-1
- libinput 1.1.5

* Tue Jan 19 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.1.4-3
- disable MT for semi-mt devices to solve the various two- and three-finger
  issues (at the cost of pinch gestures) (#1295073)

* Mon Jan 11 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.1.4-2
- fix disable-while-typing on macbooks

* Tue Dec 22 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.1.4-1
- libinput 1.1.4

* Wed Dec 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.1.3-1
- libinput 1.1.3

* Wed Dec 09 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.1.2-1
- libinput 1.1.2

* Mon Dec 07 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.1.1-2
- Reduce 2fg scroll threshold to 1mm (#1247958)

* Mon Nov 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.1.1-1
- libinput 1.1.1

* Mon Nov 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-3
- Fix invalid device group pointer, causing invalid memory access

* Wed Oct 28 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-2
- Fix crash triggered by Asus RoG Gladius mouse (#1275407)

* Mon Oct 26 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-1
- libinput 1.1.0

* Wed Oct 21 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.0.2-1
- libinput 1.0.2

* Sat Sep 19 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-3
- Fix the number of clicks sent in multitap (fdo #92016)

* Mon Sep 07 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-2
- Don't interpret short scrolls as right click (#1256045)

* Thu Sep 03 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.0.1-1
- libinput 1.0.1

* Wed Aug 26 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-1
- libinput 1.0

* Fri Aug 21 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.99.1-1
- libinput 1.0RC1

* Wed Aug 05 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.21.0-3
- Fix 2fg scroll threshold handling (#1249365)

* Tue Aug 04 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.21.0-2
- Fix pointer speed configuration, broke with 0.21.0

* Tue Aug 04 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.21.0-1
- libinput 0.21.0
- fix 3fg touch detection on Synaptics semi-mt touchpads

* Thu Jul 30 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.20.0-6
- Fix broken 2fg scrolling on single-touch touchpads (#1246651)
- Drop distance threshold for 2fg gesture detection (#1246868)

* Wed Jul 29 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.20.0-5
- Add a size hint for Apple one-button touchpads (#1246651)

* Wed Jul 29 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.20.0-4
- Disable 2fg scrolling on Synaptics semi-mt (#1235175)

* Fri Jul 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.20.0-3
- Disable thumb detection, too many false positives (#1246093)

* Tue Jul 21 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.20.0-2
- Restore parsing for trackpoing const accel

* Thu Jul 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.20.0-1
- libinput 0.20

* Tue Jul 14 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.19.0-3
- Only edge scroll when the finger is on the actual edge

* Thu Jul 09 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.19.0-2
- enable edge scrolling on clickpads (#1225579)

* Mon Jul 06 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.19.0-1
- libinput 0.19.0

* Wed Jul 01 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-5
- Improve trackpoint->touchpad transition responsiveness (#1233844)

* Mon Jun 29 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-4
- Steepen deceleration curve to get better 1:1 movement on slow speeds
  (#1231304)
- Provide custom accel method for <1000dpi mice (#1227039)

* Thu Jun 25 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-3
- Fix stuck finger after a clickpad click on resolutionless touchpads

* Wed Jun 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-2
- Fix initial jump during edge scrolling

* Mon Jun 22 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-1
- libinput 0.18.0

* Tue Jun 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-5
- Use physical values for the hystersis where possible (#1230462)
- Disable right-edge palm detection when edge scrolling is active
  (fdo#90980)

* Tue Jun 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-4
- Avoid erroneous finger movement after a physical click (#1230441)

* Fri Jun 12 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-3
- Require udev.pc for the build

* Tue Jun 09 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-2
- Cap the minimum acceleration slowdown at 0.3 (#1227796)

* Thu Jun 04 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-1
- libinput 0.17

* Tue Jun 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-4
- Always set the middle button as default button for button-scrolling
  (#1227182)

* Tue Jun 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-3
- Reduce tap-n-drag timeout (#1225998)

* Tue Jun 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-2
- Handle slow motions better (#1227039)

* Tue Jun 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-1
- libinput 0.16.0

* Fri May 29 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-4
- Add tap-to-end-drag patch (#1225998)
 
* Wed May 27 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-3
- Refine disable-while-typing (#1209753)

* Mon May 18 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-2
- Add disable-while-typing feature (#1209753)

* Tue May 05 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-1
- libinput 0.15.0

* Fri Apr 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.14.1-2
- Fix crash with the MS Surface Type Cover (#1206869)

* Wed Apr 22 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.14.1-1
- libinput 0.14.1

* Thu Apr 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-6
- git add the patch...

* Thu Apr 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-5
- Reduce palm detection threshold to 70mm (#1209753)
- Don't allow taps in the top part of the palm zone (#1209753)

* Thu Apr 09 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-4
- Fix finger miscounts on single-touch touchpads (#1209151)

* Wed Apr 08 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-3
- Fix mouse slowdown (#1208992)

* Wed Apr 08 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-2
- Fix crasher triggered by fake MT devices without ABS_X/Y (#1207574)

* Tue Mar 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-1
- libinput 0.13.0

* Fri Mar 20 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.12.0-2
- Install the udev rules in the udevdir, not libdir (#1203645)

* Tue Mar 10 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.12.0-1
- libinput 0.12.0

* Mon Feb 23 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.11.0-1
- libinput 0.11.0

* Fri Feb 06 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-1
- libinput 0.10.0

* Fri Jan 30 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.9.0-1
- libinput 0.9.0

* Mon Jan 19 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.8.0-1
- libinput 0.8.0

* Thu Dec 11 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-2.20141211git58abea394
- git snapshot, fixes a crasher and fd confusion after suspending a device

* Fri Dec 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-1
- libinput 0.7.0

* Mon Nov 24 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.6.0-3.20141124git92d178f16
- Add the hooks to build from a git snapshot
- Disable silent rules
- Update to today's git master

* Fri Sep 12 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.6.0-2
- libinput 0.6.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.5.0-1
- libinput 0.5.0

* Wed Jul 02 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.4.0-2
- Add the new touchpad pointer acceleration code

* Wed Jun 25 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.0-1
- Update to 0.4.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.2.0-1
- libinput 0.2.0

* Fri Feb 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.0-1
- Initial Fedora packaging
