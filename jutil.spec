%define section         free
%define gcj_support     1

Name:           jutil
Version:        1.3
Release:        %mkrel 1.1.2
Epoch:          0
Summary:        Parameterized collections library for Java
License:        GPL
Group:          Development/Java
URL:            http://cscott.net/Projects/JUtil
Source0:        http://cscott.net/Projects/JUtil/jutil-latest/jutil-1.3.tar.gz
BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.6
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
JUtil is a fully-parameterized (generic) collections library for
Java. It was originally part of the FLEX project.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__perl} -pi -e 's|<javac|<javac source="1.5" nowarn="true"|g' build*.xml
%{_bindir}/find . -type f -name '*.jar' | xargs -t %{__rm}

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} jar javadoc

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a api/*  %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

#%{__perl} -pi -e 's/\r$//g' 

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
