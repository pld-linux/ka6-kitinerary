#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.05.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kitinerary
Summary:	KDE Itinerary - digital travel assistent
Summary(pl.UTF-8):	KDE Itinerary - cyfrowy asystent podróży
Name:		ka6-%{kaname}
Version:	24.05.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	644238240663000a3f231e4b988e8408
Patch0:		poppler-0.82.patch
Patch1:		poppler-0.83.patch
URL:		https://community.kde.org/KDE_PIM/KDE_Itinerary
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Network-devel >= 5.11.1
BuildRequires:	Qt6Qml-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	abseil-cpp-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-kmime-devel >= %{kdeappsver}
BuildRequires:	ka6-kpkpass-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf6-kcontacts-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	libphonenumber-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libxml2-devel >= 2
BuildRequires:	ninja
BuildRequires:	poppler-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	zxing-cpp-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kitinerary is a library which provides a data model and a system to
extract information from travel reservations.

%description -l pl.UTF-8
Kitinerary to biblioteka dostarczająca model danych oraz system do
wydobywania informacji z rezerwacji podróżnych.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKPim6Itinerary.so.*.*
%ghost %{_libdir}/libKPim6Itinerary.so.6
%attr(755,root,root) %{_prefix}/libexec/kf6/kitinerary-extractor
%{_datadir}/mime/packages/application-vnd-kde-itinerary.xml
%{_datadir}/qlogging-categories6/org_kde_kitinerary.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/KItinerary
%{_includedir}/KPim6/kitinerary
%{_includedir}/KPim6/kitinerary_version.h
%{_libdir}/cmake/KPim6Itinerary
%{_libdir}/libKPim6Itinerary.so
