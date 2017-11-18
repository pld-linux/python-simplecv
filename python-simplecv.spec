#
# Conditional build:
%bcond_with	tests	# do not perform "make test"

%define		module		SimpleCV
%define		egg_name	SimpleCV
%define		pypi_name	simplecv
Summary:	Open source framework for building computer vision applications
Name:		python-%{pypi_name}
Version:	1.3
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	http://downloads.sourceforge.net/simplecv/SimpleCV-%{version}.tar.gz
# Source0-md5:	3f9688af1ac8663ebfcd672c38268801
Patch0:		test.patch
Patch1:		sample_images_path.patch
Patch2:		test_display.patch
Patch3:		test_cameras.patch
Patch4:		font.patch
Patch5:		shell_import_frontend.patch
URL:		http://simplecv.org/
BuildRequires:	python-flickrapi
BuildRequires:	python-modules
BuildRequires:	python-nose
BuildRequires:	python-numpy
BuildRequires:	python-opencv
BuildRequires:	python-pillow
BuildRequires:	python-pygame
BuildRequires:	python-scipy
BuildRequires:	python-setuptools
BuildRequires:	python-svgwrite
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if 0
Requires:	astloch-fonts
Requires:	carterone-fonts
Requires:	cyreal-wireone-fonts
Requires:	kranky-fonts
Requires:	labelleaurore-fonts
Requires:	monofett-fonts
Requires:	reeniebeanie-fonts
Requires:	shadowsintolight-fonts
Requires:	specialelite-fonts
Requires:	unifrakturmaguntia-fonts
Requires:	vt323-fonts
Requires:	wallpoet-fonts
%endif
Requires:	python-flickrapi
Requires:	python-ipython
Requires:	python-numpy
Requires:	python-opencv
Requires:	python-pillow
Requires:	python-pygame
Requires:	python-scipy
Requires:	python-svgwrite
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SimpleCV is a framework for Open Source Machine Vision, using OpenCV
and the Python programming language.

%prep
%setup -qc
mv SimpleCV .tmp; mv .tmp/* .

# This directory contains: flickrapi (bunble library) and script that do
# queries with a script copied from:
# http://graphics.cs.cmu.edu/projects/im2gps/flickr_code.html
rm -r SimpleCV/MachineLearning/query_imgs/

# This directory contains the bundled fonts.
rm -r SimpleCV/fonts

%patch0
%patch1
%patch2
%patch3
%patch4
%patch5

%build
%py_build

%if %{with tests}
cd SimpleCV/tests
nosetests-%{py_ver}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install
%py_postclean

# Remove test files that relies on cv2.SURF (unfree)
rm SimpleCV/tests/test_stereovision.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.txt LICENSE README.markdown requirements.txt doc/*
%attr(755,root,root) %{_bindir}/simplecv
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
