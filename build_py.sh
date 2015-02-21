#!/bin/bash

function check_su() {

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   return 1
fi

}


function mka() {
    case `uname -s` in
        Darwin)
            make -j `sysctl hw.ncpu|cut -d" " -f2` "$@"
            ;;
        *)
            schedtool -B -n 1 -e ionice -n 1 make -j$(cat /proc/cpuinfo | grep "^processor" | wc -l) "$@"
            ;;
    esac
}


function install_deps() {

[[ $(check_su) ]] && return 1

apt-get install mercurial
apt-get install gcc make libffi-dev pkg-config libz-dev libbz2-dev \
libsqlite3-dev libncurses-dev libexpat1-dev libssl-dev liblzma-dev

}


function build_cpython() {

[[ $(check_su) ]] && return 1

py_versions="\
v3.4.2
v3.3.6
v3.2.6
v2.7.8
v2.7.9
v2.6.9"

WORK_DIR=$(pwd)

cd ${WORK_DIR}
[[ -d "${WORK_DIR}/cpython" ]] || hg clone https://hg.python.org/cpython cpython
cd ${WORK_DIR}/cpython

for p in ${py_versions}
do
  hg update --clean ${p}
  ./configure
  [[ $(make Modules/Setup | grep "Modules/Setup.dist") ]] && cp "Modules/Setup.dist" "Modules/Setup"
  mka
  mka install
  mka clean
done

}


function build_pypy() {

[[ $(check_su) ]] && return 1

pypy_versions="\
release-2.4.0
pypy3-release-2.4.0
"

WORK_DIR=$(pwd)

cd ${WORK_DIR}
[[ -d "${WORK_DIR}/pypy" ]] || hg clone http://bitbucket.org/pypy/pypy pypy
cd ${WORK_DIR}/pypy

pypy_exec=$(which pypy)
[[ ${pypy_exec} ]] || pypy_exec="python"

alias py=${pypy_exec}

for p in ${pypy_versions}
do
  hg update --clean ${p}
  py rpython/bin/rpython -Ojit pypy/goal/targetpypystandalone.py
  [[ $p == *pypy3* ]] && bin="pypy3" || bin="pypy2"
  [[ -f "pypy/goal/pypy-c" ]] && cp "pypy/goal/pypy-c" "/usr/bin/${bin}"
done

}

