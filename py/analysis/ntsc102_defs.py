# The SSBM Data sheet was the seed for many aspects of this file.
# See this SmashBoards thread for a link and more resources:
#
#   https://smashboards.com/threads/assembly-guides-resources-q-a.397941/
#

from enum import Enum
from ramdump_util import *

# -----------------------------------------------------------------------------
# Character relevant IDs

class charExternal(Enum):
	CaptainFalcon		= 0x00
	DonkeyKong		= 0x01
	Fox			= 0x02
	MrGameNWatch		= 0x03
	Kirby			= 0x04
	Bowser			= 0x05
	Link			= 0x06
	Luigi			= 0x07
	Mario			= 0x08
	Marth			= 0x09
	Mewtwo			= 0x0A
	Ness			= 0x0B
	Peach			= 0x0C
	Pikachu			= 0x0D
	IceClimbers		= 0x0E
	Jigglypuff		= 0x0F
	Samus			= 0x10
	Yoshi			= 0x11
	Zelda			= 0x12
	Sheik			= 0x13
	Falco			= 0x14
	YoungLink		= 0x15
	DrMario			= 0x16
	Roy			= 0x17
	Pichu			= 0x18
	Ganondorf		= 0x19
	MasterHand		= 0x1A
	WireframeMale		= 0x1B
	WireframeFemale		= 0x1C
	GigaBoswer		= 0x1D
	CrazyHand		= 0x1E
	Sandbag			= 0x1F
	Popo			= 0x20
	Null			= 0x21   

class charInternal(Enum):
	Mario			= 0x00
	Fox                    	= 0x01
	CaptainFalcon         	= 0x02
	DonkeyKong            	= 0x03
	Kirby                  	= 0x04
	Bowser                 	= 0x05
	Link                   	= 0x06
	Sheik                  	= 0x07
	Ness                   	= 0x08
	Peach                  	= 0x09
	Popo                   	= 0x0A
	Nana                   	= 0x0B
	Pikachu                	= 0x0C
	Samus                  	= 0x0D
	Yoshi                  	= 0x0E
	Jigglypuff             	= 0x0F
	Mewtwo                 	= 0x10
	Luigi                  	= 0x11
	Marth                  	= 0x12
	Zelda                  	= 0x13
	YoungLink             	= 0x14
	DrMario              	= 0x15
	Falco                  	= 0x16
	Pichu                  	= 0x17
	MrGameNWatch       	= 0x18
	Ganondorf              	= 0x19
	Roy                    	= 0x1A
	MasterHand            	= 0x1B
	CrazyHand             	= 0x1C
	WireframeMale   	= 0x1D
	WireframeFemale		= 0x1E
	GigaBowser            	= 0x1F
	Sandbag                 = 0x20

# -----------------------------------------------------------------------------
# Stage relevant IDs

class stageExternal(Enum):
    # Normal (VS)
    VSFountain          = 0x002   # Fountain of Dreams (Izumi)
    VSStadium           = 0x003   # Pokémon Stadium (Pstadium)
    VSCastle            = 0x004   # Princess Peach's Castle (Castle)
    VSKongoJungle	= 0x005   # Kongo Jungle (Kongo)
    VSBrinstar          = 0x006   # Brinstar (Zebes)
    VSCorneria          = 0x007   # Corneria
    VSYoshiStory	= 0x008   # Yoshi's Story (Story)
    VSOnett		= 0x009   # Onett
    VSMuteCity	        = 0x00a   # Mute City
    VSRainbowCruise	= 0x00b   # Rainbow Cruise (RCruise)
    VSJungleJapes	= 0x00c   # Jungle Japes (Garden)
    VSGreatBay          = 0x00d   # Great Bay
    VSTemple            = 0x00e   # Hyrule Temple (Shrine)
    VSDepths            = 0x00f   # Brinstar Depths (Kraid)
    VSYoshiIsland	= 0x010   # Yoshi's Island (Yoster)
    VSGreens            = 0x011   # Green Greens (Greens)
    VSFourside          = 0x012   # Fourside
    VSMK1		= 0x013   # Mushroom Kingdom I (Inishie1)
    VSMK2		= 0x014   # Mushroom Kingdom II (Inishie2)
    VSAkanei	        = 0x015   # Akaneia (Deleted Stage)
    VSVenom		= 0x016   # Venom
    VSPokeFloats	= 0x017   # Poké Floats (Pura)
    VSBigBlue           = 0x018   # Big Blue
    VSIcemnt            = 0x019   # Icicle Mountain (Icemt)
    VSIcetop            = 0x01a   # Icetop
    VSFlatZone          = 0x01b   # Flat Zone
    VSDreamLand64	= 0x01c   # Dream Land N64 (old ppp)
    VSYoshiIsland64	= 0x01d   # Yoshi's Island N64 (old yosh)
    VSKongo64	        = 0x01e   # Kongo Jungle N64 (old kong)
    VSBattlefield	= 0x01f   # Battlefield (battle)
    VSFinalDest	        = 0x020   # Final Destination (last)

    # Target Tests
    TargetMario		= 0x021   # Target Test   # Mario (TMario)
    TargetCFalcon	= 0x022   # Target Test   # C. Falcon (TCaptain)
    TargetYL		= 0x023   # Target Test   # Young Link (TClink)
    TargetDK		= 0x024   # Target Test   # Donkey Kong (TDonkey)
    TargetDrMario	= 0x025   # Target Test   # Dr. Mario (TDrmario)
    TargetFalco		= 0x026   # Target Test   # Falco (TFalco)
    TargetFox		= 0x027   # Target Test   # Fox (TFox)
    TargetICs		= 0x028   # Target Test   # Ice Climbers (TIceclim)
    TargetKirby		= 0x029   # Target Test   # Kirby (TKirby)
    TargetBowser	= 0x02a   # Target Test   # Bowser (TKoopa)
    TargetLink		= 0x02b   # Target Test   # Link (TLink)
    TargetLuigi		= 0x02c   # Target Test   # Luigi (TLuigi)
    TargetMarth		= 0x02d   # Target Test   # Marth (TMars)
    TargetMewtwo	= 0x02e   # Target Test   # Mewtwo (TMewtwo)
    TargetNess		= 0x02f   # Target Test   # Ness (TNess)
    TargetPeach		= 0x030   # Target Test   # Peach (TPeach)
    TargetPichu		= 0x031   # Target Test   # Pichu (TPichu)
    TargetPikachu	= 0x032   # Target Test   # Pikachu (TPikachu)
    TargetJigglypuff	= 0x033   # Target Test   # Jigglypuff (TPurin)
    TargetSamus		= 0x034   # Target Test   # Samus (TSamus)
    TargetSheik		= 0x035   # Target Test   # Sheik (TSeak)
    TargetYoshi		= 0x036   # Target Test   # Yoshi (TYoshi
    TargetZelda		= 0x037   # Target Test   # Zelda (TZelda)
    TargetGnW		= 0x038   # Target Test   # Mr. Game & Watch (TGamewat)
    TargetRoy		= 0x039   # Target Test   # Roy (TEmblem)
    TargetGanon		= 0x03a   # Target Test   # Ganondorf (TGanon)

    # Adventure Mode
    AdventureKinoko		= 0x03b   # 1  #1  Kinoko (Mushroom Kingdom Adventure)
    AdventureCastle		= 0x03c   # 1  #2  Castle (vs Peach & Mario [or luigi])
    AdventureKongo		= 0x03d   # 2  #1  Kongo (vs 2 mini Donkey Kongs)
    AdventureGarden		= 0x03e   # 2  #2  Garden (vs Donkey Kong)
    AdventureMeiktu		= 0x03f   # 3  #1  Meiktu (Zelda Adventure[Underground Maze])
    AdventureShrine		= 0x040   # 3  #2  Shrine (vs Zelda)
    AdventureZebes		= 0x041   # 4  #1  Zebes (vs Samus)
    AdventureDassyut		= 0x042   # 4  #2  Dassyut (Escape from Brinstar Adventure)
    AdventureGreens		= 0x043   # 5  #1  Greens (vs Kirby)
    AdventureGreensTeam		= 0x044   # 5  #2  Greens (vs Kirby Team)
    AdventureGreensGiant	= 0x045   # 5  #3  Greens (classic Kirby music) (vs Giant Kirby)
    AdventureCorneria		= 0x046   # 6  #1  Corneria (vs Fox [or Falco])
    AdventureCorneriaArwing	= 0x047   # 6  #2  Corneria (vs Fox [or Falco] with massive arwing attack)
    AdventureStadiumTeam	= 0x048   # 7  #1  Pokémon Stadium (vs Pikachu Team
    AdventureBRoute		= 0x049   # 8  #1  B Route (F  #Zero Adventure[F  #Zero Grand Prix])
    AdventureMuteCity		= 0x04a   # 8  #2  Mute City (vs Captain Falcon)
    AdventureOnett		= 0x04b   # 9  #1  Onett (vs Ness x3
    AdventureIcemt		= 0x04c   # 10  #1 Icemt (Icicle Mountain Adventure)
    AdventureIcetop		= 0x04d   # 10  #2 Icetop (vs Ice Climbers x2)
    AdventureBattlefieldWire	= 0x04e   # 11  #1 Battle (vs Fighting Wireframe team
    AdventureBattleMetal	= 0x04f   # 11  #2 Battle (vs Metal Mario [& Metal Luigi if unlocked])
    AdventureLastBowser		= 0x050   # 12  #1 Last (vs Bowser)
    AdventureLastGiga		= 0x051   # 12  #2 Last (vs Giga Bowser)

    # Bonus Stages
    BonusRaceToFinish	        = 0x052   # Takisusume (Race to the Finish Classic)
    BonusTrophies		= 0x053   # Grab the Trophies (figureget)
    BonusHomerun		= 0x054   # Homerun Contest (homerun)
    BonusAdventureHeal	        = 0x055   # Heal (All-Star's Stage Inbetween Matches)

    # Classic Mode
    ClassicOneCastleMario	= 0x056   # Princess Peach's Castle (vs Mario)
    ClassicOneCruiseMario	= 0x057   # Rainbow Cruise (vs Mario)
    ClassicOneKongoDK		= 0x058   # Kongo Jungle (vs Donkey Kong)
    ClassicOneJungleDK		= 0x059   # Jungle Japes  (vs Donkey Kong)
    ClassicOneBayLink		= 0x05a   # Great Bay (vs Link)
    ClassicOneTempleLink	= 0x05b   # Temple (vs Link)
    ClassicOneBrinstarSamus	= 0x05c   # Brinstar (vs Samus)
    ClassicOneDepthsSamus	= 0x05d   # Brinstar Depths (vs Samus)
    ClassicOneStoryYoshi	= 0x05e   # Yoshi's Story (vs Yoshi)
    ClassicOneIslandYoshi	= 0x05f   # Yoshi's Island (vs Yoshi)
    ClassicOneFountainKirby	= 0x060   # Fountain of Dreams (vs Kirby)
    ClassicOneGreensKirby	= 0x061   # Green Greens (vs Kirby)
    ClassicOneCorneriaFox	= 0x062   # Corneria (vs Fox)
    ClassicOneVenomFox		= 0x063   # Venom (vs Fox)
    ClassicOneStadiumPika	= 0x064   # Pokémon Stadium (Only Pokeballs)(vs Pikachu)
    ClassicOneMK1Luigi		= 0x065   # Mushroom Kingdom I (vs Luigi)
    ClassicOneMK2Luigi		= 0x066   # Mushroom Kingdom II (vs Luigi)
    ClassicOneMuteCityFalcon	= 0x067   # Mute City (vs Captain Falcon)
    ClassicOneBigBlueFalcon	= 0x068   # Big Blue (vs Captain Falcon)
    ClassicOneOnettNess		= 0x069   # Onett (vs Ness)
    ClassicOneFoursideNess	= 0x06a   # Fourside (vs Ness)
    ClassicOneStadiumJiggs	= 0x06b   # Pokémon Stadium (vs Jigglypuff)
    ClassicOneCastleBowser	= 0x06c   # Princess Peach's Castle (vs Bowser)
    ClassicOneBFBowser		= 0x06d   # Battlefield (vs Bowser)
    ClassicOneCastlePeach	= 0x06e   # Princess Peach's Castle (vs Peach)
    ClassicOneMK2Peach		= 0x06f   # Mushroom Kingdom II (vs Peach)
    ClassicOneTempleZelda	= 0x070   # Temple (vs Zelda)
    ClassicOneBayMarth		= 0x071   # Great Bay (vs Marth)
    ClassicOneFDMewtwo		= 0x072   # Final Destination (vs Mewtwo)
    ClassicOneStadiumMewtwo	= 0x073   # Pokémon Stadium (vs Mewtwo)
    ClassicOneIcemntICs		= 0x074   # Icicle Mountain (vs Ice Climbers)
    ClassicOneIcemnt2ICs	= 0x075   # Icicle Mountain (vs Ice Climbers)
    ClassicOneMK1DrMario	= 0x076   # Mushroom Kingdom I (Dr. Mario Music) (vs Dr. Mario)
    ClassicOneBayYLink		= 0x077   # Great Bay (vs Young Link)
    ClassicOneTempleYLink	= 0x078   # Temple (vs Young Link)
    ClassicOneCorneriaFalco	= 0x079   # Corneria (vs Falco)
    ClassicOneVenomFalco	= 0x07a   # Venom (vs Falco)
    ClassicOneBayUnused		= 0x07b   # Great Bay (Unused)
    ClassicOneStadiumPichu	= 0x07c   # Pokémon Stadium (Pichu)

    # Classic Mode
    ClassicTwoBFMario		= 0x07d   # Battlefield (Plays Mario Theme) (vs Team Mario & Bowser)
    ClassicTwoMK2Mario		= 0x07e   # Mushroom Kingdom II (vs Team Mario & Peach)
    ClassicTwoKongoDK		= 0x07f   # Kongo Jungle (vs Team DK & Fox)
    ClassicTwoTempleLink	= 0x080   # Temple (vs Team Link & Zelda)
    ClassicTwoBayLink		= 0x081   # Great Bay (vs Team Link & Young Link)
    ClassicTwoMK1Link		= 0x082   # Mushroom Kingdom I (vs Team Link & Luigi)
    ClassicTwoBayMarth		= 0x083   # Great Bay (Saria's Song) (vs Team Marth & Link)
    ClassicTwoBigBlueSamus	= 0x084   # Big Blue (vs Team Samus & Captain Falcon)
    ClassicTwoBrinstarSamus	= 0x085   # Brinstar (vs Team Samus & Fox)
    ClassicTwoStoryYoshi	= 0x086   # Yoshi's Story (vs Team Yoshi & Luigi)
    ClassicTwoIslandYoshi	= 0x087   # Yoshi's Island (vs Team Yoshi & Ness)
    ClassicTwoGreensKirby	= 0x088   # Green Greens (vs Team Kirby & Pikachu)
    ClassicTwoFountainKirby	= 0x089   # Fountain of Dreams (vs Team Kirby & Pichu)
    ClassicTwoGreensKirby2	= 0x08a   # Green Greens (vs Team Kirby & Jigglypuff)
    ClassicTwoIcemntKirby	= 0x08b   # Icicle Mountain (vs Team Kirby & Ice Climbers)
    ClassicTwoCorneriaFox	= 0x08c   # Corneria (vs Team Fox & Falco)
    ClassicTwoMuteCityFox	= 0x08d   # Mute City (vs Team Fox & Captain Falcon)
    ClassicTwoStadiumPika	= 0x08e   # Pokémon Stadium (vs Team Pikachu & Pichu)
    ClassicTwoStadiumPika2	= 0x08f   # Pokémon Stadium (vs Team Pikachu & Jigglypuff)
    ClassicTwoMK1Luigi		= 0x090   # Mushroom Kingdom I (vs Team Luigi & Dr. Mario)
    ClassicTwoOnettNess		= 0x091   # Onett (alt music) (vs Team Ness & Peach)
    ClassicTwoFoursideNess	= 0x092   # Fourside (vs Team Ness & Mewtwo)
    ClassicTwoBigBlueFalcon	= 0x093   # Big Blue (mRider song) (vs Team Captain Falcon & Falco)
    ClassicTwoBFBowser		= 0x094   # Battlefield (vs Team Bowser & Mewtwo)
    ClassicTwoBFBowser2		= 0x095   # Battlefield (vs Team Bowser & Peach)
    ClassicTwoBFBowser3		= 0x096   # Battlefield (vs Team Bowser & Zelda)
    ClassicTwoTemplePeach	= 0x097   # Temple (vs Team Peach & Zelda)
    ClassicTwoBayZelda		= 0x098   # Great Bay (Saria's Song) (vs Team Zelda & Young Link)
    ClassicTwoTempleZelda	= 0x099   # Temple (Emblem) (vs Team Zelda & Marth)
    ClassicTwoBayUnused		= 0x09a   # Great Bay (Unused)

    # Classic Mode
    ClassicGiantMario           = 0x09b   # Princess Peach's Castle (vs Giant Mario)
    ClassicGiantDK              = 0x09c   # Kongo Jungle (vs Giant DK)
    ClassicGiantLink            = 0x09d   # Great Bay (vs vs Giant Link)
    ClassicGiantYoshi           = 0x09e   # Yoshi's Story (vs Giant Yoshi)
    ClassicGiantLuigi           = 0x09f   # Mushroom Kingdom II (vs Giant Luigi)
    ClassicGiantFalcon          = 0x0a0   # Mute City (vs Giant Captain Falcon)
    ClassicGiantJiggs           = 0x0a1   # Pokémon Stadium (vs Giant Jigglypuff)
    ClassicGiantBowser          = 0x0a2   # Fountain of Dreams (vs Giant Bowser)
    ClassicGiantDrMario         = 0x0a3   # Mushroom Kingdom I (vs Giant Dr. Mario)
    ClassicGiantLinkTemple	= 0x0a4   # Temple (vs Giant Young Link)

    # Classic Mode
    ClassicTeamMario	        = 0x0a5   # Rainbow Cruise (vs Team Mario)
    ClassicTeamDK		= 0x0a6   # Jungle Japes (vs Team Donkey Kong)
    ClassicTeamKirby	        = 0x0a7   # Fountain of Dreams (vs Team Kirby)
    ClassicTeamLuigi	        = 0x0a8   # Mushroom Kingdom II (vs Team Luigi)
    ClassicTeamNess		= 0x0a9   # Onett (vs Team Ness)
    ClassicTeamJiggs            = 0x0aa   # Pokémon Stadium (vs Team Jigglypuff)
    ClassicTeamUnused           = 0x0ab   # Icicle Mountain (Unused)
    ClassicTeamPichu            = 0x0ac   # Pokémon Stadium (vs Team Pichu)
    ClassicTeamGnW		= 0x0ad   # Flat Zone (vs Team Game & Watch)
    ClassicTeamFalcon	        = 0x0ae   # Mute City (vs Team Captain Falcon)

    # Classic Mode
    ClassicFinalMetal	        = 0x0af   # Battlefield (No items) (vs Metal Character)
    ClassicFinalMasterHand	= 0x0b0   # Final Destination (No items) (vs Master Hand)

    # All-Star Mode
    AllStarMario    = 0x0b1   # Rainbow Cruise (vs Mario)
    AllStarDK       = 0x0b2   # Kongo Jungle (vs Donkey Kong)
    AllStarLink     = 0x0b3   # Great Bay (vs Link)
    AllStarSamus    = 0x0b4   # Brinstar (vs Samus)
    AllStarYoshi    = 0x0b5   # Yoshi's Story (vs Yoshi)
    AllStarKirby    = 0x0b6   # Green Greens (vs Kirby)
    AllStarFox      = 0x0b7   # Corneria (vs Fox)
    AllStarPika     = 0x0b8   # Pokémon Stadium (vs Pikachu)
    AllStarLuigi    = 0x0b9   # Mushroom Kingdom I (vs Luigi)
    AllStarFalcon   = 0x0ba   # Mute City (vs Captain Falcon)
    AllStarNess     = 0x0bb   # Onett (vs Ness)
    AllStarJiggs    = 0x0bc   # Poké Floats (vs Jigglypuff)
    AllStarICs      = 0x0bd   # Icicle Mountain (vs Ice Climbers)
    AllStarPeach    = 0x0be   # Princess Peach's Castle (vs Peach)
    AllStarZelda    = 0x0bf   # Temple (vs Zelda)
    AllStarMarth    = 0x0c0   # Fountain of Dreams (Emblem Music) (vs Marth)
    AllStarMewtwo   = 0x0c1   # Battlefield (Poké Floats song) (vs Mewtwo)
    AllStarBowser   = 0x0c2   # Yoshi's Island (vs Bowser)
    AllStarDrMario  = 0x0c3   # Mushroom Kingdom II (Dr Mario Music) (vs Dr Mario)
    AllStarYLink    = 0x0c4   # Jungle Japes (vs Young Link)
    AllStarFalco    = 0x0c5   # Venom (vs Falco)
    AllStarPichu    = 0x0c6   # Fourside (vs Pichu)
    AllStarRoy      = 0x0c7   # Final Destination (Emblem Music) (vs Roy)
    AllStarGnW      = 0x0c8   # Flat Zone (vs Team Game & Watch)
    AllStarGanon    = 0x0c9   # Brinstar Depths (vs Gannondorf)

    # Event Mode
    Event01 = 0x0ca   # Battlefield (Event #01) (Trouble King)
    Event18 = 0x0cb   # Temple (Event #18) (Link's Adventure)
    Event03 = 0x0cc   # Princess Peach's Castle (Event #03) (Bomb-fest)
    Event04 = 0x0cd   # Yoshi's Story (Event #04) (Dino-wrangling)
    Event05 = 0x0ce   # Onett (Event #05) (Spare Change)
    Event06 = 0x0cf   # Fountain of Dreams (Event #06) (Kirbys on Parade)
    Event07 = 0x0d0   # Pokémon Stadium (Event #07) (Pokémon Battle)
    Event08 = 0x0d1   # Brinstar (Event #08) (Hot Date on Brinstar)
    Event09 = 0x0d2   # Great Bay (Event #09) (Hide 'n' Sheik)
    Event10 = 0x0d3   # Yoshi's Island (Event #10) (All-Star Match 1-1 /vs Mario)
    Event11 = 0x0d4   # Icicle Mountain (Event #11) (King of the Mountain)
    Event12 = 0x0d5   # Mute City (Event #12) (Seconds
    Event13 = 0x0d6   # Rainbow Cruise  (Event #13) (Yoshi's Egg)
    Event14 = 0x0d7   # Goomba  (Event #14) (Trophy Tussle 1)
    Event44 = 0x0d8   # Battlefield (Event #44) (Mewtwo Strikes!)
    Event16 = 0x0d9   # Corneria (Event #16) (Kirby's Air-raid)
    Event17 = 0x0da   # Jungle Japes (F-Zero Music) (Event #17) (Bounty Hunters)
    Event02 = 0x0db   # Kongo Jungle (Event #2) (Lord of the Jungle)
    Event19 = 0x0dc   # Final Destination (Event #19) (Peach's Peril)
    Event20 = 0x0dd   # Brinstar (Event #20) (All-Star Match 2-1 /vs Samus)
    Event21 = 0x0de   # Princess Peach's Castle (Event #21) (Ice Breaker)
    Event22 = 0x0df   # Mushroom Kingdom II (Event #22) (Super Mario 128)
    Event27 = 0x0e0   # Brinstar Depths (Event #27) (Cold Armor)
    Event24 = 0x0e1   # Yoshi's Island (Event #24) (The Yoshi Herd)
    Event25 = 0x0e2   # Fourside (DK Rap) (Event #25) (Gargantuans)
    Event26 = 0x0e3   # Entei (Event #26) (Trophy Tussle 2)
    Event23 = 0x0e4   # Venom (Event #23) (Slippy's Invention)
    Event28 = 0x0e5   # Green Greens (Event #28) (Puffballs Unite)
    Event29 = 0x0e6   # Temple (Great Bay music) (Event #29) (Triforce Gathering)
    Event15 = 0x0e7   # Fountain of Dreams (Event #15) (Girl Power)
    Event31 = 0x0e8   # Mushroom Kingdom I (Event #31) (Mario Bros. Madness)
    Event32 = 0x0e9   # Corneria (Many Arwings) (Event #32) (Target Acquired)
    Event33 = 0x0ea   # F  #Zero Adventure Stage (Event #33) (Lethal Marathon)
    Event34 = 0x0eb   # Great Bay (Event #34) (Seven Years)
    Event35 = 0x0ec   # Dream Land (Event #35) (Time for a Checkup)
    Event36 = 0x0ed   # Fourside (Event #36) (Space Travelers)
    Event30 = 0x0ee   # Fountain of Dreams (Event #30) (All-Star Match 3-1 /vs Kirby)
    Event38 = 0x0ef   # Mushroom Kingdom II (Event #38) (Super Mario Bros. 2)
    Event39 = 0x0f0   # Pokémon Stadium (Event #39) (Jigglypuff Live!)
    Event40 = 0x0f1   # Temple (Emblem Music) (Event #40) (All-Star Match 4-1 /vs Marth)
    Event41 = 0x0f2   # Temple (Emblem Music) (Event #41) (En Garde!)
    Event42 = 0x0f3   # Poké Floats (Event #42) (Trouble King 2)
    Event43 = 0x0f4   # Big Blue (Event #43) (Birds of Prey)
    Event37 = 0x0f5   # Battlefield (Event #37) (Legendary Pokemon)
    Event45 = 0x0f6   # Flat Zone (Event #45) (Game and Watch Forever!)
    Event46 = 0x0f7   # Temple (Emblem Music) (Event #46) (Fire Emblem Pride)
    Event47 = 0x0f8   # Majora's Mask (Event #47) (Trophy Tussle 3)
    Event48 = 0x0f9   # Yoshi's Story (Event #48) (Pikachu and Pichu)
    Event49 = 0x0fa   # Mushroom Kingdom I  (Event #49) (All-Star Match Deluxe 5-1 /vs Dr Mario)
    Event50 = 0x0fb   # Final Destination (Final Destination Match) (Event #50)
    Event51 = 0x0fc   # Final Destination (The Showdown) (Event #51)

    # All-Star Mode ?
    AllStarOtherDK		= 0x0fd   # Jungle Japes (DK Rap) (Event #10) (All-Star Match 1-2 /vs DK)
    AllStarOtherYoshi		= 0x0fe   # Yoshi's Story (Event #10) (All-Star Match 1-3 /vs Yoshi)
    AllStarOtherPeach		= 0x0ff   # Princess Peach's Castle (Event #10) (All-Star Match 1-4 /vs Peach)
    AllStarOtherBowser		= 0x100   # Rainbow Cruise (Event #10) (All-Star Match 1-5 /vs Bowser)
    AllStarOtherLink		= 0x101   # Great Bay  (All-Star Match 2-2 /vs Link)
    AllStarOtherZelda		= 0x102   # Temple  (All-Star Match 2-3 /vs Zelda)
    AllStarOtherFalcon		= 0x103   # Mute City (All-Star Match 2-4 /vs Captain Falcon)
    AllStarOtherFox		= 0x104   # Corneria (All-Star Match 2-5 /vs Fox)
    AllStarOtherPika		= 0x105   # Pokémon Stadium (All-Star Match 3-2 /vs Pikachu)
    AllStarOtherNess		= 0x106   # Onett (All-Star Match 3-3 /vs Ness)
    AllStarOtherICs		= 0x107   # Icicle Mountain (All-Star Match 3-4 /vs Ice Climbers)
    AllStarOtherLuigi		= 0x108   # Mushroom Kingdom II (All-Star Match 4-2 /vs Luigi)
    AllStarOtherJiggs		= 0x109   # Poké Floats (All-Star Match 4-3 /vs Jigglypuff)
    AllStarOtherMewtwo		= 0x10a   # Final Destination (All-Star Match 4-4 /vs Mewtwo)
    AllStarOtherGnW		= 0x10b   # Flat Zone (All-Star Match 4-5 /vs Mr Game & Watch)
    AllStarOtherFalco		= 0x10c   # Venom (All-Star Match Deluxe 5-2 /vs Falco)
    AllStarOtherPichu		= 0x10d   # Pokémon Stadium (All-Star Match Deluxe 5-3 /vs Pichu)
    AllStarOtherYLink		= 0x10e   # Great Bay (Saria's Song) (All-Star Match Deluxe 5-4 /vs Young Link)
    AllStarOtherRoy		= 0x10f   # Temple (Emblem Music) (All-Star Match Deluxe 5-5 /vs Roy)
    AllStarOtherGanon		= 0x110   # Final Destination (All-Star Match Deluxe 5-6 /vs Gannondorf)

    # Unlocking Characters
    UnlockBF            = 0x111   # Battlefield (NO CHARA)
    UnlockJiggs         = 0x112   # Pokémon Stadium #Unlocking Jigglypuff
    UnlockMewtwo	= 0x113   # Final Destination #Unlocking Mewtwo
    UnlockLuigi         = 0x114   # Mushroom Kingdom II #Unlocking Luigi
    UnlockMarth         = 0x115   # Fountain of Dreams #Unlocking Marth
    UnlockGnW           = 0x116   # Flat Zone #Unlocking Mr Game and Watch
    UnlockDrMario	= 0x117   # Princess Peach's Castle (DR Mario song) #Unlocking Dr Mario
    UnlockGanon         = 0x118   # Final Destination (Great Bay music) #Unlocking Gannondorf
    UnlockYLink         = 0x119   # Great Bay (Saria's Song) #Unlocking Young Link
    UnlockFalco         = 0x11a   # Battlefield (Corneria Music) #Unlocking Falco
    UnlockPichu         = 0x11b   # Pokémon Stadium #Unlocking Pichu?
    UnlockRoy           = 0x11c   # Temple (Emblem Music) #Unlocking Roy?

    # Multi-Man Melee
    MultiManMelee	= 0x11d   # Battlefield (Multi-Man Melee)


class stageInternal(Enum):

    Unk00               = 0x00
    Unk01               = 0x01

    Castle		= 0x02
    RainbowCruise	= 0x03
    KongoJungle		= 0x04
    JungleJapes		= 0x05
    GreatBay		= 0x06
    Temple		= 0x07
    Brinstar		= 0x08
    BrinstarDepths	= 0x09
    YoshiStory		= 0x0A
    YoshiIsland		= 0x0B
    Fountain		= 0x0C
    GreenGreens		= 0x0D
    Corneria		= 0x0E
    Venom		= 0x0F
    PokemonStadium	= 0x10
    PokeFloats		= 0x11
    MuteCity		= 0x12
    BigBlue		= 0x13
    Onett		= 0x14
    Fourside		= 0x15
    IcicleMountain	= 0x16
    MushroomKingdom	= 0x18
    Unused              = 0x17
    MushroomKingdomII	= 0x19
    Unused1a            = 0x1a
    FlatZone		= 0x1B
    DreamLand		= 0x1C
    YoshiIsland64	= 0x1D
    KongoJungle64	= 0x1E

    Unk1f	        = 0x1F
    Unk20	        = 0x20
    Unk21	        = 0x21
    Unk22	        = 0x22
    Unk23	        = 0x23

    Battlefield		= 0x24
    FinalDestination	= 0x25
    SnagTrophies        = 0x26
    RaceToTheFinish     = 0x27
    TargetMario         = 0x28
    TargetFalcon        = 0x29
    TargetYLink         = 0x2a
    TargetDK            = 0x2b
    TargetDrMario       = 0x2c
    TargetFalco         = 0x2d
    TargetFox           = 0x2e
    TargetICs           = 0x2f
    TargetKirby         = 0x30
    TargetBowser        = 0x31
    TargetLink          = 0x32
    TargetLuigi         = 0x33
    TargetMarth         = 0x34
    TargetMewtwo        = 0x35
    TargetNess          = 0x36
    TargetPeach         = 0x37
    TargetPichu         = 0x38
    TargetPika          = 0x39
    TargetPuff          = 0x3a
    TargetSamus         = 0x3b
    TargetSheik         = 0x3c
    TargetYoshi         = 0x3d
    TargetZelda         = 0x3e
    TargetGnW           = 0x3f
    TargetRoy           = 0x40
    TargetGanon         = 0x41
    AllStarRestArea     = 0x42
    HomeRunContest      = 0x43
    Trophy1             = 0x44
    Trophy2             = 0x45
    Trophy3             = 0x46

    #Unk47               = 0x47
    #Unk48               = 0x48
    #Unk49               = 0x49
    #Unk4a               = 0x4a
    #Unk4b               = 0x4b
    #Unk4c               = 0x4c
    #Unk4d               = 0x4d
    #Unk4e               = 0x4e
    #Unk4f               = 0x4f
    #Unk50               = 0x50
    #Unk51               = 0x51
    #Unk52               = 0x52
    #Unk53               = 0x53
    #Unk54               = 0x54
    #Unk55               = 0x55
    #Unk56               = 0x56
    #Unk57               = 0x57
    #Unk58               = 0x58
    #Unk59               = 0x59
    #Unk5a               = 0x5a
    #Unk5b               = 0x5b
    #Unk5c               = 0x5c
    #Unk5d               = 0x5d
    #Unk5e               = 0x5e
    #Unk5f               = 0x5f
    #Unk60               = 0x60
    #Unk61               = 0x61
    #Unk62               = 0x62
    #Unk63               = 0x63
    #Unk64               = 0x64
    #Unk65               = 0x65
    #Unk66               = 0x66
    #Unk67               = 0x67
    #Unk68               = 0x68
    #Unk69               = 0x69
    #Unk6a               = 0x6a
    #Unk6b               = 0x6b
    #Unk6c               = 0x6c
    #Unk6d               = 0x6d
    #Unk6e               = 0x6e
    #Unk6f               = 0x6f

# -----------------------------------------------------------------------------
# Action state IDs

class actionState(Enum):
    DeadDown = 0x0000
    DeadLeft = 0x0001
    DeadRight = 0x0002
    DeadUp = 0x0003
    DeadUpStar = 0x0004
    DeadUpStarIce = 0x0005
    DeadUpFall = 0x0006
    DeadUpFallHitCamera = 0x0007
    DeadUpFallHitCameraFlat = 0x0008
    DeadUpFallIce = 0x0009
    DeadUpFallHitCameraIce = 0x000A
    Sleep = 0x000B
    Rebirth = 0x000C
    RebirthWait = 0x000D
    Wait = 0x000E
    WalkSlow = 0x000F
    WalkMiddle = 0x0010
    WalkFast = 0x0011
    Turn = 0x0012
    TurnRun = 0x0013
    Dash = 0x0014
    Run = 0x0015
    RunDirect = 0x0016
    RunBrake = 0x0017
    KneeBend = 0x0018
    JumpF = 0x0019
    JumpB = 0x001A
    JumpAerialF = 0x001B
    JumpAerialB = 0x001C
    Fall = 0x001D
    FallF = 0x001E
    FallB = 0x001F
    FallAerial = 0x0020
    FallAerialF = 0x0021
    FallAerialB = 0x0022
    FallSpecial = 0x0023
    FallSpecialF = 0x0024
    FallSpecialB = 0x0025
    DamageFall = 0x0026
    Squat = 0x0027
    SquatWait = 0x0028
    SquatRv = 0x0029
    Landing = 0x002A
    LandingFallSpecial = 0x002B
    Attack11 = 0x002C
    Attack12 = 0x002D
    Attack13 = 0x002E
    Attack100Start = 0x002F
    Attack100Loop = 0x0030
    Attack100End = 0x0031
    AttackDash = 0x0032
    AttackS3Hi = 0x0033
    AttackS3HiS = 0x0034
    AttackS3S = 0x0035
    AttackS3LwS = 0x0036
    AttackS3Lw = 0x0037
    AttackHi3 = 0x0038
    AttackLw3 = 0x0039
    AttackS4Hi = 0x003A
    AttackS4HiS = 0x003B
    AttackS4S = 0x003C
    AttackS4LwS = 0x003D
    AttackS4Lw = 0x003E
    AttackHi4 = 0x003F
    AttackLw4 = 0x0040
    AttackAirN = 0x0041
    AttackAirF = 0x0042
    AttackAirB = 0x0043
    AttackAirHi = 0x0044
    AttackAirLw = 0x0045
    LandingAirN = 0x0046
    LandingAirF = 0x0047
    LandingAirB = 0x0048
    LandingAirHi = 0x0049
    LandingAirLw = 0x004A
    DamageHi1 = 0x004B
    DamageHi2 = 0x004C
    DamageHi3 = 0x004D
    DamageN1 = 0x004E
    DamageN2 = 0x004F
    DamageN3 = 0x0050
    DamageLw1 = 0x0051
    DamageLw2 = 0x0052
    DamageLw3 = 0x0053
    DamageAir1 = 0x0054
    DamageAir2 = 0x0055
    DamageAir3 = 0x0056
    DamageFlyHi = 0x0057
    DamageFlyN = 0x0058
    DamageFlyLw = 0x0059
    DamageFlyTop = 0x005A
    DamageFlyRoll = 0x005B
    LightGet = 0x005C
    HeavyGet = 0x005D
    LightThrowF = 0x005E
    LightThrowB = 0x005F
    LightThrowHi = 0x0060
    LightThrowLw = 0x0061
    LightThrowDash = 0x0062
    LightThrowDrop = 0x0063
    LightThrowAirF = 0x0064
    LightThrowAirB = 0x0065
    LightThrowAirHi = 0x0066
    LightThrowAirLw = 0x0067
    HeavyThrowF = 0x0068
    HeavyThrowB = 0x0069
    HeavyThrowHi = 0x006A
    HeavyThrowLw = 0x006B
    LightThrowF4 = 0x006C
    LightThrowB4 = 0x006D
    LightThrowHi4 = 0x006E
    LightThrowLw4 = 0x006F
    LightThrowAirF4 = 0x0070
    LightThrowAirB4 = 0x0071
    LightThrowAirHi4 = 0x0072
    LightThrowAirLw4 = 0x0073
    HeavyThrowF4 = 0x0074
    HeavyThrowB4 = 0x0075
    HeavyThrowHi4 = 0x0076
    HeavyThrowLw4 = 0x0077
    SwordSwing1 = 0x0078
    SwordSwing3 = 0x0079
    SwordSwing4 = 0x007A
    SwordSwingDash = 0x007B
    BatSwing1 = 0x007C
    BatSwing3 = 0x007D
    BatSwing4 = 0x007E
    BatSwingDash = 0x007F
    ParasolSwing1 = 0x0080
    ParasolSwing3 = 0x0081
    ParasolSwing4 = 0x0082
    ParasolSwingDash = 0x0083
    HarisenSwing1 = 0x0084
    HarisenSwing3 = 0x0085
    HarisenSwing4 = 0x0086
    HarisenSwingDash = 0x0087
    StarRodSwing1 = 0x0088
    StarRodSwing3 = 0x0089
    StarRodSwing4 = 0x008A
    StarRodSwingDash = 0x008B
    LipStickSwing1 = 0x008C
    LipStickSwing3 = 0x008D
    LipStickSwing4 = 0x008E
    LipStickSwingDash = 0x008F
    ItemParasolOpen = 0x0090
    ItemParasolFall = 0x0091
    ItemParasolFallSpecial = 0x0092
    ItemParasolDamageFall = 0x0093
    LGunShoot = 0x0094
    LGunShootAir = 0x0095
    LGunShootEmpty = 0x0096
    LGunShootAirEmpty = 0x0097
    FireFlowerShoot = 0x0098
    FireFlowerShootAir = 0x0099
    ItemScrew = 0x009A
    ItemScrewAir = 0x009B
    DamageScrew = 0x009C
    DamageScrewAir = 0x009D
    ItemScopeStart = 0x009E
    ItemScopeRapid = 0x009F
    ItemScopeFire = 0x00A0
    ItemScopeEnd = 0x00A1
    ItemScopeAirStart = 0x00A2
    ItemScopeAirRapid = 0x00A3
    ItemScopeAirFire = 0x00A4
    ItemScopeAirEnd = 0x00A5
    ItemScopeStartEmpty = 0x00A6
    ItemScopeRapidEmpty = 0x00A7
    ItemScopeFireEmpty = 0x00A8
    ItemScopeEndEmpty = 0x00A9
    ItemScopeAirStartEmpty = 0x00AA
    ItemScopeAirRapidEmpty = 0x00AB
    ItemScopeAirFireEmpty = 0x00AC
    ItemScopeAirEndEmpty = 0x00AD
    LiftWait = 0x00AE
    LiftWalk1 = 0x00AF
    LiftWalk2 = 0x00B0
    LiftTurn = 0x00B1
    GuardOn = 0x00B2
    Guard = 0x00B3
    GuardOff = 0x00B4
    GuardSetOff = 0x00B5
    GuardReflect = 0x00B6
    DownBoundU = 0x00B7
    DownWaitU = 0x00B8
    DownDamageU = 0x00B9
    DownStandU = 0x00BA
    DownAttackU = 0x00BB
    DownFowardU = 0x00BC
    DownBackU = 0x00BD
    DownSpotU = 0x00BE
    DownBoundD = 0x00BF
    DownWaitD = 0x00C0
    DownDamageD = 0x00C1
    DownStandD = 0x00C2
    DownAttackD = 0x00C3
    DownFowardD = 0x00C4
    DownBackD = 0x00C5
    DownSpotD = 0x00C6
    Passive = 0x00C7
    PassiveStandF = 0x00C8
    PassiveStandB = 0x00C9
    PassiveWall = 0x00CA
    PassiveWallJump = 0x00CB
    PassiveCeil = 0x00CC
    ShieldBreakFly = 0x00CD
    ShieldBreakFall = 0x00CE
    ShieldBreakDownU = 0x00CF
    ShieldBreakDownD = 0x00D0
    ShieldBreakStandU = 0x00D1
    ShieldBreakStandD = 0x00D2
    FuraFura = 0x00D3
    Catch = 0x00D4
    CatchPull = 0x00D5
    CatchDash = 0x00D6
    CatchDashPull = 0x00D7
    CatchWait = 0x00D8
    CatchAttack = 0x00D9
    CatchCut = 0x00DA
    ThrowF = 0x00DB
    ThrowB = 0x00DC
    ThrowHi = 0x00DD
    ThrowLw = 0x00DE
    CapturePulledHi = 0x00DF
    CaptureWaitHi = 0x00E0
    CaptureDamageHi = 0x00E1
    CapturePulledLw = 0x00E2
    CaptureWaitLw = 0x00E3
    CaptureDamageLw = 0x00E4
    CaptureCut = 0x00E5
    CaptureJump = 0x00E6
    CaptureNeck = 0x00E7
    CaptureFoot = 0x00E8
    EscapeF = 0x00E9
    EscapeB = 0x00EA
    Escape = 0x00EB
    EscapeAir = 0x00EC
    ReboundStop = 0x00ED
    Rebound = 0x00EE
    ThrownF = 0x00EF
    ThrownB = 0x00F0
    ThrownHi = 0x00F1
    ThrownLw = 0x00F2
    ThrownLwWomen = 0x00F3
    Pass = 0x00F4
    Ottotto = 0x00F5
    OttottoWait = 0x00F6
    FlyReflectWall = 0x00F7
    FlyReflectCeil = 0x00F8
    StopWall = 0x00F9
    StopCeil = 0x00FA
    MissFoot = 0x00FB
    CliffCatch = 0x00FC
    CliffWait = 0x00FD
    CliffClimbSlow = 0x00FE
    CliffClimbQuick = 0x00FF
    CliffAttackSlow = 0x0100
    CliffAttackQuick = 0x0101
    CliffEscapeSlow = 0x0102
    CliffEscapeQuick = 0x0103
    CliffJumpSlow1 = 0x0104
    CliffJumpSlow2 = 0x0105
    CliffJumpQuick1 = 0x0106
    CliffJumpQuick2 = 0x0107
    AppealR = 0x0108
    AppealL = 0x0109
    ShoulderedWait = 0x010A
    ShoulderedWalkSlow = 0x010B
    ShoulderedWalkMiddle = 0x010C
    ShoulderedWalkFast = 0x010D
    ShoulderedTurn = 0x010E
    ThrownFF = 0x010F
    ThrownFB = 0x0110
    ThrownFHi = 0x0111
    ThrownFLw = 0x0112
    CaptureCaptain = 0x0113
    CaptureYoshi = 0x0114
    YoshiEgg = 0x0115
    CaptureKoopa = 0x0116
    CaptureDamageKoopa = 0x0117
    CaptureWaitKoopa = 0x0118
    ThrownKoopaF = 0x0119
    ThrownKoopaB = 0x011A
    CaptureKoopaAir = 0x011B
    CaptureDamageKoopaAir = 0x011C
    CaptureWaitKoopaAir = 0x011D
    ThrownKoopaAirF = 0x011E
    ThrownKoopaAirB = 0x011F
    CaptureKirby = 0x0120
    CaptureWaitKirby = 0x0121
    ThrownKirbyStar = 0x0122
    ThrownCopyStar = 0x0123
    ThrownKirby = 0x0124
    BarrelWait = 0x0125
    Bury = 0x0126
    BuryWait = 0x0127
    BuryJump = 0x0128
    DamageSong = 0x0129
    DamageSongWait = 0x012A
    DamageSongRv = 0x012B
    DamageBind = 0x012C
    CaptureMewtwo = 0x012D
    CaptureMewtwoAir = 0x012E
    ThrownMewtwo = 0x012F
    ThrownMewtwoAir = 0x0130
    WarpStarJump = 0x0131
    WarpStarFall = 0x0132
    HammerWait = 0x0133
    HammerWalk = 0x0134
    HammerTurn = 0x0135
    HammerKneeBend = 0x0136
    HammerFall = 0x0137
    HammerJump = 0x0138
    HammerLanding = 0x0139
    KinokoGiantStart = 0x013A
    KinokoGiantStartAir = 0x013B
    KinokoGiantEnd = 0x013C
    KinokoGiantEndAir = 0x013D
    KinokoSmallStart = 0x013E
    KinokoSmallStartAir = 0x013F
    KinokoSmallEnd = 0x0140
    KinokoSmallEndAir = 0x0141
    Entry = 0x0142
    EntryStart = 0x0143
    EntryEnd = 0x0144
    DamageIce = 0x0145
    DamageIceJump = 0x0146
    CaptureMasterhand = 0x0147
    CapturedamageMasterhand = 0x0148
    CapturewaitMasterhand = 0x0149
    ThrownMasterhand = 0x014A
    CaptureKirbyYoshi = 0x014B
    KirbyYoshiEgg = 0x014C
    CaptureLeadead = 0x014D
    CaptureLikelike = 0x014E
    DownReflect = 0x014F
    CaptureCrazyhand = 0x0150
    CapturedamageCrazyhand = 0x0151
    CapturewaitCrazyhand = 0x0152
    ThrownCrazyhand = 0x0153
    BarrelCannonWait = 0x0154
    Wait1 = 0x0155
    Wait2 = 0x0156
    Wait3 = 0x0157
    Wait4 = 0x0158
    WaitItem = 0x0159
    SquatWait1 = 0x015A
    SquatWait2 = 0x015B
    SquatWaitItem = 0x015C
    GuardDamage = 0x015D
    EscapeN = 0x015E
    AttackS4Hold = 0x015F
    HeavyWalk1 = 0x0160
    HeavyWalk2 = 0x0161
    ItemHammerWait = 0x0162
    ItemHammerMove = 0x0163
    ItemBlind = 0x0164
    DamageElec = 0x0165
    FuraSleepStart = 0x0166
    FuraSleepLoop = 0x0167
    FuraSleepEnd = 0x0168
    WallDamage = 0x0169
    CliffWait1 = 0x016A
    CliffWait2 = 0x016B
    SlipDown = 0x016C
    Slip = 0x016D
    SlipTurn = 0x016E
    SlipDash = 0x016F
    SlipWait = 0x0170
    SlipStand = 0x0171
    SlipAttack = 0x0172
    SlipEscapeF = 0x0173
    SlipEscapeB = 0x0174
    AppealS = 0x0175
    Zitabata = 0x0176
    CaptureKoopaHit = 0x0177
    ThrownKoopaEndF = 0x0178
    ThrownKoopaEndB = 0x0179
    CaptureKoopaAirHit = 0x017A
    ThrownKoopaAirEndF = 0x017B
    ThrownKoopaAirEndB = 0x017C
    ThrownKirbyDrinkSShot = 0x017D
    ThrownKirbySpitSShot = 0x017E

    # The data sheet stops here. 
    # The rest of these appear as entries in the global AS table

    Unk17f = 0x17f
    Unk180 = 0x180
    Unk181 = 0x181
    Unk182 = 0x182
    Unk183 = 0x183
    Unk184 = 0x184
    Unk185 = 0x185
    Unk186 = 0x186
    Unk187 = 0x187
    Unk188 = 0x188
    Unk189 = 0x189
    Unk18a = 0x18a
    Unk18b = 0x18b
    Unk18c = 0x18c
    Unk18d = 0x18d
    Unk18e = 0x18e
    Unk18f = 0x18f
    Unk190 = 0x190
    Unk191 = 0x191
    Unk192 = 0x192
    Unk193 = 0x193
    Unk194 = 0x194
    Unk195 = 0x195
    Unk196 = 0x196
    Unk197 = 0x197
    Unk198 = 0x198
    Unk199 = 0x199
    Unk19a = 0x19a
    Unk19b = 0x19b
    Unk19c = 0x19c
    Unk19d = 0x19d
    Unk19e = 0x19e
    Unk19f = 0x19f
    Unk1a0 = 0x1a0
    Unk1a1 = 0x1a1
    Unk1a2 = 0x1a2
    Unk1a3 = 0x1a3
    Unk1a4 = 0x1a4
    Unk1a5 = 0x1a5
    Unk1a6 = 0x1a6
    Unk1a7 = 0x1a7
    Unk1a8 = 0x1a8
    Unk1a9 = 0x1a9
    Unk1aa = 0x1aa
    Unk1ab = 0x1ab
    Unk1ac = 0x1ac
    Unk1ad = 0x1ad
    Unk1ae = 0x1ae
    Unk1af = 0x1af
    Unk1b0 = 0x1b0
    Unk1b1 = 0x1b1
    Unk1b2 = 0x1b2
    Unk1b3 = 0x1b3
    Unk1b4 = 0x1b4
    Unk1b5 = 0x1b5
    Unk1b6 = 0x1b6
    Unk1b7 = 0x1b7
    Unk1b8 = 0x1b8
    Unk1b9 = 0x1b9
    Unk1ba = 0x1ba
    Unk1bb = 0x1bb
    Unk1bc = 0x1bc
    Unk1bd = 0x1bd
    Unk1be = 0x1be
    Unk1bf = 0x1bf
    Unk1c0 = 0x1c0
    Unk1c1 = 0x1c1
    Unk1c2 = 0x1c2
    Unk1c3 = 0x1c3
    Unk1c4 = 0x1c4
    Unk1c5 = 0x1c5
    Unk1c6 = 0x1c6
    Unk1c7 = 0x1c7
    Unk1c8 = 0x1c8
    Unk1c9 = 0x1c9
    Unk1ca = 0x1ca
    Unk1cb = 0x1cb
    Unk1cc = 0x1cc
    Unk1cd = 0x1cd
    Unk1ce = 0x1ce
    Unk1cf = 0x1cf
    Unk1d0 = 0x1d0
    Unk1d1 = 0x1d1
    Unk1d2 = 0x1d2
    Unk1d3 = 0x1d3
    Unk1d4 = 0x1d4
    Unk1d5 = 0x1d5
    Unk1d6 = 0x1d6
    Unk1d7 = 0x1d7
    Unk1d8 = 0x1d8
    Unk1d9 = 0x1d9
    Unk1da = 0x1da
    Unk1db = 0x1db
    Unk1dc = 0x1dc
    Unk1dd = 0x1dd
    Unk1de = 0x1de


# -----------------------------------------------------------------------------
# Major Scene IDs
class majScene(Enum):
    TitleScreen                     = 0x00
    MainMenu                        = 0x01
    VSMode                          = 0x02
    ClassicMode                     = 0x03
    AdventureMode                   = 0x04
    AllStarMode                     = 0x05
    MainDebugMenu                   = 0x06
    SoundTestDebugMenu              = 0x07
    HanyuTestCSS                    = 0x08
    HanyuTestSSS                    = 0x09
    CameraModeMemcardPrompt         = 0x0a
    TrophyGallery                   = 0x0b
    TrophyLottery                   = 0x0c
    TrophyCollection                = 0x0d
    DebugDairantou                  = 0x0e
    TargetTest                      = 0x0f
    SuperSuddenDeath                = 0x10
    InvisibleMelee                  = 0x11
    SloMoMelee                      = 0x12
    LightningMelee                  = 0x13
    ChallengerApproaching           = 0x14
    ClassicModeEnding               = 0x15
    AdventureModeEnding             = 0x16
    AllStarModeEnding               = 0x17
    OpeningMovie                    = 0x18
    AdventureModeCutscenesDebug     = 0x19
    EndingDebugP1                   = 0x1a
    TournamentMode                  = 0x1b
    TrainingMode                    = 0x1c
    TinyMelee                       = 0x1d
    GiantMelee                      = 0x1e
    StaminaMode                     = 0x1f
    HomeRunContest                  = 0x20
    ManMelee10                      = 0x21
    ManMelee100                     = 0x22
    MinuteMelee3                    = 0x23
    MinuteMelee15                   = 0x24
    EndlessMelee                    = 0x25
    CruelMelee                      = 0x26
    ProgressiveScanPrompt           = 0x27
    BootUp                          = 0x28
    MemcardPrompt                   = 0x29
    FixedCamera                     = 0x2a
    EventMode                       = 0x2b
    SingleButton                    = 0x2c
    Unused3                         = 0x2d


# Minor Scene Shared function list IDs
class minSceneShared(Enum):
    TitleScreen                     = 0x00
    MainMenu                        = 0x01

    InGame                          = 0x02
    InGameSuddenDeath               = 0x03
    TrainingModeInGame              = 0x04

    ResultScreen                    = 0x05
    Unused06                        = 0x06
    DebugMenu                       = 0x07

    CSS                             = 0x08
    SSS                             = 0x09

    # The entry for this in the table is zeroed out
    Unused0a                        = 0x0A

    TrophyGallery                   = 0x0B
    TrophyLottery                   = 0x0C
    TrophyCollection                = 0x0D

    AdventureModeSplash             = 0x0e

    TrophyFall1PMode                = 0x0f
    Congrats                        = 0x10

    AdventureLuigi                  = 0x11
    AdventureBrinstar               = 0x12
    AdventurePlanetExplode          = 0x13
    Adventure3KirbySpawn            = 0x14
    AdventureGiantKirby             = 0x15
    AdventureStarFoxDialog          = 0x16
    AdventureFZeroRace              = 0x17
    AdventureMetalMarioLuigi        = 0x18
    AdventureBowserTrophy           = 0x19
    AdventureGigaTransform          = 0x1a
    AdventureGigaDefeated           = 0x1b

    OpeningMovie                    = 0x1c
    EndMovie1PMode                  = 0x1d
    HowToPlay                       = 0x1e
    SpecialMovie                    = 0x1f

    ClassicModeSplash               = 0x20

    # MODE : KIM -> ALLSTAR_ENEMY: CKIND_CAPTAIN
    UnusedAllStarSplash             = 0x21

    GameOver                        = 0x22
    ComingSoon                      = 0x23

    TournamentSetup                 = 0x24
    TournamentBracket               = 0x25
    TournamentWin                   = 0x26

    SpecialMessage                  = 0x27
    ProgressiveScan                 = 0x28
    ChallengerApproach              = 0x29

    MemcardPrompt                   = 0x2A
    Credits                         = 0x2b
    CameraModeMemcardPrompt         = 0x2c


# -----------------------------------------------------------------------------
# Item IDs

# 0x00
class itemID(Enum):
    Capsule = 0x00
    Box = 0x01
    Barrel = 0x02
    Egg = 0x03
    PartyBall = 0x04
    BarrelCannon = 0x05
    BobOmb = 0x06
    MrSaturn = 0x07
    HeartContainer = 0x08
    MaximTomato = 0x09
    Starman = 0x0a
    Bat = 0x0b
    BeamSword = 0x0c
    Parasol = 0x0d
    GShell = 0x0e
    RShell = 0x0f
    RayGun = 0x10
    Freezie = 0x11
    Food = 0x12
    ProxMine = 0x13
    Flipper = 0x14
    SScope = 0x15
    StarRod = 0x16
    LipStick = 0x17
    Fan = 0x18
    FFlower = 0x19
    Mushroom = 0x1a
    WarpStar = 0x1d
    ScrewAttach = 0x1e
    BunnyHood = 0x1f
    MetalBox = 0x20
    SpyCloak = 0x21
    PokeBall = 0x22

    # No idea what these are, yet. Maybe on the data sheet
    RayGunRecoil = 0x23
    StarRodStar = 0x24
    LipStickDust = 0x25
    SScopeBeam = 0x26
    RayGunBeam = 0x27
    HammerHead = 0x28
    Flower = 0x29
    YoshisEgg = 0x2a

    # These DO NOT correspond to item IDs - they are vestigial parts 
    # of the array with regular item function tables!
    # OldOtto = 0x2b
    # OldOcta = 0x2c

# 0x2b
class charProjectile(Enum):
    Goomba = 0x0
    Redead = 0x1
    Octarok = 0x2
    Ottosea = 0x3
    OctarokProjectile = 0x4

    MarioFireball = 0x5
    DrMarioPill = 0x6
    KirbyCutter = 0x7
    KirbyHammer = 0x8
    KirbyTauntStar = 0x9
    Unk0a = 0xa
    FoxLaser = 0xb
    FalcoLaser = 0xc
    FoxShadow = 0xd
    FalcoShadow = 0xe
    LinkBomb = 0xf
    YLinkBomb = 0x10
    LinkBoomerang = 0x11
    YLinkBoomerang = 0x12
    LinkHookshot = 0x13
    YLinkHookshot = 0x014
    Arrow = 0x15
    FireArrow = 0x16

    PKFire = 0x17
    PKFireColumn = 0x18
    PKFlash = 0x19

    PKThunder1 = 0x1a
    PKThunder2 = 0x1b
    PKThunder3 = 0x1c
    PKThunder4 = 0x1d
    PKThunder5 = 0x1e

    FoxBlaster = 0x1f
    FalcoBlaster = 0x20
    LinkBow = 0x21
    YLinkBow = 0x22
    PKFlashExplosion = 0x23
    SheikNeedleThrown = 0x24
    SheikNeedleCharge = 0x25
    PikachuThunder = 0x26
    PichuThunder = 0x27
    MarioCape = 0x28
    DrMarioCape = 0x29
    SheikSmokeUpB = 0x2a
    YoshiEggUpB = 0x2b
    YoshiUnkDownB = 0x2c
    YoshiStarsDownB = 0x2d
    PikachuNeutralBAir = 0x2e
    PikachuNeutralBGround = 0x2f

    PichuNeutralBAir = 0x30
    PichuNeutralBGround = 0x31

    SamusBombDownB = 0x32
    SamusChargeShot = 0x33
    SamusMissile = 0x34
    SamusGrapple = 0x35

    Unk36 = 0x36
    Unk37 = 0x37

    PeachTurnip = 0x38
    BowserFire = 0x39
    NessBat = 0x3a
    NessYoyo = 0x3b
    PeachParasolUpB = 0x3c
    PeachToadNeutralB = 0x3d

    # not certain
    LuigiFire = 0x3e
    ICsIceNeutralB = 0x3f
    ICsBlizzardDownB = 0x40
    DinsFire = 0x41
    DinsFireExplosion = 0x42
    Unk43 = 0x43
    Unk44 = 0x44
    MewtwoShadowBall = 0x45
    ICsChainUpB = 0x46

    GnWNeutralAPesticide = 0x47
    GnWDTiltManhole = 0x48
    GnWFsmashFire = 0x49
    GnWParashute = 0x4a
    GnWBAirTurtle = 0x4b
    GnWUAir = 0x4c
    GnWHammerSideB = 0x4d
    Unk4e = 0x4e
    GnWPan = 0x4f
    YLinkMilk = 0x50
    GnWParachute = 0x51

    Unk52 = 0x52
    Unk53 = 0x53
    Unk54 = 0x54
    Unk55 = 0x55
    Unk56 = 0x56

    # These are DIFFERENT from the data sheet (and correct)!
    KirbyMario = 0x57
    KirbyDrMario = 0x58
    KirbyLuigi = 0x59
    KirbyICs = 0x5a
    KirbyPeach = 0x5b
    KirbyToad = 0x5c
    KirbyFoxLaser = 0x5d
    KirbyFalcoLaser = 0x5e
    KirbyFoxBlaster = 0x5f
    KirbyFalcoBlaster = 0x60
    KirbyLinkArrow = 0x61
    KirbyYLinkArrow = 0x62
    KirbyLinkBow = 0x63
    KirbyYLinkBow = 0x64
    KirbyMewtwo = 0x65
    KirbyNess = 0x66
    KirbyNessExplosion = 0x67
    KirbyPikachuLightningAir = 0x68
    KirbyPikachuLightningGround= 0x69
    KirbyBPichuLightningAir = 0x6a
    KirbyBPichuLightningGround = 0x6b
    KirbySamus = 0x6c
    KirbySheikNeedleThrown = 0x6d
    KirbySheikNeedleCharge = 0x6e
    KirbyBowser = 0x6f
    KirbyGnWBacon = 0x70
    KirbyGnWPan = 0x71

    Unk72 = 0x72
    Unk73 = 0x73
    Unk74 = 0x74
    Coin = 0x75


# 0xa0
class pokemonID(Enum):
    Goldeen = 0x0
    Chicorita = 0x1
    Snorlax = 0x2
    Blastoise = 0x3
    Weezing = 0x4
    Charizard = 0x5
    Moltres = 0x6
    Zapdos = 0x7
    Articuno = 0x8
    Wobbuffet = 0x9
    Scizor = 0xa
    Unown = 0xb
    Entei = 0xc
    Raikou = 0xd
    Suicune = 0xe
    Bellossom = 0x0f
    Electrode = 0x10
    Lugia = 0x11
    HoOh = 0x12
    Ditto = 0x13
    Clefairy = 0x14
    Togepi = 0x15
    Mew = 0x16
    Celebi = 0x17
    Staryu = 0x18
    Chansey = 0x19
    Porygon2 = 0x1a
    Cyndaquil = 0x1b
    Marill = 0x1c
    Venusaur = 0x1d

# 0xbf
class pokemonProjectile(Enum):
    Chicorita = 0x0
    Blastoise = 0x1
    Weezing1 = 0x2
    Weezing2 = 0x3
    Charizard1 = 0x4
    Charizard2 = 0x5
    Charizard3 = 0x6
    Charizard4 = 0x7
    Unown = 0x8
    Lugia1 = 0x9
    Lugia2 = 0xa
    Lugia3 = 0xb
    HoOh = 0xc
    Staryu = 0xd
    Chansey = 0xe
    Cyndaquil = 0x0f

# 0xd0
class monsterID(Enum):
    OldGoomba = 0x00
    Target = 0x01
    Shyguy = 0x02
    GreenKoopa = 0x03
    RedKoopa = 0x04
    Likelile = 0x05
    OldRedead = 0x06
    OldOctorok = 0x07
    OldOttosea = 0x08
    WhiteBear = 0x09
    Klap = 0x0a
    GreenShell = 0x0b
    RedShell = 0x0c

# 0xdd
class stageItemID(Enum):
    Tingle = 0x0
    UnkDE = 0x1
    UnkDF = 0x2
    UnkE0 = 0x3
    Apple = 0x4
    HealingApple = 0x5
    UnkE3 = 0x6
    UnkE4 = 0x7
    UnkE5 = 0x8
    FlatzoneTool = 0x9
    UnkE7 = 0xa
    UnkE8 = 0xb
    Birdo = 0xc
    ArwingLaser = 0xd
    GreatFoxLaser = 0xe
    BirdoEgg = 0xf


# -----------------------------------------------------------------------------
# Structures we want to analyze

# This is a list of pointers to stage structures. 0x1bc bytes long?
STAGE_PTR_TABLE = 0x803dfedc


CURRENT_STAGE_INFO = 0x8049e6c8


STATIC_PLAYER_BASE = 0x80453080


