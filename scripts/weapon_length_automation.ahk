#Include Gdip_All.ahk  ; Yoinked from https://github.com/buliasz/AHKv2-Gdip/blob/master/Gdip_All.ahk

weaponList := [
    "axe",
    "battleaxe",
    "bow",
    "carryable_candelabra",
    "changelog",
    "crab_katars",
    "cudgel",
    "dagger",
    "daneaxe",
    "executionersaxe",
    "falchion",
    "glaive",
    "goedendag",
    "greatsword",
    "greatsword_malric",
    "halberd",
    "hatchet",
    "heavycavalrysword",
    "heavymace",
    "heavyshield",
    "highlandsword",
    "javelin",
    "katars",
    "knife",
    "lance",
    "longsword",
    "longsword_argon_citadel",
    "mace",
    "maul",
    "mediumshield",
    "messer",
    "morningstar",
    "onehandedspear",
    "pickaxe",
    "polehammer",
    "poleaxe",
    "quarterstaff",
    "rapier",
    "shortsword",
    "shovel",
    "sledgehammer",
    "spear",
    "sword",
    "throwingaxe",
    "throwingknife",
    "throwingmallet",
    "twohandedhammer",
    "warhammer",
    "waraxe",
    "warclub",
    "fists",
]

; Initialize GDI+ for screenshot functionality
pToken := Gdip_Startup()
if !pToken {
    MsgBox("GDI+ failed to start. Exiting script.")
    ExitApp()
}

; Show prompt and wait for user to press OK
result := MsgBox("Press OK to start the script.",, "OKCancel")
if result = "Cancel"
    ExitApp()

Sleep(5000)

; Manually set the path to the Screenshots directory in the Pictures folder
screenshotDir := "C:\Users\" A_UserName "\Pictures\Screenshots\chiv2-weapon-stats"

; Ensure the screenshots directory exists
if !DirExist(screenshotDir)
    DirCreate(screenshotDir)


actions := [
    {key: "g", name: "slash"},
    {key: "!g", name: "alt-slash"},
    {key: "h", name: "stab"},
    {key: "!h", name: "alt-stab"},
    {key: "j", name: "overhead"},
    {key: "!j", name: "alt-overhead"}
]

for weaponName in weaponList {
    for action in actions {
        GiveWeapon(weaponName)
        
        Send("{w Down}")
        Sleep(5000)
        Send("{w Up}")

        Loop 20 {
            ; Some weapons are breakable, so we give them to ourselves every iteration just in case.

            Sleep(4000)
            Send(action.key)
            Sleep(1100)

            screenshotPath := screenshotDir "\" weaponName "-" action.name "-" A_Index ".png"
            CaptureScreen(screenshotPath)
            GiveWeapon(weaponName)
        }



        Sleep(100)
        ; s for 2 seconds
        Send("{s Down}")
        Sleep(2000)
        Send("{s Up}")
    }
}

MsgBox("Script completed for all weapons!")

GiveWeapon(weaponName) {
    Send("{NumpadSub}")
    Sleep(100)
    Send("giveweapon " weaponName)
    Sleep(100)
    Send("{Enter}")
    Sleep(100)
}

; Function to capture the screen and save it
CaptureScreen(filePath) {
    pBitmap := Gdip_BitmapFromScreen()  ; Capture the full screen (can modify for active window)
    Gdip_SaveBitmapToFile(pBitmap, filePath)
    Gdip_DisposeImage(pBitmap)  ; Clean up resources
}
