sub Main()
    m.failures = 0
    m.catalog = { videos: [], orders: { recommended: [], recent: [], az: [] } }
    for i = 0 to 49
        categories = ["math"]
        areas = ["science"]
        if i >= 25
            categories = ["ruby"]
            areas = ["software"]
        end if
        m.catalog.videos.Push({ id: i.ToStr(), title: "Video " + i.ToStr(), channel: "Test", search: "video " + i.ToStr() + " " + categories[0], categories: categories, areas: areas, recommenders: 1 })
        m.catalog.orders.recommended.Push(i)
        m.catalog.orders.recent.Push(49 - i)
        m.catalog.orders.az.Push(i)
    end for
    m.top = { request: { serial: 1, query: "", area: "", category: "", sort: "recommended", page: 0 } }
    LoadPage()
    check(m.top.result.total = 50, "all fixture videos included")
    check(m.top.result.items.Count() = 24, "page bounded to 24")
    check(m.top.result.pages = 3, "page count rounds up")
    m.top.request.page = 99
    LoadPage()
    check(m.top.result.page = 2 and m.top.result.items.Count() = 2, "out of range clamps to final page")
    m.top.request.page = -1
    m.top.request.area = "software"
    m.top.request.category = "ruby"
    m.top.request.query = " VIDEO   RUBY "
    LoadPage()
    check(m.top.result.total = 25 and m.top.result.page = 0, "case insensitive multiword search intersects filters")
    m.top.request.sort = "recent"
    LoadPage()
    check(m.top.result.items[0].id = "49", "precomputed sort order applied")
    m.top.request.category = "math"
    LoadPage()
    check(m.top.result.total = 0 and m.top.result.items.Count() = 0, "conflicting filters yield empty results")
    check(m.top.result.pages = 1, "empty results retain safe page count")
    m.top.request = { serial: 9, query: "no-such-result", area: "", category: "", sort: "bad-sort", page: 0 }
    LoadPage()
    check(m.top.result.total = 0 and m.top.result.serial = 9, "no matches and request identity preserved")

    m.catalog = ParseJson(ReadAsciiFile("pkg:/config/hackertube-catalog.json"))
    m.top.request = { serial: 10, query: "", area: "", category: "", sort: "recommended", page: 0 }
    LoadPage()
    check(m.top.result.total = 6454, "entire exported catalog is reachable")
    check(m.top.result.pages = 269, "full catalog pagination")
    m.top.request.query = "vectors 3blue1brown"
    LoadPage()
    found = false
    for each item in m.top.result.items
        if item.id = "fNk_zzaMoSs"
            found = true
        end if
    end for
    check(found, "known playable HackerTube entry is searchable")
    m.top.request.query = ""
    m.top.request.page = 268
    LoadPage()
    check(m.top.result.items.Count() = 22, "last catalog page has remaining 22 entries")
    if m.failures = 0
        print "PASS: catalog filtering and pagination"
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

function IsArray(value as dynamic) as boolean
    return Type(value) = "roArray"
end function

function IsAssociativeArray(value as dynamic) as boolean
    return Type(value) = "roAssociativeArray"
end function
