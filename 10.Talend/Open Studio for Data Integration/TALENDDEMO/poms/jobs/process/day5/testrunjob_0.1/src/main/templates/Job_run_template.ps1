$fileDir = Split-Path -Parent $MyInvocation.MyCommand.Path
cd $fileDir
java '-Dtalend.component.manager.m2.repository=%cd%/../lib' '-Xms256M' '-Xmx1024M' '-Dfile.encoding=UTF-8' -cp '.;../lib/routines.jar;../lib/crypto-utils.jar;../lib/dom4j-1.6.1.jar;../lib/jxl.jar;../lib/log4j-1.2.17.jar;testrunjob_0_1.jar;testroutine_bis_0_1.jar;' talenddemo.testrunjob_0_1.testRunJob  $args