Name:           signalrgb
Version:        2.5.86
Release:        7617%{?dist}
Summary:        Control and sync your RGB devices
License:        LicenseRef-Proprietary
URL:            https://www.signalrgb.com/
Source0:        https://pkgs.signalrgb.com/apt/pool/stable/main/s/signalrgb/signalrgb_%{version}-7617_amd64.deb
# SHA256:        5c8c29d193f75ff1d02874bbd32ca2b130b75a0312bb9d6fafea156b3da2599c

BuildArch:      x86_64
# The upstream binaries are already stripped; Fedora cannot generate a
# meaningful debuginfo or debugsource package from the Debian payload.
%global debug_package %{nil}
BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  zstd

# The upstream Debian package bundles most of Qt and its application runtime
# under /opt/signalrgb/lib. These are the host libraries it still needs.
Requires:       alsa-lib
Requires:       atk
Requires:       libatomic
Requires:       brotli
Requires:       bzip2-libs
Requires:       glibc >= 2.38
Requires:       cairo
Requires:       libcurl
Requires:       dbus-libs
Requires:       libdrm
Requires:       mesa-libEGL
Requires:       expat
Requires:       fontconfig
Requires:       freetype
Requires:       mesa-libgbm
Requires:       libgcc
Requires:       gdk-pixbuf2
Requires:       mesa-libGL
Requires:       libglvnd-glx
Requires:       glib2
Requires:       krb5-libs
Requires:       gtk3
Requires:       harfbuzz
Requires:       nspr
Requires:       nss
Requires:       libglvnd-opengl
Requires:       pango
Requires:       pipewire-libs
Requires:       pulseaudio-libs
Requires:       libsecret
Requires:       openssl3-libs
Requires:       libstdc++
Requires:       tesseract-libs
Requires:       systemd-libs
Requires:       libwayland-client
Requires:       libwayland-cursor
Requires:       libwayland-egl
Requires:       libX11
Requires:       libXcomposite
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXi
Requires:       libXrandr
Requires:       libXScrnSaver
Requires:       libXrender
Requires:       libXtst
Requires:       libxcb
Requires:       xcb-util
Requires:       xcb-util-cursor
Requires:       xcb-util-image
Requires:       xcb-util-keysyms
Requires:       xcb-util-renderutil
Requires:       xcb-util-wm
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       libxkbfile
Requires:       libxshmfence
Requires:       zlib
Requires:       libzstd
Requires:       tesseract-langpack-eng
Recommends:     vulkan-loader

# Disable automatic dependency generation: the application ships many private
# shared libraries in /opt/signalrgb/lib that must not become system Provides.
AutoReqProv:    no

%description
SignalRGB controls and synchronizes RGB lighting devices. This package is
repacked from the upstream x86_64 Debian package for Fedora systems.

%prep
%setup -q -c -T
mkdir -p payload
cd payload
ar x %{SOURCE0}
tar --zstd -xf data.tar.zst

%build
# Upstream provides a prebuilt application.

%install
mkdir -p %{buildroot}
cp -a payload/opt %{buildroot}/
cp -a payload/usr %{buildroot}/
# Fedora's Tesseract 5.5 uses a more specific SONAME than the upstream
# binary expects. Its referenced TessBaseAPI symbols are present in 5.5.
ln -s %{_libdir}/libtesseract.so.5.5 \
    %{buildroot}/opt/signalrgb/lib/libtesseract.so.5
# Fedora's bzip2 runtime provides the same 1.0 ABI as libbz2.so.1.
ln -s %{_libdir}/libbz2.so.1 \
    %{buildroot}/opt/signalrgb/lib/libbz2.so.1.0
install -Dpm0644 payload/etc/udev/rules.d/72-signalrgb.rules \
    %{buildroot}/usr/lib/udev/rules.d/72-signalrgb.rules
rm -rf %{buildroot}/etc
chmod 0755 %{buildroot}%{_bindir}/signalrgb

%posttrans
if [ -x /usr/bin/udevadm ]; then
    /usr/bin/udevadm control --reload-rules || :
    /usr/bin/udevadm trigger || :
fi
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q %{_datadir}/applications || :
fi

%postun
if [ -x /usr/bin/udevadm ]; then
    /usr/bin/udevadm control --reload-rules || :
fi
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q %{_datadir}/applications || :
fi

%files
/opt/signalrgb
%{_bindir}/signalrgb
%{_datadir}/applications/signalrgb.desktop
%{_datadir}/icons/hicolor/*/apps/signalrgb.png
%{_datadir}/pixmaps/signalrgb.png
/usr/lib/udev/rules.d/72-signalrgb.rules

%changelog
* Thu Nov 26 2026 VinVel <vinvel@users.noreply.local> - 2.5.86-7617
- Correct Fedora library dependencies and bridge Tesseract 5.5's SONAME
- Disable empty debugsource generation for prebuilt binaries
- Include the desktop icon sizes from the Debian package
- Repackage the upstream Debian build for Fedora
