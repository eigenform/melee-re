Melee includes a lot of assertion strings that we can use to help deduce the
layout of object files. Static analysis tools should be able to resolve
cross-references to these. 

If you look at cross-references in program order, the first and last references
should indicate a range of addresses that we can **assume** should belong to 
the underlying object file.

If that assumption is correct, this should be sufficient to define the layout 
of object files relative to one another, but the addresses themselves don't 
represent the exact boundaries of object files.

Scripting in Ghidra is an easy way to do this, i.e. 

```
from ghidra.program.util import DefinedDataIterator
from ghidra.app.util import XReferenceUtil

ent = {}
for s in DefinedDataIterator.definedStrings(currentProgram):
    if ".c" in s.__str__():
        reflist = XReferenceUtil.getXRefList(s)
        if len(reflist) > 1: 
            base = reflist[0].getOffset()
            tail = reflist[-1].getOffset()
            ent[reflist[0]] = (s.__str__(), base, tail)
		elif len(reflist) == 1:
			base = reflist[0].getOffset()
			ent[reflist[0]] = (s.__str__(), base, base)

for a in sorted(ent):
    print("{:24} {:08x} {:08x}".format(ent[a][0], ent[a][1], ent[a][2]))

```

This yields the following layout:

```
ds "lbvector.c"          8000e23c 8000e2f0
ds "lbshadow.c"          8000ed84 8000f4a4
ds "lbspdisplay.c"       80012254 80012254
ds "lbarq.c"             80014c20 80014c20
ds "lbmemory.c"          80014e5c 800155d8
ds "lbheap.c"            80015cfc 80015cfc
ds "lbfile.c"            8001617c 800169d0
ds "lbarchive.c"         80016a94 80017180
ds "lbdvd.c"             80017834 80018200
ds "lbcardnew.c"         80019c8c 8001a6d0
ds "lbcardgame.c"        8001c8f0 8001ce30
ds "lbsnap.c"            8001d690 8001e0dc
ds "lbmthp.c"            8001e940 8001f494
ds "lbrefract.c"         80022c10 80022c10
ds "lbaudio_ax.c"        80027400 80028568
ds "camera.c"            80029e58 8002f5f8
ds "cmsnap.c"            800315f0 800315f0
ds "player.c"            8003175c 80037090
ds "pltrick.c"           80037b78 80038670
ds "plbonus.c"           800387c8 8003d4c8
ds "plbonuslib.c"        8003e2fc 80040504
ds "mpcoll.c"            80041d34 8004c2c8
ds "mplib.c"             8004d2d4 80058854
ds "mpisland.c"          8005a7d8 8005b24c
ds "eflib.c"             8005bb94 8005c178
ds "efasync.c"           800675e8 80067928
ds "fighter.c"           80068a30 8006d4c4
ds "ftanim.c"            8006dc5c 80070548
ds "ftparts.c"           80073d94 80075fb0
ds "ftcamera.c"          8007636c 8007636c
ds "ftcoll.c"            8007670c 8007bf08
ds "ftcommon.c"          8007cdd0 8007e878
ds "ftdata.c"            800855a8 80085f80
ds "ftlib.c"             800871e4 800877a4
ds "ftwaitanim.c"        8008a900 8008a900
ds "ftpickupitem.c"      800944bc 80094bac
ds "ftdynamics.c"        8009cfc8 8009dcbc
ds "ftcmdscript.c"       800b3e7c 800b4a2c
ds "ftcpuattack.c"       800b5228 800b62e8
ds "ftdemo.c"            800bec54 800bec54
ds "ftmaterial.c"        800bf5e4 800bf9b0
ds "ftcolanimlist.c"     800c0230 800c0380
ds "ftdevice.c"          800c0744 800c0854
ds "ftafterimage.c"      800c2778 800c3078
ds "ftmetal.c"           800c82e0 800c87d4
ds "ftswing.c"           800ccf38 800cd074
ds "ftstarrodswing.c"    800cd964 800cd964
ds "ftlipstickswing.c"   800cdbe4 800cdbe4
ds "ftattacks4combo.c"   800ced80 800ced80
ds "ftchangeparam.c"     800cf5d0 800d1430
ds "ftwalkcommon.c"      800dffbc 800dffbc
ds "ftfoxspecialn.c"     800e6178 800e6274
ds "ftkirby.c"           800ef288 800ef644
ds "ftkirbyspecials.c"   800f5454 800f5454
ds "ftkirbyspecialfox.c" 800fe21c 800fe33c
ds "ftyoshi.c"           8012b7c8 8012b9e0
ds "ftbosslib.c"         8015be1c 8015be1c
ds "gmmain.c"            8015fe88 8015fe88
ds "gmresult.c"          80176abc 8017761c
ds "gmregcommon.c"       8017c094 8017c094
ds "gmregclear.c"        80180454 80180484
ds "gmtoulib.c"          8018f4e0 8018f4e0
ds "gmvsmelee.c"         801a5574 801a5574
ds "gmregenddisp.c"      801a839c 801a930c
ds "gmstaffroll.c"       801aa8f4 801ac5f4
ds "ground.c"            801c04e8 801c475c
ds "grdisplay.c"         801c5c80 801c5c80
ds "grdatfiles.c"        801c6304 801c650c
ds "granime.c"           801c6694 801c87ac
ds "grmaterial.c"        801c8ff4 801c9238
ds "grlib.c"             801c9ad0 801c9ad0
ds "grdynamicattr.c"     801ca140 801ca140
ds "grzakogenerator.c"   801ca6a0 801cae50
ds "grfzerocar.c"        801cb0cc 801cb9dc
ds "grizumi.c"           801cbda4 801cce70
ds "grcastle.c"          801cd58c 801cd58c
ds "grpstadium.c"        801d11b4 801d47e4
ds "grkongo.c"           801d53fc 801d841c
ds "grzebes.c"           801d8614 801dc220
ds "grcorneria.c"        801dd5f0 801e2c94
ds "grstory.c"           801e3190 801e3190
ds "gronett.c"           801e38ac 801e5720
ds "grbigblue.c"         801e5ab4 801ef70c
ds "grmutecity.c"        801efdc8 801f28cc
ds "grfourside.c"        801f2e8c 801f2e8c
ds "grgreatbay.c"        801f43d4 801f6650
ds "gricemt.c"           801f6a44 801fa564
ds "grinishie1.c"        801faa70 801fbfdc
ds "grinishie2.c"        801fcd98 801fcd98
ds "grkraid.c"           801fe180 801fe180
ds "grrcruise.c"         801ff384 802015b4
ds "grshrine.c"          80201dd8 80201dd8
ds "gryorster.c"         802020f4 802020f4
ds "grgarden.c"          80202d30 80202d30
ds "grvenom.c"           80203f68 80206c6c
ds "grtest.c"            80207100 80207100
ds "grkinokoroute.c"     80207604 802080c4
ds "grshrineroute.c"     8020897c 8020a380
ds "grzebesroute.c"      8020b318 8020b608
ds "grbigblueroute.c"    8020ba8c 8020de6c
ds "grfigure1.c"         8020e138 8020e138
ds "grfigure2.c"         8020e3cc 8020e3cc
ds "grfigure3.c"         8020e660 8020e660
ds "groldyoshi.c"        8020e90c 8020e90c
ds "groldkongo.c"        8020f5e8 80210758
ds "groldpupupu.c"       8021096c 80210ed0
ds "grpura.c"            80211ec0 8021265c
ds "grgreens.c"          802135dc 802169e8
ds "grflatzone.c"        80217000 80217000
ds "grpushon.c"          8021849c 80219284
ds "grfigureget.c"       80219684 80219684
ds "grbattle.c"          80219e3c 8021a5a0
ds "grlast.c"            8021a6cc 8021c304
ds "grhomerun.c"         8021c8e4 8021e63c
ds "grheal.c"            8021f0a8 8021f65c
ds "grtmario.c"          8021f99c 8021f99c
ds "grtcaptain.c"        8021fdbc 8021fdbc
ds "grtclink.c"          802200a0 802200a0
ds "grtdonkey.c"         80220384 80220384
ds "grtdrmario.c"        80220668 80220668
ds "grtfalco.c"          80220954 80220954
ds "grtfox.c"            80220ce4 80220ce4
ds "grticeclimber.c"     8022106c 8022106c
ds "grtkirby.c"          802214c0 802214c0
ds "grtkoopa.c"          802217a4 802217a4
ds "grtlink.c"           80221a88 80221a88
ds "grtluigi.c"          80221d6c 80221d6c
ds "grtmars.c"           80222050 80222050
ds "grtmewtwo.c"         8022233c 8022233c
ds "grtness.c"           8022272c 8022272c
ds "grtpeach.c"          80222a10 80222a10
ds "grtpichu.c"          80222cf4 80222cf4
ds "grtpikachu.c"        80222fd8 80222fd8
ds "grtpurin.c"          802232c4 802232c4
ds "grtsamus.c"          802236dc 802236dc
ds "grtseak.c"           802239c0 802239c0
ds "grtyoshi.c"          80223ca4 80223ca4
ds "grtzelda.c"          80223f88 80223f88
ds "grtgamewatch.c"      8022426c 8022426c
ds "grtemblem.c"         80224550 80224550
ds "grtganon.c"          8022483c 8022483c
ds "stage.c"             80224e9c 80225138
ds "dbscreenshot.c"      80228988 80228988
ds "mnmain.c"            80229f00 8022b4c8
ds "mnmainrule.c"        80230fd4 80230fd4
ds "mnruleplus.c"        802333b4 802333b4
ds "mnitemsw.c"          80235270 80235270
ds "mnstagesw.c"         80236d8c 80236d8c
ds "mnname.c"            80238e50 8023a668
ds "mnnamenew.c"         8023d4e4 8023e400
ds "mndiagram.c"         802413d4 802434e0
ds "mndiagram2.c"        80245224 80245224
ds "mndiagram3.c"        802470bc 802470bc
ds "mnvibration.c"       80248f7c 80248f7c
ds "mnsound.c"           80249cb8 80249cb8
ds "mndeflicker.c"       8024a578 8024a578
ds "mnsoundtest.c"       8024bd80 8024bd80
ds "mnlanguage.c"        8024c480 8024c480
ds "mnhyaku.c"           8024cc4c 8024cc4c
ds "mnevent.c"           8024e5e0 8024e5e0
ds "mndatadel.c"         8024ff08 8024ff08
ds "mncount.c"           8025191c 8025191c
ds "mninfo.c"            8025280c 8025280c
ds "mnsnap.c"            80253334 80255d7c
ds "mngallery.c"         802596ec 802597f0
ds "item.c"              80267a78 8026a934
ds "itcoll.c"            8026fa0c 80271798
ds "itmaplib.c"          80275c88 80275c88
ds "itmaterial.c"        80278030 802783d8
ds "itanimlist.c"        80279180 80279180
ds "itzgshell.c"         802df488 802df488
ds "iftime.c"            802f4314 802f45c8
ds "ifstatus.c"          802f6264 802f6290
ds "textlib.c"           803028dc 803028dc
ds "toy.c"               80306ec0 80308d8c
ds "tylist.c"            8031355c 8031482c
ds "tyfigupon.c"         80317574 80317e84
ds "tydisplay.c"         80318fc0 8031b360
ds "dvdfs.c"             80337ad8 80337d6c
ds "OSThread.c"          8034bd14 8034c3b0
ds "Pad.c"               8034de28 8034de28
ds "dobj.c"              8035e188 8035e2f4
ds "tobj.c"              8035e8b4 80361318
ds "tev.c"               80362744 80362b48
ds "mobj.c"              80363230 80363d78
ds "aobj.c"              80364560 803652ec
ds "lobj.c"              80365a58 80367370
ds "cobj.c"              8036853c 8036a788
ds "fobj.c"              8036b200 8036b86c
ds "pobj.c"              8036b9f4 8036e998
ds "jobj.c"              8036efe0 8037363c
ds "displayfunc.c"       8037426c 80374330
ds "initialize.c"        803750f4 8037521c
ds "video.c"             80375b5c 8037630c
ds "mtx.c"               8037a634 8037a6b0
ds "util.c"              8037a928 8037a928
ds "objalloc.c"          8037a998 8037ad74
ds "robj.c"              8037b2fc 8037cd30
ds "id.c"                8037ce94 8037ce94
ds "wobj.c"              8037d1dc 8037d83c
ds "fog.c"               8037d9d0 8037dda0
ds "perf.c"              8037e3bc 8037e3bc
ds "list.c"              8037e47c 8037e64c
ds "memory.c"            8037f21c 8037f21c
ds "shadow.c"            8037f4ac 80380088
ds "bytecode.c"          803806c0 80381b9c
ds "class.c"             80381ca0 80382448
ds "hash.c"              80382b94 80382b94
ds "texp.c"              80382f0c 80385650
ds "texpdag.c"           80385c8c 8038609c
ds "synth.c"             80388364 8038b474
ds "axdriver.c"          8038bb74 8038e808
ds "devcom.c"            8038eb1c 8038f868
ds "gobjproc.c"          8038fd90 8038fdb8
ds "gobjplink.c"         8038fffc 80390370
ds "gobjgxlink.c"        803906ec 80390950
ds "gobjobject.c"        80390aac 80390aac
ds "gobjuserdata.c"      80390bac 80390c1c
ds "debugconsole_main.c" 80397d78 80397d78
ds "particle.c"          8039853c 803985ec
ds "generator.c"         8039dd08 8039dd08
ds "psdisp.c"            803a10f4 803a10f4
ds "sobjlib.c"           803a47e0 803a47e0
ds "sislib.c"            803a57d4 803a6340
```

It seems like most of the related assertions are in the game and HSD libraries.
The layout of other libraries should be easy to sort out by cross-referencing
Melee with existing map files that were shipped with other retail titles.


