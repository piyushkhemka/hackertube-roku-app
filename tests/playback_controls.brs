sub Main()
    m.player = {visible: true, state: "playing", position: 2.0, duration: 12.0, seek: -1.0, control: ""}
    ' Native Video owns seek keys; the scene must not replace them with jumps.
    for each key in ["left", "right", "rewind", "fastforward"]
        check(not onKeyEvent(key, true), "scene leaves native seek key unhandled: " + key)
        check(m.player.seek = -1.0, "scene does not issue a custom seek")
    end for
    check(not onKeyEvent("OK", false), "key release ignored")
    check(m.player.control = "", "key release does not toggle playback")
    m.player.state = "paused"
    onKeyEvent("OK", true)
    check(m.player.control = "resume", "OK resumes")
    m.player.state = "playing"
    onKeyEvent("OK", true)
    check(m.player.control = "pause", "OK pauses")
    m.player.state = "paused"
    onKeyEvent("play", true)
    check(m.player.control = "resume", "Play resumes")
    m.player.state = "playing"
    onKeyEvent("play", true)
    check(m.player.control = "pause", "Play pauses")
    m.play = {SetFocus: function(focus)
        m.focused = focus
    end function}
    m.status = {text: ""}
    m.top = {exitRequested: false}
    onKeyEvent("back", true)
    check(m.player.control = "stop", "Back stops playback")
    check(not m.player.visible, "Back hides player")
    check(m.play.focused, "Back restores menu focus")
    check(not m.top.exitRequested, "first Back keeps app open")
    onKeyEvent("back", true)
    check(m.top.exitRequested, "menu Back exits")
    print "PASS: playback control regression tests"
end sub

sub check(condition as boolean, message as string)
    if not condition
        print "FAIL: "; message
        stop
    end if
end sub
