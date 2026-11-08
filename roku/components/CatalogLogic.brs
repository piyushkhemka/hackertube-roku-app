' Pure query functions: also exercised outside Roku with the actual catalog.
function matchesVideo(row as object, request as object, library as object) as boolean
    if request.mode = "liked" and not library.liked.DoesExist(row.id) then return false
    if request.mode = "later" and not library.later.DoesExist(row.id) then return false
    if request.mode = "related"
        found = false
        for each id in request.ids
            if id = row.id then found = true
        end for
        if not found then return false
    end if
    if request.category <> ""
        found = false
        for each category in row.categories
            if category = request.category then found = true
        end for
        if not found then return false
    end if
    if request.mode = "home"
        if row.recommenders = 0 then return false
        if request.filter = "evergreen" and row.life <> "evergreen" then return false
        if request.filter = "talks" and row.type <> "talk" then return false
    end if
    query = LCase(request.query.Trim())
    if query <> ""
        tokens = query.Tokenize(" ")
        for each token in tokens
            if Instr(1, row.search, token) = 0 then return false
        end for
    end if
    return true
end function

function rankedMatches(index as object, request as object, library as object) as object
    exact = []
    titleMatches = []
    others = []
    query = LCase(request.query.Trim())
    for each row in index
        if matchesVideo(row, request, library)
            if query <> "" and LCase(row.title) = query
                exact.Push(row)
            else if query <> "" and Instr(1, LCase(row.title), query) > 0
                titleMatches.Push(row)
            else
                others.Push(row)
            end if
        end if
    end for
    if request.mode = "home" and request.filter = "recent"
        ' Preserve source order within each year, using no fabricated upload dates.
        years = []
        for each row in others
            if years.Count() = 0
                years.Push(row.lastYear)
            else
                seen = false
                for each year in years
                    if year = row.lastYear then seen = true
                end for
                if not seen then years.Push(row.lastYear)
            end if
        end for
        years.Sort("r")
        sorted = []
        for each year in years
            for each row in others
                if row.lastYear = year then sorted.Push(row)
            end for
        end for
        others = sorted
    end if
    exact.Append(titleMatches)
    exact.Append(others)
    return exact
end function

function pageRows(rows as object, page as integer, pageSize as integer) as object
    total = rows.Count()
    pages = Int((total + pageSize - 1) / pageSize)
    if pages < 1 then pages = 1
    if page < 0 then page = 0
    if page >= pages then page = pages - 1
    result = []
    start = page * pageSize
    finish = start + pageSize - 1
    if finish >= total then finish = total - 1
    if start <= finish
        for i = start to finish
            result.Push(rows[i])
        end for
    end if
    return {items: result, page: page, pages: pages, total: total}
end function

function cardFor(row as object) as object
    return {id: row.id, title: row.title, channel: row.channel, topic: row.topic, kind: "video", score: row.score, recommenders: row.recommenders}
end function
