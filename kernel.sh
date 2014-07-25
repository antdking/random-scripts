#!/bin/bash

workspace=".kernel_workspace"

rm -rf "${workspace}"
mkdir -p "${workspace}"

domain="http://kernel.ubuntu.com/~kernel-ppa/mainline/daily/current/"

page=$(curl -s "${domain}")
[[ $? != 0 ]] && echo "failed to fetch page" && exit 1

kernel_image=${domain}$(echo ${page} | grep -r "href=\"linux-image-3.*-generic_.*_amd64.deb\"" -o | cut -d '"' -f 2)
amd64_headers=${domain}$(echo ${page} | grep -r "href=\"linux-headers-3.*-generic_.*_amd64.deb\"" -o | cut -d '"' -f 2)
all_headers=${domain}$(echo ${page} | grep -r "href=\"linux-headers-3.*_all.deb\"" -o | cut -d '"' -f 2)

extra="$(echo ${page} | grep -r "href=\"linux-image-extra-3.*-generic_.*_amd64.deb\"" -o | cut -d '"' -f 2)"

echo "${kernel_image}"
echo "${amd64_headers}"
echo "${all_headers}"

[[ $extra ]] && extra="${domain}${extra}" && echo "${extra}"

cd "${workspace}"

curl "${kernel_image}" > "kernel_image.deb"
curl "${all_headers}" > "all_headers.deb"
curl "${amd64_headers}" > "amd64_headers.deb"
[[ $extra ]] && curl "${extra}" > "extra.deb"

dpkg -i *.deb
