theme: /

    state: newNode_0
        HttpRequest:
            url = https://vtb-moretech2022.herokuapp.com/news?user_id=10
            method = GET
            body = 
            okState = /newNode_1
            timeout = 0
            headers = []
            vars = [{"name":"news","value":"$session.httpResponse"},{"name":"article_id0","value":"$session.news[0][\"article_id\"]"},{"name":"article_id1","value":"$session.news[1][\"article_id\"]"},{"name":"article_id2","value":"$session.news[2][\"article_id\"]"}]

    state: newNode_1
        a:  1. {{$session.news[0]["topic"]}}
            2. {{$session.news[1]["topic"]}}
            3. {{$session.news[2]["topic"]}} || html = "<span style=\"background-color: var(--white); letter-spacing: 0px;\">1. {{$session.news[0][\"topic\"]}}</span><br><span style=\"background-color: var(--white); letter-spacing: 0px;\">2. {{$session.news[1][\"topic\"]}}</span><br><span style=\"background-color: var(--white); letter-spacing: 0px;\">3. {{$session.news[2][\"topic\"]}}</span><br>", htmlEnabled = false
        buttons:
            "1" -> /newNode_2
            "2" -> /newNode_3
            "3" -> /newNode_4
            "дальше" -> /newNode_0
            {text: "наш сайт", url: "https://vtb-moretech2022.herokuapp.com/"}

    state: newNode_2
        HttpRequest:
            url = https://vtb-moretech2022.herokuapp.com/article?article_id=${article_id0}
            method = GET
            body = 
            okState = /newNode_5
            errorState = /newNode_6
            timeout = 0
            headers = []
            vars = [{"name":"article","value":"$session.httpResponse"}]

    state: newNode_3
        HttpRequest:
            url = https://vtb-moretech2022.herokuapp.com/article?article_id=${article_id1}
            method = GET
            body = 
            okState = /newNode_5
            errorState = /newNode_6
            timeout = 0
            headers = []
            vars = [{"name":"article","value":"$session.httpResponse"}]

    state: newNode_4
        HttpRequest:
            url = https://vtb-moretech2022.herokuapp.com/article?article_id=${article_id2}
            method = GET
            body = 
            okState = /newNode_5
            errorState = /newNode_6
            timeout = 0
            headers = []
            vars = [{"name":"article","value":"$session.httpResponse"}]

    state: newNode_5
        a: {{$session.article["content"]}}
        # Transition /newNode_8
        go!: /newNode_1

    state: newNode_6
        a: ошибка
        # Transition /newNode_7
        go!: /newNode_1