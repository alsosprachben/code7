#!/bin/sh
dir="$(dirname "${0}")"
if [ "${dir}" = . ]
then
	dir="$(pwd -L)/${dir}"
fi
fonts="${XDG_DATA_HOME:-${HOME}/.local/share}/fonts"
mkdir -p "${fonts}"
cp "${dir}/code7.ttf" "${dir}/code7sc.ttf" "${dir}/code7it.ttf" "${dir}/code7w.ttf" "${fonts}/"
confd="${XDG_CONFIG_HOME:-${HOME}/.config}/fontconfig/conf.d"
mkdir -p "${confd}"
cp "${dir}/fontconfig-code7.conf" "${confd}/50-code7.conf"
fc-cache -f "${fonts}"
xset fp+ "${dir}"
xrdb -merge "${dir}/Xresources.code7-2x"
xrdb -merge "${dir}/Xresources.code7-ttf"
xrdb -merge "${dir}/Xresources.dark"
