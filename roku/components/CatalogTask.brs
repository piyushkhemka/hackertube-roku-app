sub init()
    m.top.functionName = "runCatalog"
end sub

function readJson(path as string) as dynamic
    text = ReadAsciiFile(path)
    if text = "" then return invalid
    return ParseJson(text)
end function

sub runCatalog()
    port = CreateObject("roMessagePort")
    m.top.ObserveField("request", port)
    clock = CreateObject("roTimespan")
    clock.Mark()
    m.manifest = readJson("pkg:/catalog/catalog-manifest.json")
    m.index = readJson("pkg:/catalog/index.json")
    m.taxonomy = readJson("pkg:/catalog/taxonomy.json")
    if m.manifest = invalid or m.index = invalid or m.taxonomy = invalid
        m.top.response = {id: 0, kind: "error", message: "The bundled catalog could not be read. Reinstall the app ZIP."}
        return
    end if
    if m.manifest.schemaVersion <> 1 or m.index.Count() <> m.manifest.count
        m.top.response = {id: 0, kind: "error", message: "Catalog version or record count is invalid. Reinstall the app ZIP."}
        return
    end if
    m.byId = {}
    m.categoryCounts = {}
    m.areaCounts = {}
    m.categoryArea = {}
    for each area in m.taxonomy.areas
        m.areaCounts[area.id] = 0
        for each category in area.categories
            m.categoryCounts[category.id] = 0
            m.categoryArea[category.id] = area.id
        end for
    end for
    for each row in m.index
        m.byId[row.id] = row
        areas = {}
        for each category in row.categories
            m.categoryCounts[category] = m.categoryCounts[category] + 1
            areas[m.categoryArea[category]] = true
        end for
        for each area in areas
            m.areaCounts[area] = m.areaCounts[area] + 1
        end for
    end for
    m.registry = CreateObject("roRegistrySection", "HackerTubeLibrary")
    m.library = {liked: {}, later: {}}
    warning = ""
    if m.registry.Exists("v1")
        saved = ParseJson(m.registry.Read("v1"))
        if Type(saved) = "roAssociativeArray"
            for each name in ["liked", "later"]
                if Type(saved[name]) = "roAssociativeArray"
                    for each id in saved[name]
                        if m.byId.DoesExist(id) then m.library[name][id] = true
                    end for
                end if
            end for
        else
            warning = "Saved lists could not be read. The catalog is available; your next save will start new lists."
        end if
    end if
    m.cachedShard = -1
    m.details = invalid
    print "CATALOG loaded "; m.index.Count(); " videos in "; clock.TotalMilliseconds(); "ms"
    m.top.response = {id: 0, kind: "ready", manifest: m.manifest, library: m.library, warning: warning}
    while true
        event = Wait(0, port)
        if Type(event) = "roSGNodeEvent"
            request = event.GetData()
            if Type(request) = "roAssociativeArray"
                response = handleRequest(request)
                response.id = request.id
                response.library = m.library
                m.top.response = response
            end if
        end if
    end while
end sub

function handleRequest(request as object) as object
    if request.mode = "detail"
        if not m.byId.DoesExist(request.vid) then return {kind: "error", message: "This video is not in the bundled catalog."}
        shard = m.byId[request.vid].shard
        if shard <> m.cachedShard
            m.details = readJson("pkg:/catalog/details/" + shard.ToStr() + ".json")
            m.cachedShard = shard
        end if
        if m.details = invalid then return {kind: "error", message: "Video details could not be loaded."}
        if not m.details.DoesExist(request.vid) then return {kind: "error", message: "Video details are missing."}
        return {kind: "detail", video: m.details[request.vid]}
    else if request.mode = "toggle"
        if request.list <> "liked" and request.list <> "later" then return {kind: "error", message: "Invalid saved list."}
        if not m.byId.DoesExist(request.vid) then return {kind: "error", message: "Unknown video."}
        candidate = ParseJson(FormatJson(m.library))
        if candidate[request.list].DoesExist(request.vid)
            candidate[request.list].Delete(request.vid)
        else
            candidate[request.list][request.vid] = true
        end if
        encoded = FormatJson(candidate)
        if Len(encoded) > 12000 then return {kind: "error", message: "Saved lists are full. Remove a saved video and try again."}
        if not m.registry.Write("v1", encoded) then return {kind: "error", message: "Could not save on this Roku. Your lists have not changed."}
        if not m.registry.Flush()
            m.registry.Write("v1", FormatJson(m.library))
            return {kind: "error", message: "Roku storage could not be saved. Please try again."}
        end if
        m.library = candidate
        return {kind: "saved"}
    else if request.mode = "clear"
        if not m.registry.Write("v1", FormatJson({liked: {}, later: {}})) then return {kind: "error", message: "Could not clear saved lists."}
        if not m.registry.Flush() then return {kind: "error", message: "Could not save cleared lists."}
        m.library = {liked: {}, later: {}}
        return {kind: "cleared"}
    end if
    if request.mode = "areas"
        rows = []
        for each area in m.taxonomy.areas
            rows.Push({id: area.id, title: area.name, channel: area.categories.Count().ToStr() + " topics", topic: m.areaCounts[area.id].ToStr() + " videos", kind: "area"})
        end for
    else if request.mode = "topics"
        rows = []
        for each area in m.taxonomy.areas
            if area.id = request.area
                for each category in area.categories
                    rows.Push({id: category.id, title: category.name, channel: m.categoryCounts[category.id].ToStr() + " videos", topic: area.name, kind: "topic"})
                end for
            end if
        end for
    else
        rows = rankedMatches(m.index, request, m.library)
    end if
    result = pageRows(rows, request.page, 6)
    cards = []
    for each row in result.items
        if row.DoesExist("kind")
            cards.Push(row)
        else
            cards.Push(cardFor(row))
        end if
    end for
    result.items = cards
    result.kind = "page"
    return result
end function
