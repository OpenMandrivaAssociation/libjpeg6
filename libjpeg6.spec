%define major 62
%define libname %mklibname jpeg %{major}

Summary:	A library for manipulating JPEG image format files
Name:		libjpeg6
Version:	6b
Release:	%mkrel 45
License:	GPL-like
Group:		System/Libraries
URL:		http://www.ijg.org/
Source0:	ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v6b.tar.bz2
# Modified source files for lossless cropping of JPEG files and for
# lossless pasting of one JPEG into another (dropping). In addition a
# bug in the treatment of EXIF data is solved and the EXIF data is
# adjusted according to size/dimension changes caused by rotating and
# cropping operations
Source1:	http://jpegclub.org/droppatch.tar.bz2
# These two allow automatic lossless rotation of JPEG images from a digital
# camera which have orientation markings in the EXIF data. After rotation
# the orientation markings are reset to avoid duplicate rotation when
# applying these programs again.
Source2:	http://jpegclub.org/jpegexiforient.c
Source3:	http://jpegclub.org/exifautotran.txt
Patch0:		libjpeg-6b-arm.patch
Patch1:		libjpeg-ia64-acknowledge.patch
Patch2:		jpeg-6b-c++fixes.patch
# Use autoconf variables to know libdir et al.
Patch3:		jpeg-6b-autoconf-vars.patch
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The libjpeg package contains a shared library of functions for loading,
manipulating and saving JPEG format image files.

Install the libjpeg package if you need to manipulate JPEG files. You
should also install the jpeg-progs package.

%package -n	%{libname}
Summary:	A library for manipulating JPEG image format files
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libjpeg.

%package -n	%{libname}-devel
Summary:	Development tools for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	jpeg6-devel = %{version}-%{release}
Conflicts:	%{mklibname jpeg 7 -d}

%description -n	%{libname}-devel
The libjpeg-devel package includes the header files necessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package -n	%{libname}-static-devel
Summary:	Static libraries for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	jpeg6-static-devel = %{version}-%{release}
Conflicts:	%{mklibname jpeg 7 -d -s}

%description -n %{libname}-static-devel
The libjpeg-devel package includes the static librariesnecessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package -n	jpeg6-progs
Summary:	Programs for manipulating JPEG format image files
Group:		Graphics
Requires:	%{libname} = %{version}-%{release}
Conflicts:	jpeg-progs

%description -n jpeg6-progs
The jpeg-progs package contains simple client programs for accessing 
the libjpeg functions.  Libjpeg client programs include cjpeg, djpeg, 
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into JPEG
format. Djpeg decompresses a JPEG file into a regular image file.  Jpegtran
can perform various useful transformations on JPEG files.  Rdjpgcom displays
any text comments included in a JPEG file.  Wrjpgcom inserts text
comments into a JPEG file.

%prep

%setup -q -n jpeg-6b
%setup -q -T -D -a 1 -n jpeg-6b
rm -f jpegtran
%patch0 -p1 
%patch1 -p1
%patch2 -p1
%patch3 -p1
ln -s /usr/bin/libtool .

cp %{SOURCE2} jpegexiforient.c
cp %{SOURCE3} exifautotran

%build
export CFLAGS="%{optflags}"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared \
    --enable-static \
    --disable-rpath

#cat > have_stdlib.sed <<\EOF
#s/#define HAVE_STDLIB_H/#ifndef HAVE_STDLIB_H\
#&\
#endif/g
#EOF
#sed -f have_stdlib.sed jconfig.h > jconfig.tmp && mv jconfig.tmp jconfig.h
#rm -f have_stdlib.sed
#perl -pi -e 's,hardcode_libdir_flag_spec=",#hardcode_libdir_flag_spec=",;' libtool

%make
%ifnarch armv4l
#FIX MEEE: we know this will fail on arm
LD_LIBRARY_PATH=$PWD make test
%endif

gcc %{optflags} -o jpegexiforient jpegexiforient.c

%install
rm -rf %buildroot
mkdir -p %buildroot/{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man1}

#(neoclust) Provide jpegint.h because it is needed softwares
cp jpegint.h %buildroot%{_includedir}/jpegint.h

%makeinstall mandir=%buildroot/%{_mandir}/man1

install -m 755 jpegexiforient %{buildroot}%{_bindir}
install -m 755 exifautotran %{buildroot}%{_bindir}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %buildroot

%files -n %{libname}
%defattr(-,root,root)
%doc README change.log
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc README usage.doc change.log wizard.doc coderules.doc libjpeg.doc structure.doc example.c
%{_libdir}/*.so
%{_includedir}/*.h
%{_libdir}/*.la

%files -n %{libname}-static-devel
%defattr(-,root,root)
%doc README 
%{_libdir}/*.a

%files -n jpeg6-progs
%defattr(-,root,root)
%doc README change.log
%{_bindir}/*
%{_mandir}/man1/*
