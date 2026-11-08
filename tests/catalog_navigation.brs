sub Main()
    m.failures = 0
    m.toolbar = {focused: false, SetFocus: function(value)
        m.focused = value
    end function, hasFocus: function()
        return m.focused
    end function}
    m.grid = {focused: true, hasFocus: function()
        return m.focused
    end function}
    m.card = {visible: true, itemContent: invalid, focusPercent: 0}
    m.top = {card: m.card, findNode: function(id)
        return m.card
    end function}
    m.items = []
    for i = 0 to 23
        m.items.Push({id: i.ToStr(), title: "Video " + i.ToStr(), channel: "Test"})
    end for
    m.selected = 0
    m.firstRow = 0
    m.toolIndex = 0
    m.focusArea = "grid"
    m.pickerMode = ""
    m.loaded = true
    m.loading = false
    m.advanceAfterLoad = false
    m.page = 0
    m.pages = 3
    m.serial = 1
    m.query = ""
    m.area = ""
    m.category = ""
    m.sort = "recommended"
    m.topicName = "All topics"
    m.status = {text: ""}
    m.empty = {visible: false}
    m.task = {state: "stop"}
    m.videoQueue = {playVideo: invalid}
    MoveGrid("down")
    check(m.selected = 4 and m.firstRow = 0, "Down enters second row")
    MoveGrid("down")
    check(m.selected = 8 and m.firstRow = 1, "Down scrolls third row into view")
    MoveGrid("up")
    check(m.selected = 0+4, "Up returns to prior row")
    m.selected = 20
    MoveGrid("down")
    check(m.loading and m.task.request.page = 1, "Down at loaded boundary requests next batch")
    check(m.advanceAfterLoad, "pending Down is retained while loading")
    check(m.selected = 20 and m.items.Count() = 24, "existing videos retained during loading")
    m.task.result = {serial: m.serial, page: 1, pages: 3, total: 50, items: []}
    for i = 24 to 47
        m.task.result.items.Push({id: i.ToStr(), title: "Video " + i.ToStr(), channel: "Test"})
    end for
    OnCatalogResult()
    check(m.items.Count() = 48 and m.selected = 24, "new batch appends and completes Down")
    check(m.firstRow = 5, "new selection remains in two-row viewport")
    MoveGrid("up")
    check(m.selected = 20, "old batch remains reachable by Up")
    m.task.result = {serial: m.serial - 1, items: []}
    OnCatalogResult()
    check(m.items.Count() = 48, "stale async response ignored")
    FocusToolbar()
    check(m.toolbar.focused and m.focusArea = "toolbar", "toolbar has a separate focus target")
    OnVideoSelected()
    check(m.videoQueue.playVideo = invalid, "stale grid selection cannot play from toolbar")
    OnKeyEvent("right", true)
    check(m.toolIndex = 1, "toolbar Right selects Topics")
    check(m.videoQueue.playVideo = invalid, "toolbar movement does not play")
    m.taxonomy = {areas: [{id: "software", name: "Software", categories: [{id: "ruby", name: "Ruby"}]}]}
    m.picker = {}
    OnKeyEvent("OK", true)
    check(m.pickerMode = "topics", "toolbar OK opens Topics")
    check(m.videoQueue.playVideo = invalid, "toolbar OK does not play a video")
    OnKeyEvent("down", true)
    OnKeyEvent("OK", true)
    check(m.task.request.area = "software" and m.task.request.category = "", "topic OK immediately requests area filter")
    check(m.items.Count() = 0 and m.task.request.page = 0, "filter resets old videos and pagination")
    check(m.pickerMode = "" and m.topicName = "Software", "topic picker closes after applying choice")
    OpenTopics()
    check(m.pickerIndex = 1, "current topic highlighted on reopen")
    OnKeyEvent("down", true)
    OnKeyEvent("OK", true)
    check(m.task.request.category = "ruby", "subcategory OK requests category filter")
    m.toolIndex = 2
    ActivateTool()
    OnKeyEvent("down", true)
    OnKeyEvent("OK", true)
    check(m.task.request.sort = "recent" and m.task.request.category = "ruby", "sort applies and preserves topic")
    ActivateTool()
    check(m.pickerIndex = 1, "current sort highlighted on reopen")
    OnKeyEvent("down", true)
    OnKeyEvent("OK", true)
    check(m.task.request.sort = "az", "Title A-Z applies")
    ActivateTool()
    OnKeyEvent("up", true)
    OnKeyEvent("up", true)
    OnKeyEvent("OK", true)
    check(m.task.request.sort = "recommended", "Top recommended restores requested order")
    ActivateTool()
    OnKeyEvent("down", true)
    OnKeyEvent("back", true)
    check(m.sort = "recommended", "Back cancels without applying highlighted sort")
    m.task.state = "run"
    oldSerial = m.task.request.serial
    OpenTopics()
    OnKeyEvent("up", true)
    OnKeyEvent("up", true)
    OnKeyEvent("OK", true)
    check(m.pending <> invalid and m.task.request.serial = oldSerial, "selection during load queues latest request")
    m.task.state = "done"
    OnTaskState()
    check(m.pending = invalid and m.task.request.area = "" and m.task.request.category = "", "queued All topics runs when task completes")
    entries = []
    for i = 0 to 15
        entries.Push({id: i.ToStr(), name: i.ToStr()})
    end for
    ShowPicker("sort", entries, "Test scroll")
    for i = 0 to 11
        OnKeyEvent("down", true)
    end for
    check(m.pickerIndex = 12 and m.pickerFirst = 3, "picker scrolls past ten visible choices")
    OnKeyEvent("back", true)
    if m.failures = 0
        print "PASS: catalog navigation and continuous loading"
    else
        print "FAILURES: "; m.failures
    end if
end sub

sub check(condition as boolean, message as string)
    if not condition
        m.failures += 1
        print "FAIL: "; message
    end if
end sub

sub NodeSetFocus(node as object, focused as boolean)
    node.focused = focused
end sub
