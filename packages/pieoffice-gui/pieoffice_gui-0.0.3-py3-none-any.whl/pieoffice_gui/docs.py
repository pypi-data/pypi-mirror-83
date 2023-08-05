
doc_pie = """ PIE Rules

The transliteration scheme is close to the Harvard-Kyoto for Sanskrit. Long vowels are marked with upper-case, accute with /, vocalic ressonants with upper-case (M, N). The aspirates and bilabials are marked respectively by h and w justaposed."""

doc_polygreek = """ Polytonic Greek rules

The transliteration scheme follows the TLG Betacode Manual, using the implementation of Matias Grioni's betacode module. This script only implements the terminal based application and a couple more
letters:

    s4    Ϡ | *s4     ϡ | s5       ϻ | *s5       Ϻ
"""

doc_linarb = """ Linear B rules

Glyphs with known syllabic values should be written in lower-case, syllabically
and numbered if +2. Glyphs with known logographic values should be written in
upper-case. The only exception for said rule are the gendered logograms, which
should be followed without space by a f or m. Glyphs with unknown value should
be written with an asterisk followed by the number (2 or 3 digits).

This conversion scheme supports Aegean numbers and measurements.

"""

doc_cypriot = """ Cypriot Syllabary rules

The typing scheme is as follows:

-----------------------------------------------------------------------------
| a       𐠀   |   e       𐠁   |   i      𐠂   |    o       𐠃  |   u       𐠄 |
| wa    𐠲   |   we    𐠳   |   wi   𐠴   |    wo    𐠵  |                |
| za     𐠼   |                  |                |    zo      𐠿  |                |
| ja      𐠅    |                  |                |    jo     𐠈  |                |
| ka     𐠊   |   ke      𐠋   |   ki    𐠌   |    ko     𐠍  |   ku     𐠎 |
| la      𐠏   |   le       𐠐   |   li     𐠑   |    lo       𐠒  |   lu      𐠓 |
| ma   𐠔   |   me    𐠕  |   mi   𐠖  |    mo   𐠗  |   mu   𐠘 |
| na     𐠙   |   ne     𐠚   |   ni    𐠛   |    no     𐠜  |   nu     𐠝 |
| pa     𐠞   |   pe      𐠟   |   pi   𐠠   |    po     𐠡   |   pu     𐠢 |
| ra      𐠣   |   re      𐠤  |   ri    𐠥   |    ro      𐠦  |   ru     𐠧  |
| sa      𐠨   |   se     𐠩   |   si    𐠪  |    so      𐠫 |   su     𐠬  |
| ta       𐠭   |   te     𐠮   |   ti     𐠯  |    to       𐠰 |   tu      𐠱  |
| ksa    𐠷   |   kse  𐠸   |                |                 |                  |
-----------------------------------------------------------------------------


"""

doc_oscan = """ Oscan rules

    -------------------------------------------------------------
    | a 𐌀 | b 𐌁 | g,k 𐌂 |  d 𐌃	| e 𐌄 | v 𐌅 | z 𐌆  |
    | h 𐌇 | i 𐌉  | l      𐌋 | m 𐌌	| n 𐌍 | p 𐌐 | ś 𐌑 |
    | r 𐌓  | s 𐌔 | t     𐌕 |  u 𐌖	| f 𐌚  | ú 𐌞 | í 𐌝  |
    -------------------------------------------------------------

"""

doc_luwian = """ Hieroglyphic Luwian rules

Glyphs with known syllabic values should be written in lower-case, syllabically
and with the proper diacritic or numbered if +4. Glyphs with known logographic 
values should be written in upper-case. Variants of known glyphs should be
followed by one or more dots (.), generally the undotted variant is the more
frequent one.  Glyphs with unknown value should be written with an asterisk 
followed by the number (3 digits, including the 0).

Included graphic marks:
    "WD" for "𔖵"
    "WE" for "𔗷"
    "."  for "𔖲"
    "<"  for "𔗎"
    ">"  for "𔗏"

"""

doc_lycian = """ Lycian rules

    -------------------------------------------
    | a  𐊀 | b  𐊂 | g  𐊄 | d  𐊅 | i  𐊆 | w  𐊇 |
    | z  𐊈 | h  𐊛 | th 𐊉 | j  𐊊 | y  𐊊 | k  𐊋 |
    | l  𐊍 | m  𐊎 | n  𐊏 | u  𐊒 | p  𐊓 | k  𐊔 |
    | r  𐊕 | s  𐊖 | t  𐊗 | e  𐊁 | ã  𐊙 | ẽ  𐊚 |
    | M  𐊐 | N  𐊑 | T  𐊘 | q  𐊌 | B  𐊃 | x  𐊜 |
    -------------------------------------------

"""

doc_lydian = """ Lydian rules

    -----------------------------------------------------------------------
    | a     𐤠 | b,p   𐤡 | g     𐤢 | d     𐤣 | e     𐤤 | v,w   𐤥 | i     𐤦 |
    | y     𐤧 | k     𐤨 | l     𐤩 | m     𐤪 | n     𐤫 | o     𐤬 | r     𐤭 |
    | S,ś   𐤮 | t     𐤯 | u     𐤰 | f     𐤱 | q     𐤲 | s,sh  𐤳 | T     𐤴 |
    | ã     𐤵 | A     𐤵 | ẽ     𐤶 | E     𐤶 | L     𐤷 | N     𐤸 | c     𐤹 |
    | .      |         |         |         |         |         |         |
    -----------------------------------------------------------------------

"""

doc_carian = """ Carian rules

    -------------------------------------------------------------------
    | a      𐊠 | b      𐊡 | d      𐊢 | l      𐊣 | y      𐊤 | y2     𐋐 |
    | r      𐊥 | L      𐊦 | L2     𐋎 | A2     𐊧 | q      𐊨 | b      𐊩 |
    | m      𐊪 | o      𐊫 | D2     𐊬 | t      𐊭 | sh     𐊮 | sh2    𐊯 |
    | s      𐊰 | 18     𐊱 | u      𐊲 | N      𐊳 | c      𐊴 | n      𐊵 |
    | T2     𐊶 | p      𐊷 | 's,ś   𐊸 | i      𐊹 | e      𐊺 | ý,'y   𐊻 |
    | k      𐊼 | k2     𐊽 | dh     𐊾 | w      𐊿 | G      𐋀 | G2     𐋁 |
    | z2     𐋂 | z      𐋃 | ng     𐋄 | j      𐋅 | 39     𐋆 | T      𐋇 |
    | y3     𐋈 | r2     𐋉 | mb     𐋊 | mb2    𐋋 | mb3    𐋌 | mb4    𐋍 |
    | e2     𐋏 |                                                      |
    -------------------------------------------------------------------
"""

doc_armenian = """ Armenian rules

    ----------------------------------------------------------------
    | a 	 ա | b	    բ | g	 գ | d	    դ | e	 ե |
    | ye	 ե | z      զ | ee	 է | e'     ը | t'	 թ | 
    | zh	 ժ | i	    ի | l	 լ | x	    խ | c	 ծ | 
    | k 	 կ | h      հ | j	 ձ | g.     ղ | l.	 ղ |
    | ch.	 ճ | m      մ | y	 յ | n      ն | sh	 շ |
    | o 	 ո | ch     չ | p	 պ | jh     ջ | r.	 ռ | 
    | s	         ս | v	    վ | t        տ | r	    ր | c'	 ց |
    | w          ւ | p'     փ | k'       ք | o'     օ | f 	 ֆ |
    | u	         ու| ev     և | ?	 ՞ | .      ։ | .'	 ՝ |
    | ;          ՟ | ;'     ՛ | !	 ՜ | ``     « | ''	 » |
    ----------------------------------------------------------------
"""

doc_gothic = """ Gothic rules

    -------------------------------------------------------------------------------------
    | a     𐌰  | b     𐌱   | g     𐌲 | d     𐌳   | e     𐌴  | q     𐌵   | z     𐌶  |
    | h     𐌷  | th    𐌸 | i     𐌹    | k     𐌺   | l     𐌻   | m     𐌼 | n     𐌽 |
    | j     𐌾   | u     𐌿   | p     𐍀 | q'    𐍁   | r     𐍂  | s     𐍃    | t     𐍄  |
    | w     𐍅 | f     𐍆    | x     𐍇 | hw    𐍈 | o     𐍉 | z'    𐍊    |            |
    -------------------------------------------------------------------------------------
"""

doc_avestan = """ Avestan rules

--------------------------------------------------------------------------
| a   a   𐬀  | A   ā   𐬁  ||  á   å  𐬂  | Á ā̊  𐬃  || ã  ą  𐬄 | ãã  ą̇   𐬅 |
| æ   ə   𐬆  | Æ   ə̄   𐬇  ||  e   e  𐬈  | E ē  𐬉  || o  o  𐬊 | O   ō   𐬋 |
| i   i   𐬌  | I   ī   𐬍  ||  u   u  𐬎  | U ū  𐬏  || k  k  𐬐 | x   x   𐬑 |
| X   x́   𐬒  | xw  x   𐬓  ||  g   g  𐬔  | G ġ  𐬕  || gh γ  𐬖 | c   č   𐬗 |
| j   ǰ   𐬘  | t   t   𐬙  ||  th  ϑ  𐬚  | d d  𐬛  || dh δ  𐬜 | T   t̰   𐬝 |
| p   p   𐬞  | f   f   𐬟  ||  b   b  𐬠  | B β  𐬡  || ng ŋ  𐬢 | ngh ŋ́   𐬣 |
| ngw ŋ   𐬤  | n   n   𐬥  ||  ñ   ń  𐬦  | N ṇ  𐬧  || m  m  𐬨 | M   m̨   𐬩 |
| Y   ẏ   𐬪  | y   y   𐬫  ||  v   v  𐬬  | r r  𐬭  || s  s  𐬯 | z   z   𐬰 |
| sh  š   𐬱  | zh  ž   𐬲  ||  shy š́  𐬳  | S ṣ̌  𐬴  || h  h  𐬵 |           |
--------------------------------------------------------------------------
"""

doc_oldpersian = """ Old Persian Cuneiform rules

    -----------------------------------------------------------------
    | a    𐎠 | i    𐎡 | u    𐎢 | k    𐎣 | ku   𐎤 | x    𐎧 | xi   𐎧  |
    | xu   𐎧 | g    𐎥 | gu   𐎦 | c    𐎨 | ç    𐏂 | j    𐎩 | ji   𐎪  |
    | t    𐎫 | ti   𐎫 | tu   𐎬 | th   𐎰 | d    𐎭 | di   𐎮 | du   𐎯  |
    | p    𐎱 | f    𐎳 | b    𐎲 | n    𐎴 | ni   𐎴 | nu   𐎵 | m    𐎶  |
    | mi   𐎷 | mu   𐎸 | y    𐎹 | v    𐎺 | vi   𐎻 | r    𐎼 | ri   𐎽  |
    | l    𐎾 | s    𐎿 | z    𐏀 | š    𐏁 | sh   𐏁 | h    𐏃           |
    -----------------------------------------------------------------

    ----------------------------------------------------
    | ahuramazda1  𐏈 | ahuramazda2  𐏉 | ahuramazda3 𐏊  |
    | xshayathia   𐏋 | dahyaus1     𐏌 | dahyaus2    𐏌  |
    | baga         𐏎 | bumis        𐏏 |                |
    ----------------------------------------------------

"""

doc_ved = """ Use the Harvard-Kyoto standard.


    - anudāttaḥ:
        > anudAttaH - a=
        + अनुदात्तः - अ॒
    - svaritaḥ:
        > svaritaH - a+
        + स्वरितः - अ॑

"""

doc_ogham = """ Ogham rules

    | b           ᚁ | l           ᚂ | w           ᚃ | s           ᚄ 
    | n           ᚅ | j           ᚆ | h           ᚆ | d           ᚇ 
    | t           ᚈ | k           ᚉ | kw          ᚊ | c           ᚉ 
    | cw          ᚊ | m           ᚋ | g           ᚌ | gw          ᚍ 
    | S           ᚎ | r           ᚏ | a           ᚐ | o           ᚑ 
    | u           ᚒ | e           ᚓ | i           ᚔ | ,ear,       ᚕ 
    | ,or,        ᚖ | ,uilleann,  ᚗ | ,ifin,      ᚘ | ,eam,       ᚙ 
    | ,peith,     ᚚ | >           ᚛ | <           ᚜

"""

