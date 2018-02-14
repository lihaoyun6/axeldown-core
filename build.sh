#!/bin/bash
echo '创建临时目录...'
rm -rf build
mkdir -p build
cd build
echo '解压axel源码...'
tar -xzvf ../axel-2.5.tar.gz
axel=axel-2.5
patch=../axel-patch
echo '开始修补源码..'
diff $axel/text.c $patch/text.c > $patch/text.c.patch
diff $axel/conf.c $patch/conf.c > $patch/conf.c.patch
patch $axel/text.c $patch/text.c.patch
patch $axel/conf.c $patch/conf.c.patch
cd $axel/
export CFLAGS='-w'
echo '编译'$axel'源码...'
./configure --debug=0 --i18n=0
make
echo '清理临时目录...'
cp axel ../../
cd ../../
rm -rf build
rm -rf axel-patch
rm axel-2.5.tar.gz
rm $0
