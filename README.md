# VTB MORE.Tech 4.0 [New Kids on the Court]

## Functionality:

- Scraping news sources
- Deduplicating articles
- Emphasizing news trends
- Making up personal/role news digest

## Backend API Reference:

- https://vtb-moretech2022.herokuapp.com/ - entry point
- https://vtb-moretech2022.herokuapp.com/trends?date=${date} - list of trend news
- https://vtb-moretech2022.herokuapp.com/digest?role=[acc|ceo]&date=${date} - digest news for role
- https://vtb-moretech2022.herokuapp.com/article?id=${val} - article data

**Parameter ${date} should be in form %d.%m.%y**

## Client-bot Example:
[@vtb_moretech2022_newkids_bot](https://telegram.me/vtb_moretech2022_newkids_bot)

## Parsers:

- HTML-parsers (lenta.ru, consultant.ru)
- RSS-parsers (lenta.ru)
- TG-channels parser
