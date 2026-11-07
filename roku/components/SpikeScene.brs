sub init()
    m.play = m.top.FindNode("play")
    m.player = m.top.FindNode("player")
    m.status = m.top.FindNode("status")
    m.play.ObserveField("buttonSelected", "startDiagnostic")
    m.player.ObserveField("state", "onPlayerState")
    m.play.SetFocus(true)
end sub

sub startDiagnostic()
    info = CreateObject("roAppInfo")
    url = info.GetValue("sample_url")
    if url = ""
        m.status.text = "Build with --sample-url http://YOUR-MAC-IP:8080/diagnostic.mp4 and run the local media server. See README."
        return
    end if
    content = CreateObject("roSGNode", "ContentNode")
    content.url = url
    content.streamFormat = "mp4"
    content.title = "Original diagnostic pattern - not YouTube"
    m.player.content = content
    m.player.visible = true
    ' Handle playback keys here so OK is not consumed by the Video node.
    m.top.SetFocus(true)
    m.player.control = "play"
end sub

sub onPlayerState()
    state = m.player.state
    print "DIAGNOSTIC state="; state
    if state = "error"
        print "DIAGNOSTIC error="; m.player.errorCode; " "; m.player.errorMsg
        returnToMenu("Playback failed. Check Mac IP, media server, firewall and same LAN. No playback verified.")
    else if state = "finished"
        returnToMenu("Diagnostic finished. Record device model, OS, audio/video and remote behavior in the test log.")
    end if
end sub

sub returnToMenu(message as string)
    m.player.visible = false
    m.play.SetFocus(true)
    m.status.text = message
end sub

function onKeyEvent(key as string, press as boolean) as boolean
    if not press then return false
    if m.player.visible
        if key = "back"
            m.player.control = "stop"
            returnToMenu("Diagnostic stopped. OK to retry; Back to exit.")
            return true
        else if key = "play" or key = "OK"
            if m.player.state = "playing"
                m.player.control = "pause"
            else if m.player.state = "paused"
                m.player.control = "resume"
            end if
            return true
        end if
    end if
    if key = "back"
        m.top.exitRequested = true
        return true
    end if
    return false
end function
