sub Main()
    screen = CreateObject("roSGScreen")
    port = CreateObject("roMessagePort")
    screen.SetMessagePort(port)
    scene = screen.CreateScene("SpikeScene")
    scene.ObserveField("exitRequested", port)
    screen.Show()
    while true
        message = Wait(0, port)
        if Type(message) = "roSGScreenEvent"
            if message.IsScreenClosed() then return
        else if Type(message) = "roSGNodeEvent"
            if message.GetField() = "exitRequested" and message.GetData() = true
                screen.Close()
                return
            end if
        end if
    end while
end sub
